# WhisperLite Setup Guide

## Quick Start

```bash
git clone https://github.com/aporb/whisperlite.git
cd whisperlite
./build.sh
```

## Manual Setup (if build.sh fails)

### 1. Install System Dependencies

**Linux (Ubuntu/Debian/Linux Mint):**
```bash
sudo apt update
sudo apt install -y \
    build-essential \
    curl \
    wget \
    file \
    libssl-dev \
    libgtk-3-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev \
    pkg-config

# Try newer packages first (Ubuntu 22.04+/Linux Mint 21+)
sudo apt install -y libwebkit2gtk-4.1-dev libjavascriptcoregtk-4.1-dev libsoup-3.0-dev

# If above fails, try older packages (Ubuntu 20.04/Linux Mint 20)
# sudo apt install -y libwebkit2gtk-4.0-dev libjavascriptcoregtk-4.0-dev libsoup2.4-dev
```

**macOS:**
```bash
# Install Xcode command line tools
xcode-select --install
```

**Windows:**
```bash
# Install Microsoft C++ Build Tools
# Install WebView2 (usually pre-installed on Windows 10/11)
```

### 2. Install Rust
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env
```

### 3. Setup Python Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Download Whisper Model
```bash
mkdir models
curl -o models/ggml-tiny.en.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/models/ggml-tiny.en.bin
```

### 5. Install Tauri CLI
```bash
cargo install tauri-cli
```

### 6. Run the Application
```bash
cd rust
cargo tauri dev
```

## Features

- **Floating Overlay Window**: Always-on-top, draggable, resizable
- **Real-time Transcription**: Live speech-to-text with visual feedback
- **Modern UI**: Dark theme with smooth animations
- **Keyboard Shortcuts**: 
  - `Ctrl/Cmd + R`: Start/Stop recording
  - `Ctrl/Cmd + S`: Save transcript
  - `Ctrl/Cmd + D`: Clear transcript
  - `Escape`: Stop recording
- **Auto-save**: Transcripts saved to Downloads folder with timestamps

## Troubleshooting

### "Model not found" error
Download the model manually:
```bash
mkdir models
curl -o models/ggml-tiny.en.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/models/ggml-tiny.en.bin
```

### Build errors on Linux
Install system dependencies:
```bash
sudo apt install libwebkit2gtk-4.0-dev build-essential libssl-dev libgtk-3-dev
```

### Python import errors
Activate virtual environment:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Audio permission issues
Grant microphone permissions when prompted by your system.

## Architecture

- **Frontend**: Modern web UI (HTML/CSS/JS) in Tauri window
- **Backend**: Rust for audio capture and system integration  
- **Transcription**: Python components with Whisper.cpp integration
- **Cross-platform**: Works on Linux, macOS, and Windows

For detailed technical information, see `docs/TAURI_IMPLEMENTATION.md`.
