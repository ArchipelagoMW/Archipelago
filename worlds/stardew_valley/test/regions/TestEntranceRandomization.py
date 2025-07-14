from collections import deque
from collections.abc import Collection
from unittest.mock import patch, Mock

from BaseClasses import get_seed, MultiWorld, Entrance
from ..assertion import WorldAssertMixin
from ..bases import SVTestCase, solo_multiworld
from ... import options
from ...mods.mod_data import ModNames
from ...options import EntranceRandomization, ExcludeGingerIsland, SkillProgression
from ...options.options import all_mods
from ...regions.entrance_rando import create_entrance_rando_target, prepare_mod_data, connect_regions
from ...regions.model import RegionData, ConnectionData, RandomizationFlag
from ...strings.entrance_names import Entrance as EntranceName
from ...strings.region_names import Region as RegionName


class TestEntranceRando(SVTestCase):

    def test_given_connection_matching_randomization_when_connect_regions_then_make_connection_entrance_rando_target(self):
        region_data_by_name = {
            "Region1": RegionData("Region1", ("randomized_connection", "not_randomized")),
            "Region2": RegionData("Region2"),
            "Region3": RegionData("Region3"),
        }
        connection_data_by_name = {
            "randomized_connection": ConnectionData("randomized_connection", "Region2", flag=RandomizationFlag.PELICAN_TOWN),
            "not_randomized": ConnectionData("not_randomized", "Region2", flag=RandomizationFlag.BUILDINGS),
        }
        regions_by_name = {
            "Region1": Mock(),
            "Region2": Mock(),
            "Region3": Mock(),
        }
        player_randomization_flag = RandomizationFlag.BIT_PELICAN_TOWN

        with patch("worlds.stardew_valley.regions.entrance_rando.create_entrance_rando_target") as mock_create_entrance_rando_target:
            connect_regions(region_data_by_name, connection_data_by_name, regions_by_name, player_randomization_flag)

            expected_origin, expected_destination = regions_by_name["Region1"], regions_by_name["Region2"]
            expected_connection = connection_data_by_name["randomized_connection"]
            mock_create_entrance_rando_target.assert_called_once_with(expected_origin, expected_destination, expected_connection)

    def test_when_create_entrance_rando_target_then_create_exit_and_er_target(self):
        origin = Mock()
        destination = Mock()
        connection_data = ConnectionData("origin to destination", "destination")

        create_entrance_rando_target(origin, destination, connection_data)

        origin.create_exit.assert_called_once_with("origin to destination")
        destination.create_er_target.assert_called_once_with("destination to origin")

    def test_when_prepare_mod_data_then_swapped_connections_contains_both_directions(self):
        placements = Mock(pairings=[("A to B", "C to A"), ("C to D", "A to C")])

        swapped_connections = prepare_mod_data(placements)

        self.assertEqual({"A to B": "A to C", "C to A": "B to A", "C to D": "C to A", "A to C": "D to C"}, swapped_connections)


class TestEntranceRandoCreatesValidWorlds(WorldAssertMixin, SVTestCase):

    # The following tests validate that ER still generates winnable and logically-sane games with given mods.
    # Mods that do not interact with entrances are skipped
    # Not all ER settings are tested, because 'buildings' is, essentially, a superset of all others
    def test_ginger_island_excluded_buildings(self):
        world_options = {
            options.EntranceRandomization: options.EntranceRandomization.option_buildings,
            options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_true
        }
        with solo_multiworld(world_options) as (multi_world, _):
            self.assert_basic_checks(multi_world)

    def test_deepwoods_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.deepwoods, options.EntranceRandomization.option_buildings)

    def test_juna_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.juna, options.EntranceRandomization.option_buildings)

    def test_jasper_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.jasper, options.EntranceRandomization.option_buildings)

    def test_alec_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.alec, options.EntranceRandomization.option_buildings)

    def test_yoba_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.yoba, options.EntranceRandomization.option_buildings)

    def test_eugene_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.eugene, options.EntranceRandomization.option_buildings)

    def test_ayeisha_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.ayeisha, options.EntranceRandomization.option_buildings)

    def test_riley_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.riley, options.EntranceRandomization.option_buildings)

    def test_sve_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.sve, options.EntranceRandomization.option_buildings)

    def test_alecto_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.alecto, options.EntranceRandomization.option_buildings)

    def test_lacey_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.lacey, options.EntranceRandomization.option_buildings)

    def test_boarding_house_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(ModNames.boarding_house, options.EntranceRandomization.option_buildings)

    def test_all_mods_entrance_randomization_buildings(self):
        self.perform_basic_checks_on_mod_with_er(all_mods, options.EntranceRandomization.option_buildings)

    def perform_basic_checks_on_mod_with_er(self, mods: str | set[str], er_option: int) -> None:
        if isinstance(mods, str):
            mods = {mods}
        world_options = {
            options.EntranceRandomization: er_option,
            options.Mods: frozenset(mods),
            options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false
        }
        with solo_multiworld(world_options) as (multi_world, _):
            self.assert_basic_checks(multi_world)


# GER should have this covered, but it's good to have a backup
class TestGingerIslandEntranceRando(SVTestCase):
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
