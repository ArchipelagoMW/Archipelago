import unittest
from itertools import combinations
from typing import ClassVar

from BaseClasses import get_seed
from test.param import classvar_matrix
from ..assertion import WorldAssertMixin, ModAssertMixin
from ..bases import skip_long_tests, SVTestCase, solo_multiworld
from ..options.option_names import all_option_choices
from ... import options
from ...mods.mod_data import ModNames
from ...options.options import all_mods


@unittest.skip
class TestTroubleshootMods(WorldAssertMixin, ModAssertMixin, SVTestCase):
    def test_troubleshoot_option(self):
        seed = get_seed(78709133382876990000)

        world_options = {
            options.EntranceRandomization: options.EntranceRandomization.option_buildings,
            options.Mods: ModNames.sve
        }

        with self.solo_world_sub_test(world_options=world_options, seed=seed, world_caching=False) as (multiworld, _):
            self.assert_basic_checks(multiworld)
            self.assert_stray_mod_items(world_options[options.Mods], multiworld)


if skip_long_tests():
    raise unittest.SkipTest("Long tests disabled")


@classvar_matrix(mod_pair=combinations(sorted(all_mods), 2))
class TestGenerateModsPairs(WorldAssertMixin, ModAssertMixin, SVTestCase):
    mod_pair: ClassVar[tuple[str, str]]

    def test_given_mod_pairs_when_generate_then_basic_checks(self):
        world_options = {
            options.Mods.internal_name: frozenset(self.mod_pair)
        }

        with solo_multiworld(world_options, world_caching=False) as (multiworld, _):
            self.assert_basic_checks(multiworld)
            self.assert_stray_mod_items(list(self.mod_pair), multiworld)


@classvar_matrix(mod=all_mods, option_and_choice=all_option_choices)
class TestGenerateModAndOptionChoice(WorldAssertMixin, ModAssertMixin, SVTestCase):
    mod: ClassVar[str]
    option_and_choice: ClassVar[tuple[str, str]]

    def test_given_mod_names_when_generate_paired_with_other_options_then_basic_checks(self):
        option, choice = self.option_and_choice

        world_options = {
            option: choice,
            options.Mods.internal_name: self.mod
        }

        with solo_multiworld(world_options, world_caching=False) as (multiworld, _):
            self.assert_basic_checks(multiworld)
            self.assert_stray_mod_items(self.mod, multiworld)


@classvar_matrix(goal=options.Goal.options.keys(), option_and_choice=all_option_choices)
class TestGenerateAllGoalAndAllOptionWithAllModsWithoutQuest(WorldAssertMixin, ModAssertMixin, SVTestCase):
    goal = ClassVar[str]
    option_and_choice = ClassVar[tuple[str, str]]

    def test_given_no_quest_all_mods_when_generate_with_all_goals_then_basic_checks(self):
        option, choice = self.option_and_choice
        if option == options.QuestLocations.internal_name:
            self.skipTest("QuestLocations are disabled")

        world_options = {
            options.Goal.internal_name: self.goal,
            option: choice,
            options.QuestLocations.internal_name: -1,
            options.Mods.internal_name: frozenset(options.Mods.valid_keys),
        }

        with solo_multiworld(world_options, world_caching=False) as (multiworld, _):
            self.assert_basic_checks(multiworld)
