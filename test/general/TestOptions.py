import unittest
from worlds.AutoWorld import AutoWorldRegister


class TestOptions(unittest.TestCase):
    def testOptionsHaveDocString(self):
        for gamename, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden:
                for option_key, option in world_type.option_definitions.items():
                    with self.subTest(game=gamename, option=option_key):
                        self.assertTrue(option.__doc__)
