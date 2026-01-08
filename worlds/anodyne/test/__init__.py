from typing import ClassVar

from test.bases import WorldTestBase
from worlds.anodyne import RegionEnum


class AnodyneTestBase(WorldTestBase):
    game = "Anodyne"
    player: ClassVar[int] = 1
    
    def can_reach_region(self, region:RegionEnum):
        return super().can_reach_region(str(region))
