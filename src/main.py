#!/usr/bin/env python3
"""Entry point orchestrating capture, transcription and overlay."""

from __future__ import annotations

import argparse
import getpass
import os
import threading
import time
import sys
import json
import soundfile as sf
import tempfile
from datetime import datetime

from audio_capture import AudioCapture
from transcriber import WhisperTranscriber
from transcript_buffer import TranscriptBuffer
from display import DisplayWindow
from output_writer import save_transcript
from ui_controller import UIController

def launch_gui_mode(args) -> None:
    buffer = TranscriptBuffer()
    ui = UIController()

    display = DisplayWindow(ui.request_stop)
    display.set_buffer(buffer)
    threading.Thread(target=display.start, daemon=True).start()

    audio = AudioCapture()
    try:
        audio.start()
    except Exception:
        print("Failed to start audio")
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
                segments = transcriber.transcribe_chunk(chunk)
                if segments:
                    buffer.append(segments)

    worker = threading.Thread(target=capture_loop, daemon=True).start()

    try:
        while not ui.should_stop():
            time.sleep(0.1)
    except KeyboardInterrupt:
        ui.request_stop()

    audio.stop()
    worker.join(timeout=1)
    display.signal_stop()

def cli_main(args) -> None:
    # Check for mock transcription output for testing purposes
    if os.environ.get("MOCK_TRANSCRIPTION_OUTPUT") == "true":
        all_segments = [
            {"start": "00:00:00.000", "end": "00:00:03.000", "text": "This is a mock transcription."},
            {"start": "00:00:03.500", "end": "00:00:06.000", "text": "CLI mode is working."}
        ]
    else:
        try:
            transcriber = WhisperTranscriber(args.model, language=args.language)
        except FileNotFoundError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

        if not os.path.exists(args.input):
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)

        all_segments = []
        try:
            with sf.SoundFile(args.input, 'r') as f:
                samplerate = f.samplerate
                channels = f.channels
                # Whisper.cpp typically expects 16kHz mono audio
                if samplerate != 16000 or channels != 1:
                    print("Warning: Input audio not 16kHz mono. Resampling/downmixing might be needed for optimal results.", file=sys.stderr)

                # Process in 1.5 second chunks (adjust as needed)
                chunk_size_samples = int(samplerate * 1.5)
                
                while True:
                    data = f.read(frames=chunk_size_samples, dtype='int16')
                    if not data.any():
                        break

                    # Create a temporary WAV file for the chunk
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_wav_file:
                        sf.write(temp_wav_file.name, data, samplerate)
                        
                        # Transcribe the chunk
                        segments = transcriber.transcribe_chunk(temp_wav_file.name)
                        if segments:
                            all_segments.extend(segments)

        except Exception as e:
            print(f"Error processing audio file: {e}", file=sys.stderr)
            sys.exit(1)

    full_text = " ".join([s["text"] for s in all_segments])
    
    if args.output:
        output_dir = os.path.dirname(args.output) if os.path.dirname(args.output) else "."
        output_filename = os.path.basename(args.output)
    else:
        output_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        output_filename = f"whisperlite_transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{args.format}"

    try:
        path = save_transcript(
            segments=all_segments,
            full_text=full_text,
            username=getpass.getuser(),
            timestamp=datetime.now(),
            output_dir=output_dir,
            file_format=args.format,
            output_filename=output_filename
        )
        print(f"Transcript saved to {path}")
    except Exception as e:
        print(f"Error saving transcript: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WhisperLite Transcription App")
    parser.add_argument("--model", type=str, default="models/ggml-tiny.en.bin",
                        help="Path to the Whisper model file (e.g., models/ggml-tiny.en.bin)")
    parser.add_argument("--format", type=str, default="txt", choices=["txt", "json", "srt"],
                        help="Output format for the transcript (txt, json, srt)")
    parser.add_argument("--save-transcript", action="store_true",
                        help="Run in save-transcript mode, reading JSON segments from stdin.")
    parser.add_argument("--output-dir", type=str, default=os.path.join(os.path.expanduser("~"), "Downloads"),
                        help="Directory to save the transcript file.")
    parser.add_argument("--input", type=str, help="Path to an audio file for transcription (CLI mode).")
    parser.add_argument("--output", type=str, help="Path to save the transcript (CLI mode).")
    parser.add_argument("--language", type=str, default="en", help="Language for transcription (e.g., en, es).")
    args = parser.parse_args()

    if args.save_transcript:
        # This branch is for saving transcripts from Rust backend
        try:
            segments_json = sys.stdin.read()
            segments_to_save = json.loads(segments_json)
            username = getpass.getuser()
            # full_text is not directly available here, so we reconstruct it or pass empty
            # For now, pass an empty string for full_text, as it's not used by JSON/SRT save
            path = save_transcript(segments_to_save, "", username, datetime.now(), args.output_dir, args.format)
            print(path) # Print path to stdout for Rust to capture
        except Exception as e:
            print(f"Error saving transcript: {e}", file=sys.stderr)
            sys.exit(1)
        sys.exit(0)

    if args.input:
        # CLI mode
        cli_main(args)
    else:
        # Original GUI-driven logic
        launch_gui_mode(args)