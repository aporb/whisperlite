# Debugging Guide — WhisperLite

Debugging a hybrid application like WhisperLite, which combines Rust, Python, and Tauri, can present unique challenges. This guide aims to provide comprehensive tips and strategies to help contributors effectively diagnose and resolve issues across the different layers of the application.

## 1. General Debugging Principles

Before diving into language-specific tools, consider these general principles:

-   **Isolate the Problem**: Try to narrow down which component (Rust, Python, or UI) is causing the issue. This often involves commenting out sections of code or simplifying inputs.
-   **Logging**: Implement extensive logging at critical points in your code. Logs are invaluable for understanding the flow of execution and variable states, especially in multi-threaded or multi-process environments.
-   **Reproducibility**: Ensure you can consistently reproduce the bug. This is the first step towards fixing it.
-   **Version Control**: Use `git bisect` to find the commit that introduced a bug.

## 2. Rust Debugging

The Rust core handles audio capture, state management, and inter-process communication. Debugging Rust code typically involves:

-   **Tools**:
    -   `rust-gdb` / `rust-lldb`: Command-line debuggers for stepping through code, inspecting variables, and setting breakpoints. Install them via `rustup component add rust-src` and then `rustup component add llvm-tools-preview` (for `lldb`).
    -   VS Code with `rust-analyzer` and `CodeLLDB` extensions: Provides a powerful integrated debugging experience.
-   **Common Issues**:
    -   Compilation Errors: Rust's compiler is very strict. Pay close attention to error messages; they are often very descriptive and point to the exact problem.
    -   Runtime Panics: Unrecoverable errors that cause the program to crash. Use `RUST_BACKTRACE=1` environment variable to get a detailed stack trace.
-   **Tips**:
    -   `println!`: For quick checks, use `println!` macros to print variable values or execution flow markers.
    -   `dbg!`: A more powerful macro than `println!` that prints the value of an expression, along with its file, line, and column.
    -   Conditional Compilation: Use `#[cfg(debug_assertions)]` to include debug-only code.

## 3. Python Debugging

The Python engine is responsible for `whisper.cpp` integration and transcript processing. Debugging Python code:

-   **Tools**:
    -   `pdb`: Python's built-in command-line debugger. Insert `import pdb; pdb.set_trace()` at the point you want to start debugging.
    -   IDE Debuggers: Most IDEs (e.g., VS Code, PyCharm) offer excellent Python debugging capabilities, allowing you to set breakpoints, step through code, and inspect variables.
-   **Common Issues**:
    -   `ModuleNotFoundError`: Ensure your virtual environment is activated and all dependencies are installed (`pip install -r requirements.txt`).
    -   Runtime Exceptions: Use `try...except` blocks to gracefully handle errors and log detailed information.
-   **Tips**:
    -   `print()`: Simple `print()` statements are effective for quick inspections.
    -   Virtual Environments: Always work within a virtual environment to manage dependencies and avoid conflicts.

## 4. Tauri / Frontend Debugging

The Tauri frontend is a webview, so standard web development debugging tools apply:

-   **Tools**:
    -   Browser Developer Tools: When running in development mode (`cargo tauri dev`), you can usually right-click on the Tauri window and select "Inspect Element" (or similar) to open the browser's developer tools. This provides access to the Console, Elements, Network, and Sources tabs.
-   **Common Issues**:
    -   UI Not Updating: Check JavaScript console for errors, verify data flow from Rust to frontend.
    -   JavaScript Errors: Use the Console tab to see JavaScript errors and stack traces.
    -   Styling Issues: Use the Elements tab to inspect CSS and HTML structure.
-   **Tips**:
    -   `console.log()`: Use `console.log()` in your JavaScript to output messages and variable values to the developer console.
    -   Network Tab: Monitor API calls between the frontend and Rust backend.

## 5. Inter-process Communication (IPC) Debugging

Communication between Rust and Python is a critical integration point. Issues here can be tricky:

-   **Mechanism**: Rust spawns the Python process and communicates via `stdin` (Rust to Python) and `stdout` (Python to Rust).
-   **Tips**:
    -   **Redirect `stdout`/`stderr`**: Temporarily modify the Rust code to redirect the Python subprocess's `stdout` and `stderr` to files. This allows you to inspect what Python is actually outputting.
    -   **Add Timestamps to Logs**: When logging from both Rust and Python, include timestamps to help correlate events across processes.
    -   **Data Format Verification**: Ensure the data being sent (e.g., audio bytes, JSON segments) matches the expected format on both ends.
    -   **Process Monitoring**: Use system tools to check if the Python process is actually running, consuming CPU/memory, or if it has crashed silently.
        -   Linux: `ps aux | grep python`, `strace -p <pid>`
        -   macOS: `ps aux | grep python`, `dtrace`

## 6. Platform-Specific Debugging

-   **Linux**: `strace` can trace system calls and signals, useful for understanding process interactions and file access issues.
-   **macOS**: `dtrace` (similar to `strace`) provides powerful system-wide tracing capabilities.
-   **Windows**: Tools like Process Monitor can help trace file and registry access.

By systematically applying these debugging techniques, you can effectively troubleshoot issues within the WhisperLite application.