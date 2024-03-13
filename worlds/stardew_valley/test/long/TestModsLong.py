import unittest
from itertools import combinations, product

from BaseClasses import get_seed
from .option_names import all_option_choices
from .. import SVTestCase
from ..assertion import WorldAssertMixin, ModAssertMixin
from ... import options
from ...mods.mod_data import all_mods, ModNames

assert unittest


class TestGenerateModsOptions(WorldAssertMixin, ModAssertMixin, SVTestCase):

    def test_given_mod_pairs_when_generate_then_basic_checks(self):
        if self.skip_long_tests:
            raise unittest.SkipTest("Long tests disabled")

        for mod_pair in combinations(all_mods, 2):
            world_options = {
                options.Mods: frozenset(mod_pair)
            }

            with self.solo_world_sub_test(f"Mods: {mod_pair}", world_options, world_caching=False) as (multiworld, _):
                self.assert_basic_checks(multiworld)
                self.assert_stray_mod_items(list(mod_pair), multiworld)

    def test_given_mod_names_when_generate_paired_with_other_options_then_basic_checks(self):
        if self.skip_long_tests:
            raise unittest.SkipTest("Long tests disabled")

        for mod, (option, value) in product(all_mods, all_option_choices):
            world_options = {
                option: value,
                options.Mods: mod
            }

            with self.solo_world_sub_test(f"{option.internal_name}: {value}, Mod: {mod}", world_options, world_caching=False) as (multiworld, _):
                self.assert_basic_checks(multiworld)
                self.assert_stray_mod_items(mod, multiworld)

    @unittest.skip
    def test_troubleshoot_option(self):
        seed = get_seed(78709133382876990000)
        # This seed is also broken 61810967650051856921

        world_options = {
            options.EntranceRandomization: options.EntranceRandomization.option_buildings,
            options.Mods: ModNames.sve
        }

        with self.solo_world_sub_test(world_options=world_options, seed=seed, world_caching=False) as (multiworld, _):
            self.assert_basic_checks(multiworld)
            self.assert_stray_mod_items(world_options[options.Mods], multiworld)
