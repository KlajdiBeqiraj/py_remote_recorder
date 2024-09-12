"""
This module provides functions to interact with remote APIs for starting/stopping
screen and audio recordings, and saving the binary data to files.
"""

import os

import requests

from py_remote_recorder.utils import get_logger

logger = get_logger()


def start_video_recording(end_point: str, screen_index: int):
    """
    Sends a POST request to start screen recording.

    Args:
        end_point (str): The endpoint URL of the recording server.
        screen_index (int): The index of the screen to record.

    Returns:
        None
    """
    url = f"{end_point}/start-screen-recording/"
    payload = {"screen_index": screen_index}

    # Send the POST request to start recording
    response = requests.post(url, json=payload)

    # Log the response
    if response.status_code == 200:
        logger.info("Recording started: %s", response.json())
    else:
        logger.error(
            "Failed to start recording: %d, %s", response.status_code, response.text
        )


def stop_video_recording(end_point: str):
    """
    Sends a POST request to stop screen recording and returns the video data.

    Args:
        end_point (str): The endpoint URL of the recording server.

    Returns:
        bytes: The binary video data, or None if the request failed.
    """
    url = f"{end_point}/stop-screen-recording/"

    # Send the POST request to stop recording
    response = requests.post(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        video_data = b""  # Initialize an empty byte string
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                video_data += chunk  # Accumulate the chunks into the byte string
        logger.info("Recording stopped and video data collected.")
        return video_data  # Return the video data as byte array
    logger.error(
        "Failed to stop recording: %d, %s", response.status_code, response.text
    )
    return None


def start_audio_recording(end_point: str):
    """
    Sends a POST request to start audio recording.

    Args:
        end_point (str): The endpoint URL of the recording server.

    Returns:
        None
    """
    url = f"{end_point}/start-audio-recording/"

    # Send the POST request to start recording
    response = requests.post(url)

    # Log the response
    if response.status_code == 200:
        logger.info("Audio recording started: %s", response.json())
    else:
        logger.error(
            "Failed to start audio recording: %d, %s",
            response.status_code,
            response.text,
        )


def stop_audio_recording(end_point: str):
    """
    Sends a POST request to stop audio recording and returns the audio data.

    Args:
        end_point (str): The endpoint URL of the recording server.

    Returns:
        bytes: The binary audio data, or None if the request failed.
    """
    url = f"{end_point}/stop-audio-recording/"

    # Send the POST request to stop recording
    response = requests.post(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        audio_data = b""  # Initialize an empty byte string
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                audio_data += chunk  # Accumulate the chunks into the byte string
        logger.info("Audio recording stopped and data collected.")
        return audio_data  # Return the binary audio data
    logger.error(
        "Failed to stop audio recording: %d, %s", response.status_code, response.text
    )
    return None


def save_binary_file(data: bytes, output_file: str):
    """
    Saves binary data to a file.

    Args:
        data (bytes): The binary data to save.
        output_file (str): The path to the output file.

    Returns:
        None
    """
    try:
        with open(output_file, "wb") as file:
            file.write(data)
        logger.info("File saved: %s", os.path.abspath(output_file))
    except Exception as error:  # pylint: disable=broad-except
        logger.error("Error saving file: %s", error)
