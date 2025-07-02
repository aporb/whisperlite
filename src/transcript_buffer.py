"""transcript_buffer.py -- Rolling transcript storage for WhisperLite."""

from __future__ import annotations

import threading
from collections import deque
from datetime import datetime
from typing import Deque, List, Dict

class TranscriptBuffer:
    """Thread-safe append-only transcript buffer."""

    def __init__(self, maxlen: int | None = None):
        self._buffer: Deque[Dict] = deque(maxlen=maxlen)
        self._lock = threading.RLock()

    def append(self, segments: List[Dict]) -> None:
        """Appends a list of new segments to the buffer."""
        with self._lock:
            self._buffer.extend(segments)

    def get_segments(self) -> List[Dict]:
        """Returns all stored segments."""
        with self._lock:
            return list(self._buffer)

    def full_text(self) -> str:
        """Returns the full concatenated text from all segments."""
        with self._lock:
            return " ".join([s["text"] for s in self._buffer])

    def clear(self) -> List[Dict]:
        """Clears the buffer and returns the cleared segments."""
        with self._lock:
            segments = list(self._buffer)
            self._buffer.clear()
            return segments

    def __len__(self) -> int:
        with self._lock:
            return len(self._buffer)
