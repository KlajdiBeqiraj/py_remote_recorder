"""
Unit tests for audio recording functionality in py_remote_recorder.
"""

# Rest of test_audio_part.py


import time

from py_remote_recorder.backend.call_apis import (
    save_binary_file,
    start_audio_recording,
    stop_audio_recording,
)

if __name__ == "__main__":
    current_end_point = "https://3891-93-62-248-214.ngrok-free.app"

    # Start the audio recording
    start_audio_recording(end_point=current_end_point)

    time.sleep(10)

    # Stop the recording and save the file as output.wav
    audio_data = stop_audio_recording(end_point=current_end_point)

    if audio_data:
        save_binary_file(audio_data, output_file="local_audio_file.wav")
