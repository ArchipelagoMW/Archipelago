"""Shuffle Dirt Patch Locations."""

import randomizer.LogicFiles.AngryAztec
import randomizer.LogicFiles.CreepyCastle
import randomizer.LogicFiles.CrystalCaves
import randomizer.LogicFiles.DKIsles
import randomizer.LogicFiles.FranticFactory
import randomizer.LogicFiles.FungiForest
import randomizer.LogicFiles.GloomyGalleon
import randomizer.LogicFiles.JungleJapes
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Lists.CustomLocations import CustomLocation, CustomLocations, LocationTypes
from randomizer.LogicClasses import LocationLogic


def addPatch(spoiler, patch: CustomLocation, enum_val: int, name: str, level: Levels):
    """Add patch to relevant Logic Region."""
    level_to_name = {
        Levels.DKIsles: "Isles",
        Levels.JungleJapes: "Japes",
        Levels.AngryAztec: "Aztec",
        Levels.FranticFactory: "Factory",
        Levels.GloomyGalleon: "Galleon",
        Levels.FungiForest: "Forest",
        Levels.CrystalCaves: "Caves",
        Levels.CreepyCastle: "Castle",
    }
    spoiler.RegionList[patch.logic_region].locations.append(LocationLogic(enum_val, patch.logic))
    spoiler.LocationList[enum_val].name = f"{level_to_name[level]} Dirt: {name}"
    spoiler.LocationList[enum_val].default_mapid_data[0].map = patch.map
    spoiler.LocationList[enum_val].level = level


def removePatches(spoiler):
    """Remove all patches from Logic regions."""
    level_logic_regions = [
        randomizer.LogicFiles.DKIsles.LogicRegions,
        randomizer.LogicFiles.JungleJapes.LogicRegions,
        randomizer.LogicFiles.AngryAztec.LogicRegions,
        randomizer.LogicFiles.FranticFactory.LogicRegions,
        randomizer.LogicFiles.GloomyGalleon.LogicRegions,
        randomizer.LogicFiles.FungiForest.LogicRegions,
        randomizer.LogicFiles.CrystalCaves.LogicRegions,
        randomizer.LogicFiles.CreepyCastle.LogicRegions,
    ]
    for level in level_logic_regions:
        for region in level:
            region_data = spoiler.RegionList[region]
            region_data.locations = [x for x in region_data.locations if x.id < Locations.RainbowCoin_Location00 or x.id > Locations.RainbowCoin_Location15]


def fillPlandoDict(plando_dict: dict, plando_input):
    """Fill the plando_dict variable, using input from the plandomizer_dict."""
    for patch in plando_input:
        if patch["level"] != -1:
            plando_dict[patch["level"]].append(patch["location"])


def getPlandoDirtDistribution(random, plando_dict: dict):
    """Adapt the dirt patch balance to the user's plandomizer input."""
    distribution = []
    for level in plando_dict.keys():
        distribution.append(len(plando_dict[level]))
    running_total = sum(distribution)
    if running_total < 16:
        # Make sure as many levels as possible have 1+ dirt patch
        for level in range(len(distribution)):
            if distribution[level] < 1:
                distribution[level] += 1
                running_total += 1
                if running_total >= 16:
                    break
    # Make sure the amount of levels with 2+ dirt patches is as close to 6 (including Isles) as possible
    if running_total < 16:
        level_priority = [0]
        random_levels = list(range(1, 8))
        random.shuffle(random_levels)
        level_priority.extend(random_levels)
        amount_of_levels = 6
        for level in range(len(distribution)):
            if distribution[level_priority[level]] < 2:
                distribution[level_priority[level]] += 1
                running_total += 1
                amount_of_levels -= 1
                if running_total >= 16 or amount_of_levels <= 0:
                    break
    # Give the rest to DK Isles
    if running_total < 16:
        distribution[0] += 16 - running_total
    return distribution


def ShufflePatches(spoiler, human_spoiler):
    """Shuffle Dirt Patch Locations."""
    removePatches(spoiler)
    spoiler.dirt_patch_placement = []
    total_dirt_patch_list = {
        Levels.DKIsles: [],
        Levels.JungleJapes: [],
        Levels.AngryAztec: [],
        Levels.FranticFactory: [],
        Levels.GloomyGalleon: [],
        Levels.FungiForest: [],
        Levels.CrystalCaves: [],
        Levels.CreepyCastle: [],
    }
    for key in total_dirt_patch_list:
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
    }
    if spoiler.settings.enable_plandomizer and spoiler.settings.plandomizer_dict["plando_dirt_patches"] != []:
        fillPlandoDict(plando_dict, spoiler.settings.plandomizer_dict["plando_dirt_patches"])

    for key in total_dirt_patch_list.keys():
        for SingleDirtPatchLocation in CustomLocations[key]:
            if SingleDirtPatchLocation.is_fungi_hidden_patch or SingleDirtPatchLocation.isValidLocation(LocationTypes.DirtPatch):
                SingleDirtPatchLocation.setCustomLocation(False)
                if not spoiler.settings.enable_plandomizer or (SingleDirtPatchLocation.name not in spoiler.settings.plandomizer_dict["reserved_custom_locations"][key]):
                    total_dirt_patch_list[key].append(SingleDirtPatchLocation)

    # Make sure plandomized Dirt Patches are handled first
    if spoiler.settings.enable_plandomizer and spoiler.settings.plandomizer_dict["plando_dirt_patches"] != []:
        distribution = getPlandoDirtDistribution(spoiler.settings.random, plando_dict)
        count = 0
        for level in plando_dict.keys():
            area_dirt = total_dirt_patch_list[level]
            select_random_dirt_from_area(area_dirt, distribution[count], level, spoiler, human_spoiler, plando_dict)
            del total_dirt_patch_list[level]
            count += 1
    else:
        select_random_dirt_from_area(total_dirt_patch_list[Levels.DKIsles], 4, Levels.DKIsles, spoiler, human_spoiler, plando_dict)
        del total_dirt_patch_list[Levels.DKIsles]

        for SingleDirtPatchLocation in range(5):
            area_key = spoiler.settings.random.choice(list(total_dirt_patch_list.keys()))
            area_dirt = total_dirt_patch_list[area_key]
            select_random_dirt_from_area(area_dirt, 2, area_key, spoiler, human_spoiler, plando_dict)
            del total_dirt_patch_list[area_key]

        for area_key in total_dirt_patch_list.keys():
            area_dirt = total_dirt_patch_list[area_key]
            select_random_dirt_from_area(area_dirt, 1, area_key, spoiler, human_spoiler, plando_dict)

    # Create the locations for dirt patches
    sorted_patches = spoiler.dirt_patch_placement.copy()
    sorted_patches = sorted(sorted_patches, key=lambda d: d["score"])
    for patch_index, patch in enumerate(sorted_patches):
        patch["enum"] = Locations.RainbowCoin_Location00 + patch_index
        addPatch(spoiler, patch["patch"], patch["enum"], patch["name"], patch["level"])
        patch["patch"] = None
    # Resolve location-item combinations for plando
    if spoiler.settings.enable_plandomizer and spoiler.settings.plandomizer_dict["plando_dirt_patches"] != []:
        for item_placement in spoiler.settings.plandomizer_dict["plando_dirt_patches"]:
            for patch_index, patch in enumerate(sorted_patches):
                if item_placement["location"] == patch["name"] and item_placement["level"] == patch["level"] and item_placement["reward"] != -1:
                    spoiler.settings.plandomizer_dict["locations"][patch["enum"]] = item_placement["reward"]
    return human_spoiler.copy()


def select_random_dirt_from_area(area_dirt, amount, level, spoiler, human_spoiler, plando_input):
    """Select <amount> random dirt patches from <area_dirt>, which is a list of dirt patches. Makes sure max 1 dirt patch per group is selected."""
    human_spoiler[level.name] = []
    for iterations in range(amount):
        allow_same_group_dirt = False
        selected_patch = spoiler.settings.random.choice(area_dirt)  # selects a random patch from the list
        selected_patch_name = selected_patch.name
        # Give plandomizer an opportunity to get the final say
        if spoiler.settings.enable_plandomizer and spoiler.settings.plandomizer_dict["plando_dirt_patches"] != []:
            if len(plando_input[level]) > 1:
                allow_same_group_dirt = True
            if len(plando_input[level]) > iterations:
                selected_patch_name = plando_input[level][iterations]
        for patch in CustomLocations[level]:  # enables the selected patch
            if patch.name == selected_patch_name:
                patch.setCustomLocation(True)
                human_spoiler[level.name].append(patch.name)
                local_map_index = len([x for x in spoiler.dirt_patch_placement if x["map"] == patch.map])
                spoiler.dirt_patch_placement.append(
                    {
                        "name": patch.name,
                        "map": patch.map,
                        "patch": patch,
                        "level": level,
                        "score": (patch.map * 100) + local_map_index,
                    }
                )
                area_dirt.remove(selected_patch)
                break
        if amount > 1 and not allow_same_group_dirt:  # if multiple patches are picked, remove patches from the same group, prevent them from being picked
            area_dirt = [dirt for dirt in area_dirt if dirt.group != selected_patch.group]
