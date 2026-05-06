from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()


class GeminiADKWrapper:
    """
    使用 Google ADK (Agent Development Kit) 建立的 Gemini Chat Wrapper。

    支援 ADK 工具 (例如 google_search) 與 sub_agents (多 Agent 架構)，
    並將非同步的執行過程封裝為同步產生器 (generator) 以符合統一介面規範。
    """

    def __init__(self, model, system_instruction, tools, sub_agents=None):
        from google.adk.agents import Agent
        from google.adk.runners import Runner as _Runner
        from google.adk.sessions import InMemorySessionService
        import asyncio

        # 建立專屬的事件迴圈以執行非同步操作
        self._loop = asyncio.new_event_loop()

        # 初始化 ADK Agent，若有傳入 sub_agents 則一併設定（Multi-Agent 架構）
        agent_kwargs = dict(
            name="unified_agent",
            model=model,
            instruction=system_instruction,
            tools=tools,
        )
        if sub_agents:
            agent_kwargs["sub_agents"] = sub_agents
        self.agent = Agent(**agent_kwargs)

        # Session 相關設定
        self._app_name = "unified_agent"
        self._user_id = "user"
        self._session_id = "session_001"
        self.session_service = InMemorySessionService()

        # 建立 Session
        self._loop.run_until_complete(
            self.session_service.create_session(
                app_name=self._app_name,
                user_id=self._user_id,
                session_id=self._session_id
            )
        )

        # 初始化 ADK Runner 負責執行對話邏輯
        self.runner = _Runner(
            agent=self.agent,
            app_name=self._app_name,
            session_service=self.session_service
        )

    def send_message(self, user_input):
        """
        發送訊息並取得回應。

        將非同步產生的事件流轉為字典格式的產生器回傳。

        Yields:
            dict: 包含 'type' (log, delta, final) 與 'content' (文字內容) 的字典。
        """
        from google.genai import types

        async def _collect():
            # 建立使用者訊息物件
            content = types.Content(role='user', parts=[types.Part(text=user_input)])
            # 執行 Runner 取得事件流
            events = self.runner.run_async(
                user_id=self._user_id,
                session_id=self._session_id,
                new_message=content
            )
            chunks = []

            # 迭代非同步事件流
            async for event in events:
                # 處理過程中產生的工具調用 / Agent 轉派事件 (Log)
                if not event.is_final_response():
                    try:
                        author = getattr(event, "author", "ADK")
                        for part in (event.content.parts or []):
                            if hasattr(part, "function_call") and part.function_call:
                                fc = part.function_call
                                if fc.name == "transfer_to_agent":
                                    target = dict(fc.args).get("agent_name", "?")
                                    log = f"🔀 [{author}] 轉派任務 → {target}"
                                else:
                                    log = f"🛠️ [{author}] 呼叫工具：{fc.name}({dict(fc.args)})"
                                chunks.append({"type": "log", "content": log})
                    except Exception:
                        pass
                # 處理最終回應文字 (Delta)
                else:
                    try:
                        text = event.content.parts[0].text
                        if text:
                            chunks.append({"type": "delta", "content": text})
                    except Exception:
                        pass

            # 標記結束
            chunks.append({"type": "final", "content": ""})
            return chunks

        # 執行非同步函式並使用 yield 回傳每一個 chunk
        for c in self._loop.run_until_complete(_collect()):
            yield c
