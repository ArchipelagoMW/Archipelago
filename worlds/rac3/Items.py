from logging import DEBUG, getLogger
from typing import List, TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from constants.data.Rac3ItemData import (goal_data, item_counts, item_table, NAME_TO_PROG_DICT, non_prog_weapon_data,
                                         prog_weapon_data, progressive_data)
from constants.Rac3Items import RAC3ITEM
from constants.Rac3Options import RAC3OPTION

if TYPE_CHECKING:
    from worlds.rac3 import RaC3World


class GameItem(Item):
    game = RAC3OPTION.GAME_TITLE_FULL


rac3_logger = getLogger(RAC3OPTION.GAME_TITLE_FULL)
rac3_logger.setLevel(DEBUG)


def create_itempool(world: "RaC3World") -> List[Item]:
    itempool: List[Item] = []
    options = world.options

    for name in item_table.keys():
        item_type: ItemClassification = item_table[name].AP_CLASSIFICATION
        if item_type == ItemClassification.filler:
            continue
        item_amount: int = item_counts.get(name)

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
        if name == RAC3ITEM.PROGRESSIVE_ARMOR:
            item_amount += options.extra_armor_upgrade.value

        # Catch accidental duplicates
        if item_amount > 1 and name not in progressive_data.keys():
            rac3_logger.warning(f"multiple copies of {name} added to the item pool")

        itempool += create_multiple_items(world, name, item_amount, item_type)

    victory = create_item(world, RAC3ITEM.VICTORY)
    world.multiworld.get_location("Command Center: Biobliterator Defeated!", world.player).place_locked_item(victory)
    return itempool


def create_multiple_items(world: "RaC3World", name: str, count: int = 1,
                          item_type: ItemClassification = ItemClassification.progression) -> List[Item]:
    data = item_table[name]
    itemlist: List[Item] = []

    for i in range(count):
        itemlist += [GameItem(name, item_type, data.AP_CODE, world.player)]

    return itemlist


def create_item(world: "RaC3World", name: str) -> Item:
    data = item_table.get(name, goal_data.get(name))
    return GameItem(name, data.AP_CLASSIFICATION, data.AP_CODE, world.player)


def get_filler_item_selection(world: "RaC3World"):
    frequencies: dict[str, int] = {
        RAC3ITEM.TITANIUM_BOLT: 0,
        RAC3ITEM.WEAPON_XP: 0,
        RAC3ITEM.PLAYER_XP: 5,
        RAC3ITEM.BOLTS: 10,
        RAC3ITEM.INFERNO_MODE: 1,
        RAC3ITEM.JACKPOT: 10,
    }
    if not world.options.enable_progressive_weapons.value:
        weapon_exp: dict[str, int] = {RAC3ITEM.WEAPON_XP: 5}
        frequencies.update(weapon_exp)
    # if world.options.traps_enabled:
    #     traps = trap_items.copy()
    #     frequencies.update(traps)
    return [name for name, count in frequencies.items() for _ in range(count)]


def starting_weapons(world, dictionary: dict[str, int]) -> list[str]:
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
