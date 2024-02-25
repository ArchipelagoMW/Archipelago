import unittest

from worlds import AutoWorldRegister
from Options import Choice, NamedRange, Toggle, Range


class TestOptionPresets(unittest.TestCase):
    def test_option_presets_have_valid_options(self):
        """Test that all predefined option presets are valid options."""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            presets = world_type.web.options_presets
            for preset_name, preset in presets.items():
                for option_name, option_value in preset.items():
                    with self.subTest(game=game_name, preset=preset_name, option=option_name):
                        try:
                            option = world_type.options_dataclass.type_hints[option_name].from_any(option_value)
                            supported_types = [Choice, Toggle, Range, NamedRange]
                            if not any([issubclass(option.__class__, t) for t in supported_types]):
                                self.fail(f"'{option_name}' in preset '{preset_name}' for game '{game_name}' "
                                          f"is not a supported type for webhost. "
                                          f"Supported types: {', '.join([t.__name__ for t in supported_types])}")
                        except AssertionError as ex:
                            self.fail(f"Option '{option_name}': '{option_value}' in preset '{preset_name}' for game "
                                      f"'{game_name}' is not valid. Error: {ex}")
                        except KeyError as ex:
                            self.fail(f"Option '{option_name}' in preset '{preset_name}' for game '{game_name}' is "
                                      f"not a defined option. Error: {ex}")

    def test_option_preset_values_are_explicitly_defined(self):
        """Test that option preset values are not a special flavor of 'random' or use from_text to resolve another
        value.
        """
        for game_name, world_type in AutoWorldRegister.world_types.items():
            presets = world_type.web.options_presets
            for preset_name, preset in presets.items():
                for option_name, option_value in preset.items():
                    with self.subTest(game=game_name, preset=preset_name, option=option_name):
                        # Check for non-standard random values.
                        self.assertFalse(
                            str(option_value).startswith("random-"),
                            f"'{option_name}': '{option_value}' in preset '{preset_name}' for game '{game_name}' "
                            f"is not supported for webhost. Special random values are not supported for presets."
                        )

                        option = world_type.options_dataclass.type_hints[option_name].from_any(option_value)

                        # Check for from_text resolving to a different value. ("random" is allowed though.)
                        if option_value != "random" and isinstance(option_value, str):
                            # Allow special named values for NamedRange option presets.
                            if isinstance(option, NamedRange):
                                self.assertTrue(
                                    option_value in option.special_range_names,
                                    f"Invalid preset '{option_name}': '{option_value}' in preset '{preset_name}' "
                                    f"for game '{game_name}'. Expected {option.special_range_names.keys()} or "
                                    f"{option.range_start}-{option.range_end}."
                                )
                            else:
                                self.assertTrue(
                                    option.name_lookup.get(option.value, None) == option_value,
                                    f"'{option_name}': '{option_value}' in preset '{preset_name}' for game "
                                    f"'{game_name}' is not supported for webhost. Values must not be resolved to a "
                                    f"different option via option.from_text (or an alias)."
                                )
