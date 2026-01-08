from logging import DEBUG, getLogger
from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from worlds.rac3.constants.data.item import (goal_data, item_counts, item_table, NAME_TO_PROG_DICT,
                                             non_prog_weapon_data, prog_weapon_data, progressive_data, RAC3ITEMDATA)
from worlds.rac3.constants.item_tags import RAC3ITEMTAG
from worlds.rac3.constants.items import RAC3ITEM
from worlds.rac3.constants.locations.general import RAC3LOCATION
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.rac3options import RaC3Options

if TYPE_CHECKING:
    from worlds.rac3 import RaC3World


class GameItem(Item):
    game = RAC3OPTION.GAME_TITLE_FULL


rac3_logger = getLogger(RAC3OPTION.GAME_TITLE_FULL)
rac3_logger.setLevel(DEBUG)


def create_itempool(world: "RaC3World") -> list[Item]:
    itempool: list[Item] = []
    options: type[RaC3Options] = world.options

    for name in item_table.keys():
        item_type: ItemClassification = item_table[name].AP_CLASSIFICATION
        item_tags: list[str] = item_table[name].TAGS
        if item_type in [ItemClassification.filler, ItemClassification.trap]:
            continue
        if RAC3ITEMTAG.WEAPON_UPGRADE in item_tags:
            continue
        if RAC3ITEMTAG.UNUSED in item_tags:
            continue
        item_amount: int = item_counts.get(name, 1)

        # Already placed items (Starting items and vanilla)
        if name in world.preplaced_items:
            if item_amount == 1:
                continue
            else:
                item_amount -= 1  # remove one from the pool as it has already been placed

        # Progressive Weapons option
        if not options.enable_progressive_weapons.value:
            if name in prog_weapon_data.keys():
                continue
        else:  # options.EnableProgressiveWeapons.value:
            if name in non_prog_weapon_data.keys():
                continue

        # ExtraArmorUpgrade option
        if RAC3ITEMTAG.ARMOR in item_tags:
            if name != RAC3ITEM.PROGRESSIVE_ARMOR:
                continue
            item_amount = options.armor_upgrade.value

        # Catch accidental duplicates
        if item_amount is None:
            rac3_logger.warning(f"{name} has an incorrect amount count")
        if item_amount > 1 and name not in progressive_data.keys():
            rac3_logger.warning(f"multiple copies of {name} added to the item pool")

        itempool += create_multiple_items(world, name, item_amount, item_type)

    victory = create_item(world, RAC3ITEM.VICTORY)
    world.multiworld.get_location(RAC3LOCATION.COMMAND_CENTER_BIOBLITERATOR, world.player).place_locked_item(victory)
    return itempool


def create_multiple_items(world: "RaC3World", name: str, count: int = 1,
                          item_type: ItemClassification = ItemClassification.progression) -> list[Item]:
    data: RAC3ITEMDATA = item_table[name]
    itemlist: list[Item] = []

    for _ in range(count):
        itemlist += [GameItem(name, item_type, data.AP_CODE, world.player)]

    return itemlist


def create_item(world: "RaC3World", name: str) -> Item:
    data = item_table.get(name, goal_data.get(name))
    if data is None:
        raise KeyError(f"{name} not found in item_table")
    return GameItem(name, data.AP_CLASSIFICATION, data.AP_CODE, world.player)


def get_filler_item_selection(world: "RaC3World"):
    frequencies = world.options.filler_weight.value
    if world.options.enable_progressive_weapons.value:
        frequencies[RAC3ITEM.WEAPON_XP] = 0
    if world.options.traps_enabled.value:
        traps = world.options.trap_weight.value
        frequencies.update(traps)
    return [name for name, count in frequencies.items() for _ in range(count)]


def starting_weapons(world: "RaC3World", dictionary: dict[str, int]) -> list[str]:
    weapon_list: list[str] = []
    for name in dictionary:
        count = dictionary[name]
        if count == 0:
            continue
        if world.options.enable_progressive_weapons.value:
            for _ in range(count):
                weapon_list.append(NAME_TO_PROG_DICT[name])
        else:
            weapon_list.append(name)
    world.random.shuffle(weapon_list)
    return [weapon_list[0], weapon_list[1]]
