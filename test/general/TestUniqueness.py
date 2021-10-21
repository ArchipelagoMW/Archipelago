import unittest
from BaseClasses import MultiWorld
from worlds.AutoWorld import AutoWorldRegister


class TestBase(unittest.TestCase):
    world: MultiWorld
    _state_cache = {}

    def testUniqueItems(self):
        known_item_ids = set()
        for gamename, world_type in AutoWorldRegister.world_types.items():
            current = len(known_item_ids)
            known_item_ids |= set(world_type.item_id_to_name)
            self.assertEqual(len(known_item_ids) - len(world_type.item_id_to_name), current)

    def testUniqueLocations(self):
        known_location_ids = set()
        for gamename, world_type in AutoWorldRegister.world_types.items():
            current = len(known_location_ids)
            known_location_ids |= set(world_type.location_id_to_name)
            self.assertEqual(len(known_location_ids) - len(world_type.location_id_to_name), current)

