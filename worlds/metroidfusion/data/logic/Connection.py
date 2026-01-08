from typing import TYPE_CHECKING

from .Requirement import Requirement

if TYPE_CHECKING:
    from .FusionRegion import FusionRegion
    from ... import MetroidFusionOptions

class Connection:
    destination: "FusionRegion"
    requirements: list[Requirement]
    one_way: bool

    def __init__(self, destination, requirements, one_way=False):
        self.destination = destination
        self.requirements = requirements
        self.one_way = one_way

    def determine_destination(
            self,
            options: "MetroidFusionOptions",
            region_map: dict["FusionRegion", "FusionRegion"]):
        pass
