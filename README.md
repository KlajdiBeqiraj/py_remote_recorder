
# PyRemoteRecorder
<img src="https://github.com/KlajdiBeqiraj/py_remote_recorder/blob/main/resources/py_remote_recorder_logo.webp" alt="Image description" width="200" height="200">


`py_remote_recorder` is a Python package designed for remote screen and audio recording via API calls. It provides functionalities to start and stop screen and audio recordings on a specific monitor or input device, along with saving the recordings locally as video or audio files. This package is ideal for remote monitoring, screen capturing, and voice recording applications, with support for FastAPI-based backends and integration with frontend applications via API calls.

## Features

- **Screen Recording**: Record any screen or monitor by specifying the screen index. Capture high-quality screen recordings in `.avi` format.
- **Audio Recording**: Record audio from the system's default input device (microphone) and save it as `.wav` files.
- **API-based Control**: Start and stop both screen and audio recordings through API calls, enabling remote control via HTTP requests.
- **Ngrok Support**: Expose the local FastAPI server to the internet using Ngrok, facilitating easy remote access for external clients.
- **Multi-monitor Support**: Supports systems with multiple monitors, allowing selection of the desired screen for recording.
- **Customizable Frame Rates**: Define the frame rate (fps) for screen recording, with default settings optimized for general use.
- **Data Streaming**: Stream the recorded video or audio data directly via the API.

## Installation

You can install the `py_remote_recorder` package via pip:

```bash
conda install -c anaconda pyaudio
pip install py_remote_recorder
```

Alternatively, you can install it directly from the source:

```bash
git clone https://github.com/your-repo/py_remote_recorder.git
cd py_remote_recorder
pip install poetry
poetry install
```

## Usage

### Basic Setup

First, you'll need to set up and run the FastAPI server provided by the package. The server exposes API endpoints for starting and stopping screen/audio recordings.

```bash
pyrecorder
```

You can start the server with optional arguments:

- `--port`: Specify the port to run the FastAPI server (default is `8000`).
- `--use-ngrok`: Use this flag to expose the server via Ngrok for remote access.

### API Endpoints

#### Start Screen Recording

Start recording a specific screen by specifying the screen index.

**Endpoint**: `POST /start-screen-recording/`

**Request**:

```json
{
  "screen_index": 1
}
```

- `screen_index`: Index of the screen to record (1-based index).

**Response**:

```json
{
  "status": "Recording started",
  "screen_index": 1,
  "output_file": "output_screen_1.avi"
}
```

#### Stop Screen Recording

Stop the ongoing screen recording and download the recorded video.

**Endpoint**: `POST /stop-screen-recording/`

**Response**: Binary video data in `.avi` format.

#### Start Audio Recording

Start recording audio from the system's default microphone.

**Endpoint**: `POST /start-audio-recording/`

**Response**:

```json
{
  "status": "Audio recording started",
  "output_file": "output_audio.wav"
}
```

#### Stop Audio Recording

Stop the ongoing audio recording and download the recorded audio.

**Endpoint**: `POST /stop-audio-recording/`

**Response**: Binary audio data in `.wav` format.

### Example Python Client

Here's a simple Python script to interact with the `py_remote_recorder` API:
1. Video part

```python
from py_remote_recorder.backend.call_apis import (
    save_binary_file,
    start_video_recording,
    stop_video_recording,
)

import time
current_end_point = "yout_end_point"

# Start the recording on screen 1
start_video_recording(end_point=current_end_point, screen_index=1)

time.sleep(3)

# Stop the recording and save the file as output.avi
data = stop_video_recording(end_point=current_end_point)

save_binary_file(data, output_file="local_file.avi")
```
1. Audio part
```python
import time

from py_remote_recorder.backend.call_apis import (
    save_binary_file,
    start_audio_recording,
    stop_audio_recording,
)

current_end_point = "https://3891-93-62-248-214.ngrok-free.app"

# Start the audio recording
start_audio_recording(end_point=current_end_point)

time.sleep(10)

# Stop the recording and save the file as output.wav
audio_data = stop_audio_recording(end_point=current_end_point)

if audio_data:
    save_binary_file(audio_data, output_file="local_audio_file.wav")

```

## Ngrok Integration

1. Download Ngrok from the official website:
https://ngrok.com/download

2. Extract the downloaded file to a folder where you have write permissions (e.g., C:\ngrok on Windows).

3. If you want to access the API remotely, you can use the `--use-ngrok` flag to expose the local FastAPI server. For example:

```bash
pyrecorder --use-ngrok --port 8000
```

The public Ngrok URL will be logged in the terminal, allowing you to interact with the API remotely.

## Development

### Running Tests

To run the unit tests, use the following command:

```bash
pytest
```

Tests are located in the `tests` directory and cover both audio and video recording functionalities.

### Code Quality

The code adheres to PEP8 and Pylint guidelines. Before submitting a pull request, ensure that the code passes Pylint checks:

```bash
pylint py_remote_recorder
```

### Contributions

Contributions are welcome! Please open an issue or submit a pull request if you'd like to contribute to the project.

## Limitations

- **Platform-specific**: The package is tested on Windows and Linux platforms. MacOS support may be limited.
- **Hardware Dependencies**: The quality of screen and audio recording may vary based on the system's hardware capabilities.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any inquiries or issues, please contact the maintainer via email or open an issue on GitHub.
