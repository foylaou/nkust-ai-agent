import importlib.util
import os
import sys
import logging as _logging

from dotenv import load_dotenv
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.adk.tools.tool_context import ToolContext
from google.adk.models.llm_request import LlmRequest

load_dotenv()

# ==========================================
# DEBUG_MODE 控制 memory log 顯示
# .env 設 DEBUG_MODE=1 才顯示，否則靜音
# ==========================================
_DEBUG = os.getenv("DEBUG_MODE", "0").strip() == "1"
_mem_log = _logging.getLogger("memory_debug")
_mem_log.setLevel(_logging.DEBUG if _DEBUG else _logging.WARNING)

class DebugPreloadMemoryTool(PreloadMemoryTool):
    """PreloadMemoryTool with debug logging."""

    async def process_llm_request(
        self,
        *,
        tool_context: ToolContext,
        llm_request: LlmRequest,
    ) -> None:
        user_content = tool_context.user_content
        query = (user_content.parts[0].text
                 if user_content and user_content.parts else "(none)")
        _mem_log.debug(f"[PreloadMemory] 🔍 搜尋 query: {query[:60]}")
        try:
            response = await tool_context.search_memory(query)
            _mem_log.debug(f"[PreloadMemory] 結果數: {len(response.memories)}")
            for m in response.memories:
                txt = " ".join(p.text for p in (m.content.parts or []) if p.text)
                _mem_log.debug(f"[PreloadMemory]   → {txt[:80]}")
        except Exception as e:
            _mem_log.debug(f"[PreloadMemory] ❌ search_memory 失敗: {e}")
            return
        # 仍然呼叫原本邏輯
        await super().process_llm_request(
            tool_context=tool_context, llm_request=llm_request
        )
from google.adk.agents.callback_context import CallbackContext

load_dotenv()
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))

from UnifiedMemoryService import UnifiedMemoryService
# ==========================================
# Memory Service 初始化（全域，給 Runner 用）
# ==========================================
memory_service = UnifiedMemoryService()
# ==========================================
# 模型 / LiteLLM 設定（須在載入子 Agent 前完成）
# ==========================================

_agent_mode = os.getenv("AGENT_MODE", "gemini").lower()
_model_name  = os.getenv("MODEL_NAME", "gemini-2.5-flash")

if _agent_mode == "ollama":
    from google.adk.models.lite_llm import LiteLlm
    import httpx, litellm

    _ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
    _api_key    = os.getenv("OLLAMA_API_KEY", "")
    _root_name  = os.getenv("ROOT_MODEL", "gemma4:31b")   # 大模型做 routing
    _sub_name   = _model_name                              # MODEL_NAME 給 sub-agents

    # 改走 openai/ 路由，繞過 LiteLLM ollama_chat.py 的 tool message 轉換 bug
    # Issue: github.com/BerriAI/litellm/issues/26094
    os.environ["OPENAI_API_BASE"] = f"{_ollama_url}/v1"  # 結尾必須有 /v1
    os.environ["OPENAI_API_KEY"]  = _api_key or "ollama"
    litellm.aclient_session = httpx.AsyncClient(verify=False)

    ROOT_MODEL = LiteLlm(model=f"openai/{_root_name}")
    SUB_MODEL  = LiteLlm(model=f"openai/{_sub_name}")
else:
    ROOT_MODEL = os.getenv("ROOT_MODEL", "gemini-2.0-flash")
    SUB_MODEL  = _model_name

# ==========================================
# 載入子 Agent（各自的工具與邏輯定義在獨立檔案中）
# ==========================================

def _load(module_name: str, rel_path: str):
    """從含連字號的相對路徑載入子 Agent 模組。"""
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "..", rel_path)  # root_agent/ → muilt-agents/
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_room   = _load("room_agent_mod",   "room_agent/room_agent.py")
_search = _load("search_agent_mod", "search_agent/search_agent.py")
_book   = _load("book_agent_mod",   "book_agent/book_agent.py")
_alert  = _load("alert_agent_mod",  "aleart_agent/aleart_agent.py")
_email  = _load("email_agent_mod",  "email_agent/email_agent.py")
_sql  = _load("sql_agent_mod",  "sql_agent/sql_agent.py")

# ==========================================
# after_agent_callback：每輪結束自動存入 memory
# ==========================================

async def _auto_save_memory(callback_context: CallbackContext):
    """每次 agent 回應結束後，將本輪 session 存入 memory service。"""
    try:
        await callback_context.add_session_to_memory()
        if _DEBUG:
            session = callback_context.session
            _mem_log.debug(f"[memory] ✅ saved app={session.app_name} user={session.user_id} session={session.id}")
            for ev in session.events:
                if ev.content and ev.content.parts:
                    texts = [p.text for p in ev.content.parts if p.text]
                    if texts:
                        _mem_log.debug(f"[memory]   {ev.author}: {' '.join(texts)[:80]}")
    except Exception as e:
        _mem_log.warning(f"[memory]  add_session_to_memory 失敗: {e}")

# ==========================================
# Root Agent（管理員）
# ==========================================

SYSTEM_INSTRUCTION = (
    "你是辦公室行政管理員（Manager），統籌指揮一個六人專員團隊：\n"
    "  - room_agent（查詢專員）：查詢會議室即時可用狀態\n"
    "  - search_agent（搜尋專員）：搜尋網路上的最新資訊\n"
    "  - book_agent（預約專員）：執行會議室預約\n"
    "  - alert_agent（通知專員）：新增修改刪除查詢 Google 行事曆 + 發送 Discord 通知\n\n"
    "  - email_agent（電子郵件專員）：發送郵件、查詢未讀、標記已讀 Gmail \n\n"
    "  - sql_agent（專業數據分析助理）：石化業安全督導（Petrochemical Audits）」與「KPI 績效管理」的專業數據分析 \n\n"
    "  - mediasage_agent (圖書電影評價助理)：一位專業且品味出眾的圖書、電影與影集評價及推薦專家\n\n"
    "【預約三步驟，必須依序實際執行，不得跳過或模擬】\n"
    "  步驟 1：轉派 room_agent 查詢空閒會議室\n"
    "  步驟 2：確認 room_id、user_name、meeting_name 三項資訊後，\n"
    "          立刻轉派 book_agent 執行預約 ── 不要詢問時間，不要再次確認，直接執行\n"
    "  步驟 3：預約成功後，轉派 alert_agent 發送通知\n\n"
    "【嚴格禁止事項】\n"
    "  - 禁止以文字模擬工具呼叫（例如不得出現『模擬呼叫』、'*(以下模擬..)*' 等字樣）\n"
    "  - 禁止向使用者詢問預約時間（booking 系統不需要時間欄位）\n"
    "  - 禁止在已有完整資訊時再次詢問使用者確認\n\n"
    "【直接回答，不轉派的情況】\n"
    "  - 問候、自我介紹、閒聊、詢問你的功能或身份 → 自行回答，絕對不轉派任何 agent\n"
    "  - search_agent 只用於查詢網際網路上的外部資訊（新聞、天氣、技術問題等）\n\n"
    "【回應規則 — 非常重要】\n"
    "  - 直接輸出文字即可回覆使用者，絕對不要呼叫 'answer'、'respond' 或任何不存在的工具\n"
    "  - 你唯一可用的工具是 transfer_to_agent，只在需要轉派任務時才使用\n\n"
    "若缺少 user_name 或 meeting_name，才主動詢問，補齊後立即執行。\n"
    "請全程使用繁體中文回覆。"
)

root_agent = Agent(
    name="root_agent",
    model=ROOT_MODEL,
    instruction=SYSTEM_INSTRUCTION,
    sub_agents=[
        _room.room_agent,
        _search.search_agent,
        _book.book_agent,
        _alert.alert_agent,
        _email.email_agent,
        _sql.sql_agent,
    ],
    tools=[DebugPreloadMemoryTool()],
    after_agent_callback=_auto_save_memory,
)

# # ==========================================
# # CLI 模式（python root_agent/agent.py）
# # ==========================================
#
# if __name__ == "__main__":
#     import asyncio
#     from google.adk.agents.run_config import RunConfig
#     from google.adk.runners import Runner
#     from google.adk.sessions import InMemorySessionService
#     from google.genai import types
#
#     APP_NAME, USER_ID, SESSION = "nkust_multi_agent", "user", "session_001"
#     # 每輪最多 10 次 LLM 呼叫，防止 sub-agent 陷入無限迴圈
#     RUN_CONFIG = RunConfig(max_llm_calls=10)
#
#     async def main():
#         session_service = InMemorySessionService()
#         await session_service.create_session(
#             app_name=APP_NAME, user_id=USER_ID, session_id=SESSION
#         )
#         runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
#
#         print("\n╔══════════════════════════════════════════════╗")
#         print("║  👥 NKUST Multi-Agent Team (ADK)             ║")
#         print("║  Manager → Room / Search / Book / Notifier  ║")
#         print("╚══════════════════════════════════════════════╝")
#         print("輸入 'exit' 或 'quit' 離開\n")
#
#         while True:
#             user_input = input("👑 指令：").strip()
#             if not user_input:
#                 continue
#             if user_input.lower() in ("exit", "quit"):
#                 print("已離開。")
#                 break
#
#             content = types.Content(role="user", parts=[types.Part(text=user_input)])
#             async for event in runner.run_async(
#                 user_id=USER_ID, session_id=SESSION, new_message=content,
#                 run_config=RUN_CONFIG,
#             ):
#                 if not event.is_final_response():
#                     try:
#                         author = getattr(event, "author", "")
#                         for part in event.content.parts or []:
#                             if hasattr(part, "function_call") and part.function_call:
#                                 fc = part.function_call
#                                 if fc.name == "transfer_to_agent":
#                                     target = dict(fc.args).get("agent_name", "?")
#                                     print(f"  🔀 [{author}] 轉派 → {target}")
#                                 else:
#                                     print(f"  🛠️  [{author}] {fc.name}({dict(fc.args)})")
#                     except Exception:
#                         pass
#                 else:
#                     try:
#                         text = event.content.parts[0].text
#                         if text:
#                             print(f"\n🤖 Manager：\n{text}\n")
#                     except Exception:
#                         pass
#
#     asyncio.run(main())
