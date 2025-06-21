# WhisperLite

**A lightweight, open-source, cross-platform voice transcription tool for real-time, local, and private speech-to-text conversion.**

---

## 🚀 Overview

WhisperLite captures microphone input in real time, processes 1–2s audio chunks with [`whisper.cpp`](https://github.com/ggerganov/whisper.cpp), displays live transcription, and saves a final `.txt` file locally. All processing is offline and cross-platform.

---

## 🔧 Status & Roadmap

### 🔄 MVP Completion Checklist

This tracks progress across Epics and Tasks. Each links to a GitHub Issue for context and discussion:

#### 🎯 [Epic: MVP Core Transcription Engine #1](https://github.com/aporb/whisperlite/issues/1)
- [x] [Implement audio stream capture via sounddevice](https://github.com/aporb/whisperlite/issues/6)
- [x] [Integrate whisper.cpp transcription of audio chunks](https://github.com/aporb/whisperlite/issues/7)
- [x] [Create transcript buffer and update loop](https://github.com/aporb/whisperlite/issues/8)
- [x] [Save final .txt transcript to Downloads](https://github.com/aporb/whisperlite/issues/9)

#### 🖥️ [Epic: Live Overlay Display #2](https://github.com/aporb/whisperlite/issues/2)
- [ ] [Build floating overlay using Tkinter or Tauri](https://github.com/aporb/whisperlite/issues/10)
- [ ] [Connect live transcript feed to display](https://github.com/aporb/whisperlite/issues/11)
- [ ] [Add UI controls: Stop button, status light](https://github.com/aporb/whisperlite/issues/12)
- [ ] [Implement graceful exit and buffer flush](https://github.com/aporb/whisperlite/issues/13)

#### 📦 [Epic: Cross-Platform Packaging #3](https://github.com/aporb/whisperlite/issues/3)
- [ ] [Package for Windows with PyInstaller](https://github.com/aporb/whisperlite/issues/14)
- [ ] [Package for macOS with py2app](https://github.com/aporb/whisperlite/issues/15)
- [ ] [Package for Linux with AppImage](https://github.com/aporb/whisperlite/issues/16)

#### 🧪 [Epic: Test Suite & Error Handling #4](https://github.com/aporb/whisperlite/issues/4)
- [ ] [Add unit tests for audio_capture.py](https://github.com/aporb/whisperlite/issues/17)
- [ ] [Add integration test: record → transcribe → save](https://github.com/aporb/whisperlite/issues/18)
- [ ] [Handle mic permission and device not found](https://github.com/aporb/whisperlite/issues/19)
- [ ] [Validate output file permissions and errors](https://github.com/aporb/whisperlite/issues/20)

#### 🧭 [Epic: Contributor Onboarding and Docs #5](https://github.com/aporb/whisperlite/issues/5)
- [ ] [Finalize DEV_SETUP.md](https://github.com/aporb/whisperlite/issues/21)
- [ ] [Link all architecture docs from README](https://github.com/aporb/whisperlite/issues/22)
- [ ] [Add issue templates and contributing guide](https://github.com/aporb/whisperlite/issues/23)

---

## 🛠️ Installation

See [docs/BUILD_INSTALL.md](docs/BUILD_INSTALL.md) for full platform-specific setup.

```bash
git clone https://github.com/aporb/whisperlite.git
cd whisperlite
pip install -r requirements.txt
````

Add your Whisper model:

```bash
mkdir models
curl -o models/ggml-tiny.en.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/models/ggml-tiny.en.bin
```

---

## 🧠 Architecture Overview

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for complete module breakdown.

```text
audio_capture.py  →  transcriber.py  →  display.py
                     ↓
              output_writer.py (.txt)
```

---

## 📁 Project Layout

```text
src/
  ├── audio_capture.py     # mic input, 1–2s wav slices
  ├── transcriber.py       # whisper.cpp subprocess wrapper
  ├── transcript_buffer.py # rolling transcript store
  ├── display.py           # optional UI
  ├── output_writer.py     # save transcript
  └── main.py              # orchestrates pipeline
rust/
  src/main.rs         # cpal-based core engine
docs/
  ├── ARCHITECTURE.md
  ├── DEV_SETUP.md
  ├── BUILD_INSTALL.md
  ├── PRODUCT_REQUIREMENTS.md
  └── ...
tests/
  ├── test_audio_capture.py
  ├── test_transcriber.py
  └── test_output_writer.py
```

---

## 🧪 Testing

```bash
make test

cargo test --manifest-path rust/Cargo.toml
```

* Unit coverage: audio slicing, whisper subprocess
* Integration: end-to-end (record → transcribe → save)
* Edge cases: no mic, long processing, I/O errors

---

## 📦 Packaging

See [docs/BUILD\_INSTALL.md](docs/BUILD_INSTALL.md)
Supported via: PyInstaller, py2app, AppImage, .deb

---

## 🛡️ Privacy & Offline Guarantee

* No telemetry, logging, or cloud calls
* 100% local processing
* Safe for air-gapped or disconnected environments

See: [docs/SECURITY\_PRIVACY.md](docs/SECURITY_PRIVACY.md)

---

## 🤝 Contributing

Fork, clone, and follow onboarding in [docs/DEV\_SETUP.md](docs/DEV_SETUP.md).
New contributors can begin with [good first issue](https://github.com/aporb/whisperlite/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).

---

## 📜 License

MIT — See [LICENSE](LICENSE)
