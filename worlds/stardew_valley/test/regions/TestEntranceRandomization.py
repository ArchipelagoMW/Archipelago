from collections import deque
from collections.abc import Collection

from BaseClasses import get_seed, MultiWorld, Entrance
from .. import SVTestCase
from ... import options, StardewValleyWorld
from ...mods.mod_data import ModNames
from ...options import EntranceRandomization, ExcludeGingerIsland, SkillProgression
from ...options.options import all_mods
from ...regions import vanilla_data
from ...regions.entrance_rando import create_player_randomization_flag
from ...regions.regions import create_all_connections
from ...strings.entrance_names import Entrance as EntranceName
from ...strings.region_names import Region as RegionName


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


class TestModEntranceRando(SVTestCase):

    def test_entrance_randomization(self):
        for option in (options.EntranceRandomization.option_pelican_town, options.EntranceRandomization.option_non_progression,
                       options.EntranceRandomization.option_buildings_without_house, options.EntranceRandomization.option_buildings):
            test_options = {
                options.EntranceRandomization: option,
                options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false,
                options.SkillProgression: options.SkillProgression.option_progressive_with_masteries,
                options.Mods: frozenset(options.Mods.valid_keys)
            }
            with self.solo_world_sub_test(world_options=test_options, world_caching=False) as (multiworld, world):
                world: StardewValleyWorld
                entrances_placement = world.randomized_entrances
                flag = create_player_randomization_flag(world.options.entrance_randomization, world.content)

                expected_randomized_connections = [connection
                                                   for connection in create_all_connections(world.content.registered_packs).values()
                                                   if connection.is_eligible_for_randomization(flag)]
                for connection in expected_randomized_connections:
                    self.assertIn(connection.name, entrances_placement,
                                  f"Connection {connection.name} should be randomized but it is not in the output.")
                    self.assertIn(connection.reverse, entrances_placement,
                                  f"Connection {connection.reverse} should be randomized but it is not in the output.")

                self.assertEqual(len(set(entrances_placement.values())), len(entrances_placement.values()),
                                 f"Connections are duplicated in randomization.")

    # The following tests validate that ER still generates winnable and logically-sane games with given mods.
    # Mods that do not interact with entrances are skipped
    # Not all ER settings are tested, because 'buildings' is, essentially, a superset of all others
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
        with self.solo_world_sub_test(f"entrance_randomization: {er_option}, Mods: {mods}", world_options) as (multi_world, _):
            self.assert_basic_checks(multi_world)


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
