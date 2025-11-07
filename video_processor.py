from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import moviepy.editor
import io
import os
import logging

logger = logging.getLogger(__name__)
SCOPES = ['https://www.googleapis.com/auth/drive']
file_path = "E:/Personal/Work/Python/Projects/video-merger/json-keys/client_secret_44564984563-5hs0bbeafkqinc7r50cb8ccih49ijcp9.apps.googleusercontent.com.json"

class DriveService:
    def __init__(self, file_path:str, SCOPES:str):
        self.file_path = file_path
        self.SCOPES = SCOPES

    def get_drive_service(self, file_path:str, SCOPES:str):
        '''
        Getting google drive access

        Args:
        file_path: the file path to the credential file
        SCOPES: Giving full access to read, modify user's files
        '''
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(file_path, SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        drive_service = build("drive", "v3", credentials=creds)
        # file = drive_service.files().get(
        #     fileId='123dsi-nYM2BSh5p9BlM51XphmPYz0ZUx',
        #     fields='id, name, mimeType, size'
        #     ).execute()
        # print(file)
        return drive_service

    # get_drive_service(file_path, SCOPES)

    def list_all_files(self):
        '''
        listing all the files in the drive folder
        '''
        service = self.get_drive_service(file_path, SCOPES)
        page_token = None
        while True:
            response = service.files().list(
                fields= 'nextPageToken, files(id, name, mimeType)',
                pageToken= page_token
            ).execute()
            for file in response.get('files', []):
                print(f"{file['name']} ({file['id']}) - {file['mimeType']}")
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    def file_downloader(self, url: str, destination:str):
        '''
        Downloads a file from the drive

        url: the file url
        destination: the folder to save the downloaded file
        '''
        service = self.get_drive_service(file_path, SCOPES)
        file_id = url.split('/')[-2]
        request = service.files().get_media(fileId= file_id)
        fh = io.FileIO(destination, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        try:
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%. ")
            print(f"File downloaded to {destination}")
        except FileNotFoundError:
            logger.error("File not Found!")
        except Exception as e:
            logger.error(f"An unexpected error occured: {e}")

    def upload_file(self, local_path:str, drive_folder_id:str = None):
        '''
        Uploads the output to the Drive folder

        Args:
        local_path: the output video's path
        drive_folder_id: the folder id where the file will be uploaded
        '''
        service = self.get_drive_service(file_path, SCOPES)
        file_metadata = {'name': local_path.split('/')[-1]}
        try:
            if drive_folder_id:
                file_metadata['parents'] = [drive_folder_id]
            media = MediaFileUpload(local_path, resumable=True)
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f'File Uploaded. File ID: {file.get('id')}')
        except FileNotFoundError:
            logger.error("File not found!")
        except Exception as e:
            logger.error(f"An Unexpected Error Occured {e}")


    def merger(self, clip_1:str, clip_2:str):
        '''
        merges the two clips into one

        Args:
        clip_1: the first clip
        clip_2: the second clip
        '''
        try:
            clip_one = moviepy.editor.VideoFileClip(clip_1).resize(height=720).set_fps(30)
            clip_two = moviepy.editor.VideoFileClip(clip_2).resize(height=720).set_fps(30)

            Merged_video = moviepy.editor.concatenate_videoclips([clip_one, clip_two], method= 'compose')

            Merged_video.write_videofile('E:/Personal/Work/Python/Projects/video-merger/outputs/output.mp4', codec= 'libx264', audio_codec= 'aac', fps= 30)

            self.upload_file('E:/Personal/Work/Python/Projects/video-merger/outputs/output.mp4', '123dsi-nYM2BSh5p9BlM51XphmPYz0ZUx')

            print('Done')
        
        except FileNotFoundError:
            logger.error("File Not Found!")