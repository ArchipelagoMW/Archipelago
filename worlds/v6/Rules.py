import typing
from ..generic.Rules import add_rule
from .Regions import connect_regions

def _has_trinket_range(state,player,start,end) -> bool:
    for i in range(start,end):
        if (not state.has("Trinket " + str(i+1).zfill(2), player)):
            return False
    return True

def set_rules(world,player):
    connect_regions(world, player, "Menu", "Laboratory",      lambda state: _has_trinket_range(state,player,0,world.DoorCost[player].value))
    connect_regions(world, player, "Menu", "The Tower",       lambda state: _has_trinket_range(state,player,world.DoorCost[player].value,world.DoorCost[player].value*2))
    connect_regions(world, player, "Menu", "Space Station 2", lambda state: _has_trinket_range(state,player,world.DoorCost[player].value*2,world.DoorCost[player].value*3))
    connect_regions(world, player, "Menu", "Warp Zone",       lambda state: _has_trinket_range(state,player,world.DoorCost[player].value*3,world.DoorCost[player].value*4))

    #Special Rule for V
    add_rule(world.get_location("V",player), lambda state : state.can_reach("Laboratory",'Region',player) and
                                                            state.can_reach("The Tower",'Region',player) and
                                                            state.can_reach("Space Station 2",'Region',player) and
                                                            state.can_reach("Warp Zone",'Region',player))

    #Special Rule for NPC Trinket
    add_rule(world.get_location("NPC Trinket",player), lambda state: state.can_reach("Laboratory",'Region',player) or 
                                                                     state.can_reach("Space Station 2",'Region',player))

    connect_regions(world, player,  "Laboratory", "Menu", lambda state: True)
    connect_regions(world, player,  "The Tower", "Menu", lambda state: True)
    connect_regions(world, player,  "Space Station 2", "Menu", lambda state: True)
    connect_regions(world, player,  "Warp Zone", "Menu", lambda state: True)

    world.completion_condition[player] = lambda state: state.can_reach("V",'Location',player)
