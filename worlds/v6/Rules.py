import typing
from ..generic.Rules import add_rule
from .Regions import connect_regions

def _has_trinket_range(state,player,start,end):
    for i in range(start+1,end+1):
        if (not state.has("Trinket " + str(i).zfill(2), player)):
            return False
    return True

def create_npctrinket_rules(world,location,player):
    add_rule(location, lambda state: state.can_reach(world.get_region("Laboratory",player),'Region',player) or 
                                     state.can_reach(world.get_region("Space Station 2",player),'Region',player))

def set_rules(world,player):
    if (world.DoorCost[player].value == 0): pass
    connect_regions(world, player, "Menu", "Laboratory",      lambda state: _has_trinket_range(state,player,0,world.DoorCost[player].value))
    connect_regions(world, player, "Menu", "The Tower",       lambda state: _has_trinket_range(state,player,world.DoorCost[player].value,world.DoorCost[player].value*2))
    connect_regions(world, player, "Menu", "Space Station 2", lambda state: _has_trinket_range(state,player,world.DoorCost[player].value*2,world.DoorCost[player].value*3))
    connect_regions(world, player, "Menu", "Warp Zone",       lambda state: _has_trinket_range(state,player,world.DoorCost[player].value*3,world.DoorCost[player].value*4))

    connect_regions(world, player,  "Menu", "The Final Level", lambda state : state.can_reach("Laboratory",'Region',player) and
                                                                              state.can_reach("The Tower",'Region',player) and
                                                                              state.can_reach("Space Station 2",'Region',player) and
                                                                              state.can_reach("Warp Zone",'Region',player))

    connect_regions(world, player,  "Laboratory", "Menu", lambda state: True)
    connect_regions(world, player,  "The Tower", "Menu", lambda state: True)
    connect_regions(world, player,  "Space Station 2", "Menu", lambda state: True)
    connect_regions(world, player,  "Warp Zone", "Menu", lambda state: True)
    connect_regions(world, player,  "The Final Level", "Menu", lambda state: True)

    create_npctrinket_rules(world,world.get_location("NPC Trinket",player),player)
    world.completion_condition[player] = lambda state: state.can_reach(world.get_region("The Final Level",player),'Region',player)