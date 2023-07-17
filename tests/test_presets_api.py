import json
from pathlib import Path
from vvcli.api import Presets


class TestPresets:
    def test_01(self, save_json):
        p = Presets()
        save_json(p.presets, "presets.json")
