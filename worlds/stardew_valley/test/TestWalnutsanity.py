import unittest

from .bases import SVTestBase
from ..options import ExcludeGingerIsland, Walnutsanity, ToolProgression, SkillProgression
from ..strings.ap_names.ap_option_names import WalnutsanityOptionName


class SVWalnutsanityTestBase(SVTestBase):
    expected_walnut_locations: set[str] = set()
    unexpected_walnut_locations: set[str] = set()

    @classmethod
    def setUpClass(cls) -> None:
        if cls is SVWalnutsanityTestBase:
            raise unittest.SkipTest("Base tests disabled")

        super().setUpClass()

    def test_walnut_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for location in self.expected_walnut_locations:
            self.assertIn(location, location_names, f"{location} should be in the location names")
        for location in self.unexpected_walnut_locations:
            self.assertNotIn(location, location_names, f"{location} should not be in the location names")


class TestWalnutsanityNone(SVWalnutsanityTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Walnutsanity: Walnutsanity.preset_none,
        SkillProgression: ToolProgression.option_progressive,
        ToolProgression: ToolProgression.option_progressive,
    }
    unexpected_walnut_locations = {
        "Walnutsanity: Open Golden Coconut",
        "Walnutsanity: Fishing Walnut 4",
        "Walnutsanity: Journal Scrap #6",
        "Walnutsanity: Starfish Triangle",
        "Walnutsanity: Bush Behind Coconut Tree",
        "Walnutsanity: Purple Starfish Island Survey",
        "Walnutsanity: Volcano Monsters Walnut 3",
        "Walnutsanity: Cliff Over Island South Bush",
    }

    def test_logic_received_walnuts(self):
        # You need to receive 0, and collect 40
        self.collect("Island Obelisk")
        self.collect("Island West Turtle")
        self.collect("Progressive House")
        self.collect("5 Golden Walnuts", 10)

        self.assertFalse(self.multiworld.state.can_reach_location("Parrot Express", self.player))
        self.collect("Island North Turtle")
        self.collect("Island Resort")
        self.collect("Open Professor Snail Cave")
        self.assertFalse(self.multiworld.state.can_reach_location("Parrot Express", self.player))
        self.collect("Dig Site Bridge")
        self.collect("Island Farmhouse")
        self.collect("Qi Walnut Room")
        self.assertFalse(self.multiworld.state.can_reach_location("Parrot Express", self.player))
        self.collect("Combat Level", 10)
        self.collect("Mining Level", 10)
        self.assertFalse(self.multiworld.state.can_reach_location("Parrot Express", self.player))
        self.collect("Progressive Slingshot")
        self.collect("Progressive Weapon", 5)
        self.collect("Progressive Pickaxe", 4)
        self.collect("Progressive Watering Can", 4)
        self.assertTrue(self.multiworld.state.can_reach_location("Parrot Express", self.player))


class TestWalnutsanityPuzzles(SVWalnutsanityTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Walnutsanity: frozenset({WalnutsanityOptionName.puzzles}),
        SkillProgression: ToolProgression.option_progressive,
        ToolProgression: ToolProgression.option_progressive,
    }
    expected_walnut_locations = {
        "Walnutsanity: Open Golden Coconut",
        "Walnutsanity: Purple Starfish Island Survey",
    }
    unexpected_walnut_locations = {
        "Walnutsanity: Fishing Walnut 4",
        "Walnutsanity: Journal Scrap #6",
        "Walnutsanity: Starfish Triangle",
        "Walnutsanity: Bush Behind Coconut Tree",
        "Walnutsanity: Volcano Monsters Walnut 3",
        "Walnutsanity: Cliff Over Island South Bush",
    }

    def test_field_office_locations_require_professor_snail(self):
        location_names = ["Walnutsanity: Complete Large Animal Collection", "Walnutsanity: Complete Snake Collection",
                          "Walnutsanity: Complete Mummified Frog Collection", "Walnutsanity: Complete Mummified Bat Collection",
                          "Walnutsanity: Purple Flowers Island Survey", "Walnutsanity: Purple Starfish Island Survey", ]
        self.collect("Island Obelisk")
        self.collect("Island North Turtle")
        self.collect("Island West Turtle")
        self.collect("Island Resort")
        self.collect("Dig Site Bridge")
        self.collect("Progressive House")
        self.collect("Progressive Pan")
        self.collect("Progressive Fishing Rod")
        self.collect("Progressive Watering Can")
        self.collect("Progressive Pickaxe", 4)
        self.collect("Progressive Sword", 5)
        self.collect("Combat Level", 10)
        self.collect("Mining Level", 10)
        for location in location_names:
            self.assert_cannot_reach_location(location)
        self.collect("Open Professor Snail Cave")
        for location in location_names:
            self.assert_can_reach_location(location)


class TestWalnutsanityBushes(SVWalnutsanityTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Walnutsanity: frozenset({WalnutsanityOptionName.bushes}),
    }
    expected_walnut_locations = {
        "Walnutsanity: Bush Behind Coconut Tree",
        "Walnutsanity: Cliff Over Island South Bush",
    }
    unexpected_walnut_locations = {
        "Walnutsanity: Open Golden Coconut",
        "Walnutsanity: Fishing Walnut 4",
        "Walnutsanity: Journal Scrap #6",
        "Walnutsanity: Starfish Triangle",
        "Walnutsanity: Purple Starfish Island Survey",
        "Walnutsanity: Volcano Monsters Walnut 3",
    }


class TestWalnutsanityPuzzlesAndBushes(SVWalnutsanityTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Walnutsanity: frozenset({WalnutsanityOptionName.puzzles, WalnutsanityOptionName.bushes}),
    }
    expected_walnut_locations = {
        "Walnutsanity: Open Golden Coconut",
        "Walnutsanity: Bush Behind Coconut Tree",
        "Walnutsanity: Purple Starfish Island Survey",
        "Walnutsanity: Cliff Over Island South Bush",
    }
    unexpected_walnut_locations = {
        "Walnutsanity: Fishing Walnut 4",
        "Walnutsanity: Journal Scrap #6",
        "Walnutsanity: Starfish Triangle",
        "Walnutsanity: Volcano Monsters Walnut 3",
    }

    def test_logic_received_walnuts(self):
        # You need to receive 25, and collect 15
        self.collect("Island Obelisk")
        self.collect("Island West Turtle")
        self.collect("5 Golden Walnuts", 5)

        self.assertFalse(self.multiworld.state.can_reach_location("Parrot Express", self.player))
        self.collect("Island North Turtle")
        self.assertTrue(self.multiworld.state.can_reach_location("Parrot Express", self.player))


class TestWalnutsanityDigSpots(SVWalnutsanityTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Walnutsanity: frozenset({WalnutsanityOptionName.dig_spots}),
    }
    expected_walnut_locations = {
        "Walnutsanity: Journal Scrap #6",
        "Walnutsanity: Starfish Triangle",
    }
    unexpected_walnut_locations = {
        "Walnutsanity: Open Golden Coconut",
        "Walnutsanity: Fishing Walnut 4",
        "Walnutsanity: Bush Behind Coconut Tree",
        "Walnutsanity: Purple Starfish Island Survey",
        "Walnutsanity: Volcano Monsters Walnut 3",
        "Walnutsanity: Cliff Over Island South Bush",
    }


class TestWalnutsanityRepeatables(SVWalnutsanityTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Walnutsanity: frozenset({WalnutsanityOptionName.repeatables}),
    }
    expected_walnut_locations = {
        "Walnutsanity: Fishing Walnut 4",
        "Walnutsanity: Volcano Monsters Walnut 3",
    }
    unexpected_walnut_locations = {
        "Walnutsanity: Open Golden Coconut",
        "Walnutsanity: Journal Scrap #6",
        "Walnutsanity: Starfish Triangle",
        "Walnutsanity: Bush Behind Coconut Tree",
        "Walnutsanity: Purple Starfish Island Survey",
        "Walnutsanity: Cliff Over Island South Bush",
    }


class TestWalnutsanityAll(SVWalnutsanityTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Walnutsanity: Walnutsanity.preset_all,
    }
    expected_walnut_locations = {
        "Walnutsanity: Open Golden Coconut",
        "Walnutsanity: Fishing Walnut 4",
        "Walnutsanity: Journal Scrap #6",
        "Walnutsanity: Starfish Triangle",
        "Walnutsanity: Bush Behind Coconut Tree",
        "Walnutsanity: Purple Starfish Island Survey",
        "Walnutsanity: Volcano Monsters Walnut 3",
        "Walnutsanity: Cliff Over Island South Bush",
    }

    def test_logic_received_walnuts(self):
        # You need to receive 40, and collect 4
        self.collect("Island Obelisk")
        self.collect("Island West Turtle")
        self.assertFalse(self.multiworld.state.can_reach_location("Parrot Express", self.player))
        items = self.collect("5 Golden Walnuts", 8)
        self.assertTrue(self.multiworld.state.can_reach_location("Parrot Express", self.player))
        self.remove(items)
        self.assertFalse(self.multiworld.state.can_reach_location("Parrot Express", self.player))
        items = self.collect("3 Golden Walnuts", 14)
        self.assertTrue(self.multiworld.state.can_reach_location("Parrot Express", self.player))
        self.remove(items)
        self.assertFalse(self.multiworld.state.can_reach_location("Parrot Express", self.player))
        items = self.collect("Golden Walnut", 40)
        self.assertTrue(self.multiworld.state.can_reach_location("Parrot Express", self.player))
        self.remove(items)
        self.assertFalse(self.multiworld.state.can_reach_location("Parrot Express", self.player))
        self.collect("5 Golden Walnuts", 4)
        self.collect("3 Golden Walnuts", 6)
        self.collect("Golden Walnut", 2)
        self.assertTrue(self.multiworld.state.can_reach_location("Parrot Express", self.player))
