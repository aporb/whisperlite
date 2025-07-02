import pytest
from unittest.mock import patch, MagicMock
from src.transcriber import WhisperTranscriber

@patch('shutil.which', return_value='path/to/whisper')
def test_transcriber_init_success(mock_which):
    with patch('os.path.isfile', return_value=True):
        transcriber = WhisperTranscriber(model_path='path/to/model.bin')
        assert transcriber.model_path == 'path/to/model.bin'

@patch('shutil.which', return_value=None)
def test_transcriber_init_whisper_not_found(mock_which):
    with pytest.raises(FileNotFoundError, match='whisper.cpp binary not found'):
        WhisperTranscriber(model_path='path/to/model.bin')

@patch('shutil.which', return_value='path/to/whisper')
def test_transcriber_init_model_not_found(mock_which):
    with patch('os.path.isfile', return_value=False):
        with pytest.raises(FileNotFoundError, match='Model file not found'):
            WhisperTranscriber(model_path='path/to/model.bin')