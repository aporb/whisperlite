# Milestone 3 Plan: Expand Functionality

This document outlines the detailed plan for Milestone 3, focusing on expanding WhisperLite's functionality to support multiple output formats and a command-line interface (CLI) or headless mode.

## 1. Objective

Milestone 3 aims to enhance WhisperLite's utility by providing users with more flexible output options (JSON, SRT) and enabling non-GUI usage through a robust CLI/headless mode, catering to advanced users and integration scenarios.

## 2. Prerequisites

-   **Completed Milestone 2**: All tasks from Milestone 2 (smooth text rendering, model selection, automated builds) must be finalized and stable.
-   **Whisper.cpp Model**: A `ggml` compatible Whisper model (`.bin` file) is required for transcription functionality.
-   **Python Dependencies**: Ensure all Python dependencies listed in `requirements.txt` are installed.
-   **Rust Environment**: A functional Rust development environment is necessary for building the Tauri application.

## 3. Task 1: JSON and SRT Output Support

**Objective**: Allow users to save transcripts in industry-standard JSON and SubRip (SRT) formats, in addition to the existing plain text.

-   **Source Files Impacted**:
    -   `src/output_writer.py`: Will be modified to include logic for formatting and writing JSON and SRT files.
    -   `ui/script.js`: (Optional) If a UI toggle for output format is desired, this file will need updates to pass the selected format to the Rust backend.
    -   `rust/src/main.rs`: (Optional) If a UI toggle is implemented, the `save_transcript` Tauri command might need an additional argument for the output format.

-   **Output Formatting Specs**:
    -   **JSON**: A structured JSON array of objects, where each object represents a segment of the transcript with `start_time`, `end_time`, and `text` fields.
        ```json
        [
            {
                "start_time": "00:00:00,000",
                "end_time": "00:00:03,500",
                "text": "Hello, this is a test."
            },
            {
                "start_time": "00:00:04,100",
                "end_time": "00:00:07,800",
                "text": "Welcome to WhisperLite."
            }
        ]
        ```
    -   **SRT**: Standard SubRip format, commonly used for subtitles.
        ```srt
        1
        00:00:00,000 --> 00:00:03,500
        Hello, this is a test.

        2
        00:00:04,100 --> 00:00:07,800
        Welcome to WhisperLite.
        ```

-   **Example Transcripts**: (See above for format examples)

-   **Optional Toggles (Design Decision)**:
    -   **CLI Flag**: A new command-line argument for `src/main.py` (e.g., `--format json` or `--format srt`) to specify the output format when running in headless mode.
    -   **UI Option**: A dropdown or radio button group in the UI to select the desired output format before saving. This would require changes in `ui/index.html` and `ui/script.js`, and passing the selection through the Tauri command to Rust, and then to Python.
    -   **Recommendation**: Implement CLI flag first for headless mode, then consider UI integration as a separate enhancement if time permits or user demand arises.

## 4. Task 2: CLI/Headless Mode

**Objective**: Enable WhisperLite to run without a graphical user interface, allowing for scripting, automation, and integration into other workflows.

-   **Python Entrypoint Layout (`src/main.py`)**:
    -   The existing `main()` function will be refactored to accept arguments for input audio (file or stream), output format, and model path.
    -   A new `cli_main()` function or similar will be introduced to handle argument parsing and orchestrate the transcription process for CLI usage.
    -   The `if __name__ == "__main__":` block will be updated to dispatch to either the GUI-driven logic (when launched by Tauri) or the `cli_main()` based on arguments.

-   **Arguments Required**:
    -   `--input <path_to_audio_file>`: Path to an audio file (WAV, MP3, etc.) for transcription. (Initial focus on WAV).
    -   `--output <path_to_output_file>`: Path where the transcript should be saved. (Defaults to Downloads if not specified).
    -   `--format <json|srt|txt>`: Output format (defaults to `txt`).
    -   `--model <path_to_model>`: Path to the Whisper model (already implemented).
    -   `--language <lang_code>`: (Optional) Specify transcription language.

-   **Expected Behavior**:
    -   **Input**: Reads audio from a specified file. Future: support real-time audio from CLI.
    -   **Output**: Writes the transcribed text in the specified format to the output file or `stdout` if no output file is given.
    -   **Exit Code**: `0` on success, non-zero on failure (e.g., file not found, transcription error).

-   **Testing Strategy (CI Hooks?)**:
    -   **Unit Tests**: Add new unit tests in `tests/test_main.py` to cover argument parsing and the core CLI transcription flow.
    -   **Integration Tests**: Create a new integration test in `rust/tests/` (or a dedicated `cli_tests/` directory) that invokes the Python CLI with various arguments and verifies the output.
    -   **CI Hooks**: Integrate CLI tests into the GitHub Actions workflow (`release.yml` or a new `ci.yml`) to ensure continuous validation.

## 5. Timeline and Milestone Gating Criteria

-   **Estimated Duration**: 3-4 weeks

-   **Gating Criteria for Completion**:
    -   JSON and SRT output formats are fully implemented in `output_writer.py` with corresponding unit tests.
    -   The CLI/headless mode is functional, accepting all specified arguments, and produces correct output for audio file inputs. ✅
    -   Comprehensive unit and integration tests for the CLI are implemented and passing.
    -   All new code adheres to project style guides and passes linting checks.
    -   Documentation (`README.md`, `BUILD_INSTALL.md`, `ARCHITECTURE.md`, `PLAN_20250701.md`) is updated to reflect new features.

## 6. Risks or Design Decisions to Address

-   **Python Process Management (CLI)**: When running in CLI mode, the Python process will be directly invoked, not spawned by Rust. This simplifies the Rust side but requires `src/main.py` to be self-contained for CLI execution.
-   **Real-time CLI Audio**: Initial CLI will focus on file-based input. Real-time audio input for CLI (e.g., piping audio) is a more complex feature that might be deferred to a future milestone.
-   **Error Reporting**: Ensure consistent and clear error reporting for both new output formats and CLI mode.
-   **Dependency Management**: Verify that adding new libraries for JSON/SRT handling (if any) does not introduce significant bloat or compatibility issues.
-   **UI Integration of Output Formats**: Decide whether to add UI controls for output format selection in this milestone or defer it. Deferring simplifies this milestone but might be a desired user feature.
