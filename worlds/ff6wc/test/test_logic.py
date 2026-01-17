from collections.abc import Iterable
from typing import ClassVar

from worlds.ff6wc import Locations
from . import FF6WCTestBase


class TestFanaticsLogic(FF6WCTestBase):
    """ Everything in fanatics tower should require espers, so that it's not too difficult. """

    location_names_to_test: ClassVar[Iterable[str]] = ["White Dragon", "Gem Box"]

    def test_access(self) -> None:
        for loc_name in self.location_names_to_test:
            with self.subTest(f"{loc_name=}"):
                print(f"{loc_name=} {self.multiworld.state.prog_items[1]=}")
                self.world_setup()
                self.collect_by_name(["Strago"])
                self.assertEqual(self.can_reach_location(loc_name),
                                 False,
                                 f"fanatics {loc_name} with 0 espers")
                self.collect_by_name(["Tritoch", "Ifrit", "Bahamut"])
                self.assertEqual(self.can_reach_location(loc_name),
                                 False,
                                 f"fanatics {loc_name} with 3 espers")
                self.collect_by_name(["Maduin"])
                self.assertEqual(self.can_reach_location(loc_name),
                                 True,
                                 f"fanatics {loc_name} with 4 espers")


class TestFanaticsLogicTreasuresanity(TestFanaticsLogic):
    """ (Treasuresanity) Everything in fanatics tower should require 4 espers, so that it's not too difficult. """
    options = {
        "Treasuresanity": True
    }

    location_names_to_test = ["White Dragon", "Gem Box"] + Locations.minor_strago_ext_checks
