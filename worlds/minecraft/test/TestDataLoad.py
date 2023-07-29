import unittest

from .. import Constants

class TestDataLoad(unittest.TestCase):

    def test_item_data(self):
        item_info = Constants.item_info

        # All items in sub-tables are in all_items
        all_items: set = set(item_info['all_items'])
        assert set(item_info['progression_items']) <= all_items
        assert set(item_info['useful_items']) <= all_items
        assert set(item_info['trap_items']) <= all_items
        assert set(item_info['required_pool'].keys()) <= all_items
        assert set(item_info['junk_weights'].keys()) <= all_items

        # No overlapping ids (because of bee trap stuff)
        all_ids: set = set(Constants.item_name_to_id.values())
        assert len(all_items) == len(all_ids)

    def test_location_data(self):
        location_info = Constants.location_info
        exclusion_info = Constants.exclusion_info

        # Every location has a region and every region's locations are in all_locations
        all_locations: set = set(location_info['all_locations'])
        all_locs_2: set    = set()
        for v in location_info['locations_by_region'].values():
            all_locs_2.update(v)
        assert all_locations == all_locs_2

        # All exclusions are locations
        for v in exclusion_info.values():
            assert set(v) <= all_locations

    def test_region_data(self):
        region_info = Constants.region_info

        # Every entrance and region in mandatory/default/illegal connections is a real entrance and region
        all_regions = set()
        all_entrances = set()
        for v in region_info['regions']:
            assert isinstance(v[0], str)
            assert isinstance(v[1], list)
            all_regions.add(v[0])
            all_entrances.update(v[1])

        for v in region_info['mandatory_connections']:
            assert v[0] in all_entrances
            assert v[1] in all_regions
            
        for v in region_info['default_connections']:
            assert v[0] in all_entrances
            assert v[1] in all_regions

        for k, v in region_info['illegal_connections'].items():
            assert k in all_regions
            assert set(v) <= all_entrances

