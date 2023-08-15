import itertools

from . import WL4TestBase
from ..names import LocationName, ItemName


# I don't fully understand how these tests work so I'm reasonably sure these
# aren't thorough enough. Then again, WL4's progression is pretty simple.

class TestAccess(WL4TestBase):
    def test_spoiled_rotten(self):
        '''Test access to Spoiled Rotten'''
        locations = [LocationName.spoiled_rotten]
        items = [ItemName.entry_passage_jewel]
        self.assertAccessDependency(locations, items)

    def test_level_access(self):
        '''Test access to the sixteen main levels'''
        locations = itertools.chain(
            LocationName.palm_tree_paradise.locations(),
            LocationName.wildflower_fields.locations(),
            LocationName.mystic_lake.locations(),
            LocationName.monsoon_jungle.locations(),
            LocationName.curious_factory.locations(),
            LocationName.toxic_landfill.locations(),
            LocationName.forty_below_fridge.locations(),
            LocationName.pinball_zone.locations(),
            LocationName.toy_block_tower.locations(),
            LocationName.big_board.locations(),
            LocationName.doodle_woods.locations(),
            LocationName.domino_row.locations(),
            LocationName.crescent_moon_village.locations(),
            LocationName.arabian_night.locations(),
            LocationName.fiery_cavern.locations(),
            LocationName.hotel_horror.locations(),
        )

        items = [[ItemName.defeated_boss]]
        self.assertAccessDependency(locations, items)

    def test_cractus_access(self):
        '''Test access to Cractus'''
        locations = [LocationName.cractus]
        items = [ItemName.emerald_passage_jewel]
        self.assertAccessDependency(locations, items)

    def test_cuckoo_condor_access(self):
        '''Test access to Cuckoo Condor'''
        locations = [LocationName.cuckoo_condor]
        items = [ItemName.ruby_passage_jewel]
        self.assertAccessDependency(locations, items)

    def test_aerodent_access(self):
        '''Test access to Aerodent'''
        locations = [LocationName.aerodent]
        items = [ItemName.topaz_passage_jewel]
        self.assertAccessDependency(locations, items)

    def test_catbat_access(self):
        '''Test access to Catbat'''
        locations = [LocationName.catbat]
        items = [ItemName.sapphire_passage_jewel]
        self.assertAccessDependency(locations, items)

    def test_golden_passage_access(self):
        '''Test access to the Golden Passage'''
        locations = LocationName.golden_passage.locations()
        items = [[ItemName.defeated_boss]]
        self.assertAccessDependency(locations, items)

    def test_golden_diva_access(self):
        '''Test access to the Golden Diva'''
        locations = [LocationName.golden_diva]
        items = [ItemName.golden_pyramid_jewel]
        self.assertAccessDependency(locations, items)
