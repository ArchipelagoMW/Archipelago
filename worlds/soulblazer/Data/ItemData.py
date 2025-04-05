from dataclasses import dataclass, replace
from typing import Any

from BaseClasses import ItemClassification
from Utils import parse_yaml
from .Enums import ItemID, IDOffset, NPCID, SoulID
from ..Data import get_data_file_bytes, fromYamlOr, intFromYaml, listFromYaml, strFromYaml
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

    @staticmethod
    def from_yaml(yaml: Any) -> "SoulBlazerItemData":
        return SoulBlazerItemData(
            name = strFromYaml(yaml["name"]),
            id = intFromYaml(yaml["id"]),
            operand = intFromYaml(yaml["operand"]),
            classification = intFromYaml(yaml["classification"]),
            description = fromYamlOr(yaml["description"], strFromYaml, ""),
        )

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
class SoulBlazerItemsData:
    swords: list[SoulBlazerItemData]
    armors: list[SoulBlazerItemData]
    magics: list[SoulBlazerItemData]
    inventory_items: list[SoulBlazerItemData]
    misc_items: list[SoulBlazerItemData]
    npc_releases: list[SoulBlazerItemData]
    souls: list[SoulBlazerItemData]
    special_items: list[SoulBlazerItemData]

    @staticmethod
    def from_yaml(yaml: Any) -> "SoulBlazerItemsData":
        return SoulBlazerItemsData(
            swords = listFromYaml(yaml["swords"], SoulBlazerItemData.from_yaml),
            armors = listFromYaml(yaml["armors"], SoulBlazerItemData.from_yaml),
            magics = listFromYaml(yaml["magics"], SoulBlazerItemData.from_yaml),
            inventory_items = listFromYaml(yaml["inventory_items"], SoulBlazerItemData.from_yaml),
            misc_items = listFromYaml(yaml["misc_items"], SoulBlazerItemData.from_yaml),
            npc_releases = listFromYaml(yaml["npc_releases"], SoulBlazerItemData.from_yaml),
            souls = listFromYaml(yaml["souls"], SoulBlazerItemData.from_yaml),
            special_items = listFromYaml(yaml["special_items"], SoulBlazerItemData.from_yaml),
        )

    @property
    def all_items(self) -> list[SoulBlazerItemData]:
        return [
            *self.swords,
            *self.armors,
            *self.magics,
            *self.inventory_items,
            *self.misc_items,
            *self.npc_releases,
            *self.souls,
            *self.special_items,
        ]

items_data_bytes = get_data_file_bytes("SoulBlazerItems.yaml")
items_data_yaml = parse_yaml(items_data_bytes)
items_data: SoulBlazerItemsData = SoulBlazerItemsData.from_yaml(items_data_yaml)
"""A collection of SoulBlazer Item data loaded from SoulBlazerItems.yaml."""

ItemID.full_names = {
    data.id: data.name
    for data in [
        *items_data.swords,
        *items_data.armors,
        *items_data.magics,
        *items_data.inventory_items,
        *items_data.misc_items,
        *items_data.special_items,
    ]
}
ItemID.full_names.update(
    {ItemID.LAIR_RELEASE: "Lair Release", ItemID.SOUL: "Soul", ItemID.REMOTE_ITEM: "Remote Item"}
)

NPCID.full_names = {data.operand: data.name for data in items_data.npc_releases}

SoulID.full_names = {data.operand: data.name for data in items_data.souls}
