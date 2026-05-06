import json
import inspect
from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()




class OpenAIChatWrapper:
    """
    OpenAI Chat API 的包裝器。

    支援工具調用 (Function Calling) 自動解析執行，
    以及串流 (Streaming) 輸出文字內容。
    """
    def __init__(self, model, system_instruction, tools_list, api_key=None, base_url=None):
        self.model = model
        # 初始化對話歷史，放入系統指令
        self.messages = [{'role': 'system', 'content': system_instruction}]
        # 將 Python 函式轉換為 OpenAI 規定的工具格式
        self.tools = self._convert_tools(tools_list)
        # 建立函式名稱到實際 Python 函式的映射表，方便後續呼叫
        self.tool_map = {f.__name__: f for f in tools_list if inspect.isfunction(f)}

        from openai import OpenAI
        kwargs = {'api_key': api_key}
        if base_url:
            kwargs['base_url'] = base_url

        # 初始化 OpenAI Client
        self.client = OpenAI(**kwargs)

    @staticmethod
    def _convert_tools(functions):
        """
        將 Python 函式列表轉換為 OpenAI Function Calling 需要的 JSON Schema 格式。

        注意：這裡簡化了參數型別，全部視為字串。若需支援複雜型別需額外處理。
        """
        openai_tools = []
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
            openai_tools.append({
                'type': 'function',
                'function': {
                    'name': f.__name__,
                    'description': f.__doc__ or "",
                    'parameters': params
                }
            })
        return openai_tools

    def send_message(self, prompt):
        """
        處理單次對話。支援自動判斷是否需要呼叫工具，
        並在工具執行完畢後再次請求模型，直到產生最終文字回應為止 (串流輸出)。
        """
        # 將使用者輸入加入歷史紀錄
        self.messages.append({'role': 'user', 'content': prompt})

        # 建立處理迴圈，直到模型不再呼叫工具為止
        while True:
            # 1. 呼叫 OpenAI API (不使用串流，用於檢查是否回傳 tool_calls)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=self.tools or None
            )
            msg = response.choices[0].message

            # 2. 如果模型決定調用工具
            if msg.tool_calls:
                # 將模型的調用請求加入歷史紀錄
                self.messages.append(msg)

                # 逐一執行每一個被調用的工具
                for tool_call in msg.tool_calls:
                    func_name = tool_call.function.name
                    try:
                        args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        args = {}

                    # 輸出日誌
                    log_entry = f"🛠️ [OpenAI] 調用工具: {func_name}({args})"
                    print(f"  {log_entry}")
                    yield {"type": "log", "content": log_entry}

                    # 執行實際的 Python 函式
                    if func_name in self.tool_map:
                        try:
                            result = self.tool_map[func_name](**args)
                        except Exception as func_err:
                            result = f"工具執行出錯: {str(func_err)}"
                    else:
                        result = f"未知工具: {func_name}"

                    # 將工具的執行結果加入歷史紀錄，供模型下一回合參考
                    self.messages.append({
                        'role': 'tool',
                        'tool_call_id': tool_call.id,
                        'content': str(result)
                    })
                # 工具執行完畢後，進入下一次迴圈讓模型根據結果繼續回答
                continue

            else:
                # 3. 若無工具調用，代表模型準備回答純文字，使用串流 API (Stream) 取得打字機效果
                full_content = ""
                stream = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    stream=True
                )

                for chunk_res in stream:
                    delta = chunk_res.choices[0].delta.content or ""
                    if delta:
                        full_content += delta
                        yield {"type": "delta", "content": delta}

                # 將最終組裝的文字加入歷史紀錄
                self.messages.append({'role': 'assistant', 'content': full_content})
                yield {"type": "final", "content": ""}

                # 結束迴圈
                return
