from unittest import TestCase

from worlds.AutoWorld import AutoWorldRegister


class TestNameGroups(TestCase):
    def test_item_name_groups_not_empty(self) -> None:
        """
        Test that there are no empty item name groups, which is likely a bug.
        """
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.item_id_to_name:
                continue  # ignore worlds without items
            with self.subTest(game=game_name):
                for name, group in world_type.item_name_groups.items():
                    self.assertTrue(group, f"Item name group \"{name}\" of \"{game_name}\" is empty")

    def test_location_name_groups_not_empty(self) -> None:
        """
        Test that there are no empty location name groups, which is likely a bug.
        """
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.location_id_to_name:
                continue  # ignore worlds without locations
            with self.subTest(game=game_name):
                for name, group in world_type.location_name_groups.items():
                    self.assertTrue(group, f"Location name group \"{name}\" of \"{game_name}\" is empty")
