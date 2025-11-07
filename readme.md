# Python Video Merger (Flask + Google Drive + MoviePy)

This project lets you enter two Google Drive file URLs or IDs, download both videos, merge them into a single MP4 using MoviePy, and upload the final merged output back to your Google Drive.  
It uses OAuth2 locally for authentication, Flask for the UI, and the Google Drive API for file operations.

## Features

- Download videos directly from Google Drive by URL or file ID.
- Merge videos using MoviePy (concatenation, normalized to 720p @ 30fps).
- Upload the merged output to a specified Google Drive folder.
- Simple HTML UI built with Flask.
- Automatic token generation and caching via `token.json`.

## Requirements

- Python 3.13
- Google API credentials (`client_secret_xxx.json`)
- Browser access for OAuth2 login

Install the required packages -> pip install -r requirements.txt

## How It Works

### 1. User enters two Google Drive URLs or file IDs  
The Flask app receives them from `form.html`.

### 2. Each URL is converted to a file ID  
Handles both direct IDs and full URLs.

### 3. Files are downloaded from Drive  
Stored under `video_clips/`.

### 4. Videos are merged  
Processed using MoviePy, normalized to:
- height: 720px  
- fps: 30  

Output saved to `outputs/output.mp4`.

### 5. Final video is uploaded to a Drive folder  
Folder ID is configured inside `merger()`.


## Environment Setup

1. Place your Google API client secret file inside `json-keys/`.
2. Update the path in `video_processor.py`:


3. First run will open a browser for OAuth login.
4. `token.json` will be created and reused automatically.

## Running the Application

Then open:

http://127.0.0.1:5000/


Enter two Google Drive video URLs/IDs and click **Merge**.

## Notes

- Only MP4 files are supported.
- MoviePy 2.2.1 is required because Pillow’s `ANTIALIAS` was removed.
- The merged file uploads to the folder ID you hardcoded in `merger()`.

## Logging

All important operations use:

logger.info()
logger.error()


Logs appear directly in the terminal where you run `main.py`.