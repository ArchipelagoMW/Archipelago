import unittest
from worlds.AutoWorld import AutoWorldRegister, call_all, World
from . import setup_solo_multiworld


class TestBase(unittest.TestCase):
    def test_entrance_connection_steps(self):
        """Tests that Regions and Locations aren't created after `create_items`."""
        def get_entrance_name_to_source_and_target_dict(world: World):
            return [
                (entrance.name, entrance.parent_region.name, entrance.target.name)
                for entrance in world.get_entrances()
            ]


        gen_steps = ("generate_early", "create_regions", "create_items", "set_rules", "connect_entrances")
        additional_steps = ("generate_basic", "pre_fill")

        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest("Game", game_name=game_name):
                multiworld = setup_solo_multiworld(world_type, gen_steps)

                original_entrances = get_entrance_name_to_source_and_target_dict()

                for step in additional_steps:
                    with self.subTest("Step", step=step):
                        call_all(multiworld, "steps")
                        entrances_after_step = get_entrance_name_to_source_and_target_dict
                        self.assertEqual(
                            original_entrances, entrances_after_step, f"{game_name} modified entrances during {step}"
                        )
