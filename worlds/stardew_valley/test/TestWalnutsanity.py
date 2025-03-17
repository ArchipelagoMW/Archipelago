from . import SVTestBase
from ..options import ExcludeGingerIsland, Walnutsanity, ToolProgression, SkillProgression
from ..strings.ap_names.ap_option_names import WalnutsanityOptionName


class TestWalnutsanityNone(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Walnutsanity: Walnutsanity.preset_none,
        SkillProgression: ToolProgression.option_progressive,
        ToolProgression: ToolProgression.option_progressive,
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


class TestWalnutsanityPuzzles(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Walnutsanity: frozenset({WalnutsanityOptionName.puzzles}),
        SkillProgression: ToolProgression.option_progressive,
        ToolProgression: ToolProgression.option_progressive,
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

    def test_field_office_locations_require_professor_snail(self):
        location_names = ["Complete Large Animal Collection", "Complete Snake Collection", "Complete Mummified Frog Collection",
                          "Complete Mummified Bat Collection", "Purple Flowers Island Survey", "Purple Starfish Island Survey", ]
        locations = [location for location in self.multiworld.get_locations() if location.name in location_names]
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
        for location in locations:
            self.assert_cannot_reach_location(location, self.multiworld.state)
        self.collect("Open Professor Snail Cave")
        for location in locations:
            self.assert_can_reach_location(location, self.multiworld.state)


class TestWalnutsanityBushes(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Walnutsanity: frozenset({WalnutsanityOptionName.bushes}),
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


class TestWalnutsanityPuzzlesAndBushes(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Walnutsanity: frozenset({WalnutsanityOptionName.puzzles, WalnutsanityOptionName.bushes}),
    }

    def test_only_bush_walnut_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertIn("Open Golden Coconut", location_names)
        self.assertNotIn("Fishing Walnut 4", location_names)
        self.assertNotIn("Journal Scrap #6", location_names)
        self.assertNotIn("Starfish Triangle", location_names)
        self.assertIn("Bush Behind Coconut Tree", location_names)
        self.assertIn("Purple Starfish Island Survey", location_names)
        self.assertNotIn("Volcano Monsters Walnut 3", location_names)
        self.assertIn("Cliff Over Island South Bush", location_names)

    def test_logic_received_walnuts(self):
        # You need to receive 25, and collect 15
        self.collect("Island Obelisk")
        self.collect("Island West Turtle")
        self.collect("5 Golden Walnuts", 5)

        self.assertFalse(self.multiworld.state.can_reach_location("Parrot Express", self.player))
        self.collect("Island North Turtle")
        self.assertTrue(self.multiworld.state.can_reach_location("Parrot Express", self.player))


class TestWalnutsanityDigSpots(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Walnutsanity: frozenset({WalnutsanityOptionName.dig_spots}),
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
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Walnutsanity: frozenset({WalnutsanityOptionName.repeatables}),
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
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Walnutsanity: Walnutsanity.preset_all,
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
