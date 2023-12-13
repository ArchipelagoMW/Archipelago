import unittest

from worlds.AutoWorld import AutoWorldRegister


class TestWebDescriptions(unittest.TestCase):
    def test_item_descriptions_have_valid_names(self) -> None:
        """Ensure all item descriptions match an item name or item group name"""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            valid_names = world_type.item_names.union(world_type.item_name_groups)
            for name in world_type.web.item_descriptions:
                with self.subTest("Name should be valid", game=game_name, item=name):
                    self.assertIn(name, valid_names,
                                  "All item descriptions must match defined item names")

    def test_location_descriptions_have_valid_names(self) -> None:
        """Ensure all location descriptions match a location name or location group name"""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            valid_names = world_type.location_names.union(world_type.location_name_groups)
            for name in world_type.web.location_descriptions:
                with self.subTest("Name should be valid", game=game_name, location=name):
                    self.assertIn(name, valid_names,
                                  "All location descriptions must match defined location names")
