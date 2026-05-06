from dotenv import load_dotenv

from lib.UnifiedAgent import UnifiedAgent
from lib.ollama_tools import ollama_web_search

load_dotenv()

# ==========================================
# 本地測試用主程式
# ==========================================
if __name__ == '__main__':
    # 初始化工廠，決定當前 Agent 模式
    agent_factory = UnifiedAgent()

    # 根據不同模式預載入對應的測試工具
    if agent_factory.mode == "gemini":
        from google.adk.tools import google_search
        test_tools = [google_search]
    elif agent_factory.mode == "ollama":
        test_tools = [ollama_web_search]
    else:
        test_tools = []

    # 建立測試用的聊天會話
    chat_session = agent_factory.create_chat("你是一位行政助手，請使用繁體中文跟我對話", test_tools)
    
    # 簡易的命令列對話介面
    while True:
        user_input_text = input("\n👤 您: ")
        if user_input_text.lower() in ["exit", "quit"]: 
            break
            
        try:
            print("🤖 Agent: ", end="", flush=True)
            # 迭代產生器，處理不同類型的輸出
            for chunk_data in chat_session.send_message(user_input_text):
                if chunk_data["type"] == "delta":
                    # 串流文字片段
                    print(chunk_data["content"], end="", flush=True)
                elif chunk_data["type"] == "log":
                    # 工具執行日誌
                    print(f"\n  {chunk_data['content']}", flush=True)
                elif chunk_data["type"] == "error":
                    # 錯誤訊息
                    print(f"\n系統錯誤: {chunk_data['content']}", flush=True)
            print()  # 換行準備下一次對話
        except Exception as main_err:
            print(f"系統錯誤: {str(main_err)}")
