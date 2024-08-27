import typing

from . import JakAndDaxterTestBase
from .. import jak1_id
from ..regs.RegionBase import JakAndDaxterRegion
from ..locs import (ScoutLocations as Scouts,
                    SpecialLocations as Specials)


class LocationsTest(JakAndDaxterTestBase):

    def test_count_cells(self):
        regions = [typing.cast(JakAndDaxterRegion, reg) for reg in self.multiworld.get_regions(self.player)]
        for level in self.level_info:
            cell_count = 0
            sublevels = [reg for reg in regions if reg.level_name == level]
            for sl in sublevels:
                for loc in sl.locations:
                    if loc.address in range(jak1_id, jak1_id + Scouts.fly_offset):
                        cell_count += 1
            self.assertEqual(self.level_info[level]["cells"] - 1, cell_count, level)  # Don't count the Free 7 Cells.

    def test_count_flies(self):
        regions = [typing.cast(JakAndDaxterRegion, reg) for reg in self.multiworld.get_regions(self.player)]
        for level in self.level_info:
            fly_count = 0
            sublevels = [reg for reg in regions if reg.level_name == level]
            for sl in sublevels:
                for loc in sl.locations:
                    if loc.address in range(jak1_id + Scouts.fly_offset, jak1_id + Specials.special_offset):
                        fly_count += 1
            self.assertEqual(self.level_info[level]["flies"], fly_count, level)

    def test_count_orbs(self):
        regions = [typing.cast(JakAndDaxterRegion, reg) for reg in self.multiworld.get_regions(self.player)]
        for level in self.level_info:
            sublevels = [reg for reg in regions if reg.level_name == level]
            orb_count = sum([reg.orb_count for reg in sublevels])
            self.assertEqual(self.level_info[level]["orbs"], orb_count, level)
