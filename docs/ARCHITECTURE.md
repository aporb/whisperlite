# Architecture Overview — WhisperLite

WhisperLite is a hybrid desktop application that combines a Rust core, a Python transcription engine, and a Tauri-based web frontend to deliver a lightweight, local-first, real-time transcription experience.

## 🏗️ System Architecture Diagram

The architecture is designed to be modular and cross-platform, separating concerns between the user interface, system-level operations, and the core transcription logic.

```
┌─────────────────────────────────────────────────────────────┐
│                    Tauri Application (Rust)                 │
│                       (rust/src/main.rs)                    │
├─────────────────────────────────────────────────────────────┤
│  Frontend (WebView - ui/)                                   │
│  ├── index.html     - Main UI structure (HTML)              │
│  ├── styles.css     - Modern dark theme & animations (CSS)  │
│  └── script.js      - Frontend logic & Tauri API calls (JS) │
├─────────────────────────────────────────────────────────────┤
│  Backend (Rust Core)                                        │
│  ├── Audio Capture  - CPAL-based low-level microphone input │
│  ├── Tauri Commands - Secure API endpoints for the frontend│
│  ├── Python Bridge  - Manages and calls Python subprocess  │
│  └── State Management - Thread-safe application state      │
└─────────────────────────────────────────────────────────────┘
                         │
                         │ (Spawns and communicates via stdin/stdout)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Python Transcription Engine                │
│                         (src/__main__.py)                   │
├─────────────────────────────────────────────────────────────┤
│  ├── Transcriber    - Interfaces with Whisper.cpp model     │
│  │  (transcriber.py)                                        │
│  ├── Audio Handling - Processes audio chunks from Rust     │
│  │  (audio_capture.py - in test mode)                       │
│  └── Buffer & Output- Manages transcript and saves to file │
│     (transcript_buffer.py, output_writer.py)                │
└─────────────────────────────────────────────────────────────┘
```

##  fluxo de dados

The data flows through the system in a clear, unidirectional path:

1.  **Audio Input**: The **Rust backend** uses the `cpal` library to capture raw audio samples from the default microphone. This approach is efficient and avoids the overhead of Python's Global Interpreter Lock (GIL) for I/O-bound tasks.
2.  **Chunking & Formatting**: Audio is captured in 1.5-second chunks and converted into a WAV-like byte format in memory.
3.  **Python Bridge**: The Rust backend spawns the **Python transcription engine** as a long-running subprocess. It sends the audio chunks to the Python process's `stdin`.
4.  **Transcription**: The Python process receives the audio data, feeds it into the `whisper.cpp` model via the `transcriber.py` module, and generates a text snippet.
5.  **State Management**: The transcribed text is sent back to the Rust backend via `stdout`. Rust stores the accumulating transcript in a thread-safe `AppState` structure, specifically within an `Arc<RwLock<Vec<String>>>`.
6.  **UI Updates**: The **Tauri frontend** (JavaScript) polls the Rust backend every second using the `get_transcript` command.
7.  **Live Display**: When the frontend receives new text, it dynamically updates the DOM to display the live transcription in the floating overlay window.
8.  **Saving**: When the user clicks "Save" or uses the `Ctrl/Cmd + S` shortcut, the frontend invokes the `save_transcript` command. The Rust backend then calls the `output_writer.py` logic (via the Python process) to write the full transcript from the buffer into a timestamped `.txt` file in the user's `Downloads` directory.

## 📦 Component Responsibilities

### 1. Rust Core (`rust/src/main.rs`)

-   **Primary Role**: Manages the application lifecycle, windowing, and low-level system interactions.
-   **Audio Capture**: Uses `cpal` for direct, high-performance access to the system's microphone.
-   **State Management**: Holds the single source of truth for the application's state (e.g., `is_recording`, `transcript_buffer`) using thread-safe wrappers (`Arc`, `RwLock`).
-   **Tauri Commands**: Exposes a secure and well-defined API (`start_transcription`, `stop_transcription`, etc.) that the frontend can invoke.
-   **Python Process Management**: Spawns, monitors, and communicates with the Python subprocess, handling all `stdin`/`stdout` piping and error cases.

### 2. Python Engine (`src/`)

-   **Primary Role**: Executes the core AI/ML task of speech-to-text conversion.
-   **`transcriber.py`**: A focused module that contains the logic for loading the `whisper.cpp` model and running inference on audio data.
-   **`transcript_buffer.py`**: A thread-safe buffer that accumulates transcribed text segments. This is crucial for maintaining the full context of the conversation.
-   **`output_writer.py`**: Handles the formatting and saving of the final transcript to a `.txt` file, ensuring the correct filename and directory.
-   **`main.py`**: Serves as the entry point for the Python side, responsible for parsing commands from the Rust bridge and orchestrating the transcription pipeline.

### 3. Tauri Frontend (`ui/`)

-   **Primary Role**: Provides the user interface and user experience.
-   **`index.html`**: The semantic structure of the overlay window.
-   **`styles.css`**: Defines the modern, dark, "glassmorphism" aesthetic, including animations and responsive behavior.
-   **`script.js`**: Contains all client-side logic, including:
    -   Invoking Tauri commands to interact with the backend.
    -   Polling for transcript updates and rendering them to the screen.
    -   Handling user interactions (button clicks, keyboard shortcuts).
    -   Managing UI state (e.g., displaying "Recording" or "Stopped" status).

## 🛡️ Security & Sandboxing

The hybrid architecture provides a strong security posture:

-   The **Tauri frontend** runs in a sandboxed WebView, preventing it from accessing the local filesystem or executing arbitrary code outside its intended scope.
-   All interactions with the host system (like saving a file or accessing the microphone) are brokered by the **Rust core** through the explicit `tauri::command` API. This ensures that the web-based UI cannot perform any privileged operations without permission.
-   The **Python engine** is a completely isolated subprocess, further containing the AI model and its dependencies. It has no direct access to the network or user files, except for what is explicitly passed to it by the Rust core.