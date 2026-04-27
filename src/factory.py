import os
import json
import inspect
from dotenv import load_dotenv

load_dotenv()


def ollama_web_search(query: str) -> str:
    """搜尋網路上的最新資訊，回傳相關網頁的標題、網址與摘要"""
    import requests
    api_key = os.getenv("OLLAMA_WEB_SEARCH_API_KEY", "")
    try:
        resp = requests.post(
            "https://ollama.com/api/web_search",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"query": query, "max_results": 5},
            timeout=15
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
        if not results:
            return "未找到相關結果"
        lines = []
        for r in results:
            lines.append(f"標題: {r.get('title', '')}\nURL: {r.get('url', '')}\n摘要: {r.get('content', '')}\n")
        return "\n".join(lines)
    except Exception as e:
        return f"搜尋失敗: {e}"

class UnifiedAgent:
    """統一介面的 Agent，支援 Gemini、Ollama 與 OpenAI"""
    def __init__(self):
        self.mode = os.getenv("AGENT_MODE", "gemini").lower()
        env_model = os.getenv("MODEL_NAME")

        if self.mode == "gemini":
            self.model = env_model or "gemini-2.0-flash"
            print(f"✨ 目前模式：Gemini Online ({self.model})")

        elif self.mode == "openai":
            self.model = env_model or "gpt-4o-mini"
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
            self.openai_base_url = os.getenv("OPENAI_BASE_URL")
            print(f"🤖 目前模式：OpenAI ({self.model})")

        else:  # ollama
            self.model = env_model or "gemma2"
            self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
            self.ollama_api_key = os.getenv("OLLAMA_API_KEY")
            print(f"🦙 目前模式：Ollama Local ({self.model}) @ {self.ollama_url}")

    def create_chat(self, system_instruction, tools):
        """建立聊天會話"""
        from datetime import date
        dated_instruction = f"今天是 {date.today().strftime('%Y年%m月%d日')}。\n\n{system_instruction}"

        if self.mode == "gemini":
            return GeminiADKWrapper(self.model, dated_instruction, tools)

        elif self.mode == "openai":
            return OpenAIChatWrapper(self.model, dated_instruction, tools,
                                     api_key=self.openai_api_key,
                                     base_url=self.openai_base_url)

        else:  # ollama
            return OllamaChatWrapper(self.model, dated_instruction, tools,
                                     host=self.ollama_url, api_key=self.ollama_api_key)


class GeminiADKWrapper:
    """使用 Google ADK Agent + Runner 的 Gemini wrapper，支援 ADK 工具如 google_search"""
    def __init__(self, model, system_instruction, tools):
        from google.adk.agents import Agent
        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService
        import asyncio

        self._loop = asyncio.new_event_loop()
        self.agent = Agent(
            name="unified_agent",
            model=model,
            instruction=system_instruction,
            tools=tools
        )
        self._app_name = "unified_agent"
        self._user_id = "user"
        self._session_id = "session_001"
        self.session_service = InMemorySessionService()
        self._loop.run_until_complete(
            self.session_service.create_session(
                app_name=self._app_name,
                user_id=self._user_id,
                session_id=self._session_id
            )
        )
        from google.adk.runners import Runner as _Runner
        self.runner = _Runner(
            agent=self.agent,
            app_name=self._app_name,
            session_service=self.session_service
        )

    def send_message(self, user_input):
        from google.genai import types

        async def _collect():
            content = types.Content(role='user', parts=[types.Part(text=user_input)])
            events = self.runner.run_async(
                user_id=self._user_id,
                session_id=self._session_id,
                new_message=content
            )
            chunks = []
            async for event in events:
                if not event.is_final_response():
                    try:
                        for part in (event.content.parts or []):
                            if hasattr(part, 'function_call') and part.function_call:
                                fc = part.function_call
                                log = f"🛠️ [ADK] 調用工具: {fc.name}({dict(fc.args)})"
                                chunks.append({"type": "log", "content": log})
                    except Exception:
                        pass
                else:
                    try:
                        text = event.content.parts[0].text
                        if text:
                            chunks.append({"type": "delta", "content": text})
                    except Exception:
                        pass
            chunks.append({"type": "final", "content": ""})
            return chunks

        for chunk in self._loop.run_until_complete(_collect()):
            yield chunk


class GeminiChatWrapper:
    """將 Gemini Chat 包裝成 generator 介面，與其他 Wrapper 相容"""
    def __init__(self, chat):
        self.chat = chat

    def send_message(self, user_input):
        try:
            response = self.chat.send_message(user_input)

            try:
                for candidate in response.candidates or []:
                    for part in candidate.content.parts or []:
                        if hasattr(part, 'function_call') and part.function_call:
                            fc = part.function_call
                            log = f"🛠️ [Gemini] 調用工具: {fc.name}({dict(fc.args)})"
                            yield {"type": "log", "content": log}
            except Exception:
                pass

            text = response.text if hasattr(response, 'text') else str(response)
            if text:
                yield {"type": "delta", "content": text}
            yield {"type": "final", "content": ""}
        except Exception as e:
            yield {"type": "error", "content": str(e)}


class OpenAIChatWrapper:
    """OpenAI Chat 包裝器，支援 tool calling 與串流輸出"""
    def __init__(self, model, system_instruction, tools, api_key=None, base_url=None):
        self.model = model
        self.messages = [{'role': 'system', 'content': system_instruction}]
        self.tools = self._convert_tools(tools)
        self.tool_map = {f.__name__: f for f in tools if inspect.isfunction(f)}
        from openai import OpenAI
        kwargs = {'api_key': api_key}
        if base_url:
            kwargs['base_url'] = base_url
        self.client = OpenAI(**kwargs)

    @staticmethod
    def _convert_tools(functions):
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

    def send_message(self, user_input):
        """發送訊息並處理工具循環，以產生器方式回傳過程與最終結果"""
        self.messages.append({'role': 'user', 'content': user_input})

        while True:
            # 1. 呼叫 OpenAI（非串流，用於判斷是否有 tool call）
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=self.tools or None
            )
            msg = response.choices[0].message

            # 2. 檢查是否有工具調用
            if msg.tool_calls:
                self.messages.append(msg)

                for tool_call in msg.tool_calls:
                    func_name = tool_call.function.name
                    try:
                        args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        args = {}

                    log_entry = f"🛠️ [OpenAI] 調用工具: {func_name}({args})"
                    print(f"  {log_entry}")
                    yield {"type": "log", "content": log_entry}

                    if func_name in self.tool_map:
                        try:
                            result = self.tool_map[func_name](**args)
                        except Exception as e:
                            result = f"工具執行出錯: {str(e)}"
                    else:
                        result = f"未知工具: {func_name}"

                    self.messages.append({
                        'role': 'tool',
                        'tool_call_id': tool_call.id,
                        'content': str(result)
                    })
                continue

            else:
                # 3. 最終回覆：使用串流模式達到「打字機」效果
                full_content = ""
                stream = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    stream=True
                )

                for chunk in stream:
                    delta = chunk.choices[0].delta.content or ""
                    if delta:
                        full_content += delta
                        yield {"type": "delta", "content": delta}

                self.messages.append({'role': 'assistant', 'content': full_content})
                yield {"type": "final", "content": ""}
                return


class OllamaChatWrapper:
    """模擬 Gemini Chat 介面的 Ollama 包裝器"""
    def __init__(self, model, system_instruction, tools, host=None, api_key=None):
        self.model = model
        self.messages = [{'role': 'system', 'content': system_instruction}]
        self.tools = self._convert_tools(tools)
        self.tool_map = {f.__name__: f for f in tools if inspect.isfunction(f)}
        import ollama
        headers = {'Authorization': f'Bearer {api_key}'} if api_key else {}
        self.client = ollama.Client(host=host or "http://localhost:11434", headers=headers)

    @staticmethod
    def _convert_tools(functions):
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

    def send_message(self, user_input):
        """發送訊息並處理工具循環，並以產生器方式回傳過程與最終結果"""
        self.messages.append({'role': 'user', 'content': user_input})

        while True:
            # 1. 呼叫 Ollama
            response = self.client.chat(model=self.model, messages=self.messages, tools=self.tools)

            # 2. 檢查是否有工具調用 (Tool Calls)
            tool_calls = response.get('message', {}).get('tool_calls')

            if tool_calls:
                self.messages.append(response['message'])

                for tool in tool_calls:
                    func_name = tool['function']['name']
                    args = tool['function']['arguments']

                    log_entry = f"🛠️ [Local Reasoning] 調用工具: {func_name}({args})"
                    print(f"  {log_entry}")
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
                print(content)
                if not content:
                    self.messages.append({'role': 'user', 'content': "請彙整以上執行結果並回報給我。"})

                full_content = ""
                stream = self.client.chat(model=self.model, messages=self.messages, stream=True, tools=self.tools)

                for chunk in stream:
                    delta = chunk.get('message', {}).get('content', "")
                    if delta:
                        full_content += delta
                        yield {"type": "delta", "content": delta}

                self.messages.append({'role': 'assistant', 'content': full_content})
                yield {"type": "final", "content": ""}
                return


if __name__ == '__main__':
    agent_factory = UnifiedAgent()

    if agent_factory.mode == "gemini":
        from google.adk.tools import google_search
        tools = [google_search]
    elif agent_factory.mode == "ollama":
        tools = [ollama_web_search]
    else:
        tools = []

    chat = agent_factory.create_chat("你是一位行政助手，請使用繁體中文跟我對話", tools)
    while True:
        user_input = input("\n👤 您: ")
        if user_input.lower() in ["exit", "quit"]: break
        try:
            print("🤖 Agent: ", end="", flush=True)
            for chunk in chat.send_message(user_input):
                if chunk["type"] == "delta":
                    print(chunk["content"], end="", flush=True)
                elif chunk["type"] == "log":
                    print(f"\n  {chunk['content']}", flush=True)
                elif chunk["type"] == "error":
                    print(f"\n系統錯誤: {chunk['content']}", flush=True)
            print()
        except Exception as e:
            print(f"系統錯誤: {str(e)}")