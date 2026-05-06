import os
import requests
from dotenv import load_dotenv

from lib.UnifiedAgent import UnifiedAgent

# 載入 .env 檔案中的環境變數
load_dotenv()

# ==========================================
# 基礎工具集 (為多 Agent 協作準備的工具)
# ==========================================

def get_room_status():
    """
    查詢會議室狀態的工具函式。
    
    向本地伺服器請求所有房間目前的預約狀態，通常由團隊中負責
    「查詢/檢查」的角色 (如 Searcher) 來呼叫。
    
    Returns:
        str: 會議室狀態的 JSON 字串，或連線失敗提示。
    """
    try:
        response = requests.get("http://localhost:8080/rooms")
        return str(response.json()) if response.status_code == 200 else "無法查詢"
    except:
        return "本地系統連線失敗"

def book_room(room_id: str, user_name: str, meeting_name: str):
    """
    執行會議室預約動作的工具函式。
    
    由團隊中負責「執行預約」的角色 (如 Booker) 來呼叫。
    
    Args:
        room_id (str): 要預約的房間 ID。
        user_name (str): 預約人姓名。
        meeting_name (str): 會議名稱。
        
    Returns:
        str: 預約操作的回應訊息。
    """
    try:
        payload = {"room_id": room_id, "user_name": user_name, "meeting_name": meeting_name}
        response = requests.post("http://localhost:8080/book", json=payload)
        return response.json().get("message", "預約失敗")
    except:
        return "連線失敗"

def notify_discord(message: str):
    """
    發送 Discord 通知的工具函式。
    
    將完成的結果或通知發布到設定好的 Discord 頻道中，
    通常由團隊中負責「通知」的角色 (如 Notifier) 來呼叫。
    
    Args:
        message (str): 要發送到 Discord 的訊息內容。
        
    Returns:
        str: 執行結果的狀態訊息，提供給 Agent 參考。
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    # 若沒有設定 Webhook URL，則使用終端機印出模擬發送結果
    if not webhook_url:
        print(f"📡 [Notifier] 正在發送 Discord: {message}")
        return "✅ Discord 通知已發送 (模擬)。"
    
    try:
        # 發送 POST 請求至 Webhook
        requests.post(webhook_url, json={"content": message})
        return "✅ Discord 通知已成功發送。"
    except:
        return "❌ Discord 發送失敗。"


# ==========================================
# 啟動多代理協作展示 (Unified Team Agent)
# ==========================================

def run_team_demo():
    """
    啟動模擬多 Agent 協作的聊天機器人。
    
    透過賦予單一模型一個「團隊領導者」的角色 (System Prompt)，
    讓模型在思考過程中模擬將任務分派給不同的「虛擬團隊成員」
    (Searcher, Booker, Notifier)，並呼叫對應的工具來完成綜合性任務。
    """
    # 建立 UnifiedAgent 實例
    agent_factory = UnifiedAgent()
    
    # 註冊所有需要用到的工具
    tools = [get_room_status, book_room, notify_discord]
    
    # 設定系統指令：這是模擬 Multi-Agent 協作的核心。
    # 透過指令讓大語言模型 (LLM) 進行角色扮演，並結構化其思考與任務指派流程。
    system_instruction = (
        "你現在是一個團隊的領導者 (Manager)。你的團隊有三個成員：\n"
        "1. Searcher: 負責查資料。\n"
        "2. Booker: 負責預約。\n"
        "3. Notifier: 負責發送 Discord 通知。\n"
        "請依序呼叫合適的工具來完成任務。在回應中，請註明目前是哪位成員正在處理。"
    )
    
    # 建立聊天會話物件
    chat = agent_factory.create_chat(system_instruction, tools)

    print("\n--- 👥 NKUST Unified Multi-Agent Team (Discord Edition) 已啟動 ---")
    
    # 進入對話迴圈
    while True:
        user_input = input("\n👑 指令: ")
        
        # 檢查離開指令
        if user_input.lower() in ["exit", "quit"]: 
            break
        
        try:
            # 傳送指令給 Agent 並取得回應
            response = chat.send_message(user_input)
            
            # 處理並輸出 Agent 的回應文字
            if hasattr(response, 'text'):
                print(f"\n{response.text}")
            elif isinstance(response, dict):
                print(f"\n{response['content']}")
        except Exception as e:
            # 捕捉並顯示錯誤
            print(f"錯誤: {str(e)}")

# 當作為主程式執行時，啟動團隊展示
if __name__ == "__main__":
    run_team_demo()
