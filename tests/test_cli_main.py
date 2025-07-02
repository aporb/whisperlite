import pytest
import subprocess
import os
import sys
import soundfile as sf
import numpy as np
import tempfile
from unittest.mock import patch, MagicMock

# Mock the save_transcript function to prevent actual file writing during tests
@pytest.fixture(autouse=True)
def mock_save_transcript():
    with patch('src.output_writer.save_transcript') as mock_save:
        mock_save.return_value = "/mock/path/to/transcript.txt"
        yield mock_save

# Mock the WhisperTranscriber to control transcription output
@pytest.fixture(autouse=True)
def mock_transcriber():
    with patch('src.transcriber.WhisperTranscriber') as mock_whisper_transcriber:
        instance = mock_whisper_transcriber.return_value
        instance.transcribe_chunk.return_value = [
            {"start": "00:00:00.000", "end": "00:00:03.000", "text": "This is a test."}, 
            {"start": "00:00:03.500", "end": "00:00:06.000", "text": "CLI mode."}
        ]
        yield mock_whisper_transcriber


def test_cli_mode_basic_transcription(mock_save_transcript):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio_file:
        sf.write(tmp_audio_file.name, np.zeros((16000, 1), dtype='int16'), 16000)
        dummy_input_path = tmp_audio_file.name

    result = subprocess.run(
        [sys.executable, "src/main.py", "--input", dummy_input_path, "--model", "models/ggml-tiny.en.bin"],
        capture_output=True, text=True
    )
    
    os.remove(dummy_input_path)

    assert result.returncode == 0
    assert "Transcript saved to" in result.stdout


def test_cli_mode_json_output(mock_save_transcript):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio_file:
        sf.write(tmp_audio_file.name, np.zeros((16000, 1), dtype='int16'), 16000)
        dummy_input_path = tmp_audio_file.name

    result = subprocess.run(
        [sys.executable, "src/main.py", "--input", dummy_input_path, "--format", "json", "--model", "models/ggml-tiny.en.bin"],
        capture_output=True, text=True
    )
    
    os.remove(dummy_input_path)

    assert result.returncode == 0
    assert "Transcript saved to" in result.stdout
    assert ".json" in result.stdout


def test_cli_mode_srt_output(mock_save_transcript):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio_file:
        sf.write(tmp_audio_file.name, np.zeros((16000, 1), dtype='int16'), 16000)
        dummy_input_path = tmp_audio_file.name

    result = subprocess.run(
        [sys.executable, "src/main.py", "--input", dummy_input_path, "--format", "srt", "--model", "models/ggml-tiny.en.bin"],
        capture_output=True, text=True
    )
    
    os.remove(dummy_input_path)

    assert result.returncode == 0
    assert "Transcript saved to" in result.stdout
    assert ".srt" in result.stdout


def test_cli_mode_input_not_found():
    result = subprocess.run(
        [sys.executable, "src/main.py", "--input", "/nonexistent/audio.wav", "--model", "models/ggml-tiny.en.bin"],
        capture_output=True, text=True
    )

    assert result.returncode == 1
    assert "Error: Input file not found" in result.stderr


def test_cli_mode_model_not_found():
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio_file:
        sf.write(tmp_audio_file.name, np.zeros((16000, 1), dtype='int16'), 16000)
        dummy_input_path = tmp_audio_file.name

    result = subprocess.run(
        [sys.executable, "src/main.py", "--input", dummy_input_path, "--model", "/nonexistent/model.bin"],
        capture_output=True, text=True
    )
    
    os.remove(dummy_input_path)

    assert result.returncode == 1
    assert "Error: Model file not found" in result.stderr
