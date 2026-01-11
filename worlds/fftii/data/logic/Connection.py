from typing import TYPE_CHECKING

from .Requirement import Requirement

if TYPE_CHECKING:
    from .FFTRegion import FFTRegion

class Connection:
    destination: "FFTRegion"
    requirements: list[Requirement]

    def __init__(self, destination, requirements = None):
        if requirements is None:
            requirements = list()
        self.destination = destination
        self.requirements = requirements
