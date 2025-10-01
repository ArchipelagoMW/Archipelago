import unittest

from Fill import distribute_items_restrictive
from NetUtils import convert_to_base_types
from worlds.AutoWorld import AutoWorldRegister, call_all
from worlds import failed_world_loads
from . import setup_solo_multiworld


class TestImplemented(unittest.TestCase):
    def test_completion_condition(self):
        """Ensure a completion condition is set that has requirements."""
        for game_name, testable_world in AutoWorldRegister.testable_worlds.items():
            world_type = testable_world.world_type
            for options_name, options in testable_world.testable_options_by_name.items():
                if not world_type.hidden and game_name not in {"Sudoku"}:
                    with self.subTest(game=game_name, options=options_name):
                        multiworld = setup_solo_multiworld(world_type, options=options)
                        self.assertFalse(multiworld.completion_condition[1](multiworld.state))

    def test_entrance_parents(self):
        """Tests that the parents of created Entrances match the exiting Region."""
        for game_name, testable_world in AutoWorldRegister.testable_worlds.items():
            world_type = testable_world.world_type
            for options_name, options in testable_world.testable_options_by_name.items():
                if not world_type.hidden:
                    with self.subTest(game=game_name, options=options_name):
                        multiworld = setup_solo_multiworld(world_type, options=options)
                        for region in multiworld.regions:
                            for exit in region.exits:
                                self.assertEqual(exit.parent_region, region)

    def test_stage_methods(self):
        """Tests that worlds don't try to implement certain steps that are only ever called as stage."""
        for game_name, testable_world in AutoWorldRegister.testable_worlds.items():
            world_type = testable_world.world_type
            if not world_type.hidden:
                with self.subTest(game_name):
                    for method in ("assert_generate",):
                        self.assertFalse(hasattr(world_type, method),
                                         f"{method} must be implemented as a @classmethod named stage_{method}.")

    def test_slot_data(self):
        """Tests that if a world creates slot data, it's json serializable."""
        # has an await for generate_output which isn't being called
        excluded_games = ("Ocarina of Time",)
        for game_name, testable_world in AutoWorldRegister.testable_worlds.items():
            if game_name in excluded_games:
                continue

            world_type = testable_world.world_type
            for options_name, options in testable_world.testable_options_by_name.items():
                multiworld = setup_solo_multiworld(world_type, options=options)
                with self.subTest(game=game_name, options=options_name, seed=multiworld.seed):
                    distribute_items_restrictive(multiworld)
                    call_all(multiworld, "post_fill")
                    for key, data in multiworld.worlds[1].fill_slot_data().items():
                        self.assertIsInstance(key, str, "keys in slot data must be a string")
                        convert_to_base_types(data)  # only put base data types into slot data

    def test_no_failed_world_loads(self):
        if failed_world_loads:
            self.fail(f"The following worlds failed to load: {failed_world_loads}")

    def test_prefill_items(self):
        """Test that every world can reach every location from allstate before pre_fill."""
        steps = ("generate_early", "create_regions", "create_items", "set_rules", "connect_entrances", "generate_basic")

        for gamename, testable_world in AutoWorldRegister.testable_worlds.items():
            world_type = testable_world.world_type
            if gamename not in ("Archipelago", "Sudoku", "Final Fantasy", "Test Game"):
                for options_name, options in testable_world.testable_options_by_name.items():
                    with self.subTest(game=gamename, options=options_name):
                        multiworld = setup_solo_multiworld(world_type, steps, options=options)
                        allstate = multiworld.get_all_state(False)
                        locations = multiworld.get_locations()
                        reachable = multiworld.get_reachable_locations(allstate)
                        unreachable = [location for location in locations if location not in reachable]

                        self.assertTrue(not unreachable,
                                        f"Locations were not reachable with all state before prefill: "
                                        f"{unreachable}. Seed: {multiworld.seed}")

    def test_explicit_indirect_conditions_spheres(self):
        """Tests that worlds using explicit indirect conditions produce identical spheres as when using implicit
        indirect conditions"""
        # Because the iteration order of blocked_connections in CollectionState.update_reachable_regions() is
        # nondeterministic, this test may sometimes pass with the same seed even when there are missing indirect
        # conditions.
        for game_name, testable_world in AutoWorldRegister.testable_worlds.items():
            world_type = testable_world.world_type
            for options_name, options in testable_world.testable_options_by_name.items():
                multiworld = setup_solo_multiworld(world_type, options=options)
                world = multiworld.get_game_worlds(game_name)[0]
                if not world.explicit_indirect_conditions:
                    # The world does not use explicit indirect conditions, so it can be skipped.
                    continue
                # The world may override explicit_indirect_conditions as a property that cannot be set, so try modifying it.
                try:
                    world.explicit_indirect_conditions = False
                    world.explicit_indirect_conditions = True
                except Exception:
                    # Could not modify the attribute, so skip this world.
                    with self.subTest(
                        game=game_name,
                        options=options_name,
                        skipped="world.explicit_indirect_conditions could not be set"
                    ):
                        continue
                with self.subTest(game=game_name, options=options_name, seed=multiworld.seed):
                    distribute_items_restrictive(multiworld)
                    call_all(multiworld, "post_fill")

                    # Note: `multiworld.get_spheres()` iterates a set of locations, so the order that locations are checked
                    # is nondeterministic and may vary between runs with the same seed.
                    explicit_spheres = list(multiworld.get_spheres())
                    # Disable explicit indirect conditions and produce a second list of spheres.
                    world.explicit_indirect_conditions = False
                    implicit_spheres = list(multiworld.get_spheres())

                    # Both lists should be identical.
                    if explicit_spheres == implicit_spheres:
                        # Test passed.
                        continue

                    # Find the first sphere that was different and provide a useful failure message.
                    zipped = zip(explicit_spheres, implicit_spheres)
                    for sphere_num, (sphere_explicit, sphere_implicit) in enumerate(zipped, start=1):
                        # Each sphere created with explicit indirect conditions should be identical to the sphere created
                        # with implicit indirect conditions.
                        if sphere_explicit != sphere_implicit:
                            reachable_only_with_implicit = sorted(sphere_implicit - sphere_explicit)
                            if reachable_only_with_implicit:
                                locations_and_parents = [(loc, loc.parent_region) for loc in reachable_only_with_implicit]
                                self.fail(f"Sphere {sphere_num} created with explicit indirect conditions did not"
                                          f" contain the same locations as sphere {sphere_num} created with implicit"
                                          f" indirect conditions. There may be missing indirect conditions for"
                                          f" connections to the locations' parent regions or connections from other"
                                          f" regions which connect to these regions."
                                          f"\nLocations that should have been reachable in sphere {sphere_num} and"
                                          f" their parent regions:"
                                          f"\n{locations_and_parents}")
                            else:
                                # Some locations were only present in the sphere created with explicit indirect conditions.
                                # This should not happen because missing indirect conditions should only reduce
                                # accessibility, not increase accessibility.
                                reachable_only_with_explicit = sorted(sphere_explicit - sphere_implicit)
                                self.fail(f"Sphere {sphere_num} created with explicit indirect conditions contained"
                                          f" more locations than sphere {sphere_num} created with implicit indirect"
                                          f" conditions. This should not happen."
                                          f"\nUnexpectedly reachable locations in sphere {sphere_num}:"
                                          f"\n{reachable_only_with_explicit}")
                    self.fail("Unreachable")

    def test_no_items_or_locations_or_regions_submitted_in_init(self):
        """Test that worlds don't submit items/locations/regions to the multiworld in __init__"""
        for game_name, testable_world in AutoWorldRegister.testable_worlds.items():
            world_type = testable_world.world_type
            for options_name, options in testable_world.testable_options_by_name.items():
                with self.subTest("Game", game=game_name, options=options_name):
                    multiworld = setup_solo_multiworld(world_type, (), options=options)
                    self.assertEqual(len(multiworld.itempool), 0)
                    self.assertEqual(len(multiworld.get_locations()), 0)
                    self.assertEqual(len(multiworld.get_regions()), 0)
