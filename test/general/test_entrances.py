import unittest
from worlds.AutoWorld import AutoWorldRegister, call_all
from . import setup_solo_multiworld


class TestBase(unittest.TestCase):
    def test_entrance_connection_steps(self):
        """Tests that Regions and Locations aren't created after `create_items`."""
        gen_steps = ("generate_early", "create_regions", "create_items", "set_rules", "connect_entrances")
        additional_steps = ("generate_basic", "pre_fill")

        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest("Game", game_name=game_name):
                multiworld = setup_solo_multiworld(world_type, gen_steps)

                entrances = multiworld.get_entrances()

                for step in additional_steps:
                    with self.subTest("Step", step=step):
                        call_all(multiworld, "steps")
                        self.assertEqual(
                            entrances,
                            multiworld.get_entrances(),
                            f"{game_name} modified entrances during {step}"
                        )
