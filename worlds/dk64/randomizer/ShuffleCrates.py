"""Shuffle Melon Crate Locations."""

import randomizer.LogicFiles.AngryAztec
import randomizer.LogicFiles.CreepyCastle
import randomizer.LogicFiles.CrystalCaves
import randomizer.LogicFiles.DKIsles
import randomizer.LogicFiles.FranticFactory
import randomizer.LogicFiles.FungiForest
import randomizer.LogicFiles.GloomyGalleon
import randomizer.LogicFiles.HideoutHelm
import randomizer.LogicFiles.JungleJapes
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Lists.CustomLocations import CustomLocation, CustomLocations, LocationTypes
from randomizer.LogicClasses import LocationLogic


def addCrate(spoiler, MelonCrate: CustomLocation, enum_val: int, name: str, level: Levels):
    """Add crate to relevant Logic Region."""
    level_to_name = {
        Levels.DKIsles: "Isles",
        Levels.JungleJapes: "Japes",
        Levels.AngryAztec: "Aztec",
        Levels.FranticFactory: "Factory",
        Levels.GloomyGalleon: "Galleon",
        Levels.FungiForest: "Forest",
        Levels.CrystalCaves: "Caves",
        Levels.CreepyCastle: "Castle",
        Levels.HideoutHelm: "Helm",
    }
    spoiler.RegionList[MelonCrate.logic_region].locations.append(LocationLogic(enum_val, MelonCrate.logic))
    spoiler.LocationList[enum_val].name = f"{level_to_name[level]} Melon Crate: {name}"
    spoiler.LocationList[enum_val].default_mapid_data[0].map = MelonCrate.map
    spoiler.LocationList[enum_val].level = level


def removeMelonCrate(spoiler):
    """Remove all crates from Logic regions."""
    level_logic_regions = [
        randomizer.LogicFiles.DKIsles.LogicRegions,
        randomizer.LogicFiles.JungleJapes.LogicRegions,
        randomizer.LogicFiles.AngryAztec.LogicRegions,
        randomizer.LogicFiles.FranticFactory.LogicRegions,
        randomizer.LogicFiles.GloomyGalleon.LogicRegions,
        randomizer.LogicFiles.FungiForest.LogicRegions,
        randomizer.LogicFiles.CrystalCaves.LogicRegions,
        randomizer.LogicFiles.CreepyCastle.LogicRegions,
        randomizer.LogicFiles.HideoutHelm.LogicRegions,
    ]
    for level in level_logic_regions:
        for region in level:
            region_data = spoiler.RegionList[region]
            region_data.locations = [x for x in region_data.locations if x.id < Locations.MelonCrate_Location00 or x.id > Locations.MelonCrate_Location12]


def fillPlandoDict(plando_dict: dict, plando_input):
    """Fill the plando_dict variable, using input from the plandomizer_dict."""
    for crate in plando_input:
        if crate["level"] != -1:
            plando_dict[crate["level"]].append(crate["location"])


def getPlandoCrateDistribution(random, plando_dict: dict):
    """Adapt the melon crate balance to the user's plandomizer input."""
    distribution = []
    for level in plando_dict.keys():
        distribution.append(len(plando_dict[level]))
    running_total = sum(distribution)
    if running_total < 13:
        # Make sure as many levels as possible have 1+ melon crate
        for level in range(len(distribution)):
            if distribution[level] < 1:
                distribution[level] += 1
                running_total += 1
                if running_total >= 13:
                    break
    if running_total < 13:
        # Make sure as many levels as possible have 2 melon crates
        level_priority = list(range(0, 9))
        random.shuffle(level_priority)
        amount_of_levels = 4
        for level in range(len(distribution)):
            if distribution[level_priority[level]] < 2:
                distribution[level_priority[level]] += 1
                running_total += 1
                amount_of_levels -= 1
                if running_total >= 13 or amount_of_levels <= 0:
                    break
    return distribution


def ShuffleMelonCrates(spoiler, human_spoiler):
    """Shuffle Melon Crate Locations."""
    removeMelonCrate(spoiler)
    spoiler.meloncrate_placement = []
    total_MelonCrate_list = {
        Levels.DKIsles: [],
        Levels.JungleJapes: [],
        Levels.AngryAztec: [],
        Levels.FranticFactory: [],
        Levels.GloomyGalleon: [],
        Levels.FungiForest: [],
        Levels.CrystalCaves: [],
        Levels.CreepyCastle: [],
        Levels.HideoutHelm: [],
    }
    for key in total_MelonCrate_list:
        human_spoiler[key.name] = []  # Ensure order

    plando_dict = {
        Levels.DKIsles: [],
        Levels.JungleJapes: [],
        Levels.AngryAztec: [],
        Levels.FranticFactory: [],
        Levels.GloomyGalleon: [],
        Levels.FungiForest: [],
        Levels.CrystalCaves: [],
        Levels.CreepyCastle: [],
        Levels.HideoutHelm: [],
    }
    if spoiler.settings.enable_plandomizer and spoiler.settings.plandomizer_dict["plando_melon_crates"] != []:
        fillPlandoDict(plando_dict, spoiler.settings.plandomizer_dict["plando_melon_crates"])

    for key in total_MelonCrate_list.keys():
        for SingleMelonCrateLocation in CustomLocations[key]:
            if SingleMelonCrateLocation.is_galleon_floating_crate or SingleMelonCrateLocation.isValidLocation(LocationTypes.MelonCrate):
                SingleMelonCrateLocation.setCustomLocation(False)
                if not spoiler.settings.enable_plandomizer or (SingleMelonCrateLocation.name not in spoiler.settings.plandomizer_dict["reserved_custom_locations"][key]):
                    total_MelonCrate_list[key].append(SingleMelonCrateLocation)

    # Make sure levels with multiple Melon Crates plandomized are handled first, before the shuffler runs out of dual levels
    if spoiler.settings.enable_plandomizer and spoiler.settings.plandomizer_dict["plando_melon_crates"] != []:
        distribution = getPlandoCrateDistribution(spoiler.settings.random, plando_dict)
        count = 0
        for level in plando_dict:
            area_meloncrate = total_MelonCrate_list[level]
            select_random_meloncrate_from_area(area_meloncrate, distribution[count], level, spoiler, human_spoiler, plando_dict)
            del total_MelonCrate_list[level]
            count += 1
    else:
        for SingleMelonCrateLocation in range(4):
            area_key = spoiler.settings.random.choice(list(total_MelonCrate_list.keys()))
            area_meloncrate = total_MelonCrate_list[area_key]
            select_random_meloncrate_from_area(area_meloncrate, 2, area_key, spoiler, human_spoiler, plando_dict)
            del total_MelonCrate_list[area_key]

        for area_key in total_MelonCrate_list.keys():
            area_meloncrate = total_MelonCrate_list[area_key]
            select_random_meloncrate_from_area(area_meloncrate, 1, area_key, spoiler, human_spoiler, plando_dict)

    # Create the locations for the melon crates
    sorted_MelonCrates = spoiler.meloncrate_placement.copy()
    sorted_MelonCrates = sorted(sorted_MelonCrates, key=lambda d: d["score"])
    for MelonCrate_index, MelonCrate in enumerate(sorted_MelonCrates):
        MelonCrate["enum"] = Locations.MelonCrate_Location00 + MelonCrate_index
        addCrate(spoiler, MelonCrate["MelonCrate"], MelonCrate["enum"], MelonCrate["name"], MelonCrate["level"])
        MelonCrate["MelonCrate"] = None
    # Resolve location-item combinations for plando
    if spoiler.settings.enable_plandomizer and spoiler.settings.plandomizer_dict["plando_melon_crates"] != []:
        for item_placement in spoiler.settings.plandomizer_dict["plando_melon_crates"]:
            for MelonCrate_index, MelonCrate in enumerate(sorted_MelonCrates):
                if item_placement["location"] == MelonCrate["name"] and item_placement["level"] == MelonCrate["level"] and item_placement["reward"] != -1:
                    spoiler.settings.plandomizer_dict["locations"][MelonCrate["enum"]] = item_placement["reward"]
    return human_spoiler.copy()


def select_random_meloncrate_from_area(area_meloncrate, amount, level, spoiler, human_spoiler, plando_input):
    """Select <amount> random melon crates from <area_meloncrate>, which is a list of melon crates. Makes sure max 1 melon crate per group is selected."""
    human_spoiler[level.name] = []
    for iterations in range(amount):
        allow_same_group_crate = False
        selected_crate = spoiler.settings.random.choice(area_meloncrate)  # selects a random crate from the list
        selected_crate_name = selected_crate.name
        # Give plandomizer an opportunity to get the final say
        if spoiler.settings.enable_plandomizer and spoiler.settings.plandomizer_dict["plando_melon_crates"] != []:
            if len(plando_input[level]) > 1:
                allow_same_group_crate = True
            if len(plando_input[level]) > iterations:
                selected_crate_name = plando_input[level][iterations]
        for meloncrate in CustomLocations[level]:  # enables the selected crate
            if meloncrate.name == selected_crate_name:
                meloncrate.setCustomLocation(True)
                human_spoiler[level.name].append(meloncrate.name)
                local_map_index = len([x for x in spoiler.meloncrate_placement if x["map"] == meloncrate.map])
                spoiler.meloncrate_placement.append(
                    {
                        "name": meloncrate.name,
                        "map": meloncrate.map,
                        "MelonCrate": meloncrate,
                        "level": level,
                        "score": (meloncrate.map * 100) + local_map_index,
                    },
                )
                area_meloncrate.remove(selected_crate)
                break
        if amount > 1 and not allow_same_group_crate:  # if multiple crates are picked, remove crates from the same group, prevent them from being picked
            area_meloncrate = [crate for crate in area_meloncrate if crate.group != selected_crate.group]
