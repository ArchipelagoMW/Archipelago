from dataclasses import dataclass, field
from typing import FrozenSet, List, NamedTuple

# A WitnessRule is just an or-chain of and-conditions.
# It represents the set of all options that could fulfill this requirement.
# E.g. if something requires "Dots or (Shapers and Stars)", it'd be represented as: {{"Dots"}, {"Shapers, "Stars"}}
# {} is an unusable requirement.
# {{}} is an always usable requirement.
WitnessRule = FrozenSet[FrozenSet[str]]


@dataclass
class AreaDefinition:
    name: str
    regions: List[str] = field(default_factory=list)


@dataclass
class RegionDefinition:
    name: str
    short_name: str
    area: AreaDefinition
    logical_entities: List[int] = field(default_factory=list)
    physical_entities: List[int] = field(default_factory=list)


@dataclass
class EntityDefinition:
    entity_name: str
    entity_id: int
    region: RegionDefinition | None
    entity_type: str
    location_type: str | None
    area: AreaDefinition
    order: int = 0


class ConnectionDefinition(NamedTuple):
    target_region: str
    traversal_rule: WitnessRule

    @property
    def can_be_traversed(self) -> bool:
        return bool(self.traversal_rule)
