import pyaudio
import wave
import time

from record_screen_apis.utils import get_logger

# Global variable for stopping the recording
stop_audio_recording_flag = False

# Parameters for audio recording
audio_format = pyaudio.paInt16
channels = 2
rate = 44100
chunk = 1024

logger = get_logger()


# Function to record audio
def record_audio(output_file="output_audio.wav"):
    global stop_audio_recording_flag

    p = pyaudio.PyAudio()

    # Open the stream for recording
    stream = p.open(format=audio_format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    logger.info("Recording audio...")

    frames = []

    # Start the recording loop
    while not stop_audio_recording_flag:
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded frames as a .wav file
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(audio_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    logger.info(f"Audio saved to {output_file}")


# Function to stop audio recording
def stop_audio_recording():
    global stop_audio_recording_flag
    stop_audio_recording_flag = True  # Set the stop flag to True to break the loop
