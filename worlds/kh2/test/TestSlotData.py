import unittest

from test.general import setup_solo_multiworld
from . import KH2TestBase
from .. import KH2World, all_locations, item_dictionary_table, CheckDupingItems, AllWeaponSlot, KH2Item
from ..Names import ItemName
from ... import AutoWorldRegister
from ...AutoWorld import call_all


class TestLocalItems(KH2TestBase):

    def testSlotData(self):
        gen_steps = ("generate_early", "create_regions", "create_items", "set_rules", "generate_basic", "pre_fill")
        multiworld = setup_solo_multiworld(KH2World, gen_steps)
        for location in multiworld.get_locations():
            if location.item is None:
                location.place_locked_item(multiworld.worlds[1].create_item(ItemName.NoExperience))
        call_all(multiworld, "fill_slot_data")
        slotdata = multiworld.worlds[1].fill_slot_data()
        assert len(slotdata["LocalItems"]) > 0, f"{slotdata['LocalItems']} is empty"
