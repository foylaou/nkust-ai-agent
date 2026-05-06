## calendar_utils.py
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()

# ==========================================
# Google Calendar 授權設定
# ==========================================

# 定義授權範圍 (Scopes)。如果修改這些 SCOPES，請務必刪除本地端的 token.json 檔案，
# 以便在下次執行時重新進行授權流程。
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_calendar_service():
    """
    取得經過授權的 Google Calendar 服務實例。
    
    會先檢查本地是否存在 token.json，若存在且有效則直接使用；
    若無效但可更新則更新之；若均無效則透過本機開啟瀏覽器讓使用者進行 Oauth2 登入授權，
    並將授權成功後的 credentials 儲存為 token.json 供日後使用。
    
    Returns:
        googleapiclient.discovery.Resource: Google Calendar 服務實例
        
    Raises:
        FileNotFoundError: 如果找不到憑證檔案 (credentials.json)
    """
    creds = None
    
    # 檢查是否已有之前儲存的存取與更新權杖 (token.json)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # 如果沒有可用的憑證，或是憑證已失效，引導使用者登入授權。
    if not creds or not creds.valid:
        # 如果憑證已過期但有提供更新權杖 (refresh token)，則嘗試更新它
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # 優先從環境變數 GOOGLE_CALENDAR_CREDENTIALS 讀取憑證路徑，
            # 若無設定則預設為根目錄下的 'credentials.json'
            creds_path = os.getenv("GOOGLE_CALENDAR_CREDENTIALS", "credentials.json")
            
            # 若指定的憑證檔案不存在，拋出例外提醒使用者檢查設定
            if not os.path.exists(creds_path):
                raise FileNotFoundError(f"找不到憑證檔案：{creds_path}，請檢查 .env 設定。")
            
            # 建立 OAuth 授權流程 (flow)
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            # 在本機開啟一個小型的伺服器來接收驗證碼，完成授權
            creds = flow.run_local_server(port=0)
        
        # 成功取得有效憑證後，儲存為 token.json 供下次執行時使用
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # 使用有效的憑證建立並回傳 Google Calendar V3 API 的服務實例
    return build('calendar', 'v3', credentials=creds)


def real_google_calendar_create_event(summary: str, start_time: str, end_time: str):
    """
    在使用者的 Google Calendar (預設日曆) 中建立一個真實的活動。
    
    透過 Agent 的調用，這個函式會建立一個具有主旨與起訖時間的行程，
    時區預設為台北時間 (Asia/Taipei)。
    
    Args:
        summary (str): 會議或活動的主旨。
        start_time (str): 活動開始時間，需為 ISO 8601 格式，例如：2026-04-28T08:00:00
        end_time (str): 活動結束時間，需為 ISO 8601 格式，例如：2026-04-28T12:00:00
        
    Returns:
        str: 建立成功後的提示訊息與日曆連結，或失敗時的錯誤訊息。
    """
    try:
        # 取得授權後的 Calendar API 服務實例
        service = get_calendar_service()
        
        # 定義要建立的日曆活動物件資料結構
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

        # 呼叫 API 在 'primary' (使用者的預設日曆) 插入 (insert) 新活動，並執行 (execute)
        event = service.events().insert(calendarId='primary', body=event).execute()
        
        # 成功後回傳帶有 htmlLink (活動網頁連結) 的成功訊息
        return f"已成功在 Google 日曆建立活動！連結: {event.get('htmlLink')}"

    except Exception as e:
        # 若發生錯誤，捕捉並回傳錯誤原因
        return f"建立日曆活動失敗: {str(e)}"
