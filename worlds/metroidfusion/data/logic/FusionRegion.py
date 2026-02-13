from .Connection import Connection
from .FusionLocation import FusionLocation

class FusionRegion:
    name: str
    connections: list[Connection] = []
    locations: list[FusionLocation] = []

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()