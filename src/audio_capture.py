"""
audio_capture.py — WhisperLite
Captures real-time microphone input, slices it into precise audio chunks, and prepares for streaming STT.

- Uses sounddevice for cross-platform streaming
- Buffers output as .wav for whisper.cpp
- No internet, telemetry, or cloud
"""

import os
import sys
import threading
import queue
import logging
import time
import wave
try:
    import sounddevice as sd
except Exception as exc:  # ModuleImport or portaudio missing
    sd = None  # type: ignore
    import warnings
    warnings.warn(f"sounddevice unavailable: {exc}")

class AudioCapture:
    """
    Real-time, cross-platform microphone capture.
    Slices audio into 1–2 second, whisper.cpp-compatible .wav chunks.
    """

    def __init__(
        self,
        chunk_duration_sec=1.5,
        sample_rate=16000,
        channels=1,
        dtype='int16',
        output_dir="chunks"
    ):
        self.chunk_duration_sec = chunk_duration_sec
        self.sample_rate = sample_rate
        self.channels = channels
        self.dtype = dtype
        self.frames_per_chunk = int(self.sample_rate * self.chunk_duration_sec)
        self.device_info = None

        # Internal state
        self._chunk_counter = 0
        self._audio_queue = queue.Queue()
        self._stream = None
        self._stop_event = threading.Event()
        self._buffer = bytearray()
        self._last_chunk_path = None
        self._lock = threading.Lock()

        # Output location
        self.chunks_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), output_dir
        )
        os.makedirs(self.chunks_dir, exist_ok=True)

        # Logging setup
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt="%H:%M:%S"
        )
        self.logger = logging.getLogger("AudioCapture")

    def _list_default_input_device(self):
        """Detect and log the default microphone info."""
        if sd is None:
            self.logger.error("sounddevice not available; skipping device query")
            return False
        try:
            self.device_info = sd.query_devices(kind='input')
            self.logger.info(
                f"Using input device: {self.device_info['name']} (SR {self.device_info['default_samplerate']:.0f}Hz)"
            )
            return True
        except Exception as e:
            self.logger.error(f"No default input device found: {e}")
            return False

    def _write_wav_file(self, frames, chunk_idx):
        """Write frames to a .wav chunk, place on the chunk queue."""
        filename = f"chunk_{chunk_idx:03d}.wav"
        filepath = os.path.join(self.chunks_dir, filename)
        try:
            with wave.open(filepath, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(2)
                wf.setframerate(self.sample_rate)
                wf.writeframes(frames)
            with self._lock:
                self._last_chunk_path = filepath
            self._audio_queue.put(filepath)
            self.logger.info(f"Chunk {chunk_idx:03d} saved: {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to write {filepath}: {e}")

    def _callback(self, indata, frames, time_info, status):
        """Sounddevice stream callback: buffers and slices audio."""
        if status:
            self.logger.warning(f"Stream status: {status}")

        if self._stop_event.is_set():
            raise sd.CallbackStop

        self._buffer.extend(indata.tobytes())
        bytes_per_sample = 2
        bytes_per_chunk = self.frames_per_chunk * self.channels * bytes_per_sample

        # Write full-sized chunks from the buffer
        while len(self._buffer) >= bytes_per_chunk:
            chunk_bytes = self._buffer[:bytes_per_chunk]
            del self._buffer[:bytes_per_chunk]
            self._chunk_counter += 1
            self._write_wav_file(chunk_bytes, self._chunk_counter)

    def start(self):
        """Start capturing audio, spawn sounddevice stream."""
        if sd is None:
            self.logger.error("Audio capture unavailable: sounddevice missing")
            return
        if not self._list_default_input_device():
            self.logger.error("Audio capture aborted: no input device.")
            return
        try:
            self._stop_event.clear()
            self._chunk_counter = 0
            self._buffer = bytearray()
            self._stream = sd.InputStream(
                samplerate=self.sample_rate,
                device=None,
                channels=self.channels,
                dtype=self.dtype,
                blocksize=0,
                callback=self._callback,
                latency='low',
            )
            self._stream.start()
            self.logger.info("Audio capture started.")
        except Exception as e:
            self.logger.error(f"Audio stream start failed: {e}")

    def stop(self):
        """Stop audio stream and release device."""
        self._stop_event.set()
        if self._stream:
            try:
                self._stream.stop()
                self._stream.close()
                self.logger.info("Audio capture stopped.")
            except Exception as e:
                self.logger.error(f"Error stopping stream: {e}")
            self._stream = None

    def get_last_chunk_path(self):
        """Return last chunk .wav path or None."""
        with self._lock:
            return self._last_chunk_path

    def get_chunk(self, block=True, timeout=None):
        """Retrieve the next chunk file path from the queue."""
        try:
            return self._audio_queue.get(block=block, timeout=timeout)
        except queue.Empty:
            return None

def main():
    """
    Example/test: Capture 5 chunks, then stop and print the last chunk's path.
    """
    ac = AudioCapture(chunk_duration_sec=1.5)
    try:
        ac.start()
        max_chunks = 5
        start = time.time()
        while ac._chunk_counter < max_chunks and (time.time() - start) < 30:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Interrupted.")
    finally:
        ac.stop()
        last_path = ac.get_last_chunk_path()
        if last_path:
            print(f"Last chunk saved: {last_path}")
        else:
            print("No chunks saved.")

if __name__ == "__main__":
    main()
