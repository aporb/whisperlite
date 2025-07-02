from __future__ import annotations

import os
import json
from datetime import datetime
from typing import List, Dict

def _format_time_srt(time_str: str) -> str:
    """Converts VTT time format (HH:MM:SS.mmm) to SRT time format (HH:MM:SS,mmm)."""
    return time_str.replace('.', ',')

def _format_json(segments: List[Dict]) -> str:
    """Formats a list of segments into a JSON string."""
    # Ensure times are in SRT-like format for consistency if needed, or keep as is
    # For now, assuming the 'start' and 'end' from transcriber are suitable.
    # If transcriber outputs HH:MM:SS.mmm, JSON will keep it.
    # If SRT needs HH:MM:SS,mmm, it's handled in _format_srt.
    return json.dumps(segments, indent=4, ensure_ascii=False)

def _format_srt(segments: List[Dict]) -> str:
    """Formats a list of segments into an SRT string."""
    srt_content = []
    for i, segment in enumerate(segments):
        start_srt = _format_time_srt(segment["start"])
        end_srt = _format_time_srt(segment["end"])
        srt_content.append(f"{i + 1}")
        srt_content.append(f"{start_srt} --> {end_srt}")
        srt_content.append(segment["text"])
        srt_content.append("") # Empty line separates entries
    return "\n".join(srt_content)

def save_transcript(
    segments: List[Dict],
    full_text: str,
    username: str,
    timestamp: datetime,
    output_dir: str,
    file_format: str = "txt",
    output_filename: Optional[str] = None
) -> str:
    """
    Writes transcript data to a timestamped file in output_dir.
    Supports 'txt', 'json', and 'srt' formats.
    Returns the path to the saved file.
    """
    os.makedirs(output_dir, exist_ok=True)

    if output_filename:
        base_filename = os.path.splitext(output_filename)[0]
        extension = os.path.splitext(output_filename)[1].lstrip('.')
        if not extension:
            extension = file_format # Fallback if no extension provided in output_filename
    else:
        base_filename = f"{username}_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        extension = file_format
    
    content = ""

    if extension == "txt":
        header = f"WhisperLite Transcript - Generated on {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        content = header + full_text
    elif extension == "json":
        content = _format_json(segments)
    elif extension == "srt":
        content = _format_srt(segments)
    else:
        raise ValueError(f"Unsupported file format: {extension}")

    filename = f"{base_filename}.{extension}"
    path = os.path.join(output_dir, filename)

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except IOError as exc:
        raise RuntimeError(f"Failed to write transcript to {path}: {exc}") from exc
    return path