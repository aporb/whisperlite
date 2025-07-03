use std::process::{Command, Stdio};
use std::io::{Write, BufReader, BufRead};
use std::time::Duration;
use std::thread;

#[test]
fn test_python_subprocess_communication() {
    // This test spawns the Python main.py in CLI mode and sends dummy data to its stdin.
    // It then reads from stdout to verify basic communication.

    let python_process = Command::new("python3")
        .arg("src/main.py")
        .arg("--save-transcript") // Use save-transcript mode for simpler input/output
        .arg("--format")
        .arg("txt")
        .arg("--output-dir")
        .arg("/tmp") // Use a temporary directory for output
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn();

    let mut child = match python_process {
        Ok(c) => c,
        Err(e) => {
            panic!("Failed to spawn Python process: {}", e);
        }
    };

    let mut stdin = child.stdin.take().expect("Failed to open stdin");
    let stdout = child.stdout.take().expect("Failed to open stdout");

    // Send dummy JSON segments to Python's stdin
    let dummy_segments = r#"[{"start": "00:00:00.000", "end": "00:00:01.000", "text": "hello"}]"#;
    if let Err(e) = stdin.write_all(dummy_segments.as_bytes()) {
        panic!("Failed to write to Python stdin: {}", e);
    }
    drop(stdin); // Close stdin to signal EOF to Python

    // Read output from Python's stdout
    let reader = BufReader::new(stdout);
    let mut output_lines = Vec::new();
    for line in reader.lines() {
        output_lines.push(line.expect("Failed to read line from stdout"));
    }

    // Wait for the Python process to exit
    let status = child.wait().expect("Failed to wait for Python process");

    assert!(status.success(), "Python process exited with error: {:?}", status);
    assert!(!output_lines.is_empty(), "Python process produced no output");
    // Further assertions can be added here to check the content of output_lines
    // For now, just check if it contains a path to a saved file.
    assert!(output_lines[0].contains("/tmp/testuser_"), "Output did not contain expected path: {}", output_lines[0]);
}
