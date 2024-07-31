import unittest
from itertools import combinations, product

from BaseClasses import get_seed
from .option_names import all_option_choices, get_option_choices
from .. import SVTestCase
from ..assertion import WorldAssertMixin, ModAssertMixin
from ... import options
from ...mods.mod_data import ModNames

assert unittest


class TestGenerateModsOptions(WorldAssertMixin, ModAssertMixin, SVTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        if cls.skip_long_tests:
            raise unittest.SkipTest("Long tests disabled")

    def test_given_mod_pairs_when_generate_then_basic_checks(self):
        for mod_pair in combinations(options.Mods.valid_keys, 2):
            world_options = {
                options.Mods: frozenset(mod_pair)
            }

            with self.solo_world_sub_test(f"Mods: {mod_pair}", world_options, world_caching=False) as (multiworld, _):
                self.assert_basic_checks(multiworld)
                self.assert_stray_mod_items(list(mod_pair), multiworld)

    def test_given_mod_names_when_generate_paired_with_other_options_then_basic_checks(self):
        for mod, (option, value) in product(options.Mods.valid_keys, all_option_choices):
            world_options = {
                option: value,
                options.Mods: mod
            }

            with self.solo_world_sub_test(f"{option.internal_name}: {value}, Mod: {mod}", world_options, world_caching=False) as (multiworld, _):
                self.assert_basic_checks(multiworld)
                self.assert_stray_mod_items(mod, multiworld)

    def test_given_no_quest_all_mods_when_generate_with_all_goals_then_basic_checks(self):
        for goal, (option, value) in product(get_option_choices(options.Goal), all_option_choices):
            if option is options.QuestLocations:
                continue

            world_options = {
                options.Goal: goal,
                option: value,
                options.QuestLocations: -1,
                options.Mods: frozenset(options.Mods.valid_keys),
            }

            with self.solo_world_sub_test(f"Goal: {goal}, {option.internal_name}: {value}", world_options, world_caching=False) as (multiworld, _):
                self.assert_basic_checks(multiworld)

    @unittest.skip
    def test_troubleshoot_option(self):
        seed = get_seed(78709133382876990000)

        world_options = {
            options.EntranceRandomization: options.EntranceRandomization.option_buildings,
            options.Mods: ModNames.sve
        }

        with self.solo_world_sub_test(world_options=world_options, seed=seed, world_caching=False) as (multiworld, _):
            self.assert_basic_checks(multiworld)
            self.assert_stray_mod_items(world_options[options.Mods], multiworld)
