import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import pytest
from unittest.mock import patch, mock_open
from output_writer import save_transcript
from datetime import datetime
import json
import os

@pytest.fixture
def sample_segments():
    return [
        {"start": "00:00:00.000", "end": "00:00:03.500", "text": "Hello, this is a test."},
        {"start": "00:00:04.100", "end": "00:00:07.800", "text": "Welcome to WhisperLite."}
    ]

@pytest.fixture
def sample_full_text():
    return "Hello, this is a test. Welcome to WhisperLite."

@pytest.fixture
def sample_timestamp():
    return datetime(2025, 7, 1, 10, 30, 0)

@pytest.fixture
def sample_output_dir():
    return "/path/to/output"

@pytest.fixture
def sample_username():
    return "testuser"

@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
def test_save_transcript_txt_success(
    mock_makedirs, mock_file, sample_segments, sample_full_text, sample_username, sample_timestamp, sample_output_dir
):
    path = save_transcript(
        segments=sample_segments,
        full_text=sample_full_text,
        username=sample_username,
        timestamp=sample_timestamp,
        output_dir=sample_output_dir,
        file_format="txt"
    )

    expected_filename = f"{sample_username}_{sample_timestamp.strftime('%Y%m%d_%H%M%S')}.txt"
    expected_path = os.path.join(sample_output_dir, expected_filename)
    expected_header = f"WhisperLite Transcript - Generated on {sample_timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    expected_content = expected_header + sample_full_text

    mock_makedirs.assert_called_once_with(sample_output_dir, exist_ok=True)
    mock_file.assert_called_once_with(expected_path, "w", encoding="utf-8")
    mock_file().write.assert_called_once_with(expected_content)
    assert path == expected_path

@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
def test_save_transcript_json_success(
    mock_makedirs, mock_file, sample_segments, sample_full_text, sample_username, sample_timestamp, sample_output_dir
):
    path = save_transcript(
        segments=sample_segments,
        full_text=sample_full_text,
        username=sample_username,
        timestamp=sample_timestamp,
        output_dir=sample_output_dir,
        file_format="json"
    )

    expected_filename = f"{sample_username}_{sample_timestamp.strftime('%Y%m%d_%H%M%S')}.json"
    expected_path = os.path.join(sample_output_dir, expected_filename)
    expected_content = json.dumps(sample_segments, indent=4, ensure_ascii=False)

    mock_makedirs.assert_called_once_with(sample_output_dir, exist_ok=True)
    mock_file.assert_called_once_with(expected_path, "w", encoding="utf-8")
    mock_file().write.assert_called_once_with(expected_content)
    assert path == expected_path

@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
def test_save_transcript_srt_success(
    mock_makedirs, mock_file, sample_segments, sample_full_text, sample_username, sample_timestamp, sample_output_dir
):
    path = save_transcript(
        segments=sample_segments,
        full_text=sample_full_text,
        username=sample_username,
        timestamp=sample_timestamp,
        output_dir=sample_output_dir,
        file_format="srt"
    )

    expected_filename = f"{sample_username}_{sample_timestamp.strftime('%Y%m%d_%H%M%S')}.srt"
    expected_path = os.path.join(sample_output_dir, expected_filename)
    expected_content = """1
00:00:00,000 --> 00:00:03,500
Hello, this is a test.

2
00:00:04,100 --> 00:00:07,800
Welcome to WhisperLite.
"""

    mock_makedirs.assert_called_once_with(sample_output_dir, exist_ok=True)
    mock_file.assert_called_once_with(expected_path, "w", encoding="utf-8")
    mock_file().write.assert_called_once_with(expected_content)
    assert path == expected_path

@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
def test_save_transcript_invalid_format(
    mock_makedirs, mock_file, sample_segments, sample_full_text, sample_username, sample_timestamp, sample_output_dir
):
    with pytest.raises(ValueError, match="Unsupported file format: xyz"):
        save_transcript(
            segments=sample_segments,
            full_text=sample_full_text,
            username=sample_username,
            timestamp=sample_timestamp,
            output_dir=sample_output_dir,
            file_format="xyz"
        )
    mock_makedirs.assert_called_once_with(sample_output_dir, exist_ok=True)

@patch("builtins.open", mock_open())
@patch("os.makedirs")
def test_save_transcript_io_error(
    mock_makedirs, sample_segments, sample_full_text, sample_username, sample_timestamp, sample_output_dir
):
    with patch("builtins.open", mock_open()) as mock_file:
        mock_file.side_effect = IOError("Permission denied")
        with pytest.raises(RuntimeError, match="Failed to write transcript to /path/to/output"):
            save_transcript(
                segments=sample_segments,
                full_text=sample_full_text,
                username=sample_username,
                timestamp=sample_timestamp,
                output_dir=sample_output_dir,
                file_format="txt"
            )
