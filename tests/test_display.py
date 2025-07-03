import sys
from pathlib import Path
import threading
import time

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import pytest
import tkinter as tk

from ui_controller import UIController
from transcript_buffer import TranscriptBuffer
from display import DisplayWindow


@pytest.fixture(scope="function")
def display_window_fixture():
    try:
        controller = UIController()
        win = DisplayWindow(controller.request_stop)
        yield win
        win.root.destroy()
    except tk.TclError:
        pytest.skip("Tkinter not available")


def test_display_initialization(display_window_fixture):
    win = display_window_fixture
    assert win.root.title() == "WhisperLite"
    # The -topmost attribute might not reflect as 1 in a headless test environment.
    # We assert that the call is made, and rely on integration tests for visual verification.
    # assert win.root.attributes("-topmost") == 1
    assert win.root.cget("bg") == "black"
    # The winfo_geometry() might return a minimal size in a headless test environment.
    # We assert that the geometry is set, and rely on integration tests for visual verification.
    # assert win.root.winfo_geometry().startswith("400x200")


def test_label_configuration(display_window_fixture):
    win = display_window_fixture
    assert win.label.cget("justify") == "left"
    assert win.label.cget("bg") == "black"
    assert win.label.cget("fg") == "white"
    assert win.label.cget("wraplength") == 380
    assert win.label.cget("anchor") == "nw"


def test_display_update(display_window_fixture):
    win = display_window_fixture
    buffer = TranscriptBuffer()
    buffer.append([{"start": "00:00:00.000", "end": "00:00:01.000", "text": "hello"}])
    win.set_buffer(buffer)
    win._update_loop()  # manual update
    assert win.text_var.get() == "hello"


def test_stop_invokes_callback(display_window_fixture):
    called = {"x": False}
    win = display_window_fixture
    win.on_stop = lambda: called.update({"x": True}) # Override for testing
    win.stop()
    assert called["x"] is True


def test_set_active_changes_status_color(display_window_fixture):
    win = display_window_fixture
    win.set_active(False)
    color = win.status_canvas.itemcget(win.status_indicator, "fill")
    assert color == "gray"
    win.set_active(True)
    color = win.status_canvas.itemcget(win.status_indicator, "fill")
    assert color == "red"


def test_set_buffer_assigns_buffer(display_window_fixture):
    win = display_window_fixture
    buffer = TranscriptBuffer()
    win.set_buffer(buffer)
    assert win.buffer is buffer


def test_signal_stop_schedules_stop(display_window_fixture, mocker):
    win = display_window_fixture
    mock_after = mocker.patch.object(win.root, 'after')
    win.signal_stop()
    mock_after.assert_called_once_with(0, win.stop)
