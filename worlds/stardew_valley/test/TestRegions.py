import random
import sys
import unittest

from .. import StardewOptions, options
from ..regions import stardew_valley_regions, mandatory_connections, randomize_connections, RandomizationFlag

connections_by_name = {connection.name for connection in mandatory_connections}
regions_by_name = {region.name for region in stardew_valley_regions}


class TestRegions(unittest.TestCase):
    def test_region_exits_lead_somewhere(self):
        for region in stardew_valley_regions:
            with self.subTest(region=region):
                for exit in region.exits:
                    assert exit in connections_by_name, f"{region.name} is leading to {exit} but it does not exist."

    def test_connection_lead_somewhere(self):
        for connection in mandatory_connections:
            with self.subTest(connection=connection):
                assert connection.destination in regions_by_name, \
                    f"{connection.name} is leading to {connection.destination} but it does not exist."


class TestEntranceRando(unittest.TestCase):

    def test_pelican_town_entrance_randomization(self):
        for option, flag in [(options.EntranceRandomization.option_pelican_town, RandomizationFlag.PELICAN_TOWN),
                             (options.EntranceRandomization.option_non_progression, RandomizationFlag.NON_PROGRESSION)]:
            with self.subTest(option=option, flag=flag):
                seed = random.randrange(sys.maxsize)
                rand = random.Random(seed)
                world_options = StardewOptions({options.EntranceRandomization.internal_name: option})

                _, randomized_connections = randomize_connections(rand, world_options)

                for connection in mandatory_connections:
                    if flag in connection.flag:
                        assert connection.name in randomized_connections, \
                            f"Connection {connection.name} should be randomized but it is not in the output. Seed = {seed}"
                        assert connection.reverse in randomized_connections, \
                            f"Connection {connection.reverse} should be randomized but it is not in the output. Seed = {seed}"

                assert len(set(randomized_connections.values())) == len(
                    randomized_connections.values()), f"Connections are duplicated in randomization. Seed = {seed}"
