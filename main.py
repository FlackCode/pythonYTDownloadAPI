from fastapi import FastAPI, HTTPException
from pytube import YouTube
import requests
import os

app = FastAPI()


def download_video(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        video_file = stream.download(output_path="downloads", filename="video")
        # Add ".mp4" extension to the filename
        video_file_with_extension = os.path.splitext(video_file)[0] + ".mp4"
        os.rename(video_file, video_file_with_extension)
        return video_file_with_extension
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download/")
async def download(url: str):
    try:
        filename = download_video(url)
        return {"filename": filename, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
