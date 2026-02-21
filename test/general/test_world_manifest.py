"""Check world sources' manifest files"""

import json
import unittest
import zipfile
from pathlib import Path
from typing import Any, ClassVar

import test
from worlds import AutoWorldRegister
from ..param import classvar_matrix

test_path = Path(test.__file__).resolve().parent


def _load_manifest_for_entry(entry: dict) -> dict[str, Any]:
    """Load archipelago.json for a cache entry (folder or zip). Raises if missing or invalid."""
    path = Path(entry["path"]).resolve()
    if entry.get("is_zip"):
        if not path.is_file():
            raise FileNotFoundError(f"Manifests are mandatory: {entry['game']!r} apworld missing at {path}")
        with zipfile.ZipFile(path, "r") as zf:
            manifest_path = None
            for info in zf.infolist():
                if info.filename.endswith("archipelago.json"):
                    manifest_path = info.filename
                    break
            if manifest_path is None:
                raise FileNotFoundError(
                    f"Manifests are mandatory: {entry['game']!r} has no archipelago.json inside {path}"
                )
            with zf.open(manifest_path, "r") as f:
                return json.load(f)
    # Source folder
    manifest_path = path / "archipelago.json" if not entry.get("manifest_path") else Path(entry["manifest_path"])
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Manifests are mandatory: {entry['game']!r} has no archipelago.json at {manifest_path}")
    with manifest_path.open("r", encoding="utf-8") as f:
        return json.load(f)


_entries = AutoWorldRegister.get_world_list(force_rebuild=True)
_entries_under_test = [
    e
    for e in _entries
    if not Path(e["path"]).resolve().is_relative_to(test_path)
]
# One test class per game; cache has at most one entry per game.
source_world_names = list(dict.fromkeys(e["game"] for e in _entries_under_test))


@classvar_matrix(game=source_world_names)
class TestWorldManifest(unittest.TestCase):
    game: ClassVar[str]
    manifest: ClassVar[dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        entry = AutoWorldRegister.get_world_entry(game_name=cls.game)
        assert entry is not None, f"Cache entry for {cls.game!r} not found"
        cls.manifest = _load_manifest_for_entry(entry)

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
