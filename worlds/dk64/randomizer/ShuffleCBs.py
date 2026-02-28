"""Select CB Location selection."""

import js
import randomizer.CollectibleLogicFiles.AngryAztec
import randomizer.CollectibleLogicFiles.CreepyCastle
import randomizer.CollectibleLogicFiles.CrystalCaves
import randomizer.CollectibleLogicFiles.FranticFactory
import randomizer.CollectibleLogicFiles.FungiForest
import randomizer.CollectibleLogicFiles.GloomyGalleon
import randomizer.CollectibleLogicFiles.JungleJapes
import randomizer.Fill as Fill
import randomizer.Lists.CBLocations.AngryAztecCBLocations
import randomizer.Lists.CBLocations.CreepyCastleCBLocations
import randomizer.Lists.CBLocations.CrystalCavesCBLocations
import randomizer.Lists.CBLocations.FranticFactoryCBLocations
import randomizer.Lists.CBLocations.FungiForestCBLocations
import randomizer.Lists.CBLocations.GloomyGalleonCBLocations
import randomizer.Lists.CBLocations.JungleJapesCBLocations
import randomizer.Lists.CBLocations.DKIslesCBLocations
import randomizer.Lists.Exceptions as Ex
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Collectibles import Collectibles
from randomizer.LogicClasses import Collectible
from randomizer.Patching.Library.Generic import IsItemSelected
from randomizer.Lists.MapsAndExits import RegionMapList, LevelMapTable

level_data = {
    Levels.JungleJapes: {
        "cb": randomizer.Lists.CBLocations.JungleJapesCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.JungleJapesCBLocations.BalloonList,
        "vanilla": randomizer.CollectibleLogicFiles.JungleJapes.LogicRegions,
    },
    Levels.AngryAztec: {
        "cb": randomizer.Lists.CBLocations.AngryAztecCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.AngryAztecCBLocations.BalloonList,
        "vanilla": randomizer.CollectibleLogicFiles.AngryAztec.LogicRegions,
    },
    Levels.FranticFactory: {
        "cb": randomizer.Lists.CBLocations.FranticFactoryCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.FranticFactoryCBLocations.BalloonList,
        "vanilla": randomizer.CollectibleLogicFiles.FranticFactory.LogicRegions,
    },
    Levels.GloomyGalleon: {
        "cb": randomizer.Lists.CBLocations.GloomyGalleonCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.GloomyGalleonCBLocations.BalloonList,
        "vanilla": randomizer.CollectibleLogicFiles.GloomyGalleon.LogicRegions,
    },
    Levels.FungiForest: {
        "cb": randomizer.Lists.CBLocations.FungiForestCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.FungiForestCBLocations.BalloonList,
        "vanilla": randomizer.CollectibleLogicFiles.FungiForest.LogicRegions,
    },
    Levels.CrystalCaves: {
        "cb": randomizer.Lists.CBLocations.CrystalCavesCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.CrystalCavesCBLocations.BalloonList,
        "vanilla": randomizer.CollectibleLogicFiles.CrystalCaves.LogicRegions,
    },
    Levels.CreepyCastle: {
        "cb": randomizer.Lists.CBLocations.CreepyCastleCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.CreepyCastleCBLocations.BalloonList,
        "vanilla": randomizer.CollectibleLogicFiles.CreepyCastle.LogicRegions,
    },
    Levels.DKIsles: {
        "cb": randomizer.Lists.CBLocations.DKIslesCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.DKIslesCBLocations.BalloonList,
        "vanilla": None,
    },
}


def ShuffleCBs(spoiler):
    """Shuffle CBs selected from location files."""
    retries = 0
    levels_to_populate = 7
    MAX_BALLOONS = 105
    MAX_SINGLES = 780  # 793 Singles in Vanilla, under-representing this to help with the calculation formula
    MAX_BUNCHES = 790 - MAX_BALLOONS * 2 - round(MAX_SINGLES / 5)  # 334 bunches in vanilla, biasing this for now to help with calculation formula
    PLACEMENT_LIMIT = 1127
    add_isles_cbs = IsItemSelected(spoiler.settings.cb_rando_enabled, spoiler.settings.cb_rando_list_selected, Levels.DKIsles)
    if add_isles_cbs:
        levels_to_populate = 8
        INCREASE_FACTOR = 8 / 7
        MAX_SINGLES = int(MAX_SINGLES * INCREASE_FACTOR)
        MAX_BUNCHES = int(MAX_BUNCHES * INCREASE_FACTOR)
        PLACEMENT_LIMIT = 1400
    # Calculate how many CBs to remove from the total based off what levels aren't placed
    levels_to_place = []
    for level in level_data:
        is_level_placed = IsItemSelected(spoiler.settings.cb_rando_enabled, spoiler.settings.cb_rando_list_selected, level)
        if is_level_placed:
            # Level is placed, no need to remove CBs
            levels_to_place.append(level)
            continue
        if level == Levels.DKIsles:
            # Isles has no CBs in vanilla, don't place
            continue
        vanilla_regions = level_data[level]["vanilla"]
        singles_in_vanilla = 0
        bunches_in_vanilla = 0
        balloon_in_vanilla = 0
        for region, region_items in vanilla_regions.items():
            for item in region_items:
                if item.type == Collectibles.balloon:
                    balloon_in_vanilla += 1
                elif item.type == Collectibles.bunch:
                    bunches_in_vanilla += 1
                elif item.type == Collectibles.banana:
                    singles_in_vanilla += 1
        MAX_BALLOONS -= balloon_in_vanilla
        MAX_SINGLES -= singles_in_vanilla
        MAX_BUNCHES -= bunches_in_vanilla
        PLACEMENT_LIMIT -= singles_in_vanilla + bunches_in_vanilla + balloon_in_vanilla
        levels_to_populate -= 1

    while True:
        try:
            total_balloons = 0
            total_singles = 0
            total_bunches = 0
            cb_data = []
            # First, remove all placed colored bananas
            for region_id in spoiler.CollectibleRegions.keys():
                map_id = RegionMapList[region_id]
                level_id = None
                for lvl, map_ids in LevelMapTable.items():
                    if map_id in map_ids:
                        level_id = lvl
                if level_id is None:
                    raise Exception(f"Invalid Level ID for {map_id} in region {region_id}")
                if level_id in levels_to_place:
                    spoiler.CollectibleRegions[region_id] = [
                        collectible for collectible in spoiler.CollectibleRegions[region_id] if collectible.type not in [Collectibles.balloon, Collectibles.bunch, Collectibles.banana]
                    ]
            for level_index, level in enumerate(levels_to_place):
                if (not add_isles_cbs) and level == Levels.DKIsles:
                    continue
                level_placement = []
                global_divisor = (levels_to_populate - 1) - level_index
                kong_specific_left = {
                    Kongs.donkey: 100,
                    Kongs.diddy: 100,
                    Kongs.lanky: 100,
                    Kongs.tiny: 100,
                    Kongs.chunky: 100,
                }
                # Balloons
                # Pick random amount of balloons assigned to level
                balloons_left = MAX_BALLOONS - total_balloons
                balloon_lower = max(
                    int(balloons_left / (levels_to_populate - level_index)) - 3, 0
                )  # Select lower bound for randomization as max between 0, and balloons left distributed amongst the remaining levels minus 3
                if global_divisor == 0:
                    # Last Level
                    balloon_upper = balloons_left
                else:
                    balloon_upper = min(int(balloons_left / (levels_to_populate - level_index)) + 3, int(balloons_left / global_divisor))
                if level == Levels.FranticFactory:
                    # Fill Factory with more balloons to mitigate OM2 overpopulation
                    balloon_upper = int(balloon_upper * 1.5)
                    balloon_lower = int(balloon_lower * 1.5)
                balloon_lst = level_data[level]["balloons"].copy()
                selected_balloon_count = min(
                    spoiler.settings.random.randint(min(balloon_lower, balloon_upper), max(balloon_lower, balloon_upper)),
                    len(balloon_lst),
                )
                # selected_balloon_count = 22 # Test all balloon locations
                spoiler.settings.random.shuffle(balloon_lst)  # TODO: Maybe make this more advanced?
                # selects all balloons
                placed_balloons = 0
                for balloon in balloon_lst:
                    if placed_balloons < selected_balloon_count:
                        balloon_kongs = balloon.kongs.copy()
                        for kong in kong_specific_left:
                            if kong_specific_left[kong] < 10 and kong in balloon_kongs:  # Not enough Colored Bananas to place a balloon:
                                balloon_kongs.remove(kong)  # Remove kong from permitted list
                        if len(balloon_kongs) > 0:  # Has a kong who can be assigned to this balloon
                            selected_kong = spoiler.settings.random.choice(balloon_kongs)
                            kong_specific_left[selected_kong] -= 10  # Remove CBs for Balloon
                            level_placement.append(
                                {
                                    "id": balloon.id,
                                    "name": balloon.name,
                                    "kong": selected_kong,
                                    "level": level,
                                    "type": "balloons",
                                    "map": balloon.map,
                                }
                            )
                            placed_balloons += 1
                            if balloon.region not in spoiler.CollectibleRegions:
                                spoiler.CollectibleRegions[balloon.region] = []
                            spoiler.CollectibleRegions[balloon.region].append(Collectible(Collectibles.balloon, selected_kong, balloon.logic, None, 1, name=balloon.name))
                # Model Two CBs
                bunches_left = MAX_BUNCHES - total_bunches
                singles_left = MAX_SINGLES - total_singles
                bunches_lower = max(int(bunches_left / (levels_to_populate - level_index)) - 5, 0)
                singles_lower = max(int(singles_left / (levels_to_populate - level_index)) - 10, 0)
                if global_divisor == 0:
                    bunches_upper = bunches_left
                    singles_upper = min(
                        singles_left,
                        int((5 * (PLACEMENT_LIMIT - total_bunches - total_singles) - sum(kong_specific_left)) / 4),
                    )  # Places a hard cap of PLACEMENT_LIMIT total singles+bunches
                else:
                    bunches_upper = min(int(bunches_left / (levels_to_populate - level_index)) + 15, int(bunches_left / global_divisor))
                    singles_upper = min(int(singles_left / (levels_to_populate - level_index)) + 10, int(singles_left / global_divisor))
                groupIds = list(range(1, len(level_data[level]["cb"]) + 1))
                spoiler.settings.random.shuffle(groupIds)
                selected_bunch_count = spoiler.settings.random.randint(min(bunches_lower, bunches_upper), max(bunches_lower, bunches_upper))
                selected_single_count = spoiler.settings.random.randint(min(singles_lower, singles_upper), max(singles_lower, singles_upper))
                placed_bunches = 0
                placed_singles = 0
                for groupId in groupIds:
                    group_weight = 0
                    bunches_in_group = 0
                    singles_in_group = 0
                    colored_banana_groups = [group for group in level_data[level]["cb"] if group.group == groupId]
                    cb_kongs = list(kong_specific_left.keys())
                    for group in colored_banana_groups:
                        cb_kongs = list(set(cb_kongs) & set(group.kongs.copy()))
                        for loc in group.locations:
                            group_weight += loc[0]
                            bunches_in_group += int(loc[0] == 5)
                            singles_in_group += int(loc[0] == 1)
                    for kong in kong_specific_left:
                        if kong in cb_kongs:
                            # If this kong doesn't have space for this group, remove it. Also if this kong is close to cap, don't use this kong unless it's the last one.
                            if kong_specific_left[kong] < group_weight or (len(cb_kongs) > 1 and kong_specific_left[kong] <= 10 and (kong_specific_left[kong] - group_weight) > 0):
                                cb_kongs.remove(kong)
                    if len(cb_kongs) > 0 and selected_single_count >= placed_singles + singles_in_group and selected_bunch_count >= placed_bunches + bunches_in_group:
                        selected_kong = spoiler.settings.random.choice(cb_kongs)
                        kong_specific_left[selected_kong] -= group_weight  # Remove CBs for kong
                        # When a kong hits 0 remaining in this level, we no longer need to consider it
                        if kong_specific_left[selected_kong] == 0:
                            del kong_specific_left[selected_kong]
                        for group in colored_banana_groups:
                            # Calculate the number of bananas we have to place by lesser group so different bananas in the same group can have different logic
                            bunches_in_lesser_group = 0
                            singles_in_lesser_group = 0
                            for loc in group.locations:
                                bunches_in_lesser_group += int(loc[0] == 5)
                                singles_in_lesser_group += int(loc[0] == 1)
                            if group.region not in spoiler.CollectibleRegions:
                                spoiler.CollectibleRegions[group.region] = []
                            if bunches_in_lesser_group > 0:
                                spoiler.CollectibleRegions[group.region].append(
                                    Collectible(
                                        Collectibles.bunch,
                                        selected_kong,
                                        group.logic,
                                        None,
                                        bunches_in_lesser_group,
                                        name=group.name,
                                    )
                                )
                            if singles_in_lesser_group > 0:
                                spoiler.CollectibleRegions[group.region].append(
                                    Collectible(
                                        Collectibles.banana,
                                        selected_kong,
                                        group.logic,
                                        None,
                                        singles_in_lesser_group,
                                        name=group.name,
                                    )
                                )
                            level_placement.append(
                                {
                                    "group": group.group,
                                    "name": group.name,
                                    "kong": selected_kong,
                                    "level": level,
                                    "type": "cb",
                                    "map": group.map,
                                    "locations": group.locations,
                                }
                            )
                        placed_bunches += bunches_in_group
                        placed_singles += singles_in_group
                    # If all kongs have 0 unplaced, we're done here
                    if len(kong_specific_left.keys()) == 0:
                        break

                # Placement is valid
                total_balloons += placed_balloons
                total_bunches += placed_bunches
                total_singles += placed_singles
                cb_data.extend(level_placement.copy())
                for x in kong_specific_left:
                    if kong_specific_left[x] > 0:
                        print(f"WARNING: {kong_specific_left[x]} bananas unassigned for {x.name} in {level.name}")
                        raise Ex.CBFillFailureException
                    elif kong_specific_left[x] < 0:
                        print(f"WARNING: {-kong_specific_left[x]} too many bananas assigned for {x.name} in {level.name}")
                        raise Ex.CBFillFailureException
            if total_bunches + total_singles > PLACEMENT_LIMIT:
                print(f"WARNING: {total_bunches + total_singles} banana objects placed, exceeding cap of {PLACEMENT_LIMIT}")
                raise Ex.CBFillFailureException
            spoiler.Reset()
            if not Fill.VerifyWorld(spoiler):
                raise Ex.CBFillFailureException
            spoiler.cb_placements = cb_data
            return
        except Ex.CBFillFailureException:
            if retries >= 10:
                js.postMessage("CB Randomizer failed to fill. REPORT THIS TO THE DEVS!!")
                raise Ex.CBFillFailureException
            retries += 1
            js.postMessage("CB Randomizer failed to fill. Tries: " + str(retries))
