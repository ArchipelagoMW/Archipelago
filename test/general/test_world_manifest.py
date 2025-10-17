"""Check world sources' manifest files"""

import json
import unittest
from pathlib import Path
from typing import ClassVar

from worlds.AutoWorld import AutoWorldRegister
from ..param import classvar_matrix


# Only check source folders for now. Zip validation should probably be in the loader and/or installer.
source_world_names = [k for k, v in AutoWorldRegister.world_types.items() if not v.zip_path]


def get_source_world_manifest_path(game: str) -> Path | None:
    world_type = AutoWorldRegister.world_types[game]
    manifest_path = Path(world_type.__file__).parent / "archipelago.json"
    if manifest_path.exists():
        return manifest_path
    return None


# TODO: remove the filter once manifests are mandatory.
@classvar_matrix(game=filter(get_source_world_manifest_path, source_world_names))
class TestWorldManifest(unittest.TestCase):
    game: ClassVar[str]

    def test_game(self) -> None:
        """Test that 'game' will be correctly defined when generating APWorld manifest from source."""
        world_type = AutoWorldRegister.world_types[self.game]
        manifest_path = get_source_world_manifest_path(self.game)
        assert manifest_path  # make mypy happy
        with manifest_path.open("r", encoding="utf-8") as f:
            manifest = json.load(f)
        self.assertIn(
            "game",
            manifest,
            f"archipelago.json manifest exists for {self.game} but does not contain 'game'",
        )
        self.assertEqual(
            manifest["game"],
            world_type.game,
            f"archipelago.json manifest for {self.game} specifies wrong game '{manifest['game']}'",
        )
