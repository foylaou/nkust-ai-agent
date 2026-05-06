import os
import os.path
import base64
from email.message import EmailMessage
from google.adk.agents import Agent
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
from google.adk.tools import FunctionTool  # ← 新增 import
from datetime import datetime
import pytz

# 確保使用台灣時區並格式化當下時間
tz = pytz.timezone('Asia/Taipei')
now = datetime.now(tz)
current_time_str = now.strftime("%Y-%m-%d %A %H:%M:%S")

load_dotenv()

# 修改為 Gmail 的完整讀寫權限
GMAIL_SCOPES = ["https://mail.google.com/"]
_agent_mode = os.getenv("AGENT_MODE", "gemini").lower()
_model_name  = os.getenv("MODEL_NAME", "gemini-2.5-flash")
if _agent_mode == "ollama":
    from google.adk.models.lite_llm import LiteLlm
    MODEL = LiteLlm(model=f"openai/{_model_name}")
else:
    MODEL = _model_name

def _get_gmail_service():
    """獲取 Gmail API 授權與服務連線"""
    creds = None
    # 建議使用不同的 token 檔名，避免與 Calendar 衝突
    if os.path.exists("gmail_token.json"):
        creds = Credentials.from_authorized_user_file("gmail_token.json", GMAIL_SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds_path = os.getenv("GOOGLE_GMAIL_CREDENTIALS", "credentials.json")
            if not os.path.exists(creds_path):
                raise FileNotFoundError(f"找不到憑證檔案：{creds_path}，請檢查 .env 設定。")
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, GMAIL_SCOPES)
            creds = flow.run_local_server(port=0)
        with open("gmail_token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def send_email(to_email: str, subject: str, body_text: str):
    """
    發送電子郵件。
    to_email：收件者信箱；subject：信件主旨；body_text：信件內文。
    """
    try:
        service = _get_gmail_service()

        # 建立郵件內容
        message = EmailMessage()
        message.set_content(body_text)
        message["To"] = to_email
        message["Subject"] = subject

        # Gmail API 需要將郵件轉為 base64 urlsafe 格式
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}

        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        return f"郵件已成功發送！郵件 ID: {send_message['id']}"
    except Exception as e:
        return f"發送郵件失敗：{e}"


def get_unread_emails(max_results: int = 5):
    """
    查詢目前收件匣中的未讀郵件。
    回傳：包含郵件 ID、寄件者與主旨的字串清單。
    """
    try:
        service = _get_gmail_service()
        # 搜尋標籤為 UNREAD 的郵件
        results = service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=max_results).execute()
        messages = results.get('messages', [])

        if not messages:
            return "目前收件匣沒有未讀郵件。"

        result_str = "找到以下未讀郵件：\n"
        for msg in messages:
            msg_id = msg['id']
            # 取得郵件標頭 (Headers) 資訊
            msg_data = service.users().messages().get(
                userId='me', id=msg_id, format='metadata', metadataHeaders=['Subject', 'From']
            ).execute()

            headers = msg_data['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '無主旨')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), '未知寄件者')

            result_str += f"- ID: {msg_id} | 寄件者: {sender} | 主旨: {subject}\n"

        return result_str
    except Exception as e:
        return f"查詢未讀郵件失敗：{e}"


def mark_email_as_read(msg_id: str):
    """
    將指定的郵件標記為已讀。
    msg_id：郵件的唯一識別碼（可由 get_unread_emails 獲得）。
    """
    try:
        service = _get_gmail_service()
        # 移除 'UNREAD' 標籤
        service.users().messages().modify(
            userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}
        ).execute()
        return f"郵件 (ID: {msg_id}) 已成功標記為已讀！"
    except Exception as e:
        return f"標記已讀失敗：{e}"


# 建立 Email Agent
email_agent = Agent(
    name="email_agent",
    model=MODEL,
    description="負責收發電子郵件、檢查未讀信件並管理收件匣狀態",
    instruction=(
        f"你是專業的電子郵件專員（Email Assistant）。\n"
        f"【系統資訊】現在的台灣系統時間是：{current_time_str}。\n"
        "【時間判斷規則】\n"
        "當你需要撰寫郵件並提及時間（如「今天」、「明天開會」）時，請務必參考上述系統時間來撰寫正確的日期。\n\n"
        "你的職責包含：\n"
        "1. 發送郵件：呼叫 send_email 發信，請確保內容禮貌專業。\n"
        "2. 查詢未讀：呼叫 get_unread_emails 查詢信箱中的未讀郵件，並向使用者報告寄件者與主旨。\n"
        "3. 標記已讀：當使用者確認過某封未讀郵件後，你可以呼叫 mark_email_as_read 將其標記為已讀，避免重複提醒。\n"
        "請使用繁體中文回覆，並提供完整的執行結果報告。"
    ),
    tools=[
        FunctionTool(send_email, require_confirmation=True),  # ← 發信前需使用者確認
        get_unread_emails,
        mark_email_as_read
    ],
)