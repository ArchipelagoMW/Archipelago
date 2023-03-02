from . import MessengerTestBase
from .. import NOTES


class AccessTest(MessengerTestBase):
    options = {
        "shuffle_seals": "true",
    }

    def testTabi(self):
        """locations that hard require the Ninja Tabi"""
        locations = ["Pyro", "Key of Chaos", "Underworld Seal - Sharp and Windy Climb", "Underworld Seal - Spike Wall",
                     "Underworld Seal - Fireball Wave", "Underworld Seal - Rising Fanta", "Sun Crest", "Moon Crest",
                     "Sunken Shrine Seal - Waterfall Paradise", "Sunken Shrine Seal - Tabi Gauntlet"]
        items = [["Ninja Tabi"]]
        self.assertAccessDependency(locations, items)

    def testDart(self):
        """locations that hard require the Rope Dart"""
        locations = ["Ninja Village Seal - Tree House", "Key of Hope", "Howling Grotto Seal - Crushing Pits",
                     "Glacial Peak Seal - Ice Climbers", "Tower of Time Seal - Time Waster Seal",
                     "Tower of Time Seal - Arcane Orbs", "Underworld Seal - Rising Fanta", "Key of Symbiosis",
                     "Elemental Skylands Seal - Water", "Elemental Skylands Seal - Fire"]
        items = [["Rope Dart"]]
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
                     "Elemental Skylands Seal - Air", "Forlorn Temple Seal - Rocket Maze",
                     "Forlorn Temple Seal - Rocket Sunset", "Astral Seed"]
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
                     "Glacial Peak Seal - Glacial Air Swag", "Fairy Bottle", "Riviere Turquoise Seal - Flower Power",
                     "Searing Crags Seal - Triple Ball Spinner", "Searing Crags Seal - Raining Rocks",
                     "Searing Crags Seal - Rhythm Rocks", "Astral Seed", "Astral Tea Leaves"]
        items = [["Wingsuit", "Rope Dart"]]
        self.assertAccessDependency(locations, items)

    def testAmulet(self):
        """Locations that require Ruxxtin's Amulet"""
        locations = ["Acro", "Cloud Ruins Seal - Ghost Pit", "Cloud Ruins Seal - Toothbrush Alley",
                     "Cloud Ruins Seal - Saw Pit", "Cloud Ruins Seal - Money Farm Room"]
        """Cloud Ruins requires Ruxxtin's Amulet"""
        items = [["Ruxxtin's Amulet"]]
        self.assertAccessDependency(locations, items)

    def testBottle(self):
        """Elemental Skylands and Corrupted Future require the Fairy Bottle"""
        locations = ["Key of Symbiosis", "Elemental Skylands Seal - Air", "Elemental Skylands Seal - Fire",
                     "Elemental Skylands Seal - Water", "Key of Courage"]
        items = [["Fairy Bottle"]]
        self.assertAccessDependency(locations, items)

    def testCrests(self):
        """Test Key of Love nonsense"""
        locations = ["Key of Love"]
        items = [["Sun Crest", "Moon Crest"]]
        self.assertAccessDependency(locations, items)
        self.collect_all_but("Sun Crest")
        self.assertEqual(self.can_reach_location("Key of Love"), False)
        self.remove(self.get_item_by_name("Moon Crest"))
        self.collect_by_name("Sun Crest")
        self.assertEqual(self.can_reach_location("Key of Love"), False)

    def testThistle(self):
        """I'm a chuckster!"""
        locations = ["Key of Strength"]
        items = [["Power Thistle"]]
        self.assertAccessDependency(locations, items)

    def testCrown(self):
        """Crocomire but not"""
        locations = ["Key of Courage"]
        items = [["Demon King Crown"]]
        self.assertAccessDependency(locations, items)

    def testGoal(self):
        """Test some different states to verify goal requires the correct items"""
        self.collect_all_but([*NOTES, "Rescue Phantom"])
        self.assertEqual(self.can_reach_location("Rescue Phantom"), False)
        self.collect_all_but(["Key of Love", "Rescue Phantom"])
        self.assertBeatable(False)
        self.collect_by_name(["Key of Love"])
        self.assertEqual(self.can_reach_location("Rescue Phantom"), True)
        self.assertBeatable(True)


class NoLogicTest(MessengerTestBase):
    options = {
        "enable_logic": "false"
    }

    def testNoLogic(self):
        """Test some funny locations to make sure they aren't reachable but we can still win"""
        self.assertEqual(self.can_reach_location("Pyro"), False)
        self.assertEqual(self.can_reach_location("Rescue Phantom"), False)
        self.assertBeatable(True)
