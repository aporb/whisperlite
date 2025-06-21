import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from audio_capture import AudioCapture


def test_audio_capture_chunk_size():
    ac = AudioCapture(chunk_duration_sec=1.0, sample_rate=8000)
    assert ac.frames_per_chunk == 8000
def test_audio_capture_initialization():
    # TODO: Implement unit tests for audio_capture module
    assert True
