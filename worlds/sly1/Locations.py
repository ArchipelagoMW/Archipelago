from .Types import LocData
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from . import Sly1World

def get_total_locations(world: "Sly1World") -> int:
    # Temporarily just counts the amount. This will be important when options come along.
    total = 0
    for name in location_table.keys():
        total += 1
    return total

def get_location_names() -> Dict[str, int]:
    names = {name: data.ap_code for name, data in location_table.items()}
    return names

sly_locations = {
    ## Key Locations - Finishing the level
    # Tides of Terror
    "Stealthy Approach Key": LocData(100020101, "Tides of Terror"),
    "Into the Machine Key": LocData(100020102, "Tides of Terror", key_requirement=1),
    "High Class Heist Key": LocData(100020103, "Tides of Terror", key_requirement=1),
    "Fire Down Below Key": LocData(100020104, "Tides of Terror", key_requirement=1),
    "Cunning Disguise Key": LocData(100020105, "Tides of Terror", key_requirement=1),
    "Gunboat Graveyard Key": LocData(100020106, "Tides of Terror", key_requirement=3),
    "Treasure in the Depths Key": LocData(100020107, "Tides of Terror", key_requirement=3),

    # Sunset Snake Eyes
    "Rocky Start Key": LocData(100020108, "Sunset Snake Eyes"),
    "At the Dog Track Key": LocData(100020109, "Sunset Snake Eyes", key_requirement=1),
    "Murray's Big Gamble Key": LocData(100020110, "Sunset Snake Eyes", key_requirement=1),
    "Boneyard Casino Key": LocData(100020111, "Sunset Snake Eyes", key_requirement=1),
    "Straight to the Top Key": LocData(100020112, "Sunset Snake Eyes", key_requirement=3),
    "Two to Tango Key": LocData(100020113, "Sunset Snake Eyes", key_requirement=3),
    "Back Alley Heist Key": LocData(100020114, "Sunset Snake Eyes", key_requirement=3),

    # Vicious Voodoo
    "Dread Swamp Path Key": LocData(100020115, "Vicious Voodoo"),
    "Lair of the Beast Key": LocData(100020116, "Vicious Voodoo", key_requirement=1),
    "Grave Undertaking Key": LocData(100020117, "Vicious Voodoo", key_requirement=1),
    "Piranha Lake Key": LocData(100020118, "Vicious Voodoo", key_requirement=1),
    "Descent into Danger Key": LocData(100020119, "Vicious Voodoo", key_requirement=3),
    "Ghastly Voyage Key": LocData(100020120, "Vicious Voodoo", key_requirement=3),
    "Down Home Cooking Key": LocData(100020121, "Vicious Voodoo", key_requirement=3),

    # Fire in the Sky
    "Perilous Ascent Key": LocData(100020122, "Fire in the Sky"),
    "Unseen Foe Key": LocData(100020123, "Fire in the Sky", key_requirement=1),
    "Flaming Temple of Flame Key": LocData(100020124, "Fire in the Sky", key_requirement=1),
    "King of the Hill Key": LocData(100020125, "Fire in the Sky", key_requirement=1),
    "Rapid Fire Assault Key": LocData(100020126, "Fire in the Sky", key_requirement=3),
    "Desperate Race Key": LocData(100020127, "Fire in the Sky", key_requirement=3),
    "Duel by the Dragon Key": LocData(100020128, "Fire in the Sky", key_requirement=3),


    ## Vault Locations - Collecting all bottles in level
    # Tides of Terror
    "Stealthy Approach Vault": LocData(100020201, "Tides of Terror"),
    "Into the Machine Vault": LocData(100020202, "Tides of Terror", key_requirement=1),
    "High Class Heist Vault": LocData(100020203, "Tides of Terror", key_requirement=1),
    "Fire Down Below Vault": LocData(100020204, "Tides of Terror", key_requirement=1),
    "Cunning Disguise Vault": LocData(100020205, "Tides of Terror", key_requirement=1),
    "Gunboat Graveyard Vault": LocData(100020206, "Tides of Terror", key_requirement=3),

    # Sunset Snake Eyes
    "Rocky Start Vault": LocData(100020208, "Sunset Snake Eyes"),
    "Boneyard Casino Vault": LocData(100020211, "Sunset Snake Eyes", key_requirement=1),
    "Straight to the Top Vault": LocData(100020212, "Sunset Snake Eyes", key_requirement=3),
    "Two to Tango Vault": LocData(100020213, "Sunset Snake Eyes", key_requirement=3),
    "Back Alley Heist Vault": LocData(100020214, "Sunset Snake Eyes", key_requirement=3),

    # Vicious Voodoo
    "Dread Swamp Path Vault": LocData(100020215, "Vicious Voodoo"),
    "Lair of the Beast Vault": LocData(100020216, "Vicious Voodoo", key_requirement=1),
    "Grave Undertaking Vault": LocData(100020217, "Vicious Voodoo", key_requirement=1),
    "Descent into Danger Vault": LocData(100020219, "Vicious Voodoo", key_requirement=3),

    # Fire in the Sky
    "Perilous Ascent Vault": LocData(100020222, "Fire in the Sky"),
    "Unseen Foe Vault": LocData(100020223, "Fire in the Sky", key_requirement=1),
    "Flaming Temple of Flame Vault": LocData(100020224, "Fire in the Sky", key_requirement=1),
    "Duel by the Dragon Vault": LocData(100020228, "Fire in the Sky", key_requirement=3),


    ## Hourglass Locations - Speedrunning the level after beating boss
    # Tides of Terror
    "Stealthy Approach Vault": LocData(100020301, "Tides of Terror", key_requirement=7),
    "Into the Machine Vault": LocData(100020302, "Tides of Terror", key_requirement=7),
    "High Class Heist Vault": LocData(100020303, "Tides of Terror", key_requirement=7),
    "Fire Down Below Vault": LocData(100020304, "Tides of Terror", key_requirement=7),
    "Cunning Disguise Vault": LocData(100020305, "Tides of Terror", key_requirement=7),
    "Gunboat Graveyard Vault": LocData(100020306, "Tides of Terror", key_requirement=7),

    # Sunset Snake Eyes
    "Rocky Start Vault": LocData(100020308, "Sunset Snake Eyes", key_requirement=7),
    "Boneyard Casino Vault": LocData(100020311, "Sunset Snake Eyes", key_requirement=7),
    "Straight to the Top Vault": LocData(100020312, "Sunset Snake Eyes", key_requirement=7),
    "Two to Tango Vault": LocData(100020313, "Sunset Snake Eyes", key_requirement=7),
    "Back Alley Heist Vault": LocData(100020314, "Sunset Snake Eyes", key_requirement=7),

    # Vicious Voodoo
    "Dread Swamp Path Vault": LocData(100020315, "Vicious Voodoo", key_requirement=7),
    "Lair of the Beast Vault": LocData(100020316, "Vicious Voodoo", key_requirement=7),
    "Grave Undertaking Vault": LocData(100020317, "Vicious Voodoo", key_requirement=7),
    "Descent into Danger Vault": LocData(100020319, "Vicious Voodoo", key_requirement=7),

    # Fire in the Sky
    "Perilous Ascent Vault": LocData(100020322, "Fire in the Sky", key_requirement=7),
    "Unseen Foe Vault": LocData(100020323, "Fire in the Sky", key_requirement=7),
    "Flaming Temple of Flame Vault": LocData(100020324, "Fire in the Sky", key_requirement=7),
    "Duel by the Dragon Vault": LocData(100020328, "Fire in the Sky", key_requirement=7)
}

location_table = {
    **sly_locations
}