import enum
import typing
from dataclasses import dataclass
from typing import Optional, Union, Dict, Type

from BaseClasses import Item, ItemClassification
from ..mission_tables import SC2Race


class ItemFilterFlags(enum.IntFlag):
    """Removed > Start Inventory > Locked > Excluded > Requested > Culled"""
    Available = 0
    StartInventory = enum.auto()
    Locked = enum.auto()
    """Used to flag items that are never allowed to be culled."""
    LogicLocked = enum.auto()
    """Locked by item cull logic checks; logic-locked w/a upgrades may be removed if all parents are removed"""
    Requested = enum.auto()
    """Soft-locked items by item count checks during item culling; may be re-added"""
    Removed = enum.auto()
    """Marked for immediate removal"""
    UserExcluded = enum.auto()
    """Excluded by the user; display an error message if failing to exclude"""
    FilterExcluded = enum.auto()
    """Excluded by item filtering"""
    Culled = enum.auto()
    """Soft-removed by the item culling"""
    NonLocal = enum.auto()
    Plando = enum.auto()
    AllowedOrphan = enum.auto()
    """Used to flag items that shouldn't be filtered out with their parents"""
    ForceProgression = enum.auto()
    """Used to flag items that aren't classified as progression by default"""

    Unexcludable = StartInventory|Plando|Locked|LogicLocked
    UnexcludableUpgrade = StartInventory|Plando|Locked
    Uncullable = StartInventory|Plando|Locked|LogicLocked|Requested
    Excluded = UserExcluded|FilterExcluded
    RequestedOrBetter = StartInventory|Locked|LogicLocked|Requested
    CulledOrBetter = Removed|Excluded|Culled


class StarcraftItem(Item):
    game: str = "Starcraft 2"
    filter_flags: ItemFilterFlags = ItemFilterFlags.Available

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int, filter_flags: ItemFilterFlags = ItemFilterFlags.Available):
        super().__init__(name, classification, code, player)
        self.filter_flags = filter_flags

class ItemTypeEnum(enum.Enum):
    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, name: str, flag_word: int):
        self.display_name = name
        self.flag_word = flag_word


class TerranItemType(ItemTypeEnum):
    Armory_1 = "Armory", 0
    """General Terran unit upgrades"""
    Armory_2 = "Armory", 1
    Armory_3 = "Armory", 2
    Armory_4 = "Armory", 3
    Armory_5 = "Armory", 4
    Armory_6 = "Armory", 5
    Armory_7 = "Armory", 6
    Progressive = "Progressive Upgrade", 7
    Laboratory = "Laboratory", 8
    Upgrade = "Upgrade", 9
    Unit = "Unit", 10
    Building = "Building", 11
    Mercenary = "Mercenary", 12
    Nova_Gear = "Nova Gear", 13
    Progressive_2 = "Progressive Upgrade", 14
    Unit_2 = "Unit", 15


class ZergItemType(ItemTypeEnum):
    Ability = "Ability", 0
    """Kerrigan abilities"""
    Mutation_1 = "Mutation", 1
    Strain = "Strain", 2
    Morph = "Morph", 3
    Upgrade = "Upgrade", 4
    Mercenary = "Mercenary", 5
    Unit = "Unit", 6
    Level = "Level", 7
    """Kerrigan level packs"""
    Primal_Form = "Primal Form", 8
    Evolution_Pit = "Evolution Pit", 9
    """Zerg global economy upgrades, like automated extractors"""
    Mutation_2 = "Mutation", 10
    Mutation_3 = "Mutation", 11
    Mutation_4 = "Mutation", 12
    Progressive = "Progressive Upgrade", 13
    Mutation_5 = "Mutation", 14


class ProtossItemType(ItemTypeEnum):
    Unit = "Unit", 0
    Unit_2 = "Unit", 1
    Upgrade = "Upgrade", 2
    Building = "Building", 3
    Progressive = "Progressive Upgrade", 4
    Spear_Of_Adun = "Spear of Adun", 5
    Solarite_Core = "Solarite Core", 6
    """Protoss global effects, such as reconstruction beam or automated assimilators"""
    Forge_1 = "Forge", 7
    """General Protoss unit upgrades"""
    Forge_2 = "Forge", 8
    """General Protoss unit upgrades"""
    Forge_3 = "Forge", 9
    """General Protoss unit upgrades"""
    Forge_4 = "Forge", 10
    """General Protoss unit upgrades"""
    Forge_5 = "Forge", 11
    """General Protoss unit upgrades"""
    War_Council = "War Council", 12
    War_Council_2 = "War Council", 13
    ShieldRegeneration = "Shield Regeneration Group", 14


class FactionlessItemType(ItemTypeEnum):
    Minerals = "Minerals", 0
    Vespene = "Vespene", 1
    Supply = "Supply", 2
    MaxSupply = "Max Supply", 3
    BuildingSpeed = "Building Speed", 4
    Nothing = "Nothing Group", 5
    Deprecated = "Deprecated", 6
    MaxSupplyTrap = "Max Supply Trap", 7
    ResearchSpeed = "Research Speed", 8
    ResearchCost = "Research Cost", 9
    Keys = "Keys", -1


ItemType = Union[TerranItemType, ZergItemType, ProtossItemType, FactionlessItemType]
race_to_item_type: Dict[SC2Race, Type[ItemTypeEnum]] = {
    SC2Race.ANY: FactionlessItemType,
    SC2Race.TERRAN: TerranItemType,
    SC2Race.ZERG: ZergItemType,
    SC2Race.PROTOSS: ProtossItemType,
}


class ItemData(typing.NamedTuple):
    code: int
    type: ItemType
    number: int  # Important for bot commands to send the item into the game
    race: SC2Race
    classification: ItemClassification = ItemClassification.useful
    quantity: int = 1
    parent: typing.Optional[str] = None
    important_for_filtering: bool = False

    def is_important_for_filtering(self):
        return (
                self.important_for_filtering
                or self.classification == ItemClassification.progression
                or self.classification == ItemClassification.progression_skip_balancing
        )

@dataclass
class FilterItem:
    name: str
    data: ItemData
    index: int = 0
    flags: ItemFilterFlags = ItemFilterFlags.Available
