from types import MappingProxyType

from worlds.tmc.constants import TMCItem, TMCLocation
from worlds.tmc.test import MinishCapTestBase


class TestSplitProgressiveSword(MinishCapTestBase):

    def test_access_graveyard(self) -> None:
        """Test some different states to verify graveyard can only be reached with certain swords"""
        items = []
        items.extend(self.collect_by_name(TMCItem.BOMB_BAG))
        self.assertEqual(self.can_reach_location(TMCLocation.VALLEY_PRE_VALLEY_FUSION_CHEST), False)
        items.extend(self.collect_by_name(TMCItem.PROGRESSIVE_SWORD))
        self.assertEqual(self.can_reach_location(TMCLocation.VALLEY_PRE_VALLEY_FUSION_CHEST), False)
        items.extend(self.collect_by_name(TMCItem.PROGRESSIVE_SCROLL))
        self.assertEqual(self.can_reach_location(TMCLocation.VALLEY_PRE_VALLEY_FUSION_CHEST), True)
        self.remove_by_name([TMCItem.PROGRESSIVE_SWORD, TMCItem.PROGRESSIVE_SCROLL])


class TestSplitNonProgressiveSword(MinishCapTestBase):
    options = MappingProxyType({
        "progressive_sword": False,
        "progressive_scroll": False
    })

    def test_access_graveyard(self) -> None:
        items = []
        items.extend(self.collect_by_name(TMCItem.BOMB_BAG))
        self.assertEqual(self.can_reach_location(TMCLocation.VALLEY_PRE_VALLEY_FUSION_CHEST), False)
        items.extend(self.collect_by_name(TMCItem.SMITHS_SWORD))
        self.assertEqual(self.can_reach_location(TMCLocation.VALLEY_PRE_VALLEY_FUSION_CHEST), False)
        items.extend(self.collect_by_name(TMCItem.SPIN_ATTACK))
        self.assertEqual(self.can_reach_location(TMCLocation.VALLEY_PRE_VALLEY_FUSION_CHEST), False)
        items.extend(self.collect_by_name(TMCItem.WHITE_SWORD_GREEN))
        self.assertEqual(self.can_reach_location(TMCLocation.VALLEY_PRE_VALLEY_FUSION_CHEST), False)
        items.extend(self.collect_by_name(TMCItem.WHITE_SWORD_RED))
        self.assertEqual(self.can_reach_location(TMCLocation.VALLEY_PRE_VALLEY_FUSION_CHEST), False)
        items.extend(self.collect_by_name(TMCItem.WHITE_SWORD_BLUE))
        self.assertEqual(self.can_reach_location(TMCLocation.VALLEY_PRE_VALLEY_FUSION_CHEST), True)
        self.remove_by_name(TMCItem.WHITE_SWORD_BLUE)
        items.extend(self.collect_by_name(TMCItem.FOUR_SWORD))
        self.assertEqual(self.can_reach_location(TMCLocation.VALLEY_PRE_VALLEY_FUSION_CHEST), True)
        self.remove_by_name(TMCItem.FOUR_SWORD)
        items.extend(self.collect_by_name([TMCItem.GRAVEYARD_KEY, TMCItem.PEGASUS_BOOTS, TMCItem.LANTERN]))
        self.assertEqual(self.can_reach_location(TMCLocation.CRYPT_GIBDO_LEFT_ITEM), False)
        items.extend(self.collect_by_name(TMCItem.FOUR_SWORD))
        self.assertEqual(self.can_reach_location(TMCLocation.CRYPT_GIBDO_LEFT_ITEM), False)
        items.extend(self.collect_by_name(TMCItem.WHITE_SWORD_BLUE))
        self.assertEqual(self.can_reach_location(TMCLocation.CRYPT_GIBDO_LEFT_ITEM), True)
