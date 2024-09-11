from record_screen_apis.backend.record_functions import start_screen_recording, stop_screen_recording

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import threading
import os

app = FastAPI()

# Global variable to store the output file name
current_output_file = None


# Model to accept screen selection
class ScreenSelection(BaseModel):
    screen_index: int


# API endpoint to start recording
@app.post("/start-recording/")
def start_recording(selection: ScreenSelection):
    global current_output_file
    try:
        # Generate output file name based on screen index
        current_output_file = f"output_screen_{selection.screen_index}.avi"

        # Run the recording in a separate thread to avoid blocking the API
        threading.Thread(target=start_screen_recording,
                         args=(selection.screen_index, current_output_file)).start()
        return {"status": "Recording started", "screen_index": selection.screen_index,
                "output_file": current_output_file}
    except ValueError as e:
        return {"error": str(e)}


# Helper function to read the file in chunks
def iter_file(file_path, chunk_size=1024 * 1024):
    with open(file_path, "rb") as file:
        while chunk := file.read(chunk_size):
            yield chunk


# API endpoint to stop recording and stream the recorded file
@app.post("/stop-recording/")
def stop_recording():
    global current_output_file
    stop_screen_recording()  # Stop the recording process

    # Check if the file exists before streaming it
    if current_output_file and os.path.exists(current_output_file):
        return StreamingResponse(iter_file(current_output_file), media_type="video/x-msvideo", headers={
            "Content-Disposition": f"attachment; filename={os.path.basename(current_output_file)}"
        })
    else:
        return {"status": "No recording found or recording was not started properly."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
