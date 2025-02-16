import typing

from ..test import JakAndDaxterTestBase
from ..GameID import jak1_id
from ..regs.RegionBase import JakAndDaxterRegion
from ..locs import (ScoutLocations as Scouts,
                    SpecialLocations as Specials,
                    OrbCacheLocations as Caches,
                    OrbLocations as Orbs)


class LocationsTest(JakAndDaxterTestBase):

    def get_regions(self):
        return [typing.cast(JakAndDaxterRegion, reg) for reg in self.multiworld.get_regions(self.player)]

    def test_count_cells(self):
        
        for level in self.level_info:
            cell_count = 0
            sublevels = [reg for reg in self.get_regions() if reg.level_name == level]
            for sl in sublevels:
                for loc in sl.locations:
                    if loc.address in range(jak1_id, jak1_id + Scouts.fly_offset):
                        cell_count += 1
            self.assertEqual(self.level_info[level]["cells"] - 1, cell_count, level)  # Don't count the Free 7 Cells.

    def test_count_flies(self):
        for level in self.level_info:
            fly_count = 0
            sublevels = [reg for reg in self.get_regions() if reg.level_name == level]
            for sl in sublevels:
                for loc in sl.locations:
                    if loc.address in range(jak1_id + Scouts.fly_offset, jak1_id + Specials.special_offset):
                        fly_count += 1
            self.assertEqual(self.level_info[level]["flies"], fly_count, level)

    def test_count_orbs(self):
        for level in self.level_info:
            sublevels = [reg for reg in self.get_regions() if reg.level_name == level]
            orb_count = sum([reg.orb_count for reg in sublevels])
            self.assertEqual(self.level_info[level]["orbs"], orb_count, level)

    def test_count_caches(self):
        for level in self.level_info:
            cache_count = 0
            sublevels = [reg for reg in self.get_regions() if reg.level_name == level]
            for sl in sublevels:
                for loc in sl.locations:
                    if loc.address in range(jak1_id + Caches.orb_cache_offset, jak1_id + Orbs.orb_offset):
                        cache_count += 1
            self.assertEqual(self.level_info[level]["caches"], cache_count, level)
