# WhisperLite Architecture

WhisperLite employs a hybrid architecture combining Rust, Python, and Tauri to deliver a local-first, real-time speech transcription experience. This design leverages the strengths of each technology: Rust for high-performance audio capture and inter-process communication, Python for its robust machine learning ecosystem (specifically `whisper.cpp` integration), and Tauri for cross-platform desktop application development and UI rendering.

## 1. Overview

The core functionality of WhisperLite involves:
1.  **Audio Capture**: Real-time audio input from the microphone is captured.
2.  **Transcription**: Captured audio is processed by a `whisper.cpp` model to generate text transcripts.
3.  **Buffering**: Transcribed text segments are accumulated in a thread-safe buffer.
4.  **Display**: The live transcript is displayed in a floating overlay window.
5.  **Output**: Transcripts can be saved to various file formats (TXT, JSON, SRT).

All processing occurs locally on the user's machine, ensuring privacy and eliminating the need for an internet connection.

## 2. Component Breakdown

### 2.1. Rust Core (`rust/src/main.rs`)

The Rust component serves as the application's backend and handles critical low-level operations:
-   **Audio Capture**: Utilizes the `cpal` library to interface with the system's audio devices, capturing raw audio samples from the default input microphone.
-   **Process Management**: Spawns and manages the Python transcription subprocess, handling its `stdin` and `stdout` for inter-process communication.
-   **State Management**: Maintains the application's core state, including recording status, audio sender channels, and the transcript buffer.
-   **Tauri Integration**: Exposes commands to the Tauri frontend (e.g., `start_transcription`, `stop_transcription`, `get_transcript`, `save_transcript`, `clear_transcript`, `list_models`, `download_model`, `delete_model`).
-   **Model Management**: Handles listing, downloading, and deleting `whisper.cpp` model files.
-   **Transcript Buffer**: Manages the `TranscriptBuffer` (implemented in Rust) which stores transcribed text segments.

### 2.2. Python Logic (`src/`)

The Python components are responsible for the heavy lifting of transcription and output formatting:
-   **`main.py`**: The primary entry point for the Python application. It orchestrates the audio capture, transcription, and display/saving processes. It also handles command-line arguments for CLI/headless mode and the `save-transcript` functionality.
-   **`audio_capture.py`**: (Deprecated in favor of Rust's `cpal` for real-time audio streaming to Python `stdin`.) Previously handled audio capture and chunking into WAV files using `sounddevice`. In the current architecture, Rust streams raw audio bytes directly to Python's `stdin`.
-   **`transcriber.py`**: Interfaces with the `whisper.cpp` binary. It takes audio chunks (received via `stdin` from Rust), invokes the `whisper.cpp` subprocess, and parses its VTT output into structured text segments.
-   **`transcript_buffer.py`**: A Python-side `TranscriptBuffer` (though the primary buffer is now in Rust, this Python module might be used for internal Python-only buffering or for CLI mode). It provides thread-safe storage for transcribed text segments.
-   **`display.py`**: Implements a minimal Tkinter-based floating overlay window to display the live transcript. This is primarily used in the GUI mode.
-   **`output_writer.py`**: Handles saving the transcribed text to various file formats (TXT, JSON, SRT). It takes structured segments and formats them accordingly.
-   **`ui_controller.py`**: A simple class to manage UI-related events, particularly signaling when the UI requests the transcription process to stop.

### 2.3. Tauri Frontend (`ui/`, `rust/tauri.conf.json`)

Tauri provides the cross-platform desktop application framework and the user interface:
-   **Webview**: Renders the `ui/index.html`, `ui/script.js`, and `ui/styles.css` as the application's graphical user interface.
-   **API Bridge**: Facilitates communication between the webview (JavaScript) and the Rust backend (via `tauri::invoke_handler`).
-   **Bundling**: Packages the Rust binary, Python scripts, and web assets into a single, distributable application.

## 3. Data Flow

The primary data flow for real-time transcription is as follows:

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

For saving transcripts:

```mermaid
graph TD
    A[Tauri Frontend - `save_transcript` command] --> B{Rust `save_transcript` command};
    B --> C[Rust TranscriptBuffer - `get_segments`];
    C --> D{Serialized Segments JSON};
    D --> E[Python Subprocess `src/main.py --save-transcript` (stdin)];
    E --> F(Python `output_writer.py`);
    F --> G[Saved File (TXT/JSON/SRT)];
```

## 4. Inter-process Communication (IPC)

Communication between the Rust backend and the Python transcription process is primarily achieved via `stdin` and `stdout`:
-   **Rust to Python**: Raw audio bytes are streamed from Rust's audio capture directly to the Python subprocess's `stdin`.
-   **Python to Rust**: Transcribed text (parsed VTT segments) is printed to Python's `stdout` by `transcriber.py` and captured by the Rust process, which then updates the `TranscriptBuffer`.
-   **Tauri to Rust**: The Tauri frontend communicates with the Rust backend using `tauri::invoke_handler` for commands like starting/stopping transcription, getting the current transcript, and saving.
-   **Rust to Tauri**: Rust can send events back to the Tauri frontend for UI updates or status changes.

## 5. Key Design Choices

-   **Hybrid Approach**: Balances performance-critical audio handling (Rust) with the rich ML ecosystem (Python).
-   **Local-First**: Emphasizes user privacy and offline functionality by performing all transcription locally.
-   **`whisper.cpp`**: Chosen for its efficiency and ability to run large language models locally on various hardware.
-   **Tauri**: Provides a modern, lightweight, and cross-platform UI framework, leveraging web technologies.
-   **`stdin`/`stdout` IPC**: Simple and effective for streaming data between Rust and Python, though it requires careful error handling and process management.
