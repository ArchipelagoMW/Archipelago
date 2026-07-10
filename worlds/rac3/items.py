"""This module provides handling for Item objects"""

from logging import DEBUG, getLogger
from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from worlds.rac3.constants.data.item import (goal_data, infobot_data, item_counts, item_table, NAME_TO_PROG_DICT,
                                             ngplus_item_counts, PROG_TO_NAME_DICT, progressive_data, RAC3ITEMDATA)
from worlds.rac3.constants.item_tags import RAC3ITEMTAG
from worlds.rac3.constants.items import RAC3ITEM
from worlds.rac3.constants.locations.general import RAC3LOCATION
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.shortcuts import RAC3SHORTCUTS
from worlds.rac3.rac3options import RaC3Options

if TYPE_CHECKING:
    from worlds.rac3.world import RaC3World


class GameItem(Item):
    """Ratchet and Clank 3 Items"""
    game = RAC3OPTION.GAME_TITLE_FULL


rac3_logger = getLogger(RAC3OPTION.GAME_TITLE_FULL)
rac3_logger.setLevel(DEBUG)


def create_itempool(world: "RaC3World") -> list[Item]:
    """Returns a list of items to be added to the item pool after checking options"""
    itempool: list[Item] = []
    options: type[RaC3Options] = world.options

    for name, entry in item_table.items():
        item_type: ItemClassification = entry.AP_CLASSIFICATION
        item_tags: list[str] = entry.TAGS
        if item_type in [ItemClassification.filler, ItemClassification.trap]:
            continue
        if RAC3ITEMTAG.WEAPON_UPGRADE in item_tags:
            continue
        if RAC3ITEMTAG.UNUSED in item_tags:
            continue
        if options.ngplus_items.value:
            if name == RAC3ITEM.PROGRESSIVE_RY3N0:
                item_amount: int = 5
            else:
                item_amount: int = ngplus_item_counts.get(name, 1)
        elif name != RAC3ITEM.PROGRESSIVE_RY3N0:
            item_amount: int = item_counts.get(name, 1)
        else:
            continue
        # Already placed items (Starting items and vanilla)
        if name in world.preplaced_items:
            count = world.preplaced_items.count(name)
            if item_amount <= count:
                continue
            item_amount -= count  # remove one from the pool as it has already been placed

        # Progressive Weapons option
        if RAC3ITEMTAG.PROG_WEAPON in item_tags and not options.progressive_weapons.value:
            continue
        if RAC3ITEMTAG.NON_PROG_WEAPON in item_tags and options.progressive_weapons.value:
            continue

        # NG+ Item option
        if RAC3ITEMTAG.NGPLUS in item_tags:
            if not options.ngplus_items.value:
                continue

        # ExtraArmorUpgrade option
        if RAC3ITEMTAG.ARMOR in item_tags:
            if name != RAC3ITEM.PROGRESSIVE_ARMOR:
                continue
            item_amount = options.armor_upgrade.value

        if RAC3ITEMTAG.CLANK in item_tags:
            if options.clank_options.value == options.clank_options.option_start_with:
                continue
            if options.clank_options.value == options.clank_options.option_shuffled_as_one and name != RAC3ITEM.CLANK:
                continue
            if (options.clank_options.value == options.clank_options.option_shuffled_independently
                and name not in [RAC3ITEM.HELI_PACK, RAC3ITEM.THRUSTER_PACK]):
                continue
            if (options.clank_options.value == options.clank_options.option_shuffled_progressive
                and name != RAC3ITEM.PROGRESSIVE_PACK):
                continue

        # Vidcomics option
        if RAC3ITEMTAG.VIDCOMIC in item_tags and not options.vidcomics.value:
            continue

        # Catch accidental duplicates
        if item_amount is None:
            rac3_logger.warning(f"{name} has an incorrect amount count")
        else:
            if item_amount > 1 and name not in progressive_data.keys():
                rac3_logger.warning(f"multiple copies of {name} added to the item pool")
            itempool += create_multiple_items(world, name, item_amount, item_type)

    victory = create_item(world, RAC3ITEM.VICTORY)
    world.multiworld.get_location(RAC3LOCATION.COMMAND_CENTER_BIOBLITERATOR, world.player).place_locked_item(victory)
    return itempool


def create_multiple_items(world: "RaC3World", name: str, count: int = 1,
                          item_type: ItemClassification = ItemClassification.progression) -> list[Item]:
    """Returns a list containing multiple copies of an item requested"""
    data: RAC3ITEMDATA = item_table[name]
    itemlist: list[Item] = []

    for _ in range(count):
        itemlist += [GameItem(name, item_type, data.AP_CODE, world.player)]

    return itemlist


def create_item(world: "RaC3World", name: str) -> Item:
    """Returns a new instance of an Item"""
    data = item_table.get(name, goal_data.get(name))
    if data is None:
        raise KeyError(f"{name} not found in item_table")
    return GameItem(name, data.AP_CLASSIFICATION, data.AP_CODE, world.player)


def get_filler_selection(world: "RaC3World") -> list[str]:
    """Returns a list of item names to be used when choosing filler"""
    frequencies = world.options.filler_weight.value
    if world.options.progressive_weapons.value:
        frequencies[RAC3ITEM.WEAPON_XP] = 0
    if world.options.traps_enabled.value:
        traps = world.options.trap_weight.value
        frequencies.update(traps)
    if not frequencies or all(count == 0 for count in frequencies.values()):
        frequencies[RAC3ITEM.BOLTS] = 1  # set bolts to be the only filler if the filler weights are empty
    return [name for name, count in frequencies.items() for _ in range(count)]


def process_start_inventory(world: "RaC3World"):
    """Process the player's starting inventory options to account settings and convert items if needed"""
    if not world.options.progressive_weapons.value:
        for item in PROG_TO_NAME_DICT.keys():
            if world.options.start_inventory_from_pool.value.get(item, None):
                new_item = PROG_TO_NAME_DICT[item]
                rac3_logger.warning(f"Player: {world.player_name}'s starting {item} from pool have been converted to "
                                    f"{new_item} to match their settings, item count set to 1.")
                world.options.start_inventory_from_pool.value.pop(item)
                world.options.start_inventory_from_pool.value[new_item] = 1
            if world.options.start_inventory.value.get(item, None):
                new_item = PROG_TO_NAME_DICT[item]
                rac3_logger.warning(f"Player: {world.player_name}'s starting {item} have been converted to "
                                    f"{new_item} to match their settings, item count set to 1.")
                world.options.start_inventory.value.pop(item)
                world.options.start_inventory.value[new_item] = 1
    else:
        for item in NAME_TO_PROG_DICT.keys():
            if world.options.start_inventory_from_pool.value.get(item, None):
                new_item = NAME_TO_PROG_DICT[item]
                rac3_logger.warning(f"Player: {world.player_name}'s starting {item} from pool have been converted to "
                                    f"{new_item} to match their settings, item totals have been preserved.")
                count = world.options.start_inventory_from_pool.value[item]
                world.options.start_inventory_from_pool.value.pop(item)
                world.options.start_inventory_from_pool.value[new_item] += count
            if world.options.start_inventory.value.get(item, None):
                new_item = NAME_TO_PROG_DICT[item]
                rac3_logger.warning(f"Player: {world.player_name}'s starting {item} have been converted to "
                                    f"{new_item} to match their settings, item totals have been preserved.")
                count = world.options.start_inventory.value[item]
                world.options.start_inventory.value.pop(item)
                world.options.start_inventory.value[new_item] += count
    match world.options.clank_options.value:
        case world.options.clank_options.option_start_with:
            pass  # already handled

        case world.options.clank_options.option_shuffled_as_one:
            for item in [RAC3ITEM.HELI_PACK, RAC3ITEM.THRUSTER_PACK, RAC3ITEM.PROGRESSIVE_PACK]:
                if world.options.start_inventory_from_pool.value.get(item, None):
                    rac3_logger.warning(f"Player: {world.player_name}'s starting {item} from pool have been converted "
                                        f"to a {RAC3ITEM.CLANK} to match their settings.")
                    world.options.start_inventory_from_pool.value.pop(item)
                    world.options.start_inventory_from_pool.value[RAC3ITEM.CLANK] += 1
                if world.options.start_inventory.value.get(item, None):
                    rac3_logger.warning(f"Player: {world.player_name}'s starting {item} have been converted "
                                        f"to a {RAC3ITEM.CLANK} to match their settings.")
                    world.options.start_inventory.value.pop(item)
                    world.options.start_inventory.value[RAC3ITEM.CLANK] += 1

        case world.options.clank_options.option_shuffled_independently:
            if world.options.start_inventory_from_pool.value.get(RAC3ITEM.CLANK, None):
                rac3_logger.warning(
                    f"Player: {world.player_name}'s starting {RAC3ITEM.CLANK} from pool has been converted to a "
                    f"{RAC3ITEM.HELI_PACK} and a {RAC3ITEM.THRUSTER_PACK} to match their settings.")
                world.options.start_inventory_from_pool.value.pop(RAC3ITEM.CLANK)
                world.options.start_inventory_from_pool.value[RAC3ITEM.HELI_PACK] += 1
                world.options.start_inventory_from_pool.value[RAC3ITEM.THRUSTER_PACK] += 1
            if world.options.start_inventory.value.get(RAC3ITEM.CLANK, None):
                rac3_logger.warning(
                    f"Player: {world.player_name}'s starting {RAC3ITEM.CLANK} has been converted to a "
                    f"{RAC3ITEM.HELI_PACK} and a {RAC3ITEM.THRUSTER_PACK} to match their settings.")
                world.options.start_inventory.value.pop(RAC3ITEM.CLANK)
                world.options.start_inventory.value[RAC3ITEM.HELI_PACK] += 1
                world.options.start_inventory.value[RAC3ITEM.THRUSTER_PACK] += 1

            if world.options.start_inventory_from_pool.value.get(RAC3ITEM.PROGRESSIVE_PACK, 0) > 1:
                rac3_logger.warning(
                    f"Player: {world.player_name}'s starting {RAC3ITEM.PROGRESSIVE_PACK}s from pool have been "
                    f"converted to {RAC3ITEM.HELI_PACK}s and {RAC3ITEM.THRUSTER_PACK}s to match their settings.")
                world.options.start_inventory_from_pool.value.pop(RAC3ITEM.PROGRESSIVE_PACK)
                world.options.start_inventory_from_pool.value[RAC3ITEM.HELI_PACK] += 1
                world.options.start_inventory_from_pool.value[RAC3ITEM.THRUSTER_PACK] += 1
            if world.options.start_inventory_from_pool.value.get(RAC3ITEM.PROGRESSIVE_PACK, 0) == 1:
                world.options.start_inventory_from_pool.value.pop(RAC3ITEM.PROGRESSIVE_PACK)
                if not world.options.start_inventory_from_pool.value.get(RAC3ITEM.HELI_PACK, None):
                    rac3_logger.warning(
                        f"Player: {world.player_name}'s starting {RAC3ITEM.PROGRESSIVE_PACK} from pool has been "
                        f"converted to a {RAC3ITEM.HELI_PACK} to match their settings.")
                    world.options.start_inventory_from_pool.value[RAC3ITEM.HELI_PACK] += 1
                elif not world.options.start_inventory_from_pool.value.get(RAC3ITEM.THRUSTER_PACK, None):
                    rac3_logger.warning(
                        f"Player: {world.player_name}'s starting {RAC3ITEM.PROGRESSIVE_PACK} from pool has been "
                        f"converted to a {RAC3ITEM.THRUSTER_PACK} to match their settings.")
                    world.options.start_inventory_from_pool.value[RAC3ITEM.THRUSTER_PACK] += 1
            if world.options.start_inventory.value.get(RAC3ITEM.PROGRESSIVE_PACK, 0) > 1:
                rac3_logger.warning(
                    f"Player: {world.player_name}'s starting {RAC3ITEM.PROGRESSIVE_PACK}s have been "
                    f"converted to {RAC3ITEM.HELI_PACK}s and {RAC3ITEM.THRUSTER_PACK}s to match their settings.")
                world.options.start_inventory.value.pop(RAC3ITEM.PROGRESSIVE_PACK)
                world.options.start_inventory.value[RAC3ITEM.HELI_PACK] += 1
                world.options.start_inventory.value[RAC3ITEM.THRUSTER_PACK] += 1
            if world.options.start_inventory.value.get(RAC3ITEM.PROGRESSIVE_PACK, 0) == 1:
                world.options.start_inventory.value.pop(RAC3ITEM.PROGRESSIVE_PACK)
                if not world.options.start_inventory.value.get(RAC3ITEM.HELI_PACK, None):
                    rac3_logger.warning(
                        f"Player: {world.player_name}'s starting {RAC3ITEM.PROGRESSIVE_PACK} has been "
                        f"converted to a {RAC3ITEM.HELI_PACK} to match their settings.")
                    world.options.start_inventory.value[RAC3ITEM.HELI_PACK] += 1
                elif not world.options.start_inventory.value.get(RAC3ITEM.THRUSTER_PACK, None):
                    rac3_logger.warning(
                        f"Player: {world.player_name}'s starting {RAC3ITEM.PROGRESSIVE_PACK} has been "
                        f"converted to a {RAC3ITEM.THRUSTER_PACK} to match their settings.")
                    world.options.start_inventory.value[RAC3ITEM.THRUSTER_PACK] += 1

        case world.options.clank_options.option_shuffled_progressive:
            for item in [RAC3ITEM.HELI_PACK, RAC3ITEM.THRUSTER_PACK]:
                if world.options.start_inventory_from_pool.value.get(item, None):
                    count = world.options.start_inventory_from_pool.value[item]
                    rac3_logger.warning(f"Player: {world.player_name}'s starting {item} from pool have been converted "
                                        f"to {RAC3ITEM.PROGRESSIVE_PACK} to match their settings.")
                    world.options.start_inventory_from_pool.value.pop(item)
                    world.options.start_inventory_from_pool.value[RAC3ITEM.PROGRESSIVE_PACK] += count
                if world.options.start_inventory.value.get(item, None):
                    count = world.options.start_inventory.value[item]
                    rac3_logger.warning(f"Player: {world.player_name}'s starting {item} have been converted "
                                        f"to {RAC3ITEM.PROGRESSIVE_PACK} to match their settings.")
                    world.options.start_inventory.value.pop(item)
                    world.options.start_inventory.value[RAC3ITEM.PROGRESSIVE_PACK] += count

            if world.options.start_inventory_from_pool.value.get(RAC3ITEM.CLANK, None):
                rac3_logger.warning(f"Player: {world.player_name}'s starting {RAC3ITEM.CLANK} from pool has been "
                                    f"converted to {RAC3ITEM.PROGRESSIVE_PACK}s to match their settings.")
                world.options.start_inventory_from_pool.value.pop(item)
                world.options.start_inventory_from_pool.value[RAC3ITEM.PROGRESSIVE_PACK] += 2
            if world.options.start_inventory.value.get(item, None):
                rac3_logger.warning(f"Player: {world.player_name}'s starting {RAC3ITEM.CLANK} has been converted "
                                    f"to {RAC3ITEM.PROGRESSIVE_PACK}s to match their settings.")
                world.options.start_inventory.value.pop(item)
                world.options.start_inventory.value[RAC3ITEM.PROGRESSIVE_PACK] += 2

    world.options.start_inventory_from_pool.value.pop(RAC3ITEM.VELDIN, None)
    world.options.start_inventory.value.pop(RAC3ITEM.VELDIN, None)


def starting_weapons(world: "RaC3World") -> list[str]:
    """Returns the weapons randomly selected for the player to start with"""
    weapon_list: list[str] = []
    for name in world.options.starting_weapons.value:
        count = world.options.starting_weapons.value[name]
        if count == 0:
            continue
        if world.options.progressive_weapons.value:
            new_name = NAME_TO_PROG_DICT[name]
            item_cap = item_counts[new_name] if world.options.ngplus_items.value else ngplus_item_counts[new_name]
            preplaced_count = world.options.start_inventory_from_pool.value.get(new_name, 0)
            if preplaced_count <= item_cap - 2:
                weapon_list.extend(new_name for _ in range(count))
            elif preplaced_count == item_cap - 1:
                weapon_list.append(new_name)
        else:
            if name not in world.options.start_inventory_from_pool.value:
                weapon_list.append(name)
    world.random.shuffle(weapon_list)
    return weapon_list[:2]


def starting_planets(world: "RaC3World") -> list[str]:
    """Returns the planets randomly selected for the player to start with"""
    planet_list: list[str] = [infobot for infobot in infobot_data.keys() if
                              infobot not in world.options.start_inventory_from_pool.value]
    planet_list = remove_dead_starting_planets(world, planet_list)
    if len(planet_list) > 1:  # [Phoenix], [Florana], or [Other]
        world.random.shuffle(planet_list)
        if world.options.shortcuts.value.get(RAC3SHORTCUTS.VELDIN_SKIP, False):
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
        RAC3ITEM.VELDIN,  # Shouldn't be considered by accident
        RAC3ITEM.MUSEUM,
        RAC3ITEM.OBANI_DRACO,
        RAC3ITEM.QWARKS_HIDEOUT,
        RAC3ITEM.COMMAND_CENTER
    ]

    # If Rangers are disabled or only the optional missions are enabled, Aridia and Blackwater City are unreachable
    if world.options.rangers.value == 0 or world.options.rangers.value == 2:
        unreachable.append(RAC3ITEM.BLACKWATER_CITY)
        if world.options.weapon_vendors.value == 0:
            unreachable.append(RAC3ITEM.ARIDIA)

    # If no weapon can be purchased from the vendor, you can't get any items
    if world.options.weapon_vendors.value == 0:
        unreachable.append(RAC3ITEM.OBANI_GEMINI)

    # If clank skip or no skillpoints, you can't get the skillpoint
    # If no weapon vendor, you can't get a vendor item
    if ((world.options.shortcuts.get(RAC3SHORTCUTS.HOLOSTAR_CLANK, False) or world.options.skill_points.value < 2)
        and world.options.weapon_vendors.value == 0):
        unreachable.append(RAC3ITEM.HOLOSTAR_STUDIOS)

    # If no Arena challenges are locations or only the second half is,
    # Annihilation Nation is unreachable from the start
    if (world.options.arena.value == 0 or world.options.arena.value == 2) and world.options.weapon_vendors.value == 0:
        unreachable.append(RAC3ITEM.ANNIHILATION_NATION)

    # If you don't start with clank, you cant do leviathan
    # If you also don't have titanium bolts, you can't get the one before first hypershot node
    # If you also don't start with hypershot, you can't get the 'explore the starport' rewards
    if world.options.clank_options.value and not world.options.titanium_bolts.value and (
        RAC3ITEM.HYPERSHOT not in world.options.start_inventory.value):
        unreachable.append(RAC3ITEM.ZELDRIN_STARPORT)

    # If titanium bolts are disabled, you cant get the one on marcadia before the ranger
    # If you also don't have rangers or only the optional rangers, you cant get any of the marcadia locations
    # including LDF
    if world.options.titanium_bolts.value == 0 and (
        world.options.rangers.value == 0 or world.options.rangers.value == 2):
        unreachable.append(RAC3ITEM.MARCADIA)

    return [planet for planet in current_planet_list if planet not in unreachable]
