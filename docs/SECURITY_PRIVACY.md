# Security and Privacy — WhisperLite

WhisperLite is engineered from the ground up with a strong commitment to user privacy and data security. Our guiding principle is simple: **your data is yours, and it never leaves your device.**

## 🛡️ Local-First Guarantee

-   **No Cloud Processing**: All transcription and data processing happens locally on your machine. Your audio is never sent to the cloud or any third-party servers.
-   **No Internet Required**: The application is fully functional without an internet connection. This ensures that your data remains private, even on untrusted networks.
-   **No Telemetry or Analytics**: WhisperLite does not collect any usage data, analytics, or telemetry. We have no way of knowing who you are or how you use the application.

## 🔒 Data Flow and Storage

To provide a transparent overview of how data is handled, here is a step-by-step breakdown of the data lifecycle within the application:

1.  **Audio Capture**: The Rust core captures audio from your microphone and holds it in memory.
2.  **In-Memory Transfer**: The audio data is sent directly to the Python subprocess via its `stdin`. It is never written to a temporary file on disk.
3.  **Transcription**: The Python engine processes the in-memory audio data and generates the transcript.
4.  **Transcript Buffer**: The transcribed text is stored in a secure, in-memory buffer within the Rust core.
5.  **Temporary Files**: The only time a file is written to disk is when you explicitly save the transcript. These files are stored in your `Downloads` directory, and you have full control over them.
6.  **Graceful Exit**: When you close the application, the in-memory audio and transcript buffers are immediately cleared. No data persists between sessions unless explicitly saved by the user.

## 🔐 Permissions Model

WhisperLite requests only the minimum permissions necessary for it to function:

-   **Microphone Access**: Required for audio capture. The application will explicitly ask for your permission the first time you run it. You can revoke this permission at any time through your operating system's settings.
-   **File System Access**: Only required when you choose to save a transcript. The application will use your system's native file save dialog, ensuring that it can only write to the location you specify.

## 📦 Software Supply Chain Security

We take the security of our development and build processes seriously:

-   **Dependency Auditing**: We use tools like `cargo-audit` and `pip-audit` to regularly scan our dependencies for known vulnerabilities.
-   **Reproducible Builds**: Our build process is designed to be as deterministic as possible, ensuring that the code you see in the repository is the same code that ends up in the final application.
-   **Signed Releases**: All official releases are cryptographically signed, allowing you to verify that the application has not been tampered with.

##  Summary

| Feature                  | Status                                        |
| ------------------------ | --------------------------------------------- |
| **Data Locality**        | ✅ 100% on-device processing                  |
| **Internet Requirement** | ✅ Fully offline                                |
| **Telemetry**            | ✅ No data collection of any kind             |
| **Permissions**          | ✅ Minimal and explicitly requested           |
| **Data Persistence**     | ✅ Only when user explicitly saves a file     |
| **Secure by Design**     | ✅ Sandboxed UI, isolated processes           |