from typing import Dict, NamedTuple, Optional, Set

from BaseClasses import CollectionState
from typing import TYPE_CHECKING
from Locations import location_table
from worlds.generic.Rules import add_rule, set_rule
from worlds.generic.Rules import add_rule, forbid_item

from . import Items

if TYPE_CHECKING:
    from . import SDWorld










def set_rules(world: "SDWorld") -> None:
    player = world.player
    multiworld = world.multiworld

    # Custom rules

    def sd_party_size_meets(state: CollectionState, size: int) -> bool:
        # party_members is all items that are party members
        # keys is just the strings, which are item names
        return state.has_from_list_unique(Items.party_members.keys(), player, size)

    def sd_has_key(state: CollectionState, color:str) -> bool:
        return state.has(Items.get_key_from_color(color))
    
    def sd_can_fight_demo_boss(state: CollectionState) -> bool:
        return sd_party_size_meets(state, 2)
    
    # Nat: What does this do?
    def chaos(state: CollectionState) -> bool:
        return sd_party_size_meets(state, 4)

    #Sawyer: In the full game, add checks for all Wardens, glitches,etc.

    # Shorthands
    
    def get_entrance(entrance: str):
        return multiworld.get_entrance(entrance, player)

    def get_location(location: str):
        return multiworld.get_location(location, player)
    # def get_location(location: str):
    #     if location in location_table:
    #         location = location_table[location]
    #     return multiworld.get_location(location, player)

    # Rules!

    #You can't leave Geo's without a party member.
    set_rule(
        get_entrance("Leave_Geo_Room"),
        lambda state: sd_party_size_meets(state,1)
    )
    
    #Demo entrances!
    
    set_rule(
        get_entrance("Red_Demo_Entrance"),
        lambda state: sd_has_key(state, "yellow")
    )

    set_rule(
        get_entrance("Red2_Demo_Entrance"),
        lambda state: sd_has_key(state, "yellow") and sd_can_fight_demo_boss(state)
    )

    set_rule(
        get_entrance("Demo_End"),
        lambda state: sd_party_size_meets(state, 3)
    )

    #Sawyer: Location Rules
    
    #Yellow Key
    set_rule(get_location("Hub2Chest1"),
        lambda state: sd_has_key(state, "yellow")
    )


    #Red Key
    set_rule(get_location("Red1Chest"),
        lambda state: sd_has_key(state, "red")
    )
    set_rule(get_location("RedChasm2Chest1"),
        lambda state: sd_has_key(state, "red")
    )
    set_rule(get_location("Red3_BackdoorChest"),
        lambda state: sd_has_key(state, "red")
    )
    set_rule(get_location("Hub2Chest2"),
        lambda state: sd_has_key(state, "red")
    )


    #Boss
    set_rule(get_location("Nyx"),
        lambda state: sd_can_fight_demo_boss(state)
    )
    set_rule(get_location("Nyx1"),
        lambda state: sd_can_fight_demo_boss(state)
    )
    set_rule(get_location("Nyx2"),
        lambda state: sd_can_fight_demo_boss(state)
    )
    set_rule(get_location("Nyx3"),
        lambda state: sd_can_fight_demo_boss(state)
    )
    set_rule(get_location("QuoDefender1"),
        lambda state: sd_can_fight_demo_boss(state)
    )
    set_rule(get_location("QuoDefender2"),
        lambda state: sd_can_fight_demo_boss(state)
    )
    set_rule(get_location("QuoDefender3"),
        lambda state: sd_can_fight_demo_boss(state)
    )
    set_rule(get_location("Kingoose1"),
        lambda state: sd_can_fight_demo_boss(state)
    )
    set_rule(get_location("Kingoose2"),
        lambda state: sd_can_fight_demo_boss(state)
    )
    set_rule(get_location("Kingoose3"),
        lambda state: sd_can_fight_demo_boss(state)
    )

    #Chaos Warden

    # Completion
def set_completion_rules(world: "SDWorld"):
    player = world.player
    multiworld = world.multiworld
    multiworld.completion_condition[player] = lambda state: state.can_reach("Demo_End", "Region", player)
    #Final game
    #multiworld.completion_condition[player] = lambda state: state.can_reach("Entropy", "Region", player)