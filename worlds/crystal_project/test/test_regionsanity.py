from .bases import CrystalProjectTestBase
from .. import PROGRESSIVE_MOUNT, GAEA_STONE
from ..constants.region_passes import *
from ..constants.regions import *


class TestRegionsanityOff(CrystalProjectTestBase):
    options = {
        "regionsanity": 0,
    }

    def test_region_accessibility(self):
        self.set_collected_job_count(5)
        self.collect_mounts()
        self.collect_all_progressive_levels()
        self.assert_region_entrances(CAPITAL_SEQUOIA,
                                     reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE,
                                                        COBBLESTONE_CRAG, GREENSHIRE_REPRISE, CASTLE_SEQUOIA))

class TestRegionsanityOn(CrystalProjectTestBase):
    options = {
        "regionsanity": 1,
    }

    def test_region_accessibility(self):
        self.set_collected_job_count(5)
        self.collect_mounts()
        self.collect_all_progressive_levels()
        self.assert_region_entrances(CAPITAL_SEQUOIA,
                                     unreachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE,
                                                        COBBLESTONE_CRAG, GREENSHIRE_REPRISE, CASTLE_SEQUOIA,))
        self.collect_by_name(JOJO_SEWERS_PASS)
        self.assert_region_entrances(CAPITAL_SEQUOIA,
                                     reachable_regions=(JOJO_SEWERS,),
                                     unreachable_regions=(ROLLING_QUINTAR_FIELDS, SKUMPARADISE,
                                                        COBBLESTONE_CRAG,GREENSHIRE_REPRISE, CASTLE_SEQUOIA,))
        self.collect_by_name(ROLLING_QUINTAR_FIELDS_PASS)
        self.assert_region_entrances(CAPITAL_SEQUOIA,
                                     reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS,),
                                     unreachable_regions=(SKUMPARADISE, COBBLESTONE_CRAG,GREENSHIRE_REPRISE, CASTLE_SEQUOIA,))
        self.collect_by_name(SKUMPARADISE_PASS)
        self.assert_region_entrances(CAPITAL_SEQUOIA,
                                     reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE, ),
                                     unreachable_regions=(COBBLESTONE_CRAG,GREENSHIRE_REPRISE, CASTLE_SEQUOIA,))
        self.collect_by_name(COBBLESTONE_CRAG_PASS)
        self.assert_region_entrances(CAPITAL_SEQUOIA,
                                     reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE,
                                                        COBBLESTONE_CRAG,),
                                     unreachable_regions=(GREENSHIRE_REPRISE, CASTLE_SEQUOIA,))
        self.collect_by_name(GREENSHIRE_REPRISE_PASS)
        self.assert_region_entrances(CAPITAL_SEQUOIA,
                                     reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE,
                                                        COBBLESTONE_CRAG, GREENSHIRE_REPRISE, ),
                                     unreachable_regions=(CASTLE_SEQUOIA,))
        self.collect_by_name(CASTLE_SEQUOIA_PASS)
        self.assert_region_entrances(CAPITAL_SEQUOIA,
                                     reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE,
                                                        COBBLESTONE_CRAG, GREENSHIRE_REPRISE, CASTLE_SEQUOIA,))
    
    def test_has_rental_quintar(self):
        self.set_collected_job_count(5)
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.collect(self.get_item_by_name(GAEA_STONE))
        self.collect_all_progressive_levels()
        # Checking reachability of Salmon Pass tests whether or not has_rental_quintar is correctly making sure you can use the rental desk in rolling quintar fields
        self.collect_by_name(SALMON_PASS_PASS)
        self.collect_by_name(CAPITAL_SEQUOIA_PASS)
        self.collect_by_name(GREENSHIRE_REPRISE_PASS)
        self.assertFalse(self.can_reach_region(SALMON_PASS))
        self.collect_by_name(ROLLING_QUINTAR_FIELDS_PASS)
        self.assertTrue(self.can_reach_region(SALMON_PASS))