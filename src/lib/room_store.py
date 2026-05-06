"""
room_store — 會議室登記的 SQLite 持久層（共用 src/data/app.db）。

特性：
  - 零安裝（Python 內建 sqlite3）、檔案持久化，重啟伺服器登記仍在。
  - 支援同一會議室「多時段」預約，登記時檢查容量與時間衝突。

時間格式統一為字串 'YYYY-MM-DD HH:MM'，因為固定寬度的字典序剛好等於時間序，
直接用字串比較即可判斷時段重疊，簡單可靠。
"""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone

# 預設座位（首次啟動時 seed）
_DEFAULT_ROOMS = [
    ("A101", "創意腦力室", 6),
    ("B202", "大型會議廳", 20),
    ("C303", "焦點小組室", 4),
]


def _default_db_path() -> str:
    """與 UnifiedMemoryService 共用同一顆 SQLite 檔。"""
    env_path = os.environ.get("SQLITE_DB_PATH")
    if env_path:
        return env_path
    # __file__ = .../src/lib/room_store.py → src/data/app.db
    src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(src_dir, "data", "app.db")


_DB_PATH = _default_db_path()

_CREATE_ROOMS = """
    CREATE TABLE IF NOT EXISTS rooms (
        id        TEXT PRIMARY KEY,
        name      TEXT NOT NULL,
        capacity  INTEGER NOT NULL
    );
"""

_CREATE_BOOKINGS = """
    CREATE TABLE IF NOT EXISTS bookings (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id       TEXT    NOT NULL,
        user_name     TEXT    NOT NULL,
        meeting_name  TEXT    NOT NULL,
        attendees     INTEGER NOT NULL,
        start_time    TEXT    NOT NULL,
        end_time      TEXT    NOT NULL,
        created_at    TEXT    NOT NULL
    );
"""


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """建表並在 rooms 為空時 seed 預設會議室。"""
    os.makedirs(os.path.dirname(_DB_PATH), exist_ok=True)
    conn = _get_conn()
    try:
        with conn:
            conn.execute(_CREATE_ROOMS)
            conn.execute(_CREATE_BOOKINGS)
            count = conn.execute("SELECT COUNT(*) FROM rooms").fetchone()[0]
            if count == 0:
                conn.executemany(
                    "INSERT INTO rooms (id, name, capacity) VALUES (?, ?, ?)",
                    _DEFAULT_ROOMS,
                )
    finally:
        conn.close()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def list_rooms_with_bookings() -> list[dict]:
    """
    回傳每間會議室 + 其所有預約時段。
    為了與舊前端相容，另附 derived 的 status/booked_by/meeting_name
    （取「最近一筆」預約做為代表狀態）。
    """
    conn = _get_conn()
    try:
        rooms = conn.execute(
            "SELECT id, name, capacity FROM rooms ORDER BY id"
        ).fetchall()
        result = []
        for room in rooms:
            bookings = conn.execute(
                """
                SELECT id, user_name, meeting_name, attendees, start_time, end_time
                FROM   bookings
                WHERE  room_id = ?
                ORDER BY start_time
                """,
                (room["id"],),
            ).fetchall()
            booking_list = [dict(b) for b in bookings]
            latest = booking_list[-1] if booking_list else None
            result.append({
                "id": room["id"],
                "name": room["name"],
                "capacity": room["capacity"],
                "bookings": booking_list,
                # ── 向後相容欄位 ──
                "status": "Booked" if booking_list else "Available",
                "booked_by": latest["user_name"] if latest else None,
                "meeting_name": latest["meeting_name"] if latest else None,
            })
        return result
    finally:
        conn.close()


def _validate_time(start_time: str, end_time: str) -> str | None:
    """回傳錯誤訊息字串，正確則回 None。"""
    fmt = "%Y-%m-%d %H:%M"
    try:
        start = datetime.strptime(start_time, fmt)
        end = datetime.strptime(end_time, fmt)
    except ValueError:
        return "❌ 時間格式錯誤，請使用 'YYYY-MM-DD HH:MM'（例如 2026-06-10 14:00）。"
    if end <= start:
        return "❌ 結束時間必須晚於開始時間。"
    return None


def book_room(
    room_id: str,
    user_name: str,
    meeting_name: str,
    attendees: int,
    start_time: str,
    end_time: str,
) -> str:
    """
    登記一個會議室時段。會檢查：房間存在、容量足夠、時段不與既有預約重疊。
    成功回傳 ✅ 訊息，失敗回傳 ❌ 訊息。
    """
    try:
        count = int(attendees)
    except (ValueError, TypeError):
        count = 1
    if count < 1:
        count = 1

    time_err = _validate_time(start_time, end_time)
    if time_err:
        return time_err

    conn = _get_conn()
    try:
        room = conn.execute(
            "SELECT id, name, capacity FROM rooms WHERE id = ?", (room_id,)
        ).fetchone()
        if room is None:
            return "❌ 預約失敗：找不到該會議室 ID，請先查詢確認正確的房間 ID。"

        if room["capacity"] < count:
            return (
                f"❌ 預約失敗：{room['name']} 容量僅 {room['capacity']} 人，"
                f"無法容納 {count} 位與會者，請改選容量更大的房間。"
            )

        # 時段重疊：存在既有預約滿足 NOT(新結束<=既有開始 OR 新開始>=既有結束)
        clash = conn.execute(
            """
            SELECT user_name, start_time, end_time
            FROM   bookings
            WHERE  room_id = ?
              AND  NOT (? <= start_time OR ? >= end_time)
            ORDER BY start_time
            LIMIT 1
            """,
            (room_id, end_time, start_time),
        ).fetchone()
        if clash is not None:
            return (
                f"❌ 預約失敗：{room['name']} 在 {clash['start_time']}~{clash['end_time']} "
                f"已被 {clash['user_name']} 預約，時段衝突，請改選其他時段或房間。"
            )

        with conn:
            conn.execute(
                """
                INSERT INTO bookings
                    (room_id, user_name, meeting_name, attendees, start_time, end_time, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (room_id, user_name, meeting_name, count, start_time, end_time, _now_iso()),
            )
        return (
            f"✅ 成功預約 {room['name']}（容量 {room['capacity']} 人）："
            f"{start_time}~{end_time}，與會 {count} 人，會議「{meeting_name}」。"
        )
    finally:
        conn.close()


def reset() -> None:
    """清空所有預約，並重新 seed 預設會議室。"""
    conn = _get_conn()
    try:
        with conn:
            conn.execute("DELETE FROM bookings")
            conn.execute("DELETE FROM rooms")
            conn.executemany(
                "INSERT INTO rooms (id, name, capacity) VALUES (?, ?, ?)",
                _DEFAULT_ROOMS,
            )
    finally:
        conn.close()


# 模組載入時即確保資料表就緒
init_db()
