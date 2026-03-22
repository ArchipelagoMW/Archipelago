from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import Item, ItemClassification
import math

if TYPE_CHECKING:
    from .world import NothingWorld


ITEM_NAME_TO_ID = {
    "Nothing Item Auto Milestone Collector": 1,
    "Nothing Item Auto Timer Restart": 2,
    "Nothing Item Timer Digit": 3,
    "Nothing Item Progressive Time Cap": 4,
    "Nothing Item Gifted Coin": 5,
    "Nothing Item Song 1": 11,
    "Nothing Item Song 2": 12,
    "Nothing Item Song 3": 13,
    "Nothing Item Song 4": 14,
    "Nothing Item Song 5": 15,
    "Nothing Item Song 6": 16,
    "Nothing Item Song 7": 17,
    "Nothing Item Song 8": 18,
    "Nothing Item Song 9": 19,
    "Nothing Item Song 10": 20,
    "Nothing Item Sound 1": 21,
    "Nothing Item Sound 2": 22,
    "Nothing Item Sound 3": 23,
    "Nothing Item Sound 4": 24,
    "Nothing Item Sound 5": 25,
    "Nothing Item Sound 6": 26,
    "Nothing Item Sound 7": 27,
    "Nothing Item Sound 8": 28,
    "Nothing Item Sound 9": 29,
    "Nothing Item Sound 10": 30,
    "Nothing Item Theme Blue": 32,
    "Nothing Item Theme Green": 33,
    "Nothing Item Theme Pink": 34,
    "Nothing Item Theme White": 35,
    "Nothing Item Theme Black": 36,
    "Nothing Item Theme Orange": 37,
    "Nothing Item Theme Yellow": 38,
    "Nothing Item Theme Purple": 39,
    "Nothing Item Theme Cyan": 40
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Nothing Item Auto Milestone Collector": ItemClassification.useful,
    "Nothing Item Auto Timer Restart": ItemClassification.useful,
    "Nothing Item Timer Digit": ItemClassification.progression,
    "Nothing Item Progressive Time Cap": ItemClassification.progression,
    "Nothing Item Gifted Coin": ItemClassification.useful | ItemClassification.filler,
    "Nothing Item Song 1": ItemClassification.filler,
    "Nothing Item Song 2": ItemClassification.filler,
    "Nothing Item Song 3": ItemClassification.filler,
    "Nothing Item Song 4": ItemClassification.filler,
    "Nothing Item Song 5": ItemClassification.filler,
    "Nothing Item Song 6": ItemClassification.filler,
    "Nothing Item Song 7": ItemClassification.filler,
    "Nothing Item Song 8": ItemClassification.filler,
    "Nothing Item Song 9": ItemClassification.filler,
    "Nothing Item Song 10": ItemClassification.filler,
    "Nothing Item Sound 1": ItemClassification.filler,
    "Nothing Item Sound 2": ItemClassification.filler,
    "Nothing Item Sound 3": ItemClassification.filler,
    "Nothing Item Sound 4": ItemClassification.filler,
    "Nothing Item Sound 5": ItemClassification.filler,
    "Nothing Item Sound 6": ItemClassification.filler,
    "Nothing Item Sound 7": ItemClassification.filler,
    "Nothing Item Sound 8": ItemClassification.filler,
    "Nothing Item Sound 9": ItemClassification.filler,
    "Nothing Item Sound 10": ItemClassification.filler,
    "Nothing Item Theme Blue": ItemClassification.filler,
    "Nothing Item Theme Green": ItemClassification.filler,
    "Nothing Item Theme Pink": ItemClassification.filler,
    "Nothing Item Theme White": ItemClassification.filler,
    "Nothing Item Theme Black": ItemClassification.filler,
    "Nothing Item Theme Orange": ItemClassification.filler,
    "Nothing Item Theme Yellow": ItemClassification.filler,
    "Nothing Item Theme Purple": ItemClassification.filler,
    "Nothing Item Theme Cyan": ItemClassification.filler
}


class Nothing_Archipelago_Item(Item):
    game = "nothing_archipelago"

def get_random_filler_item_name(world: NothingWorld) -> str:
    return "Nothing Item Gifted Coin"

def create_item_with_correct_classification(world: NothingWorld, name: str) -> Nothing_Archipelago_Item:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    return Nothing_Archipelago_Item(name, classification, ITEM_NAME_TO_ID[name], world.player)

def create_all_items(world: NothingWorld) -> None:
    itempool: list[Item] = []
    for _ in range(int(math.ceil(world.options.goal/world.options.milestone_interval))):
        itempool.append(world.create_item("Nothing Item Progressive Time Cap"))
    
    if world.options.shop_upgrades:
        itempool.append(world.create_item("Nothing Item Timer Digit"))
        itempool.append(world.create_item("Nothing Item Timer Digit"))
        itempool.append(world.create_item("Nothing Item Timer Digit"))
        itempool.append(world.create_item("Nothing Item Timer Digit"))
        itempool.append(world.create_item("Nothing Item Timer Digit"))
        itempool.append(world.create_item("Nothing Item Timer Digit"))

    if (world.options.gift_coins or world.options.goal > 1200):
        if world.options.shop_upgrades:
            itempool.append(world.create_item("Nothing Item Auto Milestone Collector"))
            itempool.append(world.create_item("Nothing Item Auto Timer Restart"))
        if world.options.shop_colors:
            itempool.append(world.create_item("Nothing Item Theme Blue"))
            itempool.append(world.create_item("Nothing Item Theme Green"))
            itempool.append(world.create_item("Nothing Item Theme Pink"))
            itempool.append(world.create_item("Nothing Item Theme White"))
            itempool.append(world.create_item("Nothing Item Theme Black"))
            itempool.append(world.create_item("Nothing Item Theme Orange"))
            itempool.append(world.create_item("Nothing Item Theme Yellow"))
            itempool.append(world.create_item("Nothing Item Theme Purple"))
            itempool.append(world.create_item("Nothing Item Theme Cyan"))
        if world.options.shop_music:
            itempool.append(world.create_item("Nothing Item Song 1"))
            itempool.append(world.create_item("Nothing Item Song 2"))
            itempool.append(world.create_item("Nothing Item Song 3"))
            itempool.append(world.create_item("Nothing Item Song 4"))
            itempool.append(world.create_item("Nothing Item Song 5"))
            itempool.append(world.create_item("Nothing Item Song 6"))
            itempool.append(world.create_item("Nothing Item Song 7"))
            itempool.append(world.create_item("Nothing Item Song 8"))
            itempool.append(world.create_item("Nothing Item Song 9"))
            itempool.append(world.create_item("Nothing Item Song 10"))
        if world.options.shop_sounds:
            itempool.append(world.create_item("Nothing Item Sound 1"))
            itempool.append(world.create_item("Nothing Item Sound 2"))
            itempool.append(world.create_item("Nothing Item Sound 3"))
            itempool.append(world.create_item("Nothing Item Sound 4"))
            itempool.append(world.create_item("Nothing Item Sound 5"))
            itempool.append(world.create_item("Nothing Item Sound 6"))
            itempool.append(world.create_item("Nothing Item Sound 7"))
            itempool.append(world.create_item("Nothing Item Sound 8"))
            itempool.append(world.create_item("Nothing Item Sound 9"))
            itempool.append(world.create_item("Nothing Item Sound 10"))

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool

    if world.options.gift_coins and world.options.Starting_coin_count > 0:
        for i in range(world.options.Starting_coin_count):
            world.push_precollected(world.create_item("Nothing Item Gifted Coin"))
    