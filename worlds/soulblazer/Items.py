from BaseClasses import Item
from typing import TYPE_CHECKING
from .Data.Enums import ItemID
from .Data.ItemData import SoulBlazerItemData, SoulBlazerItemsData

if TYPE_CHECKING:
    from . import SoulBlazerWorld


class SoulBlazerItem(Item):
    game = "Soul Blazer"

    def __init__(self, player: int, itemData: SoulBlazerItemData):
        super().__init__(itemData.name, itemData.classification, itemData.code, player)
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


items_data: SoulBlazerItemsData = SoulBlazerItemsData.from_yaml_file("worlds/soulblazer/Data/SoulBlazerItems.yaml")

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
    itempool = [SoulBlazerItem(world.player, itemData) for itemData in unique_items_by_name.values()]
    itempool += [
        SoulBlazerItem(world.player, repeatable_items_by_id[ItemID.MEDICALHERB])
        for _ in range(herb_count_vanilla)
    ]
    itempool += [
        SoulBlazerItem(world.player, repeatable_items_by_id[ItemID.STRANGEBOTTLE])
        for _ in range(bottle_count_vanilla)
    ]
    # TODO: Add option to replace nothings with... something?
    itempool += [
        SoulBlazerItem(world.player, repeatable_items_by_id[ItemID.NOTHING])
        for _ in range(nothing_count_vanilla)
    ]
    world.gem_items = [world.create_item(item_names_by_id[ItemID.GEMS]).set_operand(value) for value in create_gem_pool(world)]
    itempool += world.gem_items
    world.exp_items = [world.create_item(item_names_by_id[ItemID.EXP]).set_operand(value) for value in create_exp_pool(world)]
    itempool += world.exp_items

    return itempool


# TODO: Unsure which progression items should skip balancing
swords_by_name = {data.name: data for data in items_data.swords}

armors_by_name = {data.name: data for data in items_data.armors}

magic_by_name = {data.name: data for data in items_data.magics}

castable_magic_by_name = {data.name: data for data in items_data.magics if data.id != ItemID.PHOENIX}

emblems_by_name = {
    data.name: data
    for data in items_data.inventory_items
    if data.id
    in [
        ItemID.EMBLEMA,
        ItemID.EMBLEMB,
        ItemID.EMBLEMC,
        ItemID.EMBLEMD,
        ItemID.EMBLEME,
        ItemID.EMBLEMF,
        ItemID.EMBLEMG,
        ItemID.EMBLEMH,
    ]
}

redhots_by_name = {
    data.name: data
    for data in items_data.inventory_items
    if data.id
    in [
        ItemID.REDHOTMIRROR,
        ItemID.REDHOTBALL,
        ItemID.REDHOTSTICK,
    ]
}

stones_by_name = {
    data.name: data
    for data in items_data.inventory_items
    if data.id
    in [
        ItemID.BROWNSTONE,
        ItemID.GREENSTONE,
        ItemID.BLUESTONE,
        ItemID.SILVERSTONE,
        ItemID.PURPLESTONE,
        ItemID.BLACKSTONE,
    ]
}

inventory_items_by_name = {data.name: data for data in items_data.inventory_items}

misc_items_by_name = {data.name: data for data in items_data.misc_items}

repeatable_items_by_name = {
    **{data.name: data for data in items_data.misc_items if data.id in [ItemID.MEDICALHERB, ItemID.STRANGEBOTTLE]},
    **misc_items_by_name,
}

items_by_name = {
    **swords_by_name,
    **armors_by_name,
    **magic_by_name,
    **inventory_items_by_name,
}

npc_release_by_name = {data.name: data for data in items_data.npc_releases}

souls_by_name = {data.name: data for data in items_data.souls}

special_items_by_name = {data.name: data for data in items_data.special_items}

all_items_by_name = {
    **items_by_name,
    **misc_items_by_name,
    **npc_release_by_name,
    **souls_by_name,
    **special_items_by_name,
}

unique_items_by_name = {
    k: v for k, v in all_items_by_name.items() if k not in repeatable_items_by_name and v.id != ItemID.VICTORY
}

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

repeatable_items_by_id = {
    **{data.id: data for data in items_data.misc_items if data.id in [ItemID.MEDICALHERB, ItemID.STRANGEBOTTLE]},
    **misc_items_by_name,
}

npc_by_operand = {data.operand: data.name for data in items_data.npc_releases}

soul_by_operand = {data.operand: data.name for data in items_data.souls}

# Any item can be uniquely identified by code or possibly a composite key of ID and Operand.
items_by_code = {data.code: data for data in items_data.all_items}

item_name_groups = {
    "swords": swords_by_name.keys(),
    "armors": armors_by_name.keys(),
    "magic": magic_by_name.keys(),
    "stones": stones_by_name.keys(),
    "emblems": emblems_by_name.keys(),
    "redhots": redhots_by_name.keys(),
    "souls": souls_by_name.keys(),
}
