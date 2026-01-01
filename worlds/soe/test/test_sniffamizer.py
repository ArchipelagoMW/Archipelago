import typing
from unittest import TestCase, skipUnless

from . import SoETestBase
from .. import pyevermizer
from ..options import Sniffamizer


class TestCount(TestCase):
    """
    Test that counts line up for sniff spots
    """

    def test_compare_counts(self) -> None:
        self.assertEqual(len(pyevermizer.get_sniff_locations()), len(pyevermizer.get_sniff_items()),
                         "Sniff locations and sniff items don't line up")


class Bases:
    # class in class to avoid running tests for helper class
    class TestSniffamizerLocal(SoETestBase):
        """
        Test that provided options do not add sniff items or locations
        """
        def test_no_sniff_items(self) -> None:
            self.assertLess(len(self.multiworld.itempool), 500,
                            "Unexpected number of items")
            for item in self.multiworld.itempool:
                if item.code is not None:
                    self.assertLess(item.code, 65000,
                                    "Unexpected item type")

        def test_no_sniff_locations(self) -> None:
            location_count = sum(1 for location in self.multiworld.get_locations(self.player) if location.item is None)
            self.assertLess(location_count, 500,
                            "Unexpected number of locations")
            for location in self.multiworld.get_locations(self.player):
                if location.address is not None:
                    self.assertLess(location.address, 65000,
                                    "Unexpected location type")
            self.assertEqual(location_count, len(self.multiworld.itempool),
                             "Locations and item counts do not line up")

    class TestSniffamizerPool(SoETestBase):
        """
        Test that provided options add sniff items and locations
        """
        def test_sniff_items(self) -> None:
            self.assertGreater(len(self.multiworld.itempool), 500,
                               "Unexpected number of items")

        def test_sniff_locations(self) -> None:
            location_count = sum(1 for location in self.multiworld.get_locations(self.player) if location.item is None)
            self.assertGreater(location_count, 500,
                               "Unexpected number of locations")
            self.assertTrue(any(location.address is not None and location.address >= 65000
                                for location in self.multiworld.get_locations(self.player)),
                            "No sniff locations")
            self.assertEqual(location_count, len(self.multiworld.itempool),
                             "Locations and item counts do not line up")


class TestSniffamizerShuffle(Bases.TestSniffamizerLocal):
    """
    Test that shuffle does not add extra items or locations
    """
    options: typing.Dict[str, typing.Any] = {
        "sniffamizer": "shuffle"
    }

    def test_flags(self) -> None:
        # default -> no flags
        flags = self.world.options.flags
        self.assertNotIn("s", flags)
        self.assertNotIn("S", flags)
        self.assertNotIn("v", flags)


@skipUnless(hasattr(Sniffamizer, "option_everywhere"), "Feature disabled")
class TestSniffamizerEverywhereVanilla(Bases.TestSniffamizerPool):
    """
    Test that everywhere + vanilla ingredients does add extra items and locations
    """
    options: typing.Dict[str, typing.Any] = {
        "sniffamizer": "everywhere",
        "sniff_ingredients": "vanilla_ingredients",
    }

    def test_flags(self) -> None:
        flags = self.world.options.flags
        self.assertIn("S", flags)
        self.assertNotIn("v", flags)


@skipUnless(hasattr(Sniffamizer, "option_everywhere"), "Feature disabled")
class TestSniffamizerEverywhereRandom(Bases.TestSniffamizerPool):
    """
    Test that everywhere + random ingredients also adds extra items and locations
    """
    options: typing.Dict[str, typing.Any] = {
        "sniffamizer": "everywhere",
        "sniff_ingredients": "random_ingredients",
    }

    def test_flags(self) -> None:
        flags = self.world.options.flags
        self.assertIn("S", flags)
        self.assertIn("v", flags)


@skipUnless(hasattr(Sniffamizer, "option_everywhere"), "Feature disabled")
class EverywhereAccessTest(SoETestBase):
    """
    Test that everywhere has certain rules
    """
    options: typing.Dict[str, typing.Any] = {
        "sniffamizer": "everywhere",
    }

    @staticmethod
    def _resolve_numbers(spots: typing.Mapping[str, typing.Iterable[int]]) -> typing.List[str]:
        return [f"{name} #{number}" for name, numbers in spots.items() for number in numbers]

    def test_knight_basher(self) -> None:
        locations = ["Mungola", "Lightning Storm"] + self._resolve_numbers({
            "Gomi's Tower Sniff": range(473, 491),
            "Gomi's Tower": range(195, 199),
        })
        items = [["Knight Basher"]]
        self.assertAccessDependency(locations, items)
