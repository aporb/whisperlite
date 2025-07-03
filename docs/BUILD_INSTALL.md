# Build and Install Instructions — WhisperLite

This guide provides detailed instructions for building and installing WhisperLite from source on Windows, macOS, and Linux. For a simpler installation, pre-built installers are available on the [Releases](https://github.com/your-repo/whisperlite/releases) page.

## Prerequisites

Before you begin, ensure you have the following dependencies installed on your system.

### 1. Rust

WhisperLite's core is built with Rust. If you don't have Rust installed, you can get it from [rust-lang.org](https://www.rust-lang.org/tools/install).

```bash
# Install Rust and Cargo (the Rust package manager)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### 2. Python

A Python environment (3.8+) is required for the transcription engine.

-   **Windows**: Install Python from the [Microsoft Store](https://www.microsoft.com/en-us/p/python-310/9pjpw5ldxlz5) or the [official website](https://www.python.org/downloads/).
-   **macOS**: Python is usually pre-installed. You can also use [Homebrew](https://brew.sh/) (`brew install python`).
-   **Linux**: Python is typically pre-installed on most distributions.

### 3. Node.js (for Tauri development)

Node.js is required for the Tauri CLI and managing frontend dependencies.

-   Install from [nodejs.org](https://nodejs.org/en/download/).

### 4. System-Specific Build Tools

-   **Windows**: Microsoft C++ Build Tools. You can install them with the Visual Studio Installer (select "Desktop development with C++").
-   **macOS**: Xcode Command Line Tools (`xcode-select --install`).
-   **Linux**: `build-essential` (or equivalent) and `libwebkit2gtk-4.0-dev`.

    ```bash
    # For Debian/Ubuntu
    sudo apt-get update
    sudo apt-get install build-essential libwebkit2gtk-4.0-dev
    ```

## Automated Builds and Installation

WhisperLite now uses automated GitHub Actions workflows to build and package the application for Windows, macOS, and Linux. Pre-built installers for the latest releases can be found on the [Releases](https://github.com/your-repo/whisperlite/releases) page.

### Building from Source (for Developers)

If you are a developer and wish to build WhisperLite from source, follow these steps:

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/your-repo/whisperlite.git
    cd whisperlite
    ```

2.  **Install Prerequisites**

    Ensure you have [Rust](https://www.rust-lang.org/tools/install), [Python 3.8+](https://www.python.org/downloads/), and [Node.js](https://nodejs.org/en/download/) installed. Also, install system-specific build tools as listed in the [Prerequisites](#-prerequisites) section above.

3.  **Run the Build Script**

    The `build.sh` script automates the setup of Python dependencies, downloads the Whisper model, and builds the Tauri application.

    ```bash
    ./build.sh
    ```

    Alternatively, you can manually install Python dependencies and build the Tauri app:

    ```bash
    # Install Python dependencies
    pip install -r requirements.txt

    # Download Whisper model (if not already present)
    # The application now supports in-app model download and management.

    # Build the Tauri application
    cd rust
    cargo tauri build
    ```

    The compiled application will be located in `rust/target/release/`.

### CLI/Headless Mode

WhisperLite can also be run from the command-line interface (CLI) or headless mode for scripting and automation. To use it, execute the `main.py` script directly with the `--input` and `--output` flags:

```bash
python src/main.py --input samples/hello.wav --model models/ggml-tiny.en.bin --output output.json --format json
```

**Arguments:**

-   `--input <path>`: Path to the audio file to transcribe (e.g., `.wav`, `.mp3`).
-   `--output <path>`: (Optional) Path to save the transcript. If not provided, the transcript will be saved in your system's Downloads folder with a generated filename.
-   `--format <txt|json|srt>`: (Optional) The output format for the transcript. Defaults to `txt`.
    -   `txt`: Plain text.
    -   `json`: JSON array of segments with start/end times and text.
    -   `srt`: SubRip format with indexed blocks and time ranges.
-   `--language <lang_code>`: (Optional) The language of the audio (e.g., `en` for English, `es` for Spanish). Defaults to `en`.

### Installation

After a successful build, you can install WhisperLite as follows:

-   **Windows**: Run the `.msi` installer found in `rust/target/release/bundle/msi/`.
-   **macOS**: Drag the `.app` bundle from `rust/target/release/bundle/macos/` to your `Applications` folder.
-   **Linux**: You can run the `AppImage` directly from `rust/target/release/bundle/appimage/`. To install it, you can use a tool like `AppImageLauncher`.

## Troubleshooting

-   **Build Failures**: Ensure all prerequisites are installed correctly. Run `rustup update` to get the latest version of Rust.
-   **Python Not Found**: Make sure `python3` is in your system's `PATH`.
-   **Permissions Errors**: On Linux and macOS, you may need to use `sudo` for some commands.
