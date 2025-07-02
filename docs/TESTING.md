# WhisperLite Testing Guide

This document outlines the testing strategy for WhisperLite, covering unit tests for Python modules, integration tests for the CLI, and general guidelines for adding new tests.

## 1. Testing Philosophy

WhisperLite aims for a robust testing suite to ensure reliability, prevent regressions, and facilitate future development. Given its hybrid architecture, testing focuses on:
-   **Unit Tests**: Verifying the correctness of individual Python modules and functions in isolation.
-   **Integration Tests**: Ensuring that different components (e.g., CLI arguments, Python modules) work correctly together.
-   **End-to-End Tests**: (Future consideration) Validating the entire application flow, including the Rust-Python IPC and UI interactions.

## 2. Python Unit Tests

Python unit tests are located in the `tests/` directory and are written using the `pytest` framework.

### 2.1. Running Python Tests

To run all Python unit tests, navigate to the project root and execute:

```bash
pytest
```

To run tests for a specific module (e.g., `test_transcriber.py`):

```bash
pytest tests/test_transcriber.py
```

### 2.2. Test Structure

Each Python module in `src/` typically has a corresponding test file in `tests/` (e.g., `src/transcriber.py` is tested by `tests/test_transcriber.py`).

Tests often use `unittest.mock` or `pytest` fixtures to mock external dependencies (e.g., `subprocess` calls for `whisper.cpp`, `sounddevice` for audio capture) to ensure tests are fast and isolated.

### 2.3. Adding New Python Unit Tests

1.  Create a new file `tests/test_your_module.py` (if one doesn't exist) for the module you want to test.
2.  Import `pytest` and the module/functions you intend to test.
3.  Write test functions, typically prefixed with `test_`, using `assert` statements for assertions.
4.  Use `pytest` fixtures for setup/teardown or to provide test data.
5.  If mocking external calls (e.g., `subprocess.run`), use `mocker` fixture provided by `pytest-mock`.

**Example (`tests/test_transcriber.py` excerpt):**

```python
import pytest
import subprocess
from unittest.mock import MagicMock, patch
from transcriber import WhisperTranscriber

# Mock shutil.which to ensure 'main' or 'whisper' is found
@pytest.fixture(autouse=True)
def mock_shutil_which(mocker):
    mocker.patch('shutil.which', return_value='/usr/local/bin/main')

def test_transcriber_initialization(tmp_path):
    model_path = tmp_path / "test_model.bin"
    model_path.touch()
    transcriber = WhisperTranscriber(str(model_path))
    assert transcriber.model_path == str(model_path)
    assert transcriber.use_gpu == False

def test_transcribe_chunk_success(mocker, tmp_path):
    model_path = tmp_path / "test_model.bin"
    model_path.touch()
    transcriber = WhisperTranscriber(str(model_path))

    mock_process = MagicMock()
    mock_process.communicate.return_value = ("WEBVTT\n\n00:00:00.000 --> 00:00:03.000\nHello world.\n", "")
    mock_process.returncode = 0

    mocker.patch('subprocess.Popen', return_value=mock_process)

    chunk_path = tmp_path / "audio.wav"
    chunk_path.touch()

    segments = transcriber.transcribe_chunk(str(chunk_path))
    assert len(segments) == 1
    assert segments[0]["text"] == "Hello world."
    assert segments[0]["start"] == "00:00:00.000"
```

## 3. CLI Integration Tests

CLI integration tests are located in the `cli_tests/` directory and are shell scripts that execute the `main.py` in CLI mode and verify its output.

### 3.1. Running CLI Tests

To run the CLI integration tests, execute the shell script directly:

```bash
bash cli_tests/test_cli_transcribe.sh
```

### 3.2. Test Structure

These tests typically:
1.  Set up environment variables (e.g., `MOCK_TRANSCRIPTION_OUTPUT` for predictable output).
2.  Execute `python3 src/main.py` with various CLI arguments.
3.  Check the standard output and standard error for expected messages.
4.  Verify the creation and content of output files (e.g., `.txt`, `.json`, `.srt`).
5.  Clean up any generated files.

**Example (`cli_tests/test_cli_transcribe.sh` excerpt):**

```bash
#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Define colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# --- Test 1: Basic CLI transcription to TXT (mocked) ---
echo -e "${GREEN}Running Test 1: Basic CLI transcription to TXT (mocked)${NC}"

OUTPUT_FILE="test_output.txt"

MOCK_TRANSCRIPTION_OUTPUT="true" python3 src/main.py --input "./test_audio.wav" --output "$OUTPUT_FILE" --format "txt"

if [ -f "$OUTPUT_FILE" ]; then
    echo -e "${GREEN}Test 1 Passed: Output file created.${NC}"
    grep -q "This is a mock transcription. CLI mode is working." "$OUTPUT_FILE" && \
    echo -e "${GREEN}Test 1 Passed: Content is correct.${NC}" || \
    { echo -e "${RED}Test 1 Failed: Content is incorrect.${NC}"; exit 1; }
else
    echo -e "${RED}Test 1 Failed: Output file not created.${NC}"; exit 1;
fi

rm "$OUTPUT_FILE"

echo -e "${GREEN}All CLI tests passed!${NC}"
```

## 4. Rust Tests

Rust unit tests are located in `rust/tests/` and `rust/src/main.rs` (for `TranscriptBuffer` and `AppState` related logic). They are written using Rust's built-in testing framework.

### 4.1. Running Rust Tests

To run all Rust tests, navigate to the `rust/` directory and execute:

```bash
cargo test
```

### 4.2. Test Structure

Rust tests are typically defined within `#[test]` functions. They can be in the same file as the code they are testing (within a `#[cfg(test)]` module) or in separate test files in the `tests/` directory.

**Example (`rust/src/main.rs` excerpt):**

```rust
// ... (inside TranscriptBuffer impl)

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_transcript_buffer_push_and_get() {
        let buffer = TranscriptBuffer::new();
        buffer.push("Hello".to_string());
        buffer.push("world".to_string());
        assert_eq!(buffer.get_full_text(), "Hello world");
    }

    #[test]
    fn test_transcript_buffer_clear() {
        let buffer = TranscriptBuffer::new();
        buffer.push("Test".to_string());
        buffer.clear();
        assert_eq!(buffer.get_full_text(), "");
    }
}
```

## 5. General Testing Guidelines

-   **Test Coverage**: Aim for high test coverage, especially for core logic and critical paths.
-   **Readability**: Write clear, concise, and readable tests. Tests should be easy to understand and maintain.
-   **Isolation**: Tests should be isolated and not depend on the state of other tests.
-   **Edge Cases**: Consider and test edge cases (e.g., empty input, invalid paths, error conditions).
-   **Performance**: While not the primary goal of unit tests, be mindful of test execution time. Avoid unnecessary I/O or long-running operations in unit tests.