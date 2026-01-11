from .Connection import Connection
from .FFTLocation import FFTLocation


class FFTRegion:
    name: str
    connections: list[Connection] = []
    locations: list[FFTLocation] = []

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()