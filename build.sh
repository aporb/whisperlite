#!/bin/bash

# WhisperLite Build Script
# This script helps set up and run the WhisperLite application

set -e

echo "🎙️  WhisperLite Build Script"
echo "=========================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check dependencies
echo "📋 Checking dependencies..."

if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

if ! command_exists cargo; then
    echo "❌ Rust/Cargo is required but not installed"
    echo "   Install from: https://rustup.rs/"
    exit 1
fi

if ! command_exists node; then
    echo "⚠️  Node.js not found - some Tauri features may not work optimally"
fi

# Check for Tauri system dependencies on Linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Checking Linux system dependencies for Tauri..."
    
    # Check if we can install packages (has sudo)
    if command_exists sudo; then
        echo "📦 Installing required system dependencies..."
        sudo apt update
        
        # Try the newer package names first, then fall back to older ones
        echo "🔧 Installing WebKit and GTK dependencies..."
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
            
        # Try to install WebKit2GTK (different package names on different Ubuntu versions)
        if sudo apt install -y libwebkit2gtk-4.1-dev 2>/dev/null; then
            echo "✅ Installed libwebkit2gtk-4.1-dev"
        elif sudo apt install -y libwebkit2gtk-4.0-dev 2>/dev/null; then
            echo "✅ Installed libwebkit2gtk-4.0-dev"
        else
            echo "⚠️  Could not install WebKit2GTK development package"
            echo "   Please install manually: sudo apt install libwebkit2gtk-4.1-dev"
        fi
        
        # Try to install JavaScriptCore (different package names)
        if sudo apt install -y libjavascriptcoregtk-4.1-dev 2>/dev/null; then
            echo "✅ Installed libjavascriptcoregtk-4.1-dev"
        elif sudo apt install -y libjavascriptcoregtk-4.0-dev 2>/dev/null; then
            echo "✅ Installed libjavascriptcoregtk-4.0-dev"
        else
            echo "⚠️  Could not install JavaScriptCore development package"
            echo "   Please install manually: sudo apt install libjavascriptcoregtk-4.1-dev"
        fi
        
        # Try to install libsoup (different versions)
        if sudo apt install -y libsoup-3.0-dev 2>/dev/null; then
            echo "✅ Installed libsoup-3.0-dev"
        elif sudo apt install -y libsoup2.4-dev 2>/dev/null; then
            echo "✅ Installed libsoup2.4-dev"
        else
            echo "⚠️  Could not install libsoup development package"
        fi
        
        echo "✅ System dependencies installation completed"
    else
        echo "⚠️  Please install the following system dependencies manually:"
        echo "   sudo apt install build-essential curl wget file libssl-dev libgtk-3-dev"
        echo "   sudo apt install libwebkit2gtk-4.1-dev libjavascriptcoregtk-4.1-dev libsoup-3.0-dev"
        echo "   (or try the -4.0 versions if -4.1 packages are not available)"
    fi
fi

echo "✅ Dependencies check passed"

# Check for models
echo "🤖 Checking for Whisper models..."
if [ ! -d "models" ]; then
    echo "📁 Creating models directory..."
    mkdir -p models
fi

if [ ! -f "models/ggml-tiny.en.bin" ]; then
    echo "⬇️  Downloading tiny English model..."
    echo "   This may take a few minutes..."
    curl -L -o models/ggml-tiny.en.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/models/ggml-tiny.en.bin
    echo "✅ Model downloaded successfully"
else
    echo "✅ Model found: models/ggml-tiny.en.bin"
fi

# Install Python dependencies
echo "🐍 Setting up Python environment..."
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "🔧 Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Test Python components
echo "🧪 Testing Python components..."
python3 src/main.py --test

# Build and run Tauri app
echo "🚀 Building and running Tauri application..."
cd rust

# Install Tauri CLI if not present
if ! command_exists cargo-tauri; then
    echo "📦 Installing Tauri CLI..."
    cargo install tauri-cli
fi

echo "🔨 Building Tauri application..."
cargo tauri dev

echo "✅ WhisperLite setup complete!"
