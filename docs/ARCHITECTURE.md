
# Architecture Overview — WhisperLite

## System Diagram

Audio Capture (chunks) → Streaming Whisper Transcriber → Live Text Overlay → Output Writer (on stop)

## Modules

* audio\_capture.py — microphone streaming
* transcriber.py — invokes whisper.cpp
* display.py — updates overlay window
* output\_writer.py — saves final text
