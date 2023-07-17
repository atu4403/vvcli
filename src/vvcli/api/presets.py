from typing import Dict, List, Optional
from .call import call_api


class Presets:
    def __init__(self):
        self.presets = self.get_presets()

    def get_presets(self) -> List[Dict[str, str]]:
        response = call_api("presets")
        return response.json()

    def add_preset(self, preset: Dict[str, str]) -> None:
        response = call_api("add_preset", data=preset, http_method="POST")
        if response.status_code == 200:
            self.presets = self.get_presets()

    def update_preset(self, preset: Dict[str, str]) -> None:
        response = call_api("update_preset", data=preset, http_method="PUT")
        if response.status_code == 200:
            self.presets = self.get_presets()

    def upsert_preset(self, preset: Dict[str, str]) -> None:
        if any(p["id"] == preset["id"] for p in self.presets):
            self.update_preset(preset)
        else:
            self.add_preset(preset)

    def delete_preset(self, preset_id: int) -> None:
        response = call_api(f"delete_preset/{preset_id}", http_method="DELETE")
        if response.status_code == 204:
            self.presets = self.get_presets()
