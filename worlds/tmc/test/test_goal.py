from worlds.tmc.test import MinishCapTestBase
from worlds.tmc.options import Goal


class TestVaati(MinishCapTestBase):
    options = {
        "goal": Goal.option_vaati,
        "shuffle_elements": True,
        "dungeon_small_keys": True,
        "dungeon_big_keys": True,
    }

    def test_goal_vaati(self) -> None:
        """Test some different states to verify goal requires the correct items"""
        self.collect_by_name(["Small Key (DHC)", "Big Key (DHC)"])
        self.assertEqual(self.can_reach_location("DHC B1 Big Chest"), False)
        self.collect_by_name(["Earth Element", "Fire Element", "Water Element", "Wind Element", "Progressive Sword"])
        self.assertEqual(self.can_reach_location("DHC B1 Big Chest"), True)
        self.assertBeatable(False)
        self.collect_by_name(["Gust Jar", "Progressive Bow", "Cane of Pacci", "Lantern", "Bomb Bag", "Spin Attack"])
        self.assertBeatable(True)


class TestPedestalElements(MinishCapTestBase):
    options = {
        "goal": Goal.option_pedestal,
        "shuffle_elements": True,
        "ped_swords": 0
    }

    def test_goal_ped_elements(self) -> None:
        """Test whether Pedestal is only accessible once all elements are obtained"""
        self.collect_by_name(["Earth Element", "Fire Element", "Water Element"])
        self.assertBeatable(False)
        self.collect_by_name("Wind Element")
        self.assertBeatable(True)
