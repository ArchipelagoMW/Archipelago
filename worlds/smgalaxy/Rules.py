from typing import TYPE_CHECKING
from .regions import connect_regions, region_list
from.Constants.Names import region_names as regname

if TYPE_CHECKING:
    from . import SMGWorld

# main stage logic
def set_rules(world: "SMGWorld", player: int):
    # Dome 1
    connect_regions(world, player, regname.SHIP, regname.TERRACE, "Dome 1 Entry")
    connect_regions(world, player, regname.TERRACE, regname.GOODEGG, "Terrace Inner Orbit Galaxy")
    connect_regions(world, player, regname.TERRACE, regname.HONEYHIVE, "Terrace Second Orbit Galaxy")
    connect_regions(world, player, regname.TERRACE, regname.LOOPDEELOOP, "Terrace Third Orbit Galaxy")
    connect_regions(world, player, regname.TERRACE, regname.FLIPSWITCH, "Terrace Fourth Orbit Galaxy")
    connect_regions(world, player, regname.TERRACE, regname.BOWJR1, "Terrace Outer Orbit Galaxy")
    # Dome 2
    connect_regions(world, player, regname.SHIP, regname.FOUNTAIN, "Dome 2 Entry",
                    lambda state: state.has("Grand Star", player))
    connect_regions(world, player, regname.FOUNTAIN, regname.SPACEJUNK, "Fountain Inner Orbit Galaxy")
    connect_regions(world, player, regname.FOUNTAIN, regname.ROLLINGGREEN, "Fountain Second Orbit Galaxy")
    connect_regions(world, player, regname.FOUNTAIN, regname.BATTLEROCK, "Fountain Third Orbit Galaxy")
    connect_regions(world, player, regname.FOUNTAIN, regname.HURRYSCUR, "Fountain Fourth Orbit Galaxy")
    connect_regions(world, player, regname.FOUNTAIN, regname.BOWSER1, "Fountain Outer Orbit Galaxy")
    # Dome 3
    connect_regions(world, player, regname.SHIP, regname.KITCHEN, "Dome 3 Entry",
                    lambda state: state.has("Grand Star", player, 2))
    connect_regions(world, player, regname.KITCHEN, regname.BEACHBOWL, "Kitchen Inner Orbit Galaxy")
    connect_regions(world, player, regname.KITCHEN, regname.BUBBLEBREEZE, "Kitchen Second Orbit Galaxy")
    connect_regions(world, player, regname.KITCHEN, regname.GHOSTLY, "Kitchen Third Orbit Galaxy")
    connect_regions(world, player, regname.KITCHEN, regname.BUOY, "Kitchen Fourth Orbit Galaxy")
    connect_regions(world, player, regname.KITCHEN, regname.BOWJR2, "Kitchen Outer Orbit Galaxy")
    # Dome 4
    connect_regions(world, player, regname.SHIP, regname.BEDROOM, "Dome 4 Entry",
                    lambda state: state.has("Grand Star", player, 3))
    connect_regions(world, player, regname.BEDROOM, regname.GUSTY, "Bedroom Inner Orbit Galaxy")
    connect_regions(world, player, regname.BEDROOM, regname.FREEZEFLAME, "Bedroom Second Orbit Galaxy")
    connect_regions(world, player, regname.BEDROOM, regname.DUSTY, "Bedroom Third Orbit Galaxy")
    connect_regions(world, player, regname.BEDROOM, regname.HONEYCLIMB, "Bedroom Fourth Orbit Galaxy")
    connect_regions(world, player, regname.BEDROOM, regname.BOWSER2, "Bedroom Outer Orbit Galaxy")
    # Dome 5
    connect_regions(world, player, regname.SHIP, regname.ENGINE, "Dome 5 Entry",
                    lambda state: state.has("Grand Star", player, 4))
    connect_regions(world, player, regname.ENGINE, regname.GOLDLEAF, "Engine Room Inner Orbit Galaxy")
    connect_regions(world, player, regname.ENGINE, regname.SEASLIDE, "Engine Room Second Orbit Galaxy")
    connect_regions(world, player, regname.ENGINE, regname.TOYTIME, "Engine Room Third Orbit Galaxy")
    connect_regions(world, player, regname.ENGINE, regname.BONEFIN, "Engine Room Fourth Orbit Galaxy")
    connect_regions(world, player, regname.ENGINE, regname.BOWJR3, "Engine Room Outer Orbit Galaxy")
    # Dome 6
    connect_regions(world, player, regname.SHIP, regname.GARDEN, "Dome 6 Entry",
                    lambda state: state.has("Grand Star", player, 5))
    connect_regions(world, player, regname.GARDEN, regname.DEEPDARK, "Garden Inner Orbit Galaxy")
    connect_regions(world, player, regname.GARDEN, regname.DREADNOUGHT, "Garden Second Orbit Galaxy")
    connect_regions(world, player, regname.GARDEN, regname.MATTER, "Garden Third Orbit Galaxy")
    connect_regions(world, player, regname.GARDEN, regname.MELTY, "Garden Outer Orbit Galaxy")
    #Remaining Ship Connections
    connect_regions(world, player, regname.SHIP, regname.LIBRARY, "Library Entrance")
    connect_regions(world, player, regname.SHIP, regname.COTU, "Center Of the Universe Entry",
                    lambda state: state.has("Grand Star", player, 5) and state.has("Power Star", player, world.options.stars_to_finish.value))
    connect_regions(world, player, regname.COTU, regname.BOWSER3, "Galaxy's Center")
    connect_regions(world, player, regname.SHIP, regname.SWEETSWEET, "Sweet Sweet Hungry Luma")
    connect_regions(world, player, regname.SHIP, regname.SLINGPOD, "Sling Pod Hungry Luma",
                    lambda state: state.has("Grand Star", player))
    connect_regions(world, player, regname.SHIP, regname.DRIPDROP, "Drip Drop Hungry Luma",
                    lambda state: state.has("Grand Star", player, 2))
    connect_regions(world, player, regname.SHIP, regname.BIGMOUTH, "Bigmouth Hungry Luma",
                    lambda state: state.has("Grand Star", player, 3))
    connect_regions(world, player, regname.SHIP, regname.SANDSPIRAL, "Sand Spiral Hungry Luma",
                    lambda state: state.has("Grand Star", player, 4))
    connect_regions(world, player, regname.SHIP, regname.SNOWCAP, "Snow Cap Hungry Luma",
                    lambda state: state.has("Grand Star", player, 5))
    connect_regions(world, player, regname.SHIP, regname.GATEWAY, "Gateway Dome")
    connect_regions(world, player, regname.SHIP, regname.BOOBONE, "Boo's Boneyard Hungry Luma")
    connect_regions(world, player, regname.SHIP, regname.ROLLINGGIZ, "Rolling Gizmo Launch Star",
                    lambda state: state.has("Green Star", player))
    connect_regions(world, player, regname.SHIP, regname.LOOPDEESWOOP, "Loopdeeswoop Launch Star",
                    lambda state: state.has("Green Star", player))
    connect_regions(world, player, regname.SHIP, regname.BUBBLEBLAST, "Bubble Blast Launch Star",
                    lambda state: state.has("Green Star", player))
    # connect_regions(world, player, regname.SHIP, regname.FINALE, "Grand Finale Launch Star",
    #                 lambda state: state.has("Green Star", player) and state.has("Power Star", player, 120))
    world.multiworld.completion_condition[player] = lambda state: state.has("Peach", player)


    # # special stages logic Left here for reference later on default values
    # add_rule(world.get_location("LDL: Surfing 101"), lambda state: state.has("Power Star", player, 5))
    # add_rule(world.get_location("FS: Painting the Planet Yellow"), lambda state: state.has("Power Star", player, 7))
    # add_rule(world.get_location("RG: Rolling in the Clouds"), lambda state: state.has("Power Star", player, 11) and state.has("Progressive Grand Star"))
    # add_rule(world.get_location("HS: Shrinking Satellite"), lambda state: state.has ("Power Star", player, 18) and state.has("Progressive Grand Star", player))
    # add_rule(world.get_location("BUB: Through the Poison Swamp"), lambda state: state.has ("Power Star", player, 19) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("BB: The Secret of Buoy Base"), lambda state: state.has ("Power Star", player, 30) and state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player))
    # add_rule(world.get_location("BB: The Floating Fortress"), lambda state: state.has ("Power Star", player, 30) and state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player))
    # add_rule(world.get_location("BF: Kingfin's Fearsome Waters"), lambda state: state.has("Power Star", player, 55) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("MS: Watch Your Step"), lambda state: state.has("Power Star", player, 50) and state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("DDR: Giant Eel Breakout"), lambda state: state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("RGT: Gizmos, Gears, and Gadgets"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player) and state.has("Green Star", player, 3))
    # add_rule(world.get_location("LDT: The Galaxy's Greatest Wave"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player) and state.has("Progressive Grand Star", player, 2) and state.has("Green Star", player, 3))
    # add_rule(world.get_location("BBT: The Electric Labyrinth"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player) and state.has("Progressive Grand Star", player, 2) and state.has("Green Star", player, 3))
    # add_rule(world.get_location("SS: Rocky Road"), lambda state: state.has("Power Star", player, 7))
    # add_rule(world.get_location("SP: A Very Sticky Situation"), lambda state: state.has("Progressive Grand Star", player) and state.has("Power Star", player, 9))
    # add_rule(world.get_location("BM: Bigmouth's Gold Bait"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Power Star", player, 29))
    # add_rule(world.get_location("Sandy Spiral: Choosing a Favorite Snack"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Power Star", player, 36) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("Bone's Boneyard: Racing the Spooky Speedster"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("SC: Star Bunnies in the Snow"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Power Star", player, 52))
    # # comet logic
    # add_rule(world.get_location("GE: Dino Piranha Speed Run"), lambda state: state.has("Power Star", player, 13))
    # add_rule(world.get_location("HH: Honeyhive Cosmic Mario Race"), lambda state: state.has("Power Star", player, 13))
    # add_rule(world.get_location("SJ: Pull Star Path Speed Run"), lambda state: state.has("Power Star", player, 13))
    # add_rule(world.get_location("BR: Topmanic's Dardevil Run"), lambda state: state.has("Power Star", player, 13))
    # add_rule(world.get_location("BB: Fast Foes on the Cyclone Stone"), lambda state: state.has("Power Star", player, 13))
    # # boss stage logic
    # add_rule(world.get_location("BJ: Megaleg's Moon"), lambda state: state.has("Power Star", player, 8))
    # add_rule(world.get_location("B: The Firery Stronghold"), lambda state: state.has("Power Star", player, 15) and state.has("Progressive Grand Star", player))
    # add_rule(world.get_location("BJ: Sinking the Airships"), lambda state: state.has("Power Star", player, 23) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("BJ: King Kaliente's Spicy Return"), lambda state: state.has("Power Star", player, 45) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("B:  Darkness on the Horizon"), lambda state: state.has("Power Star", player, 33) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("B: Bowser's Galaxy Reactor"), lambda state: state.has("Power Star", player, world.options.stars_to_finish.value) and state.has("Progressive Grand Star", player, 2))
    #
    #
    # # purple coin star logic
    # if world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_all:
    #     add_rule(world.get_location("DN: Battlestation's Purple Coins"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("MM: Red-Hot Purple Coins"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("TT: Luigi's Purple Coins"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("DD: Plunder the Purple Coins"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("GL: Purple Coins in the Woods"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("FF: Purple Coins on the Summit"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("SS: Purple Coins by the Seaside"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("GG: Purple Coins on the Puzzle Cube"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("G: Purple Coins in the Bone Pen"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("DDune: Purple Coin in the Desert"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("BR: Purple Coins on the Battlerock"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("GE: Purple Coin Omelet"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("HH: The Honeyhive's Purple Coins"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("SJ: Purple Coin Spacewalk"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("GG: Gateway's Purple coins"), lambda state: state.has("Peach", player))
    # elif world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_main_game_only:
    #       add_rule(world.get_location("GG: Gateway's Purple coins"), lambda state: state.has("Grand Star Engine", player))
    # else:
    #     return


