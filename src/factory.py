import os
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types
import ollama

load_dotenv()

class UnifiedAgent:
    """統一介面的 Agent，支援 Gemini 與 Ollama"""
    def __init__(self):
        self.mode = os.getenv("AGENT_MODE", "gemini").lower()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
        # 優先從環境變數讀取 MODEL_NAME，否則使用預設值
        env_model = os.getenv("MODEL_NAME")
        if self.mode == "gemini":
            self.model = env_model or "gemini-2.0-flash"
            self.client = genai.Client(api_key=self.api_key)
            print(f"✨ 目前模式：Gemini Online ({self.model})")
        else:
            self.model = env_model or "gemma2"
            print(f"🦙 目前模式：Ollama Local ({self.model})")

    def create_chat(self, system_instruction, tools):
        """建立聊天會話"""
        if self.mode == "gemini":
            return self.client.chats.create(
                model=self.model,
                config=types.GenerateContentConfig(
                    tools=tools,
                    system_instruction=system_instruction
                )
            )
        else:
            return OllamaChatWrapper(self.model, system_instruction, tools)

class OllamaChatWrapper:
    """模擬 Gemini Chat 介面的 Ollama 包裝器"""
    def __init__(self, model, system_instruction, tools):
        self.model = model
        self.messages = [{'role': 'system', 'content': system_instruction}]
        # 將 Python 函式轉換為 Ollama 工具格式
        self.tools = self._convert_tools(tools)
        self.tool_map = {f.__name__: f for f in tools}
        self.logs = [] # 新增：用於記錄工具調用日誌

    def _convert_tools(self, functions):
        ollama_tools = []
        for f in functions:
            import inspect
            sig = inspect.signature(f)
            params = {
                'type': 'object',
                'properties': {
                    name: {'type': 'string', 'description': ''} # 簡化版
                    for name in sig.parameters
                },
                'required': list(sig.parameters.keys())
            }
            ollama_tools.append({
                'type': 'function',
                'function': {
                    'name': f.__name__,
                    'description': f.__doc__ or "",
                    'parameters': params
                }
            })
        return ollama_tools

    def send_message(self, user_input):
        """發送訊息並處理工具循環，並以產生器方式回傳過程與最終結果"""
        self.messages.append({'role': 'user', 'content': user_input})
        
        while True:
            # 1. 呼叫 Ollama
            response = ollama.chat(model=self.model, messages=self.messages, tools=self.tools)
            
            # 2. 檢查是否有工具調用 (Tool Calls)
            tool_calls = response.get('message', {}).get('tool_calls')
            
            if tool_calls:
                self.messages.append(response['message'])
                
                for tool in tool_calls:
                    func_name = tool['function']['name']
                    args = tool['function']['arguments']
                    
                    log_entry = f"🛠️ [Local Reasoning] 調用工具: {func_name}({args})"
                    print(f"  {log_entry}")
                    # 即時回傳日誌
                    yield {"type": "log", "content": log_entry}
                    
                    if func_name in self.tool_map:
                        try:
                            result = self.tool_map[func_name](**args)
                        except Exception as e:
                            result = f"工具執行出錯: {str(e)}"
                        
                        self.messages.append({
                            'role': 'tool',
                            'content': str(result),
                            'name': func_name
                        })
                continue
            else:
                # 3. 最終回覆：使用串流模式達到「打字機」效果
                content = response.get('message', {}).get('content', "").strip()
                
                # 如果第一波沒內容（通常是執行完工具後），我們發送總結請求
                if not content:
                    self.messages.append({'role': 'user', 'content': "請彙整以上執行結果並回報給我。"})
                
                full_content = ""
                # 開啟 Ollama 串流
                stream = ollama.chat(model=self.model, messages=self.messages, stream=True, tools=self.tools)
                
                for chunk in stream:
                    delta = chunk.get('message', {}).get('content', "")
                    if delta:
                        full_content += delta
                        # 回傳文字片段
                        yield {"type": "delta", "content": delta}
                
                self.messages.append({'role': 'assistant', 'content': full_content})
                # 發送結束訊號
                yield {"type": "final", "content": ""}
                return

    @property
    def text(self):
        # 讓 .text 屬性在回傳的訊息物件上生效 (模擬 Gemini response)
        # 注意：這個 wrapper 回傳的是訊息物件本身，所以這裡需要一點小技巧
        pass

# 為了讓 response.text 能動，我們定義一個小類別
class UnifiedResponse:
    def __init__(self, content):
        self.text = content
