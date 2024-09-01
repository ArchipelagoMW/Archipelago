from BaseClasses import Region
from .Types import EpisodeType, Sly1Location
from .Locations import location_table
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Sly1World

episode_regions = {
    EpisodeType.ToT:      "Tides of Terror",
    EpisodeType.SSE:      "Sunset Snake Eyes",
    EpisodeType.VV:       "Vicious Voodoo",
    EpisodeType.FitS:     "Fire in the Sky"
}

## Would be for level randomizing if that ever happens
# level_names = {
#     "A Stealthy Approach":      "Tides of Terror - Intro",
#     "Into the Machine":         "Tides of Terror - First Gate",
#     "High Class Heist":         "Tides of Terror - First Gate",
#     "The Fire Down Below":      "Tides of Terror - First Gate",
#     "A Cunning Disguise":       "Tides of Terror - First Gate",
#     "The Gunboat Graveyard":    "Tides of Terror - Second Gate",
#     "Treasure in the Depths":   "Tides of Terror - Second Gate",
#     "The Eye of the Storm":     "Tides of Terror - Boss",

#     "A Rocky Start":            "Sunset Snake Eyes - Intro",
#     "At the Dog Track":         "Sunset Snake Eyes - First Gate",
#     "Murray's Big Gamble":      "Sunset Snake Eyes - First Gate",
#     "Boneyard Casino":          "Sunset Snake Eyes - First Gate",
#     "Straight to the Top":      "Sunset Snake Eyes - Second Gate",
#     "Two to Tango":             "Sunset Snake Eyes - Second Gate",
#     "Back Alley Heist":         "Sunset Snake Eyes - Second Gate",
#     "Last Call":                "Sunset Snake Eyes - Boss",

#     "The Dread Swamp Path":     "Vicious Voodoo - Intro",
#     "The Lair of the Beast":    "Vicious Voodoo - First Gate",
#     "A Grave Undertaking":      "Vicious Voodoo - First Gate",
#     "Piranha Lake":             "Vicious Voodoo - First Gate",
#     "Descent into Danger":      "Vicious Voodoo - Second Gate",
#     "A Ghastly Voyage":         "Vicious Voodoo - Second Gate",
#     "Down Home Cooking":        "Vicious Voodoo - Second Gate",
#     "A Deadly Dance":           "Vicious Voodoo - Boss",

#     "A Perilous Ascent":        "Fire in the Sky - Intro",
#     "Flaming Temple of Flame":  "Fire in the Sky - First Gate",
#     "The Unseen Foe":           "Fire in the Sky - First Gate",
#     "The King of the Hill":     "Fire in the Sky - First Gate",
#     "Rapid Fire Assault":       "Fire in the Sky - Second Gate",
#     "A Desperate Race":         "Fire in the Sky - Second Gate",
#     "Duel by the Dragon":       "Fire in the Sky - Second Gate",
#     "Flame Fu!":                "Fire in the Sky - Boss",

#     "The Cold Heart of Hate":   "The Cold Heart of Hate"
# }

def create_regions(world: "Sly1World"): 
    # I think this is where I would stitch in the paris files with a menu region
    # That connects to both the hideout and paris through a save file
    menu = create_region(world, "Menu")
    hideout = create_region_and_connect(world, "Hideout", "Save File -> Hideout", menu)

    # ------------------------------- Tides of Terror ---------------------------------- #
    tot_intro = create_region_and_connect(world, "Stealthy Approach", "Hideout -> Stealthy Approach", hideout)
    tot_hub = create_region_and_connect(world, "Prowling the Grounds", "Hideout -> Prowling the Grounds", hideout)
    tot_2 = create_region_and_connect(world, "Into the Machine", "Prowling the Grounds -> Into the Machine", tot_hub)
    tot_3 = create_region_and_connect(world, "High Class Heist", "Prowling the Grounds -> High Class Heist", tot_hub)
    tot_4 = create_region_and_connect(world, "Fire Down Below", "Prowling the Grounds -> Fire Down Below", tot_hub)
    tot_5 = create_region_and_connect(world, "Cunning Disguise", "Prowling the Grounds -> Cunning Disguise", tot_hub)
    tot_hub_2 = create_region_and_connect(world, "Prowling the Grounds - Second Gate", "Prowling the Grounds -> Prowling the Grounds - Second Gate", tot_hub)
    tot_6 = create_region_and_connect(world, "Gunboat Graveyard", "Prowling the Grounds - Second Gate -> Gunboat Graveyard", tot_hub_2)
    tot_7 = create_region_and_connect(world, "Treasure in the Depths", "Prowling the Grounds - Second Gate -> Treasure in the Depths", tot_hub_2)
    tot_boss = create_region_and_connect(world, "Eye of the Storm", "Prowling the Grounds - Second Gate -> Eye of the Storm", tot_hub_2)
    tot_intro.connect(tot_hub, "Stealthy Approach -> Prowling the Grounds")

    # ------------------------------- Sunset Snake Eyes -------------------------------- #
    sse_intro = create_region_and_connect(world, "Rocky Start", "Hideout -> Rocky Start", hideout)
    sse_hub = create_region_and_connect(world, "Muggshot's Turf", "Hideout -> Muggshot's Turf", hideout)
    sse_2 = create_region_and_connect(world, "Boneyard Casino", "Muggshot's Turf -> Boneyard Casino", sse_hub)
    sse_3 = create_region_and_connect(world, "Murray's Big Gamble", "Muggshot's Turf -> Murray's Big Gamble", sse_hub)
    sse_4 = create_region_and_connect(world, "At the Dog Track", "Muggshot's Turf -> At the Dog Track", sse_hub)
    sse_hub_2 = create_region_and_connect(world, "Muggshot's Turf - Second Gate", "Muggshot's Turf -> Muggshot's Turf - Second Gate", sse_hub)
    sse_5 = create_region_and_connect(world, "Two to Tango", "Muggshot's Turf - Second Gate -> Two to Tango", sse_hub_2)
    sse_6 = create_region_and_connect(world, "Back Alley Heist", "Muggshot's Turf - Second Gate -> Back Alley Heist", sse_hub_2)
    sse_7 = create_region_and_connect(world, "Straight to the Top", "Muggshot's Turf - Second Gate -> Straight to the Top", sse_hub_2)
    sse_boss = create_region_and_connect(world, "Last Call", "Muggshot's Turf - Second Gate -> Last Call", sse_hub_2)
    sse_intro.connect(sse_hub, "Rocky Start -> Muggshot's Turf")

    # ------------------------------- Vicious Voodoo ----------------------------------- #
    vv_intro = create_region_and_connect(world, "Dread Swamp Path", "Hideout -> Dread Swamp Path", hideout)
    vv_hub = create_region_and_connect(world, "Swamp's Dark Center", "Hideout -> Swamp's Dark Center", hideout)
    vv_2 = create_region_and_connect(world, "Lair of the Beast", "Swamp's Dark Center -> Lair of the Beast", vv_hub)
    vv_3 = create_region_and_connect(world, "Grave Undertaking", "Swamp's Dark Center -> Grave Undertaking", vv_hub)
    vv_4 = create_region_and_connect(world, "Piranha Lake", "Swamp's Dark Center -> Piranha Lake", vv_hub)
    vv_hub_2 = create_region_and_connect(world, "Swamp's Dark Center - Second Gate", "Swamp's Dark Center -> Swamp's Dark Center - Second Gate", vv_hub)
    vv_5 = create_region_and_connect(world, "Descent into Danger", "Swamp's Dark Center - Second Gate -> Descent into Danger", vv_hub_2)
    vv_6 = create_region_and_connect(world, "Ghastly Voyage", "Swamp's Dark Center - Second Gate -> Ghastly Voyage", vv_hub_2)
    vv_7 = create_region_and_connect(world, "Down Home Cooking", "Swamp's Dark Center - Second Gate -> Down Home Cooking", vv_hub_2)
    vv_boss = create_region_and_connect(world, "Deadly Dance", "Swamp's Dark Center - Second Gate -> Deadly Dance", vv_hub_2)
    vv_intro.connect(vv_hub, "Dread Swamp Path -> Swamp's Dark Center")

    # ------------------------------- Fire in the Sky ---------------------------------- #
    fits_intro = create_region_and_connect(world, "Perilous Ascent", "Hideout -> Perilous Ascent", hideout)
    fits_hub = create_region_and_connect(world, "Inside the Stronghold", "Hideout -> Inside the Stronghold", hideout)
    fits_2 = create_region_and_connect(world, "Flaming Temple of Flame", "Inside the Stronghold -> Flaming Temple of Flame", fits_hub)
    fits_3 = create_region_and_connect(world, "Unseen Foe", "Inside the Stronghold -> Unseen Foe", fits_hub)
    fits_4 = create_region_and_connect(world, "King of the Hill", "Inside the Stronghold -> King of the Hill", fits_hub)
    fits_hub_2 = create_region_and_connect(world, "Inside the Stronghold - Second Gate", "Inside the Stronghold -> Inside the Stronghold - Second Gate", fits_hub)
    fits_5 = create_region_and_connect(world, "Rapid Fire Assault", "Inside the Stronghold - Second Gate -> Rapid Fire Assault", fits_hub_2)
    fits_6 = create_region_and_connect(world, "Desperate Race", "Inside the Stronghold - Second Gate -> Desperate Race", fits_hub_2)
    fits_7 = create_region_and_connect(world, "Duel by the Dragon", "Inside the Stronghold - Second Gate -> Duel by the Dragon", fits_hub_2)
    fits_boss = create_region_and_connect(world, "Flame Fu!", "Inside the Stronghold - Second Gate -> Flame Fu!", fits_hub_2)
    fits_intro.connect(fits_hub, "Perilous Ascent -> Inside the Stronghold")

    # ------------------------------- Finale ------------------------------------------ #
    choh = create_region_and_connect(world, "Cold Heart of Hate", "Hideout -> Cold Heart of Hate", hideout)

    # ------------------------------- Other ------------------------------------------- #
    tot_intro.connect(hideout, "ToT 1")
    tot_hub.connect(hideout, "ToT Hub")
    tot_2.connect(hideout, "ToT 2")
    tot_3.connect(hideout, "ToT 3")
    tot_4.connect(hideout, "ToT 4")
    tot_5.connect(hideout, "ToT 5")
    tot_hub_2.connect(hideout, "ToT Hub 2")
    tot_6.connect(hideout, "ToT 6")
    tot_7.connect(hideout, "ToT 7")
    tot_boss.connect(hideout, "ToT Boss")

    sse_intro.connect(hideout, "SSE Intro")
    sse_hub.connect(hideout, "SSE Hub")
    sse_2.connect(hideout, "SSE 2")
    sse_3.connect(hideout, "SSE 3")
    sse_4.connect(hideout, "SSE 4")
    sse_hub_2.connect(hideout, "SSE Hub 2")
    sse_5.connect(hideout, "SSE 5")
    sse_6.connect(hideout, "SSE 6")
    sse_7.connect(hideout, "SSE 7")
    sse_boss.connect(hideout, "SSE Boss")

    vv_intro.connect(hideout, "VV Intro")
    vv_hub.connect(hideout, "VV Hub")
    vv_2.connect(hideout, "VV 2")
    vv_3.connect(hideout, "VV 3")
    vv_4.connect(hideout, "VV 4")
    vv_hub_2.connect(hideout, "VV Hub 2")
    vv_5.connect(hideout, "VV 5")
    vv_6.connect(hideout, "VV 6")
    vv_7.connect(hideout, "VV 7")
    vv_boss.connect(hideout, "VV Boss")

    fits_intro.connect(hideout, "FitS Intro")
    fits_hub.connect(hideout, "FitS Hub")
    fits_2.connect(hideout, "FitS 2")
    fits_3.connect(hideout, "FitS 3")
    fits_4.connect(hideout, "FitS 4")
    fits_hub_2.connect(hideout, "FitS Hub 2")
    fits_5.connect(hideout, "FitS 5")
    fits_6.connect(hideout, "FitS 6")
    fits_7.connect(hideout, "FitS 7")
    fits_boss.connect(hideout, "FitS Boss")

    choh.connect(hideout, "CHoH")

def create_region(world: "Sly1World", name: str) -> Region:
    reg = Region(name, world.player, world.multiworld)

    for (key, data) in location_table.items():
        if data.region == name:
            location = Sly1Location(world.player, key, data.ap_code, reg)
            reg.locations.append(location)
    
    world.multiworld.regions.append(reg)
    return reg

def create_region_and_connect(world: "Sly1World",
                               name: str, entrancename: str, connected_region: Region) -> Region:
    reg: Region = create_region(world, name)
    connected_region.connect(reg, entrancename)
    return reg