import os
import json
import inspect
from dotenv import load_dotenv
from google import genai
from google.genai import types
import ollama
from openai import OpenAI

load_dotenv()

class UnifiedAgent:
    """統一介面的 Agent，支援 Gemini、Ollama 與 OpenAI"""
    def __init__(self):
        self.mode = os.getenv("AGENT_MODE", "gemini").lower()
        env_model = os.getenv("MODEL_NAME")

        if self.mode == "gemini":
            self.model = env_model or "gemini-2.0-flash"
            self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
            print(f"✨ 目前模式：Gemini Online ({self.model})")

        elif self.mode == "openai":
            self.model = env_model or "gpt-4o-mini"
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
            self.openai_base_url = os.getenv("OPENAI_BASE_URL")  # 可選，用於相容 API
            print(f"🤖 目前模式：OpenAI ({self.model})")

        else:  # ollama
            self.model = env_model or "gemma2"
            self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
            self.ollama_api_key = os.getenv("OLLAMA_API_KEY")
            print(f"🦙 目前模式：Ollama Local ({self.model}) @ {self.ollama_url}")

    def create_chat(self, system_instruction, tools):
        """建立聊天會話"""
        if self.mode == "gemini":
            chat = self.client.chats.create(
                model=self.model,
                config=types.GenerateContentConfig(
                    tools=tools,
                    system_instruction=system_instruction
                )
            )
            return GeminiChatWrapper(chat)

        elif self.mode == "openai":
            return OpenAIChatWrapper(self.model, system_instruction, tools,
                                     api_key=self.openai_api_key,
                                     base_url=self.openai_base_url)

        else:  # ollama
            return OllamaChatWrapper(self.model, system_instruction, tools,
                                     host=self.ollama_url, api_key=self.ollama_api_key)


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
        self.tool_map = {f.__name__: f for f in tools}
        kwargs = {'api_key': api_key}
        if base_url:
            kwargs['base_url'] = base_url
        self.client = OpenAI(**kwargs)

    @staticmethod
    def _convert_tools(functions):
        openai_tools = []
        for f in functions:
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
        self.tool_map = {f.__name__: f for f in tools}
        headers = {'Authorization': f'Bearer {api_key}'} if api_key else {}
        self.client = ollama.Client(host=host or "http://localhost:11434", headers=headers)

    @staticmethod
    def _convert_tools(functions):
        ollama_tools = []
        for f in functions:
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
