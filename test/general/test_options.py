import unittest
from worlds.AutoWorld import AutoWorldRegister


class TestOptions(unittest.TestCase):
    def test_options_have_doc_string(self):
        """Test that submitted options have their own specified docstring"""
        for gamename, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden:
                for option_key, option in world_type.options_dataclass.type_hints.items():
                    with self.subTest(game=gamename, option=option_key):
                        self.assertTrue(option.__doc__)
