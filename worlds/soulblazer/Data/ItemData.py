from dataclasses import dataclass, replace
from dataclass_wizard import YAMLWizard
from BaseClasses import ItemClassification
from enum import Enum
from .Enums import ItemID, IDOffset
from ..Util import int_to_bcd

@dataclass(frozen=True)
class SoulBlazerItemData:
    name: str
    """String representation of the item"""

    id: int
    """Internal item ID"""

    operand: int
    """Either Gems/Exp Quantity or Lair ID"""

    classification: int | ItemClassification

    description: str = ""

    def duplicate(self, **changes) -> "SoulBlazerItemData":
        """Returns a copy of this ItemData with the specified changes."""
        return replace(self, **changes)

    @property
    def code(self) -> int:
        """The unique ID used by archipelago for this item"""

        if self.id == ItemID.LAIR_RELEASE:
            return IDOffset.BASE_ID + IDOffset.LAIR_ID_OFFSET + self.operand
        elif self.id == ItemID.SOUL:
            return IDOffset.BASE_ID + IDOffset.SOUL_OFFSET + self.operand
        return IDOffset.BASE_ID + self.id

    @property
    def operand_bcd(self) -> int:
        return int_to_bcd(self.operand)

    @property
    def operand_for_id(self) -> int:
        if self.id == ItemID.GEMS or self.id == ItemID.EXP:
            return self.operand_bcd
        return self.operand
    
@dataclass(frozen=True)
class SoulBlazerItemsData(YAMLWizard):
    swords: list[SoulBlazerItemData]
    armors: list[SoulBlazerItemData]
    magics: list[SoulBlazerItemData]
    inventory_items: list[SoulBlazerItemData]
    misc_items: list[SoulBlazerItemData]
    npc_releases: list[SoulBlazerItemData]
    souls: list[SoulBlazerItemData]
    special_items: list[SoulBlazerItemData]

    @property
    def all_items(self) -> list[SoulBlazerItemData]:
        return [*self.swords, *self.armors, *self.magics, *self.inventory_items, *self.misc_items, *self.npc_releases, *self.souls, *self.special_items]

##TODO: Where to load the yaml?
#items_data: SoulBlazerItemsData = SoulBlazerItemsData.from_yaml_file("worlds/soulblazer/Data/SoulBlazerItems.yaml")
#"""A collection of SoulBlazer Item data loaded from SoulBlazerItems.yaml."""

