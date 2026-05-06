import requests
from dotenv import load_dotenv

from lib.UnifiedAgent import UnifiedAgent
from lib.ollama_tools import ollama_web_search

# 載入 .env 檔案中的環境變數
load_dotenv()

# ==========================================
# 定義 Agent 可使用的工具 (Tools)
# ==========================================

def get_room_status():
    """
    查詢辦公室所有會議室的目前狀態。
    
    向本地 API 發送 GET 請求，取得所有會議室的列表，
    並將狀態格式化為易於閱讀的文字回傳給 Agent。
    
    Returns:
        str: 包含所有會議室狀態的格式化字串，若發生錯誤則回傳錯誤訊息。
    """
    try:
        # 向本地伺服器查詢會議室狀態
        response = requests.get("http://localhost:8080/rooms")
        if response.status_code == 200:
            rooms = response.json()
            status_text = "目前會議室狀態如下：\n"
            # 遍歷所有會議室並格式化狀態訊息
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
    
    向本地 API 發送 POST 請求，帶上會議室 ID、預約人姓名與會議名稱來進行預約。
    
    Args:
        room_id (str): 會議室識別碼 (如 A101)。
        user_name (str): 預約人姓名。
        meeting_name (str): 會議目的或名稱。
        
    Returns:
        str: 預約成功或失敗的訊息，供 Agent 回報給使用者。
    """
    try:
        # 準備要傳送的預約資料
        payload = {"room_id": room_id, "user_name": user_name, "meeting_name": meeting_name}
        # 發送 POST 請求進行預約
        response = requests.post("http://localhost:8080/book", json=payload)
        # 回傳 API 提供的訊息，若無則預設為 "預約失敗"
        return response.json().get("message", "預約失敗")
    except:
        return "連線失敗"

# ==========================================
# 整合與啟動 Unified Agent
# ==========================================

def run_agent_chat():
    """
    啟動統一介面的 Agent 聊天機器人。
    
    負責初始化 UnifiedAgent，根據使用的 AI 模型 (Gemini 或 Ollama) 
    動態載入對應的網頁搜尋工具，並設定系統指令與工具，最後進入對話迴圈。
    """
    # 建立 UnifiedAgent 實例
    agent_factory = UnifiedAgent()
    
    # 基本的會議室管理工具列表
    tools = [get_room_status, book_room]
    
    # 根據 agent_factory 的模式，動態加入適用的網頁搜尋工具
    if agent_factory.mode == "gemini":
        from google.adk.tools import google_search
        tools.append(google_search)
    elif agent_factory.mode == "ollama":

        tools.append(ollama_web_search)

    # 設定 Agent 的系統指令 (System Prompt)，告訴 Agent 它的角色與任務
    system_instruction = "你是一位行政助手。請協助預約會議室，如果缺少姓名或會議名稱，請主動詢問。"
    
    # 建立具有系統指令與工具的聊天會話物件
    chat = agent_factory.create_chat(system_instruction, tools)

    print("\n--- 🤖 NKUST Unified Agent 已就緒 ---")
    
    # 進入無限迴圈，等待並處理使用者的輸入
    while True:
        user_input = input("\n👤 您: ")
        
        # 檢查是否為結束指令
        if user_input.lower() in ["exit", "quit"]: 
            break
        
        try:
            # 將使用者輸入傳送給 Agent 進行處理，這裡 UnifiedAgent 提供了一致的 send_message 介面
            response = chat.send_message(user_input)
            
            # 解析並印出 Agent 的回應
            # 如果是 Gemini 模型，回應會有 'text' 屬性
            if hasattr(response, 'text'):
                print(f"🤖 Agent: {response.text}")
            # 如果是自定義的 Ollama Wrapper，回應可能是一個字典，內容在 'content' 鍵下
            elif isinstance(response, dict):
                print(f"🤖 Agent: {response['content']}")
        except Exception as e:
            # 捕捉並印出系統錯誤，避免程式直接崩潰
            print(f"系統錯誤: {str(e)}")

# 當程式被直接執行時，啟動 Agent 聊天功能
if __name__ == "__main__":
    run_agent_chat()
