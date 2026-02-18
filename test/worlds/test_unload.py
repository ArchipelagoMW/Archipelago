"""Tests for world unload and get_entry_by_path."""

import os
import tempfile
import zipfile
import unittest
from unittest.mock import MagicMock, patch

import worlds
from worlds import world_list_cache


class TestGetEntryByPath(unittest.TestCase):
    """Tests for world_list_cache.get_entry_by_path."""

    def test_get_entry_by_path_missing_returns_none(self) -> None:
        result = world_list_cache.get_entry_by_path(os.path.join(tempfile.gettempdir(), "nonexistent_xyz"))
        self.assertIsNone(result)

    def test_get_entry_by_path_returns_entry_when_in_cache(self) -> None:
        entries = worlds.get_world_list()
        if not entries:
            self.skipTest("No worlds in cache")
        path = entries[0]["path"]
        result = world_list_cache.get_entry_by_path(path)
        self.assertIsNotNone(result)
        self.assertEqual(os.path.normpath(result["path"]), os.path.normpath(path))
        self.assertEqual(result.get("game"), entries[0].get("game"))


class TestUnloadWorld(unittest.TestCase):
    """Tests for worlds.unload_world and reload behavior."""

    def test_unload_world_removes_and_allows_reload(self) -> None:
        entries = worlds.get_world_list()
        if not entries:
            self.skipTest("No worlds in cache")
        game = entries[0]["game"]
        worlds.get_world_class(game)
        self.assertIsNotNone(worlds.get_loaded_world(game))

        worlds.unload_world(game)
        self.assertIsNone(worlds.get_loaded_world(game))

        worlds.get_world_class(game)
        self.assertIsNotNone(worlds.get_loaded_world(game))

    def test_unload_world_no_op_for_unknown_game(self) -> None:
        worlds.unload_world("NonExistentGameXYZ")
        # No raise; unknown game is simply not loaded


class TestInstallApworldUnloads(unittest.TestCase):
    """Test that _install_apworld calls unload_world when the world is already loaded."""

    def test_install_apworld_calls_unload_when_already_loaded(self) -> None:
        from worlds.LauncherComponents import _install_apworld

        with tempfile.TemporaryDirectory() as tmp:
            # Install *from* source.apworld *to* Fake.apworld so "already at location" check doesn't trigger
            source_zip = os.path.join(tmp, "source.apworld")
            with zipfile.ZipFile(source_zip, "w") as zf:
                zf.writestr("Fake/__init__.py", "# minimal")
            target_apworld = os.path.join(tmp, "Fake.apworld")

            fake_source = type("WorldSource", (), {
                "path": target_apworld,
                "resolved_path": target_apworld,
                "load": MagicMock(return_value=True),
            })()
            with (
                patch.object(worlds, "user_folder", tmp),
                patch.object(worlds, "world_sources", [fake_source]),
                patch.object(worlds, "get_entry_by_path", return_value={"game": "FakeGame", "path": target_apworld}),
                patch.object(worlds, "unload_world", MagicMock()) as mock_unload,
                patch.object(worlds, "add_world_to_cache", return_value=True),
                patch("worlds.LauncherComponents.open_filename", return_value=None),
            ):
                try:
                    _install_apworld(source_zip)
                except Exception:
                    pass
                mock_unload.assert_called_once_with("FakeGame")
