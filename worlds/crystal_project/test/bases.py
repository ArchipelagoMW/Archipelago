from test.bases import WorldTestBase
from ..constants.mounts import *
from ..constants.regions import *
from ..constants.key_items import *
from ..constants.item_groups import *

class CrystalProjectTestBase(WorldTestBase):
    game = "Crystal Project"
    run_default_tests = False

    def assert_region_entrances(self, region: str, reachable_regions: tuple[str, ...] | None=None, unreachable_regions: tuple[str, ...] | None=None):
        self.world.origin_region_name = region

        if isinstance(reachable_regions, tuple):
            for reachable in reachable_regions:
                with self.subTest(msg="Test Can Reach Entrance", region=region, reachable_region=reachable):
                    self.assertTrue(self.can_reach_entrance(region + " -> " + reachable))

        if isinstance(unreachable_regions, tuple):
            for unreachable in unreachable_regions:
                with self.subTest(msg="Test Cannot Reach Entrance", region=region, unreachable_region=unreachable):
                    self.assertFalse(self.can_reach_entrance(region + " -> " + unreachable))


    def assert_locations(self, reachable_locations: list[str] | None=None, unreachable_locations: list[str] | None=None):
        if isinstance(reachable_locations, list):
            for reachable in reachable_locations:
                with self.subTest(msg="Test Can Reach Location", reachable_location=reachable):
                    self.assertTrue(self.can_reach_location(reachable))

        if isinstance(unreachable_locations, list):
            for unreachable in unreachable_locations:
                with self.subTest(msg="Test Cannot Reach Location", unreachable_location=unreachable):
                    self.assertFalse(self.can_reach_location(unreachable))

    def set_collected_job_count(self, job_count: int):
        """Guarantees that you have collected X non-starting jobs.
        If you run this twice in a single test, i.e. collect_jobs(3) and then collect_jobs(4) you should assume you have 4 jobs collected, not 7"""
        self.collect(self.get_items_by_name(self.world.item_name_groups[JOB])[:job_count])


    def collect_mounts(self):
        self.collect_by_name([PROGRESSIVE_SALMON_VIOLA, PROGRESSIVE_QUINTAR_WOODWIND, IBEK_BELL, OWL_DRUM])


    def collect_level_caps(self):
        self.collect_by_name(PROGRESSIVE_LEVEL_CAP)


    def collect_mounts_and_level_caps(self):
        self.collect_mounts()
        self.collect_level_caps()