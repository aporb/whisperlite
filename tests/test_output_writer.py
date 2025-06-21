import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from output_writer import save_transcript


def test_save_transcript(tmp_path):
    path = save_transcript("hello", "testuser", datetime(2024, 1, 1, 12, 0), tmp_path)
    assert os.path.isfile(path)
    with open(path, "r", encoding="utf-8") as f:
        contents = f.read()
    assert "WhisperLite Transcript" in contents
    assert "hello" in contents
