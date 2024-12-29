import unittest
from collections import deque
from collections.abc import Collection

from BaseClasses import get_seed, MultiWorld, Entrance
from .. import SVTestCase, RuleAssertMixin
from ..options.utils import fill_dataclass_with_default
from ... import create_content, options, StardewValleyWorld
from ...options import EntranceRandomization, ExcludeGingerIsland, SkillProgression
from ...regions import vanilla_data
from ...regions.entrance_rando import create_player_randomization_flag
from ...regions.model import RandomizationFlag, ConnectionData, reverse_connection_name
from ...regions.regions import create_all_regions, create_all_connections
from ...stardew_rule import Reach
from ...strings.entrance_names import Entrance as EntranceName
from ...strings.region_names import Region as RegionName


class TestRegions(unittest.TestCase):
    def test_region_exits_lead_somewhere(self):
        for region in vanilla_data.regions_with_ginger_island_by_name.values():
            with self.subTest(region=region):
                for exit_ in region.exits:
                    self.assertIn(exit_, vanilla_data.connections_with_ginger_island_by_name,
                                  f"{region.name} is leading to {exit_} but it does not exist.")

    def test_connection_lead_somewhere(self):
        for connection in vanilla_data.connections_with_ginger_island_by_name.values():
            with self.subTest(connection=connection):
                self.assertIn(connection.destination, vanilla_data.regions_with_ginger_island_by_name,
                              f"{connection.name} is leading to {connection.destination} but it does not exist.")

    def test_given_ginger_island_is_disabled_when_create_regions_then_no_ginger_island_regions(self):
        player_options = fill_dataclass_with_default({
            options.ExcludeGingerIsland: ExcludeGingerIsland.option_true,
        })
        content = create_content(player_options)

        regions = create_all_regions(content.registered_packs)

        self.assertDictEqual(dict(vanilla_data.regions_without_ginger_island_by_name), regions)

    def test_given_ginger_island_is_disabled_when_create_connections_then_no_ginger_island_connections(self):
        player_options = fill_dataclass_with_default({
            options.ExcludeGingerIsland: ExcludeGingerIsland.option_true,
        })
        content = create_content(player_options)

        connections = create_all_connections(content.registered_packs)

        self.assertDictEqual(dict(vanilla_data.connections_without_ginger_island_by_name), connections)


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
                (EntranceRandomization.option_disabled, RandomizationFlag.NOT_RANDOMIZED),
                (EntranceRandomization.option_pelican_town, RandomizationFlag.BIT_PELICAN_TOWN),
                (EntranceRandomization.option_non_progression, RandomizationFlag.BIT_NON_PROGRESSION),
                (EntranceRandomization.option_buildings_without_house, RandomizationFlag.BIT_BUILDINGS),
                (EntranceRandomization.option_buildings, RandomizationFlag.BIT_BUILDINGS),
                (EntranceRandomization.option_chaos, RandomizationFlag.BIT_BUILDINGS),
        ):
            player_options = fill_dataclass_with_default({EntranceRandomization: entrance_randomization_choice})
            content = create_content(player_options)

            flag = create_player_randomization_flag(player_options.entrance_randomization, content)

            self.assertEqual(flag, expected_bit)

    def test_given_masteries_not_randomized_when_create_player_randomization_flag_then_exclude_masteries_bit_enabled(self):
        for entrance_randomization_choice in set(EntranceRandomization.options.values()) ^ {EntranceRandomization.option_disabled}:
            player_options = fill_dataclass_with_default({
                EntranceRandomization: entrance_randomization_choice,
                options.SkillProgression: options.SkillProgression.option_progressive
            })
            content = create_content(player_options)

            flag = create_player_randomization_flag(player_options.entrance_randomization, content)

            self.assertIn(RandomizationFlag.EXCLUDE_MASTERIES, flag)


class TestEntranceRando(SVTestCase):

    def test_entrance_randomization(self):
        for option in (options.EntranceRandomization.option_pelican_town, options.EntranceRandomization.option_non_progression,
                       options.EntranceRandomization.option_buildings_without_house, options.EntranceRandomization.option_buildings):
            test_options = {
                options.EntranceRandomization: option,
                options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false,
                options.SkillProgression: options.SkillProgression.option_progressive_with_masteries,
            }
            with self.solo_world_sub_test(world_options=test_options, world_caching=False) as (multiworld, world):
                world: StardewValleyWorld
                entrances_placement = world.randomized_entrances
                flag = create_player_randomization_flag(world.options.entrance_randomization, world.content)

                for connection in (connection for connection in vanilla_data.connections_with_ginger_island_by_name.values()
                                   if connection.is_eligible_for_randomization(flag)):
                    self.assertIn(connection.name, entrances_placement,
                                  f"Connection {connection.name} should be randomized but it is not in the output.")
                    self.assertIn(connection.reverse, entrances_placement,
                                  f"Connection {connection.reverse} should be randomized but it is not in the output.")

                self.assertEqual(len(set(entrances_placement.values())), len(entrances_placement.values()),
                                 f"Connections are duplicated in randomization.")

    def test_cannot_put_island_access_on_island(self):
        test_options = {
            options.EntranceRandomization: EntranceRandomization.option_buildings,
            options.ExcludeGingerIsland: ExcludeGingerIsland.option_false,
            options.SkillProgression: SkillProgression.option_progressive_with_masteries,
        }

        blocked_entrances = {EntranceName.use_island_obelisk, EntranceName.boat_to_ginger_island}
        required_regions = {RegionName.wizard_tower, RegionName.boat_tunnel}

        for i in range(0, 10 if self.skip_long_tests else 1000):
            seed = get_seed()
            with self.solo_world_sub_test(f"Seed: {seed}", world_options=test_options, world_caching=False, seed=seed) as (multiworld, world):
                self.assert_can_reach_any_region_before_blockers(required_regions, blocked_entrances, multiworld)

    def assert_can_reach_any_region_before_blockers(self, required_regions: Collection[str], blocked_entrances: Collection[str], multiworld: MultiWorld):
        explored_regions = explore_regions_up_to_blockers(blocked_entrances, multiworld)
        self.assertTrue(any(region in explored_regions for region in required_regions))


def explore_regions_up_to_blockers(blocked_entrances: Collection[str], multiworld: MultiWorld) -> set[str]:
    explored_regions: set[str] = set()
    regions_by_name = multiworld.regions.region_cache[1]
    regions_to_explore = deque([regions_by_name["Menu"]])

    while regions_to_explore:
        region = regions_to_explore.pop()

        if region.name in explored_regions:
            continue

        explored_regions.add(region.name)

        for exit_ in region.exits:
            exit_: Entrance
            if exit_.name in blocked_entrances:
                continue
            regions_to_explore.append(exit_.connected_region)

    return explored_regions


class TestEntranceClassifications(SVTestCase, RuleAssertMixin):

    def test_non_progression_are_all_accessible_with_empty_inventory(self):
        for option in [EntranceRandomization.option_pelican_town, EntranceRandomization.option_non_progression]:
            world_options = {
                options.EntranceRandomization: option
            }

            with self.solo_world_sub_test(world_options=world_options) as (multiworld, sv_world):
                sv_world: StardewValleyWorld
                ap_entrances = multiworld.regions.entrance_cache[1]
                for randomized_entrance in sv_world.randomized_entrances:

                    if randomized_entrance not in ap_entrances:
                        self.assertIn(reverse_connection_name(randomized_entrance), ap_entrances)
                    else:
                        reach = Reach(randomized_entrance, "Entrance", 1)
                        self.assert_rule_true(reach, multiworld.state)
