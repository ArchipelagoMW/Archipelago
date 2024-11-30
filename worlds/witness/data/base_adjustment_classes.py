from dataclasses import dataclass

from worlds.witness.data.utils import WitnessRule


@dataclass(frozen=True)
class OptionAdjustment:
    pass


@dataclass(frozen=True)
class AddedItem(OptionAdjustment):
    item_name: str


@dataclass(frozen=True)
class RemoveItem(OptionAdjustment):
    item_name: str


@dataclass(frozen=True)
class AddToStartInventory(OptionAdjustment):
    item_name: str


@dataclass(frozen=True)
class AddedLocation(OptionAdjustment):
    entity_name: str


@dataclass(frozen=True)
class DisabledEntity(OptionAdjustment):
    entity_name: str


@dataclass(frozen=True)
class AddedEvent(OptionAdjustment):
    event_item_name: str
    target_entity: str
    trigger_entities: list[str]


@dataclass(frozen=True)
class RequirementChange(OptionAdjustment):
    entity_hex: str
    new_required_entities: str | None
    new_required_symbols: str | None


@dataclass(frozen=True)
class RegionDefinitionChange(OptionAdjustment):
    region_definition_string: str  # This should get a rework eventually


@dataclass(frozen=True)
class AddedConnection(OptionAdjustment):
    source_region: str
    target_region: str
    entity_requirement: str
