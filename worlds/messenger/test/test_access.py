from . import MessengerTestBase
from ..constants import NOTES, PHOBEKINS


class AccessTest(MessengerTestBase):
    options = {
        "shuffle_shards": "true",
    }

    def test_tabi(self) -> None:
        """locations that hard require the Lightfoot Tabi"""
        locations = [
            "Searing Crags - Pyro", "Underworld - Key of Chaos", "Underworld Seal - Sharp and Windy Climb",
            "Underworld Seal - Spike Wall", "Underworld Seal - Fireball Wave", "Underworld Seal - Rising Fanta",
            "Sunken Shrine - Sun Crest", "Sunken Shrine - Moon Crest", "Sunken Shrine Seal - Waterfall Paradise",
            "Sunken Shrine Seal - Tabi Gauntlet", "Mega Shard of the Moon", "Mega Shard of the Sun",
            "Under Entrance Mega Shard", "Hot Tub Mega Shard", "Projectile Pit Mega Shard"
        ]
        items = [["Lightfoot Tabi"]]
        self.assertAccessDependency(locations, items)

    def test_dart(self) -> None:
        """locations that hard require the Rope Dart"""
        locations = [
            "Ninja Village Seal - Tree House", "Autumn Hills - Key of Hope", "Howling Grotto Seal - Crushing Pits",
            "Glacial Peak Seal - Ice Climbers", "Tower of Time Seal - Time Waster", "Tower of Time Seal - Lantern Climb",
            "Tower of Time Seal - Arcane Orbs", "Cloud Ruins Seal - Ghost Pit", "Underworld Seal - Rising Fanta",
            "Elemental Skylands - Key of Symbiosis", "Elemental Skylands Seal - Water",
            "Elemental Skylands Seal - Fire", "Earth Mega Shard", "Water Mega Shard", "Rescue Phantom",
        ]
        items = [["Rope Dart"]]
        self.assertAccessDependency(locations, items)

    def test_wingsuit(self) -> None:
        """locations that hard require the Wingsuit"""
        locations = [
            "Ninja Village - Candle", "Ninja Village Seal - Tree House", "Autumn Hills - Climbing Claws",
            "Autumn Hills - Key of Hope", "Autumn Hills Seal - Trip Saws", "Autumn Hills Seal - Double Swing Saws",
            "Autumn Hills Seal - Spike Ball Swing", "Autumn Hills Seal - Spike Ball Darts", "Catacombs - Necro",
            "Catacombs - Ruxxtin's Amulet", "Catacombs Seal - Triple Spike Crushers",
            "Catacombs Seal - Crusher Gauntlet", "Catacombs Seal - Dirty Pond", "Bamboo Creek - Claustro",
            "Cloud Ruins - Acro", "Bamboo Creek Seal - Spike Crushers and Doors", "Bamboo Creek Seal - Spike Ball Pits",
            "Bamboo Creek Seal - Spike Crushers and Doors v2", "Howling Grotto Seal - Crushing Pits",
            "Howling Grotto Seal - Windy Saws and Balls", "Tower of Time Seal - Lantern Climb",
            "Forlorn Temple - Demon King", "Cloud Ruins Seal - Ghost Pit", "Cloud Ruins Seal - Toothbrush Alley",
            "Cloud Ruins Seal - Saw Pit", "Cloud Ruins Seal - Money Farm Room", "Tower of Time Seal - Lantern Climb",
            "Tower of Time Seal - Arcane Orbs", "Underworld Seal - Sharp and Windy Climb",
            "Underworld Seal - Fireball Wave", "Elemental Skylands Seal - Air", "Elemental Skylands Seal - Water",
            "Elemental Skylands Seal - Fire", "Elemental Skylands - Key of Symbiosis",
            "Forlorn Temple Seal - Rocket Maze", "Forlorn Temple Seal - Rocket Sunset", "Ninja Village - Astral Seed",
            "Searing Crags - Astral Tea Leaves", "Autumn Hills Mega Shard", "Hidden Entrance Mega Shard",
            "Sunny Day Mega Shard", "Down Under Mega Shard", "Catacombs Mega Shard", "Above Entrance Mega Shard",
            "Abandoned Mega Shard", "Time Loop Mega Shard", "Earth Mega Shard", "Water Mega Shard",
            "Money Farm Room Mega Shard 1", "Money Farm Room Mega Shard 2",
            "Autumn Hills - Leaf Golem", "Catacombs - Ruxxtin", "Howling Grotto - Emerald Golem"
        ]
        items = [["Wingsuit"]]
        self.assertAccessDependency(locations, items)

    def test_vertical(self) -> None:
        """locations that require either the Rope Dart or the Wingsuit"""
        locations = [
            "Ninja Village Seal - Tree House", "Howling Grotto Seal - Crushing Pits",
            "Glacial Peak Seal - Ice Climbers", "Tower of Time Seal - Time Waster",
            "Underworld Seal - Rising Fanta", "Elemental Skylands - Key of Symbiosis",
            "Elemental Skylands Seal - Water", "Elemental Skylands Seal - Fire", "Ninja Village - Candle",
            "Autumn Hills - Climbing Claws", "Autumn Hills - Key of Hope", "Autumn Hills Seal - Trip Saws",
            "Autumn Hills Seal - Double Swing Saws", "Autumn Hills Seal - Spike Ball Swing",
            "Autumn Hills Seal - Spike Ball Darts", "Catacombs - Necro", "Catacombs - Ruxxtin's Amulet",
            "Catacombs Seal - Triple Spike Crushers", "Catacombs Seal - Crusher Gauntlet",
            "Catacombs Seal - Dirty Pond", "Bamboo Creek - Claustro", "Cloud Ruins - Acro",
            "Bamboo Creek Seal - Spike Crushers and Doors", "Bamboo Creek Seal - Spike Ball Pits",
            "Bamboo Creek Seal - Spike Crushers and Doors v2", "Howling Grotto Seal - Crushing Pits",
            "Howling Grotto Seal - Windy Saws and Balls", "Forlorn Temple - Demon King", "Cloud Ruins Seal - Ghost Pit",
            "Cloud Ruins Seal - Toothbrush Alley", "Cloud Ruins Seal - Saw Pit", "Cloud Ruins Seal - Money Farm Room",
            "Tower of Time Seal - Lantern Climb", "Tower of Time Seal - Arcane Orbs",
            "Underworld Seal - Sharp and Windy Climb", "Underworld Seal - Fireball Wave",
            "Elemental Skylands Seal - Air", "Forlorn Temple Seal - Rocket Maze", "Forlorn Temple Seal - Rocket Sunset",
            "Searing Crags - Power Thistle", "Searing Crags - Key of Strength",
            "Glacial Peak Seal - Projectile Spike Pit", "Glacial Peak Seal - Glacial Air Swag",
            "Riviere Turquoise - Butterfly Matriarch", "Riviere Turquoise Seal - Flower Power",
            "Riviere Turquoise Seal - Launch of Faith",
            "Searing Crags Seal - Triple Ball Spinner", "Searing Crags Seal - Raining Rocks",
            "Searing Crags Seal - Rhythm Rocks", "Ninja Village - Astral Seed", "Searing Crags - Astral Tea Leaves",
            "Rescue Phantom", "Autumn Hills Mega Shard", "Hidden Entrance Mega Shard", "Sunny Day Mega Shard",
            "Down Under Mega Shard", "Catacombs Mega Shard", "Above Entrance Mega Shard", "Abandoned Mega Shard",
            "Time Loop Mega Shard", "Searing Crags Mega Shard", "Glacial Peak Mega Shard", "Cloud Entrance Mega Shard",
            "Time Warp Mega Shard", "Money Farm Room Mega Shard 1", "Money Farm Room Mega Shard 2",
            "Quick Restock Mega Shard 1", "Quick Restock Mega Shard 2", "Earth Mega Shard", "Water Mega Shard",
            "Autumn Hills - Leaf Golem", "Catacombs - Ruxxtin", "Howling Grotto - Emerald Golem"
        ]
        items = [["Wingsuit", "Rope Dart"]]
        self.assertAccessDependency(locations, items)

    def test_amulet(self) -> None:
        """Locations that require Ruxxtin's Amulet"""
        locations = [
            "Cloud Ruins - Acro", "Cloud Ruins Seal - Ghost Pit", "Cloud Ruins Seal - Toothbrush Alley",
            "Cloud Ruins Seal - Saw Pit", "Cloud Ruins Seal - Money Farm Room", "Cloud Entrance Mega Shard",
            "Time Warp Mega Shard", "Money Farm Room Mega Shard 1", "Money Farm Room Mega Shard 2"
        ]
        # Cloud Ruins requires Ruxxtin's Amulet
        items = [["Ruxxtin's Amulet"]]
        self.assertAccessDependency(locations, items)

    def test_firefly(self) -> None:
        """Elemental Skylands and Corrupted Future require the Magic Firefly"""
        locations = [
            "Elemental Skylands - Key of Symbiosis", "Elemental Skylands Seal - Air", "Elemental Skylands Seal - Fire",
            "Elemental Skylands Seal - Water", "Corrupted Future - Key of Courage", "Earth Mega Shard",
            "Water Mega Shard"
        ]
        items = [["Magic Firefly"]]
        self.assertAccessDependency(locations, items)

    def test_crests(self) -> None:
        """Test Key of Love nonsense"""
        locations = ["Sunken Shrine - Key of Love"]
        items = [["Sun Crest", "Moon Crest"]]
        self.assertAccessDependency(locations, items)
        self.collect_all_but("Sun Crest")
        self.assertEqual(self.can_reach_location("Sunken Shrine - Key of Love"), False)
        self.remove(self.get_item_by_name("Moon Crest"))
        self.collect_by_name("Sun Crest")
        self.assertEqual(self.can_reach_location("Sunken Shrine - Key of Love"), False)

    def test_thistle(self) -> None:
        """I'm a chuckster!"""
        locations = ["Searing Crags - Key of Strength"]
        items = [["Power Thistle"]]
        self.assertAccessDependency(locations, items)

    def test_crown(self) -> None:
        """Crocomire but not"""
        locations = ["Corrupted Future - Key of Courage"]
        items = [["Demon King Crown"]]
        self.assertAccessDependency(locations, items)

    def test_goal(self) -> None:
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

    def test_self_locking_items(self) -> None:
        """Force items that can be self locked to ensure it's valid placement."""
        location_lock_pairs = {
            "Searing Crags - Key of Strength": ["Power Thistle"],
            "Sunken Shrine - Key of Love": ["Sun Crest", "Moon Crest"],
            "Corrupted Future - Key of Courage": ["Demon King Crown"],
            "Cloud Ruins - Acro": ["Ruxxtin's Amulet"],
            "Forlorn Temple - Demon King": PHOBEKINS
        }

        self.multiworld.state = self.multiworld.get_all_state(True)
        self.remove_by_name(location_lock_pairs.values())
        for loc in location_lock_pairs:
            for item_name in location_lock_pairs[loc]:
                item = self.get_item_by_name(item_name)
                with self.subTest("Fulfills Accessibility", location=loc, item=item_name):
                    self.assertTrue(self.multiworld.get_location(loc, self.player).can_fill(self.multiworld.state, item, True))
