from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from .world import SDWorld


def set_all_rules(world: SDWorld) -> None:

    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


#Sawyer: The following are special rule shorthands for easy checking.
lookup_key_from_color = {
    "red": "Red Key",
    "orange": "Orange Key",
    "yellow": "Yellow Key",
    "green": "Green Key",
    "blue": "Blue Key",
    "purple": "Purple Key",
    "black": "Black Key"
    }

def get_key_from_color(color: str) -> str:
    # Nat: This could be made to just color.lower().capitalize() then append " Key"
    # and return, but we wanna prevent user errors in this house.
    color = color.lower()
    assert (color in lookup_key_from_color.keys()), f"Input '{color}' is not a valid key color."
    return lookup_key_from_color[color]

def sd_party_size_meets(state: CollectionState, size: int) -> bool:
    # party_members is all items that are party members
    # keys is just the strings, which are item names
    return state.has_from_list_unique(Items.party_members.keys(), player, size)

def sd_has_key(state: CollectionState, color: str) -> bool:
    return state.has(get_key_from_color(color))

def sd_can_fight_miniboss(state: CollectionState) -> bool:
    return sd_party_size_meets(state, 2)

def sd_can_fight_warden(state: CollectionState) -> bool:
    return sd_party_size_meets(state, 3)

def sd_can_fight_chaos_warden(state: CollectionState) -> bool:
    return sd_party_size_meets(state, 5)

#End of shorthands


#Sawyer: Entrance time!
def set_all_entrance_rules(world: SDWorld) -> None:
    player = world.player
    multiworld = world.multiworld
    #Sawyer: Below is a var to make it so we don't have to type CollectionState every time we wanna check a function.
    mystate = CollectionState

    begin_new_game = world.get_entrance("Begin_New_Game")
    leave_geo_room = world.get_entrance("Leave_Geo_Room")
    door_to_hub_2 = world.get_entrance("Door_To_Hub_2")
    red_main_entrance = world.get_entrance("Red_Main_Entrance")
    red_kingoose_boss_door = world.get_entrance("Red_Kingoose_Boss_Door")




    set_rule(door_to_hub_2, sd_has_key(mystate,'yellow'))
    set_rule(red_main_entrance, sd_has_key(mystate,'yellow'))
    set_rule(red_kingoose_boss_door, sd_has_key(mystate,'yellow') and sd_can_fight_miniboss(mystate))

    if world.options.minibosses:
        fight_red1_miniboss = world.get_entrance("Fight_Red1_Miniboss")
        fight_red2_miniboss = world.get_entrance("Fight_Red2_Miniboss")

        set_rule(fight_red1_miniboss, sd_can_fight_miniboss(mystate))
        set_rule(fight_red2_miniboss, sd_can_fight_miniboss(mystate))


    if world.options.wardens:
        fight_red_warden = world.get_entrance("Fight_Red_Warden")

        set_rule(fight_red_warden, sd_can_fight_warden(mystate))

#Sawyer: These are the location rules! Hoo boy there are many haha
def set_all_location_rules(world: SDWorld) -> None:
    player = world.player
    multiworld = world.multiworld
    mystate = CollectionState

    #Sawyer: Don't forget to define the locations we're adding rules to here.
    hub2chest2 = world.get_location("Hub2Chest2")
    red1chest = world.get_location("Red1Chest")
    redchasm2chest1 = world.get_location("RedChasm2Chest1")
    red3backdoorchest = world.get_location("Red3BackdoorChest")

    add_rule(hub2chest2, sd_has_key(mystate,'red'))
    add_rule(red1chest, sd_has_key(mystate,'red'))
    add_rule(redchasm2chest1, sd_has_key(mystate,'red'))
    add_rule(red3backdoorchest, sd_has_key(mystate,'red'))

#Sawyer: Time for the wincon! For now it'll just be three party members but once the demo works it should be Entropy
def set_completion_condition(world: APQuestWorld) -> None:
    player = world.player
    multiworld = world.multiworld
    mystate = CollectionState

    world.multiworld.completion_condition[world.player] = sd_party_size_meets(mystate, 3)

