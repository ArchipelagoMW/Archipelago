import unittest
from argparse import Namespace
from typing import Type

from BaseClasses import CollectionState, MultiWorld, Region
from Fill import distribute_items_restrictive
from Options import ItemLinks
from worlds.AutoWorld import AutoWorldRegister, World, call_all
from . import setup_solo_multiworld


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
    
    def testItemLinks(self) -> None:
        """
        Tests item link creation by creating a multiworld of 2 worlds for every game and linking their items together.
        """
        def setup_link_multiworld(world_type: Type[World]) -> MultiWorld:
            multiworld = MultiWorld(2)
            multiworld.game = {1: world_type.game, 2: world_type.game}
            multiworld.player_name = {1: "Linker 1", 2: "Linker 2"}
            multiworld.set_seed()
            item_link_group = [{
                "name": "ItemLinkTest",
                "item_pool": ["Everything"],
                "link_replacement": True,
                "replacement_item": None,
            }]
            args = Namespace()
            for name, option in world_type.option_definitions.items():
                setattr(args, name, {1: option.from_any(option.default), 2: option.from_any(option.default)})
            multiworld.set_options(args)
            multiworld.set_default_common_options()
            setattr(multiworld, "item_links",
                    {1: ItemLinks.from_any(item_link_group), 2: ItemLinks.from_any(item_link_group)})
            multiworld.set_item_links()
            # groups get added to state during its constructor so this has to be after item links are set
            multiworld.state = CollectionState(multiworld)
            gen_steps = ("generate_early", "create_regions", "create_items", "set_rules", "generate_basic")
            for step in gen_steps:
                call_all(multiworld, step)
            return multiworld
        
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest("Game", game=game_name):
                multiworld = setup_link_multiworld(world_type)
                # link the items together and attempt to fill
                multiworld.link_items()
                multiworld._recache()
                multiworld._all_state = None
                call_all(multiworld, "pre_fill")
                distribute_items_restrictive(multiworld)
                call_all(multiworld, "post_fill")
