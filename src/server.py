from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import datetime
import os
import requests
import json
import asyncio
from src.factory import UnifiedAgent
from src.calendar_utils import real_google_calendar_create_event

app = FastAPI(title="NKUST AI Agent Streaming Suite")

# --- 模擬資料庫 ---
rooms_db = [
    {"id": "A101", "name": "創意腦力室", "capacity": 6, "status": "Available", "booked_by": None, "meeting_name": None},
    {"id": "B202", "name": "大型會議廳", "capacity": 20, "status": "Available", "booked_by": None, "meeting_name": None},
    {"id": "C303", "name": "焦點小組室", "capacity": 4, "status": "Available", "booked_by": None, "meeting_name": None},
]

# --- 工具函式 ---
def discord_send_message(content: str):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url: return "⚠️ 未設定 Webhook，已模擬。"
    try:
        requests.post(webhook_url, json={"content": content})
        return "✅ Discord 訊息發送成功！"
    except: return "❌ Discord 失敗。"

def get_room_status():
    status_text = "目前會議室狀態：\n"
    for r in rooms_db:
        s = f"🔴 已被 {r['booked_by']} 預約" if r['status'] == "Booked" else "🟢 空閒中"
        status_text += f"- {r['name']} ({r['id']}): {s}\n"
    return status_text

def book_room_local(room_id: str, user_name: str, meeting_name: str, attendees: str = "1"):
    """預約會議室。attendees 為與會人數（字串），系統會驗證容量是否足夠。"""
    try:
        count = int(attendees)
    except ValueError:
        count = 1

    for room in rooms_db:
        if room["id"] == room_id:
            if room["status"] == "Booked":
                return f"❌ 預約失敗：{room['name']} 已被 {room['booked_by']} 預約，請改選其他房間。"
            if room["capacity"] < count:
                return (
                    f"❌ 預約失敗：{room['name']} 容量僅 {room['capacity']} 人，"
                    f"無法容納 {count} 位與會者，請改選容量更大的房間。"
                )
            room["status"] = "Booked"
            room["booked_by"] = user_name
            room["meeting_name"] = meeting_name
            return f"✅ 成功預約 {room['name']}（容量 {room['capacity']} 人，與會 {count} 人）。"
    return "❌ 預約失敗：找不到該會議室 ID，請先調用 get_room_status 確認正確的房間 ID。"

# --- 階段配置 ---
agent_factory = UnifiedAgent()
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# 根據模式動態選擇搜尋工具
if agent_factory.mode == "gemini":
    from google.adk.tools import google_search as _web_search_tool
elif agent_factory.mode == "ollama":
    from src.factory import ollama_web_search as _web_search_tool
else:
    _web_search_tool = None

_phase2_tools = [get_room_status, book_room_local, real_google_calendar_create_event, discord_send_message]
if _web_search_tool:
    _phase2_tools.append(_web_search_tool)

PHASE_CONFIGS = {
    "1": {
        "tools": [get_room_status, book_room_local],
        "instruction": (
            "你是一位基礎行政助手。\n"
            "【選房規則】\n"
            "1. 未指定房間時，必須先調用 get_room_status 查詢空房。\n"
            "2. 選擇容量『大於等於』與會人數的最小空閒房間（避免浪費大廳）。\n"
            "3. 若所有符合容量的房間皆已預約，回報無法預約並說明原因。\n"
            "4. 缺少姓名或會議名稱時才主動詢問，人數已知則直接選房。"
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
            "1. 若使用者未指定房間，請先執行 get_room_status 尋找容量『大於等於』與會人數的最小空閒房間，直接執行預約，不要詢問使用者要哪一間。\n"
            "2. 預約成功後，請『務必』主動調用 real_google_calendar_create_event 建立日曆活動。\n"
            "3. 如果指令包含『通知』，請立刻執行 discord_send_message，不要詢問是否要通知。\n"
            "4. 最後請提供一個完整的執行成果匯報，包含預約狀態、日曆連結與通知結果。"
        )
    },
    "3": { 
        "tools": [get_room_status, book_room_local, discord_send_message], 
        "instruction": (
            "你現在是一個團隊的領導者 (Manager)。你的團隊有三個成員：\n"
            "1. Searcher: 負責調用 get_room_status 查資料。\n"
            "2. Booker: 負責調用 book_room_local 執行預約。\n"
            "3. Notifier: 負責調用 discord_send_message 發送通知。\n"
            "當接到指令時，請自動指揮成員依序完成任務。例如：先叫 Searcher 找房（選容量大於等於與會人數的最小空閒房間），再叫 Booker 預約，最後叫 Notifier 通知。請在回應中註明目前是哪位成員正在處理。"
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

@app.get("/rooms")
async def get_rooms(): return rooms_db

@app.post("/reset")
async def reset_db():
    global chat_instances
    for room in rooms_db:
        room.update({"status": "Available", "booked_by": None, "meeting_name": None})
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
