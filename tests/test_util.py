import json
from pathlib import Path
from vvcli.util import split_text

SAMPLES_DIR = Path("tests/samples")


def test_split_text():
    before_text = (SAMPLES_DIR / "split_text_before.txt").read_text()
    json_path = SAMPLES_DIR / "split_text_after.json"
    result = split_text(before_text)
    expect_json = json.loads(json_path.read_text())
    assert result == expect_json
