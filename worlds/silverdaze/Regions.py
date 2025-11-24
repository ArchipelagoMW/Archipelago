#Sawyer: Don't know what a lot of this is but we'll get there!
from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .World import SDWorld

def create_and_connect_regions(world: SDWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

 # Sawyer: Okay, we had some regions defined in our last attempts.
def create_all_regions(world: SDWorld) -> None:
    #Sawyer: Probably not using New Game but it's the menu region so we should keep it here to be safe.
    new_game = Region("New_Game", world.player, world.multiworld)

    geo_room = Region("Geo_Room", world.player, world.multiworld)
    cotton = Region("Cotton", world.player, world.multiworld)
    greyhub2 = Region("GreyHub2", world.player, world.multiworld)

    #Sawyer: In vanilla, we didn't have the first instance of a zone named. Bad idea, but don't forget that red1 is 'red'
    red1 = Region("Red1", world.player, world.multiworld)
    red2 = Region("Red2", world.player, world.multiworld)

    #Sawyer: Putting them all together now! Don't forget to add the full game's regions when you're done!
    regions = [geo_room, cotton, greyhub2, red1, red2]

    #Sawyer: Bosses are optional so they'll be their own region.
    if world.options.minibosses:
        red1_minibosses = Region("Red1_Minibosses", world.player, world.multiworld)
        red2_minibosses = Region("Red2_Minibosses", world.player, world.multiworld)

        regions.append(red1_minibosses)
        regions.append(red2_minibosses)

    if world.options.wardens:
        red_wardens = Region("Red_Wardens", world.player, world.multiworld)

        regions.append(red_wardens)

    #Sawyer: Add it all together now!
    world.multiworld.regions += regions

#Sawyer: Next part has me nervous. This is entrances, right?
def connect_regions(world: SDWorld) -> None:
    new_game = world.get_region("New_Game")

    geo_room = world.get_region("Geo_Room")
    cotton = world.get_region("Cotton")
    greyhub2 = world.get_region("GreyHub2")

    red1 = world.get_region("Red1")
    red2 = world.get_region("Red2")

    #Sawyer: Siiiiigh Here goes!
    new_game.connect(geo_room, "Begin_New_Game")
    geo_room.connect(cotton, "Leave_Geo_Room")
    cotton.connect(greyhub2, "Door_To_Hub_2")
    greyhub2.connect(red1, 'Red_Main_Entrance')
    #Sawyer: This is the first connection with a special requirement,
    # being that you need two party members to pass Kingoose in logic. Return here when you define that correctly.
    red1.connect(red2, 'Red_Kingoose_Boss_Door')

    #Sawyer: Here's the optional bit again. Not using it yet but perhaps we will!
    if world.options.minibosses:
        red1_minibosses = world.get_region("Red1_Minibosses")
        red2_minibosses = world.get_region("Red2_Minibosses")

        red1.connect(red1_minibosses,"Fight_Red1_Miniboss")
        red2.connect(red2_minibosses,"Fight_Red2_Miniboss")
    if world.options.wardens:
        red_wardens = world.get_region("Red_Wardens")

        red2.connect(red_wardens,"Fight_Red_Warden")