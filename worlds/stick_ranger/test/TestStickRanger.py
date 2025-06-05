from test.general import setup_solo_multiworld
from typing import Set, Type

from worlds.AutoWorld import AutoWorldRegister, World

from ..Items import item_table
from ..Locations import (books_table, enemies_table, location_name_to_id,
                         stages_table)
from . import StickRangerTestBase


class StickRangerTest(StickRangerTestBase):
    def test_location_name_uniqueness(self) -> None:
        """Ensure all location names are unique."""
        all_locations: Set[str] = set()
        for loc_table in (stages_table, books_table, enemies_table):
            for entry in loc_table.values():
                name: str = entry["name"]
                self.assertNotIn(name, all_locations, f"Duplicate location name: {name}")
                all_locations.add(name)
        # And check location_name_to_id keys
        for name in location_name_to_id:
            self.assertIn(name, all_locations, f"Location name in location_name_to_id missing from tables: {name}")

    def test_items_classification_and_contiguity(self) -> None:
        """Ensure item codes are unique, positive, and contiguous within expected ranges."""
        codes: Set[int] = set()
        for item in item_table.values():
            self.assertGreater(item.code, 0, f"Item code for {item.item_name} not positive")
            self.assertNotIn(item.code, codes, f"Duplicate item code: {item.code}")
            codes.add(item.code)

    def test_stage_and_book_uniqueness(self) -> None:
        """Ensure stage and book names are unique and do not overlap with each other or enemies."""
        all_names: Set[str] = set(stages_table)
        for name in books_table:
            self.assertNotIn(name, all_names, f"Book location overlaps with stage: {name}")
            all_names.add(name)
        for name in enemies_table:
            self.assertNotIn(name, all_names, f"Enemy location overlaps: {name}")
            all_names.add(name)

    def test_world_registration(self) -> None:
        """Ensure Stick Ranger is registered with AutoWorldRegister."""
        self.assertIn("Stick Ranger", AutoWorldRegister.world_types.keys())

    def test_solo_multiworld(self) -> None:
        """Test generating a solo multiworld instance does not throw and returns expected world object."""
        game_name: str = "Stick Ranger"
        world_type: Type[World] = AutoWorldRegister.world_types[game_name]
        world = setup_solo_multiworld(world_type)
        self.assertIn(1, world.game)
        self.assertEqual(world.game[1], game_name)
        # Optionally: test state and progression
        state = world.get_all_state(False)
        self.assertIsNotNone(state)
