from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import TVRUHHWorld



def create_and_connect_regions(world: TVRUHHWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: TVRUHHWorld) -> None:
    #create regions
    start = Region("Start", world.player, world.multiworld)
    quickplay_unlocked = Region("Unlocked Quickplay", world.player, world.multiworld)
    alt_story_unlocked = Region("Unlocked Alt Story", world.player, world.multiworld)
    towers_unlocked = Region("Unlocked Towers", world.player, world.multiworld)
    endless_nm_unlocked = Region("Unlocked Endless Nightmare", world.player, world.multiworld)

    #collection of regions
    regions = [
        start,
        quickplay_unlocked,
        alt_story_unlocked,
        towers_unlocked
    ]


    #submit regions
    world.multiworld.regions.extend(regions)
    
    for x in locked_monster_names:
        world.multiworld.regions.append(Region("(start) Monster Unlocked: "+x, world.player,world.multiworld))
    for x in locked_monster_names:
        world.multiworld.regions.append(Region("(QP) Monster Unlocked: "+x, world.player,world.multiworld))
    
    for x in character_names:
        world.multiworld.regions.append(Region("(start) Character Unlocked: "+x, world.player,world.multiworld))
    for x in character_names:
        world.multiworld.regions.append(Region("(qp) Character Unlocked: "+x, world.player,world.multiworld))
    for x in character_names:
        world.multiworld.regions.append(Region("(altstory) Character Unlocked: "+x, world.player,world.multiworld))
    for x in character_names:
        world.multiworld.regions.append(Region("(towers) Character Unlocked: "+x, world.player,world.multiworld))
    for x in character_names:
        world.multiworld.regions.append(Region("(endless nm) Character Unlocked: "+x, world.player,world.multiworld))
    for x in character_names:
        world.multiworld.regions.append(Region("(endless str) Character Unlocked: "+x, world.player,world.multiworld))
    
def connect_regions(world: TVRUHHWorld) -> None:

    req_region(world,"Start").connect(req_region(world,"Unlocked Quickplay"),"Start to Quickplay")
    req_region(world,"Start").connect(req_region(world,"Unlocked Alt Story"),"Start to Alt Story")

    for x in world.get_regions():
        if str(x).find("(QP) Monster Unlocked: "):
            req_region(world,"Unlocked Quickplay").connect(req_region(world, "Unlocked Quickplay"),"Quickplay to " + str(x))
        if str(x).find("(start) Monster Unlocked: "):
            req_region(world,"Start").connect(req_region(world, "Start"),"Start to " + str(x))

def req_region(world: TVRUHHWorld, region:str) -> Region:
    return world.get_region(region)

locked_monster_names = [
    # shambles
    "Shy Scrambla",
    "Boiler",
    "Rage Boiler",
    "Shiny Knot Knott",
    "Avoidant Blot",
    "Null Blot",
    "Amalga",
    "Calorie",
    "Shiny Joule",
    "Emerald",
    "Moss",
    "Shamra",
    # guardians
    "Shiny Rendy",
    "Snowball",
    "Shiny Snowball",
    "Alter Roundsaw",
    "Null Roundsaw",
    "Shy Lila",
    "Voladrome",
    "Shanx",
    "Alter Shanx",
    "Ruby",
    "Scarlet",
    "Guardian Soul",
    # eyeric glyphs
    "Dendrohai",
    "Hematoren",
    "Lavalin",
    "Heliola",
    "Chionotoh",
    "Astrayo",
    "Monovai",
    "Philolu",
    "Topaz",
    "Dandy",
    "Oudenai",
    # zaramechs
    "Unit Lulu",
    "Null Unit",
    "Rage Prisma",
    "Dual Prisma",
    "Alter Syncron",
    "Shiny Syncron",
    "Flip Flap",
    "Sentinel 0X",
    "Ventra",
    "Sapphire",
    "Indigo",
    "Default",
    # glass flora
    "Alter Glacia",
    "Null Glacia",
    "Avoidant Vitrea",
    "Rage Duet",
    "Pearl",
    "Momo",
    "Shy Momo",
    "Shiny Momo",
    "Citrine",
    "Amber",
    "Echo",
    # veyerals
    "Voltage Veyeral",
    "Frozen Veyeral",
    "Vibrant Veyeral",
    "Veyeral Quartet",
    "Veyeral Rain",
    "Shiny Veyerals",
    "Storm Veyeral",
    "Molten Veyeral",
    "Blizzard Veyeral",
    "Amethyst",
    "Violet",
    "Forma",
    "Totaria",
    "Blue Veyeral",
    # special monsters
    "Wisp",
    "Shiny Anomaly",
    "Stella",
    "Celestia",
    "Unity",
    "Chroma",
    "Duality",
    "Trinity",
    "Avoidant Stella",
    "Rage Celestia",
    "Ember Polyps",
    "Volt Polyps",
    "Tox Polyps",
    "Nova",
    "Limbo"
]

character_names = [
    "Defect",
    "Twin",
    "Devil",
    "Alt. Blank",
    "Alt. Defect",
    "Alt. Twin",
    "Alt. Devil"
]