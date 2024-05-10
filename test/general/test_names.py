import unittest
from worlds.AutoWorld import AutoWorldRegister


class TestNames(unittest.TestCase):
    def test_item_names_format(self):
        """Item names must not be all numeric in order to differentiate between ID and name in !hint"""
        for gamename, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game=gamename):
                for item_name in world_type.item_name_to_id:
                    self.assertFalse(item_name.isnumeric(),
                                     f"Item name \"{item_name}\" is invalid. It must not be numeric.")

    def test_location_name_format(self):
        """Location names must not be all numeric in order to differentiate between ID and name in !hint_location"""
        for gamename, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game=gamename):
                for location_name in world_type.location_name_to_id:
                    self.assertFalse(location_name.isnumeric(),
                                     f"Location name \"{location_name}\" is invalid. It must not be numeric.")
