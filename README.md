# WhisperLite

**A lightweight, open-source, cross-platform voice transcription tool that provides real-time, local transcription—100% private and portable.**

## 🚀 Overview

- **Zero-cloud:** All processing happens on your device.  
- **Live transcription:** Speak and see your words in real time.  
- **Cross-platform:** Windows, macOS, Linux support.  
- **Simple output:** On stop, get a `.txt` transcript saved to your Downloads folder, timestamped and user-named.

---

## 🔥 Key Features

- Real-time, rolling transcription with minimal UI footprint  
- Local processing via [Whisper.cpp](https://github.com/ggerganov/whisper.cpp)  
- Cross-platform audio capture using `sounddevice`  
- Buffered chunk management for low-latency transcription  
- Modular design: `audio_capture.py`, `transcriber.py`, `display.py`, `output_writer.py`  
- No internet, no telemetry, no cloud dependencies  

---

## 🛠️ Installation

### Prerequisites

- Python 3.10+  
- [Whisper.cpp model file](https://huggingface.co/ggerganov/whisper.cpp/tree/main) (e.g. `ggml-tiny.en.bin`) placed into `models/`  
- System audio device (mic) with drivers installed  

### Setup

```bash
git clone https://github.com/aporb/whisperlite.git
cd whisperlite
pip install -r requirements.txt
````

---

## 🖥️ Quick Start

```bash
python src/main.py --model models/ggml-tiny.en.bin
```

* Captures live audio in 1–2 s chunks
* Sends chunks to `whisper.cpp` for inference
* Buffers transcript in memory, then saves as `<username>_YYYYMMDD_HHMM.txt` in Downloads when complete

---

## 📁 Project Structure

```
src/
  audio_capture.py     # real-time mic capture
  transcriber.py       # whisper.cpp integration
  display.py           # optional overlay UI
  output_writer.py     # final .txt export
  main.py              # orchestrates the pipeline
models/                # Whisper.cpp model files (.bin)
chunks/                # auto-generated .wav slices
tests/                 # unit & integration tests
docs/                  # detailed design & usage docs
```

---

## 🧪 Testing

* Unit tests: `pytest tests/unit/`
* Integration tests (record → transcribe → save): `pytest tests/integration/`
* Edge cases: no mic, I/O errors, long processing times

---

## 📦 Packaging & Distribution

See [docs/BUILD\_INSTALL.md](docs/BUILD_INSTALL.md) for platform-specific packaging via PyInstaller, py2app, or AppImage.

---

## 🤝 Contributing

Please see [docs/DEV\_SETUP.md](docs/DEV_SETUP.md) for setup, coding standards, and pull request guidelines.

---

## 🛡️ License

MIT License — see [LICENSE](LICENSE)