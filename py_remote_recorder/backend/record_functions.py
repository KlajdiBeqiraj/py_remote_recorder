import mss
import cv2
import numpy as np
from screeninfo import get_monitors

# Global variable to stop recording
stop_recording_flag = False


# Function to record the screen
def record_screen(screen, output_file="output.avi", fps=20):
    global stop_recording_flag
    monitor = {"top": screen.y, "left": screen.x, "width": screen.width, "height": screen.height}

    with mss.mss() as sct:
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(output_file, fourcc, fps, (screen.width, screen.height))

        try:
            while not stop_recording_flag:
                img = np.array(sct.grab(monitor))  # Capture the screen
                img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Convert to BGR format for OpenCV
                out.write(img_bgr)  # Write the frame to the file
                cv2.imshow("Screen Recording", img_bgr)

                if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit (optional)
                    break
        finally:
            out.release()  # Release the video file
            cv2.destroyAllWindows()


# Function to start screen recording in a separate thread
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
    stop_recording_flag = True
