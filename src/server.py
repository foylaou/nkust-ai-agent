from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
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

def book_room_local(room_id: str, user_name: str, meeting_name: str):
    for room in rooms_db:
        if room["id"] == room_id:
            if room["status"] == "Booked": return "該房間已被預約。"
            room["status"] = "Booked"
            room["booked_by"] = user_name
            room["meeting_name"] = meeting_name
            return f"成功預約 {room['name']}！"
    return "找不到該會議室。"

# --- 階段配置 ---
agent_factory = UnifiedAgent()
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

PHASE_CONFIGS = {
    "1": { 
        "tools": [get_room_status, book_room_local], 
        "instruction": "你是一位基礎行政助手。當使用者要求預約但未指定房間時，請務必先調用 get_room_status 查詢空房，並根據人數需求（如 20 人）主動挑選合適的房間進行預約。若缺少姓名或會議名稱才主動詢問。" 
    },
    "2": { 
        "tools": [get_room_status, book_room_local, real_google_calendar_create_event, discord_send_message], 
        "instruction": (
            f"你是一位高效率的企業行政助手。今天的日期是 {current_date}。\n"
            "【核心規則】\n"
            "1. 若使用者未指定房間，請先執行 get_room_status 尋找符合人數需求的空房，並直接執行預約，不要詢問使用者要哪一間。\n"
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
            "當接到指令時，請自動指揮成員依序完成任務。例如：先叫 Searcher 找房，再叫 Booker 預約，最後叫 Notifier 通知。請在回應中註明目前是哪位成員正在處理。"
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

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    clean_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>NKUST AI Agent Streaming Suite</title>
        <style>
            :root { --primary: #1a73e8; --bg: #f8f9fa; --card: #ffffff; }
            body { font-family: 'Segoe UI', sans-serif; background: var(--bg); margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; }
            .section { width: 100%; max-width: 900px; background: var(--card); border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); padding: 25px; margin-bottom: 20px; }
            h2 { color: var(--primary); margin-top: 0; }
            .room-container { display: flex; gap: 15px; justify-content: space-around; flex-wrap: wrap; }
            .room-card { border: 1px solid #ddd; border-radius: 10px; padding: 15px; width: 200px; text-align: center; border-top: 5px solid #ccc; }
            .room-card.booked { border-top-color: #ea4335; background: #fff5f5; }
            .room-card.available { border-top-color: #34a853; background: #f5fff5; }
            hr { width: 100%; max-width: 900px; border: 0; border-top: 2px dashed #ccc; margin: 20px 0; }
            #chat-box { height: 400px; overflow-y: auto; border: 1px solid #eee; padding: 15px; display: flex; flex-direction: column; gap: 10px; background: #fafafa; border-radius: 8px; }
            .msg { max-width: 80%; padding: 10px 15px; border-radius: 18px; font-size: 14px; line-height: 1.5; }
            .msg.user { align-self: flex-end; background: var(--primary); color: white; border-bottom-right-radius: 2px; }
            .msg.agent { align-self: flex-start; background: #e8e8e8; color: #333; border-bottom-left-radius: 2px; white-space: pre-wrap; }
            .msg.tool { align-self: center; background: #fff3cd; color: #856404; font-family: monospace; font-size: 11px; border: 1px solid #ffeeba; text-align: center; width: 90%; }
            .typing { align-self: flex-start; background: #e8e8e8; padding: 12px 16px; border-radius: 18px; display: flex; gap: 4px; }
            .dot { width: 6px; height: 6px; background: #888; border-radius: 50%; animation: bounce 1.4s infinite ease-in-out; }
            @keyframes bounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1.0); } }
            .input-area { display: flex; gap: 10px; margin-top: 15px; }
            input, select { padding: 10px; border-radius: 8px; border: 1px solid #ddd; outline: none; }
            input { flex-grow: 1; }
            button { background: var(--primary); color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="section">
            <h2>🏢 企業行政會議室看板</h2>
            <div id="room-list" class="room-container">載入中...</div>
        </div>
        <hr>
        <div class="section">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h2>🤖 AI 行政助手</h2>
                <button onclick="resetAll()" style="background:#666; font-size:12px;">重置 Demo</button>
            </div>
            <div style="background: #f1f3f4; padding: 15px; border-radius: 8px; margin-top: 10px;">
                <label>🚀 切換階段：</label>
                <select id="phase-select" onchange="changePhase()">
                    <option value="1">階段一：Local Agent</option>
                    <option value="2">階段二：MCP Power</option>
                    <option value="3">階段三：Multi-Agent</option>
                </select>
            </div>
            <div id="chat-box">
                <div class="msg agent">您好！我是您的 AI 行政助手。</div>
            </div>
            <div class="input-area">
                <input type="text" id="user-input" placeholder="輸入指令..." onkeypress="if(event.key==='Enter') sendMessage()">
                <button onclick="sendMessage()">發送</button>
            </div>
        </div>

        <script>
            let currentPhase = "1";

            function changePhase() {
                currentPhase = document.getElementById('phase-select').value;
                appendMessage('agent', `[系統] 已切換至階段 ${currentPhase}。`);
            }

            async function updateRooms() {
                const res = await fetch('/rooms');
                const rooms = await res.json();
                const container = document.getElementById('room-list');
                container.innerHTML = rooms.map(r => `
                    <div class="room-card ${r.status.toLowerCase()}">
                        <strong>${r.name}</strong><br>
                        <small>${r.id}</small><br>
                        <div style="font-weight:bold; margin-top:5px;">${r.status === 'Booked' ? '🔴 已預約' : '🟢 空閒中'}</div>
                    </div>
                `).join('');
            }

            async function resetAll() {
                await fetch('/reset', {method: 'POST'});
                location.reload();
            }

            function appendMessage(role, text) {
                const box = document.getElementById('chat-box');
                const div = document.createElement('div');
                div.className = `msg ${role}`;
                div.innerText = text;
                box.appendChild(div);
                box.scrollTop = box.scrollHeight;
            }

            function toggleTyping(show) {
                const existing = document.getElementById('typing-indicator');
                if (show && !existing) {
                    const div = document.createElement('div');
                    div.id = 'typing-indicator';
                    div.className = 'typing';
                    div.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
                    document.getElementById('chat-box').appendChild(div);
                } else if (!show && existing) { existing.remove(); }
                document.getElementById('chat-box').scrollTop = document.getElementById('chat-box').scrollHeight;
            }

            async function sendMessage() {
                const input = document.getElementById('user-input');
                const text = input.value.trim();
                if (!text) return;

                appendMessage('user', text);
                input.value = '';
                toggleTyping(true);

                let currentAgentMsgDiv = null;

                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({message: text, phase: currentPhase})
                    });

                    const reader = response.body.getReader();
                    const decoder = new TextDecoder();

                    while (true) {
                        const { value, done } = await reader.read();
                        if (done) break;

                        const chunk = decoder.decode(value);
                        // 處理可能的多個 JSON 片段
                        const lines = chunk.split('\\n').filter(l => l.trim());
                        for (const line of lines) {
                            try {
                                const data = JSON.parse(line);
                                
                                if (data.type === 'log') {
                                    appendMessage('tool', data.content);
                                } else if (data.type === 'delta') {
                                    toggleTyping(false);
                                    if (!currentAgentMsgDiv) {
                                        const box = document.getElementById('chat-box');
                                        currentAgentMsgDiv = document.createElement('div');
                                        currentAgentMsgDiv.className = 'msg agent';
                                        box.appendChild(currentAgentMsgDiv);
                                    }
                                    currentAgentMsgDiv.innerText += data.content;
                                    document.getElementById('chat-box').scrollTop = document.getElementById('chat-box').scrollHeight;
                                } else if (data.type === 'final') {
                                    toggleTyping(false);
                                    if (currentAgentMsgDiv && data.content) {
                                        currentAgentMsgDiv.innerText = data.content;
                                    }
                                } else if (data.type === 'error') {
                                    toggleTyping(false);
                                    appendMessage('agent', '❌ 錯誤: ' + data.content);
                                }
                            } catch (e) {
                                console.error('Parse error:', e);
                            }
                        }
                    }
                    updateRooms();
                } catch (e) {
                    toggleTyping(false);
                    appendMessage('agent', '連線失敗：' + e);
                }
            }

            setInterval(updateRooms, 3000);
            updateRooms();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=clean_html)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
