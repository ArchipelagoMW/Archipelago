from dataclasses import dataclass
from typing import List

from .position import Point2


@dataclass
class PowerSource:
    position: Point2
    radius: float
    unit_tag: int

    def __post_init__(self):
        assert self.radius > 0

    @classmethod
    def from_proto(cls, proto):
        return PowerSource(Point2.from_proto(proto.pos), proto.radius, proto.tag)

    def covers(self, position: Point2) -> bool:
        return self.position.distance_to(position) <= self.radius

    def __repr__(self):
        return f"PowerSource({self.position}, {self.radius})"


@dataclass
class PsionicMatrix:
    sources: List[PowerSource]

    @classmethod
    def from_proto(cls, proto):
        return PsionicMatrix([PowerSource.from_proto(p) for p in proto])

    def covers(self, position: Point2) -> bool:
        return any(source.covers(position) for source in self.sources)
