"""
transcriber.py — WhisperLite
Handles streaming transcription of .wav audio chunks using whisper.cpp subprocess.
- Cross-platform: Windows/macOS/Linux
- Handles error logging, GPU support, and multiple models
"""

import os
import subprocess
import shutil
import logging
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("Transcriber")

class WhisperTranscriber:
    """
    Encapsulates interaction with whisper.cpp for real-time transcription.
    """

    def __init__(self, model_path: str, use_gpu: bool = False, whisper_bin: Optional[str] = None, language: str = "en"):
        """
        Args:
            model_path: Path to .bin model file
            use_gpu: Attempt GPU acceleration if available
            whisper_bin: Path to whisper.cpp binary (optional; auto-detected if None)
            language: Language code to use (default: "en")
        """
        # Auto-detect binary if not provided
        self.whisper_bin = whisper_bin or shutil.which("main") or shutil.which("whisper")
        if not self.whisper_bin:
            error_msg = "whisper.cpp binary not found. Please ensure it is in your PATH or specify its location."
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        if not os.path.isfile(model_path):
            logger.error(f"Model file not found: {model_path}")
            raise FileNotFoundError(f"Model file not found: {model_path}")

        self.model_path = model_path
        self.use_gpu = use_gpu
        self.language = language

        logger.info(f"Initialized WhisperTranscriber with model {model_path}, GPU={use_gpu}")

    def transcribe_chunk(self, chunk_path: str, timeout: float = 10.0) -> str:
        """
        Transcribe a single .wav audio chunk file with whisper.cpp.
        Args:
            chunk_path: Path to audio .wav file.
            timeout: Timeout for the subprocess in seconds.

        Returns:
            Transcript string, or empty string on error.
        """
        if not os.path.isfile(chunk_path):
            logger.error(f"Chunk not found: {chunk_path}")
            return ""

        # Build whisper.cpp command
        cmd = [
            self.whisper_bin,
            "-m", self.model_path,
            "-f", chunk_path,
            "--language", self.language,
            "--output-txt",  # output plain text file (stdout will also be captured)
            "--print-colors", "false"
        ]
        if self.use_gpu:
            cmd.append("--gpu")
        # Add more flags if your build supports faster or partial inference

        logger.debug(f"Running: {' '.join(cmd)}")

        try:
            # Use subprocess to run whisper.cpp, capturing output
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1
            )

            transcript_lines = []
            err_lines = []

            # Stream output in real-time
            for line in process.stdout:
                clean = line.strip()
                if clean:
                    transcript_lines.append(clean)
                    logger.debug(f"Whisper output: {clean}")

            # Wait for process to finish
            try:
                process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                process.kill()
                logger.error("whisper.cpp process timed out.")
                return ""

            # Collect errors
            for err in process.stderr:
                err_clean = err.strip()
                if err_clean:
                    err_lines.append(err_clean)
                    logger.error(f"whisper.cpp stderr: {err_clean}")

            transcript = " ".join(transcript_lines).strip()
            if not transcript:
                logger.warning("No transcript returned for this chunk.")

            return transcript

        except Exception as ex:
            logger.exception(f"Failed to invoke whisper.cpp: {ex}")
            return ""

# Example usage/test
if __name__ == "__main__":
    # Update these paths as needed for your environment
    MODEL_PATH = "./models/ggml-tiny.en.bin"
    TEST_CHUNK = "./chunks/chunk_001.wav"
    transcriber = WhisperTranscriber(model_path=MODEL_PATH, use_gpu=False)

    result = transcriber.transcribe_chunk(TEST_CHUNK)
    print("--- TRANSCRIPT ---")
    print(result or "[No output]")
