from . import LADXTestBase

from ..Items import ItemName

class TestD6(LADXTestBase):
    # Force keys into pool for testing
    options = {
        "shuffle_small_keys": "any_world"
    }

    def test_keylogic(self):
        keys = self.get_items_by_name(ItemName.KEY6)
        self.collect_by_name([ItemName.FACE_KEY, ItemName.HOOKSHOT, ItemName.POWER_BRACELET, ItemName.BOMB, ItemName.FEATHER, ItemName.FLIPPERS])
        # Can reach an un-keylocked item in the dungeon
        self.assertTrue(self.can_reach_location("L2 Bracelet Chest (Face Shrine)"))

        # For each location, add a key and check that the right thing unlocks
        location_1 = "Tile Room Key (Face Shrine)"
        location_2 = "Top Right Horse Heads Chest (Face Shrine)"
        location_3 = "Pot Locked Chest (Face Shrine)"
        self.assertFalse(self.can_reach_location(location_1))
        self.assertFalse(self.can_reach_location(location_2))
        self.assertFalse(self.can_reach_location(location_3))
        self.collect(keys[0])
        self.assertTrue(self.can_reach_location(location_1))
        self.assertFalse(self.can_reach_location(location_2))
        self.assertFalse(self.can_reach_location(location_3))
        self.collect(keys[1])
        self.assertTrue(self.can_reach_location(location_1))
        self.assertTrue(self.can_reach_location(location_2))
        self.assertFalse(self.can_reach_location(location_3))
        self.collect(keys[2])
        self.assertTrue(self.can_reach_location(location_1))
        self.assertTrue(self.can_reach_location(location_2))
        self.assertTrue(self.can_reach_location(location_3))
