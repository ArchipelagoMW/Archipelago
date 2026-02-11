from types import MappingProxyType

from worlds.tmc.constants import TMCItem, TMCLocation
from worlds.tmc.options import Goal
from worlds.tmc.test import MinishCapTestBase


class TestVaati(MinishCapTestBase):
    options = MappingProxyType(
        {
            "goal": Goal.option_vaati,
            "shuffle_elements": True,
            "dungeon_small_keys": True,
            "dungeon_big_keys": True,
        }
    )

    def test_goal_vaati(self) -> None:
        """Test some different states to verify goal requires the correct items"""
        self.collect_by_name([TMCItem.SMALL_KEY_DHC, TMCItem.BIG_KEY_DHC])
        self.assertEqual(self.can_reach_location(TMCLocation.DHC_B1_BIG_CHEST), False)
        self.collect_by_name(
            [
                TMCItem.EARTH_ELEMENT,
                TMCItem.FIRE_ELEMENT,
                TMCItem.WATER_ELEMENT,
                TMCItem.WIND_ELEMENT,
                TMCItem.PROGRESSIVE_SWORD,
            ]
        )
        self.assertEqual(self.can_reach_location(TMCLocation.DHC_B1_BIG_CHEST), True)
        self.assertBeatable(False)
        self.collect_by_name(
            [
                TMCItem.GUST_JAR,
                TMCItem.PROGRESSIVE_BOW,
                TMCItem.CANE_OF_PACCI,
                TMCItem.LANTERN,
                TMCItem.BOMB_BAG,
                TMCItem.PROGRESSIVE_SCROLL,
            ]
        )
        self.assertBeatable(True)


class TestPedestalElements(MinishCapTestBase):
    options = MappingProxyType({"goal": Goal.option_pedestal, "shuffle_elements": True, "ped_swords": 0})

    def test_goal_ped_elements(self) -> None:
        """Test whether Pedestal is only accessible once all elements are obtained"""
        self.collect_by_name(["Earth Element", "Fire Element", "Water Element"])
        self.assertBeatable(False)
        self.collect_by_name("Wind Element")
        self.assertBeatable(True)
