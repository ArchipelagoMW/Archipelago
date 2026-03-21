from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import ItemClassification, Location
from . import items
import math

if TYPE_CHECKING:
    from .world import NothingWorld

def create_location_array():
    LOCATION_NAMES_TO_ID = {
        "Nothing Auto Milestone Collector": 86401,
        "Nothing Auto Timer Restart": 86402,
        "Nothing Timer Digit 1": 86403,
        "Nothing Timer Digit 2": 86404,
        "Nothing Timer Digit 3": 86405,
        "Nothing Timer Digit 4": 86406,
        "Nothing Timer Digit 5": 86407,
        "Nothing Timer Digit 6": 86408,
        "Nothing Song 1": 86410,
        "Nothing Song 2": 86411,
        "Nothing Song 3": 86412,
        "Nothing Song 4": 86413,
        "Nothing Song 5": 86414,
        "Nothing Song 6": 86415,
        "Nothing Song 7": 86416,
        "Nothing Song 8": 86417,
        "Nothing Song 9": 86418,
        "Nothing Song 10": 86419,
        "Nothing Sound 1": 86420,
        "Nothing Sound 2": 86421,
        "Nothing Sound 3": 86422,
        "Nothing Sound 4": 86423,
        "Nothing Sound 5": 86424,
        "Nothing Sound 6": 86425,
        "Nothing Sound 7": 86426,
        "Nothing Sound 8": 86427,
        "Nothing Sound 9": 86428,
        "Nothing Sound 10": 86429,
        "Nothing Theme Blue": 86432,
        "Nothing Theme Green": 86433,
        "Nothing Theme Pink": 86434,
        "Nothing Theme White": 86435,
        "Nothing Theme Black": 86436,
        "Nothing Theme Orange": 86437,
        "Nothing Theme Yellow": 86438,
        "Nothing Theme Purple": 86439,
        "Nothing Theme Cyan": 86440
    }
    for i in range(1, int(math.ceil(NothingWorld.options.goal/NothingWorld.options.milestone_interval))):
        LOCATION_NAMES_TO_ID["Nothing Milestone " + str(i+1)] = i+1

    return LOCATION_NAMES_TO_ID
    

LOCATION_NAME_TO_ID = create_location_array()


class Nothing_Archipelago_Location(Location):
    game = "Nothing_Archipelago"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def create_all_locations(world: NothingWorld) -> None:
    create_regular_locations(world)
    #create_events(world)

def create_regular_locations(world: NothingWorld) -> None:
    start = world.get_region("start")
    start_locations_intermediate = [] 
    for i in range(1, int(math.ceil(world.options.goal/world.options.milestone_interval))):
        start_locations_intermediate.append["Nothing Milestone " + str(i+1)]

    
    start_locations = get_location_names_with_ids(start_locations_intermediate)
    start.add_locations(start_locations,Nothing_Archipelago_Location)

    shopdigits_locations = get_location_names_with_ids(
        [
            "Nothing Timer Digit 1",
            "Nothing Timer Digit 2",
            "Nothing Timer Digit 3",
            "Nothing Timer Digit 4",
            "Nothing Timer Digit 5",
            "Nothing Timer Digit 6"
        ]
    )

    shopupgrades_locations = get_location_names_with_ids(
        [
            "Nothing Auto Milestone Collector",
            "Nothing Auto Timer Restart"
        ]
    )

    shopmusic_locations = get_location_names_with_ids(
        [
            "Nothing Song 1",
            "Nothing Song 2",
            "Nothing Song 3",
            "Nothing Song 4",
            "Nothing Song 5",
            "Nothing Song 6",
            "Nothing Song 7",
            "Nothing Song 8",
            "Nothing Song 9",
            "Nothing Song 10"
        ]
    )

    shopsound_locations = get_location_names_with_ids(
        [
            "Nothing Sound 1",
            "Nothing Sound 2",
            "Nothing Sound 3",
            "Nothing Sound 4",
            "Nothing Sound 5",
            "Nothing Sound 6",
            "Nothing Sound 7",
            "Nothing Sound 8",
            "Nothing Sound 9",
            "Nothing Sound 10"
        ]
    )

    shopcolor_locations = get_location_names_with_ids(
        [
            "Nothing Theme Blue",
            "Nothing Theme Green",
            "Nothing Theme Pink",
            "Nothing Theme White",
            "Nothing Theme Black",
            "Nothing Theme Orange",
            "Nothing Theme Yellow",
            "Nothing Theme Purple",
            "Nothing Theme Cyan",
        ]
    )

    if world.options.shop_upgrades:
        shopdigits = world.get_region("shopdigits")
        shopdigits.add_locations(shopdigits_locations, Nothing_Archipelago_Location)

    if (world.options.giftcoins or world.options.goal > 1200):
        if world.options.shop_upgrades:
            shopups = world.get_region("shopups")
            shopups.add_locations(shopupgrades_locations,Nothing_Archipelago_Location)
        if world.option.shop_colors:
            shopcolors = world.get_region("shopcolors")
            shopcolors.add_locations(shopcolor_locations,Nothing_Archipelago_Location)
        if world.options.shop_music:
            shopmusic = world.get_region("shopmusic")
            shopmusic.add_locations(shopmusic_locations,Nothing_Archipelago_Location)
        if world.options.shop_sounds:
            shopsounds = world.get_region("shopsounds")
            shopsounds.add_locations(shopsound_locations,Nothing_Archipelago_Location)
