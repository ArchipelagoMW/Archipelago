from BaseClasses import Item, ItemClassification
from typing import TYPE_CHECKING
from .Data.Enums import ItemID, NPCRewardID, SoulID
from .Data.ItemData import SoulBlazerItemData, items_data

if TYPE_CHECKING:
    from . import SoulBlazerWorld


class SoulBlazerItem(Item):
    game = "Soul Blazer"

    def __init__(self, player: int, itemData: SoulBlazerItemData):
        super().__init__(itemData.name, ItemClassification(itemData.classification), itemData.code, player)
        self._itemData = itemData

    def set_operand(self, value: int) -> "SoulBlazerItem":
        self._itemData = self._itemData.duplicate(operand=value)
        return self

    @property
    def id(self) -> int:
        return self._itemData.id

    @property
    def operand(self) -> int:
        return self._itemData.operand

    @operand.setter
    def operand(self, value: int):
        self._itemData.operand = value

    @property
    def operand_bcd(self) -> int:
        return self._itemData.operand_bcd

    @operand_bcd.setter
    def operand_bcd(self, bcd: int):
        self._itemData.operand_bcd = bcd

    @property
    def operand_for_id(self) -> int:
        return self._itemData.operand_for_id


herb_count_vanilla = 20
"""Number of Herbs in vanilla item pool"""

bottle_count_vanilla = 7
"""Number of Strange Bottles in vanilla item pool"""

nothing_count_vanilla = 3
"""Number of 'Nothing' rewards in vanilla item pool"""

gem_values_vanilla = [1, 12, 40, 50, 50, 50, 50, 50, 60, 60, 80, 80, 80, 80, 80, 100, 100, 100, 100, 150, 200]
"""Gem reward values in vanilla item pool"""

exp_values_vanilla = [1, 30, 80, 150, 180, 200, 250, 300, 300, 300, 300, 300, 400]
"""Exp reward values in vanilla item pool"""


def create_gem_pool(world: "SoulBlazerWorld") -> list[int]:
    if world.options.gem_exp_pool == "random_range":
        return [world.random.randint(1, 999) for _ in range(len(gem_values_vanilla))]
    if world.options.gem_exp_pool == "improved":
        return [gem * 2 for gem in gem_values_vanilla]

    return gem_values_vanilla[:]


def create_exp_pool(world: "SoulBlazerWorld") -> list[int]:
    if world.options.gem_exp_pool == "random_range":
        return [world.random.randint(1, 9999) for _ in range(len(exp_values_vanilla))]
    if world.options.gem_exp_pool == "improved":
        return [exp * 10 for exp in exp_values_vanilla]

    return exp_values_vanilla[:]


def create_itempool(world: "SoulBlazerWorld") -> list[SoulBlazerItem]:
    itempool = [world.create_item(name) for name in unique_item_names]
    itempool += [world.create_item(ItemID.MEDICALHERB.display_name) for _ in range(herb_count_vanilla)]
    itempool += [world.create_item(ItemID.STRANGEBOTTLE.display_name) for _ in range(bottle_count_vanilla)]
    # TODO: Add option to replace nothings with... something?
    itempool += [world.create_item(ItemID.NOTHING.display_name) for _ in range(nothing_count_vanilla)]
    world.gem_items = [
        world.create_item(ItemID.GEMS.display_name).set_operand(value) for value in create_gem_pool(world)
    ]
    itempool += world.gem_items
    world.exp_items = [
        world.create_item(ItemID.EXP.display_name).set_operand(value) for value in create_exp_pool(world)
    ]
    itempool += world.exp_items

    return itempool


# TODO: Unsure which progression items should skip balancing
sword_names = [data.name for data in items_data.swords]

armor_names = [data.name for data in items_data.armors]

magic_names = [data.name for data in items_data.magics]

castable_magic_names = [data.name for data in items_data.magics if data.id != ItemID.PHOENIX]

emblem_names = [
    ItemID.EMBLEMA.display_name,
    ItemID.EMBLEMB.display_name,
    ItemID.EMBLEMC.display_name,
    ItemID.EMBLEMD.display_name,
    ItemID.EMBLEME.display_name,
    ItemID.EMBLEMF.display_name,
    ItemID.EMBLEMG.display_name,
    ItemID.EMBLEMH.display_name,
]

redhot_names = [
    ItemID.REDHOTMIRROR.display_name,
    ItemID.REDHOTBALL.display_name,
    ItemID.REDHOTSTICK.display_name,
]

stone_names = [
    ItemID.BROWNSTONE.display_name,
    ItemID.GREENSTONE.display_name,
    ItemID.BLUESTONE.display_name,
    ItemID.SILVERSTONE.display_name,
    ItemID.PURPLESTONE.display_name,
    ItemID.BLACKSTONE.display_name,
]

soul_names = [data.name for data in items_data.souls]

repeatable_item_names = [
    ItemID.NOTHING.display_name,
    ItemID.MEDICALHERB.display_name,
    ItemID.STRANGEBOTTLE.display_name,
    ItemID.GEMS.display_name,
    ItemID.EXP.display_name,
]

unique_item_names = [
    data.name
    for data in items_data.all_items
    if data.name not in repeatable_item_names and data.name != ItemID.VICTORY.display_name
]

all_items_by_name = {data.name: data for data in items_data.all_items}


# IDs only uniquely identify regular items, EXP and Gems. NPC Releases, and souls are identified with themselves by operand.
item_names_by_id = {
    data.id: data.name
    for data in [
        *items_data.swords,
        *items_data.armors,
        *items_data.magics,
        *items_data.inventory_items,
        *items_data.misc_items,
    ]
}

npc_by_operand = {data.operand: data.name for data in items_data.npc_releases}

soul_by_operand = {data.operand: data.name for data in items_data.souls}

# Any item can be uniquely identified by code or possibly a composite key of ID and Operand.
items_by_code = {data.code: data for data in items_data.all_items}

item_name_groups = {
    "swords": sword_names,
    "armors": armor_names,
    "magic": magic_names,
    "stones": stone_names,
    "emblems": emblem_names,
    "redhots": redhot_names,
    "souls": soul_names,
}
