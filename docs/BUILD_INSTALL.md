# Build and Install Instructions — WhisperLite

This guide provides detailed instructions for building and installing WhisperLite from source on Windows, macOS, and Linux. For a simpler installation, pre-built installers are available on the [Releases](https://github.com/your-repo/whisperlite/releases) page.

##  Prerequisites

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

## 🚀 Build Steps

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/your-repo/whisperlite.git
    cd whisperlite
    ```

2.  **Download the Whisper.cpp Model**

    A pre-trained `whisper.cpp` model is required for transcription. The `build.sh` script will automatically download the `ggml-tiny.en.bin` model.

    ```bash
    # This script will also install Python and frontend dependencies
    ./build.sh
    ```

    Alternatively, you can download it manually:

    ```bash
    mkdir models
    curl -L -o models/ggml-tiny.en.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.en.bin
    ```

3.  **Install Dependencies**

    -   **Python Dependencies**

        ```bash
        pip install -r requirements.txt
        ```

    -   **Frontend Dependencies**

        ```bash
        cd ui
        npm install
        cd ..
        ```

4.  **Build the Application**

    The final step is to build the Tauri application. This will compile the Rust core, bundle the Python engine, and package the frontend into a single executable.

    ```bash
    # Navigate to the Rust directory and build
    cd rust
    cargo tauri build
    ```

    The compiled application will be located in `rust/target/release/`.

## 📦 Installation

After a successful build, you can install WhisperLite as follows:

-   **Windows**: Run the `.msi` installer found in `rust/target/release/bundle/msi/`.
-   **macOS**: Drag the `.app` bundle from `rust/target/release/bundle/macos/` to your `Applications` folder.
-   **Linux**: You can run the `AppImage` directly from `rust/target/release/bundle/appimage/`. To install it, you can use a tool like `AppImageLauncher`.

## Troubleshooting

-   **Build Failures**: Ensure all prerequisites are installed correctly. Run `rustup update` to get the latest version of Rust.
-   **Python Not Found**: Make sure `python3` is in your system's `PATH`.
-   **Permissions Errors**: On Linux and macOS, you may need to use `sudo` for some commands.