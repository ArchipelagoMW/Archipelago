from typing import cast

from . import GSTestBase
from .. import location_type_to_data, LocationType, loc_names_by_id, item_id_by_name, GSTLAItem, ItemType, GSTLAOptions


class TestDjinnOptions(GSTestBase):

    def test_ensure_djinn_in_djinn(self):
        world = self.get_world()
        for djinn in location_type_to_data[LocationType.Djinn]:
            self.assertEqual(LocationType.Djinn, djinn.loc_type)
            name = loc_names_by_id[djinn.ap_id]
            ap_loc = world.get_location(name)
            ap_item = ap_loc.item
            self.assertEqual(ItemType.Djinn, ap_item.item_data.type)

class TestVanillaDjinn(GSTestBase):
    options = {
        'shuffle_djinn': 0
    }

    def test_ensure_vanilla_djinn(self):
        world = self.get_world()
        for djinn in location_type_to_data[LocationType.Djinn]:
            self.assertEqual(LocationType.Djinn, djinn.loc_type)
            name = loc_names_by_id[djinn.ap_id]
            ap_loc = world.get_location(name)
            ap_item = ap_loc.item
            self.assertEqual(ItemType.Djinn, ap_item.item_data.type)
            self.assertTrue(name.endswith(ap_item.name), "Loc Name: %s Item Name: %s" % (name, ap_item.name))
