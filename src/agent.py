import os
import requests
from dotenv import load_dotenv
from src.factory import UnifiedAgent

# 載入 .env
load_dotenv()

# --- 定義 Agent 的工具 (Tools) ---

def get_room_status():
    """查詢辦公室所有會議室的目前狀態。"""
    try:
        response = requests.get("http://localhost:8000/rooms")
        if response.status_code == 200:
            rooms = response.json()
            status_text = "目前會議室狀態如下：\n"
            for r in rooms:
                status = f"🔴 已被 {r['booked_by']} 預約 (會議: {r['meeting_name']})" if r['status'] == "Booked" else "🟢 空閒中"
                status_text += f"- {r['name']} ({r['id']}): 容納 {r['capacity']} 人, 狀態: {status}\n"
            return status_text
        return "無法取得資訊"
    except:
        return "系統連線失敗"

def book_room(room_id: str, user_name: str, meeting_name: str):
    """
    預約指定的會議室。
    
    Args:
        room_id: 會議室識別碼 (如 A101)
        user_name: 預約人姓名
        meeting_name: 會議目的
    """
    try:
        payload = {"room_id": room_id, "user_name": user_name, "meeting_name": meeting_name}
        response = requests.post("http://localhost:8000/book", json=payload)
        return response.json().get("message", "預約失敗")
    except:
        return "連線失敗"

# --- 啟動 Unified Agent ---

def run_agent_chat():
    agent_factory = UnifiedAgent()
    tools = [get_room_status, book_room]
    if agent_factory.mode == "gemini":
        from google.adk.tools import google_search
        tools.append(google_search)
    elif agent_factory.mode == "ollama":
        from src.factory import ollama_web_search
        tools.append(ollama_web_search)

    system_instruction = "你是一位行政助手。請協助預約會議室，如果缺少姓名或會議名稱，請主動詢問。如使用者有最新問題想詢問可以調用search工具"
    
    chat = agent_factory.create_chat(system_instruction, tools)

    print("\n--- 🤖 NKUST Unified Agent 已就緒 ---")
    while True:
        user_input = input("\n👤 您: ")
        if user_input.lower() in ["exit", "quit"]: break
        
        try:
            # 這裡不論是 Gemini 還是 Ollama，都提供統一的 send_message 介面
            response = chat.send_message(user_input)
            
            # 處理回應文字 (Gemini 回傳物件, Ollama Wrapper 回傳字典)
            if hasattr(response, 'text'):
                print(f"🤖 Agent: {response.text}")
            elif isinstance(response, dict):
                print(f"🤖 Agent: {response['content']}")
        except Exception as e:
            print(f"系統錯誤: {str(e)}")

if __name__ == "__main__":
    run_agent_chat()
