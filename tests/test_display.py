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
