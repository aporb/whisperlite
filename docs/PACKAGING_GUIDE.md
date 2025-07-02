# Packaging Guide — WhisperLite

This guide details the process of packaging WhisperLite into distributable formats for Windows, macOS, and Linux. WhisperLite uses Tauri's built-in packaging capabilities, which simplifies the process significantly.

## 1. Overview of Tauri Packaging

Tauri leverages platform-specific tools to create native installers and bundles. The `cargo tauri build` command handles most of the complexity, but understanding the underlying mechanisms can be helpful for troubleshooting or customization.

-   **Windows**: Generates `.msi` installers using WiX Toolset.
-   **macOS**: Generates `.app` bundles and `.dmg` disk images.
-   **Linux**: Generates `.AppImage` (universal Linux binary) and can optionally generate `.deb` (Debian/Ubuntu) or `.rpm` (Fedora/RHEL) packages.

## 2. Prerequisites for Packaging

In addition to the general build prerequisites (Rust, Python, Node.js), specific tools are required for each target platform:

-   **Windows**:
    -   [WiX Toolset](https://wixtoolset.org/): Required for `.msi` generation. Install `wix311.exe` or newer.
    -   Microsoft Visual Studio with Desktop development with C++ workload.
-   **macOS**:
    -   Xcode Command Line Tools (`xcode-select --install`).
    -   Apple Developer ID and signing certificates for notarization (recommended for distribution).
-   **Linux**:
    -   `appimage-builder` (for `.AppImage`): `pip install appimage-builder`
    -   `dpkg` (for `.deb`): Usually pre-installed on Debian/Ubuntu.
    -   `rpm` (for `.rpm`): Usually pre-installed on Fedora/RHEL.
    -   `libwebkit2gtk-4.0-dev` and other GTK development libraries (as listed in `BUILD_INSTALL.md`).

## 3. Packaging Process

The primary command for packaging is `cargo tauri build`. This command will compile the Rust binary, bundle the Python scripts, and package the web assets into a single distributable.

### 3.1. General Steps

1.  **Ensure all Python dependencies are installed**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Ensure the Whisper model is downloaded**:
    ```bash
    mkdir -p models
    curl -L -o models/ggml-tiny.en.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.en.bin
    ```
3.  **Navigate to the `rust/` directory**:
    ```bash
    cd rust
    ```
4.  **Run the Tauri build command**:
    ```bash
    cargo tauri build
    ```
    This will build the application for your current operating system.

### 3.2. Platform-Specific Notes

#### Windows

-   **Output**: `.msi` installer in `rust/target/release/bundle/msi/`.
-   **Signing**: For signed installers, configure `tauri.conf.json` with your code signing certificate details.

#### macOS

-   **Output**: `.app` bundle in `rust/target/release/bundle/macos/` and `.dmg` disk image.
-   **Notarization**: Apple requires applications distributed outside the App Store to be notarized. This involves signing your app with a Developer ID certificate and submitting it to Apple for automated scanning. Configure notarization in `tauri.conf.json`.

#### Linux

-   **Output**: `.AppImage` in `rust/target/release/bundle/appimage/`.
-   **`.deb` / `.rpm`**: To build `.deb` or `.rpm` packages, you might need to specify them in `tauri.conf.json` under the `bundle` section.
    ```json
    "bundle": {
        "deb": {
            "depends": [
                "libwebkit2gtk-4.0-3",
                "libayatana-appindicator3-1",
                "libsoup-2.4-1",
                "libgtk-3-0"
            ]
        },
        "rpm": {
            "depends": [
                "webkit2gtk4.0",
                "libappindicator3",
                "libsoup",
                "gtk3"
            ]
        }
    }
    ```
    Ensure the `depends` list includes all runtime dependencies for your target distributions.
-   **Python Bundling**: Tauri's Python bundling is experimental. Ensure your `tauri.conf.json` correctly points to your Python entry point and includes necessary Python files.
    ```json
    "bundle": {
        "externalBin": [
            "../venv/bin/python3" // Example for Linux, adjust for other OS
        ],
        "resources": [
            "../src",
            "../models"
        ]
    }
    ```
    This configuration tells Tauri to include the Python interpreter and the `src` and `models` directories.

## 4. Automated Packaging with GitHub Actions

The `.github/workflows/release.yml` workflow automates the packaging process for all three operating systems whenever a new release tag is pushed to GitHub. This workflow handles:
-   Setting up Rust, Python, and Node.js environments.
-   Installing system dependencies for each OS.
-   Building the Tauri application for Windows, macOS, and Linux.
-   Uploading the generated installers/bundles as release assets.

This is the recommended way to generate official releases.

## 5. Troubleshooting Packaging Issues

-   **Missing Dependencies**: Ensure all platform-specific prerequisites are installed. Check the `cargo tauri build` output for specific error messages.
-   **Python Script Not Found**: Verify the `externalBin` and `resources` paths in `tauri.conf.json` are correct and relative to the `rust/` directory.
-   **Code Signing/Notarization Errors**: These are often platform-specific and require careful configuration of certificates and developer accounts. Refer to Tauri's official documentation for detailed guides on signing and notarization.
-   **Linux AppImage Issues**: Ensure `appimage-builder` is installed and that all runtime dependencies are correctly specified in `tauri.conf.json` if you're building `.deb` or `.rpm` packages.
-   **`whisper.cpp` binary**: Ensure that the `whisper.cpp` binary (usually named `main` or `whisper`) is accessible to the packaged application. Tauri's `resources` or `externalBin` might be needed to include it if it's not statically linked into the Rust binary or if the Python script directly calls it.