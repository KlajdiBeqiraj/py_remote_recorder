import mss
import cv2
import numpy as np
from screeninfo import get_monitors
import pyautogui
import time

# Global variable to stop recording
stop_recording_flag = False
pyautogui.FAILSAFE = False



# Function to record the screen
def record_screen(screen, output_file="output.avi", fps=20):
    monitor = {"top": screen.y, "left": screen.x, "width": screen.width, "height": screen.height}

    with mss.mss() as sct:
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(output_file, fourcc, fps, (screen.width, screen.height))

        try:
            while not stop_recording_flag:  # Check the stop flag inside the loop
                img = np.array(sct.grab(monitor))  # Capture the screen
                img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Convert to BGR format for OpenCV
                out.write(img_bgr)  # Write the frame to the video file

                time.sleep(1 / fps)  # Add a small delay to match the desired frame rate

        finally:
            out.release()  # Release the video file
            cv2.destroyAllWindows()


def start_screen_recording(screen_index: int, output_file="output.avi"):
    global stop_recording_flag
    stop_recording_flag = False  # Reset stop flag

    screens = get_monitors()  # Get all available screens
    if screen_index < 1 or screen_index > len(screens):
        raise ValueError("Invalid screen index")

    selected_screen = screens[screen_index - 1]  # Select the screen by index
    record_screen(selected_screen, output_file=output_file)


# Function to stop screen recording
def stop_screen_recording():
    global stop_recording_flag
    stop_recording_flag = True  # Set the stop flag to True to break the loop
