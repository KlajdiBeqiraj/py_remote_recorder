# Example usage
import time

from py_remote_recorder.backend.call_apis import start_video_recording, stop_video_recording, save_binary_file

if __name__ == "__main__":
    current_end_point = "https://9c9d-93-62-248-214.ngrok-free.app"

    # Start the recording on screen 1
    start_video_recording(end_point=current_end_point, screen_index=1)

    time.sleep(3)

    # Stop the recording and save the file as output.avi
    data = stop_video_recording(end_point=current_end_point)

    save_binary_file(data, output_file="local_file.avi")
