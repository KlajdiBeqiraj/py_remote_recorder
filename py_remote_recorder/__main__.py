"""
This module provides a FastAPI application for screen and audio recording,
along with optional Ngrok support to expose the server publicly.
"""

import argparse
import json
import os
import subprocess
import threading
import time

import requests
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

from py_remote_recorder.backend.audio_record_functions import (
    record_audio,
    stop_audio_recording,
)
from py_remote_recorder.backend.video_record_functions import (
    start_screen_recording,
    stop_screen_recording,
)
from py_remote_recorder.utils import get_logger

app = FastAPI()

# Global variables to store the output file names
screen_output_file = None
audio_output_file = None
logger = get_logger()


# Model to accept screen selection
class ScreenSelection(BaseModel):
    """Model to capture the screen index selection."""

    screen_index: int


# API endpoint to start screen recording
@app.post("/start-screen-recording/")
def start_screen_recording_api(selection: ScreenSelection):
    """
    Start screen recording based on the screen index.

    Args:
        selection (ScreenSelection): The screen index to record.

    Returns:
        dict: Status message and the output file details.
    """
    global screen_output_file
    try:
        # Generate the output file name based on screen index
        screen_output_file = f"output_screen_{selection.screen_index}.mp4"

        # Run the recording in a separate thread to avoid blocking the API
        threading.Thread(
            target=start_screen_recording,
            args=(selection.screen_index, screen_output_file),
        ).start()
        return {
            "status": "Recording started",
            "screen_index": selection.screen_index,
            "output_file": screen_output_file,
        }
    except ValueError as error:
        return {"error": str(error)}


# Helper function to read the file in chunks
def iter_file(file_path, chunk_size=1024 * 1024):
    """
    Read a file in chunks for streaming.

    Args:
        file_path (str): Path to the file.
        chunk_size (int): Size of each chunk in bytes.

    Yields:
        bytes: Chunk of the file.
    """
    with open(file_path, "rb") as file:
        while chunk := file.read(chunk_size):
            yield chunk


# API endpoint to stop screen recording and stream the recorded file
@app.post("/stop-screen-recording/")
def stop_screen_recording_api():
    """
    Stop the screen recording and stream the recorded MP4 file.

    Returns:
        FileResponse: The recorded video file or an error message if not found.
    """
    global screen_output_file
    stop_screen_recording()  # Stop the recording process

    # Ensure the file is fully written and closed
    if screen_output_file and os.path.exists(screen_output_file):
        # Stream the MP4 file to the client
        return FileResponse(
            screen_output_file,
            media_type="video/mp4",  # Correct MIME type for MP4
            filename=os.path.basename(screen_output_file),
        )

    return {"status": "No recording found or recording was not started properly."}


# API endpoint to start audio recording
@app.post("/start-audio-recording/")
def start_audio_recording_api():
    """
    Start the audio recording in a separate thread.

    Returns:
        dict: Status message and the output file details.
    """
    global audio_output_file
    try:
        # Generate the output audio file name
        audio_output_file = "output_audio.wav"

        # Run the recording in a separate thread to avoid blocking the API
        threading.Thread(target=record_audio, args=(audio_output_file,)).start()
        return {
            "status": "Audio recording started",
            "output_file": audio_output_file,
        }
    except Exception as error:  # pylint: disable=broad-except
        return {"error": str(error)}


# API endpoint to stop audio recording and stream the recorded file
@app.post("/stop-audio-recording/")
def stop_audio_recording_api():
    """
    Stop the audio recording and stream the recorded file.

    Returns:
        StreamingResponse: The recorded audio file or error message.
    """
    global audio_output_file
    stop_audio_recording()  # Stop the recording process

    # Check if the audio file exists before streaming it
    if audio_output_file and os.path.exists(audio_output_file):
        return StreamingResponse(
            iter_file(audio_output_file),
            media_type="audio/wav",
            headers={
                "Content-Disposition": f"attachment; "
                f"filename={os.path.basename(audio_output_file)}"
            },
        )
    return {"status": "No audio recording found or recording was not started properly."}


def start_ngrok(ngrok_port):
    """
    Start Ngrok tunnel for the given port.

    Args:
        ngrok_port (int): The local server port to expose.

    Returns:
        str: The public URL of the Ngrok tunnel or None if failed.
    """
    ngrok_command = f"ngrok http {ngrok_port}"
    with subprocess.Popen(ngrok_command.split(), stdout=subprocess.PIPE):
        time.sleep(2)

    try:
        ngrok_url = "http://localhost:4040/api/tunnels"
        tunnel_info = requests.get(ngrok_url).text
        tunnel_data = json.loads(tunnel_info)
        public_url = tunnel_data["tunnels"][0]["public_url"]
        return public_url
    except Exception as error:  # pylint: disable=broad-except
        logger.error("Error retrieving Ngrok URL: %s", error)
        return None


def parse_args():
    """
    Parse command-line arguments to control FastAPI and Ngrok usage.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Run FastAPI with optional Ngrok")
    parser.add_argument(
        "--port", type=int, default=8000, help="Specify the port number"
    )
    parser.add_argument(
        "--use-ngrok", action="store_true", help="Use Ngrok to expose the local server"
    )
    return parser.parse_args()


def log_ngrok_root(public_url):
    """
    Log the Ngrok tunnel public URL.

    Args:
        public_url (str): The public URL of the Ngrok tunnel.
    """
    blue = "\033[94m"
    reset = "\033[0m"
    logger.info("Ngrok tunnel started at %s%s%s", blue, public_url, reset)


def main():
    """
    Main function, run apis
    :return:
    """
    # Parse command-line arguments
    args = parse_args()
    server_port = args.port

    # Start Ngrok if specified
    if args.use_ngrok:
        public_ngrok_url = start_ngrok(server_port)
        if public_ngrok_url:
            log_ngrok_root(public_ngrok_url)
        else:
            logger.error("Ngrok failed to start.")
    else:
        logger.info("Ngrok not used.")

    logger.info("Starting FastAPI on port %d...", server_port)
    uvicorn.run(app, host="0.0.0.0", port=server_port)
