import unittest

from ..options.utils import fill_dataclass_with_default
from ... import create_content, options
from ...regions.entrance_rando import create_player_randomization_flag
from ...regions.model import RandomizationFlag, ConnectionData


class TestConnectionData(unittest.TestCase):

    def test_given_entrances_not_randomized_when_is_eligible_for_randomization_then_not_eligible(self):
        player_flag = RandomizationFlag.NOT_RANDOMIZED

        connection = ConnectionData("Go to Somewhere", "Somewhere", RandomizationFlag.PELICAN_TOWN)
        is_eligible = connection.is_eligible_for_randomization(player_flag)

        self.assertFalse(is_eligible)

    def test_given_pelican_town_connection_when_is_eligible_for_pelican_town_randomization_then_eligible(self):
        player_flag = RandomizationFlag.BIT_PELICAN_TOWN
        connection = ConnectionData("Go to Somewhere", "Somewhere", RandomizationFlag.PELICAN_TOWN)

        is_eligible = connection.is_eligible_for_randomization(player_flag)

        self.assertTrue(is_eligible)

    def test_given_pelican_town_connection_when_is_eligible_for_buildings_randomization_then_eligible(self):
        player_flag = RandomizationFlag.BIT_BUILDINGS
        connection = ConnectionData("Go to Somewhere", "Somewhere", RandomizationFlag.PELICAN_TOWN)

        is_eligible = connection.is_eligible_for_randomization(player_flag)

        self.assertTrue(is_eligible)

    def test_given_non_progression_connection_when_is_eligible_for_pelican_town_randomization_then_not_eligible(self):
        player_flag = RandomizationFlag.BIT_PELICAN_TOWN
        connection = ConnectionData("Go to Somewhere", "Somewhere", RandomizationFlag.NON_PROGRESSION)

        is_eligible = connection.is_eligible_for_randomization(player_flag)

        self.assertFalse(is_eligible)

    def test_given_non_progression_masteries_connection_when_is_eligible_for_non_progression_randomization_then_eligible(self):
        player_flag = RandomizationFlag.BIT_NON_PROGRESSION
        connection = ConnectionData("Go to Somewhere", "Somewhere", RandomizationFlag.NON_PROGRESSION ^ RandomizationFlag.EXCLUDE_MASTERIES)

        is_eligible = connection.is_eligible_for_randomization(player_flag)

        self.assertTrue(is_eligible)

    def test_given_non_progression_masteries_connection_when_is_eligible_for_non_progression_without_masteries_randomization_then_not_eligible(self):
        player_flag = RandomizationFlag.BIT_NON_PROGRESSION | RandomizationFlag.EXCLUDE_MASTERIES
        connection = ConnectionData("Go to Somewhere", "Somewhere", RandomizationFlag.NON_PROGRESSION ^ RandomizationFlag.EXCLUDE_MASTERIES)

        is_eligible = connection.is_eligible_for_randomization(player_flag)

        self.assertFalse(is_eligible)


class TestRandomizationFlag(unittest.TestCase):

    def test_given_entrance_randomization_choice_when_create_player_randomization_flag_then_only_relevant_bit_is_enabled(self):
        for entrance_randomization_choice, expected_bit in (
                (options.EntranceRandomization.option_disabled, RandomizationFlag.NOT_RANDOMIZED),
                (options.EntranceRandomization.option_pelican_town, RandomizationFlag.BIT_PELICAN_TOWN),
                (options.EntranceRandomization.option_non_progression, RandomizationFlag.BIT_NON_PROGRESSION),
                (options.EntranceRandomization.option_buildings_without_house, RandomizationFlag.BIT_BUILDINGS),
                (options.EntranceRandomization.option_buildings, RandomizationFlag.BIT_BUILDINGS),
                (options.EntranceRandomization.option_chaos, RandomizationFlag.BIT_BUILDINGS),
        ):
            player_options = fill_dataclass_with_default({options.EntranceRandomization: entrance_randomization_choice})
            content = create_content(player_options)

            flag = create_player_randomization_flag(player_options.entrance_randomization, content)

            self.assertEqual(flag, expected_bit)

    def test_given_masteries_not_randomized_when_create_player_randomization_flag_then_exclude_masteries_bit_enabled(self):
        for entrance_randomization_choice in set(options.EntranceRandomization.options.values()) ^ {options.EntranceRandomization.option_disabled}:
            player_options = fill_dataclass_with_default({
                options.EntranceRandomization: entrance_randomization_choice,
                options.SkillProgression: options.SkillProgression.option_progressive
            })
            content = create_content(player_options)

            flag = create_player_randomization_flag(player_options.entrance_randomization, content)

            self.assertIn(RandomizationFlag.EXCLUDE_MASTERIES, flag)
