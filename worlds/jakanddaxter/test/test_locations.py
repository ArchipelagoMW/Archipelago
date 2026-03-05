import typing

from .bases import JakAndDaxterTestBase
from ..game_id import jak1_id
from ..regs.region_base import JakAndDaxterRegion
from ..locs import (scout_locations as scouts,
                    special_locations as specials,
                    orb_cache_locations as caches,
                    orb_locations as orbs)


class LocationsTest(JakAndDaxterTestBase):

    def get_regions(self):
        return [typing.cast(JakAndDaxterRegion, reg) for reg in self.multiworld.get_regions(self.player)]

    def test_count_cells(self):
        
        for level in self.level_info:
            cell_count = 0
            sublevels = [reg for reg in self.get_regions() if reg.level_name == level]
            for sl in sublevels:
                for loc in sl.locations:
                    if loc.address in range(jak1_id, jak1_id + scouts.fly_offset):
                        cell_count += 1
            self.assertEqual(self.level_info[level]["cells"] - 1, cell_count, level)  # Don't count the Free 7 Cells.

    def test_count_flies(self):
        for level in self.level_info:
            fly_count = 0
            sublevels = [reg for reg in self.get_regions() if reg.level_name == level]
            for sl in sublevels:
                for loc in sl.locations:
                    if loc.address in range(jak1_id + scouts.fly_offset, jak1_id + specials.special_offset):
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
                    if loc.address in range(jak1_id + caches.orb_cache_offset, jak1_id + orbs.orb_offset):
                        cache_count += 1
            self.assertEqual(self.level_info[level]["caches"], cache_count, level)
