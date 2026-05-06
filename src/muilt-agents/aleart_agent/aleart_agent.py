import os
import requests
import os.path
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
from datetime import datetime
import pytz

# 確保使用台灣時區
tz = pytz.timezone('Asia/Taipei')
now = datetime.now(tz)
current_time_str = now.strftime("%Y-%m-%d %A %H:%M:%S")
# 例如：2026-05-05 Tuesday 14:11:59
load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
_agent_mode = os.getenv("AGENT_MODE", "gemini").lower()
_model_name  = os.getenv("MODEL_NAME", "gemini-2.5-flash")
if _agent_mode == "ollama":
    from google.adk.models.lite_llm import LiteLlm
    MODEL = LiteLlm(model=f"openai/{_model_name}")
else:
    MODEL = _model_name

def _get_calendar_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds_path = os.getenv("GOOGLE_CALENDAR_CREDENTIALS", "credentials.json")
            if not os.path.exists(creds_path):
                raise FileNotFoundError(f"找不到憑證檔案：{creds_path}，請檢查 .env 設定。")
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)


def create_calendar_event(summary: str, start_time: str, end_time: str):
    """
    在 Google Calendar 建立會議行程。
    summary：會議標題；start_time / end_time：ISO 8601 格式，例如 2026-05-05T10:00:00。
    """
    try:
        service = _get_calendar_service()
        event = {
            "summary": summary,
            "description": "由 NKUST AI Agent 自動建立",
            "start": {"dateTime": start_time, "timeZone": "Asia/Taipei"},
            "end": {"dateTime": end_time, "timeZone": "Asia/Taipei"},
        }
        result = service.events().insert(calendarId="primary", body=event).execute()
        return f"Google 行事曆活動已建立！連結：{result.get('htmlLink')}"
    except Exception as e:
        return f"建立行事曆失敗：{e}"
def get_calendar_events(time_min: str, time_max: str, max_results: int = 10):
    """
    查詢 Google Calendar 在指定時間範圍內的行程。
    time_min / time_max：ISO 8601 格式，必須包含時區，例如 2026-05-05T00:00:00+08:00。
    回傳：包含 event_id、標題與時間的字串清單。
    """
    try:
        service = _get_calendar_service()
        events_result = service.events().list(
            calendarId="primary",
            timeMin=time_min,
            timeMax=time_max,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])
        if not events:
            return "此時段內沒有找到任何行程。"

        result_str = "找到以下行程：\n"
        for event in events:
            # 支援全天行程 (date) 或特定時間行程 (dateTime)
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            summary = event.get("summary", "無標題")
            event_id = event["id"]
            result_str += f"- ID: {event_id} | 標題: {summary} | 開始: {start} | 結束: {end}\n"

        return result_str
    except Exception as e:
        return f"查詢行事曆失敗：{e}"


def update_calendar_event(event_id: str, new_summary: str = None, new_start_time: str = None, new_end_time: str = None):
    """
    修改現有的 Google Calendar 行程。
    event_id：行程的唯一識別碼（可由 get_calendar_events 獲得）。
    new_summary、new_start_time、new_end_time 皆為選填，僅更新有提供的值。時間需為 ISO 8601 格式，例如 2026-05-05T10:00:00。
    """
    try:
        service = _get_calendar_service()
        # 1. 取得原事件資料
        event = service.events().get(calendarId="primary", eventId=event_id).execute()

        # 2. 更新欄位
        if new_summary:
            event["summary"] = new_summary
        if new_start_time:
            event["start"] = {"dateTime": new_start_time, "timeZone": "Asia/Taipei"}
        if new_end_time:
            event["end"] = {"dateTime": new_end_time, "timeZone": "Asia/Taipei"}

        # 3. 執行更新
        updated_event = service.events().update(calendarId="primary", eventId=event_id, body=event).execute()
        return f"行程更新成功！連結：{updated_event.get('htmlLink')}"
    except Exception as e:
        return f"更新行事曆失敗：{e}"


def delete_calendar_event(event_id: str):
    """
    刪除指定的 Google Calendar 行程。
    event_id：行程的唯一識別碼（可由 get_calendar_events 獲得）。
    """
    try:
        service = _get_calendar_service()
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        return f"行程 (ID: {event_id}) 已成功刪除！"
    except Exception as e:
        return f"刪除行事曆失敗：{e}"

def discord_send_message(message: str):
    """
    發送通知訊息到 Discord 頻道。
    message：要發送的完整通知內容。
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        return f"[模擬模式] Discord 通知已送出：{message}"
    try:
        response = requests.post(webhook_url, json={"content": message})
        if response.status_code == 204:
            return "Discord 通知發送成功！"
        return f"Discord 發送失敗（狀態碼：{response.status_code}）"
    except Exception as e:
        return f"Discord 連線失敗：{e}"


alert_agent = Agent(
    name="alert_agent",
    model=MODEL,
    description="負責建立 Google Calendar 行事曆活動，並發送 Discord 通知",
    instruction=(
        f"你是行事曆與通知專員（Calendar & Notifier）。\n"
        f"【系統資訊】現在的台灣系統時間是：{current_time_str}。\n"
        "【時間推算規則】\n"
        "當使用者提到相對時間（如「明天」、「禮拜三」、「下週」）時，請務必根據上述系統時間自行推算確切的日期與 ISO 8601 格式，絕對不要反問使用者今天是幾號或禮拜幾。\n"
        "若使用者僅說某一天（如「禮拜三」）且未指定時段，請預設查詢該日的全天範圍（00:00:00 到 23:59:59）。\n"
        "你的職責包含：\n"
        "1. 新增預約：呼叫 create_calendar_event...\n"
    ),
    tools=[
        FunctionTool(create_calendar_event, require_confirmation=True),  # ← 發信前需使用者確認
        get_calendar_events,
        FunctionTool(update_calendar_event, require_confirmation=True),  # ← 發信前需使用者確認
        FunctionTool(delete_calendar_event, require_confirmation=True),  # ← 發信前需使用者確認
        discord_send_message
        ],
)
