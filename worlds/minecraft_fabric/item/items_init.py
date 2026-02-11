from __future__ import annotations

import math
from typing import TYPE_CHECKING, Optional, List

from BaseClasses import Location
from Options import OptionError
from worlds.minecraft_fabric.item.items_helper import add_item_to_pool, add_items_to_pool, get_progression_bl_items, \
    create_item, get_junk_items, get_item, add_optional_item, get_blank_filler
from worlds.minecraft_fabric.item.item_manager import ProcessedMinecraftItem

if TYPE_CHECKING:
   from worlds.minecraft_fabric import FabricMinecraftWorld


# Creates all Items in the Item Pools in the Randomizer
def create_items(world: FabricMinecraftWorld):
    total_items = len(world.multiworld.get_unfilled_locations(world.player))
    world.local_fill_amount = math.floor(len(world.itemsanity_locations) * world.options.itemsanity_local_fill * 0.01)
    total_items -= world.local_fill_amount

    # Progression Items ############################################################################################

    # Optional Progression Items
    total_items = add_optional_item(world, "Swim", "Swim", total_items)
    total_items = add_optional_item(world, "Sprint", "Sprint", total_items)
    total_items = add_optional_item(world, "Jump", "Jump", total_items)
    total_items = add_optional_item(world, "Chests", "Chests & Barrels", total_items)

    # Progressive Progression Items
    total_items = add_items_to_pool(world, "Progressive Tools", 4, total_items)
    total_items = add_items_to_pool(world, "Progressive Weapons", 4, total_items)
    total_items = add_items_to_pool(world, "Progressive Smelting", 2, total_items)
    total_items = add_items_to_pool(world, "Progressive Armor", 5, total_items)
    total_items = add_items_to_pool(world, "Progressive Archery", 2, total_items)
    total_items = add_items_to_pool(world, "Progressive Dye Recipes", 2, total_items)

    # Single Check Progression Items
    progression_bl: list[ProcessedMinecraftItem] = get_progression_bl_items()
    for item in progression_bl:
        total_items = add_item_to_pool(world, item.name, total_items)


    # Ruby Hunt Items
    if world.options.goal_condition.value == 4:
        world.max_ruby_count = min(world.options.total_rubies.value, total_items)
        total_items = add_items_to_pool(world, "Ruby", world.max_ruby_count, total_items)

    for item in get_filler(world, total_items):
        world.multiworld.itempool.append(item)


# Fills Locations for Local Fill
def create_local_fill_items(world: FabricMinecraftWorld):
    location_map: List[Location] = [world.multiworld.get_location(loc, world.player) for loc in world.itemsanity_locations]
    world.random.shuffle(location_map)
    filler_size = world.local_fill_amount
    filler_items = get_filler(world, filler_size)

    while filler_size > 0:
        if len(location_map) == 0:
            raise OptionError(
                "Another AP world is attempting to mess with Minecraft Fabric's prefill locations, please go politely inform them of this blunder posthaste!")

        location = location_map.pop()
        if not location.locked:
            location.place_locked_item(filler_items[filler_size - 1])
            filler_size -= 1

# Gets Filler Items for locations, with a Percentage of Traps
def get_filler(world: FabricMinecraftWorld, total_items: int):
    junk_items = []

    # Trap Items ###################################################################################################
    trap_weights = []
    trap_weights += add_trap_weight("Reverse Controls Trap", world.options.reverse_controls_trap_weight)
    trap_weights += add_trap_weight("Inverted Mouse Trap", world.options.inverted_mouse_trap_weight)
    trap_weights += add_trap_weight("Ice Trap", world.options.ice_trap_weight)
    trap_weights += add_trap_weight("Random Status Trap", world.options.random_effect_trap_weight)
    trap_weights += add_trap_weight("Stun Trap", world.options.stun_trap_weight)
    trap_weights += add_trap_weight("TNT Trap", world.options.tnt_trap_weight)
    trap_weights += add_trap_weight("Teleport Trap", world.options.teleport_trap_weight)
    trap_weights += add_trap_weight("Bee Trap", world.options.bee_trap_weight)
    trap_weights += add_trap_weight("Literature Trap", world.options.literature_trap_weight)
    trap_count = 0 if (len(trap_weights) == 0) else math.ceil(
        total_items * (world.options.trap_fill_percentage.value / 100.0))

    for i in range(trap_count):
        trap_item = world.random.choice(trap_weights)
        junk_items.append(create_item(world, trap_item.name))
        total_items -= 1

    # Blank Filler Items ###############################################################################################
    blank_filler: list[ProcessedMinecraftItem] = get_blank_filler()
    blank_filler_count = math.ceil(total_items * (world.options.empty_fill_percentage.value / 100.0))
    total_items -= blank_filler_count

    while blank_filler_count > 0:
        junk_items.append(create_item(world, blank_filler[world.random.randint(0, len(blank_filler) - 1)].name))
        blank_filler_count -= 1


    # Filler Items #####################################################################################################
    junk: list[ProcessedMinecraftItem] = get_junk_items()
    while total_items > 0:
        junk_items.append(create_item(world, junk[world.random.randint(0, len(junk) - 1)].name))
        total_items -= 1
    return junk_items

def add_trap_weight(name, weight):
    return [get_item(name)] * weight