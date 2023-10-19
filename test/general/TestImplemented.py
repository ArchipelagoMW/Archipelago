import json
import unittest

from Fill import distribute_items_restrictive
from worlds.AutoWorld import AutoWorldRegister, call_all
from . import setup_solo_multiworld


class TestImplemented(unittest.TestCase):
    def testCompletionCondition(self):
        """Ensure a completion condition is set that has requirements."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden and game_name not in {"Sudoku"}:
                with self.subTest(game_name):
                    multiworld = setup_solo_multiworld(world_type)
                    self.assertFalse(multiworld.completion_condition[1](multiworld.state))

    def testEntranceParents(self):
        """Tests that the parents of created Entrances match the exiting Region."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden:
                with self.subTest(game_name):
                    multiworld = setup_solo_multiworld(world_type)
                    for region in multiworld.regions:
                        for exit in region.exits:
                            self.assertEqual(exit.parent_region, region)

    def testStageMethods(self):
        """Tests that worlds don't try to implement certain steps that are only ever called as stage."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden:
                with self.subTest(game_name):
                    for method in ("assert_generate",):
                        self.assertFalse(hasattr(world_type, method),
                                         f"{method} must be implemented as a @classmethod named stage_{method}.")

    def testSlotData(self):
        """Tests that if a world creates slot data, it's json serializable."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            # has an await for generate_output which isn't being called
            if game_name in {"Ocarina of Time", "Zillion"}:
                continue
            with self.subTest(game_name):
                print(game_name)
                multiworld = setup_solo_multiworld(world_type)
                distribute_items_restrictive(multiworld)
                call_all(multiworld, "post_fill")
                slot_data = multiworld.worlds[1].fill_slot_data()
                if slot_data:
                    self.assertIsInstance(json.dumps(slot_data), str, slot_data)
