from . import MessengerTestBase
from .. import NOTES


class AccessTest(MessengerTestBase):
    options = {
        "shuffle_seals": "true",
    }

    def testDart(self):
        """locations that hard require the Rope Dart"""
        locations = ["Ninja Village Seal - Tree House", "Key of Hope", "Howling Grotto Seal - Crushing Pits",
                     "Glacial Peak Seal - Ice Climbers", "Tower of Time Seal - Time Waster Seal",
                     "Tower of Time Seal - Arcane Orbs", "Underworld Seal - Rising Fanta", "Key of Symbiosis",
                     "Elemental Skylands Seal - Water", "Elemental Skylands Seal - Fire"]
        items = [["Rope Dart"]]
        self.assertAccessDependency(locations, items)

    def testTabi(self):
        """locations that hard require the Ninja Tabi"""
        locations = ["Pyro", "Key of Chaos", "Underworld Seal - Sharp and Windy Climb", "Underworld Seal - Spike Wall",
                     "Underworld Seal - Fireball Wave", "Underworld Seal - Rising Fanta", "Sun Crest", "Moon Crest",
                     "Sunken Shrine Seal - Waterfall Paradise", "Sunken Shrine Seal - Tabi Gauntlet"]
        items = [["Ninja Tabi"]]
        self.assertAccessDependency(locations, items)

    def testWingsuit(self):
        """locations that hard require the Wingsuit"""
        locations = ["Candle", "Ninja Village Seal - Tree House", "Climbing Claws", "Key of Hope",
                     "Autumn Hills Seal - Trip Saws", "Autumn Hills Seal - Double Swing Saws",
                     "Autumn Hills Seal - Spike Ball Swing", "Autumn Hills Seal - Spike Ball Darts", "Necro",
                     "Ruxxtin's Amulet", "Catacombs Seal - Triple Spike Crushers", "Catacombs Seal - Crusher Gauntlet",
                     "Catacombs Seal - Dirty Pond", "Claustro", "Acro", "Bamboo Creek Seal - Spike Crushers and Doors",
                     "Bamboo Creek Seal - Spike Ball Pits", "Bamboo Creek Seal - Spike Crushers and Doors v2",
                     "Howling Grotto Seal - Crushing Pits", "Howling Grotto Seal - Windy Saws and Balls",
                     "Tower of Time Seal - Lantern Climb", "Demon King Crown", "Cloud Ruins Seal - Ghost Pit",
                     "Cloud Ruins Seal - Toothbrush Alley", "Cloud Ruins Seal - Saw Pit", "Cloud Ruins Seal - Money Farm Room",
                     "Tower of Time Seal - Lantern Climb", "Tower of Time Seal - Arcane Orbs",
                     "Underworld Seal - Sharp and Windy Climb", "Underworld Seal - Fireball Wave",
                     "Elemental Skylands Seal - Air", "Forlorn Temple Seal - Rocket Maze", "Forlorn Temple Seal - Rocket Sunset"]
        items = [["Wingsuit"]]
        self.assertAccessDependency(locations, items)

    def testVertical(self):
        """locations that require either the Rope Dart or the Wingsuit"""
        locations = ["Ninja Village Seal - Tree House", "Key of Hope", "Howling Grotto Seal - Crushing Pits",
                     "Glacial Peak Seal - Ice Climbers", "Tower of Time Seal - Time Waster Seal",
                     "Underworld Seal - Rising Fanta", "Key of Symbiosis",
                     "Elemental Skylands Seal - Water", "Elemental Skylands Seal - Fire", "Candle",
                     "Ninja Village Seal - Tree House", "Climbing Claws", "Key of Hope",
                     "Autumn Hills Seal - Trip Saws", "Autumn Hills Seal - Double Swing Saws",
                     "Autumn Hills Seal - Spike Ball Swing", "Autumn Hills Seal - Spike Ball Darts", "Necro",
                     "Ruxxtin's Amulet", "Catacombs Seal - Triple Spike Crushers", "Catacombs Seal - Crusher Gauntlet",
                     "Catacombs Seal - Dirty Pond", "Claustro", "Acro", "Bamboo Creek Seal - Spike Crushers and Doors",
                     "Bamboo Creek Seal - Spike Ball Pits", "Bamboo Creek Seal - Spike Crushers and Doors v2",
                     "Howling Grotto Seal - Crushing Pits", "Howling Grotto Seal - Windy Saws and Balls",
                     "Tower of Time Seal - Lantern Climb", "Demon King Crown", "Cloud Ruins Seal - Ghost Pit",
                     "Cloud Ruins Seal - Toothbrush Alley", "Cloud Ruins Seal - Saw Pit", "Cloud Ruins Seal - Money Farm Room",
                     "Tower of Time Seal - Lantern Climb", "Tower of Time Seal - Arcane Orbs",
                     "Underworld Seal - Sharp and Windy Climb", "Underworld Seal - Fireball Wave",
                     "Elemental Skylands Seal - Air", "Forlorn Temple Seal - Rocket Maze", "Forlorn Temple Seal - Rocket Sunset",
                     "Power Thistle", "Key of Strength", "Glacial Peak Seal - Projectile Spike Pit",
                     "Glacial Peak Seal - Glacial Air Swag", "Fairy Bottle", "Riviere Turquoise Seal - Flower Power"]
        items = [["Wingsuit", "Rope Dart"]]
        self.assertAccessDependency(locations, items)

    def testQuests(self):
        """specific "quest item" turn-in requirements"""
        locations = ["Acro", "Cloud Ruins Seal - Ghost Pit", "Cloud Ruins Seal - Toothbrush Alley",
                     "Cloud Ruins Seal - Saw Pit", "Cloud Ruins Seal - Money Farm Room"]
        """Cloud Ruins requires Ruxxtin's Amulet"""
        items = [["Ruxxtin's Amulet"]]
        self.assertAccessDependency(locations, items)

        locations = ["Key of Symbiosis", "Elemental Skylands Seal - Air", "Elemental Skylands Seal - Fire",
                     "Elemental Skylands Seal - Water", "Key of Courage"]
        """Elemental Skylands and Corrupted Future require the Fairy Bottle"""
        items = [["Fairy Bottle"]]
        self.assertAccessDependency(locations, items)

        locations = ["Key of Love"]
        items = [["Sun Crest", "Moon Crest"]]
        self.assertAccessDependency(locations, items)
        self.collect_all_but("Sun Crest")
        self.assertEqual(self.can_reach_location("Key of Love"), False)
        self.remove("Moon Crest")
        self.collect_all_but("Moon Crest")
        self.assertEqual(self.can_reach_location("Key of Love"), False)

        locations = ["Key of Strength"]
        items = [["Power Thistle"]]
        self.assertAccessDependency(locations, items)

        locations = ["Key of Courage"]
        items = [["Demon King Crown"]]
        self.assertAccessDependency(locations, items)

    def testGoal(self):
        self.collect_all_but([*NOTES, "Rescue Phantom"])
        self.assertBeatable(False)
        self.collect_all_but(["Key of Love", "Rescue Phantom"])
        self.assertBeatable(False)
        self.collect_by_name(["Key of Love", "Rescue Phantom"])
        self.assertBeatable(True)
