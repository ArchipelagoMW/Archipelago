import unittest
from typing import TYPE_CHECKING

from worlds import AutoWorldRegister

if TYPE_CHECKING:
    from Options import Option


class TestOptionPresets(unittest.TestCase):
    def test_option_presets_have_valid_options(self):
        """Test that all predefined option presets are valid options."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            presets = world_type.web.options_presets
            for preset_name, presets in presets.items():
                with self.subTest(game=game_name, presets=preset_name):
                    for option_name, option_value in presets.items():
                        try:
                            # We don't need to assign the return, as we're only interested if this raises an error.
                            world_type.options_dataclass.type_hints[option_name].from_any(option_value)
                        except AssertionError as ex:
                            self.fail(f"Option '{option_name}': '{option_value}' in preset '{preset_name}' for game "
                                      f"'{game_name}' is not valid. Error: {ex}")
