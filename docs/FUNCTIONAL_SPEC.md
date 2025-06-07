
# Functional Specification — WhisperLite

## Flow

1. User launches app
2. App starts capturing audio, splits into 1–2 second chunks
3. Each chunk is sent to whisper.cpp
4. Transcribed text is appended and shown live in overlay
5. On stop, transcript is finalized, saved as .txt
