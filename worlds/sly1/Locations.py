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
    "Stealthy Approach Key": LocData(10020101, "Tides of Terror"),
    "Into the Machine Key": LocData(10020102, "Tides of Terror", key_requirement=1),
    "High Class Heist Key": LocData(10020103, "Tides of Terror", key_requirement=1),
    "Fire Down Below Key": LocData(10020104, "Tides of Terror", key_requirement=1),
    "Cunning Disguise Key": LocData(10020105, "Tides of Terror", key_requirement=1),
    "Gunboat Graveyard Key": LocData(10020106, "Tides of Terror", key_requirement=3),
    "Treasure in the Depths Key": LocData(10020107, "Tides of Terror", key_requirement=3),

    # Sunset Snake Eyes
    "Rocky Start Key": LocData(10020108, "Sunset Snake Eyes"),
    "At the Dog Track Key": LocData(10020109, "Sunset Snake Eyes", key_requirement=1),
    "Murray's Big Gamble Key": LocData(10020110, "Sunset Snake Eyes", key_requirement=1),
    "Boneyard Casino Key": LocData(10020111, "Sunset Snake Eyes", key_requirement=1),
    "Straight to the Top Key": LocData(10020112, "Sunset Snake Eyes", key_requirement=3),
    "Two to Tango Key": LocData(10020113, "Sunset Snake Eyes", key_requirement=3),
    "Back Alley Heist Key": LocData(10020114, "Sunset Snake Eyes", key_requirement=3),

    # Vicious Voodoo
    "Dread Swamp Path Key": LocData(10020115, "Vicious Voodoo"),
    "Lair of the Beast Key": LocData(10020116, "Vicious Voodoo", key_requirement=1),
    "Grave Undertaking Key": LocData(10020117, "Vicious Voodoo", key_requirement=1),
    "Piranha Lake Key": LocData(10020118, "Vicious Voodoo", key_requirement=1),
    "Descent into Danger Key": LocData(10020119, "Vicious Voodoo", key_requirement=3),
    "Ghastly Voyage Key": LocData(10020120, "Vicious Voodoo", key_requirement=3),
    "Down Home Cooking Key": LocData(10020121, "Vicious Voodoo", key_requirement=3),

    # Fire in the Sky
    "Perilous Ascent Key": LocData(10020122, "Fire in the Sky"),
    "Unseen Foe Key": LocData(10020123, "Fire in the Sky", key_requirement=1),
    "Flaming Temple of Flame Key": LocData(10020124, "Fire in the Sky", key_requirement=1),
    "King of the Hill Key": LocData(10020125, "Fire in the Sky", key_requirement=1),
    "Rapid Fire Assault Key": LocData(10020126, "Fire in the Sky", key_requirement=3),
    "Desperate Race Key": LocData(10020127, "Fire in the Sky", key_requirement=3),
    "Duel by the Dragon Key": LocData(10020128, "Fire in the Sky", key_requirement=3),


    ## Vault Locations - Collecting all bottles in level
    # Tides of Terror
    "Stealthy Approach Vault": LocData(10020201, "Tides of Terror"),
    "Into the Machine Vault": LocData(10020202, "Tides of Terror", key_requirement=1),
    "High Class Heist Vault": LocData(10020203, "Tides of Terror", key_requirement=1),
    "Fire Down Below Vault": LocData(10020204, "Tides of Terror", key_requirement=1),
    "Cunning Disguise Vault": LocData(10020205, "Tides of Terror", key_requirement=1),
    "Gunboat Graveyard Vault": LocData(10020206, "Tides of Terror", key_requirement=3),

    # Sunset Snake Eyes
    "Rocky Start Vault": LocData(10020208, "Sunset Snake Eyes"),
    "Boneyard Casino Vault": LocData(10020211, "Sunset Snake Eyes", key_requirement=1),
    "Straight to the Top Vault": LocData(10020212, "Sunset Snake Eyes", key_requirement=3),
    "Two to Tango Vault": LocData(10020213, "Sunset Snake Eyes", key_requirement=3),
    "Back Alley Heist Vault": LocData(10020214, "Sunset Snake Eyes", key_requirement=3),

    # Vicious Voodoo
    "Dread Swamp Path Vault": LocData(10020215, "Vicious Voodoo"),
    "Lair of the Beast Vault": LocData(10020216, "Vicious Voodoo", key_requirement=1),
    "Grave Undertaking Vault": LocData(10020217, "Vicious Voodoo", key_requirement=1),
    "Descent into Danger Vault": LocData(10020219, "Vicious Voodoo", key_requirement=3),

    # Fire in the Sky
    "Perilous Ascent Vault": LocData(10020222, "Fire in the Sky"),
    "Unseen Foe Vault": LocData(10020223, "Fire in the Sky", key_requirement=1),
    "Flaming Temple of Flame Vault": LocData(10020224, "Fire in the Sky", key_requirement=1),
    "Duel by the Dragon Vault": LocData(10020228, "Fire in the Sky", key_requirement=3),


    ## Hourglass Locations - Speedrunning the level after beating boss
    # Tides of Terror
    "Stealthy Approach Hourglass": LocData(10020301, "Tides of Terror", key_requirement=7),
    "Into the Machine Hourglass": LocData(10020302, "Tides of Terror", key_requirement=7),
    "High Class Heist Hourglass": LocData(10020303, "Tides of Terror", key_requirement=7),
    "Fire Down Below Hourglass": LocData(10020304, "Tides of Terror", key_requirement=7),
    "Cunning Disguise Hourglass": LocData(10020305, "Tides of Terror", key_requirement=7),
    "Gunboat Graveyard Hourglass": LocData(10020306, "Tides of Terror", key_requirement=7),

    # Sunset Snake Eyes
    "Rocky Start Hourglass": LocData(10020308, "Sunset Snake Eyes", key_requirement=7),
    "Boneyard Casino Hourglass": LocData(10020311, "Sunset Snake Eyes", key_requirement=7),
    "Straight to the Top Hourglass": LocData(10020312, "Sunset Snake Eyes", key_requirement=7),
    "Two to Tango Hourglass": LocData(10020313, "Sunset Snake Eyes", key_requirement=7),
    "Back Alley Heist Hourglass": LocData(10020314, "Sunset Snake Eyes", key_requirement=7),

    # Vicious Voodoo
    "Dread Swamp Path Hourglass": LocData(10020315, "Vicious Voodoo", key_requirement=7),
    "Lair of the Beast Hourglass": LocData(10020316, "Vicious Voodoo", key_requirement=7),
    "Grave Undertaking Hourglass": LocData(10020317, "Vicious Voodoo", key_requirement=7),
    "Descent into Danger Hourglass": LocData(10020319, "Vicious Voodoo", key_requirement=7),

    # Fire in the Sky
    "Perilous Ascent Hourglass": LocData(10020322, "Fire in the Sky", key_requirement=7),
    "Unseen Foe Hourglass": LocData(10020323, "Fire in the Sky", key_requirement=7),
    "Flaming Temple of Flame Hourglass": LocData(10020324, "Fire in the Sky", key_requirement=7),
    "Duel by the Dragon Hourglass": LocData(10020328, "Fire in the Sky", key_requirement=7)
}

location_table = {
    **sly_locations
}