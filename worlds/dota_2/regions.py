from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import DOTA2World

from .locations import DOTA2Location, LocationDef
from BaseClasses import Item, ItemClassification

def create_regions_and_locations(world: DOTA2World, location_defs: list[LocationDef]) -> None:
    multiworld = world.multiworld
    player = world.player

    menu = Region("Menu", player, multiworld)
    main = Region("Main", player, multiworld)

    multiworld.regions += [menu, main]
    menu.connect(main)

    unlock_of = {name: item for item, names in world.check_unlocks.items() for name in names}
    for d in location_defs:
        loc_id = world.location_name_to_id[d.name]
        location = DOTA2Location(player, d.name, loc_id, main)
        if (d.name == "Goal Complete"):
            print("Found Game Complete:", d.name, d.type)
            location.address = None
            location.place_locked_item(Item("Complete",ItemClassification.progression, None, player)) 
        elif d.name in unlock_of:
            location.access_rule = lambda state, item=unlock_of[d.name]: state.has(item, player)
        elif(d.name.startswith("Win with Hero from Group ")):
            group_number = int(d.name.removeprefix("Win with Hero from Group "))
            required_unlocks = group_number
            location.access_rule = lambda state, required=required_unlocks: (
                state.count("Progressive Group Unlock", player) >= required
            )
        elif d.name.startswith("Win as a "):
            category = d.name.removeprefix("Win as a ").removesuffix(" Hero")
            location.access_rule = lambda state, category=category: (
                category_hero_available(world, state, category)
            )
        elif d.type == "MINIGAME":
            location.access_rule = (
                lambda state, requirements=d.requirements:
                    minigame_requirement_met(world, state, requirements)
            )
        elif d.requirements:
            location.access_rule = (
                lambda state, requirements=d.requirements:
                    item_requirements_met(world, state, requirements)
            )
    
        main.locations.append(location)

def category_hero_available(world: DOTA2World, state, category: str) -> bool:
    player = world.player
    if any(
        hero_matches_category(hero, category)
        for hero in world.starting_hero_pool
    ):
        return True

    unlocks = state.count("Progressive Group Unlock", player)

    for group_number, group in enumerate(world.hero_groups, start=1):
        if unlocks >= group_number:
            if any(
                hero_matches_category(hero, category)
                for hero in group
            ):
                return True

    return False

def hero_matches_category(hero, category: str) -> bool:
    category = category.lower()

    if category == "melee":
        return hero.attack_type == "Melee"

    if category == "ranged":
        return hero.attack_type == "Ranged"

    if category == "strength":
        return hero.primary_attr == "str"

    if category == "agility":
        return hero.primary_attr == "agi"

    if category == "intelligence":
        return hero.primary_attr == "int"

    if category == "universal":
        return hero.primary_attr == "all"

    if category == "carry":
        return "Carry" in hero.roles

    if category == "support":
        return "Support" in hero.roles
    
    if category == "0 legged":
        return hero.legs == 0

    
    if category == "2 legged":
        return hero.legs == 2
    
    if category == "4+ legged":
        return hero.legs >= 4

    return False

def item_requirements_met(
    world: DOTA2World,
    state,
    requirements: list[str]
) -> bool:
    for requirement in requirements:
        if not state.has("Unlock " + requirement, world.player):
            return False

    return True

def minigame_requirement_met(
    world: DOTA2World,
    state,
    requirements: list[str]
) -> bool:
    for requirement in requirements:
        if not state.has(requirement, world.player):
            return False
        
    return True

