from logging import DEBUG, getLogger
from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from worlds.rac3.constants.data.item import (goal_data, infobot_data, item_counts, item_table, NAME_TO_PROG_DICT,
                                             PROG_TO_NAME_DICT, progressive_data, RAC3ITEMDATA)
from worlds.rac3.constants.item_tags import RAC3ITEMTAG
from worlds.rac3.constants.items import RAC3ITEM
from worlds.rac3.constants.locations.general import RAC3LOCATION
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.rac3options import RaC3Options

if TYPE_CHECKING:
    from worlds.rac3.world import RaC3World


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
            count = world.preplaced_items.count(name)
            if item_amount <= count:
                continue
            else:
                item_amount -= count  # remove one from the pool as it has already been placed

        # Progressive Weapons option
        if RAC3ITEMTAG.PROG_WEAPON in item_tags and not options.enable_progressive_weapons.value:
            continue
        if RAC3ITEMTAG.NON_PROG_WEAPON in item_tags and options.enable_progressive_weapons.value:
            continue

        # ExtraArmorUpgrade option
        if RAC3ITEMTAG.ARMOR in item_tags:
            if name != RAC3ITEM.PROGRESSIVE_ARMOR:
                continue
            item_amount = options.armor_upgrade.value

        if RAC3ITEMTAG.CLANK in item_tags:
            if options.clank_options.value == options.clank_options.option_start_with:
                continue
            elif options.clank_options.value == options.clank_options.option_shuffled_as_one and name != RAC3ITEM.CLANK:
                continue
            elif (options.clank_options.value == options.clank_options.option_shuffled_independently
                  and name not in [RAC3ITEM.HELI_PACK, RAC3ITEM.THRUSTER_PACK]):
                continue
            elif (options.clank_options.value == options.clank_options.option_shuffled_progressive
                  and name != RAC3ITEM.PROGRESSIVE_PACK):
                continue

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


def get_filler_selection(world: "RaC3World"):
    frequencies = world.options.filler_weight.value
    if world.options.enable_progressive_weapons.value:
        frequencies[RAC3ITEM.WEAPON_XP] = 0
    if world.options.traps_enabled.value:
        traps = world.options.trap_weight.value
        frequencies.update(traps)
        # if world.options.clank_options.value > world.options.clank_options.option_start_with:
        #     frequencies[RAC3ITEM.NO_CLANK_TRAP] = 0
    if not frequencies or all(count == 0 for count in frequencies.values()):
        frequencies[RAC3ITEM.BOLTS] = 1  # set bolts to be the only filler if the filler weights are empty
        # error = "No filler items available. Please enable some filler items."
        # if world.options.enable_progressive_weapons.value:
        #     error += " Progressive Weapons option is enabled, so 'Weapon XP' cannot be used as a filler item."
        # if not world.options.traps_enabled.value:
        #     error += " Traps are disabled, so no trap items can be used as filler."
        # raise OptionError(error)
    return [name for name, count in frequencies.items() for _ in range(count)]


def process_start_inventory(world: "RaC3World") -> list[str]:
    itemlist: list[str] = []
    if not world.options.enable_progressive_weapons.value:
        for item in PROG_TO_NAME_DICT.keys():
            if world.options.start_inventory_from_pool.value.get(item, None):
                world.options.start_inventory_from_pool.value.pop(item)
                world.options.start_inventory_from_pool.value[PROG_TO_NAME_DICT[item]] = 1
    else:
        for item in NAME_TO_PROG_DICT.keys():
            if world.options.start_inventory_from_pool.value.get(item, None):
                count = world.options.start_inventory_from_pool.value[item]
                world.options.start_inventory_from_pool.value.pop(item)
                world.options.start_inventory_from_pool.value[NAME_TO_PROG_DICT[item]] += count
    world.options.start_inventory_from_pool.value.pop(RAC3ITEM.VELDIN, None)
    for item, count in world.options.start_inventory_from_pool.items():
        itemlist.extend([item for _ in range(count)])
    return itemlist


def starting_weapons(world: "RaC3World") -> list[str]:
    weapon_list: list[str] = []
    for name in world.options.starting_weapons.value:
        count = world.options.starting_weapons.value[name]
        if count == 0:
            continue
        if world.options.enable_progressive_weapons.value:
            new_name = NAME_TO_PROG_DICT[name]
            preplaced_count = world.preplaced_items.count(new_name)
            if preplaced_count <= item_counts[new_name] - 2:
                for _ in range(count):
                    weapon_list.append(new_name)
            elif preplaced_count == item_counts[new_name] - 1:
                weapon_list.append(new_name)
        else:
            if name not in world.preplaced_items:
                weapon_list.append(name)
    world.random.shuffle(weapon_list)
    return weapon_list[:2]


def starting_planets(world: "RaC3World") -> list[str]:
    planet_list: list[str] = [infobot for infobot in infobot_data.keys() if infobot not in world.preplaced_items]
    planet_list = remove_dead_starting_planets(world, planet_list)
    if len(planet_list) > 1:  # [Phoenix], [Florana], or [Other]
        world.random.shuffle(planet_list)
        if world.options.intro_skip.value:
            if RAC3ITEM.STARSHIP_PHOENIX in planet_list:
                if planet_list[0] == RAC3ITEM.STARSHIP_PHOENIX:
                    planet_list = planet_list[:2]  # [Phoenix, Other]
                else:
                    planet_list = [RAC3ITEM.STARSHIP_PHOENIX, planet_list[0]]  # [Phoenix, Other]
            else:
                planet_list = planet_list[:1]  # [Other]
        else:
            if RAC3ITEM.FLORANA in planet_list and RAC3ITEM.STARSHIP_PHOENIX in planet_list:
                planet_list = [RAC3ITEM.FLORANA, RAC3ITEM.STARSHIP_PHOENIX]  # [Florana, Phoenix]
            elif RAC3ITEM.FLORANA in planet_list:
                if planet_list[0] != RAC3ITEM.FLORANA:
                    planet_list = [RAC3ITEM.FLORANA, planet_list[0]]  # [Florana, Other]
                else:
                    planet_list = planet_list[:2]  # [Florana, Other]
            elif RAC3ITEM.STARSHIP_PHOENIX in planet_list:
                if planet_list[0] != RAC3ITEM.STARSHIP_PHOENIX:
                    planet_list = [planet_list[0], RAC3ITEM.STARSHIP_PHOENIX]  # [Other, Phoenix]
                else:
                    planet_list = [planet_list[1], RAC3ITEM.STARSHIP_PHOENIX]  # [Other, Phoenix]
            else:
                planet_list = planet_list[:2]  # [Other, Other]
    return planet_list

# TODO: Rework this function during logic overhaul
def remove_dead_starting_planets(world: "RaC3World", current_planet_list: list[str]) -> list[str]:
    """Removes any starting planets that are unreachable from Veldin"""
    # Remove unreachable planets in a single loop
    unreachable = [
        RAC3ITEM.MUSEUM,
        RAC3ITEM.OBANI_DRACO,
        RAC3ITEM.OBANI_GEMINI,
        RAC3ITEM.QWARKS_HIDEOUT,
        RAC3ITEM.COMMAND_CENTER,
        RAC3ITEM.HOLOSTAR_STUDIOS
    ]
    current_planet_list = [planet for planet in current_planet_list if planet not in unreachable]

    # If Rangers are disabled, Aridia and Blackwater City are unreachable
    if world.options.rangers.value == 0:
        to_remove = {RAC3ITEM.BLACKWATER_CITY}
        if world.options.weapon_vendors.value == 0:
            to_remove.add(RAC3ITEM.ARIDIA)
            
        current_planet_list = [planet for planet in current_planet_list if planet not in to_remove]

    # If no Arena challenges are locations or only the second half is,
    # Annihilation Nation is unreachable from the start
    if (world.options.arena.value == 0 or world.options.arena.value == 2) and world.options.weapon_vendors.value == 0:
        to_remove = {RAC3ITEM.ANNIHILATION_NATION}
        current_planet_list = [planet for planet in current_planet_list if planet not in to_remove]

    return current_planet_list
