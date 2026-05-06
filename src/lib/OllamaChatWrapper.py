import inspect
from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()


class OllamaChatWrapper:
    """
    Ollama API 的包裝器。

    提供與 OpenAI 類似的工具調用自動處理邏輯與串流文字輸出，
    讓本地端的 Ollama 模型也能具備 Function Calling能力。
    """

    def __init__(self, model, system_instruction, tools_list, host=None, api_key=None):
        self.model = model
        # 初始化對話歷史
        self.messages = [{'role': 'system', 'content': system_instruction}]
        # 轉換工具格式 (Ollama 的工具格式與 OpenAI 相近)
        self.tools = self._convert_tools(tools_list)
        self.tool_map = {f.__name__: f for f in tools_list if inspect.isfunction(f)}

        import ollama
        headers = {'Authorization': f'Bearer {api_key}'} if api_key else {}
        # 初始化 Ollama Client
        self.client = ollama.Client(host=host or "http://localhost:11434", headers=headers)

    @staticmethod
    def _convert_tools(functions):
        """將 Python 函式轉換為 Ollama 支援的 JSON Schema 格式。"""
        ollama_tools = []
        for f in functions:
            if not inspect.isfunction(f):
                continue
            sig = inspect.signature(f)
            params = {
                'type': 'object',
                'properties': {
                    name: {'type': 'string', 'description': ''}
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

    def send_message(self, prompt_text):
        """
        發送訊息並處理工具循環，最後以產生器方式回傳過程與最終結果。
        """
        # 將使用者輸入加入歷史紀錄
        self.messages.append({'role': 'user', 'content': prompt_text})

        # 處理工具調用的迴圈
        while True:
            # 1. 呼叫 Ollama API (非串流)
            response = self.client.chat(model=self.model, messages=self.messages, tools=self.tools)

            # 2. 檢查模型是否發出工具調用請求
            tool_calls = response.get('message', {}).get('tool_calls')

            if tool_calls:
                # 將模型的請求訊息存入歷史紀錄
                self.messages.append(response['message'])

                # 逐一執行工具
                for tool in tool_calls:
                    func_name = tool['function']['name']
                    args = tool['function']['arguments']

                    log_entry = f"🛠️ [Local Reasoning] 調用工具: {func_name}({args})"
                    print(f"  {log_entry}")
                    yield {"type": "log", "content": log_entry}

                    # 執行實際的 Python 函式
                    if func_name in self.tool_map:
                        try:
                            result = self.tool_map[func_name](**args)
                        except Exception as tool_err:
                            result = f"工具執行出錯: {str(tool_err)}"

                        # 將執行結果加入歷史紀錄
                        self.messages.append({
                            'role': 'tool',
                            'content': str(result),
                            'name': func_name
                        })
                # 進入下一輪，讓模型看著執行結果決定下一步
                continue

            else:
                # 3. 處理最終的純文字回應
                content = response.get('message', {}).get('content', "").strip()
                print(content)

                # 如果模型執行完工具後沒有回傳任何文字，主動提示它進行彙整
                if not content:
                    self.messages.append({'role': 'user', 'content': "請彙整以上執行結果並回報給我。"})

                # 使用串流模式重新呼叫，獲得打字機效果
                full_content = ""
                stream = self.client.chat(model=self.model, messages=self.messages, stream=True, tools=self.tools)

                for chunk_res in stream:
                    delta = chunk_res.get('message', {}).get('content', "")
                    if delta:
                        full_content += delta
                        yield {"type": "delta", "content": delta}

                # 儲存最終組裝的結果
                self.messages.append({'role': 'assistant', 'content': full_content})
                yield {"type": "final", "content": ""}

                # 結束迴圈
                return
