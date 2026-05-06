from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()


class GeminiChatWrapper:
    """
    將原生的 Gemini Chat API 包裝成 generator 介面，
    使其回傳格式與其他的 Wrapper 保持一致。
    """

    def __init__(self, chat):
        self.chat = chat

    def send_message(self, msg_input):
        try:
            # 呼叫原生 send_message
            response = self.chat.send_message(msg_input)

            # 解析是否包含工具調用 (Function Calling) 並拋出日誌
            try:
                for candidate in response.candidates or []:
                    for part in candidate.content.parts or []:
                        if hasattr(part, 'function_call') and part.function_call:
                            fc = part.function_call
                            log = f"🛠️ [Gemini] 調用工具: {fc.name}({dict(fc.args)})"
                            yield {"type": "log", "content": log}
            except Exception:
                pass

            # 解析並回傳最終文字
            text = response.text if hasattr(response, 'text') else str(response)
            if text:
                yield {"type": "delta", "content": text}

            yield {"type": "final", "content": ""}
        except Exception as e:
            # 捕捉並回傳錯誤訊息
            yield {"type": "error", "content": str(e)}
