from ..constants.jobs import *
from ..constants.keys import *
from ..constants.regions import *
from ..constants.key_items import *
from ..constants.mounts import *
from ..constants.item_groups import *
from ..constants.region_passes import *
from .bases import CrystalProjectTestBase

class TestCapitalSequoiaNoLevelGating(CrystalProjectTestBase):
    options = {
        "levelGating": 0,
        "progressiveMountMode": 0,
    }

    def test_region_connections_no_items(self):
        self.assert_region_entrances(CAPITAL_SEQUOIA, reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE,),
                                     unreachable_regions=(COBBLESTONE_CRAG, GREENSHIRE_REPRISE, CASTLE_SEQUOIA,))

    def test_region_connections_courtyard_key(self):
        self.collect_by_name(COURTYARD_KEY)
        self.assert_region_entrances(CAPITAL_SEQUOIA, reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE, COBBLESTONE_CRAG,),
                                     unreachable_regions=(GREENSHIRE_REPRISE, CASTLE_SEQUOIA,))

    def test_region_connections_quintar_flute(self):
        self.collect(self.get_item_by_name(PROGRESSIVE_QUINTAR_WOODWIND))
        self.collect(self.get_item_by_name(PROGRESSIVE_QUINTAR_WOODWIND))
        self.assert_region_entrances(CAPITAL_SEQUOIA, reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE, COBBLESTONE_CRAG,),
                                     unreachable_regions=(GREENSHIRE_REPRISE, CASTLE_SEQUOIA,))

    def test_region_connections_five_jobs(self):
        self.set_collected_job_count(4)
        self.assert_region_entrances(CAPITAL_SEQUOIA, reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE,),
                                     unreachable_regions=(COBBLESTONE_CRAG, GREENSHIRE_REPRISE, CASTLE_SEQUOIA,))
        self.set_collected_job_count(5)
        self.assert_region_entrances(CAPITAL_SEQUOIA, reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE, GREENSHIRE_REPRISE,),
                                     unreachable_regions=(COBBLESTONE_CRAG, CASTLE_SEQUOIA,))

    def test_region_connections_ibek_owl(self):
        self.collect_by_name(IBEK_BELL)
        self.collect_by_name(OWL_DRUM)
        self.assert_region_entrances(CAPITAL_SEQUOIA, reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE, COBBLESTONE_CRAG, CASTLE_SEQUOIA,),
                                     unreachable_regions=(GREENSHIRE_REPRISE,))



class TestCapitalSequoiaWithRegionsanity(CrystalProjectTestBase):
    options = {
        "levelGating": 0,
        "progressiveMountMode": 0,
        "regionsanity": 1
    }

    def test_region_connections_no_items(self):
        self.assert_region_entrances(CAPITAL_SEQUOIA,
                                     unreachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, COBBLESTONE_CRAG,
                                                          GREENSHIRE_REPRISE, CASTLE_SEQUOIA, SKUMPARADISE,))

    def test_region_connections_with_just_passes(self):
        self.collect_passes()
        self.assert_region_entrances(CAPITAL_SEQUOIA, reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE,),
                                     unreachable_regions=( COBBLESTONE_CRAG, GREENSHIRE_REPRISE, CASTLE_SEQUOIA,))

    def test_region_connections_five_jobs_and_passes(self):
        self.set_collected_job_count(5)
        self.collect_passes()
        self.assert_region_entrances(CAPITAL_SEQUOIA,
                                     reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE,
                                                        GREENSHIRE_REPRISE,),
                                     unreachable_regions=(COBBLESTONE_CRAG, CASTLE_SEQUOIA,))

    def test_region_connections_ibek_owl_and_passes(self):
        self.collect_by_name(IBEK_BELL)
        self.collect_by_name(OWL_DRUM)
        self.collect_passes()
        self.assert_region_entrances(CAPITAL_SEQUOIA,
                                     reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE,
                                                        COBBLESTONE_CRAG,),
                                     unreachable_regions=(GREENSHIRE_REPRISE, CASTLE_SEQUOIA,))

        self.assert_region_entrances(CAPITAL_SEQUOIA,
                                     reachable_regions=(JOJO_SEWERS, ROLLING_QUINTAR_FIELDS, SKUMPARADISE,
                                                        COBBLESTONE_CRAG, CASTLE_SEQUOIA,),
                                     unreachable_regions=(GREENSHIRE_REPRISE,))