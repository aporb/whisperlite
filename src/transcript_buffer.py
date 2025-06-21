"""transcript_buffer.py -- Rolling transcript storage for WhisperLite."""

from __future__ import annotations

import threading
from collections import deque
from datetime import datetime
from typing import Deque, List

class TranscriptBuffer:
    """Thread-safe append-only transcript buffer."""

    def __init__(self, maxlen: int | None = None):
        self._buffer: Deque[str] = deque(maxlen=maxlen)
        self._lock = threading.RLock()

    def append(self, text: str) -> None:
        with self._lock:
            self._buffer.append(text)

    def full_text(self) -> str:
        with self._lock:
            return "\n".join(self._buffer)

    def clear(self) -> List[str]:
        with self._lock:
            lines = list(self._buffer)
            self._buffer.clear()
            return lines

    def __len__(self) -> int:
        with self._lock:
            return len(self._buffer)
