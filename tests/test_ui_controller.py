import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from ui_controller import UIController


def test_request_stop_sets_event():
    ui = UIController()
    assert not ui.should_stop()
    ui.request_stop()
    assert ui.should_stop()
