from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import datetime
import os
import sys
import requests
import json
import asyncio

# 確保不論從專案根目錄（uvicorn src.server:app）或 src/（python src/server.py）
# 啟動，都能找到 src/lib 套件。
_SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

from lib.UnifiedAgent import UnifiedAgent
from lib.calendar_utils import real_google_calendar_create_event
from lib import room_store

app = FastAPI(title="NKUST AI Agent Streaming Suite")

# --- 工具函式 ---
def discord_send_message(content: str):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url: return "⚠️ 未設定 Webhook，已模擬。"
    try:
        requests.post(webhook_url, json={"content": content})
        return "✅ Discord 訊息發送成功！"
    except: return "❌ Discord 失敗。"

def get_room_status():
    """查詢所有會議室狀態與已登記時段（含時間、人數）。"""
    lines = ["目前會議室狀態："]
    for r in room_store.list_rooms_with_bookings():
        lines.append(f"- {r['name']} ({r['id']})：容納 {r['capacity']} 人")
        if r["bookings"]:
            for b in r["bookings"]:
                lines.append(
                    f"    🔴 {b['start_time']}~{b['end_time']}｜"
                    f"{b['user_name']}｜{b['meeting_name']}｜與會 {b['attendees']} 人"
                )
        else:
            lines.append("    🟢 目前無預約")
    return "\n".join(lines)

def book_room_local(
    room_id: str,
    user_name: str,
    meeting_name: str,
    start_time: str,
    end_time: str,
    attendees: str = "1",
):
    """
    登記會議室時段。
    Args:
        room_id: 房間 ID（如 A101）。
        user_name: 預約人姓名。
        meeting_name: 會議名稱。
        start_time: 開始時間，格式 'YYYY-MM-DD HH:MM'。
        end_time: 結束時間，格式 'YYYY-MM-DD HH:MM'。
        attendees: 與會人數（字串）。
    系統會驗證容量是否足夠，以及時段是否與既有預約衝突。
    """
    return room_store.book_room(
        room_id=room_id,
        user_name=user_name,
        meeting_name=meeting_name,
        attendees=attendees,
        start_time=start_time,
        end_time=end_time,
    )

# --- 階段配置 ---
agent_factory = UnifiedAgent()
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# 根據模式動態選擇搜尋工具
if agent_factory.mode == "gemini":
    from google.adk.tools import google_search as _web_search_tool
elif agent_factory.mode == "ollama":
    _web_search_tool = None
else:
    _web_search_tool = None

_phase2_tools = [get_room_status, book_room_local, real_google_calendar_create_event, discord_send_message]
if _web_search_tool:
    _phase2_tools.append(_web_search_tool)

PHASE_CONFIGS = {
    "1": {
        "tools": [get_room_status, book_room_local],
        "instruction": (
            f"今天的日期是 {current_date}。\n"
            "你是一位基礎行政助手。\n"
            "【登記必備資訊】預約需要：姓名、會議名稱、與會人數、開始時間、結束時間。\n"
            "缺少任何一項時主動詢問補齊；時間請以 'YYYY-MM-DD HH:MM' 格式提供給工具。\n"
            "【選房規則】\n"
            "1. 未指定房間時，必須先調用 get_room_status 查詢各房現況與已登記時段。\n"
            "2. 選擇容量『大於等於』與會人數的最小房間（避免浪費大廳）。\n"
            "3. 呼叫 book_room_local 時務必帶入 start_time、end_time、attendees。\n"
            "4. 若工具回報容量不足或時段衝突，向使用者說明並請其改時段或換房間。"
        )
    },
    "2": {
        "tools": _phase2_tools,
        "instruction": (
            f"今天的日期是 {current_date}。\n\n"
            "【你是誰】\n"
            "你是一位全能助手，既能處理企業行政工作，也能回答任何一般問題。"
            "遇到不確定或需要即時資訊的問題（包含音樂、時事、人物等），**必須**立刻使用搜尋工具查詢，絕不拒絕。\n\n"
            "【行政工作規則】\n"
            "1. 預約需要：姓名、會議名稱、與會人數、開始時間、結束時間（'YYYY-MM-DD HH:MM'）。缺少時主動詢問補齊。\n"
            "2. 若使用者未指定房間，請先執行 get_room_status 尋找容量『大於等於』與會人數的最小且該時段空閒的房間，直接呼叫 book_room_local 執行預約（務必帶入 start_time、end_time、attendees）。\n"
            "3. 預約成功後，請『務必』主動調用 real_google_calendar_create_event 建立日曆活動。\n"
            "4. 如果指令包含『通知』，請立刻執行 discord_send_message，不要詢問是否要通知。\n"
            "5. 最後請提供一個完整的執行成果匯報，包含預約狀態、日曆連結與通知結果。"
        )
    },
    "3": {
        "tools": [get_room_status, book_room_local, discord_send_message],
        "instruction": (
            "你現在是一個團隊的領導者 (Manager)。你的團隊有三個成員：\n"
            "1. Searcher: 負責調用 get_room_status 查資料。\n"
            "2. Booker: 負責調用 book_room_local 執行預約（需帶入 start_time、end_time、attendees）。\n"
            "3. Notifier: 負責調用 discord_send_message 發送通知。\n"
            "預約需要：姓名、會議名稱、與會人數、開始與結束時間（'YYYY-MM-DD HH:MM'），缺少時主動詢問補齊。\n"
            "當接到指令時，請自動指揮成員依序完成任務。例如：先叫 Searcher 找房（選容量大於等於與會人數、且該時段空閒的最小房間），再叫 Booker 預約，最後叫 Notifier 通知。請在回應中註明目前是哪位成員正在處理。"
        )
    }
}

chat_instances = {}

def get_chat_instance(phase: str):
    if phase not in chat_instances:
        config = PHASE_CONFIGS.get(phase, PHASE_CONFIGS["1"])
        chat_instances[phase] = agent_factory.create_chat(config["instruction"], config["tools"])
    return chat_instances[phase]

# --- API Endpoints ---
class ChatRequest(BaseModel):
    message: str
    phase: str

class BookRequest(BaseModel):
    room_id: str
    user_name: str
    meeting_name: str
    start_time: str
    end_time: str
    attendees: str = "1"

@app.get("/rooms")
async def get_rooms(): return room_store.list_rooms_with_bookings()

@app.post("/book")
async def book_room_endpoint(request: BookRequest):
    message = book_room_local(
        request.room_id,
        request.user_name,
        request.meeting_name,
        request.start_time,
        request.end_time,
        request.attendees,
    )
    return {"message": message}

@app.post("/reset")
async def reset_db():
    global chat_instances
    room_store.reset()
    chat_instances = {}
    return {"status": "success"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    async def event_generator():
        try:
            agent_chat = get_chat_instance(request.phase)
            # 使用產生器獲取串流
            for part in agent_chat.send_message(request.message):
                # 每個 chunk 都以 JSON 格式發送，後面加換行符號
                yield json.dumps(part) + "\n"
                await asyncio.sleep(0.1) # 稍微延遲讓 UI 更有「感」
        except Exception as e:
            yield json.dumps({"type": "error", "content": str(e)}) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")

# 生產環境：掛載 Vite build 產物（開發時由 Vite dev server 處理）
_dist = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist')
if os.path.isdir(_dist):
    app.mount("/", StaticFiles(directory=_dist, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
