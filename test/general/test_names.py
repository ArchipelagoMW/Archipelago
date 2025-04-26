import unittest
from worlds.AutoWorld import AutoWorldRegister
from . import setup_solo_multiworld


class TestNames(unittest.TestCase):
    def assertIsStr(self, v: str):
        """Helper for asserting the type of a value is exactly str, with a more helpful failure message."""
        # The default message would only print the type of the value, but printing the value itself can be helpful in
        # tracking down where the non-str type has come from.
        self.assertIs(type(v), str, f"Expected plain str type, but got '{v}' of type '{type(v)}'")

    def test_item_names_format(self) -> None:
        """Item names must not be all numeric in order to differentiate between ID and name in !hint"""
        for gamename, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game=gamename):
                for item_name in world_type.item_name_to_id:
                    self.assertFalse(item_name.isnumeric(),
                                     f"Item name \"{item_name}\" is invalid. It must not be numeric.")

    def test_names_are_plain_str(self) -> None:
        """
        Item/Location/Region/Entrance/Item Group/Location Group/Game names must be a plain `str` type and not a `str`
        subclass because games may put these names into slot_data or write them into patch files.
        """
        for gamename, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game=gamename):
                self.assertIsStr(gamename)

                with self.subTest("item_name_to_id"):
                    for item_name in world_type.item_name_to_id:
                        self.assertIsStr(item_name)
                with self.subTest("location_name_to_id"):
                    for location_name in world_type.location_name_to_id:
                        self.assertIsStr(location_name)
                with self.subTest("location_name_groups"):
                    for location_group_name in world_type.location_name_groups:
                        self.assertIsStr(location_group_name)
                with self.subTest("item_name_groups"):
                    for item_group_name in world_type.item_name_groups:
                        self.assertIsStr(item_group_name)

                multiworld = setup_solo_multiworld(world_type)

                with self.subTest("locations"):
                    for location in multiworld.get_locations():
                        self.assertIsStr(location.name)
                with self.subTest("regions"):
                    for region in multiworld.get_regions():
                        self.assertIsStr(region.name)
                with self.subTest("entrances"):
                    for entrance in multiworld.get_entrances():
                        self.assertIsStr(entrance.name)
                with self.subTest("itempool items"):
                    for item in multiworld.itempool:
                        self.assertIsStr(item.name)
                with self.subTest("precollected_items items"):
                    for item in multiworld.precollected_items[1]:
                        self.assertIsStr(item.name)
                with self.subTest("pre_fill and earlier placed items"):
                    for loc in multiworld.get_filled_locations():
                        self.assertIsStr(loc.item.name)

    def test_location_name_format(self) -> None:
        """Location names must not be all numeric in order to differentiate between ID and name in !hint_location"""
        for gamename, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game=gamename):
                for location_name in world_type.location_name_to_id:
                    self.assertFalse(location_name.isnumeric(),
                                     f"Location name \"{location_name}\" is invalid. It must not be numeric.")
