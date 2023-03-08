import collections
import typing
from .Locations import DLCquestLocation
from ..generic.Rules import add_rule, set_rule
from .Items import DLCquestItem
from BaseClasses import ItemClassification


def create_event(player, event: str):
    return DLCquestItem(event, ItemClassification.progression, None, player)

def set_rules(world, player, option):
    set_rule(world.get_entrance("Moving", player),
             lambda state: state.has("Movement Pack", player))
    set_rule(world.get_entrance("Cloud", player),
             lambda state: state.has("Psychological Warfare Pack", player))
    set_rule(world.get_entrance("Forest Entrance", player),
             lambda state: state.has("Map Pack", player))
    set_rule(world.get_entrance("Behind Ogre", player),
             lambda state: state.has("Gun Pack", player))
    set_rule(world.get_entrance("Forest True Double Jump", player),
             lambda state: state.has("Double Jump Pack", player))

    if world.time_is_money[player].value == 0 :
        set_rule(world.get_entrance("Tree", player),
                 lambda state: state.has("Time is Money Pack", player))

    if world.double_jump_glitch[player].value == 0 :
        set_rule(world.get_entrance("Cloud Double Jump", player),
                lambda state: state.has("Double Jump Pack", player))
        set_rule(world.get_entrance("Forest Double Jump", player),
                lambda state: state.has("Double Jump Pack", player))

    if world.double_jump_glitch[player].value < 2:
        set_rule(world.get_entrance("Behind Tree Double Jump", player),
                lambda state: state.has("Double Jump Pack", player))

    set_rule(world.get_location("Movement Pack", player),
             lambda state: state.has("Coin", player, 4))
    set_rule(world.get_location("Animation Pack", player),
             lambda state: state.has("Coin", player, 5))
    set_rule(world.get_location("Audio Pack", player),
             lambda state: state.has("Coin", player, 5))
    set_rule(world.get_location("Pause Menu Pack", player),
             lambda state: state.has("Coin", player, 5))
    set_rule(world.get_location("Time is Money Pack", player),
             lambda state: state.has("Coin", player, 20))
    set_rule(world.get_location("Double Jump Pack", player),
             lambda state: state.has("Coin", player, 100))
    set_rule(world.get_location("Pet Pack", player),
             lambda state: state.has("Coin", player, 5))
    set_rule(world.get_location("Sexy Outfits Pack", player),
             lambda state: state.has("Coin", player, 5))
    set_rule(world.get_location("Top Hat Pack", player),
             lambda state: state.has("Coin", player, 5))
    set_rule(world.get_location("Map Pack", player),
             lambda state: state.has("Coin", player, 140))
    set_rule(world.get_location("Gun Pack", player),
             lambda state: state.has("Coin", player, 75))
    set_rule(world.get_location("The Zombie Pack", player),
             lambda state: state.has("Coin", player, 5))
    set_rule(world.get_location("Night Map Pack", player),
             lambda state: state.has("Coin", player, 75))
    set_rule(world.get_location("Psychological Warfare Pack", player),
             lambda state: state.has("Coin", player, 50))
    set_rule(world.get_location("Armor for your Horse Pack", player),
             lambda state: state.has("Coin", player, 250))
    set_rule(world.get_location("Finish the Fight Pack", player),
             lambda state: state.has("Coin", player, 5))

    loc_win = DLCquestLocation(player,"Winning", None, world.get_region("The Final Boss Room", player))
    world.get_region("The Final Boss Room", player).locations.append(loc_win)
    loc_win.place_locked_item(create_event(player, "Victory"))
    set_rule(world.get_location("Winning", player), lambda state: state.can_reach("The Final Boss Room", 'Region', player) and
                                                            state.has("Armor for your Horse Pack", player)) and state.has("Finish The Fight Pack")
    world.completion_condition[player] = lambda state: state.has("Victory", player)



