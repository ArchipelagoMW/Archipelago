import unittest
from unittest.mock import patch

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING
from Utils import parse_yaml

if TYPE_CHECKING:
    from worlds.AutoWorld import World


class TestGenerateYamlTemplates(unittest.TestCase):
    def test_name_with_colon(self) -> None:
        from Options import generate_yaml_templates
        from worlds.AutoWorld import AutoWorldRegister, World, WebWorld

        class WebWorldWithColon(WebWorld):
            options_presets = {
                "Generic": {
                    "progression_balancing": "disabled",
                    "accessibility": "minimal",
                }
            }

        class WorldWithColon(World):
            game = "World: with colon"
            item_name_to_id = {}
            location_name_to_id = {}
            hidden = True  # test-only world
            web = WebWorldWithColon()

        test_worlds = {WorldWithColon.game: WorldWithColon}
        with patch.object(AutoWorldRegister, "world_types", test_worlds):
            with TemporaryDirectory(f"archipelago_{__name__}") as temp_dir:
                generate_yaml_templates(temp_dir)
                path: Path
                for path in Path(temp_dir).rglob("*"):
                    if path.is_file():
                        self.assertTrue(path.suffix == ".yaml")
                        with path.open(encoding="utf-8") as f:
                            try:
                                data = parse_yaml(f)
                            except Exception:
                                f.seek(0)
                                print(f"Error in {path.name}:\n{f.read()}")
                                raise
                            self.assertIn("game", data)
                            self.assertIn(":", data["game"])
                            self.assertIn(data["game"], data)
                            self.assertIsInstance(data[data["game"]], dict)
