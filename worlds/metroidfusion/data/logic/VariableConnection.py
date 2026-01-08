from typing import TYPE_CHECKING

from .Connection import Connection
from .FusionRegion import FusionRegion
from .RegionMap import full_default_region_map

if TYPE_CHECKING:
    from ... import MetroidFusionOptions

class VariableConnection(Connection):
    def determine_destination(
            self,
            options: "MetroidFusionOptions",
            region_map: dict[FusionRegion, FusionRegion]):
        if self.destination in region_map.keys():
            origin = full_default_region_map[self.destination]
            self.destination = region_map[origin]
