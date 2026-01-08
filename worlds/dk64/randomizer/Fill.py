"""Module used to distribute items randomly."""

from __future__ import annotations

from math import ceil
from typing import TYPE_CHECKING, Any, List, Optional, Set, Tuple, Union
from functools import lru_cache

import js
import randomizer.ItemPool as ItemPool
import randomizer.Lists.Exceptions as Ex
import randomizer.ShuffleExits as ShuffleExits
from randomizer.CompileHints import compileHints, compileMicrohints, compileSpoilerHints, getDoorRestrictionsForItem
from randomizer.Enums.Events import Events
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import GetKongs, Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.HintRegion import HintRegion
from randomizer.Enums.SearchMode import SearchMode
from randomizer.Enums.Settings import (
    ActivateAllBananaports,
    BananaportRando,
    CBRando,
    ClimbingStatus,
    DamageAmount,
    DKPortalRando,
    FasterChecksSelected,
    FillAlgorithm,
    FungiTimeSetting,
    HardModeSelected,
    HelmBonuses,
    LogicType,
    MinigameBarrels,
    MoveRando,
    ProgressiveHintItem,
    RandomPrices,
    RemovedBarriersSelected,
    ShockwaveStatus,
    ShuffleLoadingZones,
    ShufflePortLocations,
    SpoilerHints,
    TrainingBarrels,
    WinConditionComplex,
    WrinklyHints,
)
from randomizer.Enums.Time import Time
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Types import Types, BarrierItems
from randomizer.Lists.CustomLocations import resetCustomLocations
from randomizer.Enums.Maps import Maps
from randomizer.Lists.Item import ItemList
from randomizer.Lists.Location import SharedMoveLocations, SharedShopLocations
from randomizer.Lists.Minigame import BarrelMetaData, MinigameRequirements
from randomizer.Lists.ShufflableExit import GetLevelShuffledToIndex
from randomizer.LogicClasses import Sphere, TransitionFront
from randomizer.Patching import ApplyRandomizer
from randomizer.Patching.EnemyRando import randomize_enemies_0
from randomizer.Patching.Library.Generic import IsItemSelected
from randomizer.Prices import GetMaxForKong
from randomizer.Settings import Settings
from randomizer.ShuffleBarrels import BarrelShuffle
from randomizer.ShuffleBosses import CorrectBossKongLocations, ShuffleBossesBasedOnOwnedItems
from randomizer.ShuffleCBs import ShuffleCBs
from randomizer.ShuffleCoins import ShuffleCoins
from randomizer.ShuffleCrates import ShuffleMelonCrates
from randomizer.ShuffleCrowns import ShuffleCrowns
from randomizer.ShuffleDoors import SetProgressiveHintDoorLogic, ShuffleDoors, ShuffleVanillaDoors, UpdateDoorLevels
from randomizer.ShuffleFairies import ShuffleFairyLocations
from randomizer.ShuffleItems import ShuffleItems
from randomizer.ShuffleKasplats import (
    ResetShuffledKasplatLocations,
    ShuffleKasplatsAndLocations,
    ShuffleKasplatsInVanillaLocations,
    constants,
    shufflable,
)
from randomizer.ShufflePatches import ShufflePatches
from randomizer.ShufflePorts import ShufflePorts, ResetPorts
from randomizer.ShuffleShopLocations import ShuffleShopLocations
from randomizer.ShuffleWarps import LinkWarps, ShuffleWarpsCrossMap

if TYPE_CHECKING:
    from randomizer.LogicClasses import LogicVarHolder, Region
    from randomizer.Spoiler import Spoiler


def KasplatShuffle(spoiler: Spoiler, LogicVariables: LogicVarHolder) -> None:
    """Facilitate the shuffling of kasplat types."""
    # If these were ever set at any prior point (likely only relevant running locally) then reset them - the upcoming methods will handle this TODO: maybe do this on other shufflers
    for location in shufflable:
        spoiler.LocationList[location].inaccessible = False
    for location in constants:
        spoiler.LocationList[location].inaccessible = False
    if spoiler.settings.kasplat_rando:
        retries = 0
        while True:
            try:
                # Clear any existing logic
                ResetShuffledKasplatLocations(spoiler)
                # Shuffle kasplats
                if spoiler.settings.kasplat_location_rando:
                    ShuffleKasplatsAndLocations(spoiler, LogicVariables)
                else:
                    ShuffleKasplatsInVanillaLocations(spoiler, LogicVariables)
                # Verify world by assuring all locations are still reachable
                spoiler.Reset()
                if not VerifyWorld(spoiler):
                    if retries < 10:
                        raise Ex.KasplatPlacementException
                    else:
                        # This is the first VerifyWorld check, and serves as the canary in the coal mine
                        # If we get to this point in the code, the world itself is likely unstable from some combination of settings or bugs
                        js.postMessage("Not all locations reached.")
                        ResetShuffledKasplatLocations(spoiler)
                        raise Ex.LocationsFailureException("Unexpected failure to reach all locations - report this to the devs!")
                return
            except Ex.KasplatPlacementException:
                retries += 1
                js.postMessage("Kasplat placement failed. Retrying. Tries: " + str(retries))


# @lru_cache(maxsize=None) - Cache is disabled for now, as it's causing issues with certain bits of logic in LZR
def GetExitLevelExit(level, restart) -> Optional[Transitions]:
    """Get the exit that using the "Exit Level" button will take you to."""
    # If you have option to restart, means there is no Exit Level option
    if restart is not None:
        return None
    # Otherwise identify and return the exit that the "Exit Level" button will take you to
    if level == Levels.JungleJapes:
        return ShuffleExits.ShufflableExits[Transitions.JapesToIsles].shuffledId
    elif level == Levels.AngryAztec:
        return ShuffleExits.ShufflableExits[Transitions.AztecToIsles].shuffledId
    elif level == Levels.FranticFactory:
        return ShuffleExits.ShufflableExits[Transitions.FactoryToIsles].shuffledId
    elif level == Levels.GloomyGalleon:
        return ShuffleExits.ShufflableExits[Transitions.GalleonToIsles].shuffledId
    elif level == Levels.FungiForest:
        return ShuffleExits.ShufflableExits[Transitions.ForestToIsles].shuffledId
    elif level == Levels.CrystalCaves:
        return ShuffleExits.ShufflableExits[Transitions.CavesToIsles].shuffledId
    elif level == Levels.CreepyCastle:
        return ShuffleExits.ShufflableExits[Transitions.CastleToIsles].shuffledId


@lru_cache(maxsize=None)
def GetLobbyOfRegion(level):
    """Get the lobby region for the parameter's region."""
    if level == Levels.JungleJapes:
        return Regions.JungleJapesLobby
    elif level == Levels.AngryAztec:
        return Regions.AngryAztecLobby
    elif level == Levels.FranticFactory:
        return Regions.FranticFactoryLobby
    elif level == Levels.GloomyGalleon:
        return Regions.GloomyGalleonLobby
    elif level == Levels.FungiForest:
        return Regions.FungiForestLobby
    elif level == Levels.CrystalCaves:
        return Regions.CrystalCavesLobby
    elif level == Levels.CreepyCastle:
        return Regions.CreepyCastleLobby
    else:
        return None


@lru_cache(maxsize=None)
def GetLevelExitTransition(level):
    """Get the exit level transition for the parameter region's level."""
    if level == Levels.JungleJapes:
        return Transitions.JapesToIsles
    elif level == Levels.AngryAztec:
        return Transitions.AztecToIsles
    elif level == Levels.FranticFactory:
        return Transitions.FactoryToIsles
    elif level == Levels.GloomyGalleon:
        return Transitions.GalleonToIsles
    elif level == Levels.FungiForest:
        return Transitions.ForestToIsles
    elif level == Levels.CrystalCaves:
        return Transitions.CavesToIsles
    elif level == Levels.CreepyCastle:
        return Transitions.CastleToIsles
    else:
        return None


def should_skip_location(location, location_obj, spoiler, settings, region):
    """Check if a location should be skipped based on various criteria."""
    # Skip if location is inaccessible
    if location_obj.inaccessible:
        return True

    # Skip bonus barrels based on settings and logic
    if location.bonusBarrel:
        if not (
            (location.bonusBarrel is MinigameType.BonusBarrel and settings.bonus_barrels == MinigameBarrels.skip)
            or (location.bonusBarrel is MinigameType.HelmBarrelFirst and (settings.helm_barrels == MinigameBarrels.skip or settings.helm_room_bonus_count == HelmBonuses.zero))
            or (location.bonusBarrel is MinigameType.HelmBarrelSecond and (settings.helm_barrels == MinigameBarrels.skip or settings.helm_room_bonus_count != HelmBonuses.two))
            or (location.bonusBarrel is MinigameType.TrainingBarrel and settings.training_barrels_minigames == MinigameBarrels.skip)
        ):
            if not MinigameRequirements[BarrelMetaData[location.id].minigame].logic(spoiler.LogicVariables):
                return True

    # Skip hint doors if the wrong Kong
    if location_obj.type == Types.Hint and not spoiler.LogicVariables.HintAccess(location_obj, region.id):
        return True

    # Skip blueprint locations if the wrong Kong
    if location_obj.item and ItemList[location_obj.item].type == Types.Blueprint:
        if not spoiler.LogicVariables.BlueprintAccess(ItemList[location_obj.item]):
            return True

    # Skip Kasplats with no blueprint if the wrong Kong
    if location_obj.type == Types.Blueprint:
        if not spoiler.LogicVariables.IsKong(location_obj.kong) and not settings.free_trade_items:
            return True

    # Skip dirt patches if no shockwave
    if location_obj.type == Types.RainbowCoin and not spoiler.LogicVariables.shockwave:
        return True

    # Skip Helm crowns if Helm isn't finished
    if location_obj.type == Types.Crown and location_obj.level == Levels.HideoutHelm:
        if Events.HelmFinished not in spoiler.LogicVariables.Events:
            return True

    return False


def GetAccessibleLocations(
    spoiler: Spoiler,
    startingOwnedItems: List[Union[Any, Items]],
    searchType: SearchMode,
    purchaseList: Optional[List[Locations]] = None,
    targetItemId: None = None,
) -> Union[List[Sphere], List[Locations], bool, Set[Union[Locations, int]]]:
    """Search to find all reachable locations given owned items."""
    settings = spoiler.settings
    # No logic? Calls to this method that are checking things just return True
    if settings.logic_type == LogicType.nologic and searchType in [
        SearchMode.CheckAllReachable,
        SearchMode.CheckBeatable,
        SearchMode.CheckSpecificItemReachable,
    ]:
        return True
    if purchaseList is None:
        purchaseList = []
    accessible = set()
    newLocations = set()
    ownedItems = startingOwnedItems[:]
    newItems = []  # debug code utility
    if searchType == SearchMode.GeneratePlaythrough:
        spoiler.playthroughTransitionOrder = []
    playthroughLocations = []
    unpurchasedEmptyShopLocationIds = []
    kongAccessibleRegions = [
        {Regions.GameStart},
        {Regions.GameStart},
        {Regions.GameStart},
        {Regions.GameStart},
        {Regions.GameStart},
    ]
    eventAdded = True
    UnderwaterRegions = {
        Regions.LighthouseUnderwater,
        Regions.ShipyardUnderwater,
        Regions.TreasureRoom,
        Regions.MermaidRoom,
        Regions.Submarine,
        Regions.LankyShip,
        Regions.TinyShip,
        Regions.BongosShip,
        Regions.GuitarShip,
        Regions.TromboneShip,
        Regions.SaxophoneShip,
        Regions.TriangleShip,
    }
    SurfaceWaterRegions = {Regions.Shipyard}
    # Continue doing searches until nothing new is found
    while len(newLocations) > 0 or eventAdded:
        # Add items and events from the last search iteration
        sphere = Sphere()
        if playthroughLocations:
            sphere.availableGBs = playthroughLocations[-1].availableGBs
        for locationId in newLocations:
            accessible.add(locationId)
            location = spoiler.LocationList[locationId]
            if location.logically_relevant:
                spoiler.LogicVariables.SpecialLocationsReached.append(locationId)
            # If this location has an item placed, add it to owned items
            if location.item is not None:
                # In search mode GetReachableWithControlledPurchases, only allowed to purchase items as prescribed by purchaseOrder
                if location.type == Types.Shop and searchType == SearchMode.GetReachableWithControlledPurchases and locationId not in purchaseList:
                    continue
                ownedItems.append(location.item)
                newItems.append(location.item)
                # If we want to generate the playthrough and the item is a playthrough item, add it to the sphere
                if searchType == SearchMode.GeneratePlaythrough and ItemList[location.item].playthrough:
                    if location.item == Items.GoldenBanana:
                        sphere.availableGBs += 1
                        sphere.locations.append(locationId)
                        continue
                    # Banana hoard in a sphere by itself
                    elif location.item == Items.BananaHoard:
                        sphere.locations = [locationId]
                        break
                    # The starting shop owner locations are not eligible for the playthrough
                    if location.type not in (Types.Cranky, Types.Funky, Types.Candy, Types.Snide):
                        sphere.locations.append(locationId)
                # If we're looking for one item and we find it, we're done
                elif searchType == SearchMode.CheckSpecificItemReachable and location.item == targetItemId:
                    return True
        eventAdded = False
        # Reset new lists
        newLocations = set()
        # Update based on new items
        spoiler.LogicVariables.Update(ownedItems)
        newItems = []
        if len(sphere.locations) > 0:
            if searchType == SearchMode.GeneratePlaythrough:
                sphere.seedBeaten = spoiler.LogicVariables.bananaHoard
            playthroughLocations.append(sphere)

        # If we're checking beatability, check for the Banana Hoard after updating the last set of locations
        if searchType == SearchMode.CheckBeatable and spoiler.LogicVariables.bananaHoard:
            return True

        # Do a search for each owned kong
        for kong in set(spoiler.LogicVariables.GetKongs()):
            spoiler.LogicVariables.SetKong(kong)

            startRegion = spoiler.RegionList[Regions.GameStart]
            startRegion.id = Regions.GameStart
            startRegion.dayAccess = [Events.Day in spoiler.LogicVariables.Events] * 5
            startRegion.nightAccess = [Events.Night in spoiler.LogicVariables.Events] * 5
            regionPool = list(kongAccessibleRegions[kong])

            # Loop for each region until no more accessible regions found
            while len(regionPool) > 0:
                regionId = regionPool.pop()
                region = spoiler.RegionList[regionId]
                # If this region has a tag barrel, everyone can access this region now
                if region.tagbarrel:
                    if region.dayAccess[kong]:
                        region.dayAccess = [True] * 5
                    if region.nightAccess[kong]:
                        region.nightAccess = [True] * 5
                    for i in range(5):
                        kongAccessibleRegions[i].add(regionId)
                # Check accessibility for each event in this region
                for event in region.events:
                    if event.name not in spoiler.LogicVariables.Events and event.logic(spoiler.LogicVariables):
                        # Add the event if it's not already in the list and its logic is satisfied
                        eventAdded = True
                        spoiler.LogicVariables.Events.append(event.name)

                    # Update region access based on specific events
                    if event.name == Events.Night:
                        if event.logic(spoiler.LogicVariables):
                            region.nightAccess[kong] = True
                    elif event.name == Events.Day:
                        if event.logic(spoiler.LogicVariables):
                            region.dayAccess[kong] = True
                # Check accessibility for collectibles
                if region.id in spoiler.CollectibleRegions.keys():
                    for collectible in spoiler.CollectibleRegions[region.id]:
                        if not collectible.added and collectible.kong in (kong, Kongs.any) and collectible.enabled and collectible.logic(spoiler.LogicVariables):
                            spoiler.LogicVariables.AddCollectible(collectible, region.level)
                # Check accessibility for each location in this region

                for location in region.locations:
                    # Skip locations already accessible or not meeting logic
                    if location.id in newLocations or location.id in accessible or not location.logic(spoiler.LogicVariables):
                        continue

                    location_obj = spoiler.LocationList[location.id]

                    if should_skip_location(location, location_obj, spoiler, settings, region):
                        continue

                    # Handle shop logic
                    if location_obj.type == Types.Shop:
                        shop_is_empty = location_obj.item is None or location_obj.item == Items.NoItem
                        location_can_be_bought = searchType != SearchMode.GetReachableWithControlledPurchases or location.id in purchaseList

                        if not shop_is_empty and location_can_be_bought:
                            spoiler.LogicVariables.PurchaseShopItem(location.id)
                        elif shop_is_empty:
                            unpurchasedEmptyShopLocationIds.append(location.id)
                    elif location.id == Locations.NintendoCoin:
                        # Spend Two Coins for arcade lever
                        spoiler.LogicVariables.Coins[Kongs.donkey] -= 2
                        spoiler.LogicVariables.SpentCoins[Kongs.donkey] += 2

                    newLocations.add(location.id)

                # Check accessibility for each exit in this region
                exits = region.exits[:]
                # If loading zones are shuffled, the "Exit Level" button in the pause menu could potentially take you somewhere new
                if settings.shuffle_loading_zones == ShuffleLoadingZones.all and region.level != Levels.DKIsles and region.level != Levels.Shops:
                    levelExit = GetExitLevelExit(region.level, region.restart)
                    # When shuffling levels, unplaced level entrances will have no destination yet
                    if levelExit is not None:
                        dest = ShuffleExits.ShufflableExits[levelExit].back.regionId
                        exits.append(TransitionFront(dest, lambda l: True))
                        # If we're generating the final playthrough, note down the order in which we access entrances for LZR purposes
                        # No need to check access on this transition, it's always accessible
                        if searchType == SearchMode.GeneratePlaythrough:
                            levelExitTransitionId = GetLevelExitTransition(region.level)
                            if levelExitTransitionId not in spoiler.playthroughTransitionOrder:
                                spoiler.playthroughTransitionOrder.append(levelExitTransitionId)
                # If loading zones are not shuffled but you have a random starting location, you may need to exit level to escape some regions
                elif settings.random_starting_region and region.level != Levels.DKIsles and region.level != Levels.Shops and region.restart is None:
                    levelLobby = GetLobbyOfRegion(region.level)
                    if levelLobby is not None and levelLobby not in kongAccessibleRegions[kong]:
                        exits.append(TransitionFront(levelLobby, lambda l: True))
                for exit in exits:
                    destination = exit.dest
                    shuffle_id = exit.exitShuffleId
                    is_shuffled = shuffle_id is not None and not exit.assumed

                    # Handle shuffled exits
                    if is_shuffled:
                        shuffled_exit = ShuffleExits.ShufflableExits[shuffle_id]
                        if shuffled_exit.shuffled:
                            destination = ShuffleExits.ShufflableExits[shuffled_exit.shuffledId].back.regionId
                        elif shuffled_exit.toBeShuffled:
                            continue

                    # Check if the transition is accessible
                    if not exit.logic(spoiler.LogicVariables):
                        continue

                    # Handle water/lava restrictions
                    is_lava_water = spoiler.LogicVariables.IsLavaWater()
                    if is_lava_water and (settings.shuffle_loading_zones == ShuffleLoadingZones.all or settings.random_starting_region):
                        if destination in UnderwaterRegions and spoiler.LogicVariables.Melons < 3:
                            continue
                        if destination in SurfaceWaterRegions and spoiler.LogicVariables.Melons < 2:
                            continue

                    # Check time of day access
                    time_access = True
                    if exit.time == Time.Night and not region.nightAccess[kong]:
                        time_access = False
                    elif exit.time == Time.Day and not region.dayAccess[kong]:
                        time_access = False

                    if not time_access:
                        continue

                    # Track playthrough transitions if needed
                    if searchType == SearchMode.GeneratePlaythrough and settings.shuffle_loading_zones == ShuffleLoadingZones.all:
                        if shuffle_id and shuffle_id not in spoiler.playthroughTransitionOrder:
                            spoiler.playthroughTransitionOrder.append(shuffle_id)

                    # Add new regions to the queue
                    if destination not in kongAccessibleRegions[kong]:
                        kongAccessibleRegions[kong].add(destination)
                        new_region = spoiler.RegionList[destination]
                        new_region.id = destination
                        regionPool.append(destination)

                    # Update day/night access
                    region_list_dest = spoiler.RegionList[destination]
                    if region.dayAccess[kong] and exit.time != Time.Night and not region_list_dest.dayAccess[kong]:
                        region_list_dest.dayAccess[kong] = True
                        eventAdded = True
                    if region.nightAccess[kong] and exit.time != Time.Day and not region_list_dest.nightAccess[kong]:
                        region_list_dest.nightAccess[kong] = True
                        eventAdded = True

                    # Handle dusk time setting
                    if settings.fungi_time == FungiTimeSetting.dusk:
                        region_list_dest.dayAccess[kong] = True
                        region_list_dest.nightAccess[kong] = True

                # Deathwarps currently send to the vanilla destination
                if region.deathwarp and not settings.perma_death:
                    destination = region.deathwarp.dest
                    # If a region is accessible through this exit and has not yet been added, add it to the queue to be visited eventually
                    if destination not in kongAccessibleRegions[kong] and region.deathwarp.logic(spoiler.LogicVariables):
                        kongAccessibleRegions[kong].add(destination)
                        newRegion = spoiler.RegionList[destination]
                        newRegion.id = destination
                        regionPool.append(destination)
                        # If this region has day access, the deathwarp will occur on the same time of day
                        # Note that no deathwarps are dependent on time of day
                        if region.dayAccess[kong]:
                            spoiler.RegionList[destination].dayAccess[kong] = True
                            # Count as event added so search doesn't get stuck if region is searched,
                            # then later a new time of day access is found so it should be re-visited
                            eventAdded = True
                        # And vice versa
                        if region.nightAccess[kong]:
                            spoiler.RegionList[destination].nightAccess[kong] = True
                            eventAdded = True
    # If we're here to get accessible locations for fill purposes, we need to take a harder look at all the empty shops we didn't buy
    if searchType == SearchMode.GetReachableForFilling:
        spoiler.settings.random.shuffle(unpurchasedEmptyShopLocationIds)  # This shuffle is to not bias fills towards earlier shops
        # For each location...
        for location_id in unpurchasedEmptyShopLocationIds:
            # If we can, "buy" the empty location. This will affect our ability to buy future locations. It's not a guarantee we'll be able to buy all of these locations.
            if (location_id in SharedShopLocations and spoiler.LogicVariables.AnyKongCanBuy(location_id, buy_empty=True)) or (
                location_id not in SharedShopLocations and spoiler.LogicVariables.CanBuy(location_id, buy_empty=True)
            ):
                spoiler.LogicVariables.PurchaseShopItem(location_id)
            # If we can't, treat the location as inaccessible
            else:
                accessible.remove(location_id)
    if searchType in (
        SearchMode.GetReachable,
        SearchMode.GetReachableForFilling,
        SearchMode.GetReachableWithControlledPurchases,
    ):
        return accessible
    elif searchType == SearchMode.CheckBeatable or searchType == SearchMode.CheckSpecificItemReachable:
        # If the search has completed and the target item has not been found, then we failed to find it
        # settings.debug_accessible = accessible
        return False
    elif searchType == SearchMode.GeneratePlaythrough:
        return playthroughLocations
    elif searchType == SearchMode.CheckAllReachable:
        expected_accessible_locations = [x for x in spoiler.LocationList if not spoiler.LocationList[x].inaccessible]
        if settings.extreme_debugging:
            # Debugging variables: they are unaccessed but certainly useful. Do not touch!
            incorrectly_accessible = [x for x in accessible if x not in expected_accessible_locations]
            incorrectly_inaccessible = [x for x in expected_accessible_locations if x not in accessible]
            always_inaccessible_locations = [x for x in spoiler.LocationList if spoiler.LocationList[x].inaccessible]
            settings.debug_accessible = accessible
            settings.debug_accessible_not = [location for location in spoiler.LocationList if location not in accessible]
            settings.debug_enormous_pain_1 = [spoiler.LocationList[location] for location in settings.debug_accessible]
            settings.debug_enormous_pain_3 = [spoiler.LocationList[location] for location in settings.debug_accessible_not]
            if len(accessible) != len(expected_accessible_locations):
                return False
            return True
        return len(accessible) == len(expected_accessible_locations)
    elif searchType == SearchMode.GetUnreachable:
        return [x for x in spoiler.LocationList if x not in accessible and not spoiler.LocationList[x].inaccessible]


def VerifyWorld(spoiler: Spoiler) -> bool:
    """Make sure all item locations are reachable on current world graph with no items placed and all items owned."""
    settings = spoiler.settings
    if settings.logic_type == LogicType.nologic:
        return True  # Don't need to verify world in no logic
    unreachables = GetAccessibleLocations(spoiler, ItemPool.AllItemsUnrestricted(settings), SearchMode.GetUnreachable)
    if len(spoiler.cb_placements) == 0:
        unreachables = [
            x
            for x in unreachables
            if x
            not in [
                Locations.IslesDonkeyMedal,
                Locations.IslesDiddyMedal,
                Locations.IslesLankyMedal,
                Locations.IslesTinyMedal,
                Locations.IslesChunkyMedal,
            ]
        ]
    allLocationsReached = len(unreachables) == 0
    allCBsFound = True
    for level_index in range(9):
        isles_cb_rando_enabled = IsItemSelected(spoiler.settings.cb_rando_enabled, spoiler.settings.cb_rando_list_selected, Levels.DKIsles)
        if level_index == Levels.HideoutHelm:
            continue
        elif level_index == Levels.DKIsles and (not isles_cb_rando_enabled) or len(spoiler.cb_placements) == 0:
            continue
        if sum(spoiler.LogicVariables.ColoredBananas[level_index]) != 500:
            missingCBs = []
            for region_collectible_list in spoiler.CollectibleRegions.values():
                for collectible in region_collectible_list:
                    if collectible.enabled and not collectible.added:
                        missingCBs.append(collectible)
            allCBsFound = False
    if spoiler.settings.extreme_debugging and not allLocationsReached:
        print(f"Unable to reach all locations: {unreachables}")
    if spoiler.settings.extreme_debugging and not allCBsFound:
        print(f"Unable to reach all CBs: {spoiler.LogicVariables.ColoredBananas}")
    spoiler.Reset()
    return allLocationsReached and allCBsFound


def VerifyWorldWithWorstCoinUsage(spoiler: Spoiler) -> bool:
    """Make sure the game is beatable without it being possible to run out of coins for required moves."""
    settings = spoiler.settings
    if settings.logic_type == LogicType.nologic:
        return True  # Don't verify world in no logic
    locationsToPurchase = []
    reachable = []
    maxCoins = [
        GetMaxForKong(spoiler, Kongs.donkey),
        GetMaxForKong(spoiler, Kongs.diddy),
        GetMaxForKong(spoiler, Kongs.lanky),
        GetMaxForKong(spoiler, Kongs.tiny),
        GetMaxForKong(spoiler, Kongs.chunky),
    ]
    # Set up some thresholds for speeding this method up
    medalThreshold = settings.medal_requirement
    fairyThreshold = settings.rareware_gb_fairies
    pearlThreshold = settings.mermaid_gb_pearls
    while 1:
        spoiler.Reset()
        reachable = GetAccessibleLocations(spoiler, [], SearchMode.GetReachableWithControlledPurchases, locationsToPurchase)
        # Subtract the price of the chosen location from maxCoinsNeeded
        coinsSpent = GetMaxCoinsSpent(spoiler, locationsToPurchase)
        coinsNeeded = [maxCoins[kong] - coinsSpent[kong] for kong in range(0, 5)]
        spoiler.LogicVariables.UpdateCoins()
        coinsBefore = spoiler.LogicVariables.Coins.copy()
        # print("Coins owned during search: " + str(coinsBefore))
        # print("Coins needed during search: " + str(coinsNeeded))
        # If we found enough coins that every kong can buy all their moves, world is valid!
        if (
            coinsBefore[Kongs.donkey] >= coinsNeeded[Kongs.donkey]
            and coinsBefore[Kongs.diddy] >= coinsNeeded[Kongs.diddy]
            and coinsBefore[Kongs.lanky] >= coinsNeeded[Kongs.lanky]
            and coinsBefore[Kongs.tiny] >= coinsNeeded[Kongs.tiny]
            and coinsBefore[Kongs.chunky] >= coinsNeeded[Kongs.chunky]
        ):
            # print("Seed is valid, found enough coins with worst purchase order: " + str([LocationList[x].name + ": " + LocationList[x].item.name + ", " for x in locationsToPurchase]))
            spoiler.Reset()
            return True
        # If we found the Banana Hoard, world is valid!
        if spoiler.LogicVariables.bananaHoard:
            # print("Seed is valid, found banana hoard with worst purchase order: " + str([LocationList[x].name + ": " + LocationList[x].item.name + ", " for x in locationsToPurchase]))
            spoiler.Reset()
            return True
        # For each accessible shop location
        newReachableShops = [
            x
            for x in reachable
            if spoiler.LocationList[x].type == Types.Shop
            and spoiler.LocationList[x].item is not None
            and spoiler.LocationList[x].item != Items.NoItem
            and x not in locationsToPurchase
            and spoiler.LogicVariables.CanBuy(x)
        ]
        shopDifferentials = {}
        shopUnlocksItems = {}
        # If no accessible shop locations found, means you got coin locked and the seed is not valid
        if len(newReachableShops) == 0:
            print("Seed is invalid, coin locked with purchase order: " + str([spoiler.LocationList[x].name + ": " + spoiler.LocationList[x].item.name + ", " for x in locationsToPurchase]))
            spoiler.Reset()
            return False
        # We can cheat some - here we calculate things we know we can add to the purchase order for free
        # All we have to do is ensure that these items are not progressive in ANY way
        # If we manage to add anything to the purchase order, we cut N GetAccessibleLocation calls where N is the length of newReachableShops
        anythingAddedToPurchaseOrder = False
        # Thresholds are the values that would cause the next item of that type to give you access to more locations
        # The GB threshold is the next B. Locker from what we've previously found - opening a B. Locker likely gives you access to more coins
        currentGBCount = spoiler.LogicVariables.GoldenBananas
        gbThreshold = 1000
        for blocker in range(0, 8):
            if settings.BLockerEntryCount[blocker] > currentGBCount and settings.BLockerEntryCount[blocker] < gbThreshold:
                gbThreshold = settings.BLockerEntryCount[blocker]
        currentMedalCount = spoiler.LogicVariables.BananaMedals  # Jetpac access might give you another item that gives you access to more coins
        currentFairyCount = spoiler.LogicVariables.BananaFairies  # Rareware GB access might do the same
        currentPearlCount = spoiler.LogicVariables.Pearls  # Mermaid GB access might do the same
        for shopLocationId in newReachableShops:
            # Check all of the newly reachable shops' items
            shopItem = spoiler.LocationList[shopLocationId].item
            # If the item is not going to exactly meet that item type's threshold, we can freely purchase it knowing it will never be progression
            if shopItem == Items.Pearl and (currentPearlCount < (pearlThreshold - 1) or currentPearlCount >= pearlThreshold):
                currentPearlCount += 1  # Treat the item as collected for future calculations, we might approach the threshold during this process
                locationsToPurchase.append(shopLocationId)
                anythingAddedToPurchaseOrder = True
            if shopItem == Items.BananaMedal and (currentMedalCount < (medalThreshold - 1) or currentMedalCount >= medalThreshold):
                currentMedalCount += 1
                locationsToPurchase.append(shopLocationId)
                anythingAddedToPurchaseOrder = True
            if shopItem == Items.BananaFairy and (currentFairyCount < (fairyThreshold - 1) or currentFairyCount >= fairyThreshold):
                currentFairyCount += 1
                locationsToPurchase.append(shopLocationId)
                anythingAddedToPurchaseOrder = True
            # Treat GBs and Blueprints as identical
            if (shopItem == Items.GoldenBanana or shopItem in ItemPool.Blueprints()) and (currentGBCount < (gbThreshold - 1) or currentGBCount > gbThreshold):
                currentGBCount += 1
                locationsToPurchase.append(shopLocationId)
                anythingAddedToPurchaseOrder = True
            # These items will never practically give progression. Helm doors are not really relevant here, as any theoretical coin lock will happen WELL before this point.
            if shopItem in (Items.BattleCrown, Items.IceTrapBubble, Items.RarewareCoin, Items.NintendoCoin):
                locationsToPurchase.append(shopLocationId)
                anythingAddedToPurchaseOrder = True
        # If we added anything to the purchase order, short-circuit back to the top of the loop and keep going with a (hopefully) greatly expanded purchase list
        if anythingAddedToPurchaseOrder:
            continue
        # Now that we know our next item has to give us progression in some form, we can consolidate our "worst location candidates" into the worst options among each type
        # Find the most expensive location of each type (it may not exist)
        mostExpensivePearl = None
        pearlShops = [location for location in newReachableShops if spoiler.LocationList[location].item == Items.Pearl]
        if settings.random_prices == RandomPrices.vanilla and len(pearlShops) > 0:  # In vanilla prices, prices are by item so we know all these locations have the same price (0)
            mostExpensivePearl = pearlShops[0]
        else:
            for shop in pearlShops:
                if mostExpensivePearl is None or settings.prices[shop] > settings.prices[mostExpensivePearl]:
                    mostExpensivePearl = shop
        mostExpensiveMedal = None
        medalShops = [location for location in newReachableShops if spoiler.LocationList[location].item == Items.BananaMedal]
        if settings.random_prices == RandomPrices.vanilla and len(medalShops) > 0:  # Same vanilla price logic applies to all of the threshold types (they all cost 0)
            mostExpensiveMedal = medalShops[0]
        else:
            for shop in medalShops:
                if mostExpensiveMedal is None or settings.prices[shop] > settings.prices[mostExpensiveMedal]:
                    mostExpensiveMedal = shop
        mostExpensiveFairy = None
        fairyShops = [location for location in newReachableShops if spoiler.LocationList[location].item == Items.BananaFairy]
        if settings.random_prices == RandomPrices.vanilla and len(fairyShops) > 0:
            mostExpensiveFairy = fairyShops[0]
        else:
            for shop in fairyShops:
                if mostExpensiveFairy is None or settings.prices[shop] > settings.prices[mostExpensiveFairy]:
                    mostExpensiveFairy = shop
        mostExpensiveGB = None
        gbShops = [location for location in newReachableShops if (spoiler.LocationList[location].item == Items.GoldenBanana or spoiler.LocationList[location].item in ItemPool.Blueprints())]
        if settings.random_prices == RandomPrices.vanilla and len(gbShops) > 0:  # While GBs and Blueprints aren't the same item, they both always cost 0 in vanilla
            mostExpensiveGB = gbShops[0]
        else:
            for shop in gbShops:
                if mostExpensiveGB is None or settings.prices[shop] > settings.prices[mostExpensiveGB]:
                    mostExpensiveGB = shop
        # Prepare the candidates for "worst location" - exclude any of the threshold items that we know the worst of
        thresholdItems = ItemPool.Blueprints().copy()
        thresholdItems.extend([Items.Pearl, Items.BananaMedal, Items.BananaFairy, Items.GoldenBanana])
        worstLocationCandidates = [shop for shop in newReachableShops if spoiler.LocationList[shop].item not in thresholdItems]
        # If there exists a spot of this type, then we add the worst of this type to our list of candidates
        if mostExpensivePearl is not None:
            worstLocationCandidates.append(mostExpensivePearl)
        if mostExpensiveMedal is not None:
            worstLocationCandidates.append(mostExpensiveMedal)
        if mostExpensiveFairy is not None:
            worstLocationCandidates.append(mostExpensiveFairy)
        if mostExpensiveGB is not None:
            worstLocationCandidates.append(mostExpensiveGB)
        locationToBuy = worstLocationCandidates[0]
        if len(worstLocationCandidates) > 1:  # Things can be sped up if there's only one option (this tends to happen)
            for shopLocation in worstLocationCandidates:
                # Recheck accessible to see how many coins will be available afterward
                tempLocationsToPurchase = locationsToPurchase.copy()
                tempLocationsToPurchase.append(shopLocation)
                spoiler.Reset()
                reachableAfter: list = GetAccessibleLocations(spoiler, [], SearchMode.GetReachableWithControlledPurchases, tempLocationsToPurchase)
                spoiler.LogicVariables.UpdateCoins()
                coinsAfter = spoiler.LogicVariables.Coins.copy()
                # Calculate the coin differential
                coinDifferential = [0, 0, 0, 0, 0]
                for kong in spoiler.LogicVariables.GetKongs():
                    coinDifferential[kong] = coinsAfter[kong] - coinsBefore[kong]
                # print("Coin differential: " + str(coinDifferential))
                shopDifferentials[shopLocation] = coinDifferential
                shopUnlocksItems[shopLocation] = [spoiler.LocationList[x].item for x in reachableAfter if x not in reachable and spoiler.LocationList[x].item is not None]
                # Determine if this is the new worst move
                if locationToBuy is None:
                    locationToBuy = shopLocation
                    continue
                # Coin differential must be negative for at least one kong to be considered new worst
                if len([x for x in shopDifferentials[shopLocation] if x < 0]) == 0:
                    continue
                # If a move unlocks new kongs it is more useful than others, even if it has a worse coin differential
                existingMoveKongsUnlocked = len([x for x in shopUnlocksItems[locationToBuy] if ItemList[x].type == Types.Kong])
                currentMoveKongsUnlocked = len([x for x in shopUnlocksItems[shopLocation] if ItemList[x].type == Types.Kong])
                if currentMoveKongsUnlocked > existingMoveKongsUnlocked:
                    continue
                # If a move unlocks a new boss key it is more useful than others, even if it has a worse coin differential
                existingMoveKeysUnlocked = len([x for x in shopUnlocksItems[locationToBuy] if ItemList[x].type == Types.Key])
                currentMoveKeysUnlocked = len([x for x in shopUnlocksItems[shopLocation] if ItemList[x].type == Types.Key])
                if currentMoveKeysUnlocked > existingMoveKeysUnlocked:
                    continue
                # All else equal, pick the move with the lowest overall coin differential
                existingMoveCoinDiff = sum(list(shopDifferentials[locationToBuy]))
                currentMoveCoinDiff = sum(list(shopDifferentials[shopLocation]))
                if currentMoveCoinDiff < existingMoveCoinDiff:
                    locationToBuy = shopLocation
        # Purchase the "least helpful" move & add to owned Items
        # print("Choosing to buy " + LocationList[locationToBuy].item.name + " from " + LocationList[locationToBuy].name)
        locationsToPurchase.append(locationToBuy)


def ParePlaythrough(spoiler: Spoiler, PlaythroughLocations: List[Sphere]) -> None:
    """Pare playthrough down to only the essential elements."""
    settings = spoiler.settings
    AccessibleHintsForLocation = {}
    locationsToAddBack = []
    mostExpensiveBLocker = max(
        [
            settings.blocker_0,
            settings.blocker_1,
            settings.blocker_2,
            settings.blocker_3,
            settings.blocker_4,
            settings.blocker_5,
            settings.blocker_6,
            settings.blocker_7,
        ]
    )
    # Check every location in the list of spheres.
    for i in range(len(PlaythroughLocations) - 1, -1, -1):
        # We can immediately ignore spheres past the first sphere that is beaten
        if i > 0 and PlaythroughLocations[i - 1].seedBeaten:
            PlaythroughLocations.remove(PlaythroughLocations[i])
            continue
        sphere = PlaythroughLocations[i]
        # We want to track specific GBs in each sphere of the spoiler log up to and including the sphere where the last B. Locker becomes openable
        if i > 0 and PlaythroughLocations[i - 1].availableGBs > mostExpensiveBLocker:
            sphere.locations = [locationId for locationId in sphere.locations if spoiler.LocationList[locationId].item != Items.GoldenBanana]
        for locationId in sphere.locations.copy():
            location = spoiler.LocationList[locationId]
            # All GBs that make it here are logically required
            if location.item == Items.GoldenBanana:
                continue
            # These items aren't usually that important - to make it here they have to be part of the win condition or one of the Helm doors
            # They'll be part of the Playthrough but aren't candidates for the WotH, so we don't have to do any calculations on them
            if location.item in (Items.BananaFairy, Items.BananaMedal, Items.RainbowCoin, Items.BattleCrown):
                continue
            if location.item is not None and ItemList[location.item].type == Types.Blueprint:
                continue
            # Copy out item from location
            item = location.item
            location.item = None
            # Check if the game is still beatable
            spoiler.Reset()
            gameIsBeatable = GetAccessibleLocations(spoiler, [], SearchMode.CheckBeatable)
            # Make note of what hints are accessible without this WotH candidate in case it gets hinted later.
            # This may miss hints available after the win condition is met, but those hints are never practically getting seen anyway.
            AccessibleHintsForLocation[locationId] = spoiler.LogicVariables.Hints.copy()
            if gameIsBeatable:
                # If the game is still beatable, this is an unnecessary location. We remove it from the playthrough, as it is not strictly required.
                sphere.locations.remove(locationId)
                # In non-item rando, put back the items on a delay
                if not spoiler.settings.shuffle_items:
                    # We delay the item to ensure future locations which may rely on this one do not give a false positive for beatability.
                    # This is legacy behavior I'm not convinced needs to exist. It stays in non-item rando because the performance cost is negligible there.
                    location.SetDelayedItem(item)
                    locationsToAddBack.append(locationId)
                # In item rando, we do additional WotH paring via paths later, so we don't need to worry about getting it perfect here
                else:
                    location.PlaceItem(spoiler, item)
            else:
                # If the game is not beatable without this item, don't remove it from the playthrough and add the item back. This is now a WotH candidate.
                location.PlaceItem(spoiler, item)
                # Some important items have inherent door restrictions depending on the settings
                restrictions = getDoorRestrictionsForItem(spoiler, item)
                if len(restrictions) > 0:
                    AccessibleHintsForLocation[locationId] = [hint for hint in AccessibleHintsForLocation[locationId] if hint in restrictions]
    # Record that dictionary of hint access for when we compile hints
    spoiler.accessible_hints_for_location = AccessibleHintsForLocation
    # Check if there are any empty spheres, if so remove them
    for i in range(len(PlaythroughLocations) - 1, -1, -1):
        sphere = PlaythroughLocations[i]
        if len(sphere.locations) == 0:
            PlaythroughLocations.remove(sphere)

    # Re-place those items which were delayed earlier.
    for locationId in locationsToAddBack:
        spoiler.LocationList[locationId].PlaceDelayedItem(spoiler)


def PareWoth(spoiler: Spoiler, PlaythroughLocations: List[Sphere]) -> List[Union[Locations, int]]:
    """Pare playthrough to locations which are Way of the Hoard (hard required by logic)."""
    # The functionality is similar to ParePlaythrough, but we want to see if individual locations are
    # hard required, so items are added back after checking regardless of the outcome.
    WothLocations = []
    for sphere in PlaythroughLocations:
        # Don't want constant locations in woth and we can filter out some types of items as not being essential to the woth
        for loc in [
            loc
            for loc in sphere.locations  # If Keys are constant, we may still want path hints for them.
            if (not spoiler.LocationList[loc].constant or ItemList[spoiler.LocationList[loc].item].type == Types.Key)
            and ItemList[spoiler.LocationList[loc].item].type
            not in (
                Types.Banana,
                Types.BlueprintBanana,
                Types.Crown,
                Types.Medal,
                Types.Blueprint,
                Types.Fairy,
                Types.RainbowCoin,
                Types.CrateItem,
                Types.Enemies,
            )
        ]:
            WothLocations.append(loc)
    WothLocations.append(Locations.BananaHoard)  # The Banana Hoard is the endpoint of the Way of the Hoard

    spoiler.majorItems = []  # Initialize in case something dumb happens
    # Only need to build paths for item rando
    if spoiler.settings.shuffle_items:
        majorItems = IdentifyMajorItems(spoiler)
        spoiler.majorItems = majorItems
        CalculateWothPaths(spoiler, WothLocations, majorItems)
        CalculateFoolish(spoiler, WothLocations, majorItems)
    # Non-item rando needs additional WotH paring due to the delayed item re-placing done when paring the playthrough
    else:
        # Check every item location to see if removing it by itself makes the game unbeatable
        for i in range(len(WothLocations) - 1, -1, -1):
            locationId = WothLocations[i]
            location = spoiler.LocationList[locationId]
            item = location.item
            location.item = None
            # Check if game is still beatable
            spoiler.Reset()
            if GetAccessibleLocations(spoiler, [], SearchMode.CheckBeatable):
                # If game is still beatable, this location is not hard required
                WothLocations.remove(locationId)
            # Either way, add location back
            location.PlaceItem(spoiler, item)
    # We kept Keys around to generate paths better, but we don't need them in the spoiler log or being hinted (except for the Helm Key if it's there and also keep the Banana Hoard path)
    WothLocations = [loc for loc in WothLocations if not spoiler.LocationList[loc].constant or loc == Locations.HelmKey or loc == Locations.BananaHoard]
    if spoiler.settings.shuffle_items:
        # The non-key 8 paths are a bit misleading, so it's best not to show them
        for path_loc in [key for key in spoiler.woth_paths.keys()]:
            if path_loc not in WothLocations:
                del spoiler.woth_paths[path_loc]
    return WothLocations


def checkCommonBarriers(settings: Settings, target_item: BarrierItems, target_win_con: WinConditionComplex) -> bool:
    """Check common barriers which would make an item a major one."""
    if settings.coin_door_item == target_item:
        return True
    if settings.crown_door_item == target_item:
        return True
    if target_item in settings.BLockerEntryItems:
        return True
    return settings.win_condition_item == target_win_con


def IdentifyMajorItems(spoiler: Spoiler) -> List[Locations]:
    """Identify the Major Items in this seed based on the item placement and the settings."""
    # Use the settings to determine non-progression Major Items
    majorItems = ItemPool.AllKongMoves()
    if Types.Cranky in spoiler.settings.shuffled_location_types:
        majorItems.extend(ItemPool.CrankyItems())
    if Types.Funky in spoiler.settings.shuffled_location_types:
        majorItems.extend(ItemPool.FunkyItems())
    if Types.Candy in spoiler.settings.shuffled_location_types:
        majorItems.extend(ItemPool.CandyItems())
    if Types.Snide in spoiler.settings.shuffled_location_types:
        majorItems.extend(ItemPool.SnideItems())
    if spoiler.settings.training_barrels != TrainingBarrels.normal:
        majorItems.extend(ItemPool.TrainingBarrelAbilities())
    if spoiler.settings.climbing_status != ClimbingStatus.normal:
        majorItems.extend(ItemPool.ClimbingAbilities())
    if Types.Shockwave in spoiler.settings.shuffled_location_types:
        majorItems.extend(ItemPool.ShockwaveTypeItems(spoiler.settings))
    majorItems.extend(ItemPool.Keys())
    majorItems.extend(ItemPool.Kongs(spoiler.settings))

    if checkCommonBarriers(spoiler.settings, BarrierItems.CompanyCoin, WinConditionComplex.req_companycoins):
        majorItems.append(Items.RarewareCoin)  # A vanilla Rareware Coin should be considered a major item so medals will not be foolish
        majorItems.append(Items.NintendoCoin)  # A vanilla Nintendo Coin should be considered a major item
    if checkCommonBarriers(spoiler.settings, BarrierItems.Blueprint, WinConditionComplex.req_bp):
        majorItems.extend(ItemPool.Blueprints())
    if checkCommonBarriers(spoiler.settings, BarrierItems.Medal, WinConditionComplex.req_medal):
        majorItems.append(Items.BananaMedal)
    if checkCommonBarriers(spoiler.settings, BarrierItems.Fairy, WinConditionComplex.req_fairy):
        majorItems.append(Items.BananaFairy)
    if checkCommonBarriers(spoiler.settings, BarrierItems.Crown, WinConditionComplex.req_crown):
        majorItems.append(Items.BattleCrown)
    if checkCommonBarriers(spoiler.settings, BarrierItems.Pearl, WinConditionComplex.req_pearl):
        majorItems.append(Items.Pearl)
    if checkCommonBarriers(spoiler.settings, BarrierItems.Bean, WinConditionComplex.req_bean):
        majorItems.append(Items.Bean)
    if checkCommonBarriers(spoiler.settings, BarrierItems.RainbowCoin, WinConditionComplex.req_rainbowcoin):
        majorItems.append(Items.RainbowCoin)
    # The contents of some locations can make entire classes of items not foolish
    # Loop through these locations until no new items are added to the list of major items
    newFoolishItems = True
    while newFoolishItems:
        newFoolishItems = False
        if spoiler.LocationList[Locations.RarewareCoin].item in majorItems and Items.BananaMedal not in majorItems:
            majorItems.append(Items.BananaMedal)
            newFoolishItems = True
        if spoiler.LocationList[Locations.RarewareBanana].item in majorItems and Items.BananaFairy not in majorItems:
            majorItems.append(Items.BananaFairy)
            newFoolishItems = True
        if spoiler.LocationList[Locations.GalleonTinyPearls].item in majorItems and Items.Pearl not in majorItems:
            majorItems.append(Items.Pearl)
            newFoolishItems = True
        if spoiler.LocationList[Locations.ForestTinyBeanstalk].item in majorItems and Items.Bean not in majorItems:
            majorItems.append(Items.Bean)
            newFoolishItems = True
    return majorItems


def CalculateWothPaths(spoiler: Spoiler, WothLocations: List[Union[Locations, int]], MajorItems: List[Items]) -> None:
    """Calculate the Paths (dependencies) for each Way of the Hoard item."""
    # Helps get more accurate paths by removing important obstacles to level entry
    # Removes the following:
    # - The need for GBs and coins to reach locations
    # - The need for vines to progress in Aztec
    # - The need for swim to get into level 4
    # - The need for vines to get to upper Isles
    # - The need for all keys to access K. Rool
    # - The need for keys to open lobbies (this is done with open_lobbies)
    old_open_lobbies_temp = spoiler.settings.open_lobbies  # It's far less likely for a key to be a prerequisite
    spoiler.LogicVariables.assumePaidBLockers = True  # This means we don't have to worry about moves required to pay B. Lockers - we already know we can clear all B. Lockers
    spoiler.LogicVariables.assumeInfiniteCoins = True  # This means we don't have to worry about moves required to get coins - we already know there is no breaking purchase order
    spoiler.LogicVariables.assumeKRoolAccess = True  # This makes the K. Rool path better if we need it
    if spoiler.settings.shuffle_loading_zones != ShuffleLoadingZones.all:
        # These assumptions are only good in level order because entrances can matter more in LZR
        spoiler.LogicVariables.assumeAztecEntry = True
        spoiler.LogicVariables.assumeLevel4Entry = True
        spoiler.LogicVariables.assumeUpperIslesAccess = True
        spoiler.settings.open_lobbies = True
        # If it's not Helm in upper Krem Isle, then assume you have access to this level as soon as you have the keys, bypassing the move needed to get up there.
        if spoiler.settings.shuffle_helm_location:
            spoiler.LogicVariables.assumeLevel8Entry = True  # Do not ever assume this in LZR! It makes a specific entrance one-way to work.

    # Identify important locations we might want to find the paths to
    # Filter out the items that are never WotH
    filtered_major_items = [
        item
        for item in MajorItems
        if ItemList[item].type
        not in (
            Types.Banana,
            Types.BlueprintBanana,
            Types.Crown,
            Types.Medal,
            Types.Blueprint,
            Types.Fairy,
            Types.RainbowCoin,
            Types.CrateItem,
            Types.Enemies,
        )
    ]
    interesting_locations = []
    for id, location in spoiler.LocationList.items():
        if not location.inaccessible and location.item in filtered_major_items:
            interesting_locations.append(id)
    interesting_locations.append(Locations.BananaHoard)
    # If intentionally starting with a slam, don't count it for paths
    if spoiler.settings.start_with_slam:
        interesting_locations.remove(Locations.IslesFirstMove)
    # Starting shop owners should not be on paths - only shop owners can be in these locations
    if Locations.ShopOwner_Location00 in interesting_locations:
        interesting_locations.remove(Locations.ShopOwner_Location00)
    if Locations.ShopOwner_Location01 in interesting_locations:
        interesting_locations.remove(Locations.ShopOwner_Location01)
    if Locations.ShopOwner_Location02 in interesting_locations:
        interesting_locations.remove(Locations.ShopOwner_Location02)
    if Locations.ShopOwner_Location03 in interesting_locations:
        interesting_locations.remove(Locations.ShopOwner_Location03)

    ordered_interesting_locations = []
    # Prep the dictionaries that will contain the paths to our interesting locations
    for locationId in WothLocations:
        spoiler.woth_paths[locationId] = [locationId]  # The endpoint is on its own path
        ordered_interesting_locations.append(locationId)  # Keeping WotH locations in order makes paths MUCH easier to read
    for locationId in interesting_locations:
        if locationId not in WothLocations:
            spoiler.other_paths[locationId] = [locationId]
            ordered_interesting_locations.append(locationId)

    # If K. Rool is the win condition, prepare phase-specific paths as well
    if spoiler.settings.win_condition_item == WinConditionComplex.beat_krool:
        for phase in spoiler.settings.krool_order:
            spoiler.krool_paths[phase] = []
    for locationId in ordered_interesting_locations:
        # Remove the item from the location
        location = spoiler.LocationList[locationId]
        item_id = location.item
        location.item = None
        # We also need to assume Kongs in order to get a "pure" path instead of Kong paths being a subset of most later paths.
        # Anything locked behind a a Kong will then require everything that Kong requires.
        # This sort of defeats the purpose of paths, as it would put everything in a Kong's path into the path of many, many items.
        assumedItems = ItemPool.Kongs(spoiler.settings)
        # Find all accessible locations without this item placed
        spoiler.Reset()
        accessible = GetAccessibleLocations(spoiler, assumedItems, SearchMode.GetReachable)
        # Then check every other WotH location for accessibility
        for other_location in WothLocations:
            # If it is no longer accessible, then this location is on the path of that other location
            if other_location not in accessible:
                spoiler.woth_paths[other_location].append(locationId)
        for other_location in spoiler.other_paths.keys():
            if other_location not in accessible:
                spoiler.other_paths[other_location].append(locationId)
        # If the win condition is K. Rool, also add this location to those paths as applicable
        if spoiler.settings.win_condition_item == WinConditionComplex.beat_krool:
            final_boss_associated_event = {
                Maps.JapesBoss: Events.KRoolDillo1,
                Maps.AztecBoss: Events.KRoolDog1,
                Maps.FactoryBoss: Events.KRoolJack,
                Maps.GalleonBoss: Events.KRoolPufftoss,
                Maps.FungiBoss: Events.KRoolDog2,
                Maps.CavesBoss: Events.KRoolDillo2,
                Maps.CastleBoss: Events.KRoolKKO,
                Maps.KroolDonkeyPhase: Events.KRoolDonkey,
                Maps.KroolDiddyPhase: Events.KRoolDiddy,
                Maps.KroolLankyPhase: Events.KRoolLanky,
                Maps.KroolTinyPhase: Events.KRoolTiny,
                Maps.KroolChunkyPhase: Events.KRoolChunky,
            }
            for map_id in final_boss_associated_event:
                if map_id in spoiler.settings.krool_order and final_boss_associated_event[map_id] not in spoiler.LogicVariables.Events:
                    spoiler.krool_paths[map_id].append(locationId)
        elif spoiler.settings.win_condition_item == WinConditionComplex.dk_rap_items:
            rap_assoc_name = {
                "Donkey Verse": Events.DonkeyVerse,
                "Diddy Verse": Events.DiddyVerse,
                "Lanky Verse": Events.LankyVerse,
                "Tiny Verse": Events.TinyVerse,
                "Chunky Verse": Events.ChunkyVerse,
                "The Fridge": Events.FridgeVerse,
            }
            for verse_name in rap_assoc_name:
                if verse_name not in spoiler.rap_win_con_paths:
                    spoiler.rap_win_con_paths[verse_name] = []
                if rap_assoc_name[verse_name] not in spoiler.LogicVariables.Events:
                    spoiler.rap_win_con_paths[verse_name].append(locationId)
        # Put the item back for future calculations
        location.PlaceItem(spoiler, item_id)
    # After everything is calculated, get rid of paths for false WotH locations
    # If an item doesn't show up on any other paths, it's not actually WotH
    # This is rare, but could happen if the item at the location is needed for coins or B. Lockers - it's often required, but not helpful to hint at all
    anything_removed = True
    while anything_removed:
        anything_removed = False
        # Check every WotH location
        for locationId in WothLocations:
            location = spoiler.LocationList[locationId]
            # If this item doesn't normally show up on paths but is definitely needed, no need to calculate it, it's definitely WotH
            if location.item in assumedItems or location.item == Items.BananaHoard:
                continue
            # Check every other path to see if this location is on any other path
            inAnotherPath = False
            for otherLocationId in [loc for loc in WothLocations if loc != locationId]:
                if locationId in spoiler.woth_paths[otherLocationId]:
                    inAnotherPath = True
                    break
            # If it's not on any other path, it's not WotH
            if not inAnotherPath:
                # In Chaos B. Lockers, you may need certain items purely to pass B. Locker
                if spoiler.settings.chaos_blockers:
                    # Most likely: The Bean is always required to pass the Bean Locker - if it gets here, that means you need it and it should be WotH
                    if location.item == Items.Bean and BarrierItems.Bean in spoiler.settings.BLockerEntryItems:
                        continue
                    # Less likely: Either of the two company coins could be strictly required due to items inside the levels they lock leading to the other one
                    if location.item in (Items.NintendoCoin, Items.RarewareCoin) and BarrierItems.CompanyCoin in spoiler.settings.BLockerEntryItems:
                        continue
                    # Even less likely: Pearls are in the same boat as the company coins, but there's 5 of them so it's considerably less likely to get here
                    if location.item == Items.Pearl and BarrierItems.Pearl in spoiler.settings.BLockerEntryItems:
                        continue
                # Keys that make it here are also always WotH
                if location.item in ItemPool.Keys():
                    continue
                # We do need to double check our work sometimes - this item might be required to beat the game if it's needed to get into a level
                # Only do this double-checking outside of LZR. The assumptions blocking level entry in LZR are less burdened with assumptions, so it's more likely to be accurate on the first pass.
                skipDoubleCheck = spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.all
                doubleCheckBeatsGame = False
                if not skipDoubleCheck:
                    spoiler.LogicVariables.assumeAztecEntry = False
                    spoiler.LogicVariables.assumeLevel4Entry = False
                    spoiler.LogicVariables.assumeLevel8Entry = False
                    spoiler.LogicVariables.assumeUpperIslesAccess = False
                    spoiler.LogicVariables.assumeKRoolAccess = False  # This item may also be needed to access K. Rool because of the aforementioned level entry
                    # Quickly check beatability after deleting this item - does removing this item make the game unbeatable?
                    spoiler.Reset()
                    item = location.item
                    location.item = None
                    # We still assume Kongs here!
                    assumedItems = ItemPool.Kongs(spoiler.settings)
                    if item in assumedItems:  # Except for if it's the item we're testing
                        assumedItems.remove(item)
                    # Check if we still have every woth location
                    accessibleItems = GetAccessibleLocations(spoiler, assumedItems, SearchMode.GetReachable)
                    inaccessibleWoths = [loc for loc in WothLocations if loc not in accessibleItems]
                    if not any(inaccessibleWoths):
                        doubleCheckBeatsGame = True
                    location.PlaceItem(spoiler, item)
                # If the game is still beatable when banned with the other assumptions (or if we're skipping the double checking), this item is definitely not WotH
                if skipDoubleCheck or doubleCheckBeatsGame:
                    WothLocations.remove(locationId)
                    spoiler.other_paths[locationId] = spoiler.woth_paths[locationId]
                    del spoiler.woth_paths[locationId]
                    # If we remove anything, we have to check the whole list again
                    anything_removed = True
                    break
    # None of these assumptions should ever make it out of this method
    spoiler.LogicVariables.assumePaidBLockers = False
    spoiler.LogicVariables.assumeInfiniteCoins = False
    spoiler.LogicVariables.assumeAztecEntry = False
    spoiler.LogicVariables.assumeLevel4Entry = False
    spoiler.LogicVariables.assumeLevel8Entry = False
    spoiler.LogicVariables.assumeUpperIslesAccess = False
    spoiler.LogicVariables.assumeKRoolAccess = False
    spoiler.settings.open_lobbies = old_open_lobbies_temp  # Undo the open lobbies setting change as needed

    # Confirm that all paths that should have at least one item on them do. This sidesteps an unsolved mystery issue where sometimes paths inexplicably end up empty.
    # This should never happen, but it's *really* bad if it does, so this quickly double checks the work.
    for goal, path in spoiler.woth_paths.items():
        if len(path) < 1:
            raise Ex.FillException("Rare path calculation error - report this to the devs with your settings string. Error code PL-1")
    for goal, path in spoiler.krool_paths.items():
        if len(path) < 1:
            # Some K. Rool fights are expected to have no items on the path
            expectedEmptyPathPhases = [Maps.GalleonBoss]  # Galleon boss never requires an item
            # Castle boss requires items only with lava water
            if not spoiler.LogicVariables.IsLavaWater():
                expectedEmptyPathPhases.append(Maps.CastleBoss)
            # DK Phase sometimes needs blast and always needs climbing, but the climbing isn't relevant unless it's shuffled
            if not spoiler.settings.cannons_require_blast and Types.Climbing not in spoiler.settings.shuffled_location_types:
                expectedEmptyPathPhases.append(Maps.KroolDonkeyPhase)
            # If your training moves are unshuffled, they don't end up on paths. All the Barrels-only bosses no longer have any path requirements.
            if spoiler.settings.training_barrels == TrainingBarrels.normal:
                expectedEmptyPathPhases.extend([Maps.JapesBoss, Maps.AztecBoss, Maps.CavesBoss])
            if goal not in expectedEmptyPathPhases:
                raise Ex.FillException("Rare path calculation error - report this to the devs with your settings string. Error code PL-2")
    for goal, path in spoiler.rap_win_con_paths.items():
        if len(path) < 1:
            # One verse is sometimes expected to have no items on the path
            expectedEmptyPathVerses = []
            # If your training moves are unshuffled, they don't end up on paths. Chunky Verse only requires barrels, so it no longer has any path requirements.
            if spoiler.settings.training_barrels == TrainingBarrels.normal:
                expectedEmptyPathVerses.append(Events.ChunkyVerse)
            if rap_assoc_name[goal] not in expectedEmptyPathVerses:
                raise Ex.FillException("Rare path calculation error - report this to the devs with your settings string. Error code PL-3")


def CalculateFoolish(spoiler: Spoiler, WothLocations: List[Union[Locations, int]], MajorItems: List[Items]) -> None:
    """Calculate the items and regions that are foolish (blocking no major items)."""
    # Identify the items that count for potion hinting hints
    regionCountHintableItems = ItemPool.AllKongMoves()
    regionCountHintableItems.extend(ItemPool.JunkSharedMoves)
    if spoiler.settings.training_barrels != TrainingBarrels.normal:
        regionCountHintableItems.extend(ItemPool.TrainingBarrelAbilities())
    if spoiler.settings.climbing_status != ClimbingStatus.normal:
        regionCountHintableItems.extend(ItemPool.ClimbingAbilities())
    if spoiler.settings.shockwave_status != ShockwaveStatus.shuffled_decoupled and spoiler.settings.shockwave_status != ShockwaveStatus.start_with:
        regionCountHintableItems.append(Items.CameraAndShockwave)
    if spoiler.settings.shockwave_status == ShockwaveStatus.shuffled_decoupled and spoiler.settings.shockwave_status != ShockwaveStatus.start_with:
        regionCountHintableItems.append(Items.Shockwave)
        regionCountHintableItems.append(Items.Camera)

    # These regions never have anything useful or are otherwise accounted for in the hints and shouldn't be hinted
    neverHintableNames = {
        HintRegion.GameStart,
        HintRegion.KRool,
        HintRegion.Error,
        HintRegion.Credits,
        HintRegion.Jetpac,
    }
    nonHintableNames = {HintRegion.GameStart, HintRegion.KRool, HintRegion.Error, HintRegion.Credits, HintRegion.Jetpac}
    if not IsItemSelected(spoiler.settings.cb_rando_enabled, spoiler.settings.cb_rando_list_selected, Levels.DKIsles):
        # Disable hinting this if CBs aren't in Isles. Obviously Isles CBs would be foolish if there's no CBs to get
        nonHintableNames.add(HintRegion.IslesCBs)
    spoiler.region_hintable_count = {}
    bossLocations = [location for id, location in spoiler.LocationList.items() if location.type == Types.Key]
    # In order for a region to be foolish, it can contain none of these Major Items
    for id, region in spoiler.RegionList.items():
        locations = [spoiler.LocationList[loc.id] for loc in region.locations if loc.id in spoiler.LocationList.keys() and not loc.isAuxiliaryLocation]
        # If this region's valid locations (exclude starting moves) DO contain a major item, add it the name to the set of non-hintable hint regions
        if any([loc for loc in locations if loc.type not in (Types.TrainingBarrel, Types.PreGivenMove, Types.Climbing) and loc.item in MajorItems]):
            nonHintableNames.add(region.hint_name)
        # In addition to being empty, medal regions need the corresponding boss location to be empty to be hinted foolish - this lets us say "CBs are foolish" which is more helpful
        elif region.isMedalRegion() and region.level not in (Levels.DKIsles, Levels.HideoutHelm):
            bossLocation = [location for location in bossLocations if location.level == region.level][0]  # Matches only one
            if bossLocation.item in MajorItems:
                nonHintableNames.add(region.hint_name)
        # Ban shops from region count hinting. These are significantly worse regions to hint than any others.
        if not region.isShopRegion() and region.hint_name not in neverHintableNames:
            # Count the number of region count hintable items in the region (again, ignore training moves)
            regionItemCount = sum(1 for loc in locations if loc.type not in (Types.TrainingBarrel, Types.PreGivenMove, Types.Climbing) and loc.item in regionCountHintableItems)
            if regionItemCount > 0:
                # If we need to create a new entry due to this region, do so
                if region.hint_name not in spoiler.region_hintable_count.keys():
                    spoiler.region_hintable_count[region.hint_name] = 0
                # Keep a running tally of found vials in each region
                spoiler.region_hintable_count[region.hint_name] += regionItemCount
    # The regions that are foolish are all regions not in this list (that have locations in them!)
    spoiler.foolish_region_names = list(set([region.hint_name for id, region in spoiler.RegionList.items() if any(region.locations) and region.hint_name not in nonHintableNames]))

    # Determine non-path items (foolish v2)
    # Non-path items are items that are not on the path to anything. This is similar but different to a foolish hint, so the phrasing on the hint will be different.
    wothItems = [spoiler.LocationList[loc].item for loc in WothLocations]
    # First we need to determine what Major Items are interesting - this is basically just all Kong moves
    spoiler.pathless_moves = []
    shuffledPotionItems = set(ItemPool.AllKongMoves())
    if spoiler.settings.training_barrels != TrainingBarrels.normal:  # If the training barrels aren't shuffled, they don't end up in the WotH so watch out
        shuffledPotionItems.update(ItemPool.TrainingBarrelAbilities())
    if spoiler.settings.climbing_status != ClimbingStatus.normal:
        shuffledPotionItems.update(ItemPool.ClimbingAbilities())
    if spoiler.settings.shockwave_status not in (ShockwaveStatus.start_with, ShockwaveStatus.shuffled_decoupled):
        shuffledPotionItems.add(Items.CameraAndShockwave)
    elif spoiler.settings.shockwave_status == ShockwaveStatus.shuffled_decoupled:
        shuffledPotionItems.add(Items.Shockwave)
        shuffledPotionItems.add(Items.Camera)
    # Some items aren't WotH but are frequently a part of either/or scenarios. The paths to these items should also be considered by "pathless" hints.
    interesting_non_woth_items = [Items.Bean, Items.Pearl, Items.NintendoCoin, Items.RarewareCoin]
    # If you start with a slam and have 0 WotH slams OR you don't start with a slam and have 0-1 WotH slams
    if (spoiler.settings.start_with_slam and Items.ProgressiveSlam not in wothItems) or (not spoiler.settings.start_with_slam and wothItems.count(Items.ProgressiveSlam) <= 1):
        # That means two slams are unhintable and we must account for the paths to the unhinted slams
        interesting_non_woth_items.append(Items.ProgressiveSlam)
    # With lava water, 3rd melon is very often required but falls into the same pitfalls as progressive slams
    if IsItemSelected(spoiler.settings.hard_mode, spoiler.settings.hard_mode_selected, HardModeSelected.water_is_lava, False):
        interesting_non_woth_items.append(Items.ProgressiveInstrumentUpgrade)
    # Note down all the items on these interesting non-WotH paths
    items_on_interesting_non_woth_paths = set()
    for path_location in spoiler.other_paths.keys():
        # If this path is to an interesting non-WotH item, note down every item on this path
        if spoiler.LocationList[path_location].item in interesting_non_woth_items:
            items_on_interesting_non_woth_paths.update(set([spoiler.LocationList[loc].item for loc in spoiler.other_paths[path_location]]))
    for item in shuffledPotionItems:
        # If this item is in the WotH, it can't possibly be foolish
        if item in wothItems:
            continue
        # If this item is on an interesting non-WotH path, it is treated as not pathless
        elif item in items_on_interesting_non_woth_paths:
            continue
        spoiler.pathless_moves.append(item)
    # Saying slams aren't on the path to anything is usually utterly useless due to the progressive nature. I'm not even gonna try to pretend to make these work.
    while Items.ProgressiveSlam in spoiler.pathless_moves:
        spoiler.pathless_moves.remove(Items.ProgressiveSlam)
    # Similarly, progressive instrument upgrades are also a nightmare for pathless - BEGONE
    if IsItemSelected(spoiler.settings.hard_mode, spoiler.settings.hard_mode_selected, HardModeSelected.water_is_lava, False):
        while Items.ProgressiveInstrumentUpgrade in spoiler.pathless_moves:
            spoiler.pathless_moves.remove(Items.ProgressiveInstrumentUpgrade)


def RandomFill(spoiler: Spoiler, itemsToPlace: List[Items], inOrder: bool = False) -> int:
    """Randomly place given items in any location disregarding logic."""
    settings = spoiler.settings
    if not inOrder:
        spoiler.settings.random.shuffle(itemsToPlace)
    # Get all remaining empty locations
    empty = []
    for id, location in spoiler.LocationList.items():
        if location.item is None:
            empty.append(id)
    # Place item in random locations
    while len(itemsToPlace) > 0:
        item = itemsToPlace.pop()
        validLocations = settings.GetValidLocationsForItem(item)
        itemEmpty = [x for x in empty if x in validLocations and spoiler.LocationList[x].item is None and not spoiler.LocationList[x].inaccessible]
        if len(itemEmpty) == 0:
            if settings.extreme_debugging:
                # Debugging variables: they are unaccessed but certainly useful. Do not touch!
                invalid_empty_reachable = [x for x in itemEmpty if x not in validLocations]
                empty_locations = [x for x in spoiler.LocationList.values() if x.item is None]
                accessible_empty_locations = [x for x in empty_locations if not x.inaccessible]
                noitem_locations = [x for x in spoiler.LocationList.values() if x.type != Types.Shop and x.item is Items.NoItem]
            return len(itemsToPlace) + 1
        spoiler.settings.random.shuffle(itemEmpty)
        locationId = itemEmpty.pop()
        spoiler.LocationList[locationId].PlaceItem(spoiler, item)
        empty.remove(locationId)
        if locationId in SharedShopLocations:
            settings.placed_shared_shops += 1
            if settings.placed_shared_shops >= settings.max_shared_shops:
                BanAllRemainingSharedShops(spoiler)
                # Have to recalculate empty after filling additional locations
                empty = []
                for id, location in spoiler.LocationList.items():
                    if location.item is None:
                        empty.append(id)
    return 0


def CarefulRandomFill(spoiler: Spoiler, itemsToPlace: List[Union[Any, Items]], ownedItems: Optional[List[Union[Any, Items]]] = None) -> int:
    """Randomly place items, but try to keep shops in mind. Expected to be faster than forward fill for large quantities of items but slower than random fill."""
    spoiler.Reset()
    settings = spoiler.settings
    # This method assumes you know that whatever you're trying to place can be placed nearly entirely randomly.
    owned = ownedItems.copy()
    # That means you can assume you own all the things you're about to place with no consequence
    owned.extend(itemsToPlace)
    reachable = GetAccessibleLocations(spoiler, owned, SearchMode.GetReachableForFilling)
    # Place items randomly in the accessible locations
    spoiler.settings.random.shuffle(itemsToPlace)
    while len(itemsToPlace) > 0:
        item = itemsToPlace.pop()
        validLocations = settings.GetValidLocationsForItem(item)
        itemEmpty = [x for x in reachable if x in validLocations and spoiler.LocationList[x].item is None and not spoiler.LocationList[x].inaccessible]
        if len(itemEmpty) == 0:
            if settings.extreme_debugging:
                # Debugging variables: they are unaccessed but certainly useful. Do not touch!
                invalid_empty_reachable = [x for x in itemEmpty if x not in validLocations]
                empty_locations = [x for x in spoiler.LocationList.values() if x.item is None]
                accessible_empty_locations = [x for x in empty_locations if not x.inaccessible]
                noitem_locations = [x for x in spoiler.LocationList.values() if x.type != Types.Shop and x.item is Items.NoItem]
            return len(itemsToPlace) + 1
        spoiler.settings.random.shuffle(itemEmpty)
        spoiler.settings.random.shuffle(itemEmpty)
        locationId = itemEmpty.pop()
        spoiler.LocationList[locationId].PlaceItem(spoiler, item)
        # If you hit a shop location, we have to do some stuff
        if spoiler.LocationList[locationId].type == Types.Shop:
            # Recalculate assumed items for what we've placed so far
            spoiler.Reset()
            owned = ownedItems.copy()
            owned.extend(itemsToPlace)
            # In higher price settings, we have to be extra careful with putting things in shops - adding a new item to a shop can disturb a fragile required purchase order
            if settings.random_prices in (RandomPrices.high, RandomPrices.extreme):
                # Check if we can still 101% the seed - this is costly to do for every shop location, but should improve the consistency of seed generation for higher-priced settings
                reached_all = GetAccessibleLocations(spoiler, owned, SearchMode.CheckAllReachable)
                if not reached_all:
                    # If we can't, we've established that this location cannot hold any items without causing a coin logic break
                    # This does not preclude the possibility of a coin logic failure later, just heavily reduces the odds
                    # This will, however, prevent failed 101% checks because of purchase orders
                    spoiler.LocationList[locationId].UnplaceItem(spoiler)
                    spoiler.LocationList[locationId].inaccessible = True
                    spoiler.LocationList[locationId].tooExpensiveInaccessible = True
                    itemsToPlace.append(item)
                    continue
            # Shared shops have to respect the shared shop limit
            if locationId in SharedShopLocations:
                settings.placed_shared_shops += 1
                if settings.placed_shared_shops >= settings.max_shared_shops:
                    BanAllRemainingSharedShops(spoiler)
            spoiler.Reset()
            reachable = GetAccessibleLocations(spoiler, owned, SearchMode.GetReachableForFilling)
            if settings.extreme_debugging:
                spoiler.Reset()
                reached_all = GetAccessibleLocations(spoiler, owned, SearchMode.CheckAllReachable)
                if not reached_all:
                    print("red alert - this item placement lost 101% somehow?")
                # Debugging variables
                item_placed_before_this_one = item
                location_placed_before_this_one = spoiler.LocationList[locationId]
    return 0


def ForwardFill(
    spoiler: Spoiler,
    itemsToPlace: List[Items],
    ownedItems: Optional[List[Items]] = None,
    inOrder: bool = False,
    doubleTime: bool = False,
) -> int:
    """Forward fill algorithm for item placement."""
    settings = spoiler.settings
    if ownedItems is None:
        ownedItems = []
    if not inOrder:
        spoiler.settings.random.shuffle(itemsToPlace)
    needToRefreshReachable = True
    # While there are items to place
    while len(itemsToPlace) > 0:
        # Get a random item
        item = itemsToPlace.pop(0)
        # In "doubleTime", only refresh the list of reachable locations every other item to reduce calls to this method - this should have minimal impact on randomization depending on the item filling here
        if not doubleTime or needToRefreshReachable:
            # Find a random empty location which is reachable with current items
            spoiler.Reset()
            reachable = GetAccessibleLocations(spoiler, ownedItems.copy(), SearchMode.GetReachableForFilling)
        validLocations = settings.GetValidLocationsForItem(item)
        validReachable = [x for x in reachable if spoiler.LocationList[x].item is None and x in validLocations]
        if len(validReachable) == 0:  # If there are no empty reachable locations, reached a dead end
            if settings.extreme_debugging:
                invalid_empty_reachable = [x for x in reachable if spoiler.LocationList[x].item is None and x not in validLocations]
                valid_empty = [x for x in spoiler.LocationList.keys() if spoiler.LocationList[x].item is None and x in validLocations]
            return len(itemsToPlace) + 1
        spoiler.settings.random.shuffle(validReachable)
        locationId = validReachable.pop()
        # Place the item
        spoiler.LocationList[locationId].PlaceItem(spoiler, item)
        # Debug code utility for very important items
        if item in ItemPool.HighPriorityItems(settings):
            settings.debug_fill[spoiler.LocationList[locationId].name] = item
        if item in ItemPool.Keys():
            settings.debug_fill[spoiler.LocationList[locationId].name] = item
        needToRefreshReachable = not needToRefreshReachable  # Alternate this variable every item for doubleTime
        # If you hit a shop location, we have to do some stuff
        if spoiler.LocationList[locationId].type == Types.Shop:
            # In higher price settings, we have to be extra careful with putting things in shops - adding a new item to a shop can disturb a fragile required purchase order
            if settings.random_prices in (RandomPrices.high, RandomPrices.extreme):
                # Check if we can still 101% the seed - this is costly to do for every shop location, but should improve the consistency of seed generation for higher-priced settings
                assumedItems = ownedItems.copy()
                assumedItems.extend(itemsToPlace)
                reached_all = GetAccessibleLocations(spoiler, assumedItems, SearchMode.CheckAllReachable)
                if not reached_all:
                    # If we can't, we've established that this location cannot hold any items without causing a coin logic break
                    # This does not preclude the possibility of a coin logic failure later, just heavily reduces the odds
                    # This will, however, prevent failed 101% checks because of purchase orders
                    spoiler.LocationList[locationId].UnplaceItem(spoiler)
                    spoiler.LocationList[locationId].inaccessible = True
                    spoiler.LocationList[locationId].tooExpensiveInaccessible = True
                    itemsToPlace.append(item)
                    continue
            # Shared shops must abide by the shared shop limit
            if locationId in SharedShopLocations:
                settings.placed_shared_shops += 1
                if settings.placed_shared_shops >= settings.max_shared_shops:
                    BanAllRemainingSharedShops(spoiler)
                    needToRefreshReachable = True
        if settings.extreme_debugging:
            spoiler.Reset()
            assumedItems = ownedItems.copy()
            assumedItems.extend(itemsToPlace)
            reached_all = GetAccessibleLocations(spoiler, assumedItems, SearchMode.CheckAllReachable)
            if not reached_all:
                print("red alert - this item placement lost 101% somehow?")
            item_placed_before_this_one = item
            location_placed_before_this_one = spoiler.LocationList[locationId]
    return 0


def GetItemValidLocations(spoiler: Spoiler, validLocations, item):
    """Get the list of valid locations for this item."""
    # If validLocations is a dictionary, check for this item's value
    itemValidLocations = validLocations
    if isinstance(validLocations, dict):
        for itemKey in validLocations.keys():
            if item == itemKey:
                itemValidLocations = validLocations[itemKey]
                break
            # Valid locations entry wasn't found
            itemValidLocations = list(spoiler.LocationList)
    return itemValidLocations


def AssumedFill(spoiler: Spoiler, itemsToPlace: List[Items], ownedItems: Optional[List[Items]] = None, inOrder: bool = False) -> int:
    """Assumed fill algorithm for item placement."""
    settings = spoiler.settings
    if ownedItems is None:
        ownedItems = []
    # While there are items to place
    if not inOrder:
        spoiler.settings.random.shuffle(itemsToPlace)
    while len(itemsToPlace) > 0:
        # Get a random item, check which empty locations are still accessible without owning it
        item = itemsToPlace.pop(0)
        itemShuffled = False
        owned = itemsToPlace.copy()
        owned.extend(ownedItems)

        itemValidLocations = settings.GetValidLocationsForItem(item)
        # Find all valid reachable locations for this item
        spoiler.Reset()
        reachable = GetAccessibleLocations(spoiler, owned, SearchMode.GetReachableForFilling)
        validReachable = [x for x in reachable if spoiler.LocationList[x].item is None and x in itemValidLocations]
        # If there are no empty reachable locations, reached a dead end
        if len(validReachable) == 0:
            print("Failed placing item " + ItemList[item].name + ", no valid reachable locations without this item.")
            currentKongsFreed = [ItemList[x].name for x in owned if ItemList[x].type == Types.Kong]
            startKongList = []
            for x in settings.starting_kong_list:
                startKongList.append(x.name.capitalize())
            for i, kong in enumerate(startKongList):
                currentKongsFreed.insert(i, kong)
            currentMovesOwned = [ItemList[x].name for x in owned if ItemList[x].type in (Types.Shop, Types.TrainingBarrel, Types.Shockwave, Types.Climbing)]
            currentGbCount = len([x for x in owned if ItemList[x].type == Types.Banana])
            js.postMessage("Current Moves owned at failure: " + str(currentMovesOwned) + " with GB count: " + str(currentGbCount) + " and kongs freed: " + str(currentKongsFreed))
            return len(itemsToPlace) + 1
        spoiler.settings.random.shuffle(validReachable)
        # Get a random, empty, reachable location
        for locationId in validReachable:
            # Atempt to place the item here
            spoiler.LocationList[locationId].PlaceItem(spoiler, item)
            if len(itemsToPlace) > 0:
                # If we have more items to placed, check valid reachable after placing to see if placing it here causes problems
                # Need to re-assign owned items since the search adds a bunch of extras
                owned = itemsToPlace.copy()
                owned.extend(ownedItems)
                spoiler.Reset()
                reachable = GetAccessibleLocations(spoiler, owned, SearchMode.GetReachableForFilling)
                valid = True
                # For each remaining item, ensure that it has a valid location reachable after placing this item
                for checkItem in itemsToPlace:
                    itemValid = settings.GetValidLocationsForItem(checkItem)
                    validReachable = [x for x in reachable if x in itemValid and x != locationId]
                    if len(validReachable) == 0:
                        js.postMessage("Failed placing item " + ItemList[item].name + " in location " + spoiler.LocationList[locationId].name + ", due to too few remaining locations in play")
                        valid = False
                        break
                    reachable.remove(validReachable[0])  # Remove one so same location can't be "used" twice
                # If world is not valid, undo item placement and try next location
                if not valid:
                    spoiler.LocationList[locationId].UnplaceItem(spoiler)
                    itemShuffled = False
                    continue
            # Debug code utility for very important items
            if item in ItemPool.HighPriorityItems(settings):
                settings.debug_fill[spoiler.LocationList[locationId].name] = item
            if item in ItemPool.Keys():
                settings.debug_fill[spoiler.LocationList[locationId].name] = item
            itemShuffled = True
            if locationId in SharedShopLocations:
                settings.placed_shared_shops += 1
                if settings.placed_shared_shops >= settings.max_shared_shops:
                    BanAllRemainingSharedShops(spoiler)
            break
        if not itemShuffled:
            js.postMessage("Failed placing item " + ItemList[item].name + " in any of remaining " + str(ItemList[item].type) + " type possible locations")
            return len(itemsToPlace) + 1
        elif settings.extreme_debugging:
            spoiler.Reset()
            reached_all = GetAccessibleLocations(spoiler, owned, SearchMode.CheckAllReachable)
            if not reached_all:
                print("red alert - this item placement lost 101% somehow?")
            item_placed_before_this_one = item
    return 0


def BanAllRemainingSharedShops(spoiler: Spoiler):
    """Fill all empty shared shops with a NoItem."""
    for location in SharedShopLocations:
        if not spoiler.LocationList[location].inaccessible and spoiler.LocationList[location].item is None:
            spoiler.LocationList[location].PlaceItem(spoiler, Items.NoItem)


def GetMaxCoinsSpent(spoiler: Spoiler, purchasedShops: List[Union[Any, Locations]]) -> List[int]:
    """Calculate the max number of coins each kong could have spent given the ownedItems and the price settings."""
    settings = spoiler.settings
    MaxCoinsSpent = [0, 0, 0, 0, 0, 0]
    slamLevel = 0
    ammoBelts = 0
    instUpgrades = 0
    for location_id in purchasedShops:
        location = spoiler.LocationList[location_id]
        if location.item == Items.ProgressiveSlam:
            movePrice = settings.prices[location.item][slamLevel]
            slamLevel += 1
        elif location.item == Items.ProgressiveAmmoBelt:
            movePrice = settings.prices[location.item][ammoBelts]
            ammoBelts += 1
        elif location.item == Items.ProgressiveInstrumentUpgrade:
            movePrice = settings.prices[location.item][instUpgrades]
            instUpgrades += 1
        elif settings.random_prices == RandomPrices.vanilla:
            movePrice = settings.prices[location.item]
        else:
            movePrice = settings.prices[location_id]
        if movePrice is not None:
            MaxCoinsSpent[location.kong] += movePrice
    # All shared moves add to the cost of each Kong
    for kong_index in range(5):
        MaxCoinsSpent[kong_index] += MaxCoinsSpent[int(Kongs.any)]
    MaxCoinsSpent.pop()  # Remove the shared total, as it was just for numbers keeping
    return MaxCoinsSpent


# @pp.profile_by_line()
def GetUnplacedItemPrerequisites(spoiler: Spoiler, targetItemId, placedMoves, ownedKongs=[]):
    """Given the target item and the current world state, find a valid, minimal, unplaced set of items required to reach the location it is in."""
    # Settings-required moves are always owned in order to complete this method based on the settings
    settingsRequiredMoves = ItemPool.AllItemsForMovePlacement(spoiler.settings)
    # The most likely case - if no moves are needed, get out of here quickly
    spoiler.Reset()
    if GetAccessibleLocations(spoiler, settingsRequiredMoves.copy(), SearchMode.CheckSpecificItemReachable, targetItemId=targetItemId):
        return []
    requiredMoves = []
    # Some locations can be accessed by multiple items, so we'll shuffle the order we check the items to randomly pick one of them first
    # We should have just placed this item, so it should be available with the provided list of owned kongs
    # We don't want to find requirements for Kongs we don't own, as we shouldn't need them
    #   e.g. You own DK, Diddy, and Tiny but want to find the prerequisites for an item found in the Llama temple
    #     You intentionally only look at DK/Diddy/Tiny moves so you don't find Grape as a prerequisite because you don't have Lanky
    #     In this example (with no other shuffles), there are two possible return values depending on the shuffle order.
    #     Either [Items.Guitar, Items.Coconut] OR [Items.Guitar, Items.Feather]
    moveList = [move for move in ItemPool.AllKongMoves()]  # I really want to pare this down quickly with ownedKongs, but it hurts the fill to do so
    # Sometimes a move requires camera or shockwave as a prerequisite
    if spoiler.settings.shockwave_status != ShockwaveStatus.vanilla:
        if spoiler.settings.shockwave_status == ShockwaveStatus.shuffled_decoupled:
            moveList.append(Items.Camera)
            moveList.append(Items.Shockwave)
        else:
            moveList.append(Items.CameraAndShockwave)
    # Often moves require training barrels as prerequisites
    if spoiler.settings.training_barrels != TrainingBarrels.normal:
        moveList.extend(ItemPool.TrainingBarrelAbilities())
    if spoiler.settings.climbing_status != ClimbingStatus.normal:
        moveList.extend(ItemPool.ClimbingAbilities())
    # We only want *unplaced* prerequisites, cull all placed moves from the move list
    for move in placedMoves:
        if move in moveList:
            moveList.remove(move)
    spoiler.settings.random.shuffle(moveList)
    itemWasFound = False
    # Every item in moveList could be a required item
    for i in range(0, len(moveList)):
        # Remove one item from the moveList
        possiblyUnnecessaryItem = moveList[i]
        moveList[i] = Items.NoItem
        # Check if the target is still accessible without this item
        spoiler.Reset()
        if not GetAccessibleLocations(
            spoiler,
            settingsRequiredMoves.copy() + moveList.copy(),
            SearchMode.CheckSpecificItemReachable,
            targetItemId=targetItemId,
        ):
            # If it's no longer accessible, then this item is required
            requiredMoves.append(possiblyUnnecessaryItem)
            # Restore the item to the move list ONLY if it's required - this will cover either/or items
            moveList[i] = possiblyUnnecessaryItem
        else:
            itemWasFound = True
    # If we didn't find a required move, the item was placed improperly somehow (this shouldn't happen)
    if not itemWasFound:
        # DEBUG CODE - This helps find where items are being placed
        mysteryLocation = None
        itemobj = ItemList[targetItemId]
        if type(spoiler.settings.valid_locations[itemobj.type]) is dict:
            for possibleLocationThisItemGotPlaced in spoiler.settings.valid_locations[itemobj.type][itemobj.kong]:
                if spoiler.LocationList[possibleLocationThisItemGotPlaced].item == targetItemId:
                    mysteryLocation = spoiler.LocationList[possibleLocationThisItemGotPlaced]
                    break
        else:
            for possibleLocationThisItemGotPlaced in spoiler.settings.valid_locations[itemobj.type]:
                if spoiler.LocationList[possibleLocationThisItemGotPlaced].item == targetItemId:
                    mysteryLocation = spoiler.LocationList[possibleLocationThisItemGotPlaced]
                    break
        if mysteryLocation is None:
            raise Ex.ItemPlacementException("Target item not placed??")
        # debug_reachable = GetAccessibleLocations(spoiler, settingsRequiredMoves.copy() + moveList.copy(), SearchMode.GetReachable)
        print("Item placed in an inaccessible location: " + str(mysteryLocation.name))
        raise Ex.ItemPlacementException("Item placed in an inaccessible location: " + str(mysteryLocation.name))

    spoiler.settings.debug_prerequisites[targetItemId] = requiredMoves
    return requiredMoves


def PlaceItems(
    spoiler: Spoiler,
    algorithm: FillAlgorithm,
    itemsToPlace: List[Union[Any, Items]],
    ownedItems: Optional[List[Union[Any, Items]]] = None,
    inOrder: bool = False,
    doubleTime: bool = False,
) -> int:
    """Places items using given algorithm."""
    if ownedItems is None:
        ownedItems = []
    # Always use random fill with no logic
    if spoiler.settings.logic_type == LogicType.nologic:
        algorithm = FillAlgorithm.random
    if algorithm == FillAlgorithm.assumed:
        return AssumedFill(spoiler, itemsToPlace, ownedItems, inOrder)
    elif algorithm == FillAlgorithm.forward:
        return ForwardFill(spoiler, itemsToPlace, ownedItems, inOrder, doubleTime)
    elif algorithm == FillAlgorithm.random:
        return RandomFill(spoiler, itemsToPlace, inOrder)
    elif algorithm == FillAlgorithm.careful_random:
        return CarefulRandomFill(spoiler, itemsToPlace, ownedItems)


def FillShuffledKeys(spoiler: Spoiler, placed_types: List[Types], placed_items: List[Items]) -> None:
    """Fill Keys in shuffled locations based on the settings."""
    keysToPlace = ItemPool.KeysToPlace(spoiler.settings)
    # Don't double-place keys
    for item in placed_items:
        if item in keysToPlace:
            keysToPlace.remove(item)
    # Level-agnostic key placement settings include...
    # - No logic (totally random)
    # - Loading Zone randomizer (key unlocks are typically of lesser importance)
    # - Complex level progression (key order is non-linear)
    if spoiler.settings.logic_type == LogicType.nologic or spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.all or spoiler.settings.hard_level_progression:
        # Assumed fills tend to place multiple keys at once better
        keyAlgorithm = FillAlgorithm.assumed
        if spoiler.settings.logic_type == LogicType.nologic:  # Obviously no logic gets random fills
            keyAlgorithm = FillAlgorithm.random
        # Place all the keys
        keysUnplaced = PlaceItems(spoiler, keyAlgorithm, keysToPlace, ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types))
        if keysUnplaced > 0:
            raise Ex.ItemPlacementException(str(keysUnplaced) + " unplaced keys.")
    # # Simple linear level order progression leads to straightforward key placement
    else:
        # If Helm is not last, and we're locking key 8 and we're using the SLO ruleset,
        # place Key 8 in the 8th level somewhere
        if Items.HideoutHelmKey in keysToPlace and spoiler.settings.key_8_helm:
            last_level = spoiler.settings.level_order[8]
            if last_level != Levels.HideoutHelm:
                if spoiler.settings.shuffle_items:
                    potential_locations = [
                        loc
                        for loc in spoiler.LocationList
                        if spoiler.LocationList[loc].level == last_level
                        and spoiler.LocationList[loc].type in spoiler.settings.shuffled_location_types
                        and not spoiler.LocationList[loc].inaccessible
                        and loc in spoiler.settings.GetValidLocationsForItem(Items.HideoutHelmKey)
                    ]
                # Outside of item rando, the only eligible location is the boss in level 8. This should filter down to only one location.
                else:
                    potential_locations = [loc for loc in spoiler.LocationList if spoiler.LocationList[loc].level == last_level and spoiler.LocationList[loc].type == Types.Key]
                selected_location = spoiler.settings.random.choice(potential_locations)
                spoiler.LocationList[selected_location].PlaceItem(spoiler, Items.HideoutHelmKey)
                keysToPlace.remove(Items.HideoutHelmKey)
        # Place the keys in order
        keysToPlace.sort()
        keysUnplaced = PlaceItems(
            spoiler,
            spoiler.settings.algorithm,
            keysToPlace,
            ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types),
            inOrder=True,
        )
        if keysUnplaced > 0:
            raise Ex.ItemPlacementException(str(keysUnplaced) + " unplaced keys.")


def FillHelmLocations(spoiler: Spoiler, placed_types: List[Types], placed_items: List[Items]) -> List[Items]:
    """Fill all currently empty (non-enemy!) Helm locations with eligible unplaced items."""
    placed_in_helm = []
    # Get all the empty Helm locations
    empty_helm_locations = [
        loc_id
        for loc_id in spoiler.LocationList.keys()
        if spoiler.LocationList[loc_id].level == Levels.HideoutHelm and spoiler.LocationList[loc_id].type not in (Types.Constant, Types.Enemies) and spoiler.LocationList[loc_id].item is None
    ]
    # Make sure hints don't get placed, if progressive hints are enabled
    if spoiler.settings.progressive_hint_item != ProgressiveHintItem.off:
        placed_types.append(Types.Hint)
    # Rig the valid_locations for all relevant items to only be able to place things in Helm
    for typ in [x for x in spoiler.settings.shuffled_location_types if x not in placed_types]:  # Shops would already be placed
        # Filter the valid locations down to only Helm locations
        # Blueprints are tricky - their valid locations are organized by Kong
        if typ == Types.Blueprint:
            for kong in GetKongs():
                spoiler.settings.valid_locations[Types.Blueprint][kong] = [
                    loc for loc in spoiler.settings.valid_locations[Types.Blueprint][kong] if spoiler.LocationList[loc].level == Levels.HideoutHelm and loc in empty_helm_locations
                ]
        # Everything else can be in any Helm location they already could have been in depending on their type
        elif typ in spoiler.settings.valid_locations.keys():
            spoiler.settings.valid_locations[typ] = [loc for loc in spoiler.settings.valid_locations[typ] if spoiler.LocationList[loc].level == Levels.HideoutHelm and loc in empty_helm_locations]
        # Anything that falls out of this else is a type that doesn't have valid locations (ToughBanana, etc.)
    # Now we get the full list of items we could place here
    unplaced_items = ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types)
    for item in placed_items:
        if item in unplaced_items:
            unplaced_items.remove(item)
    debug_failed_to_place_items = []
    possible_items = [item for item in unplaced_items if item != Items.GoldenBanana]  # To save some time, we know GBs can't be in Helm
    spoiler.settings.random.shuffle(possible_items)
    # Until we have placed enough items...
    while len(placed_in_helm) < len(empty_helm_locations):
        if len(possible_items) == 0:
            spoiler.settings.update_valid_locations(spoiler)
            raise Ex.FillException("Unable to fill Helm.")
        # Grab the next one from the pile and attempt to place it
        item_to_attempt_placement = possible_items.pop()
        unplaced_items.remove(item_to_attempt_placement)
        spoiler.Reset()
        unplaced = PlaceItems(spoiler, FillAlgorithm.forward, [item_to_attempt_placement], unplaced_items)
        # If we succeed, mark this item as being placed in Helm
        if unplaced == 0:
            placed_in_helm.append(item_to_attempt_placement)
        # If we failed, go again. This is most likely either a location conflict inherent to the item or a logical restriction based on a huge Fairy/Medal requirement
        else:
            debug_failed_to_place_items.append(item_to_attempt_placement)  # This item we failed to place could be important earlier, so we need to assume it going forward
            unplaced_items.append(item_to_attempt_placement)
    # Very important - we have to reset valid_locations to the correct state after this
    spoiler.settings.update_valid_locations(spoiler)
    # Return all items we placed, all future methods must consider these when placing (and assuming) items
    return placed_in_helm


def FillBossLocations(spoiler: Spoiler, placed_types: List[Types], placed_items: List[Items]) -> List[Items]:
    """Fill all currently empty Boss locations with eligible unplaced items."""
    placed_on_bosses = []
    # Get all the empty boss locations
    empty_boss_locations = [
        loc_id
        for loc_id in spoiler.LocationList.keys()
        if spoiler.LocationList[loc_id].level != Levels.HideoutHelm and spoiler.LocationList[loc_id].type == Types.Key and spoiler.LocationList[loc_id].item is None
    ]
    # Make sure hints don't get placed, if progressive hints are enabled
    if spoiler.settings.progressive_hint_item != ProgressiveHintItem.off:
        placed_types.append(Types.Hint)
    # Rig the valid_locations for all relevant items to only be able to place things on bosses
    for typ in [x for x in spoiler.settings.shuffled_location_types if x not in placed_types]:  # Shops would already be placed
        # Any item eligible to be on a boss can be on any boss
        spoiler.settings.valid_locations[typ] = empty_boss_locations
    # Now we get the full list of items we could place here
    unplaced_items = ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types)
    # Checkless can be on bosses, but we need shops in the pool in order to have room to do this reliably
    if Types.Shop in spoiler.settings.shuffled_location_types and Types.FakeItem in spoiler.settings.shuffled_location_types:
        unplaced_items.extend(ItemPool.FakeItems(spoiler.settings))
    for item in placed_items:
        if item in unplaced_items:
            unplaced_items.remove(item)
    debug_failed_to_place_items = []
    possible_items = [item for item in unplaced_items if item < Items.JungleJapesDonkeyBlueprint or item > Items.DKIslesChunkyBlueprint]  # To save some time, we know blueprints can't be on bosses
    spoiler.settings.random.shuffle(possible_items)
    # Until we have placed enough items...
    while len(placed_on_bosses) < len(empty_boss_locations):
        if len(possible_items) == 0:
            spoiler.settings.update_valid_locations(spoiler)
            raise Ex.FillException("Unable to find all locations during the fill. Error code: BS-1")
        # Grab the next one from the pile and attempt to place it
        item_to_attempt_placement = possible_items.pop()
        unplaced_items.remove(item_to_attempt_placement)
        spoiler.Reset()
        unplaced = PlaceItems(spoiler, FillAlgorithm.forward, [item_to_attempt_placement], unplaced_items)
        # If we succeed, mark this item as being placed in Helm
        if unplaced == 0:
            placed_on_bosses.append(item_to_attempt_placement)
        # If we failed, go again. This would be really surprising to ever happen, as boss accessibility is only calculated post-fill. Maybe in plando?
        else:
            debug_failed_to_place_items.append(item_to_attempt_placement)  # Apparently the item we failed to place is important earlier, so we need to assume it going forward
            unplaced_items.append(item_to_attempt_placement)
    # Very important - we have to reset valid_locations to the correct state after this
    spoiler.settings.update_valid_locations(spoiler)
    # Return all items we placed, all future methods must consider these when placing (and assuming) items
    return placed_on_bosses


def Fill(spoiler: Spoiler) -> None:
    """Fully randomizes and places all items."""
    placed_types = []
    spoiler.settings.debug_fill = {}
    spoiler.settings.debug_prerequisites = {}
    spoiler.settings.debug_fill_blueprints = {}
    spoiler.settings.placed_shared_shops = 0
    # First place constant items - these will never vary and need to be in place for all other fills to know that
    ItemPool.PlaceConstants(spoiler)
    preplaced_items = spoiler.settings.plandomizer_items_placed

    # Place rainbow coins before all randomly placed items so that we have coins set in stone for the other fills
    # It's possible that shops could overload if we continue assuming rainbow coins for too many fills
    if Types.RainbowCoin in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.RainbowCoin)
        spoiler.Reset()
        rainbowCoinsToPlace = ItemPool.RainbowCoinItems().copy()
        for item in preplaced_items:
            if item in rainbowCoinsToPlace:
                rainbowCoinsToPlace.remove(item)
        rcoinUnplaced = PlaceItems(
            spoiler,
            FillAlgorithm.random,
            rainbowCoinsToPlace,
            ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
        )
        if rcoinUnplaced > 0:
            raise Ex.ItemPlacementException("Unable to find all locations during the fill. Error code: RC-" + str(rcoinUnplaced))
    if spoiler.settings.extreme_debugging:
        DebugCheckAllReachable(
            spoiler,
            ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
            "Rainbow Coins",
        )

    if spoiler.settings.shuffle_items and Types.Shop in spoiler.settings.shuffled_location_types:
        if spoiler.settings.kong_rando:
            FillKongs(spoiler, placed_types, preplaced_items)
        if spoiler.settings.extreme_debugging:
            DebugCheckAllReachable(
                spoiler,
                ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
                "Kongs",
            )
        preplaced_items.extend([Items.Donkey, Items.Diddy, Items.Lanky, Items.Tiny, Items.Chunky])
        preplaced_items.extend(FillTrainingMoves(spoiler, preplaced_items))
        placed_types.append(Types.Shop)
        placed_types.append(Types.TrainingBarrel)
        placed_types.append(Types.Climbing)
        placed_types.append(Types.Shockwave)
        placed_types.append(Types.Key)
        bigListOfItemsToPlace = []
        if Types.Shop in spoiler.settings.shuffled_location_types:
            bigListOfItemsToPlace.extend(ItemPool.ImportantSharedMoves.copy())
            bigListOfItemsToPlace.extend(ItemPool.JunkSharedMoves.copy())
            bigListOfItemsToPlace.extend(ItemPool.DonkeyMoves)
            bigListOfItemsToPlace.extend(ItemPool.DiddyMoves)
            bigListOfItemsToPlace.extend(ItemPool.LankyMoves)
            bigListOfItemsToPlace.extend(ItemPool.TinyMoves)
            bigListOfItemsToPlace.extend(ItemPool.ChunkyMoves)
            if spoiler.settings.training_barrels != TrainingBarrels.normal:
                bigListOfItemsToPlace.extend(ItemPool.TrainingBarrelAbilities())
            if spoiler.settings.climbing_status != ClimbingStatus.normal:
                bigListOfItemsToPlace.extend(ItemPool.ClimbingAbilities())
        if spoiler.settings.shockwave_status != ShockwaveStatus.start_with and Types.Shockwave in spoiler.settings.shuffled_location_types:
            bigListOfItemsToPlace.extend(ItemPool.ShockwaveTypeItems(spoiler.settings))
        if Types.Key in spoiler.settings.shuffled_location_types:
            bigListOfItemsToPlace.extend(ItemPool.KeysToPlace(spoiler.settings))
        if Types.Cranky in spoiler.settings.shuffled_location_types:
            placed_types.append(Types.Cranky)
            bigListOfItemsToPlace.extend(ItemPool.CrankyItems())
        if Types.Funky in spoiler.settings.shuffled_location_types:
            placed_types.append(Types.Funky)
            bigListOfItemsToPlace.extend(ItemPool.FunkyItems())
        if Types.Candy in spoiler.settings.shuffled_location_types:
            placed_types.append(Types.Candy)
            bigListOfItemsToPlace.extend(ItemPool.CandyItems())
        if Types.Snide in spoiler.settings.shuffled_location_types:
            placed_types.append(Types.Snide)
            bigListOfItemsToPlace.extend(ItemPool.SnideItems())
        for item in preplaced_items:
            if item in bigListOfItemsToPlace:
                bigListOfItemsToPlace.remove(item)
        # If Helm is not last, and we're locking key 8 and we're using the SLO ruleset, place Key 8 in the 8th level somewhere
        if (
            Items.HideoutHelmKey in bigListOfItemsToPlace
            and spoiler.settings.key_8_helm
            and spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.levels
            and not spoiler.settings.hard_level_progression
        ):
            last_level = spoiler.settings.level_order[8]
            if last_level != Levels.HideoutHelm:
                potential_locations = [
                    loc
                    for loc in spoiler.LocationList
                    if spoiler.LocationList[loc].level == last_level
                    and spoiler.LocationList[loc].type in spoiler.settings.shuffled_location_types
                    and not spoiler.LocationList[loc].inaccessible
                    and loc in spoiler.settings.GetValidLocationsForItem(Items.HideoutHelmKey)
                ]
                selected_location = spoiler.settings.random.choice(potential_locations)
                spoiler.LocationList[selected_location].PlaceItem(spoiler, Items.HideoutHelmKey)
                bigListOfItemsToPlace.remove(Items.HideoutHelmKey)
        unplaced = PlaceItems(
            spoiler,
            FillAlgorithm.assumed,
            bigListOfItemsToPlace,
            ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
        )
        if unplaced > 0:
            raise Ex.ItemPlacementException("Unable to find all locations during the fill. Error code: BIG-" + str(unplaced))
        if spoiler.settings.extreme_debugging:
            DebugCheckAllReachable(
                spoiler,
                ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
                "The Fill",
            )

    else:
        # Now we place all logically-relevant low-quantity items
        # Then fill Kongs and Moves - this should be a very early fill type for hopefully obvious reasons
        FillKongsAndMoves(spoiler, placed_types, preplaced_items)
        if spoiler.settings.extreme_debugging:
            DebugCheckAllReachable(
                spoiler,
                ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
                "all moves",
            )

        # Then place Keys
        if Types.Key in spoiler.settings.shuffled_location_types:
            placed_types.append(Types.Key)
            FillShuffledKeys(spoiler, placed_types, preplaced_items)
        if spoiler.settings.extreme_debugging:
            DebugCheckAllReachable(
                spoiler,
                ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
                "Keys",
            )

    # Then place misc progression items
    if Types.Bean in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.Bean)
        placed_types.append(Types.Pearl)
        spoiler.Reset()
        miscItemsToPlace = ItemPool.MiscItemRandoItems().copy()
        for item in preplaced_items:
            if item in miscItemsToPlace:
                miscItemsToPlace.remove(item)
        miscUnplaced = PlaceItems(
            spoiler,
            spoiler.settings.algorithm,
            miscItemsToPlace,
            ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
        )
        if miscUnplaced > 0:
            raise Ex.ItemPlacementException("Unable to find all locations during the fill. Error code: MI-" + str(miscUnplaced))
    if spoiler.settings.extreme_debugging:
        DebugCheckAllReachable(
            spoiler,
            ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
            "Miscellaneous Items",
        )

    # # Now we place the (generally) filler items
    # # If Helm is having locations shuffled and we're shuffling GBs, we have to fill Helm now.
    # # This is because GBs can't be in Helm, so we might run out of locations to place them if these spots aren't filled
    # if Types.Banana in spoiler.settings.shuffled_location_types and (
    #     Types.Medal in spoiler.settings.shuffled_location_types
    #     or Types.Crown in spoiler.settings.shuffled_location_types
    #     or Types.Fairy in spoiler.settings.shuffled_location_types
    #     or Types.Key in spoiler.settings.shuffled_location_types
    # ):
    #     preplaced_items.extend(FillHelmLocations(spoiler, placed_types.copy(), preplaced_items))
    # if spoiler.settings.extreme_debugging:
    #     DebugCheckAllReachable(spoiler, ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items), "things in Helm")

    # If keys are shuffled in the pool we want to ensure an item is on every boss
    # This is to support broader settings that rely on boss kills and to enable reads on the boss fill algorithm
    if Types.Key in spoiler.settings.shuffled_location_types:
        preplaced_items.extend(FillBossLocations(spoiler, placed_types.copy(), preplaced_items))
    if spoiler.settings.extreme_debugging:
        DebugCheckAllReachable(
            spoiler,
            ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
            "things on Bosses",
        )

    # Then place Blueprints - these are moderately restrictive in their placement
    if Types.Blueprint in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.Blueprint)
        spoiler.Reset()
        blueprintsToPlace = ItemPool.Blueprints().copy()
        for item in preplaced_items:
            if item in blueprintsToPlace:
                blueprintsToPlace.remove(item)
        # Blueprints can be placed largely randomly - there's no location (yet) that can cause blueprints to lock themselves
        blueprintsUnplaced = PlaceItems(
            spoiler,
            FillAlgorithm.careful_random,
            blueprintsToPlace,
            ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
        )
        if blueprintsUnplaced > 0:
            raise Ex.ItemPlacementException("Unable to find all locations during the fill. Error code: BP-" + str(blueprintsUnplaced))
    if spoiler.settings.extreme_debugging:
        DebugCheckAllReachable(
            spoiler,
            ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
            "Blueprints",
        )
    # Then place Nintendo & Rareware Coins
    for coin in (Types.NintendoCoin, Types.RarewareCoin):
        if coin in spoiler.settings.shuffled_location_types:
            placed_types.append(coin)
            spoiler.Reset()
            coinsToPlace = ItemPool.NintendoCoinItems() if coin == Types.NintendoCoin else ItemPool.RarewareCoinItems()
            for item in preplaced_items:
                if item in coinsToPlace:
                    coinsToPlace.remove(item)
            coinsUnplaced = PlaceItems(
                spoiler,
                spoiler.settings.algorithm,
                coinsToPlace,
                ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
            )
            if coinsUnplaced > 0:
                raise Ex.ItemPlacementException("Unable to find all locations during the fill. Error code: CC-" + str(coinsUnplaced))
    if spoiler.settings.extreme_debugging:
        DebugCheckAllReachable(
            spoiler,
            ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
            "Company Coins",
        )
    # Then place Battle Crowns
    if Types.Crown in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.Crown)
        spoiler.Reset()
        crownsToPlace = ItemPool.BattleCrownItems()
        for item in preplaced_items:
            if item in crownsToPlace:
                crownsToPlace.remove(item)
        # Crowns can be placed randomly, but only if the helm doors don't need any
        algo = FillAlgorithm.careful_random
        if spoiler.settings.coin_door_item == BarrierItems.Crown or spoiler.settings.crown_door_item == BarrierItems.Crown:
            algo = spoiler.settings.algorithm
        crownsUnplaced = PlaceItems(
            spoiler,
            algo,
            crownsToPlace,
            ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
            doubleTime=True,
        )
        if crownsUnplaced > 0:
            raise Ex.ItemPlacementException("Unable to find all locations during the fill. Error code: CR-" + str(crownsUnplaced))
    if spoiler.settings.extreme_debugging:
        DebugCheckAllReachable(
            spoiler,
            ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
            "Crowns",
        )
    # Then place Banana Medals
    if Types.Medal in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.Medal)
        spoiler.Reset()
        medalsToBePlaced = ItemPool.BananaMedalItems(spoiler.settings)
        for item in preplaced_items:
            if item in medalsToBePlaced:
                medalsToBePlaced.remove(item)
        medalAssumedItems = ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items)
        # Medals up to the logical Jetpac requirement must be placed carefully
        jetpacRequiredMedals = medalsToBePlaced[: spoiler.settings.logical_medal_requirement]
        medalsUnplaced = PlaceItems(spoiler, spoiler.settings.algorithm, jetpacRequiredMedals, medalAssumedItems)
        if medalsUnplaced > 0:
            raise Ex.ItemPlacementException("Unable to find all locations during the fill. Error code: LM-" + str(medalsUnplaced))
        # The remaining medals can be placed randomly
        medalsUnplaced = PlaceItems(
            spoiler,
            FillAlgorithm.careful_random,
            medalsToBePlaced[spoiler.settings.logical_medal_requirement :],
            medalAssumedItems,
        )
        if medalsUnplaced > 0:
            raise Ex.ItemPlacementException("Unable to find all locations during the fill. Error code: RM-" + str(medalsUnplaced))
    if spoiler.settings.extreme_debugging:
        DebugCheckAllReachable(
            spoiler,
            ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
            "Banana Medals",
        )
    # Then place Fairies
    if Types.Fairy in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.Fairy)
        spoiler.Reset()
        fairiesToBePlaced = ItemPool.FairyItems()
        for item in preplaced_items:
            if item in fairiesToBePlaced:
                fairiesToBePlaced.remove(item)
        fairyAssumedItems = ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items)
        # Fairies up to the logical Rareware GB requirement must be placed carefully
        rarewareRequiredFairies = fairiesToBePlaced[: spoiler.settings.logical_fairy_requirement]
        fairyUnplaced = PlaceItems(spoiler, spoiler.settings.algorithm, rarewareRequiredFairies, fairyAssumedItems)
        if fairyUnplaced > 0:
            raise Ex.ItemPlacementException("Unable to find all locations during the fill. Error code: LF-" + str(fairyUnplaced))
        # The remaining fairies can be placed randomly
        fairyUnplaced = PlaceItems(
            spoiler,
            FillAlgorithm.careful_random,
            fairiesToBePlaced[spoiler.settings.logical_fairy_requirement :],
            fairyAssumedItems,
        )
        if fairyUnplaced > 0:
            raise Ex.ItemPlacementException("Unable to find all locations during the fill. Error code: RF-" + str(fairyUnplaced))
    if spoiler.settings.extreme_debugging:
        DebugCheckAllReachable(
            spoiler,
            ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
            "Fairies",
        )
    # Then fill remaining locations with GBs
    preplaced_gbs_accounted_for = []  # Because GBs are placed in two parts, we may have to account for preplaced GBs in either section
    if Types.Banana in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.Banana)
        spoiler.Reset()
        gbsToBePlaced = ItemPool.GoldenBananaItems()
        for item in preplaced_items:
            if item in gbsToBePlaced:
                gbsToBePlaced.remove(item)
                # Mark this preplaced GB as accounted for
                preplaced_gbs_accounted_for.append(item)
        # After checking all preplaced items, we can treat the accounted for GBs as no longer preplaced
        # This way the upcoming ToughBanana GB fill will not double-account for them
        for item in preplaced_gbs_accounted_for:
            preplaced_items.remove(item)
        gbsUnplaced = PlaceItems(spoiler, FillAlgorithm.careful_random, gbsToBePlaced, [])
        if gbsUnplaced > 0:
            raise Ex.ItemPlacementException("Unable to find all locations during the fill. Error code: GB-" + str(gbsUnplaced))
    if spoiler.settings.extreme_debugging:
        DebugCheckAllReachable(
            spoiler,
            ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
            "GBs",
        )
    if Types.ToughBanana in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.ToughBanana)
        spoiler.Reset()
        toughGbsToBePlaced = ItemPool.ToughGoldenBananaItems()
        for item in preplaced_items:
            if item in toughGbsToBePlaced:
                toughGbsToBePlaced.remove(item)
        gbsUnplaced = PlaceItems(spoiler, FillAlgorithm.careful_random, toughGbsToBePlaced, [])
        if gbsUnplaced > 0:
            raise Ex.ItemPlacementException("Unable to find all locations during the fill. Error code: TB-" + str(gbsUnplaced))
    if spoiler.settings.extreme_debugging:
        DebugCheckAllReachable(
            spoiler,
            ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
            "Tough GBs",
        )
    # Place Hints
    if Types.Hint in spoiler.settings.shuffled_location_types and spoiler.settings.progressive_hint_item == ProgressiveHintItem.off:
        placed_types.append(Types.Hint)
        spoiler.Reset()
        hintItemsToBePlaced = ItemPool.HintItems()
        for item in preplaced_items:
            if item in hintItemsToBePlaced:
                hintItemsToBePlaced.remove(item)
        hintsUnplaced = PlaceItems(spoiler, FillAlgorithm.careful_random, hintItemsToBePlaced, [])
        if hintsUnplaced > 0:
            raise Ex.ItemPlacementException("Unable to find all locations during the fill. Error code: HN-" + str(hintsUnplaced))
    if spoiler.settings.extreme_debugging:
        DebugCheckAllReachable(
            spoiler,
            ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types, placed_items=preplaced_items),
            "Tough GBs",
        )
    # Fill in fake items
    if Types.FakeItem in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.FakeItem)
        spoiler.Reset()
        fakeItemsToBePlaced = ItemPool.FakeItems(spoiler.settings)
        for item in preplaced_items:
            if item in fakeItemsToBePlaced:
                fakeItemsToBePlaced.remove(item)
        PlaceItems(spoiler, FillAlgorithm.careful_random, fakeItemsToBePlaced, [])
        # Don't raise exception if unplaced fake items
    if spoiler.settings.extreme_debugging:
        DebugCheckAllReachable(spoiler, ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placed_types), "Fake Items")
    # Fill in junk items
    if Types.JunkItem in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.JunkItem)
        spoiler.Reset()
        PlaceItems(spoiler, FillAlgorithm.random, ItemPool.JunkItems(spoiler.settings), [])
        # Don't raise exception if unplaced junk items
    if Types.CrateItem in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.CrateItem)
        # Crates hold nothing, so leave this one empty
    if Types.Enemies in spoiler.settings.shuffled_location_types:
        placed_types.append(Types.Enemies)
        # Enemies hold nothing, so leave this one empty

    # Some locations require special care to make logic work correctly
    # This is the only location that cares about None vs NoItem - it needs to be None so it fills correctly but NoItem for logic to generate progression correctly
    if spoiler.LocationList[Locations.JapesDonkeyFreeDiddy].item is None:
        spoiler.LocationList[Locations.JapesDonkeyFreeDiddy].PlaceItem(spoiler, Items.NoItem)
    # Shopkeepers have been either placed in the world or set to vanilla. In case of the former, empty out their vanilla "locations" as needed
    for x in range(4):
        if spoiler.LocationList[Locations.ShopOwner_Location00 + x].item is None:
            spoiler.LocationList[Locations.ShopOwner_Location00 + x].PlaceItem(spoiler, Items.NoItem)

    # Finally, check if game is beatable
    spoiler.Reset()
    if not GetAccessibleLocations(spoiler, [], SearchMode.CheckAllReachable):
        print("Failed 101% check")
        raise Ex.GameNotBeatableException("Game not able to complete 101% after placing all items.")
    # We have successfully filled the seed by this point. All that is left is to confirm there are no purchase order locks
    return


def FillTrainingMoves(spoiler: Spoiler, preplacedMoves: List[Items]):
    """Fill training barrels with your starting moves."""
    # Convenient assumptions made by this method:
    # - No list is expected to pull more items than are contained in the list.
    # - Training locations that are made Constant will already have been made so. Essentially, do this after placing constants.
    # - No non-progressive item is in multiple lists. The correct quantity of progressive items are cumulatively in all lists.

    # To account for plando things, remove the possibility for plando'd items to get chosen.
    # This isn't foolproof, particularly around progressive items!
    for item in preplacedMoves:
        for i in range(len(spoiler.settings.starting_moves_lists)):
            if item in spoiler.settings.starting_moves_lists[i]:
                spoiler.settings.starting_moves_lists[i].remove(item)

    # Determine what moves will be placed in these locations
    movesToPlace = []
    # Check for if we've found what would be the vanilla starting slam - this is only necessary if the settings dictate that we should find one
    startingSlamIdentified = not spoiler.settings.start_with_slam
    for i in range(len(spoiler.settings.starting_moves_lists)):
        # If every item in this list is guaranteed to be placed, we have to watch out for vanilla items that should already be placed
        if len(spoiler.settings.starting_moves_lists[i]) <= spoiler.settings.starting_moves_list_counts[i]:
            for item in spoiler.settings.starting_moves_lists[i]:
                # Avoid vanilla training moves, the first starting slam, and climbing
                if item in ItemPool.TrainingBarrelAbilities() and spoiler.settings.training_barrels == TrainingBarrels.normal:
                    continue
                if item == Items.ProgressiveSlam and not startingSlamIdentified:
                    startingSlamIdentified = True
                    continue
                if item == Items.Climbing and spoiler.settings.climbing_status == ClimbingStatus.normal:
                    continue
                # Avoid anything that isn't supposed to be shuffled but could be in the starting move selector (Shopkeepers, Camera/Shockwave)
                if ItemList[item].type not in spoiler.settings.shuffled_location_types:
                    continue
                # Otherwise everything else in this pool is guaranteed to be placed on a starting location
                movesToPlace.append(item)
        # Otherwise we take a random selection of items in this pool equal to the corresponding desired amount
        else:
            movesToPlace.extend(spoiler.settings.random.sample(spoiler.settings.starting_moves_lists[i], k=spoiler.settings.starting_moves_list_counts[i]))

    placedMoves = []
    if spoiler.settings.start_with_slam:
        placedMoves.append(Items.ProgressiveSlam)
    # Shopkeepers can be placed in their special starting locations
    if Items.Cranky in movesToPlace:
        spoiler.LocationList[Locations.ShopOwner_Location00].PlaceItem(spoiler, Items.Cranky)
        spoiler.LocationList[Locations.ShopOwner_Location00].inaccessible = False
        placedMoves.append(Items.Cranky)
        movesToPlace.remove(Items.Cranky)
    if Items.Funky in movesToPlace:
        spoiler.LocationList[Locations.ShopOwner_Location01].PlaceItem(spoiler, Items.Funky)
        spoiler.LocationList[Locations.ShopOwner_Location01].inaccessible = False
        placedMoves.append(Items.Funky)
        movesToPlace.remove(Items.Funky)
    if Items.Candy in movesToPlace:
        spoiler.LocationList[Locations.ShopOwner_Location02].PlaceItem(spoiler, Items.Candy)
        spoiler.LocationList[Locations.ShopOwner_Location02].inaccessible = False
        placedMoves.append(Items.Candy)
        movesToPlace.remove(Items.Candy)
    if Items.Snide in movesToPlace:
        spoiler.LocationList[Locations.ShopOwner_Location03].PlaceItem(spoiler, Items.Snide)
        spoiler.LocationList[Locations.ShopOwner_Location03].inaccessible = False
        placedMoves.append(Items.Snide)
        movesToPlace.remove(Items.Snide)
    if len(movesToPlace) > 0:
        # We can expect that all locations in this region are starting move locations, Training Barrels, or starting shopkeeper locations
        for locationLogic in spoiler.RegionList[Regions.GameStart].locations:
            location = spoiler.LocationList[locationLogic.id]
            if location.item is None and location.type not in (Types.Cranky, Types.Funky, Types.Candy, Types.Snide):  # Don't put moves in shopkeeper locations!
                placedMove = movesToPlace.pop()
                location.inaccessible = False
                location.PlaceItem(spoiler, placedMove)
                placedMoves.append(placedMove)
                if len(movesToPlace) <= 0:
                    break
    return placedMoves


def ShuffleSharedMoves(spoiler: Spoiler, placedMoves: List[Items], placedTypes: List[Types]) -> None:
    """Shuffles shared kong moves into shops and then returns the remaining ones and their valid locations."""
    # If we start with a slam as the training grounds reward, it counts as placed for fill purposes
    if spoiler.settings.start_with_slam:
        placedMoves.append(Items.ProgressiveSlam)
    # If shared moves have to be in shared shops, confirm there are enough locations available for each remaining shared move
    if not spoiler.settings.shuffle_items or Types.Shop not in spoiler.settings.shuffled_location_types:
        availableSharedShops = [location for location in SharedMoveLocations if spoiler.LocationList[location].item is None]
        placedSharedMoves = [move for move in placedMoves if move in ItemPool.ImportantSharedMoves or move in ItemPool.JunkSharedMoves]
        if len(availableSharedShops) < len(ItemPool.ImportantSharedMoves) + len(ItemPool.JunkSharedMoves) - len(placedSharedMoves):
            raise Ex.ItemPlacementException(
                "Too many kong moves placed before shared moves. Only "
                + str(len(availableSharedShops))
                + " available for "
                + str(len(ItemPool.ImportantSharedMoves))
                + str(len(ItemPool.JunkSharedMoves))
                + str(len(placedSharedMoves))
                + " remaining shared moves."
            )

    # When a shared move is assigned to a shop in any particular level, that shop cannot also hold any kong-specific moves.
    # To avoid conflicts, first determine which level shops will have shared moves then remove these shops from each kong's valid locations list
    training = []
    if spoiler.settings.training_barrels != TrainingBarrels.normal:
        # First place training moves that are not placed. These should be the first moves placed outside of starting moves. Placement order is in relative importance.
        training = [Items.Barrels, Items.Vines, Items.Swim, Items.Oranges]
    if spoiler.settings.climbing_status != ClimbingStatus.normal:
        training.append(Items.Climbing)
    trainingMovesToPlace = [move for move in training if move not in placedMoves]
    assumedItems = [x for x in ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placedTypes, placedMoves) if x not in trainingMovesToPlace]
    trainingMovesUnplaced = PlaceItems(spoiler, FillAlgorithm.assumed, trainingMovesToPlace, assumedItems, inOrder=True)
    if trainingMovesUnplaced > 0:
        raise Ex.ItemPlacementException("Unable to find enough locations to place training barrel moves.")
    placedMoves.extend(training)
    importantSharedToPlace = ItemPool.ImportantSharedMoves.copy()
    # Next place any fairy moves that need placing, settings dependent
    if spoiler.settings.shockwave_status == ShockwaveStatus.shuffled and Items.CameraAndShockwave not in placedMoves:
        importantSharedToPlace.append(Items.CameraAndShockwave)
    elif spoiler.settings.shockwave_status == ShockwaveStatus.shuffled_decoupled and (Items.Camera not in placedMoves or Items.Shockwave not in placedMoves):
        importantSharedToPlace.append(Items.Camera)
        importantSharedToPlace.append(Items.Shockwave)
    for item in placedMoves:
        if item in importantSharedToPlace:
            importantSharedToPlace.remove(item)
    placedMoves.extend(importantSharedToPlace)
    importantSharedUnplaced = PlaceItems(
        spoiler,
        FillAlgorithm.assumed,
        importantSharedToPlace,
        ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placedTypes, placedMoves),
    )
    if importantSharedUnplaced > 0:
        raise Ex.ItemPlacementException("Unable to find enough locations to place " + str(importantSharedUnplaced) + " shared important items.")
    junkSharedToPlace = ItemPool.JunkSharedMoves.copy()
    for item in placedMoves:
        if item in junkSharedToPlace:
            junkSharedToPlace.remove(item)
    placedMoves.extend(junkSharedToPlace)
    junkSharedUnplaced = PlaceItems(
        spoiler,
        FillAlgorithm.random,
        junkSharedToPlace,
        [x for x in ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placedTypes) if x not in junkSharedToPlace],
    )
    if junkSharedUnplaced > 0:
        raise Ex.ItemPlacementException("Unable to find enough locations to place " + str(junkSharedUnplaced) + " shared junk items.")


def GeneratePlaythrough(spoiler: Spoiler) -> None:
    """Generate playthrough and way of the hoard and update spoiler."""
    js.postMessage("Seed generated! Finalizing spoiler...")
    spoiler.LogicVariables.assumeFillSuccess = True  # Now that we know the seed is valid, we can assume fill success for the sake of generating the playthrough and WotH
    # Generate and display the playthrough
    spoiler.Reset()
    PlaythroughLocations = GetAccessibleLocations(spoiler, [], SearchMode.GeneratePlaythrough)  # identify in the spheres where the win condition is met
    if not spoiler.LogicVariables.bananaHoard and spoiler.settings.logic_type != LogicType.nologic:
        raise Ex.FillException("Woah, you hit an EXTREMELY rare error! Please post your settings string to the discord. It's probably a freak accident so you're safe to try again.")
    ParePlaythrough(spoiler, PlaythroughLocations)
    # Generate and display woth
    WothLocations = PareWoth(spoiler, PlaythroughLocations)
    # Write data to spoiler and return
    spoiler.UpdateLocations(spoiler.LocationList)
    if any(spoiler.settings.shuffled_location_types):
        ShuffleItems(spoiler)
    spoiler.UpdatePlaythrough(spoiler.LocationList, PlaythroughLocations)
    spoiler.UpdateWoth(spoiler.LocationList, WothLocations)


def GetLogicallyAccessibleKongLocations(spoiler: Spoiler, kongLocations, ownedKongs, latestLevel):
    """Find the logically accessible Kong Locations given the current state of Kong unlocking."""
    logicallyAccessibleKongLocations = []
    for level in range(1, latestLevel + 1):
        if spoiler.settings.level_order[level] == Levels.JungleJapes and Locations.DiddyKong in kongLocations:
            logicallyAccessibleKongLocations.append(Locations.DiddyKong)
        if spoiler.settings.level_order[level] == Levels.FranticFactory and Locations.ChunkyKong in kongLocations:
            logicallyAccessibleKongLocations.append(Locations.ChunkyKong)
        if spoiler.settings.level_order[level] == Levels.AngryAztec and Locations.TinyKong in kongLocations and (Kongs.diddy in ownedKongs or Kongs.chunky in ownedKongs):
            logicallyAccessibleKongLocations.append(Locations.TinyKong)
        if (
            spoiler.settings.level_order[level] == Levels.AngryAztec
            and Locations.LankyKong in kongLocations
            # Must be able to bypass Guitar door - the active bananaports condition is in case your only Llama Temple access is through the quicksand cave
            and (
                Kongs.diddy in ownedKongs
                or IsItemSelected(
                    spoiler.settings.remove_barriers_enabled,
                    spoiler.settings.remove_barriers_selected,
                    RemovedBarriersSelected.aztec_tunnel_door,
                )
                or (Kongs.donkey in ownedKongs and spoiler.settings.activate_all_bananaports == ActivateAllBananaports.all)
            )
            and (Kongs.donkey in ownedKongs or Kongs.lanky in ownedKongs or Kongs.tiny in ownedKongs)
        ):  # Must be able to open Llama Temple
            logicallyAccessibleKongLocations.append(Locations.LankyKong)
    return logicallyAccessibleKongLocations


def PlacePriorityItems(spoiler: Spoiler, itemsToPlace, beforePlacedItems, placedTypes, levelBlock=None):
    """Place the given items with priority, also placing all dependencies depending on where they got placed. Returns a list of all items newly placed by this function."""
    if itemsToPlace == []:  # Base case of recursion - when priority items no longer have dependencies, they'll hit this method placing zero items
        return []
    # Prevent reference shenanigans because I'm too lazy to do it properly
    priorityItemsToPlace = itemsToPlace.copy()
    placedItems = beforePlacedItems.copy()
    # If we're blocking past a certain level, ban keys that would unlock anything beyond those levels
    bannedKeys = []
    if levelBlock is not None:
        bannedKeys = [key for key in ItemPool.Keys() if ItemList[key].index >= levelBlock]
    allOtherItems = ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placedTypes)
    if Types.Key in spoiler.settings.shuffled_location_types:
        # However we don't want all keys - don't assume keys for or beyond the latest logically allowed level's key
        for key in bannedKeys:
            allOtherItems.remove(key)
    # Other exceptions: we don't assume we have the items to be placed, as then they could lock themselves
    for item in priorityItemsToPlace:
        allOtherItems.remove(item)
    # We also don't assume we have any placed items. If these unlock locations we should find them as we go.
    # This should prevent circular logic (e.g. the diddy-unlocking-gun being locked behind guitar which is already priority placed in Japes Cranky)
    for item in placedItems:
        if item in allOtherItems:
            allOtherItems.remove(item)
    # At last, place all the items
    failedToPlace = PlaceItems(spoiler, FillAlgorithm.assumed, priorityItemsToPlace.copy(), ownedItems=allOtherItems)
    if failedToPlace > 0:
        item_names = ", ".join([ItemList[item].name for item in priorityItemsToPlace])
        raise Ex.ItemPlacementException(f"Failed to priority place {item_names}")
    # Note down the latest known list of owned kongs - I don't think this is necessary, but if it is less than 5 it is accurate and should speed up GetUnplacedItemPrerequisites
    ownedKongs = spoiler.LogicVariables.GetKongs()
    # The items we just placed can now be treated as such
    placedItems.extend(priorityItemsToPlace)
    unplacedDependencies = []
    for item in priorityItemsToPlace:
        # Find what items are needed to get this item
        unplacedItems = GetUnplacedItemPrerequisites(spoiler, item, placedItems, ownedKongs)
        slamsRequired = unplacedItems.count(Items.ProgressiveSlam)
        # Add each unplaced item to the list of items that now need to be placed, making sure not to add duplicates or third slams
        for item in unplacedItems:
            if item not in unplacedDependencies or (item == Items.ProgressiveSlam and slamsRequired > 1 and unplacedDependencies.count(Items.ProgressiveSlam) < 2):
                unplacedDependencies.append(item)
    # Recursively place priority items with the dependencies - anything this method places will also need to be returned by the outermost call
    priorityItemsToPlace.extend(PlacePriorityItems(spoiler, unplacedDependencies, placedItems, placedTypes, levelBlock))
    return priorityItemsToPlace


def PlaceKongsInKongLocations(spoiler: Spoiler, kongItems, kongLocations):
    """For these settings, Kongs to place, and locations to place them in, place the Kongs in such a way the generation will never error here."""
    ownedKongs = [kong for kong in spoiler.settings.starting_kong_list]
    # In entrance randomizer, it's too complicated to quickly determine kong accessibility.
    # Instead, we place Kongs in a specific order to guarantee we'll at least have an eligible freer.
    # To be at least somewhat nice to no logic users, we also use this section here so kongs don't lock each other.
    if spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.all or spoiler.settings.logic_type == LogicType.nologic:
        spoiler.settings.random.shuffle(kongItems)
        if Locations.ChunkyKong in kongLocations:
            kongItemToBeFreed = kongItems.pop()
            spoiler.LocationList[Locations.ChunkyKong].PlaceItem(spoiler, kongItemToBeFreed)
            spoiler.settings.chunky_freeing_kong = spoiler.settings.random.choice(ownedKongs)
            ownedKongs.append(ItemPool.GetKongForItem(kongItemToBeFreed))
        if Locations.DiddyKong in kongLocations:
            kongItemToBeFreed = kongItems.pop()
            spoiler.LocationList[Locations.DiddyKong].PlaceItem(spoiler, kongItemToBeFreed)
            spoiler.settings.diddy_freeing_kong = spoiler.settings.random.choice(ownedKongs)
            ownedKongs.append(ItemPool.GetKongForItem(kongItemToBeFreed))
        # The Lanky location can't be your first in cases where the Lanky freeing Kong can't get into the llama temple and you need a second Kong
        if Locations.LankyKong in kongLocations:
            kongItemToBeFreed = kongItems.pop()
            spoiler.LocationList[Locations.LankyKong].PlaceItem(spoiler, kongItemToBeFreed)
            spoiler.settings.lanky_freeing_kong = spoiler.settings.random.choice(ownedKongs)
            ownedKongs.append(ItemPool.GetKongForItem(kongItemToBeFreed))
        # Placing the Tiny location last guarantees we have one of Diddy or Chunky
        if Locations.TinyKong in kongLocations:
            kongItemToBeFreed = kongItems.pop()
            spoiler.LocationList[Locations.TinyKong].PlaceItem(spoiler, kongItemToBeFreed)
            eligibleFreers = list(set(ownedKongs).intersection([Kongs.diddy, Kongs.chunky]))
            spoiler.settings.tiny_freeing_kong = spoiler.settings.random.choice(eligibleFreers)
            ownedKongs.append(ItemPool.GetKongForItem(kongItemToBeFreed))
    # In level order shuffling, we need to be very particular about who we unlock and in what order so as to guarantee completion
    # Vanilla levels can be treated as if the level shuffler randomly placed all the levels in the same order
    elif spoiler.settings.shuffle_loading_zones in (ShuffleLoadingZones.levels, ShuffleLoadingZones.none):
        latestLogicallyAllowedLevel = len(ownedKongs) + 1
        # Logically we can always enter any level on hard level progression
        if spoiler.settings.hard_level_progression:
            latestLogicallyAllowedLevel = 8
        logicallyAccessibleKongLocations = GetLogicallyAccessibleKongLocations(spoiler, kongLocations, ownedKongs, latestLogicallyAllowedLevel)
        while len(ownedKongs) != 5:
            # If there aren't any accessible Kong locations, then the level order shuffler has a bug (this shouldn't happen)
            if not any(logicallyAccessibleKongLocations):
                raise Ex.EntrancePlacementException("Levels shuffled in a way that makes Kong unlocks impossible. SEND THIS TO THE DEVS!")
            # Begin by finding the currently accessible Kong locations
            # Randomly pick an accessible location
            progressionLocation = spoiler.settings.random.choice(logicallyAccessibleKongLocations)
            logicallyAccessibleKongLocations.remove(progressionLocation)
            # Pick a Kong to free this location from the Kongs we currently have
            if progressionLocation == Locations.DiddyKong:
                spoiler.settings.diddy_freeing_kong = spoiler.settings.random.choice(ownedKongs)
            elif progressionLocation == Locations.LankyKong:
                spoiler.settings.lanky_freeing_kong = spoiler.settings.random.choice(ownedKongs)
            elif progressionLocation == Locations.TinyKong:
                eligibleFreers = list(set(ownedKongs).intersection([Kongs.diddy, Kongs.chunky]))
                spoiler.settings.tiny_freeing_kong = spoiler.settings.random.choice(eligibleFreers)
            elif progressionLocation == Locations.ChunkyKong:
                spoiler.settings.chunky_freeing_kong = spoiler.settings.random.choice(ownedKongs)
            # Remove this location from any considerations
            kongLocations.remove(progressionLocation)
            # Pick a Kong to unlock from the locked Kongs
            kongToBeFreed = spoiler.settings.random.choice(kongItems)
            # With this kong, we can progress one level further (if we care about this logic)
            if not spoiler.settings.hard_level_progression:
                latestLogicallyAllowedLevel += 1
            # If this Kong must unlock more locked Kong locations, we have to be more careful
            # The second condition here because we don't need to worry about the last placed Kong
            if len(logicallyAccessibleKongLocations) == 0 and len(kongItems) > 1:
                # First check if that newly accessible level adds a location. If it does, then it doesn't matter who we free here
                logicallyAccessibleKongLocations = GetLogicallyAccessibleKongLocations(spoiler, kongLocations, ownedKongs, latestLogicallyAllowedLevel)
                if not any(logicallyAccessibleKongLocations):
                    # If it doesn't, then we need to see which Kongs will open more Kongs
                    progressionKongItems = []
                    for kongItem in kongItems:
                        # Test each Kong by temporarily owning them and seeing what we can now reach
                        tempOwnedKongs = [x for x in ownedKongs]
                        tempOwnedKongs.append(ItemPool.GetKongForItem(kongItem))
                        newlyAccessibleKongLocations = GetLogicallyAccessibleKongLocations(spoiler, kongLocations, tempOwnedKongs, latestLogicallyAllowedLevel)
                        if any(newlyAccessibleKongLocations):
                            progressionKongItems.append(kongItem)
                    if len(progressionKongItems) == 0:
                        raise Ex.FillException("Kongs placed in a way that is impossible to unlock everyone. SEND THIS TO THE DEVS!")
                    # Pick a random Kong from the Kongs that guarantee progression
                    kongToBeFreed = spoiler.settings.random.choice(progressionKongItems)
            # Now that we have a combination guaranteed to not break the seed or logic, lock it in
            spoiler.LocationList[progressionLocation].PlaceItem(spoiler, kongToBeFreed)
            spoiler.settings.debug_fill[spoiler.LocationList[progressionLocation].name] = kongToBeFreed
            kongItems.remove(kongToBeFreed)
            ownedKongs.append(ItemPool.GetKongForItem(kongToBeFreed))
            # Refresh the location list and repeat until all Kongs are free
            logicallyAccessibleKongLocations = GetLogicallyAccessibleKongLocations(spoiler, kongLocations, ownedKongs, latestLogicallyAllowedLevel)
    # Pick freeing kongs for any that are still "any" with no restrictions.
    if spoiler.settings.diddy_freeing_kong == Kongs.any:
        spoiler.settings.diddy_freeing_kong = spoiler.settings.random.choice(GetKongs())
    if spoiler.settings.lanky_freeing_kong == Kongs.any:
        spoiler.settings.lanky_freeing_kong = spoiler.settings.random.choice(GetKongs())
    if spoiler.settings.tiny_freeing_kong == Kongs.any:
        spoiler.settings.tiny_freeing_kong = spoiler.settings.random.choice([Kongs.diddy, Kongs.chunky])
    if spoiler.settings.chunky_freeing_kong == Kongs.any:
        spoiler.settings.chunky_freeing_kong = spoiler.settings.random.choice(GetKongs())
    # Update the locations' assigned kong with the set freeing kong list
    spoiler.LocationList[Locations.DiddyKong].kong = spoiler.settings.diddy_freeing_kong
    spoiler.LocationList[Locations.JapesDonkeyFrontofCage].kong = spoiler.settings.diddy_freeing_kong
    spoiler.LocationList[Locations.JapesDonkeyFreeDiddy].kong = spoiler.settings.diddy_freeing_kong
    spoiler.LocationList[Locations.LankyKong].kong = spoiler.settings.lanky_freeing_kong
    spoiler.LocationList[Locations.AztecDonkeyFreeLanky].kong = spoiler.settings.lanky_freeing_kong
    spoiler.LocationList[Locations.TinyKong].kong = spoiler.settings.tiny_freeing_kong
    spoiler.LocationList[Locations.AztecDiddyFreeTiny].kong = spoiler.settings.tiny_freeing_kong
    spoiler.LocationList[Locations.ChunkyKong].kong = spoiler.settings.chunky_freeing_kong
    spoiler.LocationList[Locations.FactoryLankyFreeChunky].kong = spoiler.settings.chunky_freeing_kong
    spoiler.settings.update_valid_locations(spoiler)


def FillKongs(spoiler: Spoiler, placedTypes: List[Types], placedItems: List[Items]) -> None:
    """Place Kongs in valid locations."""
    placedTypes.append(Types.Kong)
    # Determine what kong items need to be placed
    startingKongItems = [ItemPool.ItemFromKong(kong) for kong in spoiler.settings.starting_kong_list]
    kongItems = [item for item in ItemPool.Kongs(spoiler.settings) if item not in startingKongItems and item not in placedItems]
    # If Kongs can be placed anywhere, we don't need anything special
    if spoiler.settings.shuffle_items and Types.Kong in spoiler.settings.shuffled_location_types:
        # First, randomly pick who opens what cage - this prevents cases where a Kong locks themselves
        spoiler.settings.diddy_freeing_kong = spoiler.settings.random.choice(GetKongs())
        spoiler.settings.lanky_freeing_kong = spoiler.settings.random.choice(GetKongs())
        spoiler.settings.tiny_freeing_kong = spoiler.settings.random.choice([Kongs.diddy, Kongs.chunky])
        spoiler.settings.chunky_freeing_kong = spoiler.settings.random.choice(GetKongs())
        if spoiler.settings.enable_plandomizer:
            if spoiler.settings.plandomizer_dict["plando_kong_rescue_diddy"] != -1:
                spoiler.settings.diddy_freeing_kong = Kongs(spoiler.settings.plandomizer_dict["plando_kong_rescue_diddy"])
            if spoiler.settings.plandomizer_dict["plando_kong_rescue_lanky"] != -1:
                spoiler.settings.lanky_freeing_kong = Kongs(spoiler.settings.plandomizer_dict["plando_kong_rescue_lanky"])
            if spoiler.settings.plandomizer_dict["plando_kong_rescue_tiny"] != -1:
                spoiler.settings.tiny_freeing_kong = Kongs(spoiler.settings.plandomizer_dict["plando_kong_rescue_tiny"])
            if spoiler.settings.plandomizer_dict["plando_kong_rescue_chunky"] != -1:
                spoiler.settings.chunky_freeing_kong = Kongs(spoiler.settings.plandomizer_dict["plando_kong_rescue_chunky"])
        # Update the locations' assigned kong with the set freeing kong list
        spoiler.LocationList[Locations.JapesDonkeyFrontofCage].kong = spoiler.settings.diddy_freeing_kong
        spoiler.LocationList[Locations.JapesDonkeyFreeDiddy].kong = spoiler.settings.diddy_freeing_kong
        spoiler.LocationList[Locations.AztecDonkeyFreeLanky].kong = spoiler.settings.lanky_freeing_kong
        spoiler.LocationList[Locations.AztecDiddyFreeTiny].kong = spoiler.settings.tiny_freeing_kong
        spoiler.LocationList[Locations.FactoryLankyFreeChunky].kong = spoiler.settings.chunky_freeing_kong
        assumedItems = ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placedTypes, placedItems)
        spoiler.Reset()
        PlaceItems(spoiler, FillAlgorithm.assumed, kongItems, assumedItems)
        # If we didn't put an item in a kong location, then it gets a NoItem
        # This matters specifically so the logic around items inside Kong cages (VERY important for Diddy's cage) behaves properly
        if spoiler.LocationList[Locations.DiddyKong].item is None:
            spoiler.LocationList[Locations.DiddyKong].PlaceItem(spoiler, Items.NoItem)
        else:
            spoiler.LocationList[Locations.DiddyKong].kong = spoiler.settings.diddy_freeing_kong  # If any Kong cage DOES have a kong, update the location's assigned Kong
        if spoiler.LocationList[Locations.TinyKong].item is None:
            spoiler.LocationList[Locations.TinyKong].PlaceItem(spoiler, Items.NoItem)
        else:
            spoiler.LocationList[Locations.TinyKong].kong = spoiler.settings.tiny_freeing_kong
        if spoiler.LocationList[Locations.LankyKong].item is None:
            spoiler.LocationList[Locations.LankyKong].PlaceItem(spoiler, Items.NoItem)
        else:
            spoiler.LocationList[Locations.LankyKong].kong = spoiler.settings.lanky_freeing_kong
        if spoiler.LocationList[Locations.ChunkyKong].item is None:
            spoiler.LocationList[Locations.ChunkyKong].PlaceItem(spoiler, Items.NoItem)
        else:
            spoiler.LocationList[Locations.ChunkyKong].kong = spoiler.settings.chunky_freeing_kong
        spoiler.settings.update_valid_locations(spoiler)
    # If kongs must be in Kong cages, we need to be more careful
    else:
        # Plando causes problems here. Let's just not.
        if any([item for item in placedItems if ItemList[item].type == Types.Kong]):
            raise Ex.PlandoIncompatibleException("Cannot plando Kong placement if Kongs are not in the pool.")
        if spoiler.settings.enable_plandomizer and (
            spoiler.settings.plandomizer_dict["plando_kong_rescue_diddy"] != -1
            or spoiler.settings.plandomizer_dict["plando_kong_rescue_lanky"] != -1
            or spoiler.settings.plandomizer_dict["plando_kong_rescue_tiny"] != -1
            or spoiler.settings.plandomizer_dict["plando_kong_rescue_chunky"] != -1
        ):
            raise Ex.PlandoIncompatibleException("Cannot plando Kong cage openers if Kongs are not in the pool.")
        # Determine what locations the kong items need to be placed in
        if any(spoiler.settings.kong_locations):
            emptyKongLocations = [location for location in [Locations.DiddyKong, Locations.LankyKong, Locations.TinyKong, Locations.ChunkyKong] if location not in spoiler.settings.kong_locations]
            for locationId in emptyKongLocations:
                spoiler.LocationList[locationId].PlaceItem(spoiler, Items.NoItem)
        spoiler.Reset()
        # Specialized Kong placement function that will never fail to find a beatable combination of Kong unlocks for the vanilla locations
        PlaceKongsInKongLocations(spoiler, kongItems, spoiler.settings.kong_locations.copy())


def FillKongsAndMoves(spoiler: Spoiler, placedTypes: List[Types], placedItems: List[Items]) -> None:
    """Fill kongs, then progression moves, then shared moves, then rest of moves."""
    itemsToPlace = []

    # Handle kong rando first so we know what moves are most important to place
    if spoiler.settings.kong_rando:
        FillKongs(spoiler, placedTypes, placedItems)
    placedMoves = [
        Items.Donkey,
        Items.Diddy,
        Items.Lanky,
        Items.Tiny,
        Items.Chunky,
    ]  # Kongs are now placed, either in the above method or by default
    placedMoves.extend(placedItems)

    # Place Training Moves
    placedMoves.extend(FillTrainingMoves(spoiler, placedItems))

    # Fill in Shop Owners
    shop_owner_items = {
        Types.Cranky: ItemPool.CrankyItems(),
        Types.Funky: ItemPool.FunkyItems(),
        Types.Candy: ItemPool.CandyItems(),
        Types.Snide: ItemPool.SnideItems(),
    }
    for item_type in shop_owner_items:
        if item_type in spoiler.settings.shuffled_location_types:
            placedTypes.append(item_type)
            spoiler.Reset()
            shopOwnerItemsToBePlaced = shop_owner_items[item_type]
            for item in placedMoves:
                if item in shopOwnerItemsToBePlaced:
                    shopOwnerItemsToBePlaced.remove(item)
            unplacedShopOwners = PlaceItems(
                spoiler,
                FillAlgorithm.random,
                shopOwnerItemsToBePlaced,
                ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placedTypes, placedItems),
            )
            if unplacedShopOwners > 0:
                raise Ex.ItemPlacementException("Unable to find locations to place " + str(unplacedShopOwners) + " shop owners.")

    # Handle shared moves before other moves in move rando
    if spoiler.settings.move_rando != MoveRando.off:
        # Shuffle the shared move locations since they must be done first
        ShuffleSharedMoves(spoiler, placedMoves.copy(), placedTypes)
        # Set up remaining kong moves to be shuffled
        itemsToPlace.extend(ItemPool.DonkeyMoves)
        itemsToPlace.extend(ItemPool.DiddyMoves)
        itemsToPlace.extend(ItemPool.LankyMoves)
        itemsToPlace.extend(ItemPool.TinyMoves)
        itemsToPlace.extend(ItemPool.ChunkyMoves)

    # Handle remaining moves/items
    placedTypes.append(Types.Shop)
    placedTypes.append(Types.TrainingBarrel)
    placedTypes.append(Types.Climbing)
    placedTypes.append(Types.Shockwave)
    spoiler.Reset()
    itemsToPlace = [item for item in itemsToPlace if item not in placedMoves]
    unplaced = PlaceItems(
        spoiler,
        FillAlgorithm.assumed,
        itemsToPlace,
        ItemPool.GetItemsNeedingToBeAssumed(spoiler.settings, placedTypes, placedItems),
    )
    if unplaced > 0:
        # debug code - outputs all preplaced and shared items in an attempt to find where things are going wrong
        locationsAndMoves = {}
        emptyShops = []
        emptySharedShops = []
        for locationId in spoiler.LocationList:
            location = spoiler.LocationList[locationId]
            if location.item is not None and location.item != Items.NoItem and location.item <= Items.CameraAndShockwave:
                locationsAndMoves[locationId] = location.item
            if location.type == Types.Shop and location.item is None:
                emptyShops.append(location)
                if locationId in SharedMoveLocations:
                    emptySharedShops.append(location)
        raise Ex.ItemPlacementException(str(unplaced) + " unplaced items.")


def FillWorld(spoiler: Spoiler) -> None:
    """Fill all locations with Kongs, moves, items, and etc."""
    # Level order rando may have to affect the progression to be fillable - no logic doesn't care about your silly progression, however
    wipe_progression = spoiler.settings.shuffle_loading_zones != ShuffleLoadingZones.all and spoiler.settings.logic_type != LogicType.nologic
    retries = 0
    error_log = []
    while 1:
        try:
            if wipe_progression:
                # Assume we can progress through the levels so long as we have enough kongs
                spoiler.settings.kongs_for_progression = True
                WipeBLockerRequirements(spoiler.settings)
                # If we're in CLO and keys are not in the pool, don't wipe boss requirements
                if not (spoiler.settings.hard_level_progression and spoiler.settings.shuffle_items and Types.Key in spoiler.settings.shuffled_location_types):
                    WipeBossRequirements(spoiler.settings)
            # To aid in finding these locations, treat Rareware Coin and Rareware GB as being ~15-20% more expensive for fill purposes (unless it's already very expensive)
            spoiler.settings.medal_requirement = spoiler.settings.logical_medal_requirement
            spoiler.settings.rareware_gb_fairies = spoiler.settings.logical_fairy_requirement
            # Fill locations
            Fill(spoiler)
            if wipe_progression:
                # Update progression requirements based on what is now accessible after all shuffles are done
                if spoiler.settings.hard_level_progression:
                    SetNewProgressionRequirementsUnordered(spoiler)
                else:
                    SetNewProgressionRequirements(spoiler)
                # After setting B. Lockers and bosses, make sure the game is still 101%-able
                spoiler.Reset()
                if not GetAccessibleLocations(spoiler, [], SearchMode.CheckAllReachable):
                    print("Failed post-progression 101% check?")
                    raise Ex.GameNotBeatableException("Game not able to complete 101% after setting progression.")
                # Once progression requirements updated, no longer assume we need kongs freed for level progression
                spoiler.settings.kongs_for_progression = False
            # Reset the adjustments made for fill purposes
            spoiler.settings.medal_requirement = spoiler.settings.original_medal_requirement
            spoiler.settings.rareware_gb_fairies = spoiler.settings.original_fairy_requirement
            # Check if game is beatable
            if not VerifyWorldWithWorstCoinUsage(spoiler):
                raise Ex.GameNotBeatableException("Game potentially unbeatable after placing all items.")
            return
        except Ex.FillException as ex:
            error_log.append(ex)
            spoiler.Reset()
            spoiler.ClearAllLocations()
            retries += 1
            if retries == 2:
                js.postMessage("Fill failed, out of retries.")
                raise ex
            spoiler.settings.shuffle_prices(spoiler)
            # We don't really reach this block anymore now that we moved this to the server
            # Every 3rd fill, retry more aggressively by reshuffling level order, move prices, and starting location as applicable
            if retries % 3 == 0:
                js.postMessage("Retrying fill really hard. Tries: " + str(retries))
                if spoiler.settings.random_starting_region:
                    spoiler.settings.RandomizeStartingLocation(spoiler)
                if spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.levels:  # TODO: Reshuffling LZR doesn't work yet, but it might be nice? Not sure how necessary it is
                    ShuffleExits.ShuffleExits(spoiler)
                    spoiler.UpdateExits()
            else:
                js.postMessage("Retrying fill. Tries: " + str(retries))


def GetAccessibleKongLocations(levels: list, ownedKongs: list):
    """Get all kong locations within the provided levels which are reachable by owned kongs."""
    kongLocations = []
    for level in levels:
        if level == Levels.JungleJapes:
            kongLocations.append(Locations.DiddyKong)
        elif level == Levels.AngryAztec:
            if Kongs.donkey in ownedKongs or Kongs.lanky in ownedKongs or Kongs.tiny in ownedKongs:
                kongLocations.append(Locations.LankyKong)
            if Kongs.diddy in ownedKongs:
                kongLocations.append(Locations.TinyKong)
        elif level == Levels.FranticFactory:
            if Kongs.lanky in ownedKongs or Kongs.tiny in ownedKongs:
                kongLocations.append(Locations.ChunkyKong)
    return kongLocations


def WipeBLockerRequirements(settings: Settings) -> None:
    """Wipe out progression requirements to assume access through main 7 levels."""
    for i in range(0, 7):
        # Assume B.Locker amounts will be attainable for now
        settings.BLockerEntryCount[i] = 0
    # Iff Helm is shuffled amongst other levels, also wipe the Helm B. Locker
    if settings.shuffle_helm_location:
        settings.BLockerEntryCount[7] = 0


def WipeBossRequirements(settings: Settings) -> None:
    """Wipe out progression requirements to beat bosses in the main 7 levels."""
    for i in range(0, 7):
        # Assume T&S amounts will be attainable for now
        settings.BossBananas[i] = 0
        # The standard boss placement algorithm assumes the starting kong can beat all the bosses for now
        # If we are plandoing bosses, then we can't undo boss choices here because they've already been made
        if not settings.boss_plando:
            settings.boss_kongs[i] = settings.starting_kong
            settings.boss_maps[i] = Maps.GalleonBoss  # This requires nothing, allowing the fill to proceed as normal


def SetNewProgressionRequirements(spoiler: Spoiler) -> None:
    """Set new progression requirements based on what is owned or accessible heading into each level."""
    # Find for each level: # of accessible bananas, total GBs, owned kongs & owned moves
    settings = spoiler.settings
    coloredBananaCounts = []
    # goldenBananaTotals = []
    ownedKongs = {}
    ownedMoves = {}
    # Cap the B. Locker amounts based on a random fraction of accessible bananas & GBs
    BLOCKER_MIN = 0.4
    BLOCKER_MAX = 0.7
    if settings.hard_blockers:
        BLOCKER_MIN = 0.6
        BLOCKER_MAX = 0.95
    blocker_variable_mapping = {
        0: settings.blocker_0,
        1: settings.blocker_1,
        2: settings.blocker_2,
        3: settings.blocker_3,
        4: settings.blocker_4,
        5: settings.blocker_5,
        6: settings.blocker_6,
        7: settings.blocker_7,
    }
    blocker_value_projection = [0, 0, 0, 0, 0, 0, 0, 0]
    blocker_item_projection = [item for item in settings.BLockerEntryItems]
    # Get sphere 0 GB count
    BlockAccessToLevel(settings, 0)
    spoiler.Reset()
    accessible = GetAccessibleLocations(spoiler, [], SearchMode.GetReachable)
    # Find all items that could be our first B. Locker's requirement
    accessibleItems = spoiler.LogicVariables.ItemCounts()
    # In Chaos B. Lockers, we should try our best to avoid a 0
    if settings.chaos_blockers and accessibleItems[blocker_item_projection[0]] == 0:
        # Determine which items have been found and could be eligible for this door
        eligibleTypes = [item for item in settings.blocker_limits.keys() if accessibleItems[item] > 0]
        # There can be only one Bean Locker, P. Locker, and C.C. Locker so they are not eligible if it already exists
        if BarrierItems.Bean in eligibleTypes and BarrierItems.Bean in blocker_item_projection:
            eligibleTypes.remove(BarrierItems.Bean)
        if BarrierItems.Pearl in eligibleTypes and BarrierItems.Pearl in blocker_item_projection:
            eligibleTypes.remove(BarrierItems.Pearl)
        if BarrierItems.CompanyCoin in eligibleTypes and BarrierItems.CompanyCoin in blocker_item_projection:
            eligibleTypes.remove(BarrierItems.CompanyCoin)
        # If there are no eligible items (most likely on B. Locker 1) then we'll have to settle for 0 GBs
        if len(eligibleTypes) == 0:
            blocker_item_projection[0] = BarrierItems.GoldenBanana
        else:
            blocker_item_projection[0] = spoiler.settings.random.choice(eligibleTypes)
    blocker_value_projection[0] = min(1, accessibleItems[blocker_item_projection[0]])  # This should limit the first B. Locker to 1 item, no matter what it is
    if not settings.chaos_blockers:
        blocker_value_projection[0] = min(blocker_variable_mapping[0], blocker_value_projection[0])
    # For each level, calculate the available moves and number of bananas
    for level in range(1, 9):
        thisLevel = GetLevelShuffledToIndex(level - 1)
        # Block access to future levels
        BlockAccessToLevel(settings, level + 1)
        settings.BossBananas[thisLevel] = 1000  # also block this level's boss
        # Set up the logic variables with the available locations and items
        spoiler.Reset()
        accessible = GetAccessibleLocations(spoiler, [], SearchMode.GetReachable)
        # Save the available counts for this level
        coloredBananaCounts.append(spoiler.LogicVariables.ColoredBananas[thisLevel])
        # Calculate the available quantity of items for the B. Locker
        accessibleItems = spoiler.LogicVariables.ItemCounts()
        # Calculate the next level's B. Locker value based on what's available (if there is a next level)
        if level < 8:
            # In Chaos B. Lockers, we should try our best to avoid a 0
            if settings.chaos_blockers and accessibleItems[blocker_item_projection[level]] == 0:
                # Determine which items have been found and could be eligible for this door
                eligibleTypes = [item for item in settings.blocker_limits.keys() if accessibleItems[item] > 0]
                # There can be only one Bean Locker, P. Locker, and C.C. Locker so they are not eligible if it already exists
                if BarrierItems.Bean in eligibleTypes and BarrierItems.Bean in blocker_item_projection:
                    eligibleTypes.remove(BarrierItems.Bean)
                if BarrierItems.Pearl in eligibleTypes and BarrierItems.Pearl in blocker_item_projection:
                    eligibleTypes.remove(BarrierItems.Pearl)
                if BarrierItems.CompanyCoin in eligibleTypes and BarrierItems.CompanyCoin in blocker_item_projection:
                    eligibleTypes.remove(BarrierItems.CompanyCoin)
                # If there are no eligible items (staggeringly unlikely past level 1) then we'll have to settle for 0 GBs
                if len(eligibleTypes) == 0:
                    blocker_item_projection[level] = BarrierItems.GoldenBanana
                else:
                    blocker_item_projection[level] = spoiler.settings.random.choice(eligibleTypes)
            blocker_value_projection[level] = max(1, round(spoiler.settings.random.uniform(BLOCKER_MIN, BLOCKER_MAX) * accessibleItems[blocker_item_projection[level]]))
            # If we're on Chaos B. Lockers, we need a random value to compare against so we don't only follow the item availability heuristic - if we did, we'd get really expensive B. Lockers
            if settings.chaos_blockers:
                # Roll 8 random values and take the levelth one to get an approximation of what the levelth most expensive random B. Locker might be if all of them were of this item
                # This is functionally equivalent to what non-chaos B. Lockers does with GBs during settings initialization (blocker_0, blocker_1, etc.)
                # This also prevents the item availability-based values from overtaking the maximum value
                assorted_random_values = []
                for i in range(8):
                    assorted_random_values.append(spoiler.settings.random.randint(1, ceil(settings.blocker_limits[blocker_item_projection[level]] * settings.chaos_ratio)))
                assorted_random_values.sort()
                blocker_value_projection[level] = min(assorted_random_values[level], blocker_value_projection[level])
            # If we're not on Chaos B. Lockers we need to respect the UI input or the randomly generated value from earlier so the item availability calc doesn't overtake the max
            else:
                blocker_value_projection[level] = min(blocker_variable_mapping[level], blocker_value_projection[level])
        ownedKongs[thisLevel] = spoiler.LogicVariables.GetKongs()
        accessibleMoves = [
            spoiler.LocationList[x].item
            for x in accessible
            if spoiler.LocationList[x].item != Items.NoItem
            and spoiler.LocationList[x].item is not None
            and ItemList[spoiler.LocationList[x].item].type in (Types.TrainingBarrel, Types.Shop, Types.Shockwave, Types.Climbing)
        ]
        ownedMoves[thisLevel] = accessibleMoves
    settings.BLockerEntryCount = blocker_value_projection
    # Without Chaos B. Lockers, the last B. Locker is unchanged from what was generated earlier
    if not settings.chaos_blockers:
        settings.BLockerEntryCount[7] = settings.blocker_7
    # With Chaos B. Lockers, we give the last level a the maximum value for that item proportional to the chaos ratio input
    else:
        settings.BLockerEntryCount[7] = ceil(settings.chaos_ratio * settings.blocker_limits[blocker_item_projection[7]])
        settings.BLockerEntryItems = blocker_item_projection
    # Prevent scenario where B. Lockers randomize to not-always-increasing values
    if settings.randomize_blocker_required_amounts:
        for i in range(1, 7):
            for j in range(i + 1, 7):
                # If any later level j is cheaper than this level i, swap the B. Lockers
                # This will never break logic - if you could get into a more expensive level 3, you could get into an equally expensive level 4
                # This only applies if the levels have the same item required by B. Locker
                if settings.BLockerEntryItems[i] == settings.BLockerEntryItems[j] and settings.BLockerEntryCount[i] > settings.BLockerEntryCount[j]:
                    temp = settings.BLockerEntryCount[i]
                    settings.BLockerEntryCount[i] = settings.BLockerEntryCount[j]
                    settings.BLockerEntryCount[j] = temp
    if settings.troff_max > 0:
        settings.BossBananas = [
            min(
                settings.troff_0,
                sum(coloredBananaCounts[0]),
                round(settings.troff_0 / (settings.troff_max * settings.troff_weight_0) * sum(coloredBananaCounts[0])),
            ),
            min(
                settings.troff_1,
                sum(coloredBananaCounts[1]),
                round(settings.troff_1 / (settings.troff_max * settings.troff_weight_1) * sum(coloredBananaCounts[1])),
            ),
            min(
                settings.troff_2,
                sum(coloredBananaCounts[2]),
                round(settings.troff_2 / (settings.troff_max * settings.troff_weight_2) * sum(coloredBananaCounts[2])),
            ),
            min(
                settings.troff_3,
                sum(coloredBananaCounts[3]),
                round(settings.troff_3 / (settings.troff_max * settings.troff_weight_3) * sum(coloredBananaCounts[3])),
            ),
            min(
                settings.troff_4,
                sum(coloredBananaCounts[4]),
                round(settings.troff_4 / (settings.troff_max * settings.troff_weight_4) * sum(coloredBananaCounts[4])),
            ),
            min(
                settings.troff_5,
                sum(coloredBananaCounts[5]),
                round(settings.troff_5 / (settings.troff_max * settings.troff_weight_5) * sum(coloredBananaCounts[5])),
            ),
            min(
                settings.troff_6,
                sum(coloredBananaCounts[6]),
                round(settings.troff_6 / (settings.troff_max * settings.troff_weight_6) * sum(coloredBananaCounts[6])),
            ),
            min(
                settings.troff_7,
                sum(coloredBananaCounts[7]),
                round(settings.troff_7 / (settings.troff_max * settings.troff_weight_7) * sum(coloredBananaCounts[7])),
            ),
        ]
    else:
        settings.BossBananas = [0, 0, 0, 0, 0, 0, 0, 0]
    # Update values based on actual level progression
    ShuffleExits.UpdateLevelProgression(settings)
    # We only need to shuffle bosses based on these calculated items if they aren't placed already
    if not settings.boss_plando:
        ShuffleBossesBasedOnOwnedItems(spoiler, ownedKongs, ownedMoves)
    settings.owned_kongs_by_level = ownedKongs
    settings.owned_moves_by_level = ownedMoves


def SetNewProgressionRequirementsUnordered(spoiler: Spoiler) -> None:
    """Set level progression requirements based on a random path of accessible levels."""
    settings = spoiler.settings
    isKeyItemRando = settings.shuffle_items and Types.Key in settings.shuffled_location_types
    ownedKongs = {}
    ownedMoves = {}
    allMoves = ItemPool.DonkeyMoves.copy()
    allMoves.extend(ItemPool.DiddyMoves)
    allMoves.extend(ItemPool.LankyMoves)
    allMoves.extend(ItemPool.TinyMoves)
    allMoves.extend(ItemPool.ChunkyMoves)
    allMoves.extend(ItemPool.ImportantSharedMoves)
    allMoves.extend(ItemPool.TrainingBarrelAbilities())
    allMoves.extend(ItemPool.ClimbingAbilities())
    KeyEvents = [
        Events.JapesKeyTurnedIn,
        Events.AztecKeyTurnedIn,
        Events.FactoryKeyTurnedIn,
        Events.GalleonKeyTurnedIn,
        Events.ForestKeyTurnedIn,
        Events.CavesKeyTurnedIn,
        Events.CastleKeyTurnedIn,
        Events.HelmKeyTurnedIn,
    ]

    # Limit the B. Locker amounts based on a fraction of the accessible GBs
    BLOCKER_MIN = 0.4
    BLOCKER_MAX = 0.7
    if settings.hard_blockers:
        BLOCKER_MIN = 0.6
        BLOCKER_MAX = 0.95

    # Before doing anything else, determine how many GBs we can access without entering any levels
    # This is likely to be 1, but depending on the settings there are pretty good odds more are available
    BlockAccessToLevel(settings, 0)
    spoiler.Reset()
    accessible = GetAccessibleLocations(spoiler, [], SearchMode.GetReachable)
    runningGBTotal = spoiler.LogicVariables.GoldenBananas

    # Reset B. Lockers and T&S to initial values
    settings.BLockerEntryCount = [
        settings.blocker_0,
        settings.blocker_1,
        settings.blocker_2,
        settings.blocker_3,
        settings.blocker_4,
        settings.blocker_5,
        settings.blocker_6,
        settings.blocker_7,
    ]
    settings.BossBananas = [
        settings.troff_0,
        settings.troff_1,
        settings.troff_2,
        settings.troff_3,
        settings.troff_4,
        settings.troff_5,
        settings.troff_6,
        settings.troff_7,
    ]
    if settings.randomize_blocker_required_amounts or settings.chaos_blockers:  # If amounts are random, they need to be maxed out to properly generate random values
        settings.BLockerEntryCount = [1000, 1000, 1000, 1000, 1000, 1000, 1000, settings.blocker_7]
        # If Helm is shuffled with the rest of the levels, this algorithm should settle its value
        if settings.shuffle_helm_location:
            settings.BLockerEntryCount[7] = 1000
        # Chaos B. Lockers will be determined as we arrive at them - blank all of them out except for Helm for now
        if settings.chaos_blockers:
            settings.BLockerEntryItems[0] = BarrierItems.GoldenBanana
            settings.BLockerEntryItems[1] = BarrierItems.GoldenBanana
            settings.BLockerEntryItems[2] = BarrierItems.GoldenBanana
            settings.BLockerEntryItems[3] = BarrierItems.GoldenBanana
            settings.BLockerEntryItems[4] = BarrierItems.GoldenBanana
            settings.BLockerEntryItems[5] = BarrierItems.GoldenBanana
            settings.BLockerEntryItems[6] = BarrierItems.GoldenBanana
            if settings.shuffle_helm_location:
                settings.BLockerEntryItems[7] = BarrierItems.GoldenBanana
            else:
                # If guaranteed to be 8, Helm will be a max roll of a random item
                settings.BLockerEntryCount[7] = ceil(settings.blocker_limits[settings.BLockerEntryItems[7]] * settings.chaos_ratio)
        # Add a buffer to the Helm B. Locker value if it's your last B. Locker. This should make it less likely you need every item available to enter Helm.
        # This protection does not apply if your last B. Locker could be a huge number. You'll have to face the music then.
        settings.BLockerEntryCount[7] = min(
            ceil(settings.BLockerEntryCount[7] / BLOCKER_MAX), max(settings.BLockerEntryCount[7], ceil(settings.blocker_limits[settings.BLockerEntryItems[7]] * BLOCKER_MAX))
        )
    # We also need to remember T&S values in an array as we'll overwrite the settings value in the process of determining location availability
    initialTNS = [
        settings.troff_0,
        settings.troff_1,
        settings.troff_2,
        settings.troff_3,
        settings.troff_4,
        settings.troff_5,
        settings.troff_6,
        settings.troff_7,
    ]
    # Reshuffle these values to the correct level index
    ShuffleExits.UpdateLevelProgression(settings)

    maximumMinRoll = round((settings.blocker_max / BLOCKER_MAX) * BLOCKER_MIN)

    levelsProgressed = []
    foundProgressionKeyEvents = []

    number_of_progressable_levels = 8 if settings.shuffle_helm_location else 7
    # Until we've completed every level...
    while len(levelsProgressed) < number_of_progressable_levels:
        openLevels = GetAccessibleOpenLevels(spoiler)
        if not settings.chaos_blockers:
            # Pick a random accessible B. Locker
            maxEnterableBlocker = round(runningGBTotal * BLOCKER_MAX)
            accessibleIncompleteLevels = [level for level in openLevels if level not in levelsProgressed and settings.BLockerEntryCount[level] <= maxEnterableBlocker]
            # If we have no levels accessible, we need to lower a B. Locker count to make one accessible
            if len(accessibleIncompleteLevels) == 0:
                openUnprogressedLevels = [level for level in openLevels if level not in levelsProgressed]
                if len(openUnprogressedLevels) == 0:
                    raise Ex.FillException("E1: Hard level order shuffler failed to progress through levels.")
                # Next level chosen randomly (possible room for improvement here?) from accessible levels
                nextLevelToBeat = spoiler.settings.random.choice(openUnprogressedLevels)
                # If the level still isn't accessible, we have to truncate the required amount
                if settings.BLockerEntryCount[nextLevelToBeat] > maxEnterableBlocker:
                    # Each B. Locker must be greater than the previous one and at least a specified percentage of available GBs
                    highroll = min(settings.blocker_max, maxEnterableBlocker)  # Max max roll vs max progression roll
                    lowroll = min(maximumMinRoll, round(runningGBTotal * BLOCKER_MIN))  # Max min roll vs min progression roll
                    if lowroll > highroll:  # I think this impossible? It probably takes insane rng and very specific numbers
                        lowroll = highroll
                    settings.BLockerEntryCount[nextLevelToBeat] = spoiler.settings.random.randint(lowroll, highroll)
                accessibleIncompleteLevels = [nextLevelToBeat]
            else:
                nextLevelToBeat = spoiler.settings.random.choice(accessibleIncompleteLevels)
            # If this is the last level in a world where Helm is shuffled into the order and we need to maximize the last B. Locker...
            if settings.maximize_helm_blocker and settings.shuffle_helm_location and len(levelsProgressed) == (number_of_progressable_levels - 1):
                # Set the B. Locker value equal to the cap. If we aren't shuffling Helm, we'll sort it out at the end.
                settings.BLockerEntryCount[nextLevelToBeat] = min(settings.blocker_max, maxEnterableBlocker)
        # Chaos B. Lockers will always have to update the B. Locker
        else:
            accessibleIncompleteLevels = [level for level in openLevels if level not in levelsProgressed]
            if len(accessibleIncompleteLevels) == 0:
                raise Ex.FillException("E1-C: Hard level order shuffler failed to progress through levels.")
            nextLevelToBeat = spoiler.settings.random.choice(accessibleIncompleteLevels)
            # In CLO, we always recalculate the B. Locker items
            # Calculate the available quantity of the item for the B. Locker
            accessibleItems = spoiler.LogicVariables.ItemCounts()
            # In Chaos B. Lockers, we should try our best to avoid a 0
            # Determine which items have been found and could be eligible for this door
            eligibleTypes = [item for item in settings.blocker_limits.keys() if accessibleItems[item] > 0]
            # There can be only one Bean Locker, P. Locker, and C.C. Locker so they are not eligible if it already exists
            if BarrierItems.Bean in eligibleTypes and BarrierItems.Bean in settings.BLockerEntryItems:
                eligibleTypes.remove(BarrierItems.Bean)
            if BarrierItems.Pearl in eligibleTypes and BarrierItems.Pearl in settings.BLockerEntryItems:
                eligibleTypes.remove(BarrierItems.Pearl)
            if BarrierItems.CompanyCoin in eligibleTypes and BarrierItems.CompanyCoin in settings.BLockerEntryItems:
                eligibleTypes.remove(BarrierItems.CompanyCoin)
            # If there are no eligible items (staggeringly unlikely past the first level) then we'll have to settle for 0 GBs
            if len(eligibleTypes) == 0:
                settings.BLockerEntryItems[nextLevelToBeat] = BarrierItems.GoldenBanana
                progression_roll = 0
            else:
                settings.BLockerEntryItems[nextLevelToBeat] = spoiler.settings.random.choice(eligibleTypes)
                progression_roll = max(1, round(spoiler.settings.random.uniform(BLOCKER_MIN, BLOCKER_MAX) * accessibleItems[settings.BLockerEntryItems[nextLevelToBeat]]))
            # If this is the last level in a world where Helm is shuffled into the order, set the B. Locker value equal to the cap. If we aren't shuffling Helm, we'll sort it out at the end.
            if settings.shuffle_helm_location and len(levelsProgressed) == (number_of_progressable_levels - 1):
                # This will likely be a max roll but in some rare circumstances it may not be due to needing something out of your last progression level extremely early
                settings.BLockerEntryCount[nextLevelToBeat] = min(
                    ceil(settings.blocker_limits[settings.BLockerEntryItems[nextLevelToBeat]] * settings.chaos_ratio), round(BLOCKER_MAX * accessibleItems[settings.BLockerEntryItems[nextLevelToBeat]])
                )
            # Otherwise, generate a random value
            else:
                # Roll 8 random values and take the nth one to get an approximation of what the nth most expensive random B. Locker might be if all of them were of this item
                # n in this scenario is the nth level to be entered
                # This also prevents the item availability-based values from overtaking the maximum value
                assorted_random_values = []
                for i in range(9):
                    assorted_random_values.append(spoiler.settings.random.randint(1, ceil(settings.blocker_limits[settings.BLockerEntryItems[nextLevelToBeat]] * settings.chaos_ratio)))
                assorted_random_values.sort()
                settings.BLockerEntryCount[nextLevelToBeat] = min(progression_roll, assorted_random_values[len(levelsProgressed)])
        levelsProgressed.append(nextLevelToBeat)

        # Determine the Kong, GB, and Move accessibility from this level
        # If we get keys (and thus level progression) from the boss...
        if not isKeyItemRando:
            # Block the ability to complete the boss of every level we could complete but haven't yet (including this one)
            # This allows logic to get items from any other accessible level to beat this one
            BlockCompletionOfLevelSet(settings, accessibleIncompleteLevels)
        spoiler.Reset()
        accessible = GetAccessibleLocations(spoiler, [], SearchMode.GetReachable)
        runningGBTotal = spoiler.LogicVariables.GoldenBananas

        # -------------------------------------------------------------------------------------------------------------------------------------------
        # This chunk of code is here if we need to lower T&S values for whatever reason. This was the original attempt for CLO + item rando w/ keys.
        # This is no longer believed to be necessary, but preserved here in case we need to revert because it mostly worked.
        # -------------------------------------------------------------------------------------------------------------------------------------------
        # If at any moment we can get keys, let's see if we found any here
        # if isKeyItemRando:
        #     # Until we know a new level is accessible...
        #     while 1:
        #         openLevels = GetAccessibleOpenLevels(spoiler)
        #         # If we haven't found all the levels and have progressed through all open levels, we need to lower the CB requirement of one or more bosses for progression
        #         if len(openLevels) < 7 and len(openLevels) == len(levelsProgressed):
        #             bossLocations = [location for id, location in spoiler.LocationList.items() if location.type == Types.Key and location.level in levelsProgressed]
        #             shuffle(bossLocations)
        #             priorityBossLocation = None
        #             priorityStrength = -1
        #             # Loop through the boss locations, looking for the most likely progression candidate
        #             for bossLocation in bossLocations:
        #                 # If this location has nothing, don't even pretend to consider it
        #                 if bossLocation.item is None or bossLocation.item == Items.NoItem:
        #                     continue
        #                 # If this one is already reachable, skip
        #                 availableCBs = sum(spoiler.LogicVariables.ColoredBananas[bossLocation.level])
        #                 if availableCBs < settings.BossBananas[bossLocation.level]:  # Note we track against current values so we take into account already-lowered ones
        #                     # Absolute top priority for boss rewards is barrels - this can lock other bosses
        #                     if bossLocation.item == Items.Barrels:
        #                         priorityBossLocation = bossLocation
        #                         priorityStrength = 1000
        #                     # Next up is Keys - these can directly lock lobbies
        #                     itemOnBoss = ItemList[bossLocation.item]
        #                     if itemOnBoss.type == Types.Key and priorityStrength < 100:
        #                         priorityBossLocation = bossLocation
        #                         priorityStrength = 100
        #                     # Next up is Swim - if this is shuffled it locks a lobby
        #                     if bossLocation.item == Items.Swim and priorityStrength < 99:
        #                         priorityBossLocation = bossLocation
        #                         priorityStrength = 99
        #                     # Next up is Vines - if this is shuffled it sometimes locks a lobby but is also often locking a lot of things
        #                     if bossLocation.item == Items.Vines and priorityStrength < 98:
        #                         priorityBossLocation = bossLocation
        #                         priorityStrength = 98
        #                     # Next up is Guns/Instruments - these are more likely to lock Kongs which unlock Keys
        #                     if bossLocation.item in ItemPool.Guns(settings) or bossLocation.item in ItemPool.Instruments(settings):
        #                         priorityBossLocation = bossLocation
        #                         priorityStrength = 50
        #                     # Other boss rewards of interest would be moves with no particular priority
        #                     elif itemOnBoss.type == Types.Shop and priorityStrength < 10:
        #                         priorityBossLocation = bossLocation
        #                         priorityStrength = 10
        #                     # Very low priority reward moves are Oranges and Shockwave/Camera
        #                     elif itemOnBoss.type in (Types.TrainingBarrel, Types.Shockwave) and priorityStrength < 9:
        #                         priorityBossLocation = bossLocation
        #                         priorityStrength = 9
        #                     # Zero priority rewards is basically everything else
        #                     elif priorityStrength < 0:
        #                         priorityBossLocation = bossLocation
        #                         priorityStrength = 0
        #                     # The rest won't be locking progression so don't need to be lowered
        #             if priorityBossLocation is None:
        #                 # If we've already lowered all the T&S we can, then that's a fill error
        #                 raise Ex.FillException("E2: Hard level order shuffler failed to progress through levels.")
        #             randomlyRolledRatio = initialTNS[priorityBossLocation.level] / settings.troff_max
        #             settings.BossBananas[priorityBossLocation.level] = round(availableCBs * randomlyRolledRatio)
        #             accessibleMoves = [
        #                 spoiler.LocationList[x].item
        #                 for x in accessible
        #                 if spoiler.LocationList[x].item != Items.NoItem
        #                 and spoiler.LocationList[x].item is not None
        #                 and ItemList[spoiler.LocationList[x].item].type in (Types.TrainingBarrel, Types.Shop, Types.Shockwave)
        #             ]
        #             if priorityBossLocation.item in accessibleMoves:
        #                 accessibleMoves.remove(priorityBossLocation.item)
        #             ownedMoves[priorityBossLocation.level] = accessibleMoves
        #             ownedKongs[priorityBossLocation.level] = spoiler.LogicVariables.GetKongs()
        #             # Now that this boss location is accessible, let's see what's new and then repeat this loop in case we didn't find a new key
        #             spoiler.Reset()
        #             accessible = GetAccessibleLocations(spoiler, [], SearchMode.GetReachable)
        #         else:
        #             # To break out of this loop, we either have a level we can progress to or we've just found all the levels
        #             break

        # If we acquire keys in the traditional way, we go get this level's boss key
        if not isKeyItemRando:
            # Determine if the level we picked was a level progression key
            if not settings.open_lobbies:
                lobbyIndex = -1
                for key in settings.level_order.keys():
                    if settings.level_order[key] == nextLevelToBeat:
                        lobbyIndex = key - 1
                        break
                foundKeyEvent = KeyEvents[lobbyIndex]
                # If we need this key to open new lobbies, it's a progression key
                if foundKeyEvent in settings.krool_keys_required and foundKeyEvent != Events.FactoryKeyTurnedIn:
                    # If Helm is shuffled among other levels, Keys 6 and 7 become progression keys
                    if settings.shuffle_helm_location or foundKeyEvent not in [
                        Events.CavesKeyTurnedIn,
                        Events.CastleKeyTurnedIn,
                    ]:
                        foundProgressionKeyEvents.append(foundKeyEvent)
            eligibleProgressionKeyEvents = [event for event in foundProgressionKeyEvents]
            # Keys 6 and 7 are useless in isolation - they aren't progression unless you have both
            if Events.CavesKeyTurnedIn in eligibleProgressionKeyEvents and Events.CastleKeyTurnedIn not in eligibleProgressionKeyEvents:
                eligibleProgressionKeyEvents.remove(Events.CavesKeyTurnedIn)
            if Events.CastleKeyTurnedIn in eligibleProgressionKeyEvents and Events.CavesKeyTurnedIn not in eligibleProgressionKeyEvents:
                eligibleProgressionKeyEvents.remove(Events.CastleKeyTurnedIn)
            # If we've progressed through all open levels, then we need to pick a progression key we've found to acquire and set that level's Troff n Scoff
            if len(openLevels) == len(levelsProgressed) and any(eligibleProgressionKeyEvents):
                chosenKeyEvent = spoiler.settings.random.choice(eligibleProgressionKeyEvents)
                foundProgressionKeyEvents.remove(chosenKeyEvent)
                # Determine what levels need to be completed
                levelsToCompleteBoss = []
                if chosenKeyEvent == Events.JapesKeyTurnedIn:
                    spoiler.LogicVariables.Events.append(Events.JapesKeyTurnedIn)
                    levelsToCompleteBoss.append(settings.level_order[1])
                elif chosenKeyEvent == Events.AztecKeyTurnedIn:
                    spoiler.LogicVariables.Events.append(Events.AztecKeyTurnedIn)
                    levelsToCompleteBoss.append(settings.level_order[2])
                elif chosenKeyEvent == Events.GalleonKeyTurnedIn:
                    spoiler.LogicVariables.Events.append(Events.GalleonKeyTurnedIn)
                    levelsToCompleteBoss.append(settings.level_order[4])
                elif chosenKeyEvent == Events.ForestKeyTurnedIn:
                    spoiler.LogicVariables.Events.append(Events.ForestKeyTurnedIn)
                    levelsToCompleteBoss.append(settings.level_order[5])
                elif chosenKeyEvent in [Events.CavesKeyTurnedIn, Events.CastleKeyTurnedIn]:
                    spoiler.LogicVariables.Events.append(Events.CavesKeyTurnedIn)
                    spoiler.LogicVariables.Events.append(Events.CastleKeyTurnedIn)
                    levelsToCompleteBoss.append(settings.level_order[6])
                    levelsToCompleteBoss.append(settings.level_order[7])
                for bossCompletedLevel in levelsToCompleteBoss:
                    availableCBs = sum(spoiler.LogicVariables.ColoredBananas[bossCompletedLevel])
                    # If we don't have enough CBs to beat the boss per the settings-determined value
                    if availableCBs < initialTNS[bossCompletedLevel]:
                        # Reduce the requirement to an amount guaranteed to be available, based on the ratio of the initial T&S roll
                        randomlyRolledRatio = initialTNS[bossCompletedLevel] / settings.troff_max
                        settings.BossBananas[bossCompletedLevel] = round(availableCBs * randomlyRolledRatio)
                    else:
                        settings.BossBananas[bossCompletedLevel] = initialTNS[bossCompletedLevel]
                    ownedKongs[bossCompletedLevel] = spoiler.LogicVariables.GetKongs()
                    accessibleMoves = [
                        spoiler.LocationList[x].item
                        for x in accessible
                        if spoiler.LocationList[x].item != Items.NoItem
                        and spoiler.LocationList[x].item is not None
                        and ItemList[spoiler.LocationList[x].item].type in (Types.TrainingBarrel, Types.Shop, Types.Shockwave, Types.Climbing)
                    ]
                    ownedMoves[bossCompletedLevel] = accessibleMoves
                # After unblocking at least one T&S, the next loop needs the logic variables to know new lobbies are accessible
                # We've now made the key on this boss accessible, so this iteration should be identical plus keys from the unblocked bosses
                spoiler.Reset()
                GetAccessibleLocations(spoiler, [], SearchMode.GetReachable)

    # For any boss location behind a T&S we didn't lower...
    bossLocations = [
        location
        for id, location in spoiler.LocationList.items()
        if location.type == Types.Key and location.level in levelsProgressed and location.level != Levels.HideoutHelm and settings.BossBananas[location.level] >= initialTNS[location.level]
    ]
    for bossLocation in bossLocations:
        # For any level we explicitly blocked, undo the blocking
        if settings.BossBananas[bossLocation.level] > 500:
            # We should have access to everything by this point
            settings.BossBananas[bossLocation.level] = initialTNS[bossLocation.level]
        # For any level we haven't lowered yet, assume we own everything
        if bossLocation.level not in ownedKongs.keys():
            ownedKongs[bossLocation.level] = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
            ownedMoves[bossLocation.level] = allMoves
        # -------------------------------------------------------------------------------------------------------------------------------------------
        # This chunk of code is here if we need to lower T&S values for whatever reason. This was the original attempt for CLO + item rando w/ keys.
        # This is no longer believed to be necessary, but preserved here in case we need to revert because it mostly worked.
        # -------------------------------------------------------------------------------------------------------------------------------------------
        # If boss rewards could be anything, we have to make sure they're accessible independent of all else
        # if isKeyItemRando:
        #     bossReward = bossLocation.item
        #     # If the boss reward doesn't contain progression, it's fine
        #     if bossReward is None or ItemList[bossReward].type not in (Types.TrainingBarrel, Types.Shop, Types.Shockwave, Types.Key):
        #         continue
        #     # You never have the boss reward when fighting it, so remove it from consideration for boss placement
        #     if bossReward in ownedMoves[bossLocation.level]:
        #         ownedMoves[bossLocation.level].remove(bossReward)
        #     # If it could contain progression, place a dummy item there and see if we can reach it
        #     bossLocation.PlaceItem(spoiler, Items.TestItem)
        #     spoiler.Reset()
        #     accessible = GetAccessibleLocations(spoiler, [], SearchMode.GetReachable)
        #     if not spoiler.LogicVariables.found_test_item:
        #         # If we can't reach it eventually in this world state, then we need to lower this T&S
        #         randomlyRolledRatio = initialTNS[bossLocation.level] / settings.troff_max
        #         availableCBs = sum(spoiler.LogicVariables.ColoredBananas[bossLocation.level])
        #         settings.BossBananas[bossLocation.level] = round(availableCBs * randomlyRolledRatio)
        #         accessibleMoves = [
        #             spoiler.LocationList[x].item
        #             for x in accessible
        #             if spoiler.LocationList[x].item != Items.NoItem
        #             and spoiler.LocationList[x].item is not None
        #             and ItemList[spoiler.LocationList[x].item].type in (Types.TrainingBarrel, Types.Shop, Types.Shockwave)
        #         ]
        #         ownedMoves[bossLocation.level] = accessibleMoves
        #         ownedKongs[bossLocation.level] = spoiler.LogicVariables.GetKongs()
        #     # Put it back so we don't accidentally an item
        #     bossLocation.PlaceItem(spoiler, bossReward)
    # If we're not shuffling Helm with the rest of the levels, we need to sort out its B. Locker value here
    if not settings.shuffle_helm_location:
        mostExpensiveBLocker = max(settings.BLockerEntryCount[0:7])
        settings.BLockerEntryCount[7] = settings.blocker_7  # Reset the buffer that we applied earlier (Chaos B. Lockers is about to ignore this and that's good)
        # Chaos B. Lockers needs to also update the Helm B. Locker - max roll whatever the item there is
        if settings.chaos_blockers:
            settings.BLockerEntryCount[7] = ceil(settings.blocker_limits[settings.BLockerEntryItems[7]] * settings.chaos_ratio)
        # Because we might not have sorted the B. Lockers when they're randomly generated, Helm might be a surprisingly low number if it's not maximized
        elif settings.randomize_blocker_required_amounts and not settings.maximize_helm_blocker and settings.BLockerEntryCount[7] < mostExpensiveBLocker:
            # Ensure that Helm is the most expensive B. Locker
            # This may raise the Helm B. Locker and in some ***rare*** scenarios violate the B. Locker buffer, but it'll be a relatively small violation.
            settings.BLockerEntryCount[7] = spoiler.settings.random.randint(mostExpensiveBLocker, settings.blocker_max)
    # Only if keys are shuffled off of bosses do we need to reshuffle the bosses
    if not isKeyItemRando:
        # Place boss locations based on kongs and moves found for each level
        # We only need to shuffle bosses based on these calculated items if they aren't placed already
        if not spoiler.settings.boss_plando:
            ShuffleBossesBasedOnOwnedItems(spoiler, ownedKongs, ownedMoves)
        settings.owned_kongs_by_level = ownedKongs
        settings.owned_moves_by_level = ownedMoves

    # After setting all the progression, make sure we did it right
    # Technically the coin logic check after this will cover it, but this will help identify issues better
    spoiler.Reset()
    if not GetAccessibleLocations(spoiler, [], SearchMode.CheckAllReachable):
        raise Ex.GameNotBeatableException("Complex progression generation prevented 101%.")


def GetAccessibleOpenLevels(spoiler: Spoiler) -> List[int]:
    """Return the list of levels (not lobbies) you have access to after running GetAccessibleLocations()."""
    lobbyAccessEvents = [event for event in spoiler.LogicVariables.Events if event >= Events.JapesLobbyAccessed and event <= Events.HelmLobbyTraversable]
    accessibleOpenLevels = []
    if Events.JapesLobbyAccessed in lobbyAccessEvents:
        accessibleOpenLevels.append(Levels.JungleJapes)
    if Events.AztecLobbyAccessed in lobbyAccessEvents:
        # Also make sure we can do anything in Aztec. BONUS: if your DK portal is random the odds are very high it's not behind the vines, so this will suffice.
        if (
            spoiler.LogicVariables.vines
            or (spoiler.LogicVariables.tiny and spoiler.LogicVariables.twirl)
            or spoiler.LogicVariables.CanPhase()
            or spoiler.settings.dk_portal_location_rando_v2 != DKPortalRando.off
        ):
            accessibleOpenLevels.append(Levels.AngryAztec)
    if Events.FactoryLobbyAccessed in lobbyAccessEvents:
        accessibleOpenLevels.append(Levels.FranticFactory)
    if Events.GalleonLobbyAccessed in lobbyAccessEvents:
        accessibleOpenLevels.append(Levels.GloomyGalleon)
    if Events.ForestLobbyAccessed in lobbyAccessEvents:
        accessibleOpenLevels.append(Levels.FungiForest)
    if Events.CavesLobbyAccessed in lobbyAccessEvents:
        accessibleOpenLevels.append(Levels.CrystalCaves)
    if Events.CastleLobbyAccessed in lobbyAccessEvents:
        accessibleOpenLevels.append(Levels.CreepyCastle)
    # Not only do we need Helm Lobby access, we also need to make sure we can traverse it to logically enter it
    if spoiler.settings.shuffle_helm_location and Events.HelmLobbyAccessed in lobbyAccessEvents and Events.HelmLobbyTraversable in lobbyAccessEvents:
        accessibleOpenLevels.append(Levels.HideoutHelm)
    return accessibleOpenLevels


def BlockAccessToLevel(settings: Settings, level: int) -> None:
    """Assume the level index passed in is the furthest level you have access to in the level order."""
    for i in range(0, 8):
        if i >= level - 1:
            # This level and those after it are locked out
            settings.BLockerEntryCount[i] = 1000
            if i < 7:
                settings.BossBananas[i] = 1000
        else:
            # Previous levels assumed accessible
            settings.BLockerEntryCount[i] = 0
            if i < 7:
                settings.BossBananas[i] = 0
    # Update values based on actual level progression
    ShuffleExits.UpdateLevelProgression(settings)


def BlockCompletionOfLevelSet(settings: Settings, lockedLevels):
    """Prevent acquiring the keys of the levels provided."""
    for i in range(0, 7):
        if i in lockedLevels:
            # This level's boss is incompletable
            settings.BossBananas[i] = 1000


def Generate_Spoiler(spoiler: Spoiler) -> Tuple[bytes, Spoiler]:
    """Generate a complete spoiler based on input settings."""
    # Check for settings incompatibilities
    CheckForIncompatibleSettings(spoiler.settings)
    if spoiler.settings.wrinkly_hints == WrinklyHints.fixed_racing:
        ValidateFixedHints(spoiler.settings)
    # Reset LocationList for a new fill
    if not spoiler.settings.archipelago:
        spoiler.ResetLocationList()
    # Initiate kasplat map with default
    spoiler.InitKasplatMap()
    # Handle misc randomizations
    ShuffleMisc(spoiler)
    if spoiler.settings.archipelago:
        return
    # Handle Loading Zones - this will handle LO and LZR appropriately
    if spoiler.settings.shuffle_loading_zones != ShuffleLoadingZones.none:
        ShuffleExits.ExitShuffle(spoiler)
        spoiler.UpdateExits()
    # Handle Item Fill
    if spoiler.settings.move_rando != MoveRando.off or spoiler.settings.kong_rando or any(spoiler.settings.shuffled_location_types):
        FillWorld(spoiler)
    else:
        # Just check if normal item locations are beatable with given settings
        ItemPool.PlaceConstants(spoiler)
        if not GetAccessibleLocations(spoiler, [], SearchMode.CheckBeatable):
            raise Ex.VanillaItemsGameNotBeatableException("Game unbeatable.")
    CorrectBossKongLocations(spoiler)
    GeneratePlaythrough(spoiler)
    compileMicrohints(spoiler)
    if spoiler.settings.wrinkly_hints != WrinklyHints.off:
        compileHints(spoiler)
    if spoiler.settings.spoiler_hints != SpoilerHints.off:
        compileSpoilerHints(spoiler)
    spoiler.Reset()
    ShuffleExits.Reset(spoiler)
    spoiler.createJson()
    js.postMessage("Patching ROM...")
    # print(spoiler)
    # print(spoiler.json)
    patch_data, password = ApplyRandomizer.patching_response(spoiler)
    return patch_data, spoiler, password


class ItemReference:
    """Class to store information regarding an item's location."""

    def __init__(self, item: Items, item_name: str, locations):
        """Initialize with given parameters."""
        self.item = item
        self.item_name = item_name
        self.locations = [locations] if isinstance(locations, str) else locations

    def setLocation(self, index: int, new_name: str):
        """Set new name for location."""
        self.locations[index] = new_name


def ShuffleMisc(spoiler: Spoiler) -> None:
    """Shuffle miscellaneous objects outside of main fill algorithm, including Kasplats, Bonus barrels, and bananaport warps."""
    resetCustomLocations(spoiler)
    ResetPorts()
    if spoiler.settings.bananaport_placement_rando != ShufflePortLocations.off:
        port_replacements = {}
        port_human_replacements = {}
        ShufflePorts(spoiler, port_replacements, port_human_replacements)
        spoiler.warp_locations = port_replacements
        spoiler.human_warps = port_human_replacements
    if spoiler.settings.progressive_hint_item != ProgressiveHintItem.off:
        SetProgressiveHintDoorLogic(spoiler)
    # T&S and Wrinkly Door Shuffle
    if spoiler.settings.vanilla_door_rando:  # Includes Dos' Doors
        ShuffleVanillaDoors(spoiler)
        if spoiler.settings.dk_portal_location_rando_v2 != DKPortalRando.off:
            ShuffleDoors(spoiler, True)
    elif (
        spoiler.settings.wrinkly_location_rando
        or spoiler.settings.tns_location_rando
        or spoiler.settings.remove_wrinkly_puzzles
        or spoiler.settings.dk_portal_location_rando_v2 != DKPortalRando.off
        or (spoiler.settings.progressive_hint_item != ProgressiveHintItem.off and Types.Hint in spoiler.settings.shuffled_location_types)
    ):
        ShuffleDoors(spoiler, False)
    if Types.Hint in spoiler.settings.shuffled_location_types:
        UpdateDoorLevels(spoiler)
    # Handle Crown Placement
    if spoiler.settings.crown_placement_rando:
        crown_replacements = {}
        crown_human_replacements = {}
        ShuffleCrowns(spoiler, crown_replacements, crown_human_replacements)
        spoiler.crown_locations = crown_replacements
        spoiler.human_crowns = dict(sorted(crown_human_replacements.items()))
    # Handle Bananaports
    if spoiler.settings.bananaport_rando in (BananaportRando.crossmap_coupled, BananaportRando.crossmap_decoupled):
        replacements = []
        human_replacements = {}
        ShuffleWarpsCrossMap(
            spoiler,
            replacements,
            human_replacements,
            spoiler.settings.bananaport_rando == BananaportRando.crossmap_coupled,
            spoiler.settings.warp_level_list_selected,
        )
        spoiler.bananaport_replacements = replacements.copy()
        spoiler.human_warp_locations = human_replacements
    LinkWarps(spoiler)
    # Handle kasplats - this is the first VerifyWorld check, all shuffles affecting Locations must be before this one
    KasplatShuffle(spoiler, spoiler.LogicVariables)
    spoiler.human_kasplats = {}
    spoiler.UpdateKasplats(spoiler.LogicVariables.kasplat_map)
    # Enemy Rando
    spoiler.enemy_rando_data = {}
    spoiler.pkmn_snap_data = []
    if spoiler.settings.enemy_rando:
        randomize_enemies_0(spoiler)
    # Handle bonus barrels
    if (
        spoiler.settings.bonus_barrels in (MinigameBarrels.random, MinigameBarrels.selected)
        or spoiler.settings.helm_barrels == MinigameBarrels.random
        or spoiler.settings.training_barrels_minigames == MinigameBarrels.random
    ):
        BarrelShuffle(spoiler.settings)
        spoiler.UpdateBarrels()
    # CB Shuffle
    if spoiler.settings.cb_rando_enabled:
        ShuffleCBs(spoiler)
    # Coin Shuffle
    if spoiler.settings.coin_rando:
        ShuffleCoins(spoiler)
    # Random Patches
    if spoiler.settings.random_patches:
        human_patches = {}
        spoiler.human_patches = ShufflePatches(spoiler, human_patches).copy()
    if spoiler.settings.random_fairies:
        ShuffleFairyLocations(spoiler)
    if spoiler.settings.shuffle_shops:
        ShuffleShopLocations(spoiler)
    # Crate Shuffle
    if spoiler.settings.random_crates:
        human_crates = {}
        spoiler.human_crates = ShuffleMelonCrates(spoiler, human_crates).copy()
    # Populate location references
    spoiler.location_references = [
        # DK Moves
        ItemReference(Items.BaboonBlast, "Baboon Blast", "DK Japes Cranky"),
        ItemReference(Items.StrongKong, "Strong Kong", "DK Aztec Cranky"),
        ItemReference(Items.GorillaGrab, "Gorilla Grab", "DK Factory Cranky"),
        ItemReference(Items.Coconut, "Coconut Gun", "DK Japes Funky"),
        ItemReference(Items.Bongos, "Bongo Blast", "DK Aztec Candy"),
        # Diddy Moves
        ItemReference(Items.ChimpyCharge, "Chimpy Charge", "Diddy Japes Cranky"),
        ItemReference(Items.RocketbarrelBoost, "Rocketbarrel Boost", "Diddy Aztec Cranky"),
        ItemReference(Items.SimianSpring, "Simian Spring", "Diddy Factory Cranky"),
        ItemReference(Items.Peanut, "Peanut Popguns", "Diddy Japes Funky"),
        ItemReference(Items.Guitar, "Guitar Gazump", "Diddy Aztec Candy"),
        # Lanky Moves
        ItemReference(Items.Orangstand, "Orangstand", "Lanky Japes Cranky"),
        ItemReference(Items.BaboonBalloon, "Baboon Balloon", "Lanky Factory Cranky"),
        ItemReference(Items.OrangstandSprint, "Orangstand Sprint", "Lanky Caves Cranky"),
        ItemReference(Items.Grape, "Grape Shooter", "Lanky Japes Funky"),
        ItemReference(Items.Trombone, "Trombone Tremor", "Lanky Aztec Candy"),
        # Tiny Moves
        ItemReference(Items.MiniMonkey, "Mini Monkey", "Tiny Japes Cranky"),
        ItemReference(Items.PonyTailTwirl, "Pony Tail Twirl", "Tiny Factory Cranky"),
        ItemReference(Items.Monkeyport, "Monkeyport", "Tiny Caves Cranky"),
        ItemReference(Items.Feather, "Feather Bow", "Tiny Japes Funky"),
        ItemReference(Items.Saxophone, "Saxophone Slam", "Tiny Aztec Candy"),
        # Chunky Moves
        ItemReference(Items.HunkyChunky, "Hunky Chunky", "Chunky Japes Cranky"),
        ItemReference(Items.PrimatePunch, "Primate Punch", "Chunky Factory Cranky"),
        ItemReference(Items.GorillaGone, "Gorilla Gone", "Chunky Caves Cranky"),
        ItemReference(Items.Pineapple, "Pineapple Launcher", "Chunky Japes Funky"),
        ItemReference(Items.Triangle, "Triangle Trample", "Chunky Aztec Candy"),
        # Gun Upgrades
        ItemReference(Items.HomingAmmo, "Homing Ammo", "Shared Forest Funky"),
        ItemReference(Items.SniperSight, "Sniper Scope", "Shared Castle Funky"),
        ItemReference(Items.ProgressiveAmmoBelt, "Progressive Ammo Belt", ["Shared Factory Funky", "Shared Caves Funky"]),
        ItemReference(Items.Camera, "Fairy Camera", "Banana Fairy Gift"),
        ItemReference(Items.Shockwave, "Shockwave", "Banana Fairy Gift"),
        # Basic Moves
        ItemReference(Items.Swim, "Diving", "Dive Barrel"),
        ItemReference(Items.Oranges, "Orange Throwing", "Orange Barrel"),
        ItemReference(Items.Barrels, "Barrel Throwing", "Barrel Barrel"),
        ItemReference(Items.Vines, "Vine Swinging", "Vine Barrel"),
        ItemReference(Items.Climbing, "Climbing", "Starting Move"),
        # Instrument Upgrades & Slams
        ItemReference(
            Items.ProgressiveInstrumentUpgrade,
            "Progressive Instrument Upgrade",
            ["Shared Galleon Candy", "Shared Caves Candy", "Shared Castle Candy"],
        ),
        ItemReference(
            Items.ProgressiveSlam,
            "Progressive Slam",
            ["Shared Isles Cranky", "Shared Forest Cranky", "Shared Castle Cranky"],
        ),
        # Kongs
        ItemReference(Items.Donkey, "Donkey Kong", "Starting Kong"),
        ItemReference(Items.Diddy, "Diddy Kong", "Japes Diddy Cage"),
        ItemReference(Items.Lanky, "Lanky Kong", "Llama Lanky Cage"),
        ItemReference(Items.Tiny, "Tiny Kong", "Aztec Tiny Cage"),
        ItemReference(Items.Chunky, "Chunky Kong", "Factory Chunky Cage"),
        # Shopkeepers
        ItemReference(Items.Cranky, "Cranky Kong", "Starting Item"),
        ItemReference(Items.Candy, "Candy Kong", "Starting Item"),
        ItemReference(Items.Funky, "Funky Kong", "Starting Item"),
        ItemReference(Items.Snide, "Snide", "Starting Item"),
        # Early Keys
        ItemReference(Items.JungleJapesKey, "Key 1", "Starting Key"),
        ItemReference(Items.AngryAztecKey, "Key 2", "Starting Key"),
        ItemReference(Items.FranticFactoryKey, "Key 3", "Starting Key"),
        ItemReference(Items.GloomyGalleonKey, "Key 4", "Starting Key"),
        # Late Keys
        ItemReference(Items.FungiForestKey, "Key 5", "Starting Key"),
        ItemReference(Items.CrystalCavesKey, "Key 6", "Starting Key"),
        ItemReference(Items.CreepyCastleKey, "Key 7", "Starting Key"),
        ItemReference(Items.HideoutHelmKey, "Key 8", "Starting Key"),
    ]
    # Item Rando
    spoiler.human_item_assignment = {}
    spoiler.settings.update_valid_locations(spoiler)


def ValidateFixedHints(settings: Settings) -> None:
    """Check for some known incompatibilities with the Fixed hint system ASAP so we don't waste time genning this seed."""
    if settings.logic_type == LogicType.nologic:
        raise Ex.SettingsIncompatibleException("No Logic is not compatible with fixed hints.")
    if not settings.shuffle_items:
        raise Ex.SettingsIncompatibleException("Item Randomizer must be enabled with Fixed hints.")
    if settings.win_condition_item != WinConditionComplex.beat_krool:
        raise Ex.SettingsIncompatibleException("Alternate win conditions will not work with Fixed hints.")
    if len(settings.starting_kong_list) != 2:
        raise Ex.SettingsIncompatibleException("Fixed hints require starting with exactly 2 Kongs.")
    if settings.enable_plandomizer and len(settings.plandomizer_dict["hints"]) > 5:
        raise Ex.SettingsIncompatibleException("Fixed hints are incompatible with more than 5 plandomized hints.")


def CheckForIncompatibleSettings(settings: Settings) -> None:
    """Check for known settings conflicts and throw an exception immediately."""
    found_incompatibilities = ""
    if not settings.fast_start_beginning_of_game:
        if settings.shuffle_loading_zones == ShuffleLoadingZones.all:
            found_incompatibilities += "Cannot turn off Fast Start with Loading Zones Randomized. "
        if settings.random_starting_region:
            found_incompatibilities += "Cannot turn off Fast Start with a Random Starting Location. "
        if not settings.start_with_slam:
            found_incompatibilities += "Cannot turn off Fast Start unless you are guaranteed to start with a Progressive Slam. "
        if Types.Cranky in settings.shuffled_location_types:
            found_incompatibilities += "Cannot turn off Fast start unless you start with Cranky. "
    if not settings.shuffle_items:
        if not settings.start_with_slam:
            found_incompatibilities += "Cannot turn off Item Randomizer without starting with a Progressive Slam. "
        if settings.training_barrels != TrainingBarrels.normal:
            found_incompatibilities += "Cannot turn off Item Randomizer without starting with all Training Moves. "
        if settings.climbing_status != ClimbingStatus.normal:
            found_incompatibilities += "Cannot turn off Item Randomizer without starting with Climbing. "
    if IsItemSelected(settings.hard_mode, settings.hard_mode_selected, HardModeSelected.water_is_lava, False):
        if settings.no_healing:
            found_incompatibilities += "Cannot turn on 'Water is Lava' whilst disabling healing. "
    if IsItemSelected(settings.hard_mode, settings.hard_mode_selected, HardModeSelected.angry_caves, False):
        if settings.perma_death:
            if settings.damage_amount == DamageAmount.quad or settings.damage_amount == DamageAmount.ohko:
                found_incompatibilities += "Cannot turn on 'Angry Caves' with a damage modifier higher than double damage with Irondonk enabled. "
    if not settings.is_valid_item_pool():
        found_incompatibilities += "Item pool is not a valid combination of items and cannot successfully fill the world. "
    if settings.krool_access and Items.HideoutHelmKey in settings.starting_keys_list_selected:
        found_incompatibilities += "Cannot start with Key 8 and guarantee Key 8 to be required at the same time. "
    if found_incompatibilities != "":
        raise Ex.SettingsIncompatibleException(found_incompatibilities)


def DebugCheckAllReachable(spoiler: Spoiler, owned, what_just_got_placed):
    """Immediately check if the world is 101%-able. Only used with extreme_debugging."""
    spoiler.Reset()
    reached_all = GetAccessibleLocations(spoiler, owned, SearchMode.CheckAllReachable)
    if not reached_all:
        print("red alert - we have just lost 101% after placing " + what_just_got_placed + "!")
