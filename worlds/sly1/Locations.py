from .Types import LocData, EpisodeType
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from . import Sly1World

def did_include_hourglasses(world: "Sly1World") -> bool:
    return bool(world.options.IncludeHourglasses)

def get_total_locations(world: "Sly1World") -> int:
    total = 0
    for name in location_table:
        if not did_include_hourglasses(world) and name in hourglass_locations:
            continue

        if is_valid_location:
            total += 1

    return total

def get_location_names() -> Dict[str, int]:
    names = {name: data.ap_code for name, data in location_table.items()}
    return names

def is_valid_location(world: "Sly1World",name) -> bool:
    if not did_include_hourglasses(world) and name in hourglass_locations:
        return False
    
    return True

sly_locations = {
    ## Key Locations - Finishing the level
    # Tide of Terror
    "Stealthy Approach Key": LocData(10020101, "Stealthy Approach", key_type=EpisodeType.TOT),
    "Into the Machine Key": LocData(10020102, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "High Class Heist Key": LocData(10020103, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Fire Down Below Key": LocData(10020104, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Cunning Disguise Key": LocData(10020105, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Gunboat Graveyard Key": LocData(10020106, "Prowling the Grounds - Second Gate", key_type=EpisodeType.TOT, key_requirement = 3),
    "Treasure in the Depths Key": LocData(10020107, "Prowling the Grounds - Second Gate", key_type=EpisodeType.TOT, key_requirement = 3),

    # Sunset Snake Eyes
    "Rocky Start Key": LocData(10020108, "Rocky Start", key_type=EpisodeType.SSE),
    "At the Dog Track Key": LocData(10020109, "Muggshot's Turf", key_type=EpisodeType.SSE, key_requirement = 1),
    "Murray's Big Gamble Key": LocData(10020110, "Muggshot's Turf", key_type=EpisodeType.SSE, key_requirement = 1),
    "Boneyard Casino Key": LocData(10020111, "Muggshot's Turf", key_type=EpisodeType.SSE, key_requirement = 1),
    "Straight to the Top Key": LocData(10020112, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),
    "Two to Tango Key": LocData(10020113, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),
    "Back Alley Heist Key": LocData(10020114, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),

    # Vicious Voodoo
    "Dread Swamp Path Key": LocData(10020115, "Dread Swamp Path", key_type=EpisodeType.VV),
    "Lair of the Beast Key": LocData(10020116, "Swamp's Dark Center", key_type=EpisodeType.VV, key_requirement = 1),
    "Grave Undertaking Key": LocData(10020117, "Swamp's Dark Center", key_type=EpisodeType.VV, key_requirement = 1),
    "Piranha Lake Key": LocData(10020118, "Swamp's Dark Center", key_type=EpisodeType.VV, key_requirement = 1),
    "Descent into Danger Key": LocData(10020119, "Swamp's Dark Center - Second Gate", key_type=EpisodeType.VV, key_requirement = 3),
    "Ghastly Voyage Key": LocData(10020120, "Swamp's Dark Center - Second Gate", key_type=EpisodeType.VV, key_requirement = 3),
    "Down Home Cooking Key": LocData(10020121, "Swamp's Dark Center - Second Gate", key_type=EpisodeType.VV, key_requirement = 3),

    # Fire in the Sky
    "Perilous Ascent Key": LocData(10020122, "Perilous Ascent", key_type=EpisodeType.FITS),
    "Unseen Foe Key": LocData(10020123, "Inside the Stronghold", key_type=EpisodeType.FITS, key_requirement = 1),
    "Flaming Temple of Flame Key": LocData(10020124, "Inside the Stronghold", key_type=EpisodeType.FITS, key_requirement = 1),
    "King of the Hill Key": LocData(10020125, "Inside the Stronghold", key_type=EpisodeType.FITS, key_requirement = 1),
    "Rapid Fire Assault Key": LocData(10020126, "Inside the Stronghold - Second Gate", key_type=EpisodeType.FITS, key_requirement = 3),
    "Desperate Race Key": LocData(10020127, "Inside the Stronghold - Second Gate", key_type=EpisodeType.FITS, key_requirement = 3),
    "Duel by the Dragon Key": LocData(10020128, "Inside the Stronghold - Second Gate", key_type=EpisodeType.FITS, key_requirement = 3),


    ## Vault Locations - Collecting all bottles in level
    # Tide of Terror
    "Stealthy Approach Vault": LocData(10020201, "Stealthy Approach", key_type=EpisodeType.TOT),
    "Into the Machine Vault": LocData(10020202, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "High Class Heist Vault": LocData(10020203, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Fire Down Below Vault": LocData(10020204, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Cunning Disguise Vault": LocData(10020205, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Gunboat Graveyard Vault": LocData(10020206, "Prowling the Grounds - Second Gate", key_type=EpisodeType.TOT, key_requirement = 3),

    # Sunset Snake Eyes
    "Rocky Start Vault": LocData(10020208, "Rocky Start", key_type=EpisodeType.SSE),
    "Boneyard Casino Vault": LocData(10020211, "Muggshot's Turf", key_type=EpisodeType.SSE, key_requirement = 1),
    "Straight to the Top Vault": LocData(10020212, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),
    "Two to Tango Vault": LocData(10020213, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),
    "Back Alley Heist Vault": LocData(10020214, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),

    # Vicious Voodoo
    "Dread Swamp Path Vault": LocData(10020215, "Dread Swamp Path", key_type=EpisodeType.VV),
    "Lair of the Beast Vault": LocData(10020216, "Swamp's Dark Center", key_type=EpisodeType.VV, key_requirement = 1),
    "Grave Undertaking Vault": LocData(10020217, "Swamp's Dark Center", key_type=EpisodeType.VV, key_requirement = 1),
    "Descent into Danger Vault": LocData(10020219, "Swamp's Dark Center - Second Gate", key_type=EpisodeType.VV, key_requirement = 3),

    # Fire in the Sky
    "Perilous Ascent Vault": LocData(10020222, "Perilous Ascent", key_type=EpisodeType.FITS),
    "Unseen Foe Vault": LocData(10020223, "Inside the Stronghold", key_type=EpisodeType.FITS, key_requirement = 1),
    "Flaming Temple of Flame Vault": LocData(10020224, "Inside the Stronghold", key_type=EpisodeType.FITS, key_requirement = 1),
    "Duel by the Dragon Vault": LocData(10020228, "Inside the Stronghold - Second Gate", key_type=EpisodeType.FITS, key_requirement = 3),


    ## Boss Victories
    "Beat Raleigh": LocData(None, "Eye of the Storm", key_type=EpisodeType.TOT, key_requirement = 7),
    "Beat Muggshot": LocData(None, "Last Call", key_type=EpisodeType.SSE, key_requirement = 7),
    "Beat Mz Ruby": LocData(None, "Deadly Dance", key_type=EpisodeType.VV, key_requirement = 7),
    "Beat Panda King": LocData(None, "Flame Fu!", key_type=EpisodeType.FITS, key_requirement = 7),
    "Beat Clockwerk": LocData(None, "Cold Heart of Hate", key_type=EpisodeType.CHOH)
}

hourglass_locations = {
    ## Hourglass Locations - Speedrunning the level
    # Tide of Terror
    "Stealthy Approach Hourglass": LocData(10020301, "Stealthy Approach"),
    "Into the Machine Hourglass": LocData(10020302, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "High Class Heist Hourglass": LocData(10020303, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Fire Down Below Hourglass": LocData(10020304, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Cunning Disguise Hourglass": LocData(10020305, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Gunboat Graveyard Hourglass": LocData(10020306, "Prowling the Grounds - Second Gate", key_type=EpisodeType.TOT, key_requirement = 3),

    # Sunset Snake Eyes
    "Rocky Start Hourglass": LocData(10020308, "Rocky Start"),
    "Boneyard Casino Hourglass": LocData(10020311, "Muggshot's Turf", key_type=EpisodeType.SSE, key_requirement = 1),
    "Straight to the Top Hourglass": LocData(10020312, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),
    "Two to Tango Hourglass": LocData(10020313, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),
    "Back Alley Heist Hourglass": LocData(10020314, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),

    # Vicious Voodoo
    "Dread Swamp Path Hourglass": LocData(10020315, "Dread Swamp Path"),
    "Lair of the Beast Hourglass": LocData(10020316, "Swamp's Dark Center", key_type=EpisodeType.VV, key_requirement = 1),
    "Grave Undertaking Hourglass": LocData(10020317, "Swamp's Dark Center", key_type=EpisodeType.VV, key_requirement = 1),
    "Descent into Danger Hourglass": LocData(10020319, "Swamp's Dark Center - Second Gate", key_type=EpisodeType.VV, key_requirement = 3),

    # Fire in the Sky
    "Perilous Ascent Hourglass": LocData(10020322, "Perilous Ascent"),
    "Unseen Foe Hourglass": LocData(10020323, "Inside the Stronghold", key_type=EpisodeType.FITS, key_requirement = 1),
    "Flaming Temple of Flame Hourglass": LocData(10020324, "Inside the Stronghold", key_type=EpisodeType.FITS, key_requirement = 1),
    "Duel by the Dragon Hourglass": LocData(10020328, "Inside the Stronghold - Second Gate", key_type=EpisodeType.FITS, key_requirement = 3),
}

event_locations = {
    "Eye of the Storm": LocData(None, "Eye of the Storm", key_type=EpisodeType.TOT, key_requirement = 7),
    "Last Call": LocData(None, "Last Call", key_type=EpisodeType.SSE, key_requirement = 7),
    "Deadly Dance": LocData(None, "Deadly Dance", key_type=EpisodeType.VV, key_requirement = 7),
    "Flame Fu!": LocData(None, "Flame Fu!", key_type=EpisodeType.FITS, key_requirement = 7),
    "Cold Heart of Hate": LocData(None, "Cold Heart of Hate", key_type=EpisodeType.CHOH)
}

location_table = {
    **sly_locations,
    **hourglass_locations,
    **event_locations
}