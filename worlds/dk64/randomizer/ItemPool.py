"""Contains functions related to setting up the pool of shuffled items."""

import itertools

from randomizer.Enums.Events import Events
import randomizer.Enums.Kongs as KongObject
from randomizer.Enums.Items import Items
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Plandomizer import GetItemsFromPlandoItem, PlandoItems
from randomizer.Enums.Settings import (
    ClimbingStatus,
    HardModeSelected,
    MoveRando,
    ShockwaveStatus,
    ShuffleLoadingZones,
    TrainingBarrels,
    CBRando,
)
from randomizer.Enums.Types import Types
from randomizer.Enums.Levels import Levels
from randomizer.Lists.Item import ItemFromKong
from randomizer.Lists.LevelInfo import LevelInfoList
from randomizer.Lists.ShufflableExit import ShufflableExits
from randomizer.Patching.Library.Generic import getIceTrapCount, IsItemSelected
from randomizer.ShuffleBosses import PlandoBosses


def getHelmKey(settings) -> Items:
    """Get the item that will be placed in the final room in Helm."""
    key_item = Items.HideoutHelmKey
    if settings.shuffle_loading_zones == ShuffleLoadingZones.levels:
        level_index = None
        key_items = [
            Items.JungleJapesKey,
            Items.AngryAztecKey,
            Items.FranticFactoryKey,
            Items.GloomyGalleonKey,
            Items.FungiForestKey,
            Items.CrystalCavesKey,
            Items.CreepyCastleKey,
            Items.HideoutHelmKey,
        ]
        for x in range(8):
            if settings.level_order[x + 1] == Levels.HideoutHelm:
                key_item = key_items[x]
                level_index = x
                break
        if level_index is None:
            raise Exception("Unable to find Helm in the level order to remove Helm Key constant")
    return key_item


def PlaceConstants(spoiler):
    """Place items which are to be put in a hard-coded location."""
    # Settings-dependent locations
    settings = spoiler.settings
    # Determine what types of locations are being shuffled
    typesOfItemsShuffled = [Types.PreGivenMove]  # Your starting moves are always eligible to be shuffled if needed
    if settings.kong_rando:
        typesOfItemsShuffled.append(Types.Kong)
    if settings.move_rando != MoveRando.off:
        typesOfItemsShuffled.append(Types.Shop)
        if settings.training_barrels == TrainingBarrels.shuffled:
            typesOfItemsShuffled.append(Types.TrainingBarrel)
        if settings.climbing_status == ClimbingStatus.shuffled:
            typesOfItemsShuffled.append(Types.Climbing)
    if settings.shuffle_loading_zones == ShuffleLoadingZones.levels:
        typesOfItemsShuffled.append(Types.Key)
    typesOfItemsShuffled.extend(settings.shuffled_location_types)
    # Invert this list because I think it'll be faster
    typesOfItemsNotShuffled = [typ for typ in Types if typ not in typesOfItemsShuffled]
    # Place the default item at every location of a type we're not shuffling
    for location in spoiler.LocationList:
        if spoiler.LocationList[location].type in typesOfItemsNotShuffled:
            spoiler.LocationList[location].PlaceDefaultItem(spoiler)
            # If we're placing a vanilla training move, we have to make the location available
            if spoiler.LocationList[location].type in (Types.TrainingBarrel, Types.Climbing, Types.PreGivenMove):
                spoiler.LocationList[location].inaccessible = False
        else:
            spoiler.LocationList[location].constant = False
            spoiler.LocationList[location].item = None
        # While we're looping here, also reset shops that became inaccessible due to fill lockouts
        if spoiler.LocationList[location].type == Types.Shop:
            spoiler.LocationList[location].inaccessible = spoiler.LocationList[location].smallerShopsInaccessible
            spoiler.LocationList[location].tooExpensiveInaccessible = False
    # Make extra sure the Helm Key is right
    if settings.key_8_helm:
        helm_key = getHelmKey(spoiler.settings)
        if helm_key in KeysToPlace(spoiler.settings, excludeHelmKey=False):
            spoiler.LocationList[Locations.HelmKey].PlaceConstantItem(spoiler, helm_key)
        else:
            spoiler.LocationList[Locations.HelmKey].PlaceConstantItem(spoiler, Items.NoItem)
    # If no CB rando in isles, clear these locations
    if not IsItemSelected(spoiler.settings.cb_rando_enabled, spoiler.settings.cb_rando_list_selected, Levels.DKIsles):
        for x in range(5):
            spoiler.LocationList[Locations.IslesDonkeyMedal + x].PlaceConstantItem(spoiler, Items.NoItem)
    # Handle key placements
    if settings.shuffle_loading_zones == ShuffleLoadingZones.levels and Types.Key not in settings.shuffled_location_types:
        # Place keys in the lobbies they normally belong in
        # Ex. Whatever level is in the Japes lobby entrance will always have the Japes key
        for level in LevelInfoList.values():
            # If level exit isn't shuffled, use vanilla key
            if not ShufflableExits[level.TransitionTo].shuffled:
                spoiler.LocationList[level.KeyLocation].PlaceConstantItem(spoiler, level.KeyItem)
            else:
                # Find the transition this exit is attached to, and use that to get the proper location to place this key
                dest = ShufflableExits[level.TransitionTo].shuffledId
                shuffledTo = [x for x in LevelInfoList.values() if x.TransitionTo == dest][0]
                spoiler.LocationList[shuffledTo.KeyLocation].PlaceConstantItem(spoiler, level.KeyItem)
        # The End of Helm is always a Key in these settings (unless you start with it)
        helm_key = getHelmKey(spoiler.settings)
        if helm_key in KeysToPlace(spoiler.settings, excludeHelmKey=False):
            spoiler.LocationList[Locations.HelmKey].PlaceConstantItem(spoiler, getHelmKey(spoiler.settings))
        else:
            spoiler.LocationList[Locations.HelmKey].PlaceConstantItem(spoiler, Items.NoItem)

    # Empty out some locations based on the settings
    if settings.starting_kongs_count == 5:
        spoiler.LocationList[Locations.DiddyKong].PlaceConstantItem(spoiler, Items.NoItem)
        spoiler.LocationList[Locations.LankyKong].PlaceConstantItem(spoiler, Items.NoItem)
        spoiler.LocationList[Locations.TinyKong].PlaceConstantItem(spoiler, Items.NoItem)
        spoiler.LocationList[Locations.ChunkyKong].PlaceConstantItem(spoiler, Items.NoItem)
    if settings.start_with_slam:
        spoiler.LocationList[Locations.IslesFirstMove].PlaceConstantItem(spoiler, Items.ProgressiveSlam)
        spoiler.LocationList[Locations.IslesFirstMove].inaccessible = False

    # Plando items are placed with constants but should not change locations to Constant type
    settings.plandomizer_items_placed = []
    if settings.enable_plandomizer:
        blueprints_planned = []
        for location_id, plando_item in settings.plandomizer_dict["locations"].items():
            if plando_item in [
                PlandoItems.DonkeyBlueprint,
                PlandoItems.DiddyBlueprint,
                PlandoItems.LankyBlueprint,
                PlandoItems.TinyBlueprint,
                PlandoItems.ChunkyBlueprint,
            ]:
                item = settings.random.choice([x for x in GetItemsFromPlandoItem(plando_item) if x not in blueprints_planned])
                blueprints_planned.append(item)
            else:
                item = settings.random.choice(GetItemsFromPlandoItem(plando_item))
            spoiler.LocationList[int(location_id)].PlaceItem(spoiler, item)
            settings.plandomizer_items_placed.append(item)
        # If any bosses are plando'd, do it now ahead of placing any items randomly.
        if spoiler.settings.boss_plando:
            # Doing it here has the added benefit of rerolling on fill failure.
            PlandoBosses(spoiler)


def AllItemsUnrestricted(settings):
    """Return all placeable items regardless of shuffle status."""
    allItems = []
    allItems.extend(Blueprints())
    allItems.extend(GoldenBananaItems())
    allItems.extend(ToughGoldenBananaItems())
    allItems.extend(NintendoCoinItems())
    allItems.extend(RarewareCoinItems())
    allItems.extend(BattleCrownItems())
    allItems.extend(Keys())
    allItems.extend(BananaMedalItems(settings))
    allItems.extend(MiscItemRandoItems())
    allItems.extend(FairyItems())
    allItems.extend(RainbowCoinItems())
    allItems.extend(MelonCrateItems())
    allItems.extend(EnemyItems())
    allItems.extend(FakeItems(settings))
    allItems.extend(JunkItems(settings))
    allItems.extend(DonkeyMoves)
    allItems.extend(DiddyMoves)
    allItems.extend(LankyMoves)
    allItems.extend(TinyMoves)
    allItems.extend(ChunkyMoves)
    allItems.extend(ImportantSharedMoves)
    allItems.extend(JunkSharedMoves)
    allItems.extend(TrainingBarrelAbilities().copy())
    allItems.extend(ClimbingAbilities().copy())
    if settings.shockwave_status == ShockwaveStatus.shuffled_decoupled:
        allItems.append(Items.Camera)
        allItems.append(Items.Shockwave)
    else:
        allItems.append(Items.CameraAndShockwave)
    allItems.extend(Kongs(settings))
    allItems.extend(CrankyItems())
    allItems.extend(FunkyItems())
    allItems.extend(CandyItems())
    allItems.extend(SnideItems())
    return allItems


def AllItems(settings):
    """Return all shuffled items."""
    allItems = []
    if Types.Blueprint in settings.shuffled_location_types:
        allItems.extend(Blueprints())
    if Types.Banana in settings.shuffled_location_types:
        allItems.extend(GoldenBananaItems())
    if Types.ToughBanana in settings.shuffled_location_types:
        allItems.extend(ToughGoldenBananaItems())
    if Types.NintendoCoin in settings.shuffled_location_types:
        allItems.extend(NintendoCoinItems())
    if Types.RarewareCoin in settings.shuffled_location_types:
        allItems.extend(RarewareCoinItems())
    if Types.Crown in settings.shuffled_location_types:
        allItems.extend(BattleCrownItems())
    if Types.Key in settings.shuffled_location_types:
        allItems.extend(Keys())
    if Types.Medal in settings.shuffled_location_types:
        allItems.extend(BananaMedalItems(settings))
    if Types.Bean in settings.shuffled_location_types:  # Could check for pearls as well
        allItems.extend(MiscItemRandoItems())
    if Types.Fairy in settings.shuffled_location_types:
        allItems.extend(FairyItems())
    if Types.RainbowCoin in settings.shuffled_location_types:
        allItems.extend(RainbowCoinItems())
    if Types.CrateItem in settings.shuffled_location_types:
        allItems.extend(MelonCrateItems())
    if Types.Hint in settings.shuffled_location_types:
        allItems.extend(HintItems())
    if Types.Enemies in settings.shuffled_location_types:
        allItems.extend(EnemyItems())
    if Types.Cranky in settings.shuffled_location_types:
        allItems.extend(CrankyItems())
    if Types.Funky in settings.shuffled_location_types:
        allItems.extend(FunkyItems())
    if Types.Candy in settings.shuffled_location_types:
        allItems.extend(CandyItems())
    if Types.Snide in settings.shuffled_location_types:
        allItems.extend(SnideItems())
    if Types.FakeItem in settings.shuffled_location_types:
        allItems.extend(FakeItems(settings))
    if Types.JunkItem in settings.shuffled_location_types:
        allItems.extend(JunkItems(settings))
    if settings.move_rando != MoveRando.off:
        allItems.extend(DonkeyMoves)
        allItems.extend(DiddyMoves)
        allItems.extend(LankyMoves)
        allItems.extend(TinyMoves)
        allItems.extend(ChunkyMoves)
        allItems.extend(ImportantSharedMoves)

        if settings.training_barrels == TrainingBarrels.shuffled:
            allItems.extend(TrainingBarrelAbilities().copy())
        if settings.climbing_status == ClimbingStatus.shuffled:
            allItems.extend(ClimbingAbilities().copy())
        if settings.shockwave_status == ShockwaveStatus.shuffled_decoupled:
            allItems.append(Items.Camera)
            allItems.append(Items.Shockwave)
        else:
            allItems.append(Items.CameraAndShockwave)
    if settings.kong_rando or Types.Kong in settings.shuffled_location_types:
        allItems.extend(Kongs(settings))
    return allItems


def AllItemsForMovePlacement(settings):
    """Return all shuffled items we need to assume for move placement."""
    allItems = []
    if Types.Blueprint in settings.shuffled_location_types:
        allItems.extend(Blueprints())
    if Types.Banana in settings.shuffled_location_types:
        allItems.extend(GoldenBananaItems())
    if Types.ToughBanana in settings.shuffled_location_types:
        allItems.extend(ToughGoldenBananaItems())
    if Types.NintendoCoin in settings.shuffled_location_types:
        allItems.extend(NintendoCoinItems())
    if Types.RarewareCoin in settings.shuffled_location_types:
        allItems.extend(RarewareCoinItems())
    if Types.Crown in settings.shuffled_location_types:
        allItems.extend(BattleCrownItems())
    if Types.Key in settings.shuffled_location_types:
        allItems.extend(Keys())
    if Types.Medal in settings.shuffled_location_types:
        allItems.extend(BananaMedalItems(settings))
    if Types.Bean in settings.shuffled_location_types:  # Could check for pearls as well
        allItems.extend(MiscItemRandoItems())
    if Types.Fairy in settings.shuffled_location_types:
        allItems.extend(FairyItems())
    if Types.RainbowCoin in settings.shuffled_location_types:
        allItems.extend(RainbowCoinItems())
    if Types.CrateItem in settings.shuffled_location_types:
        allItems.extend(MelonCrateItems())
    if Types.Hint in settings.shuffled_location_types:
        allItems.extend(HintItems())
    if Types.Enemies in settings.shuffled_location_types:
        allItems.extend(EnemyItems())
    if Types.Cranky in settings.shuffled_location_types:
        allItems.extend(CrankyItems())
    if Types.Funky in settings.shuffled_location_types:
        allItems.extend(FunkyItems())
    if Types.Candy in settings.shuffled_location_types:
        allItems.extend(CandyItems())
    if Types.Snide in settings.shuffled_location_types:
        allItems.extend(SnideItems())
    if Types.FakeItem in settings.shuffled_location_types:
        allItems.extend(FakeItems(settings))
    if Types.JunkItem in settings.shuffled_location_types:
        allItems.extend(JunkItems(settings))
    return allItems


def AllKongMoves():
    """Return all moves."""
    allMoves = []
    allMoves.extend(DonkeyMoves)
    allMoves.extend(DiddyMoves)
    allMoves.extend(LankyMoves)
    allMoves.extend(TinyMoves)
    allMoves.extend(ChunkyMoves)
    allMoves.extend(ImportantSharedMoves)
    return allMoves


def AllMovesForOwnedKongs(kongs):
    """Return all moves for the given list of Kongs."""
    kongMoves = []
    if KongObject.Kongs.donkey in kongs:
        kongMoves.extend(DonkeyMoves)
    if KongObject.Kongs.diddy in kongs:
        kongMoves.extend(DiddyMoves)
    if KongObject.Kongs.lanky in kongs:
        kongMoves.extend(LankyMoves)
    if KongObject.Kongs.tiny in kongs:
        kongMoves.extend(TinyMoves)
    if KongObject.Kongs.chunky in kongs:
        kongMoves.extend(ChunkyMoves)
    kongMoves.extend(ImportantSharedMoves)
    return kongMoves


def ShockwaveTypeItems(settings):
    """Return the Shockwave-type items for the given settings."""
    if settings.shockwave_status == ShockwaveStatus.shuffled_decoupled:
        return [Items.Camera, Items.Shockwave]
    else:
        return [Items.CameraAndShockwave]


def Blueprints():
    """Return all blueprint items."""
    blueprints = [
        Items.DKIslesDonkeyBlueprint,
        Items.DKIslesDiddyBlueprint,
        Items.DKIslesLankyBlueprint,
        Items.DKIslesTinyBlueprint,
        Items.DKIslesChunkyBlueprint,
        Items.JungleJapesDonkeyBlueprint,
        Items.JungleJapesDiddyBlueprint,
        Items.JungleJapesLankyBlueprint,
        Items.JungleJapesTinyBlueprint,
        Items.JungleJapesChunkyBlueprint,
        Items.AngryAztecDonkeyBlueprint,
        Items.AngryAztecDiddyBlueprint,
        Items.AngryAztecLankyBlueprint,
        Items.AngryAztecTinyBlueprint,
        Items.AngryAztecChunkyBlueprint,
        Items.FranticFactoryDonkeyBlueprint,
        Items.FranticFactoryDiddyBlueprint,
        Items.FranticFactoryLankyBlueprint,
        Items.FranticFactoryTinyBlueprint,
        Items.FranticFactoryChunkyBlueprint,
        Items.GloomyGalleonDonkeyBlueprint,
        Items.GloomyGalleonDiddyBlueprint,
        Items.GloomyGalleonLankyBlueprint,
        Items.GloomyGalleonTinyBlueprint,
        Items.GloomyGalleonChunkyBlueprint,
        Items.FungiForestDonkeyBlueprint,
        Items.FungiForestDiddyBlueprint,
        Items.FungiForestLankyBlueprint,
        Items.FungiForestTinyBlueprint,
        Items.FungiForestChunkyBlueprint,
        Items.CrystalCavesDonkeyBlueprint,
        Items.CrystalCavesDiddyBlueprint,
        Items.CrystalCavesLankyBlueprint,
        Items.CrystalCavesTinyBlueprint,
        Items.CrystalCavesChunkyBlueprint,
        Items.CreepyCastleDonkeyBlueprint,
        Items.CreepyCastleDiddyBlueprint,
        Items.CreepyCastleLankyBlueprint,
        Items.CreepyCastleTinyBlueprint,
        Items.CreepyCastleChunkyBlueprint,
    ]
    return blueprints


def Keys():
    """Return all key items."""
    return [
        Items.JungleJapesKey,
        Items.AngryAztecKey,
        Items.FranticFactoryKey,
        Items.GloomyGalleonKey,
        Items.FungiForestKey,
        Items.CrystalCavesKey,
        Items.CreepyCastleKey,
        Items.HideoutHelmKey,
    ]


def KeysToPlace(settings, excludeHelmKey=True):
    """Return all keys that are non-starting keys."""
    keysToPlace = []
    for keyEvent in settings.krool_keys_required:
        if keyEvent == Events.JapesKeyTurnedIn:
            keysToPlace.append(Items.JungleJapesKey)
        elif keyEvent == Events.AztecKeyTurnedIn:
            keysToPlace.append(Items.AngryAztecKey)
        elif keyEvent == Events.FactoryKeyTurnedIn:
            keysToPlace.append(Items.FranticFactoryKey)
        elif keyEvent == Events.GalleonKeyTurnedIn:
            keysToPlace.append(Items.GloomyGalleonKey)
        elif keyEvent == Events.ForestKeyTurnedIn:
            keysToPlace.append(Items.FungiForestKey)
        elif keyEvent == Events.CavesKeyTurnedIn:
            keysToPlace.append(Items.CrystalCavesKey)
        elif keyEvent == Events.CastleKeyTurnedIn:
            keysToPlace.append(Items.CreepyCastleKey)
        elif keyEvent == Events.HelmKeyTurnedIn:
            keysToPlace.append(Items.HideoutHelmKey)
    if settings.key_8_helm and excludeHelmKey:
        key_item = getHelmKey(settings)
        if key_item in keysToPlace:
            keysToPlace.remove(key_item)
    return keysToPlace


def Kongs(settings):
    """Return Kong items depending on settings."""
    kongs = []
    if settings.starting_kongs_count != 5:
        kongs = [Items.Donkey, Items.Diddy, Items.Lanky, Items.Tiny, Items.Chunky]
        kongs.remove(ItemFromKong(settings.starting_kong))
    return kongs


def GetKongForItem(item):
    """Return Kong object from kong-type item."""
    if item == Items.Donkey:
        return KongObject.Kongs.donkey
    elif item == Items.Diddy:
        return KongObject.Kongs.diddy
    elif item == Items.Lanky:
        return KongObject.Kongs.lanky
    elif item == Items.Tiny:
        return KongObject.Kongs.tiny
    else:
        return KongObject.Kongs.chunky


def Guns(settings):
    """Return all gun items."""
    return [Items.Coconut, Items.Peanut, Items.Grape, Items.Feather, Items.Pineapple]


def Instruments(settings):
    """Return all instrument items."""
    return [Items.Bongos, Items.Guitar, Items.Trombone, Items.Saxophone, Items.Triangle]


def TrainingBarrelAbilities():
    """Return all training barrel abilities."""
    barrelAbilities = [Items.Vines, Items.Swim, Items.Oranges, Items.Barrels]
    return barrelAbilities


def ClimbingAbilities():
    """Return all climbing abilities."""
    return [Items.Climbing]


def Upgrades(settings):
    """Return all upgrade items."""
    upgrades = []
    # Add training barrel items to item pool if shuffled
    if settings.training_barrels == TrainingBarrels.shuffled:
        upgrades.extend(TrainingBarrelAbilities())
    # Add climbing to item pool if shuffled
    if settings.climbing_status == ClimbingStatus.shuffled:
        upgrades.extend(ClimbingAbilities())
    # Add either progressive upgrade items or individual ones depending on settings
    slam_count = 3
    if settings.start_with_slam:
        slam_count = 2
    upgrades.extend(itertools.repeat(Items.ProgressiveSlam, slam_count))
    upgrades.extend(
        [
            Items.BaboonBlast,
            Items.StrongKong,
            Items.GorillaGrab,
            Items.ChimpyCharge,
            Items.RocketbarrelBoost,
            Items.SimianSpring,
            Items.Orangstand,
            Items.BaboonBalloon,
            Items.OrangstandSprint,
            Items.MiniMonkey,
            Items.PonyTailTwirl,
            Items.Monkeyport,
            Items.HunkyChunky,
            Items.PrimatePunch,
            Items.GorillaGone,
        ]
    )
    upgrades.append(Items.HomingAmmo)
    upgrades.append(Items.SniperSight)
    upgrades.extend(itertools.repeat(Items.ProgressiveAmmoBelt, 2))
    upgrades.extend(itertools.repeat(Items.ProgressiveInstrumentUpgrade, 3))
    if settings.shockwave_status != ShockwaveStatus.start_with:
        if settings.shockwave_status == ShockwaveStatus.vanilla or settings.shockwave_status == ShockwaveStatus.shuffled:
            upgrades.append(Items.CameraAndShockwave)
        else:
            upgrades.append(Items.Camera)
            upgrades.append(Items.Shockwave)

    return upgrades


def HighPriorityItems(settings):
    """Get all items which are of high importance logically."""
    itemPool = []
    itemPool.extend(Kongs(settings))
    itemPool.extend(Guns(settings))
    itemPool.extend(Instruments(settings))
    itemPool.extend(Upgrades(settings))
    itemPool.extend(CrankyItems())
    itemPool.extend(CandyItems())
    itemPool.extend(FunkyItems())
    itemPool.extend(SnideItems())
    return itemPool


def NintendoCoinItems():
    """Return Nintendo Coin."""
    return [Items.NintendoCoin]


def RarewareCoinItems():
    """Return Rareware Coin."""
    return [Items.RarewareCoin]


TOUGH_BANANA_COUNT = 13


def GoldenBananaItems():
    """Return a list of GBs to be placed."""
    itemPool = []
    itemPool.extend(itertools.repeat(Items.GoldenBanana, 161 - TOUGH_BANANA_COUNT))  # 40 Blueprint GBs are always already placed (see Types.BlueprintBanana)
    return itemPool


def ToughGoldenBananaItems():
    """Return a list of GBs to be placed."""
    itemPool = []
    itemPool.extend(itertools.repeat(Items.GoldenBanana, TOUGH_BANANA_COUNT))
    return itemPool


def BananaMedalItems(settings):
    """Return a list of Banana Medals to be placed."""
    itemPool = []
    count = 40
    if IsItemSelected(settings.cb_rando_enabled, settings.cb_rando_list_selected, Levels.DKIsles):
        count = 45
    itemPool.extend(itertools.repeat(Items.BananaMedal, count))
    return itemPool


def BattleCrownItems():
    """Return a list of Crowns to be placed."""
    itemPool = []
    itemPool.extend(itertools.repeat(Items.BattleCrown, 10))
    return itemPool


def MiscItemRandoItems():
    """Return a list of Items that are classed as miscellaneous."""
    itemPool = []
    itemPool.append(Items.Bean)
    itemPool.extend(itertools.repeat(Items.Pearl, 5))
    return itemPool


def RainbowCoinItems():
    """Return a list of Rainbow Coins to be placed."""
    itemPool = []
    itemPool.extend(itertools.repeat(Items.RainbowCoin, 16))
    return itemPool


def MelonCrateItems():
    """Return a list of No Items to be placed."""
    return []


def EnemyItems():
    """Return a list of No Items to be placed."""
    return []


def FairyItems():
    """Return a list of Fairies to be placed."""
    itemPool = []
    itemPool.extend(itertools.repeat(Items.BananaFairy, 20))
    return itemPool


def FakeItems(settings):
    """Return a list of Fake Items to be placed."""
    itemPool = []
    total_count = getIceTrapCount(settings)
    slow_count = int(total_count / 3)
    reverse_count = int(total_count / 3)
    bubble_count = total_count - (slow_count + reverse_count)
    itemPool.extend(itertools.repeat(Items.IceTrapBubble, bubble_count))
    itemPool.extend(itertools.repeat(Items.IceTrapReverse, reverse_count))
    itemPool.extend(itertools.repeat(Items.IceTrapSlow, slow_count))
    return itemPool


def CrankyItems():
    """Return a list of Cranky shop owners to be placed."""
    return [Items.Cranky]


def FunkyItems():
    """Return a list of Funky shop owners to be placed."""
    return [Items.Funky]


def CandyItems():
    """Return a list of Candy shop owners to be placed."""
    return [Items.Candy]


def SnideItems():
    """Return a list of Snide shop owners to be placed."""
    return [Items.Snide]


def HintItems():
    """Return a list of Hint Items to be placed."""
    return [
        Items.JapesDonkeyHint,
        Items.JapesDiddyHint,
        Items.JapesLankyHint,
        Items.JapesTinyHint,
        Items.JapesChunkyHint,
        Items.AztecDonkeyHint,
        Items.AztecDiddyHint,
        Items.AztecLankyHint,
        Items.AztecTinyHint,
        Items.AztecChunkyHint,
        Items.FactoryDonkeyHint,
        Items.FactoryDiddyHint,
        Items.FactoryLankyHint,
        Items.FactoryTinyHint,
        Items.FactoryChunkyHint,
        Items.GalleonDonkeyHint,
        Items.GalleonDiddyHint,
        Items.GalleonLankyHint,
        Items.GalleonTinyHint,
        Items.GalleonChunkyHint,
        Items.ForestDonkeyHint,
        Items.ForestDiddyHint,
        Items.ForestLankyHint,
        Items.ForestTinyHint,
        Items.ForestChunkyHint,
        Items.CavesDonkeyHint,
        Items.CavesDiddyHint,
        Items.CavesLankyHint,
        Items.CavesTinyHint,
        Items.CavesChunkyHint,
        Items.CastleDonkeyHint,
        Items.CastleDiddyHint,
        Items.CastleLankyHint,
        Items.CastleTinyHint,
        Items.CastleChunkyHint,
    ]


def JunkItems(settings):
    """Return a list of Junk Items to be placed."""
    junk_count = min(100, 116 - getIceTrapCount(settings))
    if Types.Enemies in settings.shuffled_location_types:
        junk_count += 427
    itemPool = []
    # items_to_place = (Items.JunkAmmo, Items.JunkCrystal, Items.JunkFilm, Items.JunkMelon, Items.JunkOrange)
    # items_to_place = (Items.JunkAmmo, Items.JunkCrystal, Items.JunkMelon, Items.JunkOrange)
    items_to_place = [Items.JunkMelon]
    lim = int(junk_count / len(items_to_place))
    for item_type in items_to_place:
        itemPool.extend(itertools.repeat(item_type, lim))
    return itemPool


def GetItemsNeedingToBeAssumed(settings, placed_types, placed_items=[]):
    """Return a list of all items that will be assumed for immediate item placement."""
    itemPool = []
    unplacedTypes = [typ for typ in settings.shuffled_location_types if typ not in placed_types]
    if Types.Banana in unplacedTypes:
        itemPool.extend(GoldenBananaItems())
    if Types.ToughBanana in unplacedTypes:
        itemPool.extend(ToughGoldenBananaItems())
    if Types.Shop in unplacedTypes:
        itemPool.extend(AllKongMoves())
    if Types.Blueprint in unplacedTypes:
        itemPool.extend(Blueprints())
    if Types.Fairy in unplacedTypes:
        itemPool.extend(FairyItems())
    if Types.Key in unplacedTypes:
        itemPool.extend(Keys())
    if Types.Crown in unplacedTypes:
        itemPool.extend(BattleCrownItems())
    if Types.NintendoCoin in unplacedTypes:
        itemPool.extend(NintendoCoinItems())
    if Types.RarewareCoin in unplacedTypes:
        itemPool.extend(RarewareCoinItems())
    if Types.TrainingBarrel in unplacedTypes:
        itemPool.extend(TrainingBarrelAbilities())
    if Types.Climbing in unplacedTypes:
        itemPool.extend(ClimbingAbilities())
    if Types.Kong in unplacedTypes:
        itemPool.extend(Kongs(settings))
    if Types.Medal in unplacedTypes:
        itemPool.extend(BananaMedalItems(settings))
    if Types.Shockwave in unplacedTypes:
        itemPool.extend(ShockwaveTypeItems(settings))
    if Types.Bean in unplacedTypes:
        itemPool.extend(MiscItemRandoItems())  # Covers Bean and Pearls
    if Types.RainbowCoin in unplacedTypes:
        itemPool.extend(RainbowCoinItems())
    if Types.CrateItem in unplacedTypes:
        itemPool.extend(MelonCrateItems())
    if Types.Enemies in unplacedTypes:
        itemPool.extend(EnemyItems())
    if Types.ToughBanana in unplacedTypes:
        itemPool.extend(ToughGoldenBananaItems())
    if Types.Cranky in unplacedTypes:
        itemPool.extend(CrankyItems())
    if Types.Funky in unplacedTypes:
        itemPool.extend(FunkyItems())
    if Types.Candy in unplacedTypes:
        itemPool.extend(CandyItems())
    if Types.Snide in unplacedTypes:
        itemPool.extend(SnideItems())
    # Never logic-affecting items
    # if Types.FakeItem in unplacedTypes:
    #     itemPool.extend(FakeItems())
    # if Types.JunkItem in unplacedTypes:
    #     itemPool.extend(JunkItems())
    if Types.Hint in unplacedTypes:
        itemPool.extend(HintItems())
    # If shops are not part of the larger item pool and are not placed, we may still need to assume them
    # It is worth noting that TrainingBarrel and Shockwave type items are contingent on Shop type items being in the item rando pool
    if Types.Shop not in settings.shuffled_location_types and Types.Shop not in placed_types and settings.move_rando != MoveRando.off:
        itemPool.extend(AllKongMoves())
        if settings.training_barrels == TrainingBarrels.shuffled:
            itemPool.extend(TrainingBarrelAbilities().copy())
        if settings.climbing_status == ClimbingStatus.shuffled:
            itemPool.extend(ClimbingAbilities().copy())
    # With a list of specifically placed items, we can't assume those
    for item in placed_items:
        if item in itemPool:
            itemPool.remove(item)  # Remove one instance of the item (do not filter!)
    # If there is a Key forced into Helm, be sure it's not being assumed
    if settings.key_8_helm or Types.Key not in settings.shuffled_location_types:
        key_forced_into_helm = getHelmKey(settings)
        if key_forced_into_helm in itemPool:
            itemPool.remove(key_forced_into_helm)
    return itemPool


DonkeyMoves = [Items.Coconut, Items.Bongos, Items.BaboonBlast, Items.StrongKong, Items.GorillaGrab]
DiddyMoves = [Items.Peanut, Items.Guitar, Items.ChimpyCharge, Items.RocketbarrelBoost, Items.SimianSpring]
LankyMoves = [Items.Grape, Items.Trombone, Items.Orangstand, Items.BaboonBalloon, Items.OrangstandSprint]
TinyMoves = [Items.Feather, Items.Saxophone, Items.MiniMonkey, Items.PonyTailTwirl, Items.Monkeyport]
ChunkyMoves = [Items.Pineapple, Items.Triangle, Items.HunkyChunky, Items.PrimatePunch, Items.GorillaGone]
ImportantSharedMoves = [
    Items.ProgressiveSlam,
    Items.ProgressiveSlam,
    Items.ProgressiveSlam,
    Items.SniperSight,
    Items.HomingAmmo,
]
JunkSharedMoves = [
    Items.ProgressiveAmmoBelt,
    Items.ProgressiveAmmoBelt,
    Items.ProgressiveInstrumentUpgrade,
    Items.ProgressiveInstrumentUpgrade,
    Items.ProgressiveInstrumentUpgrade,
]
ProgressiveSharedMovesSet = {Items.ProgressiveAmmoBelt, Items.ProgressiveInstrumentUpgrade, Items.ProgressiveSlam}
