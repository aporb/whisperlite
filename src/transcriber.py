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
            "--output-vtt",  # output VTT file (stdout will also be captured)
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

            # Read all stdout and stderr
            stdout, stderr = process.communicate(timeout=timeout)

            if stderr:
                for line in stderr.splitlines():
                    logger.error(f"whisper.cpp stderr: {line.strip()}")

            if not stdout:
                logger.warning("No output from whisper.cpp for this chunk.")
                return []

            # Parse VTT output
            segments = []
            lines = stdout.splitlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if "-->" in line:
                    try:
                        time_str = line
                        text_line = lines[i + 1].strip()
                        
                        start_time_str, end_time_str = time_str.split(" --> ")
                        
                        segments.append({
                            "start": start_time_str,
                            "end": end_time_str,
                            "text": text_line
                        })
                        i += 1 # Skip text line
                    except IndexError:
                        logger.error(f"Malformed VTT output near: {line}")
                    except ValueError:
                        logger.error(f"Could not parse time string: {line}")
                i += 1
            
            if not segments:
                logger.warning("No segments parsed from VTT output.")

            return segments

        except subprocess.TimeoutExpired:
            process.kill()
            logger.error("whisper.cpp process timed out.")
            return []
        except Exception as ex:
            logger.exception(f"Failed to invoke whisper.cpp or parse output: {ex}")
            return []

# Example usage/test
if __name__ == "__main__":
    # Update these paths as needed for your environment
    MODEL_PATH = "./models/ggml-tiny.en.bin"
    TEST_CHUNK = "./chunks/chunk_001.wav"
    transcriber = WhisperTranscriber(model_path=MODEL_PATH, use_gpu=False)

    result = transcriber.transcribe_chunk(TEST_CHUNK)
    print("--- TRANSCRIPT ---")
    print(result or "[No output]")
