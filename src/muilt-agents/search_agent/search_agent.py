import os
import sys
from dotenv import load_dotenv
from google.adk.agents import Agent


load_dotenv()

_agent_mode = os.getenv("AGENT_MODE", "gemini").lower()
_model_name  = os.getenv("MODEL_NAME", "gemini-2.5-flash")

if _agent_mode == "ollama":
    from google.adk.models.lite_llm import LiteLlm
    MODEL = LiteLlm(model=f"openai/{_model_name}")
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))
    from ollama_tools import ollama_web_search
    search_tool = ollama_web_search
elif _agent_mode == "litellm":
    # google_search 為 Gemini 專屬內建工具，litellm 接非 Gemini 會失效，
    # 故改用 model-agnostic 的 ollama_web_search 函式工具（需 OLLAMA_WEB_SEARCH_API_KEY）。
    from google.adk.models.lite_llm import LiteLlm
    _ll_kwargs = {}
    if os.getenv("LITELLM_BASE_URL"):
        _ll_kwargs["api_base"] = os.getenv("LITELLM_BASE_URL")
    if os.getenv("LITELLM_API_KEY"):
        _ll_kwargs["api_key"] = os.getenv("LITELLM_API_KEY")
    MODEL = LiteLlm(model=_model_name, **_ll_kwargs)
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))
    from ollama_tools import ollama_web_search
    search_tool = ollama_web_search
else:
    MODEL = _model_name
    from google.adk.tools import google_search
    search_tool = google_search


search_agent = Agent(
    name="search_agent",
    model=MODEL,
    description="負責搜尋網際網路上的外部資訊，例如新聞、天氣、技術問題。不處理問候或系統內部查詢。",
    instruction=(
        "你是網路搜尋專員（Web Searcher）。"
        "當管理員需要查詢任何網路資訊時，請使用搜尋工具找到相關內容，"
        "並將結果整理摘要後回報。請使用繁體中文回覆。"
    ),
    tools=[search_tool],
)
