from .bases import CrystalProjectTestBase
from ..constants.key_items import *
from ..constants.keys import *
from ..constants.mounts import *
from ..constants.region_passes import *
from ..constants.regions import *


class TestRegionsanityOff(CrystalProjectTestBase):
    options = {
        "regionsanity": 0,
    }

    def test_region_accessibility(self):
        self.set_collected_job_count(5)
        self.collect_mounts()
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
        self.assert_region_entrances(CAPITAL_SEQUOIA,
                                     unreachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE,
                                                        COBBLESTONE_CRAG, GREENSHIRE_REPRISE, CASTLE_SEQUOIA,))
        self.collect_by_name(JOJO_SEWERS_PASS)
        self.assert_region_entrances(CAPITAL_SEQUOIA,
                                     reachable_regions=(JOJO_SEWERS,),
                                     unreachable_regions=(ROLLING_QUINTAR_FIELDS, SKUMPARADISE,
                                                        COBBLESTONE_CRAG,GREENSHIRE_REPRISE, CASTLE_SEQUOIA,))
        self.collect_by_name(ROLLING_QUINTAR_FIELDS)
        self.assert_region_entrances(CAPITAL_SEQUOIA,
                                     reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS,),
                                     unreachable_regions=(SKUMPARADISE, COBBLESTONE_CRAG,GREENSHIRE_REPRISE, CASTLE_SEQUOIA,))
        self.collect_by_name(SKUMPARADISE)
        self.assert_region_entrances(CAPITAL_SEQUOIA,
                                     reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE, ),
                                     unreachable_regions=(COBBLESTONE_CRAG,GREENSHIRE_REPRISE, CASTLE_SEQUOIA,))
        self.collect_by_name(COBBLESTONE_CRAG)
        self.assert_region_entrances(CAPITAL_SEQUOIA,
                                     reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE,
                                                        COBBLESTONE_CRAG,),
                                     unreachable_regions=(GREENSHIRE_REPRISE, CASTLE_SEQUOIA,))
        self.collect_by_name(GREENSHIRE_REPRISE)
        self.assert_region_entrances(CAPITAL_SEQUOIA,
                                     reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE,
                                                        COBBLESTONE_CRAG, GREENSHIRE_REPRISE, ),
                                     unreachable_regions=(CASTLE_SEQUOIA,))
        self.collect_by_name(CASTLE_SEQUOIA)
        self.assert_region_entrances(CAPITAL_SEQUOIA,
                                     reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE,
                                                        COBBLESTONE_CRAG, GREENSHIRE_REPRISE, CASTLE_SEQUOIA,))