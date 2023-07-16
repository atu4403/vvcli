import sys
import json
import pytest
from pathlib import Path

SAMPLES_DIR = Path("tests/samples")


@pytest.fixture(scope="session")
def samples_dir():
    return SAMPLES_DIR


@pytest.fixture(scope="session")
def audio_query_sample():
    audio_query_str = (SAMPLES_DIR / "audio_query.json").read_text()
    return json.loads(audio_query_str)


@pytest.fixture
def argv():
    original_argv = sys.argv
    yield
    sys.argv = original_argv
