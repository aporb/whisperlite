import pytest
from unittest.mock import patch, mock_open
from src.output_writer import save_transcript
from datetime import datetime

@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
def test_save_transcript_success(mock_makedirs, mock_file):
    full_text = "This is a test transcript."
    username = "testuser"
    timestamp = datetime.now()
    output_dir = "/path/to/output"

    save_transcript(full_text, username, timestamp, output_dir)

    mock_makedirs.assert_called_once_with(output_dir, exist_ok=True)
    mock_file.assert_called_once_with(
        f"{output_dir}/{username}_{timestamp.strftime('%Y%m%d_%H%M')}.txt", "w", encoding="utf-8"
    )
    mock_file().write.assert_any_call(
        f"WhisperLite Transcript - Generated on {timestamp.strftime('%Y-%m-%d %H:%M')}\n\n"
    )
    mock_file().write.assert_any_call(full_text)

@patch("builtins.open", mock_open())
@patch("os.makedirs")
def test_save_transcript_io_error(mock_makedirs):
    full_text = "This is a test transcript."
    username = "testuser"
    timestamp = datetime.now()
    output_dir = "/path/to/output"

    with patch("builtins.open", mock_open()) as mock_file:
        mock_file.side_effect = IOError("Permission denied")
        with pytest.raises(RuntimeError, match="Failed to write transcript to /path/to/output"):
            save_transcript(full_text, username, timestamp, output_dir)