from flask import Flask, render_template, request
from video_processor import DriveService, file_path, SCOPES
import logging

logging.basicConfig(
    level=logging.INFO,
    format= "%(levelname)s: %(message)s"
)
import video_processor
print(video_processor.__file__)

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("form.html")

@app.route("/submit", methods= ['POST'])
def merge():
    if request.method == "POST":
        id_01 = request.form.get('id01')
        id_02 = request.form.get('id02')
        print(id_01, id_02)

        drive_obj = DriveService(file_path, SCOPES)
        drive_obj.file_downloader(id_01, r'E:/Personal/Work/Python/Projects/video-merger/video_clips/clip1.mp4')
        drive_obj.file_downloader(id_02, r'E:/Personal/Work/Python/Projects/video-merger/video_clips/clip2.mp4')
        drive_obj.merger(r'E:/Personal/Work/Python/Projects/video-merger/video_clips/clip1.mp4', r'E:/Personal/Work/Python/Projects/video-merger/video_clips/clip2.mp4')

    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug= True)