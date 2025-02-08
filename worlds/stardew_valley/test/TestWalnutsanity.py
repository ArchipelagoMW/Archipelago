from . import SVTestBase
from ..options import ExcludeGingerIsland, Walnutsanity
from ..strings.ap_names.ap_option_names import WalnutsanityOptionName
from ..strings.ap_names.transport_names import Transportation


class TestWalnutsanityNone(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Walnutsanity: Walnutsanity.preset_none,
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
        self.assert_cannot_reach_location(Transportation.parrot_express)

        self.collect("Island North Turtle")
        self.collect("Island Resort")
        self.collect("Open Professor Snail Cave")
        self.assert_cannot_reach_location(Transportation.parrot_express)

        self.collect("Dig Site Bridge")
        self.collect("Island Farmhouse")
        self.collect("Qi Walnut Room")
        self.assert_cannot_reach_location(Transportation.parrot_express)

        self.collect("Combat Level", 10)
        self.collect("Mining Level", 10)
        self.assert_cannot_reach_location(Transportation.parrot_express)

        self.collect("Progressive Slingshot")
        self.collect("Progressive Weapon", 5)
        self.collect("Progressive Pickaxe", 4)
        self.collect("Progressive Watering Can", 4)
        self.assert_can_reach_location(Transportation.parrot_express)


class TestWalnutsanityPuzzles(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Walnutsanity: frozenset({WalnutsanityOptionName.puzzles}),
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

        self.assert_cannot_reach_location(Transportation.parrot_express)
        self.collect("Island North Turtle")
        self.assert_can_reach_location(Transportation.parrot_express)


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
        self.assert_cannot_reach_location(Transportation.parrot_express)
        items = self.collect("5 Golden Walnuts", 8)
        self.assert_can_reach_location(Transportation.parrot_express)
        self.remove(items)
        self.assert_cannot_reach_location(Transportation.parrot_express)
        items = self.collect("3 Golden Walnuts", 14)
        self.assert_can_reach_location(Transportation.parrot_express)
        self.remove(items)
        self.assert_cannot_reach_location(Transportation.parrot_express)
        items = self.collect("Golden Walnut", 40)
        self.assert_can_reach_location(Transportation.parrot_express)
        self.remove(items)
        self.assert_cannot_reach_location(Transportation.parrot_express)
        self.collect("5 Golden Walnuts", 4)
        self.collect("3 Golden Walnuts", 6)
        self.collect("Golden Walnut", 2)
        self.assert_can_reach_location(Transportation.parrot_express)
