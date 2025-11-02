from ..constants.keys import *
from ..constants.ap_regions import *
from ..constants.mounts import *
from ..constants.region_passes import *

from .bases import CrystalProjectTestBase

class TestCapitalSequoiaNoLevelGating(CrystalProjectTestBase):
    options = {
        "level_gating": 0,
        "progressive_mount_mode": 0,
    }

    def test_region_connections_no_items(self):
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION, reachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION,),
                                     unreachable_regions=(COBBLESTONE_CRAG_AP_REGION, GREENSHIRE_REPRISE_AP_REGION, CASTLE_SEQUOIA_AP_REGION,))

    def test_region_connections_courtyard_key(self):
        self.collect_by_name(COURTYARD_KEY)
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION, reachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION, COBBLESTONE_CRAG_AP_REGION,),
                                     unreachable_regions=(GREENSHIRE_REPRISE_AP_REGION, CASTLE_SEQUOIA_AP_REGION,))

    def test_region_connections_quintar_flute(self):
        self.collect(self.get_item_by_name(PROGRESSIVE_QUINTAR_WOODWIND))
        self.collect(self.get_item_by_name(PROGRESSIVE_QUINTAR_WOODWIND))
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION, reachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION, COBBLESTONE_CRAG_AP_REGION,),
                                     unreachable_regions=(GREENSHIRE_REPRISE_AP_REGION, CASTLE_SEQUOIA_AP_REGION,))

    def test_region_connections_five_jobs(self):
        self.set_collected_job_count(4)
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION, reachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION,),
                                     unreachable_regions=(COBBLESTONE_CRAG_AP_REGION, GREENSHIRE_REPRISE_AP_REGION, CASTLE_SEQUOIA_AP_REGION,))
        self.set_collected_job_count(5)
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION, reachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION, GREENSHIRE_REPRISE_AP_REGION,),
                                     unreachable_regions=(COBBLESTONE_CRAG_AP_REGION, CASTLE_SEQUOIA_AP_REGION,))

    def test_region_connections_ibek_owl(self):
        self.collect_by_name(IBEK_BELL)
        self.collect_by_name(OWL_DRUM)
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION, reachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION, COBBLESTONE_CRAG_AP_REGION, CASTLE_SEQUOIA_AP_REGION,),
                                     unreachable_regions=(GREENSHIRE_REPRISE_AP_REGION,))



class TestCapitalSequoiaWithRegionsanity(CrystalProjectTestBase):
    options = {
        "level_gating": 0,
        "progressive_mount_mode": 0,
        "regionsanity": 1,
        "start_inventory_from_pool": {SPAWNING_MEADOWS_PASS: 1}
    }

    def test_region_connections_no_items(self):
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION,
                                     unreachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, COBBLESTONE_CRAG_AP_REGION,
                                                          GREENSHIRE_REPRISE_AP_REGION, CASTLE_SEQUOIA_AP_REGION, SKUMPARADISE_AP_REGION,))

    def test_region_connections_with_just_passes(self):
        self.collect_passes()
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION, reachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION,),
                                     unreachable_regions=(COBBLESTONE_CRAG_AP_REGION, GREENSHIRE_REPRISE_AP_REGION, CASTLE_SEQUOIA_AP_REGION,))

    def test_region_connections_five_jobs_and_passes(self):
        self.set_collected_job_count(5)
        self.collect_passes()
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION,
                                     reachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION,
                                                        GREENSHIRE_REPRISE_AP_REGION,),
                                     unreachable_regions=(COBBLESTONE_CRAG_AP_REGION, CASTLE_SEQUOIA_AP_REGION,))

    def test_region_connections_ibek_owl_and_passes(self):
        self.collect_by_name(IBEK_BELL)
        self.collect_by_name(OWL_DRUM)
        self.collect_passes()
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION,
                                     reachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION,
                                                        COBBLESTONE_CRAG_AP_REGION, CASTLE_SEQUOIA_AP_REGION,),
                                     unreachable_regions=(GREENSHIRE_REPRISE_AP_REGION,))