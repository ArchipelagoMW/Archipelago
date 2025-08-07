import unittest
from worlds.AutoWorld import AutoWorldRegister, call_all, World
from . import setup_solo_multiworld


class TestBase(unittest.TestCase):
    def test_entrance_connection_steps(self):
        """Tests that Entrances are connected and not changed after connect_entrances."""
        def get_entrance_name_to_source_and_target_dict(world: World):
            return [
                (entrance.name, entrance.parent_region, entrance.connected_region)
                for entrance in world.get_entrances()
            ]

        gen_steps = ("generate_early", "create_regions", "create_items", "set_rules", "connect_entrances")
        additional_steps = ("generate_basic", "pre_fill")

        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest("Game", game_name=game_name):
                multiworld = setup_solo_multiworld(world_type, gen_steps)

                original_entrances = get_entrance_name_to_source_and_target_dict(multiworld.worlds[1])

                self.assertTrue(
                    all(entrance[1] is not None and entrance[2] is not None for entrance in original_entrances),
                    f"{game_name} had unconnected entrances after connect_entrances"
                )

                for step in additional_steps:
                    with self.subTest("Step", step=step):
                        call_all(multiworld, step)
                        step_entrances = get_entrance_name_to_source_and_target_dict(multiworld.worlds[1])

                        self.assertEqual(
                            original_entrances, step_entrances, f"{game_name} modified entrances during {step}"
                        )

    def test_all_state_before_connect_entrances(self):
        """Before connect_entrances, Entrance objects may be unconnected.
        Thus, we test that get_all_state is performed with allow_partial_entrances if used before or during
        connect_entrances."""

        gen_steps = ("generate_early", "create_regions", "create_items", "set_rules", "connect_entrances")

        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest("Game", game_name=game_name):
                multiworld = setup_solo_multiworld(world_type, ())

                original_get_all_state = multiworld.get_all_state

                def patched_get_all_state(use_cache: bool | None = None, allow_partial_entrances: bool = False,
                                          **kwargs):
                    self.assertTrue(allow_partial_entrances, (
                        "Before the connect_entrances step finishes, other worlds might still have partial entrances. "
                        "As such, any call to get_all_state must use allow_partial_entrances = True."
                    ))

                    return original_get_all_state(use_cache, allow_partial_entrances, **kwargs)

                multiworld.get_all_state = patched_get_all_state

                for step in gen_steps:
                    with self.subTest("Step", step=step):
                        call_all(multiworld, step)
