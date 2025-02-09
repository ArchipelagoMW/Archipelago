from .Types import LocData, EpisodeType, LevelData, Sly1Location
from typing import Dict, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from . import Sly1World

def did_include_hourglasses(world: "Sly1World") -> bool:
    return bool(world.options.IncludeHourglasses)

def hourglasses_roll(world: "Sly1World") -> bool:
    return bool(world.options.HourglassesRequireRoll)

def did_avoid_early_bk(world: "Sly1World") -> bool:
    return bool(world.options.AvoidEarlyBK)

def get_total_locations(world: "Sly1World") -> int:
    total = 0
    for name in location_table:
        if not did_include_hourglasses(world) and name in hourglass_locations:
            continue

        if location_table[name].level_type in world.options.ExcludeMinigames.value:
            continue

        if is_valid_location:
            total += 1
    
    if world.options.LocationCluesanityBundleSize.value > 0:
            for name in bottle_amounts.keys():
                bundle_amount = get_bundle_amount_for_level(name, world.options.LocationCluesanityBundleSize.value)
                
                total += bundle_amount

    for name, data in minigame_locations.items():
        if data.level_type in world.options.ExcludeMinigames.value:
            continue

        total += world.options.MinigameCaches.value

    return total

def get_location_names() -> Dict[str, int]:
    # There HAS to be a better way. I just dont know it since I can't pass the world in here so I can't check the options

    # For all possible bottle numbers, create location entries
    all_possible_bottle_locations = {}
    for name, data in bottle_amounts.items():
        for bottle_number in range(1, data.bottle_amount + 1):
            bottle_code = data.ap_code + (bottle_number - 1)
            bottle_location_name = f"{name} Bottle #{bottle_number}"
            all_possible_bottle_locations[bottle_location_name] = bottle_code

    # Add all the normal key minigame locations and all the cache options
    all_possible_minigame_locations = {}
    for name, data in minigame_locations.items():
        all_possible_minigame_locations[f"{name} Key"] = data.ap_code
        for cache_number in range(1, 11):
            cache_code = data.ap_code + (cache_number - 1)
            cache_location_name = f"{name} Cache #{cache_number}"
            all_possible_minigame_locations[cache_location_name] = cache_code

    names = {**{name: data.ap_code for name, data in location_table.items()}, **all_possible_bottle_locations, **all_possible_minigame_locations}

    return names

def is_valid_location(world: "Sly1World", name) -> bool:
    if not did_include_hourglasses(world) and name in hourglass_locations:
        return False
    
    if location_table[name].level_type in world.options.ExcludeMinigames.value:
        return False
    
    if world.options.LocationCluesanityBundleSize.value == 0 and 'Bottle' in name:
        return False
    
    return True

def get_bundle_amount_for_level(level_name: str, bundle_size: int) -> int:
    level_data = bottle_amounts[level_name]

    bundle_amount = int(level_data.bottle_amount/bundle_size)
    if level_data.bottle_amount%bundle_size != 0:
        bundle_amount += 1

    return bundle_amount

def generate_bottle_locations(world: "Sly1World", bundle_size: int) -> Dict[str, LocData]:
    for name, data in bottle_amounts.items():
        bundle_amount = get_bundle_amount_for_level(name, bundle_size)

        reg = world.multiworld.get_region(data.region, world.player)

        for x in range(1, bundle_amount + 1):
            bottle_number = bundle_size * x
            if bottle_number > data.bottle_amount:
                bottle_number = data.bottle_amount
            bottle_code = data.ap_code + (bottle_number - 1)
            # Delete every bottle so we can add only the ones that are valid
            bottle_name = f"{name} Bottle #{bottle_number}"
            if bottle_name in location_table:
                del location_table[bottle_name]

            location = Sly1Location(world.player, bottle_name, bottle_code, reg)
            reg.locations.append(location)

def generate_minigame_locations(world: "Sly1World", cache_size: int) -> Dict[str, LocData]:
    # If the cache size is one, add the word key and add it to the region
    # Otherwise, create however many caches are needed and add them to the region
    for name, data in minigame_locations.items():
        if data.level_type in world.options.ExcludeMinigames.value:
            continue

        reg = world.multiworld.get_region(data.region, world.player)

        if cache_size == 1:
            location_name = f"{name} Key"
            location = Sly1Location(world.player, location_name, data.ap_code, reg)
            reg.locations.append(location)
        else:
            for cache_number in range(1, cache_size + 1):
                location_name = f"{name} Cache #{cache_number}"
                cache_code = data.ap_code + cache_number - 1
                location = Sly1Location(world.player, location_name, cache_code, reg)
                reg.locations.append(location)
    
sly_locations = {
    "Paris Files": LocData(10020000, "Paris",),

    ## Key Locations - Finishing the level
    # Tide of Terror
    "Stealthy Approach Key": LocData(10020101, "Stealthy Approach", key_type=EpisodeType.TOT),
    "Into the Machine Key": LocData(10020102, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "High Class Heist Key": LocData(10020103, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Fire Down Below Key": LocData(10020104, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Cunning Disguise Key": LocData(10020105, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Gunboat Graveyard Key": LocData(10020106, "Prowling the Grounds - Second Gate", key_type=EpisodeType.TOT, key_requirement = 3),

    # Sunset Snake Eyes
    "Rocky Start Key": LocData(10020108, "Rocky Start", key_type=EpisodeType.SSE),
    "Boneyard Casino Key": LocData(10020111, "Muggshot's Turf", key_type=EpisodeType.SSE, key_requirement = 1),
    "Straight to the Top Key": LocData(10020112, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),
    "Two to Tango Key": LocData(10020113, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),
    "Back Alley Heist Key": LocData(10020114, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),

    # Vicious Voodoo
    "Dread Swamp Path Key": LocData(10020115, "Dread Swamp Path", key_type=EpisodeType.VV),
    "Lair of the Beast Key": LocData(10020116, "Swamp's Dark Center", key_type=EpisodeType.VV, key_requirement = 1),
    "Grave Undertaking Key": LocData(10020117, "Swamp's Dark Center", key_type=EpisodeType.VV, key_requirement = 1),
    "Descent into Danger Key": LocData(10020119, "Swamp's Dark Center - Second Gate", key_type=EpisodeType.VV, key_requirement = 3),

    # Fire in the Sky
    "Perilous Ascent Key": LocData(10020122, "Perilous Ascent", key_type=EpisodeType.FITS),
    "Unseen Foe Key": LocData(10020123, "Inside the Stronghold", key_type=EpisodeType.FITS, key_requirement = 1),
    "Flaming Temple of Flame Key": LocData(10020124, "Inside the Stronghold", key_type=EpisodeType.FITS, key_requirement = 1),
    "Duel by the Dragon Key": LocData(10020128, "Inside the Stronghold - Second Gate", key_type=EpisodeType.FITS, key_requirement = 3),

    ## Boss Victories
    "Eye of the Storm": LocData(10020229, "Eye of the Storm", key_type=EpisodeType.TOT, key_requirement = 7),
    "Last Call": LocData(10020230, "Last Call", key_type=EpisodeType.SSE, key_requirement = 7),
    "Deadly Dance": LocData(10020231, "Deadly Dance", key_type=EpisodeType.VV, key_requirement = 7),
    "Flame Fu!": LocData(10020232, "Flame Fu!", key_type=EpisodeType.FITS, key_requirement = 7),
}

hourglass_locations = {
    ## Hourglass Locations - Speedrunning the level
    # Tide of Terror
    "Stealthy Approach Hourglass": LocData(10020301, "Stealthy Approach", key_type=EpisodeType.TOT, key_requirement = 1),
    "Into the Machine Hourglass": LocData(10020302, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "High Class Heist Hourglass": LocData(10020303, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Fire Down Below Hourglass": LocData(10020304, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Cunning Disguise Hourglass": LocData(10020305, "Prowling the Grounds", key_type=EpisodeType.TOT, key_requirement = 1),
    "Gunboat Graveyard Hourglass": LocData(10020306, "Prowling the Grounds - Second Gate", key_type=EpisodeType.TOT, key_requirement = 3),

    # Sunset Snake Eyes
    "Rocky Start Hourglass": LocData(10020308, "Rocky Start", key_type=EpisodeType.SSE, key_requirement = 1),
    "Boneyard Casino Hourglass": LocData(10020311, "Muggshot's Turf", key_type=EpisodeType.SSE, key_requirement = 1),
    "Straight to the Top Hourglass": LocData(10020312, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),
    "Two to Tango Hourglass": LocData(10020313, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),
    "Back Alley Heist Hourglass": LocData(10020314, "Muggshot's Turf - Second Gate", key_type=EpisodeType.SSE, key_requirement = 3),

    # Vicious Voodoo
    "Dread Swamp Path Hourglass": LocData(10020315, "Dread Swamp Path", key_type=EpisodeType.VV, key_requirement = 1),
    "Lair of the Beast Hourglass": LocData(10020316, "Swamp's Dark Center", key_type=EpisodeType.VV, key_requirement = 1),
    "Grave Undertaking Hourglass": LocData(10020317, "Swamp's Dark Center", key_type=EpisodeType.VV, key_requirement = 1),
    "Descent into Danger Hourglass": LocData(10020319, "Swamp's Dark Center - Second Gate", key_type=EpisodeType.VV, key_requirement = 3),

    # Fire in the Sky
    "Perilous Ascent Hourglass": LocData(10020322, "Perilous Ascent", key_type=EpisodeType.FITS, key_requirement = 1),
    "Unseen Foe Hourglass": LocData(10020323, "Inside the Stronghold", key_type=EpisodeType.FITS, key_requirement = 1),
    "Flaming Temple of Flame Hourglass": LocData(10020324, "Inside the Stronghold", key_type=EpisodeType.FITS, key_requirement = 1),
    "Duel by the Dragon Hourglass": LocData(10020328, "Inside the Stronghold - Second Gate", key_type=EpisodeType.FITS, key_requirement = 3),
}

vault_locations = {
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
    "Duel by the Dragon Vault": LocData(10020228, "Inside the Stronghold - Second Gate", key_type=EpisodeType.FITS, key_requirement = 3)
}

minigame_locations = {
    "Treasure in the Depths": LocData(10021000, "Prowling the Grounds - Second Gate", key_type=EpisodeType.TOT, key_requirement = 3, level_type = "Crabs"),
    "At the Dog Track": LocData(10021100, "Muggshot's Turf", key_type=EpisodeType.SSE, key_requirement = 1, level_type = "Races"),
    "Murray's Big Gamble": LocData(10021200, "Muggshot's Turf", key_type=EpisodeType.SSE, key_requirement = 1, level_type = "Turrets"),
    "Piranha Lake": LocData(10021300, "Swamp's Dark Center", key_type=EpisodeType.VV, key_requirement = 1, level_type = "Swamp Skiff"),
    "Ghastly Voyage": LocData(10021400, "Swamp's Dark Center - Second Gate", key_type=EpisodeType.VV, key_requirement = 3, level_type = "Hover Blasters"),
    "Down Home Cooking": LocData(10021500, "Swamp's Dark Center - Second Gate", key_type=EpisodeType.VV, key_requirement = 3, level_type = "Chicken Killing"),
    "King of the Hill": LocData(10021600, "Inside the Stronghold", key_type=EpisodeType.FITS, key_requirement = 1, level_type = "Turrets"),
    "Rapid Fire Assault": LocData(10021700, "Inside the Stronghold - Second Gate", key_type=EpisodeType.FITS, key_requirement = 3, level_type = "Hover Blasters"),
    "Desperate Race": LocData(10021800, "Inside the Stronghold - Second Gate", key_type=EpisodeType.FITS, key_requirement = 3, level_type = "Races")
}

event_locations = {
    "Beat Raleigh": LocData(None, "Eye of the Storm", key_type=EpisodeType.TOT, key_requirement = 7),
    "Beat Muggshot": LocData(None, "Last Call", key_type=EpisodeType.SSE, key_requirement = 7),
    "Beat Mz. Ruby": LocData(None, "Deadly Dance", key_type=EpisodeType.VV, key_requirement = 7),
    "Beat Panda King": LocData(None, "Flame Fu!", key_type=EpisodeType.FITS, key_requirement = 7),
    "Beat Clockwerk": LocData(10020233, "Cold Heart of Hate", key_type=EpisodeType.CHOH)
}

bottle_amounts = {
    "Stealthy Approach":      LevelData(10020400, "Stealthy Approach", 20),
    "Into the Machine":         LevelData(10020420, "Into the Machine", 30),
    "High Class Heist":         LevelData(10020450, "High Class Heist", 30),
    "Fire Down Below":      LevelData(10020480, "Fire Down Below", 30),
    "Cunning Disguise":       LevelData(10020510, "Cunning Disguise", 30),
    "Gunboat Graveyard":    LevelData(10020540, "Gunboat Graveyard", 20),

    "Rocky Start":            LevelData(10020560, "Rocky Start", 40),
    "Boneyard Casino":          LevelData(10020600, "Boneyard Casino", 40),
    "Straight to the Top":      LevelData(10020640, "Straight to the Top", 40),
    "Two to Tango":             LevelData(10020680, "Two to Tango", 30),
    "Back Alley Heist":         LevelData(10020710, "Back Alley Heist", 30),

    "Dread Swamp Path":     LevelData(10020740, "Dread Swamp Path", 20),
    "Lair of the Beast":    LevelData(10020760, "Lair of the Beast", 30),
    "Grave Undertaking":      LevelData(10020790, "Grave Undertaking", 40),
    "Descent into Danger":      LevelData(10020830, "Descent into Danger", 40),

    "Perilous Ascent":        LevelData(10020870, "Perilous Ascent", 30),
    "Flaming Temple of Flame":  LevelData(10020930, "Flaming Temple of Flame", 25),
    "Unseen Foe":           LevelData(10020900, "Unseen Foe", 30),
    "Duel by the Dragon":       LevelData(10020955, "Duel by the Dragon", 40)
}

location_table = {
    **sly_locations,
    **vault_locations,
    **hourglass_locations,
    **event_locations,
}