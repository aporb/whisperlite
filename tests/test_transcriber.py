import pytest
from unittest.mock import patch, MagicMock
import subprocess
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from transcriber import WhisperTranscriber

@pytest.fixture(autouse=True)
def mock_shutil_which(mocker):
    mocker.patch('shutil.which', return_value='/usr/local/bin/main')

@pytest.fixture
def mock_transcriber(tmp_path):
    model_path = tmp_path / "test_model.bin"
    model_path.touch()
    return WhisperTranscriber(str(model_path))

def test_transcriber_init_success(mock_transcriber):
    assert mock_transcriber.model_path.endswith("test_model.bin")
    assert mock_transcriber.use_gpu == False

def test_transcriber_init_whisper_not_found(mocker):
    mocker.patch('shutil.which', return_value=None)
    with pytest.raises(FileNotFoundError, match='whisper.cpp binary not found'):
        WhisperTranscriber(model_path='path/to/model.bin')

def test_transcriber_init_model_not_found(mocker):
    mocker.patch('os.path.isfile', return_value=False)
    with pytest.raises(FileNotFoundError, match='Model file not found'):
        WhisperTranscriber(model_path='path/to/model.bin')

def test_transcribe_chunk_success(mock_transcriber, mocker, tmp_path):
    mock_process = MagicMock()
    mock_process.communicate.return_value = (
        "WEBVTT\n\n00:00:00.000 --> 00:00:03.000\nHello world.\n\n00:00:03.500 --> 00:00:06.000\nHow are you?\n",
        ""
    )
    mock_process.returncode = 0
    mocker.patch('subprocess.Popen', return_value=mock_process)

    chunk_path = tmp_path / "audio.wav"
    chunk_path.touch()

    segments = mock_transcriber.transcribe_chunk(str(chunk_path))
    assert len(segments) == 2
    assert segments[0]["text"] == "Hello world."
    assert segments[0]["start"] == "00:00:00.000"
    assert segments[0]["end"] == "00:00:03.000"
    assert segments[1]["text"] == "How are you?"

def test_transcribe_chunk_timeout(mock_transcriber, mocker, tmp_path):
    mock_process = MagicMock()
    mock_process.communicate.side_effect = subprocess.TimeoutExpired(cmd="test", timeout=1)
    mocker.patch('subprocess.Popen', return_value=mock_process)

    chunk_path = tmp_path / "audio.wav"
    chunk_path.touch()

    segments = mock_transcriber.transcribe_chunk(str(chunk_path))
    assert segments == []

def test_transcribe_chunk_subprocess_error(mock_transcriber, mocker, tmp_path):
    mock_process = MagicMock()
    mock_process.communicate.return_value = ("", "Error from whisper.cpp")
    mock_process.returncode = 1
    mocker.patch('subprocess.Popen', return_value=mock_process)

    chunk_path = tmp_path / "audio.wav"
    chunk_path.touch()

    segments = mock_transcriber.transcribe_chunk(str(chunk_path))
    assert segments == []

def test_transcribe_chunk_malformed_vtt(mock_transcriber, mocker, tmp_path):
    mock_process = MagicMock()
    mock_process.communicate.return_value = (
        "WEBVTT\n\n00:00:00.000 --> 00:00:03.000\nHello world.\nMALFORMED LINE\n",
        ""
    )
    mock_process.returncode = 0
    mocker.patch('subprocess.Popen', return_value=mock_process)

    chunk_path = tmp_path / "audio.wav"
    chunk_path.touch()

    segments = mock_transcriber.transcribe_chunk(str(chunk_path))
    assert len(segments) == 1 # Only the first valid segment should be parsed
    assert segments[0]["text"] == "Hello world."

def test_transcribe_chunk_no_output(mock_transcriber, mocker, tmp_path):
    mock_process = MagicMock()
    mock_process.communicate.return_value = ("", "")
    mock_process.returncode = 0
    mocker.patch('subprocess.Popen', return_value=mock_process)

    chunk_path = tmp_path / "audio.wav"
    chunk_path.touch()

    segments = mock_transcriber.transcribe_chunk(str(chunk_path))
    assert segments == []
