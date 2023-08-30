from . import WL4TestBase
from ..locations import location_table
from ..types import LocationType, Passage


# I don't fully understand how these tests work so I'm reasonably sure these
# aren't thorough enough. Then again, WL4's progression is pretty simple.

class TestAccess(WL4TestBase):
    def test_spoiled_rotten(self):
        '''Test access to Spoiled Rotten'''
        locations = ['Spoiled Rotten']
        items = [['Top Right Entry Jewel Piece',
                  'Bottom Right Entry Jewel Piece',
                  'Bottom Left Entry Jewel Piece',
                  'Top Left Entry Jewel Piece']]
        self.assertAccessDependency(locations, items)

    def test_level_access(self):
        '''Test access to the sixteen main levels'''
        locations = filter(lambda l: location_table[l].source == LocationType.BOX
                                     and location_table[l].passage() not in (Passage.ENTRY, Passage.GOLDEN),
                           location_table)
        items = [['Entry Passage Clear']]
        self.assertAccessDependency(locations, items)

    def test_cractus_access(self):
        '''Test access to Cractus'''
        locations = ['Cractus']
        items = [['Top Right Emerald Piece',
                  'Bottom Right Emerald Piece',
                  'Bottom Left Emerald Piece',
                  'Top Left Emerald Piece']]
        self.assertAccessDependency(locations, items)

    def test_cuckoo_condor_access(self):
        '''Test access to Cuckoo Condor'''
        locations = ['Cuckoo Condor']
        items = [['Top Right Ruby Piece',
                  'Bottom Right Ruby Piece',
                  'Bottom Left Ruby Piece',
                  'Top Left Ruby Piece']]
        self.assertAccessDependency(locations, items)

    def test_aerodent_access(self):
        '''Test access to Aerodent'''
        locations = ['Aerodent']
        items = [['Top Right Topaz Piece',
                  'Bottom Right Topaz Piece',
                  'Bottom Left Topaz Piece',
                  'Top Left Topaz Piece']]
        self.assertAccessDependency(locations, items)

    def test_catbat_access(self):
        '''Test access to Catbat'''
        locations = ['Catbat']
        items = [['Top Right Sapphire Piece',
                  'Bottom Right Sapphire Piece',
                  'Bottom Left Sapphire Piece',
                  'Top Left Sapphire Piece']]
        self.assertAccessDependency(locations, items)

    def test_golden_passage_access(self):
        '''Test access to the Golden Passage'''
        locations = filter(lambda l: location_table[l].source == LocationType.BOX
                                     and location_table[l].passage() == Passage.GOLDEN,
                           location_table)
        items = [['Emerald Passage Clear', 'Ruby Passage Clear',
                  'Topaz Passage Clear', 'Sapphire Passage Clear']]
        self.assertAccessDependency(locations, items)

    def test_golden_diva_access(self):
        '''Test access to the Golden Diva'''
        locations = ['Golden Diva']
        items = [['Top Right Golden Jewel Piece',
                  'Bottom Right Golden Jewel Piece',
                  'Bottom Left Golden Jewel Piece',
                  'Top Left Golden Jewel Piece']]
        self.assertAccessDependency(locations, items)
