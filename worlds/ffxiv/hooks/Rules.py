
from BaseClasses import CollectionState, MultiWorld
from worlds.AutoWorld import World

from ..Helpers import get_option_value

# Sometimes you have a requirement that is just too messy or repetitive to write out with boolean logic.
# Define a function here, and you can use it in a requires string with (function_name()}.
# def overfishedAnywhere(world: World, mw: MultiWorld, state: CollectionState, player: int):
#     """Has the player collected all fish from any fishing log?"""
#     for cat, items in world.item_name_groups:
#         if cat.endswith("Fishing Log") and state.has_all(items, player):
#             return True
#     return False

# You can also pass an argument to your function, like |$function_name:arg|
def anyClassLevel(world: World, multiworld: MultiWorld, state: CollectionState, player: int, level: str):
    """Has the player reached the given level in any class?"""
    if int(level) < 5:
        return True
    for job in world.item_name_groups["DOW/DOM"]:
        if (state.count(job, player) * 5) >= int(level):
            return True
    return False

def anyCrafterLevel(world: World, multiworld: MultiWorld, state: CollectionState, player: int, level: str):
    """Has the player reached the given level in any class?"""
    if int(level) < 5:
        return True
    for job in world.item_name_groups["DOH"]:
        if (state.count(job, player) * 5) >= int(level):
            return True
    return False

def EnoughMemories(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Has the player collected enough Memories to complete the game?"""
    goal_count = get_option_value(multiworld, player, "mcguffins_needed")
    assert isinstance(goal_count, int)
    return state.count("Memory of a Distant World", player) >= goal_count
