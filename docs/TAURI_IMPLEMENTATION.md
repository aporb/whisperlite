# Tauri Implementation Guide — WhisperLite

This document explains the new Tauri-based architecture for WhisperLite's Live Overlay Display.

## 🏗️ Architecture Overview

WhisperLite now uses a hybrid architecture:

- **Frontend**: Modern web technologies (HTML/CSS/JavaScript) in a Tauri window
- **Backend**: Rust for audio capture and system integration
- **Transcription**: Python components called from Rust backend
- **UI**: Floating overlay window with modern design

```
┌─────────────────────────────────────────────────────────────┐
│                    Tauri Application                        │
├─────────────────────────────────────────────────────────────┤
│  Frontend (ui/)                                             │
│  ├── index.html     - Main UI structure                     │
│  ├── styles.css     - Modern dark theme styling            │
│  └── script.js      - Frontend logic & Tauri API calls     │
├─────────────────────────────────────────────────────────────┤
│  Backend (rust/src/main.rs)                                │
│  ├── Audio Capture  - CPAL-based microphone input         │
│  ├── Tauri Commands - API endpoints for frontend          │
│  ├── Python Bridge  - Calls Python transcriber           │
│  └── State Management - Thread-safe app state            │
├─────────────────────────────────────────────────────────────┤
│  Python Components (src/)                                  │
│  ├── transcriber.py - Whisper.cpp integration             │
│  ├── transcript_buffer.py - Thread-safe transcript store  │
│  └── Other modules  - Audio capture, output writing       │
└─────────────────────────────────────────────────────────────┘
```

## 🎨 UI Features

### Modern Design
- **Dark theme** with professional color scheme
- **Glassmorphism effects** with subtle transparency
- **Smooth animations** for state transitions
- **Responsive layout** that works at different window sizes

### Window Behavior
- **Always on top** - stays visible over other applications
- **Draggable** - can be moved around the screen
- **Resizable** - minimum size constraints with resize handle
- **Corner positioning** - starts in top-left corner by default

### Controls
- **Start/Stop** - Begin and end transcription
- **Save** - Export transcript to Downloads folder
- **Clear** - Reset transcript buffer
- **Status indicator** - Visual feedback for app state

### Keyboard Shortcuts
- `Ctrl/Cmd + R` - Start/Stop recording
- `Ctrl/Cmd + S` - Save transcript
- `Ctrl/Cmd + D` - Clear transcript
- `Escape` - Stop recording (if active)

## 🔧 Technical Implementation

### Tauri Commands

The frontend communicates with the Rust backend through these commands:

```rust
#[tauri::command]
async fn start_transcription(state: State<'_, AppState>) -> Result<CommandResponse, ()>

#[tauri::command]
async fn stop_transcription(state: State<'_, AppState>) -> Result<CommandResponse, ()>

#[tauri::command]
async fn get_transcript(state: State<'_, AppState>) -> Result<CommandResponse, ()>

#[tauri::command]
async fn save_transcript(state: State<'_, AppState>) -> Result<CommandResponse, ()>

#[tauri::command]
async fn clear_transcript(state: State<'_, AppState>) -> Result<CommandResponse, ()>
```

### Audio Processing Flow

1. **Audio Capture**: CPAL captures microphone input in 1.5-second chunks
2. **WAV Generation**: Raw audio data is converted to WAV format
3. **Python Integration**: Rust calls Python transcriber via subprocess
4. **Transcript Update**: Results are stored in thread-safe buffer
5. **UI Update**: Frontend polls for updates every second

### State Management

```rust
struct AppState {
    transcript_buffer: Arc<RwLock<Vec<String>>>,
    is_recording: Arc<RwLock<bool>>,
    audio_sender: Arc<RwLock<Option<Sender<Vec<i16>>>>>,
    stream_handle: Arc<RwLock<Option<cpal::Stream>>>,
}
```

## 🚀 Development Workflow

### Prerequisites
- Rust (latest stable)
- Python 3.8+
- Node.js (optional, for enhanced development)
- Whisper model file

### Quick Start
```bash
# Clone and setup
git clone <repo>
cd whisperlite
./build.sh

# Or manual setup
pip install -r requirements.txt
cargo install tauri-cli
cd rust && cargo tauri dev
```

### Development Commands
```bash
# Run in development mode
cd rust && cargo tauri dev

# Build for production
cd rust && cargo tauri build

# Test Python components
python src/main.py --test

# Run Rust tests
cargo test --manifest-path rust/Cargo.toml
```

## 📁 File Structure

```
whisperlite/
├── ui/                          # Frontend assets
│   ├── index.html              # Main UI
│   ├── styles.css              # Styling
│   └── script.js               # Frontend logic
├── rust/                       # Tauri backend
│   ├── src/main.rs            # Main Rust application
│   ├── Cargo.toml             # Rust dependencies
│   ├── tauri.conf.json        # Tauri configuration
│   └── icons/                 # Application icons
├── src/                        # Python components
│   ├── transcriber.py         # Whisper integration
│   ├── transcript_buffer.py   # Buffer management
│   └── main.py                # Python entry point
├── models/                     # Whisper models (gitignored)
└── build.sh                   # Setup script
```

## 🎯 Epic #2 Completion

This implementation completes all tasks in Epic #2:

### ✅ Task #10: Build floating overlay using Tauri
- Modern Tauri-based floating window
- Always-on-top behavior
- Draggable and resizable
- Professional dark theme UI

### ✅ Task #11: Connect live transcript feed to display
- Real-time transcript polling
- Smooth text updates with animations
- Auto-scroll to latest content
- Thread-safe data flow

### ✅ Task #12: Add UI controls
- Start/Stop recording buttons
- Save and Clear functionality
- Visual status indicators with animations
- Keyboard shortcuts for power users

### ✅ Task #13: Implement graceful exit and buffer flush
- Proper cleanup on window close
- Audio stream termination
- Final transcript save
- Thread cleanup and resource management

## 🔍 Troubleshooting

### Common Issues

**Model not found**
```bash
mkdir models
curl -o models/ggml-tiny.en.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/models/ggml-tiny.en.bin
```

**Python not found**
- Ensure Python 3 is installed and accessible as `python3`
- Check that all Python dependencies are installed

**Audio permissions**
- Grant microphone permissions when prompted
- Check system audio settings

**Build failures**
- Ensure Rust is up to date: `rustup update`
- Install Tauri CLI: `cargo install tauri-cli`

## 🚀 Future Enhancements

Potential improvements for future versions:

1. **Multiple model support** - Allow switching between different Whisper models
2. **Custom themes** - User-configurable color schemes
3. **Export formats** - Support for JSON, SRT, VTT formats
4. **Hotkey customization** - User-defined keyboard shortcuts
5. **Window presets** - Saved window positions and sizes
6. **Real-time confidence scores** - Display transcription confidence
7. **Language detection** - Automatic language switching
8. **Plugin system** - Extensible architecture for custom features

## 📚 Resources

- [Tauri Documentation](https://tauri.app/v1/guides/)
- [CPAL Audio Library](https://docs.rs/cpal/)
- [Whisper.cpp](https://github.com/ggerganov/whisper.cpp)
- [Rust Cross-platform Development](https://forge.rust-lang.org/infra/cross-platform-support.html)
