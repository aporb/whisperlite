# WhisperLite

**WhisperLite** is a lightweight, local-first, real-time speech transcription application that runs on your desktop. It leverages a hybrid Rust-Python-Tauri architecture to provide fast, accurate, and private transcriptions without sending your data to the cloud.

![WhisperLite UI Screenshot](https://via.placeholder.com/800x450.png?text=WhisperLite+UI+Screenshot)

## ✨ Features

-   **Real-Time Transcription**: Get a live feed of your speech as you talk.
-   **Local-First & Private**: All processing is done on your device. No internet connection required, and no data leaves your machine.
-   **Cross-Platform**: Works seamlessly on Windows, macOS, and Linux.
-   **Lightweight**: Designed for minimal resource usage.
-   **Always-on-Top Overlay**: The transcript display window stays on top of other applications for easy access.
-   **Multiple Output Formats**: Save your transcripts to `.txt`, `.json`, or `.srt` files.
-   **CLI/Headless Mode**: Transcribe audio files directly from the command line for scripting and automation.
-   **In-app Model Management**: Easily select, download, and manage `whisper.cpp` models directly within the application.

## 🚀 Getting Started

### Installation

Download the latest version for your operating system from the [Releases](https://github.com/your-repo/whisperlite/releases) page.

### Usage (GUI)

1.  Launch the application.
2.  Click the "Start" button to begin real-time transcription.
3.  Click the "Stop" button to end transcription.
4.  Click the "Save" button to save the transcript to your `Downloads` folder in your chosen format.

### Usage (CLI/Headless Mode)

WhisperLite can also be run from the command line for scripting and automation. This mode allows you to transcribe audio files directly and save the output in various formats.

```bash
python src/main.py --input <path_to_audio_file> --model <path_to_whisper_model> [--output <output_file_path>] [--format <txt|json|srt>] [--language <lang_code>]
```

**Example:**

```bash
python src/main.py --input samples/hello.wav --model models/ggml-tiny.en.bin --output output.json --format json --language en
```

**Arguments:**

-   `--input <path>`: Path to the audio file to transcribe (e.g., `.wav`, `.mp3`).
-   `--model <path>`: Path to the `whisper.cpp` model file (e.g., `models/ggml-tiny.en.bin`).
-   `--output <path>`: (Optional) Path to save the transcript. If not provided, the transcript will be saved in your system's Downloads folder with a generated filename.
-   `--format <txt|json|srt>`: (Optional) The output format for the transcript. Defaults to `txt`.
    -   `txt`: Plain text.
    -   `json`: JSON array of segments with start/end times and text.
    -   `srt`: SubRip format with indexed blocks and time ranges.
-   `--language <lang_code>`: (Optional) The language of the audio (e.g., `en` for English, `es` for Spanish). Defaults to `en`.

## 🏗️ Architecture

WhisperLite employs a hybrid architecture combining Rust, Python, and Tauri. Rust handles high-performance audio capture and inter-process communication, Python manages `whisper.cpp` transcription, and Tauri provides the cross-platform GUI.

```mermaid
graph TD
    A[Microphone Input] --> B(Rust Audio Capture - `cpal`);
    B --> C{Raw Audio Bytes};
    C --> D[Python Subprocess `src/main.py` (stdin)];
    D --> E(Python `transcriber.py`);
    E --> F{VTT Output};
    F --> G(Python `transcriber.py` Parsing);
    G --> H{Structured Text Segments};
    H --> I[Rust TranscriptBuffer];
    I --> J(Tauri Frontend - `get_transcript` command);
    J --> K[UI Display];
```

For a more detailed explanation, see the [Architecture](docs/ARCHITECTURE.md) document.

## ✅ MVP Checklist

-   [x] Real-time transcription
-   [x] Local-first processing
-   [x] Cross-platform support
-   [x] Save transcript to file
-   [x] Floating overlay window
-   [x] Custom model selection
-   [x] Multiple output formats (JSON, SRT)
-   [x] CLI/headless mode

## 🤝 Contributing

Contributions are welcome! Please see the [Contributing Guide](docs/CONTRIBUTING.md) for more information.

## 🧑‍💻 Contributors

-   [Your Name/GitHub Handle Here](https://github.com/your-profile)

## 📄 License

This project is licensed under the [MIT License](LICENSE).
