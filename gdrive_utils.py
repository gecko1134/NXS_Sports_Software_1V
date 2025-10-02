
import os, json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
def upload_file(local_path, filename=None, folder_id=None):
    folder_id = folder_id or os.getenv("GOOGLE_DRIVE_FOLDER_ID")
    sa_json=os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"); sa_file=os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
    scopes=["https://www.googleapis.com/auth/drive.file"]
    if sa_json: creds=service_account.Credentials.from_service_account_info(json.loads(sa_json), scopes=scopes)
    elif sa_file and os.path.exists(sa_file): creds=service_account.Credentials.from_service_account_file(sa_file, scopes=scopes)
    else: raise RuntimeError("Missing Google Drive credentials")
    service=build("drive","v3",credentials=creds)
    media=MediaFileUpload(local_path,resumable=True)
    body={"name": filename or os.path.basename(local_path)}
    if folder_id: body["parents"]=[folder_id]
    file=service.files().create(body=body,media_body=media,fields="id,name,webViewLink,webContentLink").execute()
    return file
