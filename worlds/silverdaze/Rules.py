from typing import Dict, NamedTuple, Optional, Set

from BaseClasses import CollectionState
from typing import TYPE_CHECKING
from Locations import location_table
from worlds.generic.Rules import add_rule, set_rule
from worlds.generic.Rules import add_rule, forbid_item

if TYPE_CHECKING:
    from . import SDWorld

def set_rules(world: "SDWorld") -> None:
    player = world.player
    multiworld = world.multiworld


    def party(state: CollectionState, n: int) -> bool:
        return state.has_from_list_unique([
            "Pinn",
            "Kani",
            "Geo",
        ], player, n)

    def key(state: CollectionState, name: str) -> bool:
        return state.has(name, player)

    def boss(state: CollectionState) -> bool:
        return party(state,2)

    def chaos(state: CollectionState) -> bool:
        return party(state,4)

    #Sawyer: In the full game, add checks for all Wardens, glitches,etc.

    def get_entrance(entrance: str):
        return multiworld.get_entrance(entrance, player)

    def get_location(location: str):
        if location in location_table:
            location = location_table[location]

        return multiworld.get_location(location, player)
#You can't leave Geo's without a party member.
    set_rule(
        get_entrance("Leave_Geo_Room"),
        lambda state: party(state,1)
    )
#Demo entrances!
    set_rule(
        get_entrance("Red_Demo_Entrance"),
        lambda state: key(state, "Yellow Key")
    )

    set_rule(
        get_entrance("Red2_Demo_Entrance"),
        lambda state: key(state, "Yellow Key") and boss(state)
    )

    set_rule(
        get_entrance("Demo_End"),
        lambda state: party(state, 3)
    )

#Sawyer: Location Rules
    #Yellow Key
    set_rule(multiworld.get_location("Hub2Chest1", player),
        lambda state: key(state, "Yellow Key")
    )


    #Red Key
    set_rule(multiworld.get_location("Red1Chest", player),
        lambda state: key(state, "Red Key")
    )
    set_rule(multiworld.get_location("RedChasm2Chest1", player),
        lambda state: key(state, "Red Key")
    )
    set_rule(multiworld.get_location("Red3_BackdoorChest", player),
        lambda state: key(state, "Red Key")
    )
    set_rule(multiworld.get_location("Hub2Chest2", player),
        lambda state: key(state, "Red Key")
    )


    #Boss
    set_rule(multiworld.get_location("Nyx", player),
        lambda state: boss(state)
    )
    set_rule(multiworld.get_location("Nyx1", player),
        lambda state: boss(state)
    )
    set_rule(multiworld.get_location("Nyx2", player),
        lambda state: boss(state)
    )
    set_rule(multiworld.get_location("Nyx3", player),
        lambda state: boss(state)
    )
    set_rule(multiworld.get_location("QuoDefender1", player),
        lambda state: boss(state)
    )
    set_rule(multiworld.get_location("QuoDefender2", player),
        lambda state: boss(state)
    )
    set_rule(multiworld.get_location("QuoDefender3", player),
        lambda state: boss(state)
    )
    set_rule(multiworld.get_location("Kingoose1", player),
        lambda state: boss(state)
    )
    set_rule(multiworld.get_location("Kingoose2", player),
        lambda state: boss(state)
    )
    set_rule(multiworld.get_location("Kingoose3", player),
        lambda state: boss(state)
    )


    #Chaos Warden

    # Completion
def set_completion_rules(world: "SDWorld"):
    player = world.player
    multiworld = world.multiworld
    multiworld.completion_condition[player] = lambda state: state.can_reach("Demo_End", "Region", player)
    #Final game
    #multiworld.completion_condition[player] = lambda state: state.can_reach("Entropy", "Region", player)