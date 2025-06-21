import importlib
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))


def test_transcriber_importable():
    assert importlib.import_module("transcriber")
