from . import MessengerTestBase
from ..Constants import NOTES, PHOBEKINS


class AccessTest(MessengerTestBase):
    options = {
        "shuffle_shards": "true",
    }

    def testTabi(self) -> None:
        """locations that hard require the Ninja Tabi"""
        locations = ["Pyro", "Key of Chaos", "Underworld Seal - Sharp and Windy Climb", "Underworld Seal - Spike Wall",
                     "Underworld Seal - Fireball Wave", "Underworld Seal - Rising Fanta", "Sun Crest", "Moon Crest",
                     "Sunken Shrine Seal - Waterfall Paradise", "Sunken Shrine Seal - Tabi Gauntlet",
                     "Mega Shard of the Moon", "Mega Shard of the Sun", "Under Entrance Mega Shard",
                     "Hot Tub Mega Shard", "Projectile Pit Mega Shard"]
        items = [["Ninja Tabi"]]
        self.assertAccessDependency(locations, items)

    def testDart(self) -> None:
        """locations that hard require the Rope Dart"""
        locations = ["Ninja Village Seal - Tree House", "Key of Hope", "Howling Grotto Seal - Crushing Pits",
                     "Glacial Peak Seal - Ice Climbers", "Tower of Time Seal - Time Waster Seal",
                     "Tower of Time Seal - Arcane Orbs", "Underworld Seal - Rising Fanta", "Key of Symbiosis",
                     "Elemental Skylands Seal - Water", "Elemental Skylands Seal - Fire", "Earth Mega Shard",
                     "Water Mega Shard"]
        items = [["Rope Dart"]]
        self.assertAccessDependency(locations, items)

    def testWingsuit(self) -> None:
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
                     "Forlorn Temple Seal - Rocket Sunset", "Astral Seed", "Astral Tea Leaves",
                     "Autumn Hills Mega Shard", "Hidden Entrance Mega Shard", "Sunny Day Mega Shard",
                     "Down Under Mega Shard", "Catacombs Mega Shard", "Above Entrance Mega Shard",
                     "Abandoned Mega Shard", "Time Loop Mega Shard", "Money Farm Room Mega Shard 1",
                     "Money Farm Room Mega Shard 2", "Leaf Golem", "Ruxxtin", "Emerald Golem"]
        items = [["Wingsuit"]]
        self.assertAccessDependency(locations, items)

    def testVertical(self) -> None:
        """locations that require either the Rope Dart or the Wingsuit"""
        locations = ["Ninja Village Seal - Tree House", "Key of Hope", "Howling Grotto Seal - Crushing Pits",
                     "Glacial Peak Seal - Ice Climbers", "Tower of Time Seal - Time Waster Seal",
                     "Underworld Seal - Rising Fanta", "Key of Symbiosis",
                     "Elemental Skylands Seal - Water", "Elemental Skylands Seal - Fire", "Candle",
                     "Climbing Claws", "Key of Hope", "Autumn Hills Seal - Trip Saws",
                     "Autumn Hills Seal - Double Swing Saws", "Autumn Hills Seal - Spike Ball Swing",
                     "Autumn Hills Seal - Spike Ball Darts", "Necro", "Ruxxtin's Amulet",
                     "Catacombs Seal - Triple Spike Crushers", "Catacombs Seal - Crusher Gauntlet",
                     "Catacombs Seal - Dirty Pond", "Claustro", "Acro", "Bamboo Creek Seal - Spike Crushers and Doors",
                     "Bamboo Creek Seal - Spike Ball Pits", "Bamboo Creek Seal - Spike Crushers and Doors v2",
                     "Howling Grotto Seal - Crushing Pits", "Howling Grotto Seal - Windy Saws and Balls",
                     "Demon King Crown", "Cloud Ruins Seal - Ghost Pit", "Cloud Ruins Seal - Toothbrush Alley",
                     "Cloud Ruins Seal - Saw Pit", "Cloud Ruins Seal - Money Farm Room",
                     "Tower of Time Seal - Lantern Climb", "Tower of Time Seal - Arcane Orbs",
                     "Underworld Seal - Sharp and Windy Climb", "Underworld Seal - Fireball Wave",
                     "Elemental Skylands Seal - Air", "Forlorn Temple Seal - Rocket Maze",
                     "Forlorn Temple Seal - Rocket Sunset", "Power Thistle", "Key of Strength",
                     "Glacial Peak Seal - Projectile Spike Pit", "Glacial Peak Seal - Glacial Air Swag",
                     "Fairy Bottle", "Riviere Turquoise Seal - Flower Power", "Searing Crags Seal - Triple Ball Spinner",
                     "Searing Crags Seal - Raining Rocks", "Searing Crags Seal - Rhythm Rocks", "Astral Seed",
                     "Astral Tea Leaves", "Rescue Phantom", "Autumn Hills Mega Shard", "Hidden Entrance Mega Shard",
                     "Sunny Day Mega Shard", "Down Under Mega Shard", "Catacombs Mega Shard",
                     "Above Entrance Mega Shard", "Abandoned Mega Shard", "Time Loop Mega Shard",
                     "Searing Crags Mega Shard", "Glacial Peak Mega Shard", "Cloud Entrance Mega Shard",
                     "Time Warp Mega Shard", "Money Farm Room Mega Shard 1", "Money Farm Room Mega Shard 2",
                     "Quick Restock Mega Shard 1", "Quick Restock Mega Shard 2", "Earth Mega Shard", "Water Mega Shard",
                     "Leaf Golem", "Ruxxtin", "Emerald Golem"]
        items = [["Wingsuit", "Rope Dart"]]
        self.assertAccessDependency(locations, items)

    def testAmulet(self) -> None:
        """Locations that require Ruxxtin's Amulet"""
        locations = ["Acro", "Cloud Ruins Seal - Ghost Pit", "Cloud Ruins Seal - Toothbrush Alley",
                     "Cloud Ruins Seal - Saw Pit", "Cloud Ruins Seal - Money Farm Room", "Cloud Entrance Mega Shard",
                     "Time Warp Mega Shard", "Money Farm Room Mega Shard 1", "Money Farm Room Mega Shard 2"]
        # Cloud Ruins requires Ruxxtin's Amulet
        items = [["Ruxxtin's Amulet"]]
        self.assertAccessDependency(locations, items)

    def testBottle(self) -> None:
        """Elemental Skylands and Corrupted Future require the Fairy Bottle"""
        locations = ["Key of Symbiosis", "Elemental Skylands Seal - Air", "Elemental Skylands Seal - Fire",
                     "Elemental Skylands Seal - Water", "Key of Courage", "Earth Mega Shard", "Water Mega Shard"]
        items = [["Fairy Bottle"]]
        self.assertAccessDependency(locations, items)

    def testCrests(self) -> None:
        """Test Key of Love nonsense"""
        locations = ["Key of Love"]
        items = [["Sun Crest", "Moon Crest"]]
        self.assertAccessDependency(locations, items)
        self.collect_all_but("Sun Crest")
        self.assertEqual(self.can_reach_location("Key of Love"), False)
        self.remove(self.get_item_by_name("Moon Crest"))
        self.collect_by_name("Sun Crest")
        self.assertEqual(self.can_reach_location("Key of Love"), False)

    def testThistle(self) -> None:
        """I'm a chuckster!"""
        locations = ["Key of Strength"]
        items = [["Power Thistle"]]
        self.assertAccessDependency(locations, items)

    def testCrown(self) -> None:
        """Crocomire but not"""
        locations = ["Key of Courage"]
        items = [["Demon King Crown"]]
        self.assertAccessDependency(locations, items)

    def testGoal(self) -> None:
        """Test some different states to verify goal requires the correct items"""
        self.collect_all_but([*NOTES, "Rescue Phantom"])
        self.assertEqual(self.can_reach_location("Rescue Phantom"), False)
        self.collect_all_but(["Key of Love", "Rescue Phantom"])
        self.assertBeatable(False)
        self.collect_by_name(["Key of Love"])
        self.assertEqual(self.can_reach_location("Rescue Phantom"), True)
        self.assertBeatable(True)


class ItemsAccessTest(MessengerTestBase):
    options = {
        "shuffle_seals": "false",
        "accessibility": "items",
    }

    def testSelfLockingItems(self) -> None:
        """Force items that can be self locked to ensure it's valid placement."""
        location_lock_pairs = {
            "Key of Strength": ["Power Thistle"],
            "Key of Love": ["Sun Crest", "Moon Crest"],
            "Key of Courage": ["Demon King Crown"],
            "Acro": ["Ruxxtin's Amulet"],
            "Demon King Crown": PHOBEKINS
        }

        for loc in location_lock_pairs:
            for item_name in location_lock_pairs[loc]:
                item = self.get_item_by_name(item_name)
                with self.subTest("Fulfills Accessibility", location=loc, item=item_name):
                    self.assertTrue(self.multiworld.get_location(loc, self.player).can_fill(self.multiworld.state, item, True))

