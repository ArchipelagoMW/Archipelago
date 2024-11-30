from dataclasses import dataclass

from ..utils import WitnessRule


@dataclass(frozen=True)
class Adjustment:
    pass


@dataclass(frozen=True)
class AddedItem(Adjustment):
    item_name: str


@dataclass(frozen=True)
class RemoveItem(Adjustment):
    item_name: str


@dataclass(frozen=True)
class AddToStartInventory(Adjustment):
    item_name: str


@dataclass(frozen=True)
class AddedLocation(Adjustment):
    entity_hex: str


@dataclass(frozen=True)
class DisabledLocation(Adjustment):
    entity_hex: str


@dataclass(frozen=True)
class AddedEvent(Adjustment):
    event_item_name: str
    target_entity: str
    trigger_entities: list[str]


@dataclass(frozen=True)
class RequirementChange(Adjustment):
    entity_hex: str
    required_entities: WitnessRule
    required_symbols: WitnessRule


@dataclass(frozen=True)
class RegionDefinitionChange(Adjustment):
    region_definition_string: str  # This should get a rework eventually


@dataclass(frozen=True)
class AddedConnection(Adjustment):
    source_region: str
    target_region: str
