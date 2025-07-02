#!/usr/bin/env python3
"""Entry point orchestrating capture, transcription and overlay."""

from __future__ import annotations

import argparse
import getpass
import os
import threading
import time
from datetime import datetime

from audio_capture import AudioCapture
from transcriber import WhisperTranscriber
from transcript_buffer import TranscriptBuffer
from display import DisplayWindow
from output_writer import save_transcript
from ui_controller import UIController

def main() -> None:
    parser = argparse.ArgumentParser(description="WhisperLite Transcription App")
    parser.add_argument("--model", type=str, default="models/ggml-tiny.en.bin",
                        help="Path to the Whisper model file (e.g., models/ggml-tiny.en.bin)")
    args = parser.parse_args()

    buffer = TranscriptBuffer()
    ui = UIController()

    display = DisplayWindow(ui.request_stop)
    display.set_buffer(buffer)
    threading.Thread(target=display.start, daemon=True).start()

    audio = AudioCapture()
    try:
        audio.start()
    except Exception:
        print("Failed to start audio capture")
        return

    try:
        transcriber = WhisperTranscriber(args.model)
    except FileNotFoundError as exc:
        print(exc)
        audio.stop()
        return

    def capture_loop() -> None:
        while not ui.should_stop():
            chunk = audio.get_chunk(timeout=0.1)
            if chunk:
                text = transcriber.transcribe_chunk(chunk)
                if text:
                    buffer.append(text)

    worker = threading.Thread(target=capture_loop, daemon=True)
    worker.start()

    try:
        while not ui.should_stop():
            time.sleep(0.1)
    except KeyboardInterrupt:
        ui.request_stop()

    audio.stop()
    worker.join(timeout=1)
    display.signal_stop()

    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    username = getpass.getuser()
    full_text = buffer.full_text()
    path = save_transcript(full_text, username, datetime.now(), downloads)
    buffer.clear()
    print(f"Transcript saved to {path}")


if __name__ == "__main__":
    main()
