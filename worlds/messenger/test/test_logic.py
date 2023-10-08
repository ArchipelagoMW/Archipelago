from BaseClasses import ItemClassification
from . import MessengerTestBase


class HardLogicTest(MessengerTestBase):
    options = {
        "logic_level": "hard",
        "shuffle_shards": "true",
    }

    def test_vertical(self) -> None:
        """Test the locations that still require wingsuit or rope dart."""
        locations = [
            # tower of time
            "Tower of Time Seal - Time Waster", "Tower of Time Seal - Lantern Climb",
            "Tower of Time Seal - Arcane Orbs",
            # ninja village
            "Ninja Village - Candle", "Ninja Village - Astral Seed", "Ninja Village Seal - Tree House",
            # autumn hills
            "Autumn Hills - Climbing Claws", "Autumn Hills - Key of Hope", "Autumn Hills - Leaf Golem",
            "Autumn Hills Seal - Trip Saws", "Autumn Hills Seal - Double Swing Saws",
            "Autumn Hills Seal - Spike Ball Swing", "Autumn Hills Seal - Spike Ball Darts",
            "Autumn Hills Mega Shard", "Hidden Entrance Mega Shard",
            # forlorn temple
            "Forlorn Temple - Demon King",
            "Forlorn Temple Seal - Rocket Maze", "Forlorn Temple Seal - Rocket Sunset",
            "Sunny Day Mega Shard", "Down Under Mega Shard",
            # catacombs
            "Catacombs - Necro", "Catacombs - Ruxxtin's Amulet", "Catacombs - Ruxxtin",
            "Catacombs Seal - Triple Spike Crushers", "Catacombs Seal - Crusher Gauntlet", "Catacombs Seal - Dirty Pond",
            "Catacombs Mega Shard",
            # bamboo creek
            "Bamboo Creek - Claustro",
            "Bamboo Creek Seal - Spike Crushers and Doors", "Bamboo Creek Seal - Spike Ball Pits",
            "Bamboo Creek Seal - Spike Crushers and Doors v2",
            "Above Entrance Mega Shard", "Abandoned Mega Shard", "Time Loop Mega Shard",
            # howling grotto
            "Howling Grotto - Emerald Golem", "Howling Grotto Seal - Crushing Pits", "Howling Grotto Seal - Crushing Pits",
            # searing crags
            "Searing Crags - Astral Tea Leaves",
            # cloud ruins
            "Cloud Ruins - Acro", "Cloud Ruins Seal - Ghost Pit",
            "Cloud Ruins Seal - Toothbrush Alley", "Cloud Ruins Seal - Saw Pit", "Cloud Ruins Seal - Money Farm Room",
            "Cloud Entrance Mega Shard", "Time Warp Mega Shard", "Money Farm Room Mega Shard 1", "Money Farm Room Mega Shard 2",
            # underworld
            "Underworld Seal - Rising Fanta", "Underworld Seal - Sharp and Windy Climb",
            # elemental skylands
            "Elemental Skylands Seal - Air",
            # phantom
            "Rescue Phantom",
        ]
        items = [["Wingsuit", "Rope Dart"]]
        self.assertAccessDependency(locations, items)

    def test_windmill(self) -> None:
        """Windmill Shuriken isn't progression on normal difficulty, so test it's marked correctly and required."""
        self.assertEqual(ItemClassification.progression, self.get_item_by_name("Windmill Shuriken").classification)
        windmill_locs = [
            "Searing Crags - Key of Strength",
            "Elemental Skylands - Key of Symbiosis",
            "Underworld Seal - Fireball Wave",
        ]
        for loc in windmill_locs:
            with self.subTest("can't reach location with nothing", location=loc):
                self.assertFalse(self.can_reach_location(loc))

        items = self.get_items_by_name(["Windmill Shuriken", "Lightfoot Tabi", "Magic Firefly"])
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

    def test_glacial(self) -> None:
        """Test Glacial Peak locations."""
        self.assertAccessDependency(["Glacial Peak Seal - Ice Climbers"],
                                    [["Second Wind", "Meditation"], ["Rope Dart"], ["Wingsuit"]],
                                    True)
        self.assertAccessDependency(["Glacial Peak Seal - Projectile Spike Pit"],
                                    [["Strike of the Ninja"], ["Windmill Shuriken"], ["Rope Dart"], ["Wingsuit"]],
                                    True)
        self.assertAccessDependency(["Glacial Peak Seal - Glacial Air Swag", "Glacial Peak Mega Shard"],
                                    [["Windmill Shuriken"], ["Wingsuit"], ["Rope Dart"]],
                                    True)


class NoLogicTest(MessengerTestBase):
    options = {
        "logic_level": "oob",
    }

    def test_access(self) -> None:
        """Test the locations with rules still require things."""
        all_locations = [
            "Bamboo Creek - Claustro", "Searing Crags - Key of Strength", "Elemental Skylands - Key of Symbiosis",
            "Sunken Shrine - Key of Love", "Searing Crags - Pyro", "Underworld - Key of Chaos",
            "Corrupted Future - Key of Courage", "Autumn Hills Seal - Spike Ball Darts",
            "Ninja Village Seal - Tree House", "Underworld Seal - Fireball Wave", "Tower of Time Seal - Time Waster",
            "Rescue Phantom", "Elemental Skylands Seal - Air", "Elemental Skylands Seal - Water",
            "Elemental Skylands Seal - Fire",
        ]
        for loc in all_locations:
            with self.subTest("Default unreachables", location=loc):
                self.assertFalse(self.can_reach_location(loc))
        self.assertBeatable(True)
