from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2 import service_account
import io
from config import DRIVE_FOLDER_ID

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service_account.json'

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=creds)

def prepare_video_folder(file_id):

    file = service.files().get(fileId=file_id,
                              fields='name, parents').execute()

    filename = file['name']
    parent = file['parents'][0]

    folder_name = filename.split(".")[0]

    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [DRIVE_FOLDER_ID]
    }

    folder = service.files().create(body=folder_metadata,
                                    fields='id').execute()

    folder_id = folder['id']

    service.files().update(
        fileId=file_id,
        addParents=folder_id,
        removeParents=parent,
        fields='id, parents'
    ).execute()

    return folder_id, filename

def download_video(file_id):

    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO("video.mp4", 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()

    return "video.mp4"

def upload_result(file_path, folder_id):

    file_metadata = {'name': file_path,
                     'parents': [folder_id]}

    media = MediaFileUpload(file_path)

    service.files().create(
        body=file_metadata,
        media_body=media).execute()

def mark_processed(folder_id):

    file_metadata = {'name': 'processed.txt',
                     'parents': [folder_id]}

    service.files().create(body=file_metadata).execute()

def already_processed(folder_id):

    query = f"'{folder_id}' in parents and name='processed.txt'"

    res = service.files().list(q=query).execute()

    return len(res.get('files', [])) > 0
