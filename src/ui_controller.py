"""ui_controller.py -- Manage overlay button events."""

from __future__ import annotations

import threading


class UIController:
    """Central place to handle UI commands."""

    def __init__(self) -> None:
        self._stop_event = threading.Event()

    def request_stop(self) -> None:
        self._stop_event.set()

    def should_stop(self) -> bool:
        return self._stop_event.is_set()
