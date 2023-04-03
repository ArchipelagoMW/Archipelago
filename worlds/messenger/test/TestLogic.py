from BaseClasses import ItemClassification
from . import MessengerTestBase


class HardLogicTest(MessengerTestBase):
    options = {
        "logic_level": "hard"
    }

    def testVertical(self) -> None:
        """Test the locations that still require wingsuit or rope dart."""
        locations = [
            # tower of time
            "Tower of Time Seal - Time Waster Seal", "Tower of Time Seal - Lantern Climb",
            "Tower of Time Seal - Arcane Orbs",
            # ninja village
            "Candle", "Astral Seed", "Ninja Village Seal - Tree House",
            # autumn hills
            "Climbing Claws", "Key of Hope",
            "Autumn Hills Seal - Trip Saws", "Autumn Hills Seal - Double Swing Saws",
            "Autumn Hills Seal - Spike Ball Swing", "Autumn Hills Seal - Spike Ball Darts",
            # forlorn temple
            "Demon King Crown",
            "Forlorn Temple Seal - Rocket Maze", "Forlorn Temple Seal - Rocket Sunset",
            # catacombs
            "Necro", "Ruxxtin's Amulet",
            "Catacombs Seal - Triple Spike Crushers", "Catacombs Seal - Crusher Gauntlet", "Catacombs Seal - Dirty Pond",
            # bamboo creek
            "Claustro",
            "Bamboo Creek Seal - Spike Crushers and Doors", "Bamboo Creek Seal - Spike Ball Pits",
            "Bamboo Creek Seal - Spike Crushers and Doors v2",
            # howling grotto
            "Howling Grotto Seal - Crushing Pits", "Howling Grotto Seal - Crushing Pits",
            # glacial peak
            "Glacial Peak Seal - Ice Climbers",
            # cloud ruins
            "Acro", "Cloud Ruins Seal - Ghost Pit",
            "Cloud Ruins Seal - Toothbrush Alley", "Cloud Ruins Seal - Saw Pit", "Cloud Ruins Seal - Money Farm Room",
            # underworld
            "Underworld Seal - Rising Fanta", "Underworld Seal - Sharp and Windy Climb",
            # riviere turquoise
            "Fairy Bottle", "Riviere Turquoise Seal - Flower Power",
            # elemental skylands
            "Elemental Skylands Seal - Air", "Elemental Skylands Seal - Water", "Elemental Skylands Seal - Fire",
            # phantom
            "Rescue Phantom",
        ]
        items = [["Wingsuit", "Rope Dart"]]
        self.assertAccessDependency(locations, items)

    def testWindmill(self) -> None:
        """Windmill Shuriken isn't progression on normal difficulty, so test it's marked correctly and required."""
        self.assertEqual(ItemClassification.progression, self.get_item_by_name("Windmill Shuriken").classification)
        windmill_locs = [
            "Key of Strength",
            "Key of Symbiosis",
            "Underworld Seal - Fireball Wave"
        ]
        for loc in windmill_locs:
            with self.subTest("can't reach location with nothing", location=loc):
                self.assertFalse(self.can_reach_location(loc))

        items = self.get_items_by_name(["Windmill Shuriken", "Ninja Tabi", "Fairy Bottle"])
        self.collect(items)
        for loc in windmill_locs:
            with self.subTest("can reach with Windmill", location=loc):
                self.assertTrue(self.can_reach_location(loc))

        special_loc = "Autumn Hills Seal - Spike Ball Darts"
        item = self.get_item_by_name("Wingsuit")
        self.collect(item)
        self.assertTrue(self.can_reach_location(special_loc))
        self.remove(item)

        item = self.get_item_by_name("Rope Dart")
        self.collect(item)
        self.assertTrue(self.can_reach_location(special_loc))


class ChallengingLogicTest(MessengerTestBase):
    options = {
        "shuffle_seals": "false",
        "logic_level": "challenging"
    }


class NoLogicTest(MessengerTestBase):
    options = {
        "logic_level": "oob"
    }

    def testAccess(self) -> None:
        """Test the locations with rules still require things."""
        all_locations = [
            "Claustro", "Key of Strength", "Key of Symbiosis", "Key of Love", "Pyro", "Key of Chaos", "Key of Courage",
            "Autumn Hills Seal - Spike Ball Darts", "Ninja Village Seal - Tree House", "Underworld Seal - Fireball Wave",
            "Tower of Time Seal - Time Waster Seal", "Rescue Phantom", "Elemental Skylands Seal - Air",
            "Elemental Skylands Seal - Water", "Elemental Skylands Seal - Fire",
        ]
        for loc in all_locations:
            with self.subTest("Default unreachables", location=loc):
                self.assertFalse(self.can_reach_location(loc))

    def testNoLogic(self) -> None:
        """Test some funny locations to make sure they aren't reachable, but we can still win"""
        self.assertEqual(self.can_reach_location("Pyro"), False)
        self.assertEqual(self.can_reach_location("Rescue Phantom"), False)
        self.assertBeatable(True)
