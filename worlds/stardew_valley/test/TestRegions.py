import random
import sys
import unittest

from .. import StardewOptions, options
from ..regions import vanilla_regions, vanilla_connections, randomize_connections, RandomizationFlag

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


class TestEntranceRando(unittest.TestCase):

    def test_entrance_randomization(self):
        #for option, flag in [(options.EntranceRandomization.option_pelican_town, RandomizationFlag.PELICAN_TOWN),
        #                     (options.EntranceRandomization.option_non_progression, RandomizationFlag.NON_PROGRESSION),
        #                     (options.EntranceRandomization.option_buildings, RandomizationFlag.BUILDINGS)]:
        option = options.EntranceRandomization.option_buildings
        flag = RandomizationFlag.BUILDINGS
        for i in range(0, 100000):
            seed = random.randrange(sys.maxsize)
            with self.subTest(flag=flag, msg=f"Seed: {seed}"):
                rand = random.Random(seed)
                world_options = StardewOptions({options.EntranceRandomization.internal_name: option,
                                                options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_false})
                regions_by_name = {region.name: region for region in vanilla_regions}

                _, randomized_connections = randomize_connections(rand, world_options, regions_by_name)

                for connection in vanilla_connections:
                    if flag in connection.flag:
                        connection_in_randomized = connection.name in randomized_connections
                        reverse_in_randomized = connection.reverse in randomized_connections
                        self.assertTrue(connection_in_randomized,
                                      f"Connection {connection.name} should be randomized but it is not in the output. Seed = {seed}")
                        self.assertTrue(reverse_in_randomized,
                                      f"Connection {connection.reverse} should be randomized but it is not in the output. Seed = {seed}")

                self.assertEqual(len(set(randomized_connections.values())), len(randomized_connections.values()),
                                 f"Connections are duplicated in randomization. Seed = {seed}")

    def test_entrance_randomization_without_island(self):
        for option, flag in [(options.EntranceRandomization.option_pelican_town, RandomizationFlag.PELICAN_TOWN),
                             (options.EntranceRandomization.option_non_progression, RandomizationFlag.NON_PROGRESSION),
                             (options.EntranceRandomization.option_buildings, RandomizationFlag.BUILDINGS)]:
            with self.subTest(option=option, flag=flag):
                seed = random.randrange(sys.maxsize)
                rand = random.Random(seed)
                world_options = StardewOptions({options.EntranceRandomization.internal_name: option,
                                                options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true})
                regions_by_name = {region.name: region for region in vanilla_regions}

                _, randomized_connections = randomize_connections(rand, world_options, regions_by_name)

                for connection in vanilla_connections:
                    if flag in connection.flag:
                        if RandomizationFlag.GINGER_ISLAND in connection.flag:
                            self.assertNotIn(connection.name, randomized_connections,
                                          f"Connection {connection.name} should not be randomized but it is in the output. Seed = {seed}")
                            self.assertNotIn(connection.reverse, randomized_connections,
                                          f"Connection {connection.reverse} should not be randomized but it is in the output. Seed = {seed}")
                        else:
                            self.assertIn(connection.name, randomized_connections,
                                          f"Connection {connection.name} should be randomized but it is not in the output. Seed = {seed}")
                            self.assertIn(connection.reverse, randomized_connections,
                                          f"Connection {connection.reverse} should be randomized but it is not in the output. Seed = {seed}")

                self.assertEqual(len(set(randomized_connections.values())), len(randomized_connections.values()),
                                 f"Connections are duplicated in randomization. Seed = {seed}")
