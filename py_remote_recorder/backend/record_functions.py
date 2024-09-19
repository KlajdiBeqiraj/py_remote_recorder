"""
recording functions
"""

import cv2
import mss
import numpy as np
from screeninfo import get_monitors

# Global flag to signal when to stop the screen recording
stop_recording_flag = False


def record_screen(screen, output_file="output.mp4", fps=20):
    """
    Function to record the selected screen and save it to a video file.

    Args:
        screen: The screen object containing position and dimensions.
        output_file (str): The path to the output video file (default: 'output.mp4').
        fps (int): Frames per second for the video recording (default: 20).
    """
    global stop_recording_flag

    # Define the monitor area to capture based on screen properties
    monitor = {
        "top": screen.y,
        "left": screen.x,
        "width": screen.width,
        "height": screen.height,
    }

    with mss.mss() as sct:
        # Set up video writer with the MP4 codec (H.264)
        fourcc = cv2.VideoWriter_fourcc(*"avc1")  # More compatible codec
        out = cv2.VideoWriter(output_file, fourcc, fps, (screen.width, screen.height))

        try:
            while not stop_recording_flag:
                # Capture the screen and convert it to a NumPy array
                img = np.array(sct.grab(monitor))

                # Convert the captured image to BGR format for OpenCV
                img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

                # Write the BGR frame to the video file
                out.write(img_bgr)

                # Display the recording in a window (optional)
                cv2.imshow("Screen Recording", img_bgr)

                # Optional: Press 'q' to stop recording manually
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        finally:
            # Release the video writer and close the OpenCV window
            out.release()
            cv2.destroyAllWindows()


def start_screen_recording(screen_index: int, output_file="output.mp4"):
    """
    Start screen recording for a specific screen index.

    Args:
        screen_index (int): The index of the screen to record (1-based index).
        output_file (str): The path to the output video file (default: 'output.mp4').

    Raises:
        ValueError: If the screen index is invalid.
    """
    global stop_recording_flag
    stop_recording_flag = False  # Reset stop flag before starting

    # Get all available monitors
    screens = get_monitors()

    # Validate the screen index
    if screen_index < 1 or screen_index > len(screens):
        raise ValueError("Invalid screen index")

    # Select the screen based on the provided index
    selected_screen = screens[screen_index - 1]

    # Start the recording process for the selected screen
    record_screen(selected_screen, output_file=output_file)


def stop_screen_recording():
    """
    Function to stop the screen recording by setting the stop flag.
    """
    global stop_recording_flag
    stop_recording_flag = True  # Set stop flag to True to break the recording loop
