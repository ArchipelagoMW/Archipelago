from .bases import CrystalProjectTestBase
from ..options import *
from ..constants.jobs import *
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
                                                        WEST_COBBLESTONE_CRAG_AP_REGION, EAST_GREENSHIRE_AP_REGION, CASTLE_SEQUOIA_AP_REGION))

class TestRegionsanityOn(CrystalProjectTestBase):
    options = {
        "regionsanity": 1,
        "start_inventory_from_pool": {SPAWNING_MEADOWS_PASS: 1},
        "kill_bosses_mode": KillBossesMode.option_true,
    }

    def test_region_accessibility(self):
        self.set_collected_job_count(5)
        self.collect_mounts()
        self.collect_all_progressive_levels()
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION,
                                     unreachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION,
                                                          WEST_COBBLESTONE_CRAG_AP_REGION, EAST_GREENSHIRE_AP_REGION, CASTLE_SEQUOIA_AP_REGION,))
        self.collect_by_name(JOJO_SEWERS_PASS)
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION,
                                     reachable_regions=(JOJO_SEWERS_AP_REGION,),
                                     unreachable_regions=(ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION,
                                                          WEST_COBBLESTONE_CRAG_AP_REGION, EAST_GREENSHIRE_AP_REGION, CASTLE_SEQUOIA_AP_REGION,))
        self.collect_by_name(ROLLING_QUINTAR_FIELDS_PASS)
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION,
                                     reachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION,),
                                     unreachable_regions=(SKUMPARADISE_AP_REGION, WEST_COBBLESTONE_CRAG_AP_REGION, EAST_GREENSHIRE_AP_REGION, CASTLE_SEQUOIA_AP_REGION,))
        self.collect_by_name(SKUMPARADISE_PASS)
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION,
                                     reachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION,),
                                     unreachable_regions=(WEST_COBBLESTONE_CRAG_AP_REGION, EAST_GREENSHIRE_AP_REGION, CASTLE_SEQUOIA_AP_REGION,))
        self.collect_by_name(COBBLESTONE_CRAG_PASS)
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION,
                                     reachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION,
                                                        WEST_COBBLESTONE_CRAG_AP_REGION,),
                                     unreachable_regions=(EAST_GREENSHIRE_AP_REGION, CASTLE_SEQUOIA_AP_REGION,))
        self.collect_by_name(GREENSHIRE_REPRISE_PASS)
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION,
                                     reachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION,
                                                        WEST_COBBLESTONE_CRAG_AP_REGION, EAST_GREENSHIRE_AP_REGION,),
                                     unreachable_regions=(CASTLE_SEQUOIA_AP_REGION,))
        self.collect_by_name(CASTLE_SEQUOIA_PASS)
        self.assert_region_entrances(CAPITAL_SEQUOIA_AP_REGION,
                                     reachable_regions=(JOJO_SEWERS_AP_REGION, ROLLING_QUINTAR_FIELDS_AP_REGION, SKUMPARADISE_AP_REGION,
                                                        WEST_COBBLESTONE_CRAG_AP_REGION, EAST_GREENSHIRE_AP_REGION, CASTLE_SEQUOIA_AP_REGION,))
    
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
        self.collect_by_name([POKO_POKO_DESERT_PASS, ANCIENT_RESERVOIR_PASS, SARA_SARA_BAZAAR_PASS, SARA_SARA_BEACH_PASS])
        self.assertFalse(self.can_reach_region(ANCIENT_RESERVOIR_AP_REGION))
        self.assertTrue(self.can_reach_region(IBEK_CAVE_AP_REGION))
        self.assert_locations(unreachable_locations=[f"{ANCIENT_RESERVOIR_DISPLAY_NAME} Region Completion"])

        self.collect_by_name(PYRAMID_KEY)
        self.assertTrue(self.can_reach_region(ANCIENT_RESERVOIR_AP_REGION))
        self.assert_locations(reachable_locations=[f"{ANCIENT_RESERVOIR_DISPLAY_NAME} Region Completion"])

    def test_region_completion3(self):
        # This test attempts to validate region completion logic for spawning meadows
        self.assertFalse(self.can_reach_location(SPAWNING_MEADOWS_DISPLAY_NAME + " Region Completion"))
        self.assertFalse(self.can_reach_location(SPAWNING_MEADOWS_DISPLAY_NAME + " Boss - Shaku Summon"))
        self.assertFalse(self.can_reach_location(SPAWNING_MEADOWS_DISPLAY_NAME + " NPC - Butterfly Goo"))
        self.collect_all_progressive_levels()
        self.collect_by_name([SUMMONER_JOB])
        self.assertFalse(self.can_reach_location(SPAWNING_MEADOWS_DISPLAY_NAME + " Region Completion"))
        self.assertTrue(self.can_reach_location(SPAWNING_MEADOWS_DISPLAY_NAME + " Boss - Shaku Summon"))
        self.assertFalse(self.can_reach_location(SPAWNING_MEADOWS_DISPLAY_NAME + " NPC - Butterfly Goo"))
        self.collect(self.get_item_by_name(BLACK_SQUIRREL))
        self.collect(self.get_item_by_name(BLACK_SQUIRREL))
        self.assertFalse(self.can_reach_location(SPAWNING_MEADOWS_DISPLAY_NAME + " Region Completion"))
        self.assertTrue(self.can_reach_location(SPAWNING_MEADOWS_DISPLAY_NAME + " Boss - Shaku Summon"))
        self.assertFalse(self.can_reach_location(SPAWNING_MEADOWS_DISPLAY_NAME + " NPC - Butterfly Goo"))
        self.collect(self.get_item_by_name(BLACK_SQUIRREL))
        self.assertTrue(self.can_reach_location(SPAWNING_MEADOWS_DISPLAY_NAME + " Region Completion"))
        self.assertTrue(self.can_reach_location(SPAWNING_MEADOWS_DISPLAY_NAME + " Boss - Shaku Summon"))
        self.assertTrue(self.can_reach_location(SPAWNING_MEADOWS_DISPLAY_NAME + " NPC - Butterfly Goo"))

    def world_setup(self, *args, **kwargs):
        super().world_setup(seed=995067462)

