import os
import requests
from dotenv import load_dotenv
from src.factory import UnifiedAgent

# 載入 .env
load_dotenv()

# --- 基礎工具集 ---

def get_room_status():
    """查詢會議室狀態。"""
    try:
        response = requests.get("http://localhost:8000/rooms")
        return str(response.json()) if response.status_code == 200 else "無法查詢"
    except:
        return "本地系統連線失敗"

def book_room(room_id: str, user_name: str, meeting_name: str):
    """執行預約動作。"""
    try:
        payload = {"room_id": room_id, "user_name": user_name, "meeting_name": meeting_name}
        response = requests.post("http://localhost:8000/book", json=payload)
        return response.json().get("message", "預約失敗")
    except:
        return "連線失敗"

def notify_discord(message: str):
    """發送 Discord 通知。"""
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print(f"📡 [Notifier] 正在發送 Discord: {message}")
        return "✅ Discord 通知已發送 (模擬)。"
    
    try:
        requests.post(webhook_url, json={"content": message})
        return "✅ Discord 通知已成功發送。"
    except:
        return "❌ Discord 發送失敗。"

# --- 啟動 Unified Team Agent ---

def run_team_demo():
    agent_factory = UnifiedAgent()
    
    tools = [get_room_status, book_room, notify_discord]
    system_instruction = (
        "你現在是一個團隊的領導者 (Manager)。你的團隊有三個成員：\n"
        "1. Searcher: 負責查資料。\n"
        "2. Booker: 負責預約。\n"
        "3. Notifier: 負責發送 Discord 通知。\n"
        "請依序呼叫合適的工具來完成任務。在回應中，請註明目前是哪位成員正在處理。"
    )
    
    chat = agent_factory.create_chat(system_instruction, tools)

    print("\n--- 👥 NKUST Unified Multi-Agent Team (Discord Edition) 已啟動 ---")
    while True:
        user_input = input("\n👑 指令: ")
        if user_input.lower() in ["exit", "quit"]: break
        
        try:
            response = chat.send_message(user_input)
            if hasattr(response, 'text'):
                print(f"\n{response.text}")
            elif isinstance(response, dict):
                print(f"\n{response['content']}")
        except Exception as e:
            print(f"錯誤: {str(e)}")

if __name__ == "__main__":
    run_team_demo()
