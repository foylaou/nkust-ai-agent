import os
import requests
import datetime
from dotenv import load_dotenv

from lib.UnifiedAgent import UnifiedAgent
from lib.calendar_utils import real_google_calendar_create_event

# 載入 .env 檔案中的環境變數
load_dotenv()

# ==========================================
# Discord 相關工具
# ==========================================

def discord_send_message(content: str):
    """
    發送訊息到 Discord 頻道。
    
    Args:
        content (str): 要發送的訊息內容。
        
    Returns:
        str: 執行結果的狀態訊息，提供給 Agent 參考。
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    # 若沒有設定 Webhook URL，則進入模擬模式並印出訊息
    if not webhook_url:
        print(f"📡 [模擬模式] Discord 訊息內容: {content}")
        return "⚠️ 未設定 Webhook URL，已進入模擬模式。"
    
    try:
        payload = {"content": content}
        # 發送 POST 請求至 Discord Webhook
        response = requests.post(webhook_url, json=payload)
        
        # 204 No Content 代表請求成功且沒有回傳內容
        if response.status_code == 204:
            return "✅ Discord 訊息發送成功！"
        else:
            return f"❌ Discord 發送失敗: {response.status_code}"
    except Exception as e:
        return f"❌ Discord 連線錯誤: {str(e)}"

# ==========================================
# 本地伺服器相關工具
# ==========================================

def get_room_status():
    """
    查詢辦公室所有會議室的狀態。
    
    Returns:
        dict | str: 會議室狀態的 JSON 資料，或連線失敗的提示訊息。
    """
    try:
        # 向本地 API 獲取房間狀態
        response = requests.get("http://localhost:8080/rooms")
        return response.json() if response.status_code == 200 else "無法查詢"
    except:
        return "本地系統連線失敗"

def book_room_local(room_id: str, user_name: str, meeting_name: str):
    """
    預約本機會議室看板上的房間。
    
    Args:
        room_id (str): 會議室的 ID。
        user_name (str): 預約人姓名。
        meeting_name (str): 會議名稱。
        
    Returns:
        str: 預約成功或失敗的訊息。
    """
    try:
        payload = {"room_id": room_id, "user_name": user_name, "meeting_name": meeting_name}
        # 向本地 API 傳送預約請求
        response = requests.post("http://localhost:8080/book", json=payload)
        return response.json().get("message", "預約失敗")
    except:
        return "本地看板連線失敗"

# ==========================================
# 整合與啟動 Agent
# ==========================================

# 定義給 Agent 使用的工具列表
tools = [
    get_room_status, 
    book_room_local, 
    real_google_calendar_create_event, # 使用真實的日曆工具建立 Google 日曆活動
    discord_send_message
]

def run_mcp_agent():
    """啟動 MCP 聊天機器人代理 (Agent)，設定系統指令與工具並開始對話迴圈。"""
    
    # 建立 UnifiedAgent 實例
    agent_factory = UnifiedAgent()
    
    # 根據不同的 AI 模型模式，動態載入並加入網頁搜尋工具
    if agent_factory.mode == "gemini":
        from google.adk.tools import google_search
        tools.append(google_search)
    elif agent_factory.mode == "ollama":
        from lib.ollama_tools import ollama_web_search
        tools.append(ollama_web_search)
        
    # 取得當前日期，用於系統指令中
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # 設定 Agent 的系統指令 (System Prompt)
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

    # 建立聊天對話 (Chat) 物件
    chat = agent_factory.create_chat(system_instruction, tools)

    print("\n--- 🤖 NKUST Unified Enterprise Agent (Google + Discord) ---")
    print("提示：第一次執行日曆功能會彈出瀏覽器授權。")
    
    # 進入對話輸入迴圈
    while True:
        user_input = input("\n🎮 指令: ")
        # 判斷是否為離開指令
        if user_input.lower() in ["exit", "quit"]: 
            break
        
        try:
            # 傳送使用者輸入給 Agent 並取得回應
            response = chat.send_message(user_input)
            
            # 根據回傳物件的類型，印出對應的回應內容
            if hasattr(response, 'text'):
                print(f"\n🤖 Agent:\n{response.text}")
            elif isinstance(response, dict):
                print(f"\n🤖 Agent:\n{response['content']}")
        except Exception as e:
            print(f"發生錯誤: {str(e)}")

# 當作為主程式執行時，啟動 Agent
if __name__ == "__main__":
    run_mcp_agent()
