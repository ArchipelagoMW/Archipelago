"""File that shuffles loading zone exits."""

import js
import randomizer.Fill as Fill
import randomizer.Lists.Exceptions as Ex
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Settings import ActivateAllBananaports, RandomPrices, ShuffleLoadingZones, RemovedBarriersSelected, CrownEnemyDifficulty, CBRequirement
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Types import Types
from randomizer.Lists.ShufflableExit import ShufflableExits
from randomizer.LogicClasses import TransitionFront
from randomizer.Settings import Settings
from randomizer.Patching.Library.Generic import IsDDMSSelected, IsItemSelected, MEDAL_PROGRESSIVE_RATIOS

# Used when level order rando is ON
LobbyEntrancePool = [
    Transitions.IslesMainToJapesLobby,
    Transitions.IslesMainToAztecLobby,
    Transitions.IslesMainToFactoryLobby,
    Transitions.IslesMainToGalleonLobby,
    Transitions.IslesMainToForestLobby,
    Transitions.IslesMainToCavesLobby,
    Transitions.IslesMainToCastleLobby,
    Transitions.IslesMainToHelmLobby,
]

# Root is the starting spawn, which is the main area of DK Isles.
root = Regions.GameStart


def GetRootExit(spoiler, exitId):
    """Query the world root to return an exit with a matching exit id."""
    return [x for x in spoiler.RegionList[root].exits if x.assumed and x.exitShuffleId is not None and x.exitShuffleId == exitId][0]


def RemoveRootExit(spoiler, exit):
    """Remove an exit from the world root."""
    spoiler.RegionList[root].exits.remove(exit)


def AddRootExit(spoiler, exit):
    """Add an exit to the world root."""
    spoiler.RegionList[root].exits.append(exit)


def Reset(spoiler):
    """Reset shufflable exit properties set during shuffling."""
    for exit in ShufflableExits.values():
        exit.shuffledId = None
        exit.shuffled = False
    assumedExits = []
    for exit in [x for x in spoiler.RegionList[root].exits if x.assumed]:
        assumedExits.append(exit)
    for exit in assumedExits:
        RemoveRootExit(spoiler, exit)


def AttemptConnect(spoiler, frontExit, frontId, backExit, backId):
    """Attempt to connect two exits, checking if the world is valid if they are connected."""
    # Remove connections to world root
    settings = spoiler.settings
    frontReverse = None
    if not settings.decoupled_loading_zones:
        # Prevents an error if trying to assign an entrance back to itself
        if frontExit.back.reverse == backId:
            return False
        frontReverse = GetRootExit(spoiler, frontExit.back.reverse)
        RemoveRootExit(spoiler, frontReverse)
    backRootExit = GetRootExit(spoiler, backId)
    RemoveRootExit(spoiler, backRootExit)
    # Add connection between selected exits
    frontExit.shuffled = True
    frontExit.shuffledId = backId
    if not settings.decoupled_loading_zones:
        backReverse = ShufflableExits[backExit.back.reverse]
        backReverse.shuffled = True
        backReverse.shuffledId = frontExit.back.reverse
    # Attempt to verify world
    valid = Fill.VerifyWorld(spoiler)
    # If world is not valid, restore root connections and undo new connections
    if not valid:
        AddRootExit(spoiler, backRootExit)
        frontExit.shuffled = False
        frontExit.shuffledId = None
        if not settings.decoupled_loading_zones:
            AddRootExit(spoiler, frontReverse)
            backReverse.shuffled = False
            backReverse.shuffledId = None
    return valid


def ShuffleExitsInPool(spoiler, frontpool, backpool):
    """Shuffle exits within a specific pool."""
    settings = spoiler.settings
    NonTagRegions = [x for x in backpool if not spoiler.RegionList[ShufflableExits[x].back.regionId].tagbarrel]
    NonTagLeaves = [x for x in NonTagRegions if len(spoiler.RegionList[ShufflableExits[x].back.regionId].exits) == 1]
    settings.random.shuffle(NonTagLeaves)
    NonTagNonLeaves = [x for x in NonTagRegions if x not in NonTagLeaves]
    settings.random.shuffle(NonTagNonLeaves)

    TagRegions = [x for x in backpool if x not in NonTagRegions]
    TagLeaves = [x for x in TagRegions if len(spoiler.RegionList[ShufflableExits[x].back.regionId].exits) == 1]
    settings.random.shuffle(TagLeaves)
    TagNonLeaves = [x for x in TagRegions if x not in TagLeaves]
    settings.random.shuffle(TagNonLeaves)

    backpool = NonTagLeaves
    backpool.extend(NonTagNonLeaves)
    backpool.extend(TagLeaves)
    backpool.extend(TagNonLeaves)

    # Coupled is more restrictive and need to also order the front pool to lower rate of failures
    if not settings.decoupled_loading_zones:
        NonTagRegions = [x for x in frontpool if not spoiler.RegionList[ShufflableExits[x].back.regionId].tagbarrel]
        NonTagLeaves = [x for x in NonTagRegions if len(spoiler.RegionList[ShufflableExits[x].back.regionId].exits) == 1]
        settings.random.shuffle(NonTagLeaves)
        NonTagNonLeaves = [x for x in NonTagRegions if x not in NonTagLeaves]
        settings.random.shuffle(NonTagNonLeaves)

        TagRegions = [x for x in frontpool if x not in NonTagRegions]
        TagLeaves = [x for x in TagRegions if len(spoiler.RegionList[ShufflableExits[x].back.regionId].exits) == 1]
        settings.random.shuffle(TagLeaves)
        TagNonLeaves = [x for x in TagRegions if x not in TagLeaves]
        settings.random.shuffle(TagNonLeaves)

        frontpool = NonTagLeaves
        frontpool.extend(NonTagNonLeaves)
        frontpool.extend(TagLeaves)
        frontpool.extend(TagNonLeaves)
    else:
        settings.random.shuffle(frontpool)

    # For each back exit, select a random valid front entrance to attach to it
    while len(backpool) > 0:
        backId = backpool.pop(0)
        backExit = ShufflableExits[backId]
        # Filter origins to make sure that if this target requires a certain kong's access, then the entrance will be accessible by that kong
        origins = [x for x in frontpool if ShufflableExits[x].entryKongs.issuperset(backExit.regionKongs)]
        if not settings.decoupled_loading_zones and backExit.category is None:
            # In coupled, if both front & back are leaves, the result will be invalid
            origins = [x for x in origins if ShufflableExits[ShufflableExits[x].back.reverse].category is not None]
            # Also validate the entry & region kongs overlap in reverse direction
            origins = [x for x in origins if ShufflableExits[backExit.back.reverse].entryKongs.issuperset(ShufflableExits[ShufflableExits[x].back.reverse].regionKongs)]
        elif settings.decoupled_loading_zones and backExit.back.regionId in [
            Regions.JapesMinecarts,
            Regions.ForestMinecarts,
        ]:
            # In decoupled, we still have to prevent one-way minecart exits from leading to the minecarts themselves
            if Transitions.JapesCartsToMain in origins:
                origins.remove(Transitions.JapesCartsToMain)
            if Transitions.ForestCartsToMain in origins:
                origins.remove(Transitions.ForestCartsToMain)
        if len(origins) == 0:
            print("Failed to connect to " + backExit.name + ", found no suitable origins!")
            raise Ex.EntranceOutOfDestinations
        # Select a random origin
        for frontId in origins:
            frontExit = ShufflableExits[frontId]
            if AttemptConnect(spoiler, frontExit, frontId, backExit, backId):
                # print("Assigned " + frontExit.name + " --> " + backExit.name)
                frontpool.remove(frontId)
                if not settings.decoupled_loading_zones:
                    # If coupled, the opposite pairing also needs to be removed from the pool
                    # print("Assigned " + ShufflableExits[backExit.back.reverse].name + " --> " + ShufflableExits[frontExit.back.reverse].name)
                    frontpool.remove(backExit.back.reverse)
                    backpool.remove(frontExit.back.reverse)
                break
        if not frontExit.shuffled:
            print("Failed to connect to " + backExit.name + " from any of the remaining " + str(len(origins)) + " origins!")
            raise Ex.EntranceOutOfDestinations
        if len(frontpool) != len(backpool):
            print("Length of frontpool " + len(frontpool) + " and length of backpool " + len(backpool) + " do not match!")
            raise Ex.EntranceOutOfDestinations


def AssumeExits(spoiler, frontpool, backpool, newpool):
    """Split exit pool into front and back pools, and assumes exits reachable from root."""
    for i in range(len(newpool)):
        exitId = newpool[i]
        exit = ShufflableExits[exitId]
        # When coupled, only transitions which have a reverse path can be included in the pools
        if not spoiler.settings.decoupled_loading_zones and exit.back.reverse is None:
            continue
        # Don't shuffle the Aztec temples if they are not eligible to be shuffled
        if not spoiler.settings.shuffle_aztec_temples and exitId in (
            Transitions.AztecStartToTemple,
            Transitions.AztecTempleToStart,
            Transitions.AztecMainToLlama,
            Transitions.AztecLlamaToMain,
        ):
            continue
        # Don't shuffle the Prison if we're not automatically turning in keys
        if not spoiler.settings.auto_keys and exitId in (Transitions.IslesMainToPrison, Transitions.IslesPrisonToMain):
            continue
        # Shuffling Helm's location is opt-in
        if not spoiler.settings.shuffle_helm_location and exitId in (
            Transitions.IslesMainToHelmLobby,
            Transitions.IslesHelmLobbyToMain,
            Transitions.IslesToHelm,
            Transitions.HelmToIsles,
        ):
            continue
        # "front" is the entrance you go into, "back" is the exit you come out of
        frontpool.append(exitId)
        backpool.append(exitId)
        # Set up assumed connection
        # 1) Break connection
        exit.shuffledId = None
        exit.toBeShuffled = True
        # 2) Attach to root of world (DK Isles)
        newExit = TransitionFront(exit.back.regionId, lambda _: True, exitId, True)
        AddRootExit(spoiler, newExit)


def ShuffleExits(spoiler):
    """Shuffle exit pools depending on settings."""
    # Set up front and back entrance pools for each setting
    # Assume all shuffled exits reachable by default
    settings = spoiler.settings
    if settings.shuffle_loading_zones == ShuffleLoadingZones.levels:
        new_level_order = None
        # If we are restricted on kong locations, we need to carefully place levels in order to meet the kongs-by-level requirement
        if settings.kongs_for_progression and not (settings.shuffle_items and Types.Kong in settings.shuffled_location_types):
            new_level_order = GenerateLevelOrderWithRestrictions(settings)
        else:
            new_level_order = GenerateLevelOrderUnrestricted(settings)
        ShuffleLevelExits(settings, newLevelOrder=new_level_order)
        if settings.alter_switch_allocation:
            allocation = [
                settings.prog_slam_level_1,
                settings.prog_slam_level_2,
                settings.prog_slam_level_3,
                settings.prog_slam_level_4,
                settings.prog_slam_level_5,
                settings.prog_slam_level_6,
                settings.prog_slam_level_7,
                settings.prog_slam_level_8,
            ]
            for x in range(8):
                level = settings.level_order[x + 1]
                settings.switch_allocation[level] = allocation[x]
        if settings.cb_medal_behavior_new == CBRequirement.progressive:
            ratios = MEDAL_PROGRESSIVE_RATIOS.copy()
            if not IsItemSelected(settings.cb_rando_enabled, settings.cb_rando_list_selected, Levels.DKIsles):
                ratios[6] = 1
            allocation = [int(settings.medal_cb_req * x) for x in ratios]
            # ensures that progressive will never set a 0 for CB medal which would fuck logic
            allocation = [max(1, cb_req) for cb_req in allocation]
            for x in range(8):
                level = settings.level_order[x + 1]
                settings.medal_cb_req_level[level] = allocation[x]
        if settings.crown_enemy_difficulty == CrownEnemyDifficulty.progressive:
            # There's 4 levels of easy, 2 of medium, 2 of hard
            # Both Isles crowns will be a random difficulty.
            # One will either be easy or medium. The other will either be medium or hard.
            allocation = [CrownEnemyDifficulty.easy] * 4
            allocation.extend([CrownEnemyDifficulty.medium] * 2)
            allocation.extend([CrownEnemyDifficulty.hard] * 2)
            for x in range(8):
                level = settings.level_order[x + 1]
                settings.crown_difficulties[level] = allocation[x]
            settings.crown_difficulties[8] = settings.random.choice([CrownEnemyDifficulty.easy, CrownEnemyDifficulty.medium])
            settings.crown_difficulties[9] = settings.random.choice([CrownEnemyDifficulty.medium, CrownEnemyDifficulty.hard])

    elif settings.shuffle_loading_zones == ShuffleLoadingZones.all:
        frontpool = []
        backpool = []
        AssumeExits(spoiler, frontpool, backpool, list(ShufflableExits.keys()))
        # Shuffle each entrance pool
        ShuffleExitsInPool(spoiler, frontpool, backpool)
    # If levels rando is on, need to update Blocker and T&S requirements to match
    if settings.shuffle_loading_zones == ShuffleLoadingZones.levels:
        UpdateLevelProgression(settings)


def ExitShuffle(spoiler, skip_verification=False):
    """Facilitate shuffling of exits."""
    retries = 0
    while True:
        try:
            # Shuffle entrances based on settings
            ShuffleExits(spoiler)
            # Verify world by assuring all locations are still reachable
            if not skip_verification and not Fill.VerifyWorld(spoiler):
                raise Ex.EntrancePlacementException
            return
        except Ex.EntrancePlacementException:
            if retries == 20:
                js.postMessage("Entrance placement failed, out of retries.")
                raise Ex.EntranceAttemptCountExceeded
            retries += 1
            js.postMessage("Entrance placement failed. Retrying. Tries: " + str(retries))
            Reset(spoiler)


def UpdateLevelProgression(settings: Settings):
    """Update level progression and reorder variables to match the actual level order."""
    newBLockerEntryItems = settings.BLockerEntryItems.copy()
    newBLockerEntryCount = settings.BLockerEntryCount.copy()
    newBossBananas = settings.BossBananas.copy()
    lobbies = [
        Regions.JungleJapesLobby,
        Regions.AngryAztecLobby,
        Regions.FranticFactoryLobby,
        Regions.GloomyGalleonLobbyEntrance,
        Regions.FungiForestLobby,
        Regions.CrystalCavesLobby,
        Regions.CreepyCastleLobby,
        Regions.HideoutHelmLobby,
    ]
    for levelIndex in range(len(lobbies)):
        newIndex = levelIndex
        if settings.shuffle_loading_zones == ShuffleLoadingZones.levels:
            shuffledEntrance = ShufflableExits[LobbyEntrancePool[levelIndex]].shuffledId
            newDestRegion = ShufflableExits[shuffledEntrance].back.regionId
            # print(LobbyEntrancePool[levelIndex].name + " goes to " + newDestRegion.name)
            newIndex = lobbies.index(newDestRegion)
        newBLockerEntryItems[newIndex] = settings.BLockerEntryItems[levelIndex]
        newBLockerEntryCount[newIndex] = settings.BLockerEntryCount[levelIndex]
        newBossBananas[newIndex] = settings.BossBananas[levelIndex]
    settings.BLockerEntryItems = newBLockerEntryItems
    settings.BLockerEntryCount = newBLockerEntryCount
    settings.BossBananas = newBossBananas


def ShuffleLevelExits(settings: Settings, newLevelOrder: dict = None):
    """Shuffle level exits according to new level order if provided, otherwise shuffle randomly."""
    frontpool = LobbyEntrancePool.copy()
    backpool = LobbyEntrancePool.copy()

    if newLevelOrder is not None:
        for index, level in newLevelOrder.items():
            backpool[index - 1] = LobbyEntrancePool[level]
    else:
        settings.random.shuffle(frontpool)

    # Initialize reference variables
    lobby_entrance_map = {
        Transitions.IslesMainToJapesLobby: Levels.JungleJapes,
        Transitions.IslesMainToAztecLobby: Levels.AngryAztec,
        Transitions.IslesMainToFactoryLobby: Levels.FranticFactory,
        Transitions.IslesMainToGalleonLobby: Levels.GloomyGalleon,
        Transitions.IslesMainToForestLobby: Levels.FungiForest,
        Transitions.IslesMainToCavesLobby: Levels.CrystalCaves,
        Transitions.IslesMainToCastleLobby: Levels.CreepyCastle,
        Transitions.IslesMainToHelmLobby: Levels.HideoutHelm,
    }
    shuffledLevelOrder = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None}

    # For each back exit, select a random valid front entrance to attach to it
    # Assuming there are no inherently invalid level orders, but if there are, validation will check after this
    while len(backpool) > 0:
        backId = backpool.pop()
        backExit = ShufflableExits[backId]
        # Select a random origin
        frontId = frontpool.pop()
        frontExit = ShufflableExits[frontId]
        # Add connection between selected exits
        frontExit.shuffled = True
        frontExit.shuffledId = backId
        # print("Assigned " + frontExit.name + " --> " + backExit.name)
        # Add reverse connection
        backReverse = ShufflableExits[backExit.back.reverse]
        backReverse.shuffled = True
        backReverse.shuffledId = frontExit.back.reverse

        shuffledLevelOrder[lobby_entrance_map[frontId] + 1] = lobby_entrance_map[backId]
    settings.level_order = shuffledLevelOrder


def GenerateLevelOrderWithRestrictions(settings: Settings):
    """Generate a level order given starting kong and the need to find more kongs along the way."""
    # All methods here follow this Kongs vs level progression rule:
    # Must be able to have 2 kongs no later than level 2
    # Must be able to have 3 kongs no later than level 3
    # Must be able to have 4 kongs no later than level 4
    # Must be able to have 5 kongs no later than level 5
    # Valid Example:
    #   1. Caves - No kongs found
    #   2. Aztec - Can free 2nd kong here, other kong is move locked
    #   3. Japes - Can free 3rd kong here
    #   4. Galleon - Find move to free other kong from aztec
    #   5. Factory - Find last kong
    #   6. Castle
    #   7. Fungi
    if settings.hard_level_progression:  # Unless you're CLO - you get no such restrictions
        newLevelOrder = GenerateLevelOrderUnrestricted(settings)
    elif settings.starting_kongs_count == 1:
        newLevelOrder = GenerateLevelOrderForOneStartingKong(settings)
    else:
        newLevelOrder = GenerateLevelOrderForMultipleStartingKongs(settings)
    if None in newLevelOrder.values():
        raise Ex.EntrancePlacementException("Invalid level order with fewer than the 8 required main levels.")
    return newLevelOrder


def GenerateLevelOrderUnrestricted(settings):
    """Generate a level order without Kong placement restrictions."""
    newLevelOrder = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None}
    unplacedLevels = [
        Levels.JungleJapes,
        Levels.AngryAztec,
        Levels.FranticFactory,
        Levels.GloomyGalleon,
        Levels.FungiForest,
        Levels.CrystalCaves,
        Levels.CreepyCastle,
        Levels.HideoutHelm,
    ]
    if settings.enable_plandomizer:
        for i in range(len(newLevelOrder.keys())):
            if settings.plandomizer_dict["plando_level_order_" + str(i)] != -1:
                newLevelOrder[i + 1] = Levels(settings.plandomizer_dict["plando_level_order_" + str(i)])
                unplacedLevels.remove(newLevelOrder[i + 1])
    # If HideoutHelm is not in unplacedLevels, it was already assigned by the
    # plandomizer.
    if not settings.shuffle_helm_location and Levels.HideoutHelm in unplacedLevels:
        newLevelOrder[8] = Levels.HideoutHelm
        unplacedLevels.remove(Levels.HideoutHelm)
    for i in range(len(newLevelOrder.keys())):
        if newLevelOrder[i + 1] is None:
            # Helm can't be in levels 1 or 2 in Simple Level Order
            if not settings.hard_level_progression and i < 2:
                validLevels = [x for x in unplacedLevels if x != Levels.HideoutHelm]
            else:
                validLevels = unplacedLevels
            newLevelOrder[i + 1] = settings.random.choice(validLevels)
            unplacedLevels.remove(newLevelOrder[i + 1])
    return newLevelOrder


def GenerateLevelOrderForOneStartingKong(settings):
    """Generate a level order given only starting with one kong and the need to find more kongs along the way."""
    levelIndexChoices = {1, 2, 3, 4, 5, 6, 7, 8}
    # Place Helm if helm isn't in the pool
    if not settings.shuffle_helm_location:
        helmIndex = 8
        levelIndexChoices.remove(8)
    # Decide where Aztec will go
    # Diddy can reasonably make progress if Aztec is first level
    if settings.starting_kong == Kongs.diddy:
        aztecIndex = settings.random.randint(1, 4)
    else:
        aztecIndex = settings.random.randint(2, 4)
    levelIndexChoices.remove(aztecIndex)

    # Decide where Japes will go
    japesOptions = []
    # If Aztec is level 4, both of Japes/Factory need to be in level 1-3
    if aztecIndex == 4:
        # Tiny has no coins and no T&S access in Japes so it can't be first for her unless prices are free
        if settings.starting_kong == Kongs.tiny and settings.random_prices != RandomPrices.free:
            japesOptions = list(levelIndexChoices.intersection({2, 3}))
        else:
            japesOptions = list(levelIndexChoices.intersection({1, 3}))
    else:
        # Tiny has no coins and no T&S access in Japes so it can't be first for her unless prices are free
        if settings.starting_kong == Kongs.tiny and settings.random_prices != RandomPrices.free:
            japesOptions = list(levelIndexChoices.intersection({2, 3, 4, 5}))
        else:
            japesOptions = list(levelIndexChoices.intersection({1, 2, 3, 4, 5}))
    japesIndex = settings.random.choice(japesOptions)
    levelIndexChoices.remove(japesIndex)

    # Decide where Factory will go
    factoryOptions = []
    # If Aztec is level 4, both of Japes/Factory need to be in level 1-3
    if aztecIndex == 4:
        factoryOptions = list(levelIndexChoices.intersection({1, 2, 3}))
    # If Aztec is level 3, one of Japes/Factory needs to be in level 1-2 and other in level 1-5
    elif aztecIndex == 3:
        if japesIndex < 3:
            factoryOptions = list(levelIndexChoices.intersection({1, 2, 3, 4, 5}))
        else:
            factoryOptions = list(levelIndexChoices.intersection({1, 2}))
    # If Aztec is level 2 and don't start with diddy or chunky, one of Japes/Factory needs to be level 1 and other in level 3-5
    elif aztecIndex == 2 and settings.starting_kong != Kongs.diddy and settings.starting_kong != Kongs.chunky:
        if japesIndex == 1:
            factoryOptions = list(levelIndexChoices.intersection({3, 4, 5}))
        else:
            factoryOptions = list(levelIndexChoices.intersection({1}))
    # If Aztec is level 2 and start with chunky, one of Japes/Factory needs to be level 1-3 and other in level 3-5
    elif aztecIndex == 2 and settings.starting_kong == Kongs.chunky:
        if japesIndex in (1, 3):
            factoryOptions = list(levelIndexChoices.intersection({3, 4, 5}))
        else:
            factoryOptions = list(levelIndexChoices.intersection({1, 2, 3}))
    # If Aztec is level 1 or 2, one of Japes/Factory needs to be in level 1-4 and other in level 1-5
    else:
        if japesIndex < 5:
            factoryOptions = list(levelIndexChoices.intersection({1, 2, 3, 4, 5}))
        else:
            factoryOptions = list(levelIndexChoices.intersection({1, 2, 3, 4}))
    factoryIndex = settings.random.choice(factoryOptions)
    levelIndexChoices.remove(factoryIndex)

    # Helm can't be in levels 1 or 2
    if settings.shuffle_helm_location:
        helmOptions = list(levelIndexChoices.intersection({3, 4, 5, 6, 7, 8}))
        helmIndex = settings.random.choice(helmOptions)
        levelIndexChoices.remove(helmIndex)

    # Decide the remaining level order randomly
    remainingLevels = list(levelIndexChoices)
    settings.random.shuffle(remainingLevels)
    cavesIndex = remainingLevels.pop()
    galleonIndex = remainingLevels.pop()
    forestIndex = remainingLevels.pop()
    castleIndex = remainingLevels.pop()
    newLevelOrder = {
        japesIndex: Levels.JungleJapes,
        aztecIndex: Levels.AngryAztec,
        factoryIndex: Levels.FranticFactory,
        galleonIndex: Levels.GloomyGalleon,
        forestIndex: Levels.FungiForest,
        cavesIndex: Levels.CrystalCaves,
        castleIndex: Levels.CreepyCastle,
        helmIndex: Levels.HideoutHelm,
    }
    settings.level_order = newLevelOrder
    return newLevelOrder


def GenerateLevelOrderForMultipleStartingKongs(settings: Settings):
    """Generate a level order given starting with 2 to 4 kongs and the need to find more kongs along the way."""
    levelIndicesToFill = {1, 2, 3, 4, 5, 6, 7}
    last_level_index = 7
    # Initialize level order
    newLevelOrder = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None}
    # Sort levels by most to least kongs
    kongsInLevels = {
        Levels.JungleJapes: 1 if Locations.DiddyKong in settings.kong_locations else 0,
        Levels.AngryAztec: len([x for x in [Locations.LankyKong, Locations.TinyKong] if x in settings.kong_locations]),
        Levels.FranticFactory: 1 if Locations.ChunkyKong in settings.kong_locations else 0,
        Levels.GloomyGalleon: 0,
        Levels.FungiForest: 0,
        Levels.CrystalCaves: 0,
        Levels.CreepyCastle: 0,
    }
    if not settings.shuffle_helm_location:
        # Pre-place Helm
        newLevelOrder[8] = Levels.HideoutHelm
    else:
        kongsInLevels[Levels.HideoutHelm] = 0.5  # Make sure Helm is always the first one to be shuffled if you have something of zero index
        levelIndicesToFill.add(8)
        last_level_index = 8
    levelsSortedByKongs = [kongsInLevel[0] for kongsInLevel in sorted(kongsInLevels.items(), key=lambda x: x[1], reverse=True)]
    if settings.shuffle_helm_location:
        kongsInLevels[Levels.HideoutHelm] = 0  # Reset helm back to 0 (I hate this whole system more than you do)
    # Iterate over levels to place them in the level order
    kongsUnplaced = sum(kongsInLevels.values())

    for levelToPlace in levelsSortedByKongs:
        # Determine the latest this level can appear
        kongsUnplaced = kongsUnplaced - kongsInLevels[levelToPlace]
        kongsOwned = settings.starting_kongs_count
        # Assume we can own the kongs for levels not yet placed
        kongsAssumed = settings.starting_kongs_count + kongsUnplaced
        levelsReachable = []
        # Traverse through levels in order
        for level in range(1, (last_level_index + 1)):
            # If don't have 5 kongs yet, stop if don't have enough kongs to reach this level
            if kongsAssumed < 5 and level > kongsAssumed + 1:
                break
            if kongsOwned == settings.starting_kongs_count:
                # If reached Aztec without freeing anyone yet, specific combinations of kongs are needed to open those cages (if they have any occupants)
                if newLevelOrder[level] == Levels.AngryAztec and (Locations.TinyKong in settings.kong_locations or Locations.LankyKong in settings.kong_locations):
                    # Assume we can free any locked kongs here
                    tinyAccessible = Locations.TinyKong in settings.kong_locations
                    lankyAccessible = Locations.LankyKong in settings.kong_locations
                    # If a kong is in Tiny Temple, either Diddy or Chunky can free them
                    if tinyAccessible:
                        if Kongs.diddy not in settings.starting_kong_list and Kongs.chunky not in settings.starting_kong_list:
                            tinyAccessible = False
                    # If a kong is in Llama temple, need to be able to get past the guitar door and one of Donkey, Lanky, or Tiny to open the Llama temple
                    if lankyAccessible:
                        guitarDoorAccess = (
                            Kongs.diddy in settings.starting_kong_list
                            or IsDDMSSelected(
                                settings.remove_barriers_selected,
                                RemovedBarriersSelected.aztec_tunnel_door,
                            )
                            or (Kongs.donkey in settings.starting_kong_list and settings.activate_all_bananaports == ActivateAllBananaports.all)
                        )
                        if not guitarDoorAccess or (
                            Kongs.donkey not in settings.starting_kong_list and Kongs.lanky not in settings.starting_kong_list and Kongs.tiny not in settings.starting_kong_list
                        ):
                            lankyAccessible = False
                    # If we can unlock one kong then we can unlock both, so if we can't reach either then we can't assume we can unlock any kong from here
                    if not tinyAccessible and not lankyAccessible:
                        break
            levelsReachable.append(level)
            # Check if a level has been assigned here
            if newLevelOrder[level] is not None:
                # Update kongsOwned & kongsAssumed with kongs freeable in current level
                kongsOwned = kongsOwned + kongsInLevels[newLevelOrder[level]]
                kongsAssumed = kongsAssumed + kongsInLevels[newLevelOrder[level]]
        # Choose where levelWithKongs will go in new level order
        levelIndexOptions = list(levelIndicesToFill.intersection(levelsReachable))
        if levelToPlace == Levels.HideoutHelm:
            # Don't place Helm earlier than level 3
            levelIndexOptions = [x for x in levelIndexOptions if x > 2]
        # If we hit one of the `break`s above, it's likely we can't logically access any level past it
        # If this happens, we got unlucky (settings dependending) and restart this process or else we crash
        # The most common instance of this is when Aztec is level 1 and you don't start with Diddy
        if levelIndexOptions == []:
            return GenerateLevelOrderForMultipleStartingKongs(settings)
        # Place level in newLevelOrder and remove from list of remaining slots
        shuffledLevelIndex = settings.random.choice(levelIndexOptions)
        levelIndicesToFill.remove(shuffledLevelIndex)
        newLevelOrder[shuffledLevelIndex] = levelToPlace
    return newLevelOrder
