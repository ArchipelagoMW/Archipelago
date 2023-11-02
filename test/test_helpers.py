from . import WL4TestBase

from .. import items, locations
from ..types import ItemType, Passage

main_levels = ['Palm Tree Paradise', 'Wildflower Fields', 'Mystic Lake', 'Monsoon Jungle',
               'The Curious Factory', 'The Toxic Landfill', '40 Below Fridge', 'Pinball Zone',
               'Toy Block Tower', 'The Big Board', 'Doodle Woods', 'Domino Row',
               'Crescent Moon Village', 'Arabian Night', 'Fiery Cavern', 'Hotel Horror']

class TestHelpers(WL4TestBase):

    def test_item_filter(self):
        '''Ensure item filters and item names match.'''
        with self.subTest('Jewel Pieces'):
            pieces = items.filter_items(type=ItemType.JEWEL)
            assert all(map(lambda p: p[0].endswith('Piece'), pieces))
            assert all(map(lambda p: p[1].type, pieces))

        with self.subTest('CDs'):
            cds = items.filter_item_names(type=ItemType.CD)
            assert all(map(lambda c: c.endswith('CD'), cds))

        for passage in Passage:
            with self.subTest(passage.long_name()):
                pieces = items.filter_item_names(type=ItemType.JEWEL, passage=passage)
                assert all(map(lambda p: passage.short_name() in p, pieces))

    def test_location_filter(self):
        '''Test that the location filter and location names match'''
        with self.subTest('Hall of Hieroglyphs'):
            checks = locations.get_level_locations(Passage.ENTRY, 0)
            assert all(map(lambda l: l.startswith('Hall of Hieroglyphs'), checks))

        for passage in range(1, 5):
            for level in range(4):
                level_name = main_levels[passage * 4 - 4 + level]
                with self.subTest(level_name):
                    checks = locations.get_level_locations(passage, level)
                    assert all(map(lambda l: l.startswith(level_name), checks))

        with self.subTest('Golden Passage'):
            checks = locations.get_level_locations(Passage.GOLDEN, 0)
            assert all(map(lambda l: l.startswith('Golden Passage'), checks))
