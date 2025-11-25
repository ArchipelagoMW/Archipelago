#Sawyer: Okay we have a whole lotta locations, here's hoping for the best!

#Snagging all the below from APQuest again
from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import Items

if TYPE_CHECKING:
    from .World import SDWorld

#Okay, looks like everything needs an ID. Blehhh it is what it is, I'll just go in order from the default thingy.

LOCATION_NAME_TO_ID = {
    #Start Game
    "Ultima": 1,
    "PinnJoin": 2,
    "PinnMP3": 33,
    "StarterHealToken1": 3,
    "StarterHealToken3": 4,
    #Grey Zone 1
    "GeoJoin": 5,
    "GeoMP3": 34,
    "GeoWeapon1": 35,
    "Cotton2Chest1": 6,
    "Cotton3Chest1": 7,
    "YellowKey": 8,
    #Grey Zone 2
    "Hub2Chest1": 9,
    #Red Zone 1
    "Red1Chest": 10,
    "Red3Chest": 11,
    "Red3BackdoorChest": 33,
    #Red Zone 2
    "Red4Chest1": 12,
    "Red4Chest2": 13,
    "Red4Chest3": 14,
    "RedTower2Chest": 15,
    "RedTower3Chest": 16,
    "Kani": 18,
    "KaniMP3": 36,
    "KaniWeapon1": 37,
    "KaniWeapon2": 38,
    "KaniWeapon3": 39,
    "RedChasm1Chest": 19,
    "RedChasm2Chest1": 20,
    "RedChasm2Chest2": 21,
    "RedChasmReunionChest": 22,
    #Grey Zone Red Chest
    "Hub2Chest2": 23,
    #Red MiniBoss Drops
    "QuoDefender1": 24,
    "QuoDefender2": 25,
    "QuoDefender3": 26,
    "Kingoose1": 27,
    "Kingoose2": 28,
    "Kingoose3": 29,
    #Red Wardens
    "Nyx": 17,
    "Nyx1": 30,
    "Nyx2": 31,
    "Nyx3": 32,
}
#Sawyer: PHEW! That covers the demo stuff. It'll be fun adding more haha

class SDLocation(Location):
    game = "Silver Daze"

#Sawyer: NGL I don't really get this but APQuest said to do it.
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def create_all_locations(world: SDWorld) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: SDWorld) -> None:
    #Sawyer: First up, getting regions! I kinda wanna make this a function...
    #new_game = world.get_region("New_Game")

    geo_room = world.get_region("Geo_Room")
    cotton = world.get_region("Cotton")
    greyhub2 = world.get_region("GreyHub2")

    red1 = world.get_region("Red1")
    red2 = world.get_region("Red2")

    if world.options.minibosses:
        red1_minibosses = world.get_region("Red1_Minibosses")
        red2_minibosses = world.get_region("Red2_Minibosses")
    if world.options.wardens:
        red_wardens = world.get_region("Red_Wardens")

    #Sawyer: Now we add stuff to regions!

    #Sawyer: This is intentionally empty for easy copying!
    #new_game_locations = get_location_names_with_ids(
    #    [

    #    ]
    #)

    geo_room_locations = get_location_names_with_ids(
        [
            "Ultima","PinnJoin","PinnMP3","StarterHealToken1","StarterHealToken3",
        ]
    )
    geo_room.add_locations(geo_room_locations, SDLocation)

    cotton_locations = get_location_names_with_ids(
        [
            "GeoJoin","GeoJoin","GeoMP3","GeoWeapon1","Cotton2Chest1","Cotton3Chest1","YellowKey",
        ]
    )
    cotton.add_locations(cotton_locations, SDLocation)
    greyhub2_locations = get_location_names_with_ids(
        [
            "Hub2Chest1",
        ]
    )
    greyhub2.add_locations(greyhub2_locations,SDLocation)
    red1_locations = get_location_names_with_ids(
        [
            "Red1Chest","Red3Chest","Red3BackdoorChest",
        ]
    )
    red1.add_locations(red1_locations,SDLocation)
    red2_locations = get_location_names_with_ids(
        [
            "Red4Chest1","Red4Chest2","Red4Chest3","RedTower2Chest","RedTower3Chest","Nyx","Kani","KaniMP3",
            "KaniWeapon1","KaniWeapon2","KaniWeapon3","RedChasm1Chest","RedChasm2Chest1","RedChasm2Chest2",
            "RedChasmReunionChest","Hub2Chest2",
        ]
    )
    red2.add_locations(red2_locations,SDLocation)

    if world.options.minibosses:
        red1_minibosses_locations = get_location_names_with_ids(
            [
                "QuoDefender1","QuoDefender2","QuoDefender3",
         ]
        )
        red1_minibosses.add_locations(red1_minibosses_locations,SDLocation)
        red2_minibosses_locations = get_location_names_with_ids(
            [
                "Kingoose1","Kingoose2","Kingoose3",
            ]
        )
        red2_minibosses.add_locations(red2_minibosses_locations,SDLocation)


    if world.options.wardens:
        red_wardens_locations = get_location_names_with_ids(
            [
                "Nyx","Nyx1","Nyx2","Nyx3",
            ]
        )
        red_wardens.add_locations(red_wardens_locations,SDLocation)

#Sawyer: Okay, the game literally has zero events because we turned all of those into items. Soooo... don't sweat it?
#Sawyer: I put the regions here just so my IDE wouldn't scream at me for leaving this empty.
def create_events(world: SDWorld) -> None:
    #new_game = world.get_region("New_Game")

    geo_room = world.get_region("Geo_Room")
    cotton = world.get_region("Cotton")
    greyhub2 = world.get_region("GreyHub2")

    red1 = world.get_region("Red1")
    red2 = world.get_region("Red2")