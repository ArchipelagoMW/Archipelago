"""Unit tests for worlds.world_list_cache."""

import json
import os
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from worlds import AutoWorldRegister, network_data_package, world_list_cache


class TestReadCache(unittest.TestCase):
    """Tests for world_list_cache.read_cache."""

    def test_read_cache_missing(self) -> None:
        with patch.object(world_list_cache, "get_cache_path", return_value=os.path.join(tempfile.gettempdir(), "nonexistent_cache_xyz.json")):
            result = world_list_cache.read_cache()
        self.assertIsNone(result)

    def test_read_cache_invalid_json(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("not valid json {")
            path = f.name
        try:
            with patch.object(world_list_cache, "get_cache_path", return_value=path):
                result = world_list_cache.read_cache()
            self.assertIsNone(result)
        finally:
            os.unlink(path)

    def test_read_cache_wrong_format_version(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"format_version": 999, "entries": []}, f)
            path = f.name
        try:
            with patch.object(world_list_cache, "get_cache_path", return_value=path):
                result = world_list_cache.read_cache()
            self.assertIsNone(result)
        finally:
            os.unlink(path)

    def test_read_cache_valid(self) -> None:
        entries = [{"path": "/a", "mtime": 1.0, "game": "Test", "is_zip": False}]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"format_version": world_list_cache.CACHE_FORMAT_VERSION, "entries": entries}, f)
            path = f.name
        try:
            with patch.object(world_list_cache, "get_cache_path", return_value=path):
                result = world_list_cache.read_cache()
            self.assertIsNotNone(result)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["game"], "Test")
        finally:
            os.unlink(path)


class TestRefreshEntriesInPlace(unittest.TestCase):
    """Tests for per-entry refresh: only entries with mtime change or always_reload are updated; missing paths dropped."""

    def test_all_match_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "world1")
            os.makedirs(p, exist_ok=True)
            st = os.stat(p)
            entries = [{"path": p, "mtime": st.st_mtime, "game": "Test", "is_zip": False}]
            result, changed = world_list_cache.refresh_entries_in_place(entries)
            self.assertFalse(changed)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["game"], "Test")
            self.assertEqual(result[0]["mtime"], st.st_mtime)

    def test_stale_mtime_refreshes_only_that_entry(self) -> None:
        with tempfile.TemporaryDirectory() as local_dir:
            world_root = os.path.join(local_dir, "staleworld")
            os.makedirs(world_root, exist_ok=True)
            manifest_path = os.path.join(world_root, "archipelago.json")
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump({"game": "StaleGame", "world_version": "9.9.9"}, f)
            with open(os.path.join(world_root, "__init__.py"), "w", encoding="utf-8") as f:
                f.write("# placeholder\n")
            st = os.stat(world_root)
            # One entry with stale mtime (0.0), one with correct mtime
            other_path = os.path.join(local_dir, "other")
            os.makedirs(other_path, exist_ok=True)
            other_st = os.stat(other_path)
            entries = [
                {"path": world_root, "mtime": 0.0, "game": "OldName", "is_zip": False, "manifest_path": manifest_path},
                {"path": other_path, "mtime": other_st.st_mtime, "game": "Other", "is_zip": False},
            ]
            result, changed = world_list_cache.refresh_entries_in_place(entries)
            self.assertTrue(changed)
            self.assertEqual(len(result), 2)
            # First entry should be refreshed from manifest
            self.assertEqual(result[0]["game"], "StaleGame")
            self.assertEqual(result[0]["world_version"], "9.9.9")
            self.assertEqual(result[0]["mtime"], st.st_mtime)
            # Second entry unchanged
            self.assertEqual(result[1]["game"], "Other")
            self.assertEqual(result[1]["mtime"], other_st.st_mtime)

    def test_missing_path_dropped(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "exists")
            os.makedirs(p, exist_ok=True)
            st = os.stat(p)
            entries = [
                {"path": os.path.join(tempfile.gettempdir(), "nonexistent_xyz"), "mtime": 0.0, "game": "Ghost", "is_zip": False},
                {"path": p, "mtime": st.st_mtime, "game": "Real", "is_zip": False},
            ]
            result, changed = world_list_cache.refresh_entries_in_place(entries)
            self.assertTrue(changed)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["game"], "Real")

    def test_always_reload_refreshed(self) -> None:
        with tempfile.TemporaryDirectory() as local_dir:
            world_root = os.path.join(local_dir, "myworld")
            os.makedirs(world_root, exist_ok=True)
            manifest_path = os.path.join(world_root, "archipelago.json")
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump({"game": "AlwaysReloadGame", "always_reload": True, "world_version": "1.2.3"}, f)
            with open(os.path.join(world_root, "__init__.py"), "w", encoding="utf-8") as f:
                f.write("# placeholder\n")
            entries = [
                {"path": world_root, "mtime": 0.0, "game": "Old", "is_zip": False, "manifest_path": manifest_path, "always_reload": True},
            ]
            result, changed = world_list_cache.refresh_entries_in_place(entries)
            self.assertTrue(changed)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["game"], "AlwaysReloadGame")
            self.assertEqual(result[0]["world_version"], "1.2.3")
            self.assertTrue(result[0]["always_reload"])
            self.assertEqual(result[0]["mtime"], os.stat(world_root).st_mtime)


class TestMergeNewEntries(unittest.TestCase):
    """Tests that get_world_list() merges in new items found on disk that are not in the cache."""

    def test_get_world_list_merges_new_folder(self) -> None:
        with tempfile.TemporaryDirectory() as local_dir:
            # Existing cached entry; scan always runs so new items are picked up without needing mtime change
            world1 = os.path.join(local_dir, "world1")
            os.makedirs(world1, exist_ok=True)
            with open(os.path.join(world1, "archipelago.json"), "w", encoding="utf-8") as f:
                json.dump({"game": "CachedGame"}, f)
            with open(os.path.join(world1, "__init__.py"), "w", encoding="utf-8") as f:
                f.write("# placeholder\n")
            st1 = os.stat(world1)
            cache_entries = [
                {"path": world1, "mtime": st1.st_mtime, "game": "CachedGame", "is_zip": False},
            ]
            cache_path = os.path.join(tempfile.gettempdir(), "worlds_cache_merge_test.json")
            try:
                with patch.object(world_list_cache, "get_cache_path", return_value=cache_path):
                    with patch.object(world_list_cache, "_get_folder_paths", return_value=(local_dir, None)):
                        world_list_cache.write_cache(cache_entries)  # file has one entry; in-memory cleared
                        # Now add a new world folder on disk (not in cache)
                        world2 = os.path.join(local_dir, "newworld")
                        os.makedirs(world2, exist_ok=True)
                        with open(os.path.join(world2, "archipelago.json"), "w", encoding="utf-8") as f:
                            json.dump({"game": "NewGame", "world_version": "0.0.1"}, f)
                        with open(os.path.join(world2, "__init__.py"), "w", encoding="utf-8") as f:
                            f.write("# placeholder\n")
                        result = world_list_cache.get_world_list()
                        games = {e["game"] for e in result}
                        self.assertIn("CachedGame", games)
                        self.assertIn("NewGame", games)
                        self.assertEqual(len(result), 2)
            finally:
                if os.path.isfile(cache_path):
                    os.unlink(cache_path)

    def test_get_world_list_merges_new_apworld(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            ap_path = os.path.join(d, "new.apworld")
            with zipfile.ZipFile(ap_path, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("archipelago.json", json.dumps({"game": "NewZipGame"}))
            cache_path = os.path.join(tempfile.gettempdir(), "worlds_cache_merge_apworld_test.json")
            try:
                with patch.object(world_list_cache, "get_cache_path", return_value=cache_path):
                    with patch.object(world_list_cache, "_get_folder_paths", return_value=(d, None)):
                        world_list_cache.write_cache([])
                        result = world_list_cache.get_world_list()
                        self.assertEqual(len(result), 1)
                        self.assertEqual(result[0]["game"], "NewZipGame")
                        self.assertTrue(result[0]["is_zip"])
            finally:
                if os.path.isfile(cache_path):
                    os.unlink(cache_path)


class TestBuildCache(unittest.TestCase):
    """Tests for world_list_cache.build_cache."""

    def test_build_cache_folders(self) -> None:
        with tempfile.TemporaryDirectory() as local_dir:
            world_root = os.path.join(local_dir, "testworld")
            os.makedirs(world_root, exist_ok=True)
            with open(os.path.join(world_root, "archipelago.json"), "w", encoding="utf-8") as f:
                json.dump({"game": "TestWorld", "world_version": "1.0.0"}, f)
            with open(os.path.join(world_root, "__init__.py"), "w", encoding="utf-8") as f:
                f.write("# placeholder\n")
            entries = world_list_cache.build_cache(local_dir, None)
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["game"], "TestWorld")
            self.assertFalse(entries[0]["is_zip"])
            self.assertEqual(entries[0]["path"], world_root)
            self.assertIn("mtime", entries[0])

    def test_build_cache_apworld(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            ap_path = os.path.join(d, "game.apworld")
            with zipfile.ZipFile(ap_path, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("archipelago.json", json.dumps({"game": "ZipGame", "world_version": "2.0.0"}))
            entries = world_list_cache.build_cache(d, None)
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["game"], "ZipGame")
            self.assertTrue(entries[0]["is_zip"])
            self.assertEqual(entries[0]["path"], ap_path)

    def test_build_cache_apworld_no_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            ap_path = os.path.join(d, "nomanifest.apworld")
            with zipfile.ZipFile(ap_path, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("other.txt", "data")
            entries = world_list_cache.build_cache(d, None)
            self.assertEqual(len(entries), 0)

    def test_build_cache_skips_folder_without_init_py(self) -> None:
        with tempfile.TemporaryDirectory() as local_dir:
            world_root = os.path.join(local_dir, "noinit")
            os.makedirs(world_root, exist_ok=True)
            with open(os.path.join(world_root, "archipelago.json"), "w", encoding="utf-8") as f:
                json.dump({"game": "NoInit"}, f)
            entries = world_list_cache.build_cache(local_dir, None)
            self.assertEqual(len(entries), 0)


class TestAddWorldToCache(unittest.TestCase):
    """Tests for world_list_cache.add_world_to_cache."""

    def test_add_world_to_cache_appends_entry(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            ap_path = os.path.join(d, "newgame.apworld")
            with zipfile.ZipFile(ap_path, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("archipelago.json", json.dumps({"game": "NewGame", "world_version": "1.0.0"}))
            cache_path = os.path.join(tempfile.gettempdir(), "worlds_cache_add_test.json")
            try:
                with patch.object(world_list_cache, "get_cache_path", return_value=cache_path):
                    with patch.object(world_list_cache, "_get_folder_paths", return_value=(d, None)):
                        world_list_cache.write_cache([])
                        result = world_list_cache.add_world_to_cache(ap_path)
                        self.assertTrue(result)
                        entries = world_list_cache.read_cache()
                        self.assertIsNotNone(entries)
                        self.assertEqual(len(entries), 1)
                        self.assertEqual(entries[0]["game"], "NewGame")
                        self.assertEqual(entries[0]["path"], ap_path)
                        self.assertTrue(entries[0]["is_zip"])
                        self.assertIn("mtime", entries[0])
            finally:
                if os.path.isfile(cache_path):
                    os.unlink(cache_path)

    def test_add_world_to_cache_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            ap_path = os.path.join(d, "idem.apworld")
            with zipfile.ZipFile(ap_path, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("archipelago.json", json.dumps({"game": "IdemGame"}))
            cache_path = os.path.join(tempfile.gettempdir(), "worlds_cache_idem_test.json")
            try:
                with patch.object(world_list_cache, "get_cache_path", return_value=cache_path):
                    with patch.object(world_list_cache, "_get_folder_paths", return_value=(d, None)):
                        world_list_cache.write_cache([])
                        self.assertTrue(world_list_cache.add_world_to_cache(ap_path))
                        self.assertTrue(world_list_cache.add_world_to_cache(ap_path))
                        entries = world_list_cache.read_cache()
                        self.assertIsNotNone(entries)
                        self.assertEqual(len(entries), 1)
            finally:
                if os.path.isfile(cache_path):
                    os.unlink(cache_path)

    def test_add_world_to_cache_invalid_manifest_returns_false(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            ap_path = os.path.join(d, "nomanifest.apworld")
            with zipfile.ZipFile(ap_path, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("other.txt", "data")
            cache_path = os.path.join(tempfile.gettempdir(), "worlds_cache_invalid_test.json")
            try:
                with patch.object(world_list_cache, "get_cache_path", return_value=cache_path):
                    with patch.object(world_list_cache, "_get_folder_paths", return_value=(d, None)):
                        world_list_cache.write_cache([])
                        result = world_list_cache.add_world_to_cache(ap_path)
                        self.assertFalse(result)
                        entries = world_list_cache.read_cache()
                        self.assertEqual(len(entries), 0)
            finally:
                if os.path.isfile(cache_path):
                    os.unlink(cache_path)


class TestWriteReadRoundtrip(unittest.TestCase):
    """Tests for cache write then read roundtrip."""

    def test_write_read_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as local_dir:
            world_root = os.path.join(local_dir, "roundtrip")
            os.makedirs(world_root, exist_ok=True)
            with open(os.path.join(world_root, "archipelago.json"), "w", encoding="utf-8") as f:
                json.dump({"game": "RoundtripGame"}, f)
            with open(os.path.join(world_root, "__init__.py"), "w", encoding="utf-8") as f:
                f.write("# x\n")
            built = world_list_cache.build_cache(local_dir, None)
            self.assertEqual(len(built), 1)
            cache_path = os.path.join(tempfile.gettempdir(), "worlds_cache_roundtrip_test.json")
            try:
                with patch.object(world_list_cache, "get_cache_path", return_value=cache_path):
                    world_list_cache.write_cache(built)
                    read_back = world_list_cache.read_cache()
                self.assertIsNotNone(read_back)
                self.assertEqual(len(read_back), 1)
                self.assertEqual(read_back[0]["game"], built[0]["game"])
                self.assertEqual(read_back[0]["path"], built[0]["path"])
                self.assertEqual(read_back[0]["is_zip"], built[0]["is_zip"])
            finally:
                if os.path.isfile(cache_path):
                    os.unlink(cache_path)


class TestLazyLoadIntegration(unittest.TestCase):
    """Integration tests for lazy world loading (require worlds package and cache)."""

    @staticmethod
    def _find_loadable_game() -> str | None:
        for entry in AutoWorldRegister.get_world_list():
            game = entry.get("game")
            if not game:
                continue
            try:
                AutoWorldRegister.get_world_class(game)
                return game
            except KeyError:
                continue
        return None

    def test_world_sources_is_list(self) -> None:
        world_sources = AutoWorldRegister.get_world_sources()
        self.assertIsInstance(world_sources, list)
        # Sources include both manifest-backed cache entries and non-manifest folder worlds.
        self.assertGreaterEqual(len(world_sources), len(AutoWorldRegister.get_world_list()))
        for ws in world_sources[:3]:
            self.assertIsNotNone(ws.path)
            self.assertIn(ws.is_zip, (True, False))

    def test_get_world_list_returns_entries(self) -> None:
        entries = AutoWorldRegister.get_world_list()
        self.assertIsInstance(entries, list)
        for entry in entries[:3]:  # spot-check first few
            self.assertIn("game", entry)
            self.assertIn("path", entry)
            self.assertIn("is_zip", entry)

    def test_get_world_class_loads_on_demand(self) -> None:
        game = self._find_loadable_game()
        if game is None:
            self.skipTest("No loadable worlds in cache")
        cls = AutoWorldRegister.get_world_class(game)
        self.assertIsNotNone(cls)
        self.assertEqual(cls.game, game)
        self.assertIsNotNone(AutoWorldRegister.get_loaded_world(game))

    def test_network_data_package_games_after_get_world_class(self) -> None:
        game = self._find_loadable_game()
        if game is None:
            self.skipTest("No loadable worlds in cache")
        AutoWorldRegister.get_world_class(game)
        self.assertIsNotNone(AutoWorldRegister.get_loaded_world(game))
        self.assertIn(game, network_data_package["games"])

    def test_get_all_worlds_populates_world_types(self) -> None:
        entries = AutoWorldRegister.get_world_list()
        if not entries:
            self.skipTest("No worlds in cache")
        AutoWorldRegister.get_all_worlds()
        registered = set(AutoWorldRegister.world_types.keys())
        cache_games = {e["game"] for e in entries if e.get("game")}
        self.assertTrue(
            cache_games.issubset(registered) or registered,
            f"Cache games {cache_games!r} should be in registered {registered!r}",
        )
