#!/usr/bin/env bash
# --------------------------------------------------------------------------------
# setup_whisperlite.sh
#
# A comprehensive script to scaffold the WhisperLite project folder, files, Git
# initialization, and GitHub remote creation/push. 
#
# Usage: 
#   1. Make sure `git` and GitHub CLI (`gh`) are installed and authenticated.
#   2. From an empty or target directory, run: ./setup_whisperlite.sh
#   3. Follow prompts for GitHub username and repo name.
#
# --------------------------------------------------------------------------------

set -euo pipefail

#############################################
# 1. Helper Functions
#############################################

print_banner() {
  cat << "EOF"
*************************************************************
*                                                           *
*          WhisperLite: Real-Time Transcription Tool         *
*      Setup Script — Creates Local & GitHub Repo for You   *
*                                                           *
*************************************************************
EOF
}

check_dependency() {
  local cmd="$1"
  if ! command -v "$cmd" &> /dev/null; then
    echo "ERROR: Required command '$cmd' not found in PATH. Please install it and try again."
    exit 1
  fi
}

prompt_for_continue() {
  read -p "⚠️  Directory is not empty. Continue anyway? [y/N]: " yn
  case "$yn" in
    [Yy]* ) echo "Proceeding...";;
    * ) echo "Aborting."; exit 1;;
  esac
}

#############################################
# 2. Initial Checks & Banner
#############################################

print_banner

# 2.1 Check for required commands: git, gh
check_dependency "git"
check_dependency "gh"

# 2.2 Ensure current directory is appropriate
if [ "$(ls -A .)" ]; then
  echo "Notice: Current directory is not empty:"
  ls -1A
  prompt_for_continue
fi

# 2.3 Capture timestamp for use in file headers (optional)
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

#############################################
# 3. Create Project Structure & Files
#############################################

echo "✅  Creating project folders..."

mkdir -p src
mkdir -p models
mkdir -p tests
mkdir -p docs

echo "✅  Writing project files..."

# 3.1 Top-level README.md
cat << 'EOF' > README.md
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
EOF

# 3.2 LICENSE (MIT)

cat << 'EOF' > LICENSE
MIT License

Copyright (c) 2025 WhisperLite

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# 3.3 .gitignore

cat << 'EOF' > .gitignore
**pycache**/
\*.pyc
\*.pyo
\*.pyd
models/
\*.bin
\*.wav
\*.flac
\*.mp3
.DS\_Store
.env
dist/
build/
\*.egg-info
EOF

# 3.4 requirements.txt

cat << 'EOF' > requirements.txt
sounddevice
numpy
EOF

# 3.5 Makefile

cat << 'EOF' > Makefile
run:
\tpython src/main.py

test:
\tpytest tests/

build:
\t# Insert packaging commands here (e.g., PyInstaller, py2app, etc.)
\techo "Packaging commands to be added."

EOF

# 3.6 src/main.py

cat << 'EOF' > src/main.py
\#!/usr/bin/env python3
"""
main.py — Entry point for WhisperLite
Orchestrates audio capture, real-time transcription, live display, and file output.
"""

def main():
\# TODO: Orchestrate:
\#   - Start audio\_capture
\#   - Feed data to Transcriber (Whisper.cpp)
\#   - Update LiveDisplay with partial text
\#   - On stop, hand off to OutputWriter to save final transcript
print("WhisperLite starting... (features not yet implemented)")

if **name** == "**main**":
main()
EOF
chmod +x src/main.py

# 3.7 src/audio\_capture.py

cat << 'EOF' > src/audio\_capture.py
"""
audio\_capture.py — Capture microphone audio in chunks for real-time transcription.
"""

def initialize\_audio\_stream():
'''
TODO: Use sounddevice (or PyAudio) to start recording in 1–2 second chunks,
then hand off each chunk to the Transcriber module.
'''
pass
EOF

# 3.8 src/transcriber.py

cat << 'EOF' > src/transcriber.py
"""
transcriber.py — Invoke Whisper.cpp for streaming transcription of audio chunks.
"""

def transcribe\_chunk(audio\_chunk\_path):
'''
TODO: Call whisper.cpp binary with streaming flags,
return partial/transcribed text to LiveDisplay.
'''
pass
EOF

# 3.9 src/display.py

cat << 'EOF' > src/display.py
"""
display.py — Render a minimal, always-on-top overlay window that shows rolling transcript.
"""

def update\_display(text\_fragment):
'''
TODO: Append or refresh the overlay window with new text from Transcriber.
'''
pass
EOF

# 3.10 src/output\_writer.py

cat << 'EOF' > src/output\_writer.py
"""
output\_writer.py — After recording stops, compile full transcript and save to .txt file.
"""

def save\_transcript(full\_text, username, timestamp, output\_dir):
'''
TODO: Create file named: <username>*<YYYYMMDD>*<HHMM>.txt in output\_dir (Downloads),
write headers and the full transcript content, then close.
'''
pass
EOF

# 3.11 tests/test\_audio\_capture.py

cat << 'EOF' > tests/test\_audio\_capture.py
import pytest

def test\_audio\_capture\_initialization():
\# TODO: Implement unit tests for audio\_capture module
assert True
EOF

# 3.12 tests/test\_transcriber.py

cat << 'EOF' > tests/test\_transcriber.py
import pytest

def test\_transcriber\_stub():
\# TODO: Implement unit tests for transcriber module
assert True
EOF

# 3.13 tests/test\_output\_writer.py

cat << 'EOF' > tests/test\_output\_writer.py
import pytest

def test\_output\_writer\_stub():
\# TODO: Implement unit tests for output\_writer module
assert True
EOF

# 3.14 docs/PRODUCT\_REQUIREMENTS.md

cat << 'EOF' > docs/PRODUCT\_REQUIREMENTS.md

# Product Requirements Document (PRD) — WhisperLite

## Objective

Enable local, real-time speech transcription on any major OS, saving output to a timestamped, user-named .txt file in Downloads.

## Use Case

* User launches app, speaks, sees live transcript, and on stopping gets a file in Downloads.

## Functional Requirements

* Real-time transcription, rolling display, cross-platform, output as \<username>*\<YYYYMMDD>*\<HHMM>.txt

## Non-functional Requirements

* Lightweight, local-only, no internet required, under 100MB RAM at run-time, model <50MB
EOF

# 3.15 docs/ARCHITECTURE.md

cat << 'EOF' > docs/ARCHITECTURE.md

# Architecture Overview — WhisperLite

## System Diagram

Audio Capture (chunks) → Streaming Whisper Transcriber → Live Text Overlay → Output Writer (on stop)

## Modules

* audio\_capture.py — microphone streaming
* transcriber.py — invokes whisper.cpp
* display.py — updates overlay window
* output\_writer.py — saves final text
EOF

# 3.16 docs/FUNCTIONAL\_SPEC.md

cat << 'EOF' > docs/FUNCTIONAL\_SPEC.md

# Functional Specification — WhisperLite

## Flow

1. User launches app
2. App starts capturing audio, splits into 1–2 second chunks
3. Each chunk is sent to whisper.cpp
4. Transcribed text is appended and shown live in overlay
5. On stop, transcript is finalized, saved as .txt
EOF

# 3.17 docs/PLATFORM\_MATRIX.md

cat << 'EOF' > docs/PLATFORM\_MATRIX.md

# Platform Support Matrix — WhisperLite

| Feature     | Windows | macOS | Linux            |
| ----------- | ------- | ----- | ---------------- |
| Mic access  | ✅       | ✅     | ✅                |
| Output file | ✅       | ✅     | ✅                |
| Installer   | .exe    | .app  | .AppImage / .deb |
EOF

# 3.18 docs/SECURITY\_PRIVACY.md

cat << 'EOF' > docs/SECURITY\_PRIVACY.md

# Security & Privacy — WhisperLite

* No data leaves device
* No telemetry or analytics
* No cloud, no internet requirement
* Temporary audio files deleted after usage
EOF

# 3.19 docs/BUILD\_INSTALL.md

cat << 'EOF' > docs/BUILD\_INSTALL.md

# Build & Install Instructions — WhisperLite

## Dependencies

* Python 3.10+
* `sounddevice`, `numpy`
* `whisper.cpp` model (.bin)

## Build Steps

1. pip install -r requirements.txt
2. Download and place model in /models
3. python src/main.py

## Packaging

* Windows: PyInstaller → `.exe`
* macOS: py2app or Tauri → `.app`
* Linux: AppImage or `.deb`
EOF

# 3.20 docs/DEV\_SETUP.md

cat << 'EOF' > docs/DEV\_SETUP.md

# Development Setup — WhisperLite

## Environment

* Python 3.10+
* Recommended: Virtual environment (venv)

## Onboarding

1. Fork the repo, clone locally
2. pip install -r requirements.txt
3. Download `ggml-*.bin` model into /models
4. Run: python src/main.py
EOF

# 3.21 docs/TEST\_PLAN.md

cat << 'EOF' > docs/TEST\_PLAN.md

# Test Plan — WhisperLite

## Unit Tests

* Audio capture, chunking, error handling
* Whisper transcription (stub)

## Integration

* End-to-end: record → transcribe → save

## Edge Cases

* No mic present
* No write permission in Downloads

## Manual Testing

* UI appearance
* Resource usage
EOF

echo "✅  Project files and folders created successfully."

#############################################

# 4. Initialize Git & Commit

#############################################

echo "🔧  Initializing Git repository..."
git init -q
git add .
git commit -m "Initial commit: Scaffold WhisperLite project structure" -q
echo "✅  Git repository initialized and initial commit created."

#############################################
# 5. GitHub Remote Creation & Push
#############################################

# 5.1 Check if 'gh' is authenticated
if ! gh auth status &> /dev/null; then
  echo "❌ You are not authenticated with GitHub CLI. Run: gh auth login"
  exit 1
fi

# 5.2 Prompt for GitHub Username and Repo Name
echo
echo "----------------------------------------------"
echo "🏷️  GitHub Repository Setup"
echo "----------------------------------------------"
read -p "Enter your GitHub username (e.g. your-username): " GH_USERNAME
read -p "Enter the name of the new GitHub repo (e.g. whisperlite): " REPO_NAME

# 5.3 Create the remote repository on GitHub and push
echo "🔗  Creating GitHub repository '$GH_USERNAME/$REPO_NAME'..."
gh repo create "$GH_USERNAME/$REPO_NAME" \
  --public \
  --source="." \
  --remote="origin" \
  --push \
  --confirm

echo "✅  Remote repository created and code pushed to GitHub."

#############################################
# 6. Final Message
#############################################

echo
echo "*************************************************************"
echo "🎉  WhisperLite repository is ready!"
echo "Local files: $(pwd)"
echo "GitHub URL: https://github.com/$GH_USERNAME/$REPO_NAME"
echo
echo "Next Steps:"
echo "  • Clone elsewhere or collaborate via pull requests."
echo "  • Start implementing modules in src/, updating docs in docs/, and writing tests in tests/."
echo "  • When ready, update README.md with usage instructions, or publish new releases."
echo
echo "Happy coding! 🚀"
echo "*************************************************************"
