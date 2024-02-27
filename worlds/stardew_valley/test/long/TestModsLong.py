from itertools import combinations, product

from .option_names import options_to_include
from .. import SVTestCase
from ..assertion import WorldAssertMixin, ModAssertMixin
from ...mods.mod_data import all_mods
from ...options import Mods


class TestGenerateModsOptions(WorldAssertMixin, ModAssertMixin, SVTestCase):

    def test_given_mod_pairs_when_generate_then_basic_checks(self):
        if self.skip_long_tests:
            return
        for mod_pair in combinations(all_mods, 2):
            world_options = {Mods: mod_pair}
            with self.solo_world_sub_test(f"Mods: {mod_pair}", world_options, world_caching=False) as (multiworld, _):
                self.assert_basic_checks(multiworld)
                self.assert_stray_mod_items(list(mod_pair), multiworld)

    def test_given_mod_names_when_generate_paired_with_other_options_then_basic_checks(self):
        if self.skip_long_tests:
            return
        option_choices = [(option, value)
                          for option in options_to_include
                          if option.options
                          for value in option.options]
        for mod, (option, value) in product(all_mods, option_choices):
            world_options = {
                option.internal_name: option.options[value],
                Mods: mod
            }
            with self.solo_world_sub_test(f"{option.internal_name}: {value}, Mod: {mod}", world_options, world_caching=False) as (multiworld, _):
                self.assert_basic_checks(multiworld)
                self.assert_stray_mod_items(mod, multiworld)
