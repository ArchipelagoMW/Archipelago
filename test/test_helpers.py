import itertools
from test.bases import TestBase

from ..data import Passage
from ..items import ItemType, ap_id_from_wl4_data, filter_items, filter_item_names, item_table, wl4_data_from_ap_id
from ..locations import get_level_locations, location_table
from ..options import Difficulty
from ..region_data import level_table


main_levels = ['Palm Tree Paradise', 'Wildflower Fields', 'Mystic Lake', 'Monsoon Jungle',
               'The Curious Factory', 'The Toxic Landfill', '40 Below Fridge', 'Pinball Zone',
               'Toy Block Tower', 'The Big Board', 'Doodle Woods', 'Domino Row',
               'Crescent Moon Village', 'Arabian Night', 'Fiery Cavern', 'Hotel Horror']

class TestHelpers(TestBase):
    def test_item_filter(self):
        """Ensure item filters and item names match."""
        with self.subTest('Jewel Pieces'):
            pieces = filter_items(type=ItemType.JEWEL)
            assert all(map(lambda p: p[0].endswith('Piece'), pieces))
            assert all(map(lambda p: p[1].type == ItemType.JEWEL, pieces))

        with self.subTest('CDs'):
            cds = filter_item_names(type=ItemType.CD)
            assert all(map(lambda c: c.endswith('CD'), cds))

        for passage in Passage:
            with self.subTest(passage.long_name()):
                pieces = filter_item_names(type=ItemType.JEWEL, passage=passage)
                assert all(map(lambda p: passage.short_name() in p, pieces))

    def test_location_filter(self):
        """Test that the location filter and location names match"""
        with self.subTest('Hall of Hieroglyphs'):
            checks = get_level_locations(Passage.ENTRY, 0)
            assert all(map(lambda l: l.startswith('Hall of Hieroglyphs'), checks))

        for passage in range(1, 5):
            for level in range(4):
                level_name = main_levels[passage * 4 - 4 + level]
                with self.subTest(level_name):
                    checks = get_level_locations(Passage(passage), level)
                    assert all(map(lambda l: l.startswith(level_name), checks))

        with self.subTest('Golden Passage'):
            checks = get_level_locations(Passage.GOLDEN, 0)
            assert all(map(lambda l: l.startswith('Golden Passage'), checks))

    def test_item_id_conversion(self):
        """Test that item ID conversion works both ways"""
        for name, data in item_table.items():
            with self.subTest(name):
                ap_id = ap_id_from_wl4_data(data)
                self.assertEqual((name, data), wl4_data_from_ap_id(ap_id))


class TestLocationExistence(TestBase):
    def _test_locations_match(self, difficulty):
        locations_from_table = {
            name
            for name, data in location_table.items()
            if difficulty in data.difficulties and data.level < 4
        }
        locations_from_tree = {
            f'{level_name} - {location.name}'
            for level_name, level in level_table.items()
            for region in level.regions
            for location in itertools.chain(region.locations, region.diamonds)
            if difficulty in location.difficulties and not location.event
        }
        self.assertEqual(locations_from_table, locations_from_tree)

    def test_normal_locations_match(self):
        self._test_locations_match(Difficulty.option_normal)

    def test_hard_locations_match(self):
        self._test_locations_match(Difficulty.option_hard)

    def test_s_hard_locations_match(self):
        self._test_locations_match(Difficulty.option_s_hard)
