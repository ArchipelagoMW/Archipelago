import unittest
from worlds.AutoWorld import AutoWorldRegister, Status


class TestNames(unittest.TestCase):
    def test_item_names_format(self):
        """Item names must not be all numeric in order to differentiate between ID and name in !hint"""
        for world_type in AutoWorldRegister.get_testable_world_types():
            with self.subTest(game=world_type.game):
                for item_name in world_type.item_name_to_id:
                    self.assertFalse(item_name.isnumeric(),
                                     f"Item name \"{item_name}\" is invalid. It must not be numeric.")

    def test_location_name_format(self):
        """Location names must not be all numeric in order to differentiate between ID and name in !hint_location"""
        for world_type in AutoWorldRegister.get_testable_world_types():
            with self.subTest(game=world_type.game):
                for location_name in world_type.location_name_to_id:
                    self.assertFalse(location_name.isnumeric(),
                                     f"Location name \"{location_name}\" is invalid. It must not be numeric.")
