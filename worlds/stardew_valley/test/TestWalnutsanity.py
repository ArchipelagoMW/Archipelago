import unittest
from typing import ClassVar, Set

from . import SVTestBase
from ..content.feature import fishsanity
from ..mods.mod_data import ModNames
from ..options import Fishsanity, ExcludeGingerIsland, Mods, SpecialOrderLocations, Walnutsanity
from ..strings.fish_names import Fish, SVEFish, DistantLandsFish


class TestWalnutsanityNone(SVTestBase):
    options = {
        Walnutsanity.internal_name: [],
    }

    def test_no_walnut_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertNotIn("Open Golden Coconut", location_names)
        self.assertNotIn("Fishing Walnut 4", location_names)
        self.assertNotIn("Journal Scrap #6", location_names)
        self.assertNotIn("Starfish Triangle", location_names)
        self.assertNotIn("Bush Behind Coconut Tree", location_names)
        self.assertNotIn("Purple Starfish Island Survey", location_names)
        self.assertNotIn("Volcano Monsters Walnut 3", location_names)
        self.assertNotIn("Cliff Over Island South Bush", location_names)


class TestWalnutsanityPuzzles(SVTestBase):
    options = {
        Walnutsanity.internal_name: ["Puzzles"],
    }

    def test_only_puzzle_walnut_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertIn("Open Golden Coconut", location_names)
        self.assertNotIn("Fishing Walnut 4", location_names)
        self.assertNotIn("Journal Scrap #6", location_names)
        self.assertNotIn("Starfish Triangle", location_names)
        self.assertNotIn("Bush Behind Coconut Tree", location_names)
        self.assertIn("Purple Starfish Island Survey", location_names)
        self.assertNotIn("Volcano Monsters Walnut 3", location_names)
        self.assertNotIn("Cliff Over Island South Bush", location_names)


class TestWalnutsanityBushes(SVTestBase):
    options = {
        Walnutsanity.internal_name: ["Bushes"],
    }

    def test_only_bush_walnut_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertNotIn("Open Golden Coconut", location_names)
        self.assertNotIn("Fishing Walnut 4", location_names)
        self.assertNotIn("Journal Scrap #6", location_names)
        self.assertNotIn("Starfish Triangle", location_names)
        self.assertIn("Bush Behind Coconut Tree", location_names)
        self.assertNotIn("Purple Starfish Island Survey", location_names)
        self.assertNotIn("Volcano Monsters Walnut 3", location_names)
        self.assertIn("Cliff Over Island South Bush", location_names)


class TestWalnutsanityDigSpots(SVTestBase):
    options = {
        Walnutsanity.internal_name: ["Dig Spots"],
    }

    def test_only_dig_spots_walnut_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertNotIn("Open Golden Coconut", location_names)
        self.assertNotIn("Fishing Walnut 4", location_names)
        self.assertIn("Journal Scrap #6", location_names)
        self.assertIn("Starfish Triangle", location_names)
        self.assertNotIn("Bush Behind Coconut Tree", location_names)
        self.assertNotIn("Purple Starfish Island Survey", location_names)
        self.assertNotIn("Volcano Monsters Walnut 3", location_names)
        self.assertNotIn("Cliff Over Island South Bush", location_names)


class TestWalnutsanityRepeatables(SVTestBase):
    options = {
        Walnutsanity.internal_name: ["Repeatables"],
    }

    def test_only_repeatable_walnut_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertNotIn("Open Golden Coconut", location_names)
        self.assertIn("Fishing Walnut 4", location_names)
        self.assertNotIn("Journal Scrap #6", location_names)
        self.assertNotIn("Starfish Triangle", location_names)
        self.assertNotIn("Bush Behind Coconut Tree", location_names)
        self.assertNotIn("Purple Starfish Island Survey", location_names)
        self.assertIn("Volcano Monsters Walnut 3", location_names)
        self.assertNotIn("Cliff Over Island South Bush", location_names)


class TestWalnutsanityAll(SVTestBase):
    options = {
        Walnutsanity.internal_name: ["Puzzles", "Bushes", "Dig Spots", "Repeatables", ],
    }

    def test_all_walnut_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertIn("Open Golden Coconut", location_names)
        self.assertIn("Fishing Walnut 4", location_names)
        self.assertIn("Journal Scrap #6", location_names)
        self.assertIn("Starfish Triangle", location_names)
        self.assertIn("Bush Behind Coconut Tree", location_names)
        self.assertIn("Purple Starfish Island Survey", location_names)
        self.assertIn("Volcano Monsters Walnut 3", location_names)
        self.assertIn("Cliff Over Island South Bush", location_names)

