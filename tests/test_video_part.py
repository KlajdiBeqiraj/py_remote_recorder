"""
Unit tests for video recording functionality in py_remote_recorder.
"""

# Rest of test_video_part.py

# Example usage
import time

from py_remote_recorder.backend.call_apis import (
    save_binary_file,
    start_video_recording,
    stop_video_recording,
)

if __name__ == "__main__":
    current_end_point = "http://192.168.1.9:8000"

    # Start the recording on screen 1
    start_video_recording(end_point=current_end_point, screen_index=2)

    time.sleep(3)

    # Stop the recording and save the file as output.avi
    data = stop_video_recording(end_point=current_end_point)

    save_binary_file(data, output_file="local_file.mp4")
