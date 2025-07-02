"""output_writer.py -- Save final transcript to the user's Downloads folder."""

from __future__ import annotations

import os
from datetime import datetime


def save_transcript(full_text: str, username: str, timestamp: datetime, output_dir: str) -> str:
    """Write ``full_text`` to a timestamped file in ``output_dir`` and return the path."""

    os.makedirs(output_dir, exist_ok=True)
    filename = f"{username}_{timestamp.strftime('%Y%m%d_%H%M')}.txt"
    path = os.path.join(output_dir, filename)
    header = f"WhisperLite Transcript - Generated on {timestamp.strftime('%Y-%m-%d %H:%M')}\n\n"

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(header)
            f.write(full_text)
    except IOError as exc:
        raise RuntimeError(f"Failed to write transcript to {path}: {exc}") from exc
    return path
