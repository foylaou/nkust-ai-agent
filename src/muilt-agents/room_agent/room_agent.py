import os
import requests
from dotenv import load_dotenv
from google.adk.agents import Agent

load_dotenv()

_agent_mode = os.getenv("AGENT_MODE", "gemini").lower()
_model_name  = os.getenv("MODEL_NAME", "gemini-2.5-flash")
MODEL = f"openai/{_model_name}" if _agent_mode == "ollama" else _model_name


def get_room_status():
    """查詢辦公室所有會議室的即時狀態，回傳名稱、容量與預約情況。"""
    try:
        response = requests.get("http://localhost:8080/rooms", timeout=5)
        if response.status_code == 200:
            rooms = response.json()
            lines = ["目前會議室狀態："]
            for r in rooms:
                if r["status"] == "Booked":
                    status = f"已被 {r['booked_by']} 預約（會議：{r['meeting_name']}）"
                else:
                    status = "空閒中"
                lines.append(f"  - {r['name']} ({r['id']}): 容納 {r['capacity']} 人，{status}")
            return "\n".join(lines)
        return "無法取得會議室資訊，請稍後再試。"
    except Exception as e:
        return f"本地系統連線失敗：{e}"


room_agent = Agent(
    name="room_agent",
    model=MODEL,
    description="負責查詢會議室的即時可用狀態",
    instruction=(
        "你是會議室查詢專員（Room Checker）。\n\n"
        "【執行步驟 — 只做一次，不重複】\n"
        "1. 呼叫 get_room_status 工具一次\n"
        "2. 收到工具回傳資料後，立刻將結果整理成繁體中文文字輸出\n"
        "3. 完成，不再呼叫任何工具\n\n"
        "【嚴格禁止】\n"
        "- 禁止在已收到查詢資料後再次呼叫 get_room_status\n"
        "- 禁止呼叫 'answer' 或任何其他不存在的工具\n\n"
        "【超出查詢範圍的請求】\n"
        "若使用者同時提出預約需求（如指定時段），請先回報目前會議室基本狀態，"
        "然後告知將轉交預約專員處理。\n\n"
        "請使用繁體中文回覆。"
    ),
    tools=[get_room_status],
)
