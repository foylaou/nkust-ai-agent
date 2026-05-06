import os
from dotenv import load_dotenv

from lib.GeminiADKWrapper import GeminiADKWrapper
from lib.OllamaChatWrapper import OllamaChatWrapper
from lib.OpenAIChatWrapper import OpenAIChatWrapper

load_dotenv()


# ==========================================
# Agent 工廠與包裝器 (Wrapper) 區塊
# ==========================================

class UnifiedAgent:
    """
    統一介面的 Agent 工廠類別，支援 Gemini、Ollama 與 OpenAI 模型。

    根據環境變數 `AGENT_MODE` 決定使用的底層模型與對應的設定。
    提供單一進入點建立聊天會話 (Chat)，屏蔽不同底層模型的差異。
    """

    def __init__(self):
        # 讀取並設定 Agent 運作模式，預設為 'gemini'
        self.mode = os.getenv("AGENT_MODE", "gemini").lower()
        env_model = os.getenv("MODEL_NAME")

        if self.mode == "gemini":
            # Gemini 模式設定
            self.model = env_model or "gemini-2.0-flash"
            print(f"✨ 目前模式：Gemini Online ({self.model})")

        elif self.mode == "openai":
            # OpenAI 模式設定
            self.model = env_model or "gpt-4o-mini"
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
            self.openai_base_url = os.getenv("OPENAI_BASE_URL")
            print(f"🤖 目前模式：OpenAI ({self.model})")

        else:
            # Ollama 本地模式設定
            self.model = env_model or "gemma2"
            self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
            self.ollama_api_key = os.getenv("OLLAMA_API_KEY")
            print(f"🦙 目前模式：Ollama Local ({self.model}) @ {self.ollama_url}")

    def create_chat(self, system_instruction, tools, sub_agents=None):
        """
        根據當前模式建立對應的聊天會話物件 (Chat Wrapper)。

        會自動將當前日期加入到系統指令 (system_instruction) 的開頭，
        幫助模型了解當前時間。

        Args:
            system_instruction (str): 給予模型的角色扮演或規則提示。
            tools (list): 允許模型呼叫的 Python 函式列表。
            sub_agents (list, optional): ADK 子 Agent 列表（僅 Gemini 模式支援）。

        Returns:
            object: 實作了 `send_message` 方法的 Chat Wrapper 實例。
        """
        from datetime import date
        # 將今天的日期注入到系統指令中
        dated_instruction = f"今天是 {date.today().strftime('%Y年%m月%d日')}。\n\n{system_instruction}"

        # 根據模式回傳對應的 Wrapper 實例
        if self.mode == "gemini":
            return GeminiADKWrapper(self.model, dated_instruction, tools, sub_agents=sub_agents)

        elif self.mode == "openai":
            if sub_agents:
                print("⚠️  OpenAI 模式不支援 sub_agents，請改用 Gemini 模式。")
            return OpenAIChatWrapper(self.model, dated_instruction, tools,
                                     api_key=self.openai_api_key,
                                     base_url=self.openai_base_url)

        else:  # ollama
            if sub_agents:
                print("⚠️  Ollama 模式不支援 sub_agents，請改用 Gemini 模式。")
            return OllamaChatWrapper(self.model, dated_instruction, tools,
                                     host=self.ollama_url, api_key=self.ollama_api_key)
