import os
import requests
import datetime
from dotenv import load_dotenv
from src.factory import UnifiedAgent
from src.calendar_utils import real_google_calendar_create_event

# 載入 .env
load_dotenv()

# --- Discord 工具 ---

def discord_send_message(content: str):
    """
    發送訊息到 Discord 頻道。
    
    Args:
        content: 要發送的訊息內容。
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print(f"📡 [模擬模式] Discord 訊息內容: {content}")
        return "⚠️ 未設定 Webhook URL，已進入模擬模式。"
    
    try:
        payload = {"content": content}
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            return "✅ Discord 訊息發送成功！"
        else:
            return f"❌ Discord 發送失敗: {response.status_code}"
    except Exception as e:
        return f"❌ Discord 連線錯誤: {str(e)}"

# --- 本地工具 ---

def get_room_status():
    """查詢辦公室所有會議室的狀態。"""
    try:
        response = requests.get("http://localhost:8000/rooms")
        return response.json() if response.status_code == 200 else "無法查詢"
    except:
        return "本地系統連線失敗"

def book_room_local(room_id: str, user_name: str, meeting_name: str):
    """預約本機會議室看板上的房間。"""
    try:
        payload = {"room_id": room_id, "user_name": user_name, "meeting_name": meeting_name}
        response = requests.post("http://localhost:8000/book", json=payload)
        return response.json().get("message", "預約失敗")
    except:
        return "本地看板連線失敗"

# --- 整合所有工具 ---
tools = [
    get_room_status, 
    book_room_local, 
    real_google_calendar_create_event, # 使用真實的日曆工具
    discord_send_message
]

def run_mcp_agent():
    agent_factory = UnifiedAgent()
    if agent_factory.mode == "gemini":
        from google.adk.tools import google_search
        tools.append(google_search)
    elif agent_factory.mode == "ollama":
        from src.factory import ollama_web_search
        tools.append(ollama_web_search)
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    system_instruction = (
        f"今天的日期是 {current_date}。\n\n"
        "【你是誰】\n"
        "你是一位全能助手，既能處理企業行政工作，也能回答任何一般問題。"
        "遇到不確定或需要即時資訊時，**必須**使用 web_search 工具，絕不拒絕查詢。\n\n"
        "回答問題時**必須** 使用 繁體中文 回答 拒絕簡體字"
        "【行政工作規則】\n"
        "1. 預約含「通知」或「Discord」→ 預約成功後立即發送 Discord 通知。\n"
        "2. 完成會議室預約後 → 主動建立 Google Calendar 活動，通知中附上日曆連結。\n"
        "3. 缺少姓名或會議名稱 → 主動詢問。\n"
        "4. 所有工具執行完畢後 → 提供完整匯報（預約狀態、日曆結果含連結、Discord 發送狀態）。\n"
    )

    chat = agent_factory.create_chat(system_instruction, tools)

    print("\n--- 🤖 NKUST Unified Enterprise Agent (Google + Discord) ---")
    print("提示：第一次執行日曆功能會彈出瀏覽器授權。")
    
    while True:
        user_input = input("\n🎮 指令: ")
        if user_input.lower() in ["exit", "quit"]: break
        
        try:
            response = chat.send_message(user_input)
            if hasattr(response, 'text'):
                print(f"\n🤖 Agent:\n{response.text}")
            elif isinstance(response, dict):
                print(f"\n🤖 Agent:\n{response['content']}")
        except Exception as e:
            print(f"發生錯誤: {str(e)}")

if __name__ == "__main__":
    run_mcp_agent()
