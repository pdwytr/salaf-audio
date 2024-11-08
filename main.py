from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
import asyncio
import os
from typing import Dict, Tuple
import time

import wave
import sys

import pyaudio
from mutagen.mp3 import MP3

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class AudioStreamer:
    def __init__(self, audio_files_dir: str):
        self.audio_dir = audio_files_dir
        self.audio_file = "audio.mp3"
        # Get file duration
        audio_path = os.path.join(audio_files_dir, self.audio_file)
        audio = MP3(audio_path)
        self.duration = audio.info.length
        self.start_time = time.time()
        # Initialize current_position based on timestamp
        self.file_size = os.path.getsize(audio_path)
        self.p = pyaudio.PyAudio()
        self.current_position = self.calculate_start_position()



    def calculate_start_position(self) -> int:
        """Calculate the starting position based on current Unix timestamp"""
        position_in_seconds = time.time() % self.duration
        byte_position = int((position_in_seconds / self.duration) * self.file_size)
        # Align to 4 bytes to avoid frame misalignment
        return byte_position - (byte_position % 4)

    def get_next_chunk(self, chunk_size: int = 16384) -> bytes:
        """Returns the next chunk of audio data and current filename"""
        file_path = os.path.join(self.audio_dir, self.audio_file)
        with open(file_path, 'rb') as f:
            f.seek(self.current_position)
            chunk = f.read(chunk_size)
            if chunk:  # If we got some data
                self.current_position += len(chunk)
            else:  # End of file reached
                self.current_position = 0
                # Seek back to beginning of file
                f.seek(0)
                chunk = f.read(chunk_size)
                self.current_position = len(chunk)
            return chunk


                
    def reset_position(self):
        """Reset the position to sync with current timestamp"""
        self.current_position = self.calculate_start_position()

# Initialize streamer
streamer = AudioStreamer("audio_files")

@app.get("/")
async def read_root():
    with open("static/index.html") as f:
        return Response(content=f.read(), media_type="text/html")

@app.get("/stream")
async def stream_audio() -> StreamingResponse:
    # Reset position when new connection is made
    
    streamer.reset_position()
    
    async def audio_generator():
        chunk_size = 4096  # Reduce chunk size for better performance on mobile
        while True:
            chunk = streamer.get_next_chunk(chunk_size)
            if chunk:
                yield chunk
            await asyncio.sleep(0.1)  # Small delay to prevent CPU overload

    return StreamingResponse(
        audio_generator(),
        media_type="audio/mpeg",
        headers={
            "Accept-Ranges": "bytes",
            "Content-Type": "audio/mpeg",
            "Cache-Control": "no-cache"
        }
    )

@app.get("/stream_pyaudio")
async def stream_audio_pyaudio() -> StreamingResponse:
    # Reset position when new connection is made
    streamer.reset_position()

    CHUNK = 1024
    file_path = os.path.join("audio_files", "audio.wav")
    wf = wave.open(file_path, 'rb')
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    pause_event = asyncio.Event()

    async def audio_generator(pause_event):
        try:
            while True:
                if pause_event.is_set():
                    await pause_event.wait()
                data = wf.readframes(CHUNK)
                if not data:
                    break
                stream.write(data)
                yield data
        finally:
            # Close stream and release PortAudio system resources
            stream.close()
            p.terminate()

    return StreamingResponse(
        audio_generator(pause_event),
        media_type="audio/wav",
        headers={
            "Accept-Ranges": "bytes",
            "Content-Type": "audio/wav",
            "Cache-Control": "no-cache"
        }
    )
    # Reset position when new connection is made
    streamer.reset_position()

    CHUNK = 1024
    file_path = os.path.join("audio_files", "audio.wav")
    wf = wave.open(file_path, 'rb')
    p = pyaudio.PyAudio()

    # Open stream

    async def audio_generator():
        try:
            while True:
                data = wf.readframes(CHUNK)
                if not data:
                    break
                
                yield data
        finally:


    return StreamingResponse(
        audio_generator(),
        media_type="audio/wav",
        headers={
            "Accept-Ranges": "bytes",
            "Content-Type": "audio/wav",
            "Cache-Control": "no-cache"
        }
    )
    # Reset position when new connection is made
    streamer.reset_position()
    
    CHUNK = 1024
    file_path = os.path.join("audio_files", "audio.wav")
    wf = wave.open(file_path, 'rb')
    p = pyaudio.PyAudio()
    
    # Open stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    async def audio_generator():
        while True:
            data = wf.readframes(CHUNK)
            if not data:
                break
            stream.write(data)
            yield data

    # Close stream and release PortAudio system resources
    stream.close()
    p.terminate()

    return StreamingResponse(
        audio_generator(),
        media_type="audio/wav",
        headers={
            "Accept-Ranges": "bytes",
            "Content-Type": "audio/wav",
            "Cache-Control": "no-cache"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)