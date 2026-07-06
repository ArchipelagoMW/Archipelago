from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, List

from BaseClasses import Item, ItemClassification
from . import PotionCraftBase, POTION_CRAFT
from .data import ItemTypeEnum, ItemData, ItemFiller
from .data.items import junk_fillers
from .data.locations import ChapterCompletes
from .options import Goal


class PotionCraftItem(Item):
    game: str = POTION_CRAFT



def get_junk_items(world, amount: int) -> list[ItemFiller]:
    junk: list[ItemFiller] = world.random.choices(
        junk_fillers,
        weights=[item.weight for item in junk_fillers],
        k=amount
    )
    return junk

def create_item(world: PotionCraftBase, item: ItemData):
    for i in range(item.amount):
        world.itempool.append(world.create_item(item.type.value))


def create_single_item(world: PotionCraftBase, item_type: ItemTypeEnum):
    world.itempool.append(world.create_item(item_type.value))

def create_items(world: PotionCraftBase):

    #TODO: ACTUALLY ADD THE ITEMS TO THE MULTIWORLD
    total_location_count = len(world.multiworld.get_unfilled_locations(world.player)) #adds items to world.item pool

    print(len(world.itempool))

    remaining_locations: int = total_location_count - len(world.itempool)
    junk_count: int = remaining_locations - 1  # Minus 1 because we placed victory at the goal check in Rules.py
    for filler in get_junk_items(world.random, junk_count):
        create_single_item(world, filler.type)
    world.multiworld.itempool += world.itempool

def create_events(world: PotionCraftBase):
    goal_loc = ""
    match world.options.goal.value:
        case Goal.option_Chapter_1:
            goal_loc = ChapterCompletes.COMPLETE_CHAPTER_1.value
        case Goal.option_Chapter_2:
            goal_loc = ChapterCompletes.COMPLETE_CHAPTER_2.value
        case Goal.option_Chapter_3:
            goal_loc = ChapterCompletes.COMPLETE_CHAPTER_3.value
        case Goal.option_Chapter_4:
            goal_loc = ChapterCompletes.COMPLETE_CHAPTER_4.value
        case Goal.option_Chapter_5:
            goal_loc = ChapterCompletes.COMPLETE_CHAPTER_5.value
        case Goal.option_Chapter_6:
            goal_loc = ChapterCompletes.COMPLETE_CHAPTER_6.value
        case Goal.option_Chapter_7:
            goal_loc = ChapterCompletes.COMPLETE_CHAPTER_7.value
        case Goal.option_Chapter_8:
            goal_loc = ChapterCompletes.COMPLETE_CHAPTER_8.value
        case Goal.option_Chapter_9:
            goal_loc = ChapterCompletes.COMPLETE_CHAPTER_9.value
        case Goal.option_Chapter_10:
            goal_loc = ChapterCompletes.COMPLETE_CHAPTER_10.value

    world.multiworld.get_location(goal_loc, world.player).place_locked_item(
        PotionCraftItem("Victory", ItemClassification.progression, None, world.player))  # victory gives event


