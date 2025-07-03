import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from transcript_buffer import TranscriptBuffer

@pytest.fixture
def transcript_buffer():
    return TranscriptBuffer()

def test_append_single_segment(transcript_buffer):
    segment = {"start": "00:00:00.000", "end": "00:00:01.000", "text": "hello"}
    transcript_buffer.append([segment])
    assert transcript_buffer.get_segments() == [segment]
    assert transcript_buffer.full_text() == "hello"

def test_append_multiple_segments(transcript_buffer):
    segments = [
        {"start": "00:00:00.000", "end": "00:00:01.000", "text": "hello"},
        {"start": "00:00:01.500", "end": "00:00:02.500", "text": "world"}
    ]
    transcript_buffer.append(segments)
    assert transcript_buffer.get_segments() == segments
    assert transcript_buffer.full_text() == "hello world"

def test_clear_buffer(transcript_buffer):
    segment = {"start": "00:00:00.000", "end": "00:00:01.000", "text": "hello"}
    transcript_buffer.append([segment])
    cleared_segments = transcript_buffer.clear()
    assert cleared_segments == [segment]
    assert transcript_buffer.get_segments() == []
    assert transcript_buffer.full_text() == ""

def test_buffer_length(transcript_buffer):
    assert len(transcript_buffer) == 0
    transcript_buffer.append([{"text": "one"}])
    assert len(transcript_buffer) == 1
    transcript_buffer.append([{"text": "two"}, {"text": "three"}])
    assert len(transcript_buffer) == 3

def test_maxlen_behavior():
    buffer = TranscriptBuffer(maxlen=2)
    buffer.append([{"text": "one"}])
    buffer.append([{"text": "two"}])
    buffer.append([{"text": "three"}])
    assert len(buffer) == 2
    assert buffer.get_segments() == [{"text": "two"}, {"text": "three"}]
    assert buffer.full_text() == "two three"

def test_empty_buffer_full_text(transcript_buffer):
    assert transcript_buffer.full_text() == ""

def test_empty_buffer_get_segments(transcript_buffer):
    assert transcript_buffer.get_segments() == []
