import unittest
from worlds.AutoWorld import AutoWorldRegister
from . import setup_default_world


class TestBase(unittest.TestCase):
    def testCreateItem(self):
        for game_name, world_type in AutoWorldRegister.world_types.items():
            proxy_world = world_type(None, 0)  # this is identical to MultiServer.py creating worlds
            for item_name in world_type.item_name_to_id:
                with self.subTest("Create Item", item_name=item_name, game_name=game_name):
                    item = proxy_world.create_item(item_name)
                    self.assertEqual(item.name, item_name)

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

            if game_name in {"Final Fantasy"}:
                continue
            with self.subTest("Game", game=game_name):
                world = setup_default_world(world_type)
                location_count = sum(0 if location.event or location.item else 1 for location in world.get_locations())
                self.assertGreaterEqual(
                    len(world.itempool),
                    location_count,
                    f"{game_name} Item count MUST meet or exceede the number of locations",
                )
