from .bases import CrystalProjectTestBase
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