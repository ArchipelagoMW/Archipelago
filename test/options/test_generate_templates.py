import unittest

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Dict, Type
from Utils import parse_yaml

if TYPE_CHECKING:
    from worlds.AutoWorld import World


class TestGenerateYamlTemplates(unittest.TestCase):
    old_world_types: Dict[str, Type["World"]]

    def setUp(self) -> None:
        import worlds.AutoWorld

        self.old_world_types = worlds.AutoWorld.AutoWorldRegister.world_types

    def tearDown(self) -> None:
        import worlds.AutoWorld

        worlds.AutoWorld.AutoWorldRegister.world_types = self.old_world_types

        if "World: with colon" in worlds.AutoWorld.AutoWorldRegister.world_types:
            del worlds.AutoWorld.AutoWorldRegister.world_types["World: with colon"]

    def test_name_with_colon(self) -> None:
        from Options import generate_yaml_templates
        from worlds.AutoWorld import AutoWorldRegister
        from worlds.AutoWorld import World

        class WorldWithColon(World):
            game = "World: with colon"
            item_name_to_id = {}
            location_name_to_id = {}

        AutoWorldRegister.world_types = {WorldWithColon.game: WorldWithColon}
        with TemporaryDirectory(f"archipelago_{__name__}") as temp_dir:
            generate_yaml_templates(temp_dir)
            path: Path
            for path in Path(temp_dir).iterdir():
                self.assertTrue(path.is_file())
                self.assertTrue(path.suffix == ".yaml")
                with path.open(encoding="utf-8") as f:
                    try:
                        data = parse_yaml(f)
                    except:
                        f.seek(0)
                        print(f"Error in {path.name}:\n{f.read()}")
                        raise
                    self.assertIn("game", data)
                    self.assertIn(":", data["game"])
                    self.assertIn(data["game"], data)
                    self.assertIsInstance(data[data["game"]], dict)
