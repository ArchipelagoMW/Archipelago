"""Contains functions related to setting up the pool of shuffled items."""

import itertools

from randomizer.Enums.Events import Events
import randomizer.Enums.Kongs as KongObject
from randomizer.Enums.Items import Items
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Plandomizer import GetItemsFromPlandoItem, PlandoItems
from randomizer.Enums.Settings import (
    ClimbingStatus,
    MoveRando,
    ShockwaveStatus,
    ShuffleLoadingZones,
    TrainingBarrels,
)
from randomizer.Enums.Types import Types
from randomizer.Enums.Levels import Levels
from randomizer.Lists.Item import ItemFromKong
from randomizer.Lists.LevelInfo import LevelInfoList
from randomizer.Lists.ShufflableExit import ShufflableExits
from randomizer.Patching.Library.Generic import IsItemSelected
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


race_gb_locations = [
    Locations.JapesDiddyMinecarts,
    Locations.AztecDiddyVultureRace,
    Locations.AztecTinyBeetleRace,
    Locations.FactoryTinyCarRace,
    Locations.GalleonDonkeySealRace,
    Locations.ForestDiddyOwlRace,
    Locations.ForestLankyRabbitRace,
    Locations.ForestChunkyMinecarts,
    Locations.CavesLankyBeetleRace,
    Locations.CastleDonkeyMinecarts,
    Locations.CastleTinyCarRace,
]
gauntlet_gb_locations = [
    Locations.JapesLankyFairyCave,
    Locations.AztecTinyKlaptrapRoom,
    Locations.AztecChunkyKlaptrapRoom,
    Locations.FactoryDiddyRandD,
    Locations.ForestLankyAttic,
    Locations.ForestTinyAnthill,
    Locations.ForestTinySpiderBoss,
    Locations.ForestChunkyApple,
    Locations.CavesDonkey5DoorCabin,
    Locations.CavesDiddy5DoorCabinLower,
    Locations.CavesLanky5DoorIgloo,
    Locations.CavesTiny5DoorCabin,
    Locations.CavesChunky5DoorIgloo,
    Locations.CastleDonkeyLibrary,
    Locations.CastleTinyTrashCan,
    Locations.CastleChunkyShed,
]
blueprint_gb_locations = [Locations.TurnInDKIslesDonkeyBlueprint + x for x in range(40)]


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
    banana_types = {
        Types.RaceBanana: race_gb_locations.copy(),
        Types.GauntletBanana: gauntlet_gb_locations.copy(),
        Types.BlueprintBanana: blueprint_gb_locations.copy(),
    }
    unshuffled_bananas = []
    for btype, lst in banana_types.items():
        if btype not in settings.shuffled_location_types:
            unshuffled_bananas.extend(lst)
    for location in spoiler.LocationList:
        if spoiler.LocationList[location].type in typesOfItemsNotShuffled or location in unshuffled_bananas:
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
    if Types.BlueprintBanana in spoiler.settings.shuffled_location_types:
        for location_id in spoiler.settings.excluded_bp_locations:
            spoiler.LocationList[location_id].PlaceDefaultItem(spoiler)
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
            spoiler.LocationList[Locations.IslesDonkeyHalfMedal + x].PlaceConstantItem(spoiler, Items.NoItem)
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
    # if settings.starting_kongs_count == 5:
    #     spoiler.LocationList[Locations.DiddyKong].PlaceConstantItem(spoiler, Items.NoItem)
    #     spoiler.LocationList[Locations.LankyKong].PlaceConstantItem(spoiler, Items.NoItem)
    #     spoiler.LocationList[Locations.TinyKong].PlaceConstantItem(spoiler, Items.NoItem)
    #     spoiler.LocationList[Locations.ChunkyKong].PlaceConstantItem(spoiler, Items.NoItem)
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
    allItems.extend(GoldenBananaItems(settings))
    allItems.extend(NintendoCoinItems())
    allItems.extend(RarewareCoinItems())
    allItems.extend(BattleCrownItems(settings))
    allItems.extend(Keys())
    allItems.extend(BananaMedalItems(settings))
    allItems.extend(BeanItems())
    allItems.extend(PearlItems(settings))
    allItems.extend(FairyItems(settings))
    allItems.extend(RainbowCoinItems(settings))
    allItems.extend(MelonCrateItems())
    allItems.extend(HalfMedalItems())
    allItems.extend(BoulderItems())
    allItems.extend(EnemyItems())
    allItems.extend(FakeItems(settings))
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
        allItems.extend(GoldenBananaItems(settings))
    if Types.NintendoCoin in settings.shuffled_location_types:
        allItems.extend(NintendoCoinItems())
    if Types.RarewareCoin in settings.shuffled_location_types:
        allItems.extend(RarewareCoinItems())
    if Types.Crown in settings.shuffled_location_types:
        allItems.extend(BattleCrownItems(settings))
    if Types.Key in settings.shuffled_location_types:
        allItems.extend(Keys())
    if Types.Medal in settings.shuffled_location_types:
        allItems.extend(BananaMedalItems(settings))
    if Types.Bean in settings.shuffled_location_types:
        allItems.extend(BeanItems())
    if Types.Pearl in settings.shuffled_location_types:
        allItems.extend(PearlItems(settings))
    if Types.Fairy in settings.shuffled_location_types:
        allItems.extend(FairyItems(settings))
    if Types.RainbowCoin in settings.shuffled_location_types:
        allItems.extend(RainbowCoinItems(settings))
    if Types.CrateItem in settings.shuffled_location_types:
        allItems.extend(MelonCrateItems())
    if Types.HalfMedal in settings.shuffled_location_types:
        allItems.extend(HalfMedalItems())
    if Types.BoulderItem in settings.shuffled_location_types:
        allItems.extend(BoulderItems())
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
    filler_types = [
        x for x in [Types.FillerBanana, Types.FillerCrown, Types.FillerFairy, Types.FillerPearl, Types.FillerMedal, Types.FillerRainbowCoin, Types.JunkItem] if x in settings.shuffled_location_types
    ]
    if len(filler_types) > 0:
        allItems.extend(FillerItems(settings))
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
        allItems.extend(GoldenBananaItems(settings))
    if Types.NintendoCoin in settings.shuffled_location_types:
        allItems.extend(NintendoCoinItems())
    if Types.RarewareCoin in settings.shuffled_location_types:
        allItems.extend(RarewareCoinItems())
    if Types.Crown in settings.shuffled_location_types:
        allItems.extend(BattleCrownItems(settings))
    if Types.Key in settings.shuffled_location_types:
        allItems.extend(Keys())
    if Types.Medal in settings.shuffled_location_types:
        allItems.extend(BananaMedalItems(settings))
    if Types.Bean in settings.shuffled_location_types:
        allItems.extend(BeanItems())
    if Types.Pearl in settings.shuffled_location_types:
        allItems.extend(PearlItems(settings))
    if Types.Fairy in settings.shuffled_location_types:
        allItems.extend(FairyItems(settings))
    if Types.RainbowCoin in settings.shuffled_location_types:
        allItems.extend(RainbowCoinItems(settings))
    if Types.CrateItem in settings.shuffled_location_types:
        allItems.extend(MelonCrateItems())
    if Types.HalfMedal in settings.shuffled_location_types:
        allItems.extend(HalfMedalItems())
    if Types.BoulderItem in settings.shuffled_location_types:
        allItems.extend(BoulderItems())
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
    filler_types = [
        x for x in [Types.FillerBanana, Types.FillerCrown, Types.FillerFairy, Types.FillerPearl, Types.FillerMedal, Types.FillerRainbowCoin, Types.JunkItem] if x in settings.shuffled_location_types
    ]
    if len(filler_types) > 0:
        allItems.extend(FillerItems(settings))
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
    blueprints = []
    for bp in (Items.DonkeyBlueprint, Items.DiddyBlueprint, Items.LankyBlueprint, Items.TinyBlueprint, Items.ChunkyBlueprint):
        blueprints.extend(itertools.repeat(bp, 8))
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


def GoldenBananaItems(settings):
    """Return a list of GBs to be placed."""
    itemPool = []
    decrease = 0
    decrease_values = {
        Types.RaceBanana: 11,
        Types.GauntletBanana: 16,
        Types.BlueprintBanana: 40,
    }
    for item_type, value in decrease_values.items():
        if item_type not in settings.shuffled_location_types:
            decrease += value
    if Types.BlueprintBanana in settings.shuffled_location_types:
        decrease += len(settings.excluded_bp_locations)
    itemPool.extend(itertools.repeat(Items.GoldenBanana, settings.total_gbs - decrease))
    return itemPool


def BananaMedalItems(settings):
    """Return a list of Banana Medals to be placed."""
    itemPool = []
    count = 40
    if IsItemSelected(settings.cb_rando_enabled, settings.cb_rando_list_selected, Levels.DKIsles):
        count = 45
    itemPool.extend(itertools.repeat(Items.BananaMedal, settings.total_medals))
    return itemPool


def BattleCrownItems(settings):
    """Return a list of Crowns to be placed."""
    itemPool = []
    itemPool.extend(itertools.repeat(Items.BattleCrown, settings.total_crowns))
    return itemPool


def BeanItems():
    """Return a list of the bean."""
    return [Items.Bean]


def PearlItems(settings):
    """Return a list of pearls."""
    return list(itertools.repeat(Items.Pearl, settings.total_pearls))


def RainbowCoinItems(settings):
    """Return a list of Rainbow Coins to be placed."""
    itemPool = []
    itemPool.extend(itertools.repeat(Items.RainbowCoin, settings.total_rainbow_coins))
    return itemPool


def MelonCrateItems():
    """Return a list of No Items to be placed."""
    return []


def HalfMedalItems():
    """Return a list of No Items to be placed."""
    return []


def BoulderItems():
    """Return a list of boulder items to be placed."""
    return []


def EnemyItems():
    """Return a list of No Items to be placed."""
    return []


def FairyItems(settings):
    """Return a list of Fairies to be placed."""
    itemPool = []
    itemPool.extend(itertools.repeat(Items.BananaFairy, settings.total_fairies))
    return itemPool


def DistributeItems(items: list, count: int, distro: list[int] = None) -> list:
    """Distribute the items so that there is a roughly even amount of them placed in the seed."""
    if count == 0:
        return []
    item_post_rebalance = items.copy()
    if distro is not None:
        item_post_rebalance = []
        for index, item in enumerate(items):
            for _ in range(distro[index]):
                item_post_rebalance.append(item)
    repeat_count = int(count / len(item_post_rebalance)) + 1
    selection = []
    for _ in range(repeat_count):
        selection.extend(item_post_rebalance)
    return selection[:count]


def FakeItems(settings):
    """Return a copy of the list of Fake Items to be placed."""
    # This order of items helps ensure that with low ice trap counts, you see models other than GBs
    return [item for item in settings.trap_assortment]


def FillerItems(settings):
    """Return a list of misc filler items to be placed."""
    filler_mapping = {
        Types.FillerBanana: Items.FillerBanana,  # Don't think we need to worry about the 8 bit limit, but just to be safe
        Types.FillerCrown: Items.FillerCrown,
        Types.FillerFairy: Items.FillerFairy,
        Types.FillerPearl: Items.FillerPearl,
        Types.FillerMedal: Items.FillerMedal,
        Types.FillerRainbowCoin: Items.FillerRainbowCoin,
        Types.JunkItem: Items.JunkMelon,
    }
    filler_mapping_allowances = {
        Items.FillerBanana: {
            # Don't think we need to worry about the 8 bit limit, but just to be safe
            "count": 255 - settings.total_gbs,
            "weight": 10,
        },
        Items.FillerCrown: {
            "count": 255 - settings.total_crowns,
            "weight": 2,
        },
        Items.FillerFairy: {
            "count": 255 - settings.total_fairies,
            "weight": 4,
        },
        Items.FillerPearl: {
            "count": 255 - settings.total_pearls,
            "weight": 1,
        },
        Items.FillerMedal: {
            "count": 255 - settings.total_medals,
            "weight": 6,
        },
        Items.FillerRainbowCoin: {
            "count": 255 - settings.total_rainbow_coins,
            "weight": 3,
        },
        Items.JunkMelon: {"count": 1000, "weight": 2},
    }
    max_weight = max([x["weight"] for x in list(filler_mapping_allowances.values())])
    filler_types_in_pool = [x for x in list(filler_mapping.keys()) if x in settings.shuffled_location_types]
    item_types_for_filler = []
    for item_type in filler_types_in_pool:
        item_types_for_filler.append(filler_mapping[item_type])
    distro = []
    placed_count = {}
    total_placed_count = 0
    offset = settings.junk_offset
    compiled_weights = []  # Compiled weight distro to avoid clumping
    for x in range(max_weight):
        for item_type in item_types_for_filler:
            assoc_weight = filler_mapping_allowances[item_type]["weight"]
            count_per_item = max_weight / assoc_weight
            prev_index = int(x / count_per_item)
            curr_index = int((x + 1) / count_per_item)
            if prev_index != curr_index:
                compiled_weights.append(item_type)
    if len(compiled_weights) == 0:
        return []
    for x in range(1000):
        for item_type in compiled_weights:
            existing_count = placed_count.get(item_type, 0)
            if existing_count < filler_mapping_allowances[item_type]["count"]:
                if offset > 0:
                    offset -= 1
                    continue
                distro.append(item_type)
                placed_count[item_type] = existing_count + 1
                total_placed_count += 1
        if total_placed_count > 1000:
            break
    return distro


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


def GetItemsNeedingToBeAssumed(settings, placed_types, placed_items=[]):
    """Return a list of all items that will be assumed for immediate item placement."""
    itemPool = []
    unplacedTypes = [typ for typ in settings.shuffled_location_types if typ not in placed_types]
    if Types.Banana in unplacedTypes:
        itemPool.extend(GoldenBananaItems(settings))
    if Types.Shop in unplacedTypes:
        itemPool.extend(AllKongMoves())
    if Types.Blueprint in unplacedTypes:
        itemPool.extend(Blueprints())
    if Types.Fairy in unplacedTypes:
        itemPool.extend(FairyItems(settings))
    if Types.Key in unplacedTypes:
        itemPool.extend(Keys())
    if Types.Crown in unplacedTypes:
        itemPool.extend(BattleCrownItems(settings))
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
        itemPool.extend(BeanItems())
    if Types.Pearl in unplacedTypes:
        itemPool.extend(PearlItems(settings))
    if Types.RainbowCoin in unplacedTypes:
        itemPool.extend(RainbowCoinItems(settings))
    if Types.CrateItem in unplacedTypes:
        itemPool.extend(MelonCrateItems())
    if Types.HalfMedal in unplacedTypes:
        itemPool.extend(HalfMedalItems())
    if Types.BoulderItem in unplacedTypes:
        itemPool.extend(BoulderItems())
    if Types.Enemies in unplacedTypes:
        itemPool.extend(EnemyItems())
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
