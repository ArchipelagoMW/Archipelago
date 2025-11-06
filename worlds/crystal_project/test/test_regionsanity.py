from .bases import CrystalProjectTestBase
from ..constants.region_passes import *
from ..constants.ap_regions import *
from ..constants.display_regions import *
from ..constants.teleport_stones import *
from ..constants.keys import *
from ..constants.key_items import *
from ..constants.mounts import *

class TestRegionsanityOff(CrystalProjectTestBase):
    options = {
        "regionsanity": 0,
    }

    def test_region_accessibility(self):
        self.set_collected_job_count(5)
        self.collect_mounts()
        self.collect_all_progressive_levels()
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION,
                                     reachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION,
                                                        COBBLESTONE_CRAG_AP_REGION, GREENSHIRE_REPRISE_AP_REGION, CASTLE_SEQUOIA_AP_REGION))

class TestRegionsanityOn(CrystalProjectTestBase):
    options = {
        "regionsanity": 1,
        "start_inventory_from_pool": {SPAWNING_MEADOWS_PASS: 1}
    }

    def test_region_accessibility(self):
        self.set_collected_job_count(5)
        self.collect_mounts()
        self.collect_all_progressive_levels()
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION,
                                     unreachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION,
                                                          COBBLESTONE_CRAG_AP_REGION, GREENSHIRE_REPRISE_AP_REGION, CASTLE_SEQUOIA_AP_REGION,))
        self.collect_by_name(JOJO_SEWERS_PASS)
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION,
                                     reachable_regions=(JOJO_SEWERS_AP_REGION,),
                                     unreachable_regions=(ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION,
                                                          COBBLESTONE_CRAG_AP_REGION, GREENSHIRE_REPRISE_AP_REGION, CASTLE_SEQUOIA_AP_REGION,))
        self.collect_by_name(ROLLING_QUINTAR_FIELDS_PASS)
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION,
                                     reachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION,),
                                     unreachable_regions=(SKUMPARADISE_AP_REGION, COBBLESTONE_CRAG_AP_REGION, GREENSHIRE_REPRISE_AP_REGION, CASTLE_SEQUOIA_AP_REGION,))
        self.collect_by_name(SKUMPARADISE_PASS)
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION,
                                     reachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION,),
                                     unreachable_regions=(COBBLESTONE_CRAG_AP_REGION, GREENSHIRE_REPRISE_AP_REGION, CASTLE_SEQUOIA_AP_REGION,))
        self.collect_by_name(COBBLESTONE_CRAG_PASS)
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION,
                                     reachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION,
                                                        COBBLESTONE_CRAG_AP_REGION,),
                                     unreachable_regions=(GREENSHIRE_REPRISE_AP_REGION, CASTLE_SEQUOIA_AP_REGION,))
        self.collect_by_name(GREENSHIRE_REPRISE_PASS)
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION,
                                     reachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION,
                                                        COBBLESTONE_CRAG_AP_REGION, GREENSHIRE_REPRISE_AP_REGION,),
                                     unreachable_regions=(CASTLE_SEQUOIA_AP_REGION,))
        self.collect_by_name(CASTLE_SEQUOIA_PASS)
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION,
                                     reachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION,
                                                        COBBLESTONE_CRAG_AP_REGION, GREENSHIRE_REPRISE_AP_REGION, CASTLE_SEQUOIA_AP_REGION,))
    
    def test_has_rental_quintar(self):
        self.set_collected_job_count(5)
        self.collect(self.get_item_by_name(PROGRESSIVE_MOUNT))
        self.collect(self.get_item_by_name(GAEA_STONE))
        self.collect_all_progressive_levels()
        # Checking reachability of Salmon Pass tests whether or not has_rental_quintar is correctly making sure you can use the rental desk in rolling quintar fields
        self.collect_by_name(SALMON_PASS_PASS)
        self.collect_by_name(CAPITAL_SEQUOIA_PASS)
        self.collect_by_name(GREENSHIRE_REPRISE_PASS)
        self.assertFalse(self.can_reach_region(SALMON_PASS_EAST_AP_REGION))
        self.collect_by_name(ROLLING_QUINTAR_FIELDS_PASS)
        self.assertTrue(self.can_reach_region(SALMON_PASS_EAST_AP_REGION))

    def test_region_completion(self):
        #Verifying that all subregions must be reachable before the region completion location is reachable
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR_AP_REGION))
        self.collect_mounts()
        self.collect_all_progressive_levels()
        self.collect_by_name([POKO_POKO_DESERT_PASS, ANCIENT_RESERVOIR_PASS, SARA_SARA_BAZAAR_PASS, SARA_SARA_BEACH_EAST_PASS])
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR_AP_REGION))
        self.assertTrue(self.can_reach_region(IBEK_CAVE_AP_REGION))
        self.assert_locations(unreachable_locations=[f"{ANCIENT_RESERVOIR_DISPLAY_NAME} Region Completion"])

        self.collect_by_name(PYRAMID_KEY)
        self.assertTrue(self.can_reach_region(ANCIENT_RESERVOIR_AP_REGION))
        self.assert_locations(reachable_locations=[f"{ANCIENT_RESERVOIR_DISPLAY_NAME} Region Completion"])

    def test_region_completion2(self):
        # This test validates that you must be able to complete each location in a display region before the region completion will be accessible
        self.assertFalse(self.can_reach_region(SLIP_GLIDE_RIDE_AP_REGION))
        self.collect_mounts()
        self.collect_all_progressive_levels()
        self.collect_by_name([TRITON_STONE, TALL_TALL_HEIGHTS_PASS, NORTHERN_CAVE_PASS, SLIP_GLIDE_RIDE_PASS])
        self.assertTrue(self.can_reach_region(UPPER_ICE_LAKES_AP_REGION))
        self.assertTrue(self.can_reach_region(MIDDLE_NORTHERN_CAVE_AP_REGION))
        self.assertTrue(self.can_reach_region(SLIP_GLIDE_RIDE_AP_REGION))
        self.assert_locations(unreachable_locations=[SLIP_GLIDE_RIDE_DISPLAY_NAME + " Chest - Back out to 1st room"])
        self.assert_locations(unreachable_locations=[f"{SLIP_GLIDE_RIDE_DISPLAY_NAME} Region Completion"])

        self.collect_by_name(RED_DOOR_KEY)
        self.assert_locations(reachable_locations=[f"{SLIP_GLIDE_RIDE_DISPLAY_NAME} Region Completion"])