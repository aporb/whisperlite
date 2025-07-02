# WhisperLite

**WhisperLite** is a lightweight, local-first, real-time transcription application that runs on your desktop. It uses the power of `whisper.cpp` to provide fast and accurate transcriptions without sending your data to the cloud.

![WhisperLite UI](https://i.imgur.com/your-screenshot.png)

## ✨ Features

-   **Real-Time Transcription**: Get a live feed of your speech as you talk.
-   **Local-First**: All processing is done on your device. No internet connection required.
-   **Cross-Platform**: Works on Windows, macOS, and Linux.
-   **Lightweight**: Minimal resource usage.
-   **Always-on-Top**: The overlay window stays on top of other applications for easy access.
-   **Save to File**: Save your transcripts to a `.txt` file with a single click.

## 🚀 Getting Started

### Installation

Download the latest version for your operating system from the [Releases](https://github.com/your-repo/whisperlite/releases) page.

### Usage

1.  Launch the application.
2.  Click the "Start" button to begin transcription.
3.  Click the "Stop" button to end transcription.
4.  Click the "Save" button to save the transcript to your `Downloads` folder.

## 🏗️ Architecture

WhisperLite uses a hybrid architecture that combines a Rust core, a Python transcription engine, and a Tauri-based web frontend.

```
┌─────────────────────────────────────────────────────────────┐
│                    Tauri Application (Rust)                 │
├─────────────────────────────────────────────────────────────┤
│  Frontend (WebView - ui/)                                   │
│  Backend (Rust Core)                                        │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Python Transcription Engine                │
└─────────────────────────────────────────────────────────────┘
```

For a more detailed explanation, see the [Architecture](docs/ARCHITECTURE.md) document.

## ✅ MVP Checklist

-   [x] Real-time transcription
-   [x] Local-first processing
-   [x] Cross-platform support
-   [x] Save transcript to file
-   [x] Floating overlay window
-   [x] Custom model selection
-   [ ] Multiple output formats (JSON, SRT)

## 🤝 Contributing

Contributions are welcome! Please see the [Contributing Guide](docs/CONTRIBUTING.md) for more information.

## 📄 License

This project is licensed under the [MIT License](LICENSE).