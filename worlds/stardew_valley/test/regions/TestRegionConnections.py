import unittest

from ..options.utils import fill_dataclass_with_default
from ... import options
from ...content import create_content
from ...mods.region_data import region_data_by_content_pack
from ...regions import vanilla_data
from ...regions.model import MergeFlag
from ...regions.regions import create_all_regions, create_all_connections


class TestVanillaRegionsConnectionsWithGingerIsland(unittest.TestCase):
    def test_region_exits_lead_somewhere(self):
        for region in vanilla_data.regions_with_ginger_island_by_name.values():
            with self.subTest(region=region.name):
                for exit_ in region.exits:
                    self.assertIn(exit_, vanilla_data.connections_with_ginger_island_by_name,
                                  f"{region.name} is leading to {exit_} but it does not exist.")

    def test_connection_lead_somewhere(self):
        for connection in vanilla_data.connections_with_ginger_island_by_name.values():
            with self.subTest(connection=connection.name):
                self.assertIn(connection.destination, vanilla_data.regions_with_ginger_island_by_name,
                              f"{connection.name} is leading to {connection.destination} but it does not exist.")


class TestVanillaRegionsConnectionsWithoutGingerIsland(unittest.TestCase):
    def test_region_exits_lead_somewhere(self):
        for region in vanilla_data.regions_without_ginger_island_by_name.values():
            with self.subTest(region=region.name):
                for exit_ in region.exits:
                    self.assertIn(exit_, vanilla_data.connections_without_ginger_island_by_name,
                                  f"{region.name} is leading to {exit_} but it does not exist.")

    def test_connection_lead_somewhere(self):
        for connection in vanilla_data.connections_without_ginger_island_by_name.values():
            with self.subTest(connection=connection.name):
                self.assertIn(connection.destination, vanilla_data.regions_without_ginger_island_by_name,
                              f"{connection.name} is leading to {connection.destination} but it does not exist.")


class TestModsConnections(unittest.TestCase):
    options = {
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false,
        options.Mods: frozenset(options.Mods.valid_keys)
    }
    content = create_content(fill_dataclass_with_default(options))
    all_regions_by_name = create_all_regions(content.registered_packs)
    all_connections_by_name = create_all_connections(content.registered_packs)

    def test_region_exits_lead_somewhere(self):
        for mod_region_data in region_data_by_content_pack.values():
            for region in mod_region_data.regions:
                if MergeFlag.REMOVE_EXITS in region.flag:
                    continue

                with self.subTest(mod=mod_region_data.mod_name, region=region.name):
                    for exit_ in region.exits:
                        self.assertIn(exit_, self.all_connections_by_name, f"{region.name} is leading to {exit_} but it does not exist.")

    def test_connection_lead_somewhere(self):
        for mod_region_data in region_data_by_content_pack.values():
            for connection in mod_region_data.connections:
                with self.subTest(mod=mod_region_data.mod_name, connection=connection.name):
                    self.assertIn(connection.destination, self.all_regions_by_name,
                                  f"{connection.name} is leading to {connection.destination} but it does not exist.")
