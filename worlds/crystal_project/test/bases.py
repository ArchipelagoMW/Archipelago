from test.bases import WorldTestBase
from ..constants.mounts import *
from ..constants.regions import *
from ..constants.key_items import *


class CrystalProjectTestBase(WorldTestBase):
    game = "Crystal Project"

    def assert_region_entrances(self, region: str, reachable_regions: tuple[str, ...] | None=None, unreachable_regions: tuple[str, ...] | None=None):
        menu_entrance: str = MENU + " -> " + region
        menu_entrances = self.multiworld.get_entrances(self.world.player)
        menu_entrance_exists: bool = False
        for entrance in menu_entrances:
            if entrance.name == menu_entrance:
                menu_entrance_exists = True

        if not menu_entrance_exists:
            self.multiworld.get_region(MENU, self.world.player).add_exits([region])

        if isinstance(reachable_regions, tuple):
            for reachable in reachable_regions:
                with self.subTest(msg="Test Can Reach Entrance", region=region, reachable_region=reachable):
                    self.assertTrue(self.can_reach_entrance(region + " -> " + reachable))

        if isinstance(unreachable_regions, tuple):
            for unreachable in unreachable_regions:
                with self.subTest(msg="Test Cannot Reach Entrance", region=region, unreachable_region=unreachable):
                    self.assertFalse(self.can_reach_entrance(region + " -> " + unreachable))

    def collect_mounts(self):
        self.collect_by_name([PROGRESSIVE_SALMON_VIOLA, PROGRESSIVE_QUINTAR_WOODWIND, IBEK_BELL, OWL_DRUM])

    def collect_level_caps(self):
        self.collect_by_name(PROGRESSIVE_LEVEL_CAP)

    def collect_mounts_and_level_caps(self):
        self.collect_mounts()
        self.collect_level_caps()