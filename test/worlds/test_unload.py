"""Tests for world unload and world-list entry lookup helpers."""

import os
import tempfile
import zipfile
import unittest
from unittest.mock import MagicMock, patch

from worlds import AutoWorldRegister


def _is_reloadable_game(game: str) -> bool:
    try:
        AutoWorldRegister.get_world_class(game)
        AutoWorldRegister.unload_world(game)
        AutoWorldRegister.get_world_class(game)
        return True
    except KeyError:
        return False


def _find_reloadable_game_entry() -> dict | None:
    for entry in AutoWorldRegister.get_world_list():
        game = entry.get("game")
        if not game:
            continue
        if _is_reloadable_game(game):
            return entry
    return None


class TestGetEntryByPath(unittest.TestCase):
    """Tests for AutoWorldRegister.get_world_entry(path=...)."""

    def test_get_entry_by_path_missing_returns_none(self) -> None:
        result = AutoWorldRegister.get_world_entry(path=os.path.join(tempfile.gettempdir(), "nonexistent_xyz"))
        self.assertIsNone(result)

    def test_get_entry_by_path_returns_entry_when_in_cache(self) -> None:
        entries = AutoWorldRegister.get_world_list()
        if not entries:
            self.skipTest("No worlds in cache")
        path = entries[0]["path"]
        result = AutoWorldRegister.get_world_entry(path=path)
        self.assertIsNotNone(result)
        self.assertEqual(os.path.normpath(result["path"]), os.path.normpath(path))
        self.assertEqual(result.get("game"), entries[0].get("game"))


class TestGetEntryByGame(unittest.TestCase):
    """Tests for AutoWorldRegister.get_world_entry(game_name=...)."""

    def test_get_entry_by_game_missing_returns_none(self) -> None:
        result = AutoWorldRegister.get_world_entry(game_name="NonExistentGameXYZ")
        self.assertIsNone(result)

    def test_get_entry_by_game_returns_entry_when_in_cache(self) -> None:
        entries = AutoWorldRegister.get_world_list()
        if not entries:
            self.skipTest("No worlds in cache")
        game = entries[0].get("game")
        if not game:
            self.skipTest("First entry has no game name")
        result = AutoWorldRegister.get_world_entry(game_name=game)
        self.assertIsNotNone(result)
        self.assertEqual(result.get("game"), game)
        self.assertEqual(os.path.normpath(result["path"]), os.path.normpath(entries[0]["path"]))


class TestUnloadWorld(unittest.TestCase):
    """Tests for AutoWorldRegister.unload_world and reload behavior."""

    def test_unload_world_removes_and_allows_reload(self) -> None:
        entry = _find_reloadable_game_entry()
        if entry is None:
            self.skipTest("No reloadable world in cache")
        game = entry["game"]
        AutoWorldRegister.get_world_class(game)
        self.assertIsNotNone(AutoWorldRegister.get_loaded_world(game))

        AutoWorldRegister.unload_world(game)
        self.assertIsNone(AutoWorldRegister.get_loaded_world(game))

        AutoWorldRegister.get_world_class(game)
        self.assertIsNotNone(AutoWorldRegister.get_loaded_world(game))

    def test_unload_world_no_op_for_unknown_game(self) -> None:
        AutoWorldRegister.unload_world("NonExistentGameXYZ")
        # No raise; unknown game is simply not loaded

    def test_unload_world_invalidates_settings_key_world_cache(self) -> None:
        entry = next(
            (
                candidate
                for candidate in AutoWorldRegister.get_world_list()
                if candidate.get("game")
                and candidate.get("settings_key")
                and _is_reloadable_game(candidate["game"])
            ),
            None,
        )
        if entry is None:
            self.skipTest("No reloadable entry with both game and settings_key")

        game = entry["game"]
        settings_key = entry["settings_key"]
        first_world = AutoWorldRegister.get_world_class_for_settings_key(settings_key)
        self.assertIsNotNone(first_world)
        self.assertEqual(first_world.game, game)

        AutoWorldRegister.unload_world(game)
        self.assertIsNone(AutoWorldRegister.get_loaded_world(game))

        second_world = AutoWorldRegister.get_world_class_for_settings_key(settings_key)
        self.assertIsNotNone(second_world)
        self.assertEqual(second_world.game, game)
        self.assertIsNotNone(AutoWorldRegister.get_loaded_world(game))


class TestWorldQueryHelpers(unittest.TestCase):
    def test_get_worlds_loaded_only_does_not_trigger_load(self) -> None:
        entry = _find_reloadable_game_entry()
        if entry is None:
            self.skipTest("No reloadable world in cache")

        game = entry["game"]
        AutoWorldRegister.unload_world(game)
        self.assertIsNone(AutoWorldRegister.get_loaded_world(game))

        loaded_only_worlds = AutoWorldRegister.get_worlds(loaded_only=True)
        self.assertNotIn(game, loaded_only_worlds)
        self.assertIsNone(AutoWorldRegister.get_loaded_world(game))

    def test_get_worlds_loads_cache_known_worlds(self) -> None:
        entry = _find_reloadable_game_entry()
        if entry is None:
            self.skipTest("No reloadable world in cache")

        game = entry["game"]
        AutoWorldRegister.unload_world(game)
        self.assertIsNone(AutoWorldRegister.get_loaded_world(game))

        worlds = AutoWorldRegister.get_worlds()
        self.assertIn(game, worlds)
        self.assertIsNotNone(AutoWorldRegister.get_loaded_world(game))


class TestInstallApworldUnloads(unittest.TestCase):
    """Test that _install_apworld calls unload_world when the world is already loaded."""

    def test_install_apworld_calls_unload_when_already_loaded(self) -> None:
        from worlds.LauncherComponents import _install_apworld

        with tempfile.TemporaryDirectory() as tmp:
            # Install *from* source.apworld *to* Fake.apworld so "already at location" check doesn't trigger
            source_zip = os.path.join(tmp, "Fake_source.apworld")
            with zipfile.ZipFile(source_zip, "w") as zf:
                zf.writestr("Fake/__init__.py", "# minimal")
            target_apworld = os.path.join(tmp, "Fake.apworld")
            with open(target_apworld, "wb"):
                pass

            fake_source = type("WorldSource", (), {
                "path": target_apworld,
                "resolved_path": target_apworld,
                "load": MagicMock(return_value=True),
            })()
            with (
                patch("worlds.user_folder", tmp),
                patch.object(AutoWorldRegister, "get_world_sources", return_value=[fake_source]),
                patch.object(AutoWorldRegister, "get_world_entry",
                             return_value={"game": "FakeGame", "path": target_apworld}),
                patch.object(AutoWorldRegister, "unload_world", MagicMock()) as mock_unload,
                patch.object(AutoWorldRegister, "add_world_to_cache", return_value=True),
                patch("worlds.LauncherComponents.open_filename", return_value=None),
            ):
                try:
                    _install_apworld(source_zip)
                except Exception:
                    pass
                mock_unload.assert_called_once_with("FakeGame")
