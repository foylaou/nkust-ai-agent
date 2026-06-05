import json
import inspect
from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()


class LiteLLMChatWrapper:
    """
    LiteLLM 的包裝器，透過單一 OpenAI 相容介面接通 100+ 家供應商
    （Anthropic、OpenAI、Gemini、Groq、Ollama…）。

    與 OpenAIChatWrapper 介面一致：
      - send_message 為 generator，yield {"type": log/delta/final/error, "content": str}
      - 自動處理 Function Calling 迴圈與 streaming 輸出

    model 直接使用完整的 litellm 模型字串，例如：
      - "gpt-4o-mini"
      - "anthropic/claude-sonnet-4-5"
      - "gemini/gemini-2.0-flash"
      - "groq/llama-3.3-70b-versatile"
      - "ollama/gemma2"
    各供應商的金鑰走其原生環境變數（ANTHROPIC_API_KEY / OPENAI_API_KEY / GROQ_API_KEY…），
    litellm 會自動讀取；也可用 api_key / base_url 覆寫。
    """

    def __init__(self, model, system_instruction, tools_list, api_key=None, base_url=None):
        self.model = model
        # 初始化對話歷史，放入系統指令
        self.messages = [{'role': 'system', 'content': system_instruction}]
        # 將 Python 函式轉換為 OpenAI 規定的工具格式（litellm 採同一格式）
        self.tools = self._convert_tools(tools_list)
        # 函式名稱 → 實際 Python 函式
        self.tool_map = {f.__name__: f for f in tools_list if inspect.isfunction(f)}

        import litellm
        self._litellm = litellm

        # 額外傳給 litellm.completion 的參數（金鑰 / 自訂端點）
        self._call_kwargs = {}
        if api_key:
            self._call_kwargs['api_key'] = api_key
        if base_url:
            self._call_kwargs['api_base'] = base_url

    @staticmethod
    def _convert_tools(functions):
        """將 Python 函式列表轉換為 Function Calling 需要的 JSON Schema 格式（參數一律視為字串）。"""
        tools = []
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
            tools.append({
                'type': 'function',
                'function': {
                    'name': f.__name__,
                    'description': f.__doc__ or "",
                    'parameters': params
                }
            })
        return tools

    def send_message(self, prompt):
        """
        處理單次對話。自動判斷是否需要呼叫工具，
        工具執行完畢後再次請求模型，直到產生最終文字回應為止（串流輸出）。
        """
        self.messages.append({'role': 'user', 'content': prompt})

        while True:
            # 1. 先以非串流方式呼叫，檢查是否回傳 tool_calls
            response = self._litellm.completion(
                model=self.model,
                messages=self.messages,
                tools=self.tools or None,
                **self._call_kwargs,
            )
            msg = response.choices[0].message

            # 2. 模型決定調用工具
            if getattr(msg, "tool_calls", None):
                # 將模型的調用請求加入歷史（轉成 dict 以相容各家供應商）
                self.messages.append(
                    msg.model_dump() if hasattr(msg, "model_dump") else msg
                )

                for tool_call in msg.tool_calls:
                    func_name = tool_call.function.name
                    try:
                        args = json.loads(tool_call.function.arguments)
                    except (json.JSONDecodeError, TypeError):
                        args = {}

                    log_entry = f"🛠️ [LiteLLM] 調用工具: {func_name}({args})"
                    print(f"  {log_entry}")
                    yield {"type": "log", "content": log_entry}

                    if func_name in self.tool_map:
                        try:
                            result = self.tool_map[func_name](**args)
                        except Exception as func_err:
                            result = f"工具執行出錯: {str(func_err)}"
                    else:
                        result = f"未知工具: {func_name}"

                    self.messages.append({
                        'role': 'tool',
                        'tool_call_id': tool_call.id,
                        'content': str(result),
                    })
                # 工具執行完畢，進入下一回合
                continue

            else:
                # 3. 無工具調用 → 以 streaming 取得打字機效果
                full_content = ""
                stream = self._litellm.completion(
                    model=self.model,
                    messages=self.messages,
                    stream=True,
                    **self._call_kwargs,
                )
                for chunk_res in stream:
                    delta = chunk_res.choices[0].delta.content or ""
                    if delta:
                        full_content += delta
                        yield {"type": "delta", "content": delta}

                self.messages.append({'role': 'assistant', 'content': full_content})
                yield {"type": "final", "content": ""}
                return
