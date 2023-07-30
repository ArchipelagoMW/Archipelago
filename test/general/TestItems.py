import unittest
from worlds.AutoWorld import AutoWorldRegister
from . import setup_solo_multiworld


class TestBase(unittest.TestCase):
    def testItem(self):
        for game_name, world_type in AutoWorldRegister.world_types.items():
            multiworld = setup_solo_multiworld(world_type)
            proxy_world = multiworld.worlds[1]
            empty_prog_items = multiworld.state.prog_items.copy()
            for item_name in world_type.item_name_to_id:
                with self.subTest("Create Item", item_name=item_name, game_name=game_name):
                    item = proxy_world.create_item(item_name)

                with self.subTest("Item Name", item_name=item_name, game_name=game_name):
                    self.assertEqual(item.name, item_name)

                if item.advancement:
                    with self.subTest("Item State Collect", item_name=item_name, game_name=game_name):
                        multiworld.state.collect(item, True)

                    with self.subTest("Item State Remove", item_name=item_name, game_name=game_name):
                        multiworld.state.remove(item)

                        self.assertEqual(multiworld.state.prog_items, empty_prog_items,
                                         "Item Collect -> Remove should restore empty state.")
                else:
                    with self.subTest("Item State Collect No Change", item_name=item_name, game_name=game_name):
                        # Non-Advancement should not modify state.
                        base_state = multiworld.state.prog_items.copy()
                        multiworld.state.collect(item)
                        self.assertEqual(base_state, multiworld.state.prog_items)

                multiworld.state.prog_items = empty_prog_items

    def testItemNameGroupHasValidItem(self):
        """Test that all item name groups contain valid items. """
        # This cannot test for Event names that you may have declared for logic, only sendable Items.
        # In such a case, you can add your entries to this Exclusion dict. Game Name -> Group Names
        exclusion_dict = {
            "A Link to the Past":
                {"Pendants", "Crystals"},
            "Ocarina of Time":
                {"medallions", "stones", "rewards", "logic_bottles"},
            "Starcraft 2 Wings of Liberty":
                {"Missions"},
        }
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game_name, game_name=game_name):
                exclusions = exclusion_dict.get(game_name, frozenset())
                for group_name, items in world_type.item_name_groups.items():
                    if group_name not in exclusions:
                        with self.subTest(group_name, group_name=group_name):
                            for item in items:
                                self.assertIn(item, world_type.item_name_to_id)

    def testItemNameGroupConflict(self):
        """Test that all item name groups aren't also item names."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game_name, game_name=game_name):
                for group_name in world_type.item_name_groups:
                    with self.subTest(group_name, group_name=group_name):
                        self.assertNotIn(group_name, world_type.item_name_to_id)

    def testItemCountGreaterEqualLocations(self):
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest("Game", game=game_name):
                multiworld = setup_solo_multiworld(world_type)
                self.assertGreaterEqual(
                    len(multiworld.itempool),
                    len(multiworld.get_unfilled_locations()),
                    f"{game_name} Item count MUST meet or exceed the number of locations",
                )

    def testItemsInDatapackage(self):
        """Test that any created items in the itempool are in the datapackage"""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest("Game", game=game_name):
                multiworld = setup_solo_multiworld(world_type)
                for item in multiworld.itempool:
                    self.assertIn(item.name, world_type.item_name_to_id)
