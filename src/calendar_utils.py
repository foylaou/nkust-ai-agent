import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from dotenv import load_dotenv
load_dotenv()

# 如果修改這些 SCOPES，請刪除 token.json 檔案。
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_calendar_service():
    """取得 Google Calendar 服務實例"""
    creds = None
    # token.json 儲存使用者的存取與更新權杖
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # 如果沒有可用的憑證，讓使用者登入。
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # 優先從環境變數讀取路徑，預設為 credentials.json
            creds_path = os.getenv("GOOGLE_CALENDAR_CREDENTIALS", "credentials.json")
            
            if not os.path.exists(creds_path):
                raise FileNotFoundError(f"找不到憑證檔案：{creds_path}，請檢查 .env 設定。")
            
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # 儲存憑證供下次使用
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

def real_google_calendar_create_event(summary: str, start_time: str, end_time: str):
    """
    在 Google Calendar 建立一個真實活動。
    
    Args:
        summary: 會議主旨
        start_time: 開始時間 (ISO 格式，如 2026-04-28T08:00:00)
        end_time: 結束時間 (ISO 格式，如 2026-04-28T12:00:00)
    """
    try:
        service = get_calendar_service()
        
        event = {
            'summary': summary,
            'description': '由 NKUST AI Agent 自動建立',
            'start': {
                'dateTime': start_time,
                'timeZone': 'Asia/Taipei',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'Asia/Taipei',
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        return f"✅ 已成功在 Google 日曆建立活動！連結: {event.get('htmlLink')}"

    except Exception as e:
        return f"❌ 建立日曆活動失敗: {str(e)}"
