import unittest

from Fill import distribute_items_restrictive
from NetUtils import encode
from worlds.AutoWorld import AutoWorldRegister, call_all
from . import setup_solo_multiworld


class TestImplemented(unittest.TestCase):
    def test_completion_condition(self):
        """Ensure a completion condition is set that has requirements."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden and game_name not in {"Sudoku"}:
                with self.subTest(game_name):
                    multiworld = setup_solo_multiworld(world_type)
                    self.assertFalse(multiworld.completion_condition[1](multiworld.state))

    def test_entrance_parents(self):
        """Tests that the parents of created Entrances match the exiting Region."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden:
                with self.subTest(game_name):
                    multiworld = setup_solo_multiworld(world_type)
                    for region in multiworld.regions:
                        for exit in region.exits:
                            self.assertEqual(exit.parent_region, region)

    def test_stage_methods(self):
        """Tests that worlds don't try to implement certain steps that are only ever called as stage."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden:
                with self.subTest(game_name):
                    for method in ("assert_generate",):
                        self.assertFalse(hasattr(world_type, method),
                                         f"{method} must be implemented as a @classmethod named stage_{method}.")

    def test_slot_data(self):
        """Tests that if a world creates slot data, it's json serializable."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            # has an await for generate_output which isn't being called
            if game_name in {"Ocarina of Time", "Zillion"}:
                continue
            multiworld = setup_solo_multiworld(world_type)
            with self.subTest(game=game_name, seed=multiworld.seed):
                distribute_items_restrictive(multiworld)
                call_all(multiworld, "post_fill")
                for key, data in multiworld.worlds[1].fill_slot_data().items():
                    self.assertIsInstance(key, str, "keys in slot data must be a string")
                    self.assertIsInstance(encode(data), str, f"object {type(data).__name__} not serializable.")

    def test_world_determinism(self):
        """Tests that the state of a generated multiworld is the same per world."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game=game_name):
                multi_one = setup_solo_multiworld(world_type, seed=0)
                multi_two = setup_solo_multiworld(world_type, seed=0)
                self.assertEqual(multi_one.random.randrange(99999), multi_two.random.randrange(99999))
                for region_name in multi_one.regions.region_cache:
                    self.assertIn(region_name, multi_two.regions.region_cache)
                    self.assertEqual(list(multi_one.regions.region_cache.keys()).index(region_name),
                                     list(multi_two.regions.region_cache.keys()).index(region_name),
                                     "regions were created in a separate order")
                for entrance_name in multi_one.regions.entrance_cache:
                    self.assertIn(region_name, multi_two.regions.entrance_cache)
                    self.assertEqual(list(multi_one.regions.entrance_cache.keys()).index(entrance_name),
                                     list(multi_two.regions.entrance_cache.keys()).index(entrance_name),
                                     "entrances were created in a different order")
                for location_name in multi_one.regions.location_cache:
                    self.assertIn(region_name, multi_two.regions.location_cache)
                    self.assertEqual(list(multi_one.regions.location_cache.keys()).index(location_name),
                                     list(multi_two.regions.location_cache.keys()).index(location_name),
                                     "locations were created in a different order")
                for multi_one_loc in multi_one.get_filled_locations():
                    multi_two_loc = multi_two.get_location(multi_one_loc.name, 1)
                    self.assertEqual(multi_one_loc.item, multi_two_loc.item,
                                     f"{multi_one_loc} has a different item placed on it between seeds: "
                                     f"{multi_one_loc.item}, {multi_two_loc.item}")
                self.assertEqual(multi_one.itempool, multi_two.itempool)
