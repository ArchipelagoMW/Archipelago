from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from .itemData import fillers, royal_arts, skills, prog_skills, prog_skill_uprades, prog_magic_levels, misc
if TYPE_CHECKING:
    from .world import CatQuestWorld

ALL_ITEMS: list[Item] = fillers + royal_arts + skills + prog_skills + prog_skill_uprades + prog_magic_levels + misc

def create_item_name_to_id() -> dict[str, int]:
    item_id_dict = {}
    current_id = 1

    for item in ALL_ITEMS:
        item_id_dict[item["name"]] = current_id
        current_id += 1

    return item_id_dict

ITEM_NAME_TO_ID = create_item_name_to_id()

ITEM_ID_TO_NAME = {v: k for k, v in ITEM_NAME_TO_ID.items()}


def create_item_classification() -> dict[str, ItemClassification]:
    item_classification_dict = {}

    for item in ALL_ITEMS:
        item_classification_dict[item["name"]] = item["classification"]
   
    return item_classification_dict

DEFAULT_ITEM_CLASSIFICATIONS = create_item_classification()


class CatQuestItem(Item):
    game = "Cat Quest"


def get_random_filler_item_name(world: CatQuestWorld) -> str:
    return ITEM_ID_TO_NAME.get(world.random.randint(1, len(fillers)))

def create_item_with_correct_classification(world: CatQuestWorld, name: str) -> CatQuestItem:
    return CatQuestItem(name, DEFAULT_ITEM_CLASSIFICATIONS[name], ITEM_NAME_TO_ID[name], world.player)

def create_all_items(world: CatQuestWorld) -> None:
    itempool = []

    required_items: list[Item] = royal_arts + misc + skills

    for item in required_items:
        itempool.append(world.create_item(item["name"]))
    
    # if world.options.skill_upgrade == "progressive_skills":
    #    for skill in prog_skills:
    #        for i in range(10):
    #            itempool.append(world.create_item(skill["name"]))
    #else:
    #    for skill in skills:
    #        itempool.append(world.create_item(skill["name"]))

    #    if world.options.skill_upgrade == "upgrades":
    #        for upgrade in prog_skill_uprades:
    #            for i in range(9):
    #                itempool.append(world.create_item(upgrade["name"]))
    #    if world.options.skill_upgrade == "magic_levels":
    #        for level in prog_magic_levels:
    #            for i in range(9):
    #                itempool.append(world.create_item(level["name"]))

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool
    