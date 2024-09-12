import requests
import time
import os

from record_screen_apis.utils import get_logger

logger = get_logger()

# Function to start screen recording
def start_video_recording(end_point: str, screen_index: int):
    url = end_point + "/start-screen-recording/"
    payload = {"screen_index": screen_index}

    # Send the POST request to start recording
    response = requests.post(url, json=payload)

    # Print the response
    if response.status_code == 200:
        logger.info(f"Recording started: {response.json()}")
    else:
        logger.error(f"Failed to start recording: {response.status_code}, {response.text}")


def stop_video_recording(end_point: str):
    url = end_point + "/stop-screen-recording/"

    # Send the POST request to stop recording
    response = requests.post(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Collect the video data in chunks and return it
        video_data = b""  # Initialize an empty byte string
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                video_data += chunk  # Accumulate the chunks into the byte string
        logger.info("Recording stopped and video data collected.")
        return video_data  # Return the video data as byte array
    else:
        logger.error(f"Failed to stop recording: {response.status_code}, {response.text}")
        return None


# Function to start audio recording
def start_audio_recording(end_point: str):
    url = f"{end_point}/start-audio-recording/"

    response = requests.post(url)

    if response.status_code == 200:
        logger.info(f"Audio recording started: {response.json()}")
    else:
        logger.error(f"Failed to start audio recording: {response.status_code}, {response.text}")


# Function to stop audio recording and retrieve the binary data
def stop_audio_recording(end_point: str):
    url = f"{end_point}/stop-audio-recording/"

    response = requests.post(url, stream=True)

    if response.status_code == 200:
        audio_data = b""  # Initialize an empty byte string
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                audio_data += chunk  # Accumulate the chunks into the byte string
        logger.info("Audio recording stopped and data collected.")
        return audio_data  # Return the binary audio data
    else:
        logger.error(f"Failed to stop audio recording: {response.status_code}, {response.text}")
        return None


def save_binary_file(video_data, output_file):
    try:
        with open(output_file, 'wb') as file:
            file.write(video_data)
        logger.info(f"Save file {os.path.abspath(output_file)}")
    except Exception as e:
        logger.error(f"Saving error: {e}")
