import builtins
import inspect

from Options import PerGameCommonOptions, OptionSet
from . import SVTestCase
from .. import sv_options_presets, StardewValleyOptions


class TestPresets(SVTestCase):
    def test_all_presets_explicitly_set_all_options(self):
        all_option_names = {option_key for option_key in StardewValleyOptions.type_hints}
        omitted_option_names = {option_key for option_key in PerGameCommonOptions.type_hints}
        mandatory_option_names = {option_key for option_key in all_option_names
                                  if option_key not in omitted_option_names and
                                  not issubclass(StardewValleyOptions.type_hints[option_key], OptionSet)}

        for preset_name in sv_options_presets:
            with self.subTest(f"{preset_name}"):
                for option_name in mandatory_option_names:
                    with self.subTest(f"{preset_name} -> {option_name}"):
                        self.assertIn(option_name, sv_options_presets[preset_name])