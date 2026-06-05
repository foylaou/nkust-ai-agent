import os
import requests
from dotenv import load_dotenv
from google.adk.agents import Agent

load_dotenv()

_agent_mode = os.getenv("AGENT_MODE", "gemini").lower()
_model_name  = os.getenv("MODEL_NAME", "gemini-2.5-flash")
if _agent_mode == "ollama":
    from google.adk.models.lite_llm import LiteLlm
    MODEL = LiteLlm(model=f"openai/{_model_name}")
elif _agent_mode == "litellm":
    from google.adk.models.lite_llm import LiteLlm
    _ll_kwargs = {}
    if os.getenv("LITELLM_BASE_URL"):
        _ll_kwargs["api_base"] = os.getenv("LITELLM_BASE_URL")
    if os.getenv("LITELLM_API_KEY"):
        _ll_kwargs["api_key"] = os.getenv("LITELLM_API_KEY")
    MODEL = LiteLlm(model=_model_name, **_ll_kwargs)
else:
    MODEL = _model_name


def book_room(
    room_id: str,
    user_name: str,
    meeting_name: str,
    start_time: str,
    end_time: str,
    attendees: str = "1",
):
    """
    執行會議室預約動作的工具函式。

    由團隊中負責「執行預約」的角色 (如 Booker) 來呼叫。

    Args:
        room_id (str): 要預約的房間 ID。
        user_name (str): 預約人姓名。
        meeting_name (str): 會議名稱。
        start_time (str): 開始時間，格式 'YYYY-MM-DD HH:MM'。
        end_time (str): 結束時間，格式 'YYYY-MM-DD HH:MM'。
        attendees (str): 與會人數。

    Returns:
        str: 預約操作的回應訊息。
    """
    try:
        payload = {
            "room_id": room_id,
            "user_name": user_name,
            "meeting_name": meeting_name,
            "start_time": start_time,
            "end_time": end_time,
            "attendees": attendees,
        }
        response = requests.post("http://localhost:8080/book", json=payload)
        return response.json().get("message", "預約失敗")
    except:
        return "連線失敗"



book_agent = Agent(
    name="book_agent",
    model=MODEL,
    description="負責執行會議室預約操作",
    instruction=(
        "你是預約專員（Booker）。\n"
        "收到管理員提供的 room_id、user_name、meeting_name、start_time、end_time、attendees 後，"
        "立刻呼叫 book_room 工具執行預約，然後直接輸出文字回報結果。\n"
        "時間格式為 'YYYY-MM-DD HH:MM'。若工具回報容量不足或時段衝突，請如實回報原因。\n"
        "不要呼叫 'answer' 或任何不存在的工具。請使用繁體中文回覆。"
    ),
    tools=[book_room],
)
