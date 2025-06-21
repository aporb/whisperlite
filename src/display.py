"""display.py -- Minimal Tkinter overlay for live transcripts."""

from __future__ import annotations

import tkinter as tk
from typing import Callable, Optional

from transcript_buffer import TranscriptBuffer


class DisplayWindow:
    """Floating window that displays the rolling transcript."""

    def __init__(self, on_stop: Callable[[], None], refresh_ms: int = 500) -> None:
        self.on_stop = on_stop
        self.refresh_ms = refresh_ms
        self.buffer: Optional[TranscriptBuffer] = None

        self.root = tk.Tk()
        self.root.title("WhisperLite")
        self.root.attributes("-topmost", True)
        self.root.geometry("400x200")
        self.root.configure(bg="black")

        self.text_var = tk.StringVar()
        self.label = tk.Label(
            self.root,
            textvariable=self.text_var,
            justify="left",
            bg="black",
            fg="white",
            wraplength=380,
            anchor="nw",
        )
        self.label.pack(fill="both", expand=True, padx=4, pady=4)

        bottom = tk.Frame(self.root, bg="black")
        bottom.pack(fill="x")
        self.status_canvas = tk.Canvas(bottom, width=12, height=12, highlightthickness=0, bg="black")
        self.status_indicator = self.status_canvas.create_oval(2, 2, 10, 10, fill="green")
        self.status_canvas.pack(side="left", padx=4, pady=4)
        self.stop_button = tk.Button(bottom, text="Stop", command=self.stop)
        self.stop_button.pack(side="right", padx=4, pady=4)

        self.root.protocol("WM_DELETE_WINDOW", self.stop)

    def set_buffer(self, buffer: TranscriptBuffer) -> None:
        """Assign a :class:`TranscriptBuffer` to display."""
        self.buffer = buffer

    def start(self) -> None:
        """Begin periodic updates and enter the Tk main loop."""
        self.root.after(self.refresh_ms, self._update_loop)
        self.root.mainloop()

    # Public for tests
    def _update_loop(self) -> None:
        if self.buffer is not None:
            text = self.buffer.full_text()
            self.text_var.set(text)
        self.root.after(self.refresh_ms, self._update_loop)

    def stop(self) -> None:
        """Invoke stop callback and close the window."""
        self.on_stop()
        self.root.quit()
        self.root.destroy()
