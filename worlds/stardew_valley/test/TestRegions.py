import random
import unittest
from typing import Set

from BaseClasses import get_seed
from . import SVTestCase
from .options.utils import fill_dataclass_with_default
from .. import create_content
from ..options import EntranceRandomization, ExcludeGingerIsland, SkillProgression
from ..regions import vanilla_regions, vanilla_connections, randomize_connections, RandomizationFlag, create_final_connections_and_regions
from ..strings.entrance_names import Entrance as EntranceName
from ..strings.region_names import Region as RegionName

connections_by_name = {connection.name for connection in vanilla_connections}
regions_by_name = {region.name for region in vanilla_regions}


class TestRegions(unittest.TestCase):
    def test_region_exits_lead_somewhere(self):
        for region in vanilla_regions:
            with self.subTest(region=region):
                for exit in region.exits:
                    self.assertIn(exit, connections_by_name,
                                  f"{region.name} is leading to {exit} but it does not exist.")

    def test_connection_lead_somewhere(self):
        for connection in vanilla_connections:
            with self.subTest(connection=connection):
                self.assertIn(connection.destination, regions_by_name,
                              f"{connection.name} is leading to {connection.destination} but it does not exist.")


def explore_connections_tree_up_to_blockers(blocked_entrances: Set[str], connections_by_name, regions_by_name):
    explored_entrances = set()
    explored_regions = set()
    entrances_to_explore = set()
    current_node_name = "Menu"
    current_node = regions_by_name[current_node_name]
    entrances_to_explore.update(current_node.exits)
    while entrances_to_explore:
        current_entrance_name = entrances_to_explore.pop()
        current_entrance = connections_by_name[current_entrance_name]
        current_node_name = current_entrance.destination

        explored_entrances.add(current_entrance_name)
        explored_regions.add(current_node_name)

        if current_entrance_name in blocked_entrances:
            continue

        current_node = regions_by_name[current_node_name]
        entrances_to_explore.update({entrance for entrance in current_node.exits if entrance not in explored_entrances})
    return explored_regions


class TestEntranceRando(SVTestCase):

    def test_entrance_randomization(self):
        for option, flag in [(EntranceRandomization.option_pelican_town, RandomizationFlag.PELICAN_TOWN),
                             (EntranceRandomization.option_non_progression, RandomizationFlag.NON_PROGRESSION),
                             (EntranceRandomization.option_buildings_without_house, RandomizationFlag.BUILDINGS),
                             (EntranceRandomization.option_buildings, RandomizationFlag.BUILDINGS)]:
            sv_options = fill_dataclass_with_default({
                EntranceRandomization.internal_name: option,
                ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_false,
                SkillProgression.internal_name: SkillProgression.option_progressive_with_masteries,
            })
            content = create_content(sv_options)
            seed = get_seed()
            rand = random.Random(seed)
            with self.subTest(flag=flag, msg=f"Seed: {seed}"):
                entrances, regions = create_final_connections_and_regions(sv_options)
                _, randomized_connections = randomize_connections(rand, sv_options, content, regions, entrances)

                for connection in vanilla_connections:
                    if flag in connection.flag:
                        connection_in_randomized = connection.name in randomized_connections
                        reverse_in_randomized = connection.reverse in randomized_connections
                        self.assertTrue(connection_in_randomized, f"Connection {connection.name} should be randomized but it is not in the output.")
                        self.assertTrue(reverse_in_randomized, f"Connection {connection.reverse} should be randomized but it is not in the output.")

                self.assertEqual(len(set(randomized_connections.values())), len(randomized_connections.values()),
                                 f"Connections are duplicated in randomization.")

    def test_entrance_randomization_without_island(self):
        for option, flag in [(EntranceRandomization.option_pelican_town, RandomizationFlag.PELICAN_TOWN),
                             (EntranceRandomization.option_non_progression, RandomizationFlag.NON_PROGRESSION),
                             (EntranceRandomization.option_buildings_without_house, RandomizationFlag.BUILDINGS),
                             (EntranceRandomization.option_buildings, RandomizationFlag.BUILDINGS)]:

            sv_options = fill_dataclass_with_default({
                EntranceRandomization.internal_name: option,
                ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true,
                SkillProgression.internal_name: SkillProgression.option_progressive_with_masteries,
            })
            content = create_content(sv_options)
            seed = get_seed()
            rand = random.Random(seed)
            with self.subTest(option=option, flag=flag, seed=seed):
                entrances, regions = create_final_connections_and_regions(sv_options)
                _, randomized_connections = randomize_connections(rand, sv_options, content, regions, entrances)

                for connection in vanilla_connections:
                    if flag in connection.flag:
                        if RandomizationFlag.GINGER_ISLAND in connection.flag:
                            self.assertNotIn(connection.name, randomized_connections,
                                             f"Connection {connection.name} should not be randomized but it is in the output.")
                            self.assertNotIn(connection.reverse, randomized_connections,
                                             f"Connection {connection.reverse} should not be randomized but it is in the output.")
                        else:
                            self.assertIn(connection.name, randomized_connections,
                                          f"Connection {connection.name} should be randomized but it is not in the output.")
                            self.assertIn(connection.reverse, randomized_connections,
                                          f"Connection {connection.reverse} should be randomized but it is not in the output.")

                self.assertEqual(len(set(randomized_connections.values())), len(randomized_connections.values()),
                                 f"Connections are duplicated in randomization.")

    def test_cannot_put_island_access_on_island(self):
        sv_options = fill_dataclass_with_default({
            EntranceRandomization.internal_name: EntranceRandomization.option_buildings,
            ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_false,
            SkillProgression.internal_name: SkillProgression.option_progressive_with_masteries,
        })
        content = create_content(sv_options)

        for i in range(0, 100 if self.skip_long_tests else 10000):
            seed = get_seed()
            rand = random.Random(seed)
            with self.subTest(msg=f"Seed: {seed}"):
                entrances, regions = create_final_connections_and_regions(sv_options)
                randomized_connections, randomized_data = randomize_connections(rand, sv_options, content, regions, entrances)
                connections_by_name = {connection.name: connection for connection in randomized_connections}

                blocked_entrances = {EntranceName.use_island_obelisk, EntranceName.boat_to_ginger_island}
                required_regions = {RegionName.wizard_tower, RegionName.boat_tunnel}
                self.assert_can_reach_any_region_before_blockers(required_regions, blocked_entrances, connections_by_name, regions)

    def assert_can_reach_any_region_before_blockers(self, required_regions, blocked_entrances, connections_by_name, regions_by_name):
        explored_regions = explore_connections_tree_up_to_blockers(blocked_entrances, connections_by_name, regions_by_name)
        self.assertTrue(any(region in explored_regions for region in required_regions))


class TestEntranceClassifications(SVTestCase):

    def test_non_progression_are_all_accessible_with_empty_inventory(self):
        for option, flag in [(EntranceRandomization.option_pelican_town, RandomizationFlag.PELICAN_TOWN),
                             (EntranceRandomization.option_non_progression, RandomizationFlag.NON_PROGRESSION)]:
            world_options = {
                EntranceRandomization.internal_name: option
            }
            with self.solo_world_sub_test(world_options=world_options, flag=flag) as (multiworld, sv_world):
                ap_entrances = {entrance.name: entrance for entrance in multiworld.get_entrances()}
                for randomized_entrance in sv_world.randomized_entrances:
                    if randomized_entrance in ap_entrances:
                        ap_entrance_origin = ap_entrances[randomized_entrance]
                        self.assertTrue(ap_entrance_origin.access_rule(multiworld.state))
                    if sv_world.randomized_entrances[randomized_entrance] in ap_entrances:
                        ap_entrance_destination = multiworld.get_entrance(sv_world.randomized_entrances[randomized_entrance], 1)
                        self.assertTrue(ap_entrance_destination.access_rule(multiworld.state))

    def test_no_ginger_island_entrances_when_excluded(self):
        world_options = {
            EntranceRandomization.internal_name: EntranceRandomization.option_disabled,
            ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true
        }
        with self.solo_world_sub_test(world_options=world_options) as (multiworld, _):
            ap_entrances = {entrance.name: entrance for entrance in multiworld.get_entrances()}
            entrance_data_by_name = {entrance.name: entrance for entrance in vanilla_connections}
            for entrance_name in ap_entrances:
                entrance_data = entrance_data_by_name[entrance_name]
                with self.subTest(f"{entrance_name}: {entrance_data.flag}"):
                    self.assertFalse(entrance_data.flag & RandomizationFlag.GINGER_ISLAND)
