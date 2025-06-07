
# Build & Install Instructions — WhisperLite

## Dependencies

* Python 3.10+
* `sounddevice`, `numpy`
* `whisper.cpp` model (.bin)

## Build Steps

1. pip install -r requirements.txt
2. Download and place model in /models
3. python src/main.py

## Packaging

* Windows: PyInstaller → `.exe`
* macOS: py2app or Tauri → `.app`
* Linux: AppImage or `.deb`
