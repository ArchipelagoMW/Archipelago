"""Check world sources' manifest files"""

import json
import unittest
from pathlib import Path
from typing import Any, ClassVar

import test
from Utils import home_path, local_path
from worlds.AutoWorld import AutoWorldRegister
from ..param import classvar_matrix


test_path = Path(test.__file__).parent
worlds_paths = [
    Path(local_path("worlds")),
    Path(local_path("custom_worlds")),
    Path(home_path("worlds")),
    Path(home_path("custom_worlds")),
]

# Only check source folders for now. Zip validation should probably be in the loader and/or installer.
source_world_names = [
    k
    for k, v in AutoWorldRegister.world_types.items()
    if not v.zip_path and not Path(v.__file__).is_relative_to(test_path)
]


def get_source_world_manifest_path(game: str) -> Path | None:
    """Get path of archipelago.json in the world's root folder from game name."""
    # TODO: add a feature to AutoWorld that makes this less annoying
    world_type = AutoWorldRegister.world_types[game]
    world_type_path = Path(world_type.__file__)
    for worlds_path in worlds_paths:
        if world_type_path.is_relative_to(worlds_path):
            world_root = worlds_path / world_type_path.relative_to(worlds_path).parents[0]
            manifest_path = world_root / "archipelago.json"
            return manifest_path if manifest_path.exists() else None
    assert False, f"{world_type_path} not found in any worlds path"


# TODO: remove the filter once manifests are mandatory.
@classvar_matrix(game=filter(get_source_world_manifest_path, source_world_names))
class TestWorldManifest(unittest.TestCase):
    game: ClassVar[str]
    manifest: ClassVar[dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        world_type = AutoWorldRegister.world_types[cls.game]
        assert world_type.game == cls.game
        manifest_path = get_source_world_manifest_path(cls.game)
        assert manifest_path  # make mypy happy
        with manifest_path.open("r", encoding="utf-8") as f:
            cls.manifest = json.load(f)

    def test_game(self) -> None:
        """Test that 'game' will be correctly defined when generating APWorld manifest from source."""
        self.assertIn(
            "game",
            self.manifest,
            f"archipelago.json manifest exists for {self.game} but does not contain 'game'",
        )
        self.assertEqual(
            self.manifest["game"],
            self.game,
            f"archipelago.json manifest for {self.game} specifies wrong game '{self.manifest['game']}'",
        )

    def test_world_version(self) -> None:
        """Test that world_version matches the requirements in apworld specification.md""" 
        if "world_version" in self.manifest:
            world_version: str = self.manifest["world_version"]
            self.assertIsInstance(
                world_version,
                str,
                f"world_version in archipelago.json for '{self.game}' has to be string if provided.",
            )
            parts = world_version.split(".")
            self.assertEqual(
                len(parts),
                3,
                f"world_version in archipelago.json for '{self.game}' has to be in the form of 'major.minor.build'.",
            )
            for part in parts:
                self.assertTrue(
                    part.isdigit(),
                    f"world_version in archipelago.json for '{self.game}' may only contain numbers.",
                )

    def test_no_container_version(self) -> None:
        self.assertNotIn(
            "version",
            self.manifest,
            f"archipelago.json for '{self.game}' must not define 'version', see apworld specification.md.",
        )
        self.assertNotIn(
            "compatible_version",
            self.manifest,
            f"archipelago.json for '{self.game}' must not define 'compatible_version', see apworld specification.md.",
        )
