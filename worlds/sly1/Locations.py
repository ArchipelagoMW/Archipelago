from .Types import LocData
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from . import Sly1World

def get_total_locations(world: "Sly1World") -> int:
    # Temporarily just counts the amount. This will be important when options come along.
    total = 0
    for _ in location_table:
        total += 1
    return total

def get_location_names() -> Dict[str, int]:
    names = {name: data.ap_code for name, data in location_table.items()}
    return names

sly_locations = {
    ## Key Locations - Finishing the level
    # Tides of Terror
    "Stealthy Approach Key": LocData(10020101, "Stealthy Approach"),
    "Into the Machine Key": LocData(10020102, "Prowling the Grounds"),
    "High Class Heist Key": LocData(10020103, "Prowling the Grounds"),
    "Fire Down Below Key": LocData(10020104, "Prowling the Grounds"),
    "Cunning Disguise Key": LocData(10020105, "Prowling the Grounds"),
    "Gunboat Graveyard Key": LocData(10020106, "Prowling the Grounds - Second Gate"),
    "Treasure in the Depths Key": LocData(10020107, "Prowling the Grounds - Second Gate"),

    # Sunset Snake Eyes
    "Rocky Start Key": LocData(10020108, "Rocky Start"),
    "At the Dog Track Key": LocData(10020109, "Muggshot's Turf"),
    "Murray's Big Gamble Key": LocData(10020110, "Muggshot's Turf"),
    "Boneyard Casino Key": LocData(10020111, "Muggshot's Turf"),
    "Straight to the Top Key": LocData(10020112, "Muggshot's Turf - Second Gate"),
    "Two to Tango Key": LocData(10020113, "Muggshot's Turf - Second Gate"),
    "Back Alley Heist Key": LocData(10020114, "Muggshot's Turf - Second Gate"),

    # Vicious Voodoo
    "Dread Swamp Path Key": LocData(10020115, "Dread Swamp Path"),
    "Lair of the Beast Key": LocData(10020116, "Swamp's Dark Center"),
    "Grave Undertaking Key": LocData(10020117, "Swamp's Dark Center"),
    "Piranha Lake Key": LocData(10020118, "Swamp's Dark Center"),
    "Descent into Danger Key": LocData(10020119, "Swamp's Dark Center - Second Gate"),
    "Ghastly Voyage Key": LocData(10020120, "Swamp's Dark Center - Second Gate"),
    "Down Home Cooking Key": LocData(10020121, "Swamp's Dark Center - Second Gate"),

    # Fire in the Sky
    "Perilous Ascent Key": LocData(10020122, "Perilous Ascent"),
    "Unseen Foe Key": LocData(10020123, "Inside the Stronghold"),
    "Flaming Temple of Flame Key": LocData(10020124, "Inside the Stronghold"),
    "King of the Hill Key": LocData(10020125, "Inside the Stronghold"),
    "Rapid Fire Assault Key": LocData(10020126, "Inside the Stronghold - Second Gate"),
    "Desperate Race Key": LocData(10020127, "Inside the Stronghold - Second Gate"),
    "Duel by the Dragon Key": LocData(10020128, "Inside the Stronghold - Second Gate"),


    ## Vault Locations - Collecting all bottles in level
    # Tides of Terror
    "Stealthy Approach Vault": LocData(10020201, "Stealthy Approach"),
    "Into the Machine Vault": LocData(10020202, "Prowling the Grounds"),
    "High Class Heist Vault": LocData(10020203, "Prowling the Grounds"),
    "Fire Down Below Vault": LocData(10020204, "Prowling the Grounds"),
    "Cunning Disguise Vault": LocData(10020205, "Prowling the Grounds"),
    "Gunboat Graveyard Vault": LocData(10020206, "Prowling the Grounds - Second Gate"),

    # Sunset Snake Eyes
    "Rocky Start Vault": LocData(10020208, "Rocky Start"),
    "Boneyard Casino Vault": LocData(10020211, "Muggshot's Turf"),
    "Straight to the Top Vault": LocData(10020212, "Muggshot's Turf - Second Gate"),
    "Two to Tango Vault": LocData(10020213, "Muggshot's Turf - Second Gate"),
    "Back Alley Heist Vault": LocData(10020214, "Muggshot's Turf - Second Gate"),

    # Vicious Voodoo
    "Dread Swamp Path Vault": LocData(10020215, "Dread Swamp Path"),
    "Lair of the Beast Vault": LocData(10020216, "Swamp's Dark Center"),
    "Grave Undertaking Vault": LocData(10020217, "Swamp's Dark Center"),
    "Descent into Danger Vault": LocData(10020219, "Swamp's Dark Center - Second Gate"),

    # Fire in the Sky
    "Perilous Ascent Vault": LocData(10020222, "Perilous Ascent"),
    "Unseen Foe Vault": LocData(10020223, "Inside the Stronghold"),
    "Flaming Temple of Flame Vault": LocData(10020224, "Inside the Stronghold"),
    "Duel by the Dragon Vault": LocData(10020228, "Inside the Stronghold - Second Gate"),


    ## Hourglass Locations - Speedrunning the level after beating boss
    # Tides of Terror
    "Stealthy Approach Hourglass": LocData(10020301, "Stealthy Approach"),
    "Into the Machine Hourglass": LocData(10020302, "Prowling the Grounds"),
    "High Class Heist Hourglass": LocData(10020303, "Prowling the Grounds"),
    "Fire Down Below Hourglass": LocData(10020304, "Prowling the Grounds"),
    "Cunning Disguise Hourglass": LocData(10020305, "Prowling the Grounds"),
    "Gunboat Graveyard Hourglass": LocData(10020306, "Prowling the Grounds - Second Gate"),

    # Sunset Snake Eyes
    "Rocky Start Hourglass": LocData(10020308, "Rocky Start"),
    "Boneyard Casino Hourglass": LocData(10020311, "Muggshot's Turf"),
    "Straight to the Top Hourglass": LocData(10020312, "Muggshot's Turf - Second Gate"),
    "Two to Tango Hourglass": LocData(10020313, "Muggshot's Turf - Second Gate"),
    "Back Alley Heist Hourglass": LocData(10020314, "Muggshot's Turf - Second Gate"),

    # Vicious Voodoo
    "Dread Swamp Path Hourglass": LocData(10020315, "Dread Swamp Path"),
    "Lair of the Beast Hourglass": LocData(10020316, "Swamp's Dark Center"),
    "Grave Undertaking Hourglass": LocData(10020317, "Swamp's Dark Center"),
    "Descent into Danger Hourglass": LocData(10020319, "Swamp's Dark Center - Second Gate"),

    # Fire in the Sky
    "Perilous Ascent Hourglass": LocData(10020322, "Perilous Ascent"),
    "Unseen Foe Hourglass": LocData(10020323, "Inside the Stronghold"),
    "Flaming Temple of Flame Hourglass": LocData(10020324, "Inside the Stronghold"),
    "Duel by the Dragon Hourglass": LocData(10020328, "Inside the Stronghold - Second Gate"),

    ## Boss Victories
    "Eye of the Storm": LocData(None, "Prowling the Grounds - Second Gate"),
    "Last Call": LocData(None, "Muggshot's Turf - Second Gate"),
    "Deadly Dance": LocData(None, "Swamp's Dark Center - Second Gate"),
    "Flame Fu!": LocData(None, "Inside the Stronghold - Second Gate"),
    "Cold Heart of Hate": LocData(None, "Cold Heart of Hate")
}

location_table = {
    **sly_locations
}