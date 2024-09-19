"""
This module provides functions to record the screen using OpenCV and MSS,
allowing the recording of a selected screen and saving the output as a video file.
"""

import time

import cv2
import mss
import numpy as np
import pyautogui
from screeninfo import get_monitors

# Global flag to signal when to stop the recording
stop_recording_flag = False
pyautogui.FAILSAFE = False  # Disable PyAutoGUI failsafe


def record_screen(screen, output_file="output.avi", fps=20):
    """
    Record the selected screen and save the recording to a video file.

    Args:
        screen: The screen object containing position and dimensions.
        output_file (str): The path to the output video file (default: 'output.avi').
        fps (int): Frames per second for the video recording (default: 20).
    """
    monitor = {
        "top": screen.y,
        "left": screen.x,
        "width": screen.width,
        "height": screen.height,
    }

    with mss.mss() as sct:
        # Set up the video writer with the avc1 codec
        fourcc = cv2.VideoWriter_fourcc(*"avc1")
        out = cv2.VideoWriter(output_file, fourcc, fps, (screen.width, screen.height))

        try:
            while not stop_recording_flag:  # Check stop flag inside the loop
                # Capture the screen and convert it to a NumPy array
                img = np.array(sct.grab(monitor))

                # Convert the captured image to BGR format for OpenCV
                img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

                # Write the BGR frame to the video file
                out.write(img_bgr)

                # Delay to maintain the desired frame rate
                time.sleep(1 / fps)
        finally:
            # Release the video writer and close OpenCV windows
            out.release()
            cv2.destroyAllWindows()


def start_screen_recording(screen_index: int, output_file="output.avi"):
    """
    Start screen recording for the specified screen index.

    Args:
        screen_index (int): The index of the screen to record (1-based index).
        output_file (str): The path to the output video file (default: 'output.avi').

    Raises:
        ValueError: If the screen index is invalid.
    """
    global stop_recording_flag
    stop_recording_flag = False  # Reset the stop flag before starting

    # Get all available screens
    screens = get_monitors()

    # Validate the screen index
    if screen_index < 1 or screen_index > len(screens):
        raise ValueError("Invalid screen index")

    # Select the screen based on the provided index
    selected_screen = screens[screen_index - 1]

    # Start recording the selected screen
    record_screen(selected_screen, output_file=output_file)


def stop_screen_recording():
    """
    Function to stop the screen recording by setting the stop flag.
    Ensure that the file is fully written and closed before proceeding.
    """
    global stop_recording_flag
    stop_recording_flag = True  # Set stop flag to True to break the recording loop

    # Ensure the recording process has completely stopped and the file is closed
    time.sleep(1)  # Add a short delay to ensure file writing completes
