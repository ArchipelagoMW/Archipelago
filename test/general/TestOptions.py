import unittest
from collections import ChainMap

import Options
from worlds.AutoWorld import AutoWorldRegister


class TestOptions(unittest.TestCase):

    def testOptionsHaveDocString(self):
        for gamename, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden:
                for option_key, option in world_type.option_definitions.items():
                    with self.subTest(game=gamename, option=option_key):
                        self.assertTrue(option.__doc__)

    def testOptionsGetChoice(self):
        weights = {
            "progression_balancing":
                {
                    "0": 50,
                    "50":  50,
                    "99": 50,
                },
            "accessibility": 1,  # items
            "start_inventory":
                {
                    "Progressive Sword": 2,
                },
        }

        world_type = AutoWorldRegister.world_types["A Link to the Past"]  # what else
        for option_key, option in ChainMap(Options.common_options, Options.per_game_common_options,
                                           world_type.option_definitions).items():
            result = option.get_choice(weights[option_key]) if option_key in weights else option.from_any(option.default)
            if option_key == "progression_balancing":
                self.assertIn(result.value, {0, 50, 99})
            else:
                expected_result = option.default if option_key not in weights else weights[option_key]
                self.assertEqual(result.value, expected_result)
