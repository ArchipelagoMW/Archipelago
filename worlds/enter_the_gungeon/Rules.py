import typing
import math
from BaseClasses import CollectionState, MultiWorld
from .Options import GungeonOptions
from .Items import item_table, normal_item_table
from .Locations import GungeonLocation
from .Regions import get_total_chests
from ..generic.Rules import add_rule

def get_chest_string(number: int) -> str:
    return f"Chest {number + 1} (Any Rarity)"

def has_completed_objectives(multiworld: MultiWorld, options: GungeonLocation, player, state: CollectionState) -> bool:
    if options.additional_goals.__contains__("Old King"):
        if not state.has("Defeat The Old King", player):
            return False

    if options.additional_goals.__contains__("Resourceful Rat"):
        if not state.has("Defeat The Resourceful Rat", player):
            return False
        
    if options.additional_goals.__contains__("Agunim"):
        if not state.has("Defeat Agunim", player):
            return False
        
    if options.additional_goals.__contains__("Advanced Dragun"):
        if not state.has("Defeat The Advanced Dragun", player):
            return False

    return state.has("Defeat The Lich", player)

def set_rules(multiworld: MultiWorld, options: GungeonOptions, player, area_connections: typing.Dict[int, int], area_cost_map: typing.Dict[int, int]):
    total_chests = get_total_chests(options)
    
    #Make sure we have at least n progression items after opening a percentage of total chests
    for i in range (math.floor(total_chests * 0.125), total_chests):
        multiworld.get_location(get_chest_string(i), player).access_rule = lambda state: state.count_from_list(item_table, player) >= 1
    for i in range (math.floor(total_chests * 0.25), total_chests):
        multiworld.get_location(get_chest_string(i), player).access_rule = lambda state: state.count_from_list(item_table, player) >= 2
    for i in range (math.floor(total_chests * 0.375), total_chests):
        multiworld.get_location(get_chest_string(i), player).access_rule = lambda state: state.count_from_list(item_table, player) >= 3
    
    multiworld.get_location("The Old King", player).access_rule = lambda state: state.has("Old Crest", player)
    multiworld.get_location("The Resourceful Rat", player).access_rule = lambda state: state.has("Gnawed Key", player)
    multiworld.get_location("The Advanced Dragun", player).access_rule = lambda state: state.has("Weird Egg", player)
    multiworld.get_location("The Lich", player).access_rule = lambda state: state.count_from_list(item_table, player) >= 3

    multiworld.completion_condition[player] = lambda state: has_completed_objectives(multiworld, options, player, state)
