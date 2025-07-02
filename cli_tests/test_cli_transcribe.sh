#!/bin/bash

set -euo pipefail

# Create a dummy audio file for testing
dummy_audio_file="test_audio.wav"
venv/bin/python3 -c "import soundfile as sf; import numpy as np; samplerate = 16000; duration = 0.5; frequency = 1000; t = np.linspace(0., duration, int(samplerate * duration), endpoint=False); amplitude = np.iinfo(np.int16).max * 0.1; data = amplitude * np.sin(2. * np.pi * frequency * t); sf.write('$dummy_audio_file', data.astype(np.int16), samplerate)"

# Ensure the model path is correct for testing
MODEL_PATH="models/ggml-tiny.en.bin"

export MOCK_TRANSCRIPTION_OUTPUT="true"

# Test basic transcription (default to txt format)
echo "Testing basic CLI transcription (txt format)..."
venv/bin/python3 src/main.py --input "$dummy_audio_file" --model "$MODEL_PATH" --output "./output.txt"
if [ $? -ne 0 ]; then
    echo "Basic CLI transcription failed!"
    rm "$dummy_audio_file" "output.txt"
    exit 1
fi
if [ ! -f "output.txt" ]; then
    echo "output.txt not created!"
    rm "$dummy_audio_file"
    exit 1
fi
echo "Basic CLI transcription (txt) successful."

# Test JSON output
echo "Testing CLI transcription (json format)..."
venv/bin/python3 src/main.py --input "$dummy_audio_file" --model "$MODEL_PATH" --output "./output.json" --format json
if [ $? -ne 0 ]; then
    echo "JSON CLI transcription failed!"
    rm "$dummy_audio_file" "output.txt" "output.json"
    exit 1
fi
if [ ! -f "output.json" ]; then
    echo "output.json not created!"
    rm "$dummy_audio_file" "output.txt"
    exit 1
fi
# Basic check for JSON content (starts with [ and ends with ])
if ! head -n 1 "output.json" | grep -q "^\["; then
    echo "output.json does not look like JSON!"
    rm "$dummy_audio_file" "output.txt" "output.json"
    exit 1
fi
echo "JSON CLI transcription successful."

# Test SRT output
echo "Testing CLI transcription (srt format)..."
venv/bin/python3 src/main.py --input "$dummy_audio_file" --model "$MODEL_PATH" --output "./output.srt" --format srt
if [ $? -ne 0 ]; then
    echo "SRT CLI transcription failed!"
    rm "$dummy_audio_file" "output.txt" "output.json" "output.srt"
    exit 1
fi
if [ ! -f "output.srt" ]; then
    echo "output.srt not created!"
    rm "$dummy_audio_file" "output.txt" "output.json"
    exit 1
fi
cat "output.srt"
echo "SRT CLI transcription successful."

echo "All CLI tests passed!"

# Clean up
rm "$dummy_audio_file" "output.txt" "output.json" "output.srt"
