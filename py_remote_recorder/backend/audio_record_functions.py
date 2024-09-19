"""
This module provides functions for recording audio and stopping the recording process.
"""

import time
import wave

import pyaudio

from py_remote_recorder.utils import get_logger

# Global flag to signal when to stop the audio recording
stop_audio_recording_flag = False

# Parameters for audio recording
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
CHUNK = 1024

logger = get_logger()


def record_audio(output_file="output_audio.wav"):
    """
    Function to record audio and save it to a .wav file.

    Args:
        output_file (str): The path to the output .wav file (default: 'output_audio.wav').
    """
    global stop_audio_recording_flag
    stop_audio_recording_flag = False  # Reset the flag at the beginning

    # Initialize PyAudio instance
    audio_interface = pyaudio.PyAudio()

    # Open the stream for audio input
    stream = audio_interface.open(
        format=AUDIO_FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    logger.info("Recording audio...")

    frames = []

    # Record until the stop flag is set to True
    while not stop_audio_recording_flag:
        data = stream.read(CHUNK)
        frames.append(data)
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio_interface.terminate()

    # Save the recorded audio as a .wav file
    with wave.open(output_file, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio_interface.get_sample_size(AUDIO_FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))

    logger.info("Audio saved to %s", output_file)


def stop_audio_recording():
    """
    Function to stop the audio recording by setting the stop flag.
    """
    global stop_audio_recording_flag
    # Set the stop flag to True to break the recording loop
    stop_audio_recording_flag = True
    # Ensure the recording process has completely stopped and the file is closed
    time.sleep(1)  # Add a short delay to ensure file writing completes
