import unittest
from argparse import Namespace
from typing import Type

from BaseClasses import CollectionState, MultiWorld
from Fill import distribute_items_restrictive
from Options import ItemLinks
from worlds.AutoWorld import AutoWorldRegister, World, call_all
from . import setup_solo_multiworld


class TestBase(unittest.TestCase):
    def test_create_item(self):
        """Test that a world can successfully create all items in its datapackage"""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            multiworld = setup_solo_multiworld(world_type, steps=("generate_early", "create_regions", "create_items"))
            proxy_world = multiworld.worlds[1]
            for item_name in world_type.item_name_to_id:
                test_state = CollectionState(multiworld)
                with self.subTest("Create Item", item_name=item_name, game_name=game_name):
                    item = proxy_world.create_item(item_name)

                with self.subTest("Item Name", item_name=item_name, game_name=game_name):
                    self.assertEqual(item.name, item_name)

                if item.advancement:
                    with self.subTest("Item State Collect", item_name=item_name, game_name=game_name):
                        test_state.collect(item, True)

                    with self.subTest("Item State Remove", item_name=item_name, game_name=game_name):
                        test_state.remove(item)

                        self.assertEqual(test_state.prog_items, multiworld.state.prog_items,
                                         "Item Collect -> Remove should restore empty state.")
                else:
                    with self.subTest("Item State Collect No Change", item_name=item_name, game_name=game_name):
                        # Non-Advancement should not modify state.
                        test_state.collect(item)
                        self.assertEqual(test_state.prog_items, multiworld.state.prog_items)

    def test_item_name_group_has_valid_item(self):
        """Test that all item name groups contain valid items. """
        # This cannot test for Event names that you may have declared for logic, only sendable Items.
        # In such a case, you can add your entries to this Exclusion dict. Game Name -> Group Names
        exclusion_dict = {
            "A Link to the Past":
                {"Pendants", "Crystals"},
            "Ocarina of Time":
                {"medallions", "stones", "rewards", "logic_bottles"},
            "Starcraft 2":
                {"Missions", "WoL Missions"},
            "Yu-Gi-Oh! 2006":
                {"Campaign Boss Beaten"}
        }
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game_name, game_name=game_name):
                exclusions = exclusion_dict.get(game_name, frozenset())
                for group_name, items in world_type.item_name_groups.items():
                    if group_name not in exclusions:
                        with self.subTest(group_name, group_name=group_name):
                            for item in items:
                                self.assertIn(item, world_type.item_name_to_id)

    def test_item_name_group_conflict(self):
        """Test that all item name groups aren't also item names."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game_name, game_name=game_name):
                for group_name in world_type.item_name_groups:
                    with self.subTest(group_name, group_name=group_name):
                        self.assertNotIn(group_name, world_type.item_name_to_id)

    def test_item_count_equal_locations(self):
        """Test that by the pre_fill step under default settings, each game submits items == locations"""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest("Game", game=game_name):
                multiworld = setup_solo_multiworld(world_type)
                self.assertEqual(
                    len(multiworld.itempool),
                    len(multiworld.get_unfilled_locations()),
                    f"{game_name} Item count MUST match the number of locations",
                )

    def test_items_in_datapackage(self):
        """Test that any created items in the itempool are in the datapackage"""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest("Game", game=game_name):
                multiworld = setup_solo_multiworld(world_type)
                for item in multiworld.itempool:
                    self.assertIn(item.name, world_type.item_name_to_id)
    
    def test_item_links(self) -> None:
        """
        Tests item link creation by creating a multiworld of 2 worlds for every game and linking their items together.
        """
        def setup_link_multiworld(world: Type[World], link_replace: bool) -> None:
            multiworld = MultiWorld(2)
            multiworld.game = {1: world.game, 2: world.game}
            multiworld.player_name = {1: "Linker 1", 2: "Linker 2"}
            multiworld.set_seed()
            item_link_group = [{
                "name": "ItemLinkTest",
                "item_pool": ["Everything"],
                "link_replacement": link_replace,
                "replacement_item": None,
            }]
            args = Namespace()
            for name, option in world.options_dataclass.type_hints.items():
                setattr(args, name, {1: option.from_any(option.default), 2: option.from_any(option.default)})
            setattr(args, "item_links",
                    {1: ItemLinks.from_any(item_link_group), 2: ItemLinks.from_any(item_link_group)})
            multiworld.set_options(args)
            multiworld.set_item_links()
            # groups get added to state during its constructor so this has to be after item links are set
            multiworld.state = CollectionState(multiworld)
            gen_steps = ("generate_early", "create_regions", "create_items", "set_rules", "connect_entrances", "generate_basic")
            for step in gen_steps:
                call_all(multiworld, step)
            # link the items together and attempt to fill
            multiworld.link_items()
            multiworld._all_state = None
            call_all(multiworld, "pre_fill")
            distribute_items_restrictive(multiworld)
            call_all(multiworld, "post_fill")
            self.assertTrue(multiworld.can_beat_game(CollectionState(multiworld)), f"seed = {multiworld.seed}")

        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest("Can generate with link replacement", game=game_name):
                setup_link_multiworld(world_type, True)
            with self.subTest("Can generate without link replacement", game=game_name):
                setup_link_multiworld(world_type, False)

    def test_itempool_not_modified(self):
        """Test that worlds don't modify the itempool after `create_items`"""
        gen_steps = ("generate_early", "create_regions", "create_items")
        additional_steps = ("set_rules", "connect_entrances", "generate_basic", "pre_fill")
        excluded_games = ("Links Awakening DX", "Ocarina of Time", "SMZ3")
        worlds_to_test = {game: world
                          for game, world in AutoWorldRegister.world_types.items() if game not in excluded_games}
        for game_name, world_type in worlds_to_test.items():
            with self.subTest("Game", game=game_name):
                multiworld = setup_solo_multiworld(world_type, gen_steps)
                created_items = multiworld.itempool.copy()
                for step in additional_steps:
                    with self.subTest("step", step=step):
                        call_all(multiworld, step)
                        self.assertEqual(created_items, multiworld.itempool,
                                         f"{game_name} modified the itempool during {step}")

    def test_locality_not_modified(self):
        """Test that worlds don't modify the locality of items after duplicates are resolved"""
        gen_steps = ("generate_early", "create_regions", "create_items")
        additional_steps = ("set_rules", "connect_entrances", "generate_basic", "pre_fill")
        worlds_to_test = {game: world for game, world in AutoWorldRegister.world_types.items()}
        for game_name, world_type in worlds_to_test.items():
            with self.subTest("Game", game=game_name):
                multiworld = setup_solo_multiworld(world_type, gen_steps)
                local_items = multiworld.worlds[1].options.local_items.value.copy()
                non_local_items = multiworld.worlds[1].options.non_local_items.value.copy()
                for step in additional_steps:
                    with self.subTest("step", step=step):
                        call_all(multiworld, step)
                        self.assertEqual(local_items, multiworld.worlds[1].options.local_items.value,
                                         f"{game_name} modified local_items during {step}")
                        self.assertEqual(non_local_items, multiworld.worlds[1].options.non_local_items.value,
                                         f"{game_name} modified non_local_items during {step}")
