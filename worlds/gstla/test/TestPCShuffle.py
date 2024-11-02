from . import GSTestBase
from .. import location_type_to_data, LocationType, loc_names_by_id, ItemType, LocationName


class TestVanillaPCShuffle(GSTestBase):
    options = {
        'shuffle_characters': 0
    }

    def test_ensure_vanilla_placement(self):
        world = self.get_world()
        for char in location_type_to_data[LocationType.Character]:
            self.assertEqual(LocationType.Character, char.loc_type)
            name = loc_names_by_id[char.ap_id]
            ap_loc = world.get_location(name)
            ap_item = ap_loc.item
            self.assertEqual(ItemType.Character, ap_item.item_data.type)
            self.assertEqual(ap_loc.location_data.vanilla_contents, ap_item.item_data.id)

class TestPCShuffleInVanilla(GSTestBase):
    options = {
        'shuffle_characters': 1
    }

    def test_ensure_placement_within_vanilla(self):
        world = self.get_world()
        for char in location_type_to_data[LocationType.Character]:
            self.assertEqual(LocationType.Character, char.loc_type)
            name = loc_names_by_id[char.ap_id]
            ap_loc = world.get_location(name)
            ap_item = ap_loc.item
            self.assertEqual(ItemType.Character, ap_item.item_data.type)
            # self.assertEqual(ap_loc.location_data.vanilla_contents, ap_item.item_data.id)

class TestFullPCShuffle(GSTestBase):
    options = {
        'shuffle_characters': 2
    }

    def test_ensure_jenna_is_char(self):
        world = self.get_world()
        jenna_loc = world.get_location(LocationName.Idejima_Jenna)
        self.assertEqual(ItemType.Character, jenna_loc.item.item_data.type)