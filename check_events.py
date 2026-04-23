import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar.events.readonly']

def get_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds_path = os.getenv("GOOGLE_CALENDAR_CREDENTIALS", "key/credentials.json")
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def list_events(date_str):
    print(f"Checking events for {date_str}...")
    try:
        service = get_calendar_service()
        
        start_dt = datetime.datetime.fromisoformat(f"{date_str}T00:00:00Z")
        end_dt = datetime.datetime.fromisoformat(f"{date_str}T23:59:59Z")
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=start_dt.isoformat(),
            timeMax=end_dt.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            print('No events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"{start}: {event['summary']}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    list_events("2024-04-28")
    print("-" * 20)
    list_events("2026-04-28")
