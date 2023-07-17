import sys
import json
import pytest
from pathlib import Path

SAMPLES_DIR = Path("tests/samples")
SITE_DIR = Path("site")


def _save_json(obj, filename):
    savepath = SAMPLES_DIR / filename
    savepath.write_text(json.dumps(obj, indent=2, ensure_ascii=False))


def _load_json(filename):
    path = SAMPLES_DIR / filename
    return json.loads(path.read_text())


@pytest.fixture(scope="session")
def save_json():
    return _save_json


@pytest.fixture(scope="session")
def samples_dir():
    return SAMPLES_DIR


@pytest.fixture(scope="session")
def audio_query_sample():
    return _load_json("audio_query.json")


@pytest.fixture(scope="session")
def presets_sample():
    return _load_json("presets.json")


@pytest.fixture(scope="session")
def speakers_sample():
    return _load_json("speakers.json")


@pytest.fixture(scope="session")
def speaker_info_sample():
    return _load_json("speaker_info.json")


@pytest.fixture(scope="session")
def site_dir():
    return SITE_DIR


@pytest.fixture(scope="session")
def resources_dir():
    return SITE_DIR / "resources"


@pytest.fixture
def argv():
    original_argv = sys.argv
    yield
    sys.argv = original_argv
