import unittest
from worlds.AutoWorld import AutoWorldRegister
from . import setup_solo_multiworld


class TestNames(unittest.TestCase):
    def assertIsStr(self, v: str, extra_msg: str | None = None):
        """Helper for asserting the type of a value is exactly str, with a more helpful failure message."""
        # The default message would only print the type of the value, but printing the value itself can be helpful in
        # tracking down where the non-str type has come from.
        msg = f"Expected plain str type, but got '{v}' of type '{type(v)}'"
        # Add an extra message to the end if one is provided.
        if extra_msg:
            msg += f" - {extra_msg}"
        self.assertIs(type(v), str, msg)

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
                    for location_group_name, names_in_group in world_type.location_name_groups.items():
                        self.assertIsStr(location_group_name)
                        for name in names_in_group:
                            self.assertIsStr(name, f"Location name within location group '{location_group_name}'")
                with self.subTest("item_name_groups"):
                    for item_group_name, names_in_group in world_type.item_name_groups.items():
                        self.assertIsStr(item_group_name)
                        for name in names_in_group:
                            self.assertIsStr(name, f"Item name within item group '{item_group_name}'")

                multiworld = setup_solo_multiworld(world_type)

                with self.subTest("non-event locations"):
                    for location in multiworld.get_locations():
                        if not location.is_event:
                            self.assertIsStr(location.name)
                with self.subTest("event locations"):
                    for location in multiworld.get_locations():
                        if location.is_event:
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
                with self.subTest("non-event items placed in pre_fill and earlier"):
                    for loc in multiworld.get_filled_locations():
                        item = loc.item
                        assert item is not None
                        if not item.is_event:
                            self.assertIsStr(item.name)
                with self.subTest("event items placed in pre_fill and earlier"):
                    for loc in multiworld.get_filled_locations():
                        item = loc.item
                        assert item is not None
                        if item.is_event:
                            self.assertIsStr(item.name)

    def test_location_name_format(self) -> None:
        """Location names must not be all numeric in order to differentiate between ID and name in !hint_location"""
        for gamename, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game=gamename):
                for location_name in world_type.location_name_to_id:
                    self.assertFalse(location_name.isnumeric(),
                                     f"Location name \"{location_name}\" is invalid. It must not be numeric.")
