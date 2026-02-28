import typing as t
from copy import deepcopy

import Utils
import apmw.webhost.customserver.gamespackage.cache
from NetUtils import GamesPackage
from apmw.webhost.customserver.gamespackage.cache import DBGamesPackageCache
from test.multiserver.test_gamespackage_cache import GamesPackageCacheTest


class FakeGameDataPackage:
    _rows: "t.ClassVar[dict[str, FakeGameDataPackage]]" = {}
    data: bytes

    @classmethod
    def get(cls, checksum: str) -> "FakeGameDataPackage | None":
        return cls._rows.get(checksum, None)

    @classmethod
    def add(cls, checksum: str, full_games_package: GamesPackage) -> None:
        row = FakeGameDataPackage()
        row.data = Utils.restricted_dumps(full_games_package)
        cls._rows[checksum] = row


class DBGamesPackageCacheTest(GamesPackageCacheTest):
    cache: DBGamesPackageCache
    any_game: t.ClassVar[str] = "My Game"
    static_data: t.ClassVar[dict[str, GamesPackage]] = {  # noqa: pycharm doesn't understand this
        "My Game": {
            "item_name_to_id": {"Item 1": 1},
            "location_name_to_id": {"Location 1": 1},
            "item_name_groups": {"Everything": ["Item 1"]},
            "location_name_groups": {"Everywhere": ["Location 1"]},
            "checksum": "2345",
        }
    }
    orig_db_type: t.Any

    def setUp(self) -> None:
        self.orig_db_type = apmw.webhost.customserver.gamespackage.cache.GameDataPackage  # type: ignore[attr-defined]
        self.cache = DBGamesPackageCache(self.static_data)
        apmw.webhost.customserver.gamespackage.cache.GameDataPackage = FakeGameDataPackage  # type: ignore

    def tearDown(self) -> None:
        apmw.webhost.customserver.gamespackage.cache.GameDataPackage = self.orig_db_type  # type: ignore[attr-defined]

    def assert_conversion(
        self,
        full_games_package: GamesPackage,
        reduced_games_package: dict[str, t.Any],
        item_name_groups: dict[str, t.Any],
        location_name_groups: dict[str, t.Any],
    ) -> None:
        for key in ("item_name_to_id", "location_name_to_id", "checksum"):
            if key in full_games_package:
                self.assertEqual(reduced_games_package[key], full_games_package[key])  # noqa: pycharm
        self.assertEqual(item_name_groups, full_games_package["item_name_groups"])
        self.assertEqual(location_name_groups, full_games_package["location_name_groups"])

    def assert_static_conversion(
        self,
        full_games_package: GamesPackage,
        reduced_games_package: dict[str, t.Any],
        item_name_groups: dict[str, t.Any],
        location_name_groups: dict[str, t.Any],
    ) -> None:
        self.assert_conversion(full_games_package, reduced_games_package, item_name_groups, location_name_groups)
        for key in ("item_name_to_id", "location_name_to_id", "checksum"):
            self.assertIs(reduced_games_package[key], full_games_package[key])  # noqa: pycharm

    def test_get_static_contents(self) -> None:
        """Tests that get_static returns the correct data"""
        reduced_games_package, item_name_groups, location_name_groups = self.cache.get_static(self.any_game)
        for key in ("item_name_to_id", "location_name_to_id", "checksum"):
            self.assertIs(reduced_games_package[key], self.static_data[self.any_game][key])  # noqa: pycharm
        self.assertEqual(item_name_groups, self.static_data[self.any_game]["item_name_groups"])
        self.assertEqual(location_name_groups, self.static_data[self.any_game]["location_name_groups"])

    def test_static_not_evicted(self) -> None:
        """Tests that static data is not evicted from cache during gc"""
        import gc

        game_name = next(iter(self.static_data.keys()))
        ids = [id(o) for o in self.cache.get_static(game_name)]
        gc.collect()
        self.assertEqual(ids, [id(o) for o in self.cache.get_static(game_name)])

    def test_get_is_static(self) -> None:
        """Tests that a get with correct checksum return the static items"""
        # NOTE: this is only true for the DB cache, not the "regular" one, since we want to avoid loading worlds there
        cks: GamesPackage = {"checksum": self.static_data[self.any_game]["checksum"]}  # noqa: pycharm doesn't like this
        reduced_games_package1, item_name_groups1, location_name_groups1 = self.cache.get(self.any_game, cks)
        reduced_games_package2, item_name_groups2, location_name_groups2 = self.cache.get_static(self.any_game)
        self.assertIs(reduced_games_package1, reduced_games_package2)
        self.assertEqual(location_name_groups1, location_name_groups2)
        self.assertEqual(item_name_groups1, item_name_groups2)

    def test_get_from_db(self) -> None:
        """Tests that a get with only checksum will load the full data from db and is cached"""
        game_name = "Another Game"
        full_games_package = deepcopy(self.static_data[self.any_game])
        full_games_package["checksum"] = "3456"
        cks: GamesPackage = {"checksum": full_games_package["checksum"]}  # noqa: pycharm doesn't like this
        FakeGameDataPackage.add(full_games_package["checksum"], full_games_package)
        before_add = len(self.cache._reduced_games_packages)
        data = self.cache.get(game_name, cks)
        self.assert_conversion(full_games_package, *data)  # type: ignore
        self.assertEqual(before_add + 1, len(self.cache._reduced_games_packages))

    def test_get_missing_from_db_uses_full_games_package(self) -> None:
        """Tests that a get with full data (missing from db) will use the full data and is cached"""
        game_name = "Yet Another Game"
        full_games_package = deepcopy(self.static_data[self.any_game])
        full_games_package["checksum"] = "4567"
        before_add = len(self.cache._reduced_games_packages)
        data = self.cache.get(game_name, full_games_package)
        self.assert_conversion(full_games_package, *data)  # type: ignore
        self.assertEqual(before_add + 1, len(self.cache._reduced_games_packages))

    def test_get_without_checksum_uses_full_games_package(self) -> None:
        """Tests that a get with full data and no checksum will use the full data and is not cached"""
        game_name = "Yet Another Game"
        full_games_package = deepcopy(self.static_data[self.any_game])
        del full_games_package["checksum"]
        before_add = len(self.cache._reduced_games_packages)
        data = self.cache.get(game_name, full_games_package)
        self.assert_conversion(full_games_package, *data)  # type: ignore
        self.assertEqual(before_add, len(self.cache._reduced_games_packages))

    def test_get_missing_from_db_raises(self) -> None:
        """Tests that a get that requires a row to exist raise an exception if it doesn't"""
        with self.assertRaises(Exception):
            _ = self.cache.get("Does not exist", {"checksum": "0000"})
