import typing as t
from copy import deepcopy
from unittest import TestCase

from typing_extensions import override

import NetUtils
from NetUtils import GamesPackage
from apmw.multiserver.gamespackage.cache import GamesPackageCache


class GamesPackageCacheTest(TestCase):
    cache: GamesPackageCache
    any_game: t.ClassVar[str] = "APQuest"
    example_games_package: GamesPackage = {
        "item_name_to_id": {"Item 1": 1},
        "item_name_groups": {"Everything": ["Item 1"]},
        "location_name_to_id": {"Location 1": 1},
        "location_name_groups": {"Everywhere": ["Location 1"]},
        "checksum": "1234",
    }

    @override
    def setUp(self) -> None:
        self.cache = GamesPackageCache()

    def test_get_static_is_same(self) -> None:
        """Tests that get_static returns the same objects twice"""
        reduced_games_package1, item_name_groups1, location_name_groups1 = self.cache.get_static(self.any_game)
        reduced_games_package2, item_name_groups2, location_name_groups2 = self.cache.get_static(self.any_game)
        self.assertIs(reduced_games_package1, reduced_games_package2)
        self.assertIs(item_name_groups1, item_name_groups2)
        self.assertIs(location_name_groups1, location_name_groups2)

    def test_get_static_data_format(self) -> None:
        """Tests that get_static returns data in the correct format"""
        reduced_games_package, item_name_groups, location_name_groups = self.cache.get_static(self.any_game)
        self.assertTrue(reduced_games_package["checksum"])
        self.assertTrue(reduced_games_package["item_name_to_id"])
        self.assertTrue(reduced_games_package["location_name_to_id"])
        self.assertNotIn("item_name_groups", reduced_games_package)
        self.assertNotIn("location_name_groups", reduced_games_package)
        self.assertTrue(item_name_groups["Everything"])
        self.assertTrue(location_name_groups["Everywhere"])

    def test_get_static_is_serializable(self) -> None:
        """Tests that get_static returns data that can be serialized"""
        NetUtils.encode(self.cache.get_static(self.any_game))

    def test_get_static_missing_raises(self) -> None:
        """Tests that get_static raises KeyError if the world is missing"""
        with self.assertRaises(KeyError):
            _ = self.cache.get_static("Does not exist")

    def test_eviction(self) -> None:
        """Tests that unused items get evicted from cache"""
        game_name = "Test"
        before_add = len(self.cache._reduced_games_packages)
        data = self.cache.get(game_name, self.example_games_package)
        self.assertTrue(data)
        self.assertEqual(before_add + 1, len(self.cache._reduced_games_packages))

        del data
        if len(self.cache._reduced_games_packages) != before_add:  # gc.collect() may not even be required
            import gc

            gc.collect()

        self.assertEqual(before_add, len(self.cache._reduced_games_packages))

    def test_get_required_field(self) -> None:
        """Tests that missing required field raises a KeyError"""
        for field in ("item_name_to_id", "location_name_to_id", "item_name_groups"):
            with self.subTest(field=field):
                games_package = deepcopy(self.example_games_package)
                del games_package[field]  # type: ignore
                with self.assertRaises(KeyError):
                    _ = self.cache.get(self.any_game, games_package)

    def test_get_optional_properties(self) -> None:
        """Tests that missing optional field works"""
        for field in ("checksum", "location_name_groups"):
            with self.subTest(field=field):
                games_package = deepcopy(self.example_games_package)
                del games_package[field]  # type: ignore
                _, item_name_groups, location_name_groups = self.cache.get(self.any_game, games_package)
                self.assertTrue(item_name_groups)
                self.assertEqual(field != "location_name_groups", bool(location_name_groups))

    def test_item_name_deduplication(self) -> None:
        n = 1
        s1 = f"Item {n}"
        s2 = f"Item {n}"
        # check if the deduplication is actually gonna do anything
        self.assertIsNot(s1, s2)
        self.assertEqual(s1, s2)
        # do the thing
        game_name = "Test"
        games_package: GamesPackage = {
            "item_name_to_id": {s1: n},
            "item_name_groups": {"Everything": [s2]},
            "location_name_to_id": {},
            "location_name_groups": {},
            "checksum": "1234",
        }
        reduced_games_package, item_name_groups, location_name_groups = self.cache.get(game_name, games_package)
        self.assertIs(
            next(iter(reduced_games_package["item_name_to_id"].keys())),
            item_name_groups["Everything"][0],
        )

    def test_location_name_deduplication(self) -> None:
        n = 1
        s1 = f"Location {n}"
        s2 = f"Location {n}"
        # check if the deduplication is actually gonna do anything
        self.assertIsNot(s1, s2)
        self.assertEqual(s1, s2)
        # do the thing
        game_name = "Test"
        games_package: GamesPackage = {
            "item_name_to_id": {},
            "item_name_groups": {},
            "location_name_to_id": {s1: n},
            "location_name_groups": {"Everywhere": [s2]},
            "checksum": "1234",
        }
        reduced_games_package, item_name_groups, location_name_groups = self.cache.get(game_name, games_package)
        self.assertIs(
            next(iter(reduced_games_package["location_name_to_id"].keys())),
            location_name_groups["Everywhere"][0],
        )
