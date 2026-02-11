from collections import Counter
from types import MappingProxyType

from worlds.tmc.constants import TMCItem
from worlds.tmc.options import DungeonWarp, PedReward
from worlds.tmc.test import MinishCapTestBase

DUNGEON_KEYS = {
    TMCItem.SMALL_KEY_DWS: 4,
    TMCItem.BIG_KEY_DWS: 1,
    TMCItem.SMALL_KEY_COF: 2,
    TMCItem.BIG_KEY_COF: 1,
    TMCItem.SMALL_KEY_FOW: 4,
    TMCItem.BIG_KEY_FOW: 1,
    TMCItem.SMALL_KEY_TOD: 4,
    TMCItem.BIG_KEY_TOD: 1,
    TMCItem.SMALL_KEY_RC: 3,
    TMCItem.SMALL_KEY_POW: 6,
    TMCItem.BIG_KEY_POW: 1,
    TMCItem.SMALL_KEY_DHC: 5,
    TMCItem.BIG_KEY_DHC: 1,
}

PROGRESSIVES = {
    TMCItem.PROGRESSIVE_SWORD: 5,
    TMCItem.PROGRESSIVE_SCROLL: 5,
    TMCItem.PROGRESSIVE_BOW: 2,
    TMCItem.PROGRESSIVE_BOOMERANG: 2,
    TMCItem.PROGRESSIVE_SHIELD: 2,
}

NON_PROGRESSIVES = {
    TMCItem.SMITHS_SWORD: 1,
    TMCItem.WHITE_SWORD_GREEN: 1,
    TMCItem.WHITE_SWORD_RED: 1,
    TMCItem.WHITE_SWORD_BLUE: 1,
    TMCItem.FOUR_SWORD: 1,
    TMCItem.BOW: 1,
    TMCItem.LIGHT_ARROW: 1,
    TMCItem.BOOMERANG: 1,
    TMCItem.MAGIC_BOOMERANG: 1,
    TMCItem.SHIELD: 1,
    TMCItem.MIRROR_SHIELD: 1,
    TMCItem.SPIN_ATTACK: 1,
    TMCItem.GREATSPIN: 1,
    TMCItem.FAST_SPIN_SCROLL: 1,
    TMCItem.FAST_SPLIT_SCROLL: 1,
    TMCItem.LONG_SPIN: 1,
}

ADVENTURE_ITEMS = {
    TMCItem.BOMB_BAG: 4,
    TMCItem.REMOTE_BOMB: 1,
    TMCItem.LANTERN: 1,
    TMCItem.GUST_JAR: 1,
    TMCItem.CANE_OF_PACCI: 1,
    TMCItem.MOLE_MITTS: 1,
    TMCItem.ROCS_CAPE: 1,
    TMCItem.PEGASUS_BOOTS: 1,
    TMCItem.OCARINA: 1,
    TMCItem.EMPTY_BOTTLE: 4,
    TMCItem.GRIP_RING: 1,
    TMCItem.POWER_BRACELETS: 1,
    TMCItem.FLIPPERS: 1,
    TMCItem.ROLL_ATTACK: 1,
    TMCItem.DASH_ATTACK: 1,
    TMCItem.ROCK_BREAKER: 1,
    TMCItem.SWORD_BEAM: 1,
    TMCItem.DOWNTHRUST: 1,
    TMCItem.PERIL_BEAM: 1,
}


class TestBasicPool(MinishCapTestBase):
    def test_keys(self) -> None:
        """Test whether there are the expected number of dungeon keys in the pool"""
        self.assertDictEqual(DUNGEON_KEYS, dictionary_count(DUNGEON_KEYS, self.multiworld.get_items()))

    def test_adventure_items(self) -> None:
        """Test whether there are the expected number of inventory items (excluding quests)"""
        items = self.multiworld.get_items()
        self.assertDictEqual(ADVENTURE_ITEMS, dictionary_count(ADVENTURE_ITEMS, items))
        np = {item: 0 for item, _ in NON_PROGRESSIVES.items()}
        self.assertDictEqual(np, dictionary_count(np, items))


class TestFigurinesLess(MinishCapTestBase):
    options = MappingProxyType(
        {
            "ped_figurines": 10,
            "figurine_amount": 5,
        }
    )

    def test_figurines(self) -> None:
        """Figurines (the mcguffin) should have exactly as much as figurine amount unless ped_figurines is higher"""
        figurines = {TMCItem.FIGURINE: 10}
        self.assertDictEqual(figurines, dictionary_count(figurines, self.multiworld.get_items()))


class TestFigurinesMore(MinishCapTestBase):
    options = MappingProxyType(
        {
            "ped_figurines": 10,
            "figurine_amount": 20,
        }
    )

    def test_figurines(self) -> None:
        """Figurines (the mcguffin) should have exactly as much as figurine amount unless ped_figurines is higher"""
        figurines = {TMCItem.FIGURINE: 20}
        self.assertDictEqual(figurines, dictionary_count(figurines, self.multiworld.get_items()))


class TestComplicatedKeys(MinishCapTestBase):
    options = MappingProxyType(
        {"ped_reward": PedReward.option_dhc_big_key, "dungeon_warp_tod": DungeonWarp.option_both}
    )

    def test_keys(self) -> None:
        """Test whether there are the expected number of dungeon keys in the pool"""
        self.assertDictEqual(DUNGEON_KEYS, dictionary_count(DUNGEON_KEYS, self.multiworld.get_items()))


class TestNonProgressives(MinishCapTestBase):
    options = MappingProxyType(
        {
            "progressive_sword": False,
            "progressive_bow": False,
            "progressive_boomerang": False,
            "progressive_shield": False,
            "progressive_scroll": False,
        }
    )

    def test_adventure_items(self) -> None:
        """Test whether there are the expected number of inventory items (excluding quests)"""
        items = self.multiworld.get_items()
        self.assertDictEqual(ADVENTURE_ITEMS, dictionary_count(ADVENTURE_ITEMS, items))
        p = {item: 0 for item, _ in PROGRESSIVES.items()}
        self.assertDictEqual(p, dictionary_count(p, items))


def dictionary_count(counts: dict[str, int], items: list[str]):
    occurrences = Counter(item.name for item in items)
    return {item_name: occurrences.get(item_name, 0) for item_name in counts.keys()}
