# Testing Strategy — WhisperLite

WhisperLite employs a multi-layered testing strategy to ensure reliability, correctness, and a smooth user experience. The strategy includes unit tests for individual components, integration tests for the end-to-end workflow, and manual tests for user interface and system-level interactions.

## 🧪 Test Coverage

Testing is focused on the most critical and complex parts of the application:

-   **Python Engine**: Core transcription logic, audio data handling, and output formatting.
-   **Rust Core**: State management, audio capture, and the Python bridge.
-   **Frontend**: UI-to-backend communication and state synchronization.

### 1. Unit Tests

Unit tests are designed to validate the functionality of individual modules in isolation.

-   **Location**: `tests/`
-   **Framework**: `pytest` for the Python engine.
-   **Execution**: `pytest tests/`

**Python Unit Test Examples (`tests/test_*.py`):**

-   `test_audio_capture.py`: Mocks the microphone input and verifies that the `AudioCapture` class correctly chunks and queues audio data.
-   `test_transcriber.py`: Uses a mock `whisper.cpp` model to ensure the `Transcriber` class correctly processes audio data and returns the expected text output.
-   `test_output_writer.py`: Verifies that the `OutputWriter` class generates correctly formatted filenames and writes the transcript to the specified directory.
-   `test_ui_controller.py`: Tests the logic for updating the UI state and handling user commands.

### 2. Integration Tests

Integration tests validate the entire workflow, from audio input to the final text output.

-   **Location**: `rust/tests/`
-   **Framework**: `cargo test` for the Rust core.
-   **Execution**: `cargo test --manifest-path rust/Cargo.toml`

**Rust Integration Test Example (`rust/tests/basic.rs`):**

-   **`test_end_to_end_transcription`**: This test simulates a full transcription session:
    1.  Starts the Rust application.
    2.  Spawns the Python subprocess.
    3.  Sends a pre-recorded audio file (e.g., `tests/fixtures/test_audio.wav`) to the Python process's `stdin`.
    4.  Polls the `get_transcript` command to retrieve the transcribed text.
    5.  Asserts that the returned transcript matches the expected output.
    6.  Invokes the `save_transcript` command and verifies that the output file is created with the correct content.

### 3. Manual Testing

Manual testing is essential for validating the user experience and system-level interactions that are difficult to automate.

-   **UI/UX**: Verifying the appearance and behavior of the floating overlay window, including:
    -   Dark theme and glassmorphism effects.
    -   Smooth animations for state transitions.
    -   Window dragging, resizing, and always-on-top behavior.
-   **System Integration**: Testing on different operating systems (Windows, macOS, Linux) to ensure:
    -   Correct microphone permissions handling.
    -   Proper installation and uninstallation.
    -   Compatibility with different hardware configurations.
-   **Edge Cases**: Manually testing for unexpected scenarios, such as:
    -   No microphone connected.
    -   No write permissions for the `Downloads` directory.
    -   Corrupted or missing `whisper.cpp` model file.

## ➕ How to Add a New Test

### Adding a Python Unit Test

1.  **Create a new test file**: If you are testing a new module (e.g., `src/new_module.py`), create a corresponding test file `tests/test_new_module.py`.
2.  **Write the test function**: Follow the `pytest` conventions. Use fixtures to set up any necessary objects or mock data.

    ```python
    # tests/test_new_module.py
    import pytest
    from src.new_module import MyClass

    @pytest.fixture
    def my_class_instance():
        """Returns an instance of MyClass for testing."""
        return MyClass()

    def test_my_function(my_class_instance):
        """Tests the my_function method."""
        # Given
        input_data = "test"

        # When
        result = my_class_instance.my_function(input_data)

        # Then
        assert result == "expected_output"
    ```

3.  **Run the tests**: `pytest tests/`

### Adding a Rust Integration Test

1.  **Create a new test file**: Add a new file in the `rust/tests/` directory (e.g., `rust/tests/new_feature_test.rs`).
2.  **Write the test function**: Use the `#[test]` attribute.

    ```rust
    // rust/tests/new_feature_test.rs
    use super::*;

    #[test]
    fn test_new_feature() {
        // Setup: Initialize the application state
        let app_state = setup_app_state();

        // Action: Call the command or function to be tested
        let result = my_new_feature(app_state);

        // Assertion: Verify the result
        assert!(result.is_ok());
    }
    ```

3.  **Run the tests**: `cargo test --manifest-path rust/Cargo.toml`
