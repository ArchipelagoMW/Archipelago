from .option_names import options_to_include
from .. import setup_solo_multiworld, SVTestCase
from ..assertion import WorldAssertMixin, ModAssertMixin
from ...mods.mod_data import all_mods
from ...options import Mods


class TestGenerateModsOptions(WorldAssertMixin, ModAssertMixin, SVTestCase):

    def test_given_mod_pairs_when_generate_then_basic_checks(self):
        if self.skip_long_tests:
            return
        mods = list(all_mods)
        num_mods = len(mods)
        for mod1_index in range(0, num_mods):
            for mod2_index in range(mod1_index + 1, num_mods):
                mod1 = mods[mod1_index]
                mod2 = mods[mod2_index]
                mod_pair = (mod1, mod2)
                with self.subTest(f"Mods: {mod_pair}"):
                    multiworld = setup_solo_multiworld({Mods: mod_pair})
                    self.assert_basic_checks(multiworld)
                    self.assert_stray_mod_items(list(mod_pair), multiworld)

    def test_given_mod_names_when_generate_paired_with_other_options_then_basic_checks(self):
        if self.skip_long_tests:
            return
        num_options = len(options_to_include)
        for option_index in range(0, num_options):
            option = options_to_include[option_index]
            if not option.options:
                continue
            for value in option.options:
                for mod in all_mods:
                    with self.subTest(f"{option.internal_name}: {value}, Mod: {mod}"):
                        multiworld = setup_solo_multiworld({option.internal_name: option.options[value], Mods: mod})
                        self.assert_basic_checks(multiworld)
                        self.assert_stray_mod_items(mod, multiworld)
