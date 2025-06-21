import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import pytest
import tkinter as tk

from ui_controller import UIController
from transcript_buffer import TranscriptBuffer
from display import DisplayWindow


def test_display_update():
    controller = UIController()
    buffer = TranscriptBuffer()
    buffer.append("hello")
    # Create display but do not enter mainloop
    try:
        win = DisplayWindow(controller.request_stop)
    except tk.TclError:
        pytest.skip("Tkinter not available")
    win.set_buffer(buffer)
    win._update_loop()  # manual update
    assert win.text_var.get() == "hello"
    win.root.destroy()


def test_stop_invokes_callback():
    called = {}

    def cb():
        called["x"] = True

    try:
        win = DisplayWindow(cb)
    except tk.TclError:
        pytest.skip("Tkinter not available")
    win.stop()
    assert called.get("x") is True


def test_set_active_changes_status_color():
    try:
        win = DisplayWindow(lambda: None)
    except tk.TclError:
        pytest.skip("Tkinter not available")
    win.set_active(False)
    color = win.status_canvas.itemcget(win.status_indicator, "fill")
    assert color == "gray"
    win.root.destroy()
