# WhisperLite

**A lightweight, open-source, cross-platform voice transcription tool that transcribes speech in real-time—100% local, private, and portable.**

## 🚀 Overview

- **Zero-cloud:** All processing on your device.
- **Live transcription:** See your words as you speak, in a floating overlay window.
- **Cross-platform:** Windows, macOS, Linux.
- **Simple output:** When you stop, get a `.txt` file in your Downloads folder, named by username and timestamp.

---

## 🔥 Features

- Real-time, rolling transcription with minimal UI.
- Local processing via [Whisper.cpp](https://github.com/ggerganov/whisper.cpp).
- No internet connection or cloud dependencies.
- Lightweight: runs on most modern machines.

---

## 🖥️ Installation

### Requirements

- Python 3.10+
- [Whisper.cpp model file](https://huggingface.co/ggerganov/whisper.cpp/tree/main) (e.g. `ggml-tiny.en.bin`)
- `pip install -r requirements.txt`

### Quick Start

```bash
git clone https://github.com/<YOUR_USERNAME>/whisperlite.git
cd whisperlite
pip install -r requirements.txt
python src/main.py
```

### Platform Packaging

See [docs/BUILD\_INSTALL.md](docs/BUILD_INSTALL.md) for instructions on creating platform-specific executables.

---

## 📁 Output

* Files saved to `~/Downloads/` or equivalent, as:

  ```
  <username>_YYYYMMDD_HHMM.txt
  ```

---

## 💻 Repo Structure

```
src/       # App source code
models/    # Whisper model files (.bin)
tests/     # Unit and integration tests
docs/      # All specifications and architecture docs
```

---

## 📚 Documentation

* [Product Requirements](docs/PRODUCT_REQUIREMENTS.md)
* [Architecture](docs/ARCHITECTURE.md)
* [Functional Specification](docs/FUNCTIONAL_SPEC.md)
* [Platform Matrix](docs/PLATFORM_MATRIX.md)
* [Security & Privacy](docs/SECURITY_PRIVACY.md)
* [Build & Install](docs/BUILD_INSTALL.md)
* [Development Setup](docs/DEV_SETUP.md)
* [Test Plan](docs/TEST_PLAN.md)

---

## 🛡️ License

MIT License (see [LICENSE](LICENSE))

---

## 🤝 Contributing

See [docs/DEV\_SETUP.md](docs/DEV_SETUP.md) for onboarding, coding standards, and how to help!

---

## 🙏 Acknowledgements

* [Whisper.cpp](https://github.com/ggerganov/whisper.cpp)
* OpenAI for the Whisper model
