from . import CrossCodeTestBase

overworld_area_unlocks = [
    "Green Leaf Shade",
    "Blue Ice Shade",
    "Red Flame Shade",
    "Green Seed Shade",
    "Star Shade",
    "Meteor Shade",
]

dungeon_unlocks = [
    "Mine Pass",
    "Yellow Sand Shade",
    "Purple Bolt Shade",
    "Azure Drop Shade",
]

class TestProgressive(CrossCodeTestBase):
    item_amounts: dict[str, int] = {}

    def test_items_are_progressive(self):
        for name, amount in self.item_amounts.items():
            local_overworld_area_unlocks = self.get_items_by_name_with_precollected(name)
            self.assertEqual(amount, len(local_overworld_area_unlocks))

class TestProgressiveAreasOverworld(TestProgressive):
    options = { "progressive_area_unlocks": "overworld" }
    item_amounts = {
        "Progressive Overworld Area Unlock": len(overworld_area_unlocks),
        "Progressive Dungeon Unlock": 0,
        "Progressive Area Unlock": 0,
    }

class TestProgressiveAreasOverworldNoShadeStart(TestProgressiveAreasOverworld):
    options = { "progressive_area_unlocks": "overworld", "start_with_green_leaf_shade": False }

class TestProgressiveAreasDungeon(TestProgressive):
    options = { "progressive_area_unlocks": "dungeons" }
    item_amounts = {
        "Progressive Overworld Area Unlock": 0,
        "Progressive Dungeon Unlock": len(dungeon_unlocks),
        "Progressive Area Unlock": 0,
    }

class TestProgressiveAreasSplit(TestProgressive):
    options = { "progressive_area_unlocks": "split" }
    item_amounts = {
        "Progressive Overworld Area Unlock": len(overworld_area_unlocks),
        "Progressive Dungeon Unlock": len(dungeon_unlocks),
        "Progressive Area Unlock": 0,
    }

class TestProgressiveAreasCombined(TestProgressive):
    options = { "progressive_area_unlocks": "combined" }
    item_amounts = {
        "Progressive Overworld Area Unlock": 0,
        "Progressive Dungeon Unlock": 0,
        "Progressive Area Unlock": len(overworld_area_unlocks) + len(dungeon_unlocks),
    }
