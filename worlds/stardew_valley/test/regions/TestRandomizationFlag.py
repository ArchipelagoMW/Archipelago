import unittest
from random import Random

from ... import create_content, options
from ...regions.entrance_rando import create_player_randomization_flag
from ...regions.model import ConnectionData, RandomizationFlag
from ..options.utils import fill_dataclass_with_default


class TestConnectionData(unittest.TestCase):

    def test_given_entrances_not_randomized_when_is_eligible_for_randomization_then_not_eligible(self):
        player_flag = RandomizationFlag.NOT_RANDOMIZED

        connection = ConnectionData("Go to Somewhere", "Somewhere", RandomizationFlag.PELICAN_TOWN)
        is_eligible = connection.is_eligible_for_randomization(player_flag)

        self.assertFalse(is_eligible)

    def test_given_pelican_town_connection_when_is_eligible_for_pelican_town_randomization_then_eligible(self):
        player_flag = RandomizationFlag.SET_PELICAN_TOWN
        connection = ConnectionData("Go to Somewhere", "Somewhere", RandomizationFlag.PELICAN_TOWN)

        is_eligible = connection.is_eligible_for_randomization(player_flag)

        self.assertTrue(is_eligible)

    def test_given_pelican_town_connection_when_is_eligible_for_buildings_randomization_then_eligible(self):
        player_flag = RandomizationFlag.SET_BUILDINGS
        connection = ConnectionData("Go to Somewhere", "Somewhere", RandomizationFlag.PELICAN_TOWN)

        is_eligible = connection.is_eligible_for_randomization(player_flag)

        self.assertTrue(is_eligible)

    def test_given_non_progression_connection_when_is_eligible_for_pelican_town_randomization_then_not_eligible(self):
        player_flag = RandomizationFlag.SET_PELICAN_TOWN
        connection = ConnectionData("Go to Somewhere", "Somewhere", RandomizationFlag.NON_PROGRESSION)

        is_eligible = connection.is_eligible_for_randomization(player_flag)

        self.assertFalse(is_eligible)

    def test_given_non_progression_masteries_connection_when_is_eligible_for_non_progression_randomization_then_eligible(self, ):
        player_flag = RandomizationFlag.SET_NON_PROGRESSION | RandomizationFlag.MASTERY_CAVE
        connection = ConnectionData("Go to Somewhere", "Somewhere", RandomizationFlag.NON_PROGRESSION | RandomizationFlag.MASTERY_CAVE)

        is_eligible = connection.is_eligible_for_randomization(player_flag)

        self.assertTrue(is_eligible)

    def test_given_non_progression_masteries_connection_when_is_eligible_for_non_progression_without_masteries_randomization_then_not_eligible(self, ):
        player_flag = RandomizationFlag.SET_NON_PROGRESSION
        connection = ConnectionData("Go to Somewhere", "Somewhere", RandomizationFlag.NON_PROGRESSION | RandomizationFlag.MASTERY_CAVE)

        is_eligible = connection.is_eligible_for_randomization(player_flag)

        self.assertFalse(is_eligible)


class TestRandomizationFlag(unittest.TestCase):

    def test_given_entrance_randomization_choice_when_create_player_randomization_flag_then_only_relevant_bit_is_enabled(self, ):
        for entrance_randomization_choice, expected_bit in (
                (options.EntranceRandomization.option_disabled, RandomizationFlag.NOT_RANDOMIZED),
                (options.EntranceRandomization.option_pelican_town, RandomizationFlag.SET_PELICAN_TOWN | RandomizationFlag.MASTERY_CAVE),
                (options.EntranceRandomization.option_non_progression, RandomizationFlag.SET_NON_PROGRESSION | RandomizationFlag.MASTERY_CAVE),
                (options.EntranceRandomization.option_buildings, RandomizationFlag.SET_BUILDINGS | RandomizationFlag.MASTERY_CAVE),
                (options.EntranceRandomization.option_overworld, RandomizationFlag.SET_OVERWORLD | RandomizationFlag.MASTERY_CAVE),
                (options.EntranceRandomization.option_everywhere, RandomizationFlag.SET_EVERYTHING | RandomizationFlag.MASTERY_CAVE),
        ):
            player_options = fill_dataclass_with_default({
                options.EntranceRandomization: entrance_randomization_choice,
                options.EntranceRandomizationBehaviour: options.EntranceRandomizationBehaviour.default,
                options.SkillProgression: options.SkillProgression.option_progressive_with_masteries,
                options.IncludeEndgameLocations: options.IncludeEndgameLocations.option_false, })
            content = create_content(player_options, Random(1))

            flag = create_player_randomization_flag(
                player_options.entrance_randomization,
                player_options.entrance_randomization_behaviour.value,
                player_options.include_endgame_locations.value == options.IncludeEndgameLocations.option_true,
                content,
            )

            self.assertEqual(flag, expected_bit)

    def test_given_masteries_not_randomized_when_create_player_randomization_flag_then_exclude_masteries_bit_enabled(self, ):
        for entrance_randomization_choice in set(options.EntranceRandomization.options.values()) ^ {options.EntranceRandomization.option_disabled}:
            player_options = fill_dataclass_with_default({
                options.EntranceRandomization: entrance_randomization_choice,
                options.EntranceRandomizationBehaviour: options.EntranceRandomizationBehaviour.default,
                options.SkillProgression: options.SkillProgression.option_progressive,
                options.IncludeEndgameLocations: options.IncludeEndgameLocations.option_false, })
            content = create_content(player_options, Random(1))

            flag = create_player_randomization_flag(
                player_options.entrance_randomization,
                player_options.entrance_randomization_behaviour.value,
                player_options.include_endgame_locations.value == options.IncludeEndgameLocations.option_true,
                content,
            )

            self.assertNotIn(RandomizationFlag.MASTERY_CAVE, flag)
