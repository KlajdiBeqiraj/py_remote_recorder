import requests
import time

# Function to start screen recording
def start_recording(end_point: str, screen_index: int):
    url = end_point + "/start-recording/"
    payload = {"screen_index": screen_index}

    # Send the POST request to start recording
    response = requests.post(url, json=payload)

    # Print the response
    if response.status_code == 200:
        print(f"Recording started: {response.json()}")
    else:
        print(f"Failed to start recording: {response.status_code}, {response.text}")


# Function to stop screen recording and download the video
def stop_recording(end_point: str, output_file: str):
    url = end_point + "/stop-recording/"

    # Send the POST request to stop recording
    response = requests.post(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the video file
        with open(output_file, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"Recording stopped and video saved as: {output_file}")
    else:
        print(f"Failed to stop recording: {response.status_code}, {response.text}")


# Example usage
if __name__ == "__main__":
    end_point = " http://127.0.0.1:8000"
    # Start the recording on screen 1
    start_recording(end_point=end_point, screen_index=1)

    time.sleep(10)

    # Stop the recording and save the file as output.avi
    stop_recording(end_point=end_point, output_file="output_screen_1.avi")