import json
import time

import requests
import uvicorn

from record_screen_apis.backend.audio_record_functions import record_audio, stop_audio_recording
from record_screen_apis.backend.video_record_functions import start_screen_recording, stop_screen_recording

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import threading
import os
import subprocess
import argparse
import logging

from record_screen_apis.utils import get_logger

app = FastAPI()

# Global variable to store the output file name
current_screen_output_file = None
# Global variable to store the audio output file name
current_audio_output_file = None
logger = get_logger()


# Model to accept screen selection
class ScreenSelection(BaseModel):
    screen_index: int


# API endpoint to start recording
@app.post("/start-screen-recording/")
def start_screen_recording_api(selection: ScreenSelection):
    global current_screen_output_file
    try:
        # Generate output file name based on screen index
        current_screen_output_file = f"output_screen_{selection.screen_index}.avi"

        # Run the recording in a separate thread to avoid blocking the API
        threading.Thread(target=start_screen_recording,
                         args=(selection.screen_index, current_screen_output_file)).start()
        return {"status": "Recording started", "screen_index": selection.screen_index,
                "output_file": current_screen_output_file}
    except ValueError as e:
        return {"error": str(e)}


# Helper function to read the file in chunks
def iter_file(file_path, chunk_size=1024 * 1024):
    with open(file_path, "rb") as file:
        while chunk := file.read(chunk_size):
            yield chunk


# API endpoint to stop recording and stream the recorded file
@app.post("/stop-screen-recording/")
def stop_screen_recording_api():
    global current_screen_output_file
    stop_screen_recording()  # Stop the recording process

    # Check if the file exists before streaming it
    if current_screen_output_file and os.path.exists(current_screen_output_file):
        return StreamingResponse(iter_file(current_screen_output_file), media_type="video/x-msvideo", headers={
            "Content-Disposition": f"attachment; filename={os.path.basename(current_screen_output_file)}"
        })
    else:
        return {"status": "No recording found or recording was not started properly."}


# API endpoint to start audio recording
@app.post("/start-audio-recording/")
def start_audio_recording_api():
    global current_audio_output_file
    try:
        # Generate the output audio file name
        current_audio_output_file = f"output_audio.wav"

        # Run the recording in a separate thread to avoid blocking the API
        threading.Thread(target=record_audio, args=(current_audio_output_file,)).start()
        return {"status": "Audio recording started", "output_file": current_audio_output_file}
    except Exception as e:
        return {"error": str(e)}


# API endpoint to stop audio recording and stream the recorded file
@app.post("/stop-audio-recording/")
def stop_audio_recording_api():
    global current_audio_output_file
    stop_audio_recording()  # Stop the recording process

    # Check if the audio file exists before streaming it
    if current_audio_output_file and os.path.exists(current_audio_output_file):
        return StreamingResponse(iter_file(current_audio_output_file), media_type="audio/wav", headers={
            "Content-Disposition": f"attachment; filename={os.path.basename(current_audio_output_file)}"
        })
    else:
        return {"status": "No audio recording found or recording was not started properly."}


def start_ngrok(port):
    ngrok_command = f"ngrok http {port}"
    ngrok_process = subprocess.Popen(ngrok_command.split(), stdout=subprocess.PIPE)

    time.sleep(2)

    try:
        ngrok_url = "http://localhost:4040/api/tunnels"
        tunnel_info = requests.get(ngrok_url).text
        tunnel_data = json.loads(tunnel_info)
        public_url = tunnel_data['tunnels'][0]['public_url']
        return public_url
    except Exception as e:
        logger.error(f"Errore nel recupero dell'URL di Ngrok: {e}")
        return None


def parse_args():
    parser = argparse.ArgumentParser(description="Run FastAPI with optional Ngrok")
    parser.add_argument("--port", type=int, default=8000, help="Specify the port number")
    parser.add_argument("--use-ngrok", action="store_true", help="Use Ngrok to expose the local server")
    return parser.parse_args()


def log_ngrok_root(public_url):
    blue = "\033[94m"
    reset = "\033[0m"
    logger.info(f"Ngrok tunnel started at {blue}{public_url}{reset}")


if __name__ == "__main__":
    args = parse_args()
    port = args.port

    if args.use_ngrok:
        public_url = start_ngrok(port)
        if public_url:
            log_ngrok_root(public_url)
        else:
            logger.error("Ngrok failed to start.")
    else:
        logger.info("Ngrok not used.")

    logger.info(f"Starting FastAPI on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
