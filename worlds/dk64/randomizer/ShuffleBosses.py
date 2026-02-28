"""Randomize Boss Locations."""

from array import array
import math

from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Settings import SlamRequirement, HardBossesSelected, KroolInBossPool
from randomizer.Lists.Exceptions import BossOutOfLocationsException, PlandoIncompatibleException
from randomizer.Enums.Maps import Maps
from randomizer.Patching.Library.Generic import IsDDMSSelected

BossMapList = [
    Maps.JapesBoss,
    Maps.AztecBoss,
    Maps.FactoryBoss,
    Maps.GalleonBoss,
    Maps.FungiBoss,
    Maps.CavesBoss,
    Maps.CastleBoss,
]
KRoolMaps = [
    Maps.KroolDonkeyPhase,
    Maps.KroolDiddyPhase,
    Maps.KroolLankyPhase,
    Maps.KroolTinyPhase,
    Maps.KroolChunkyPhase,
]


def getBosses(settings) -> list:
    """Get list of bosses."""
    boss_maps = BossMapList.copy()
    if settings.krool_in_boss_pool_v2 != KroolInBossPool.off:
        boss_maps.extend(KRoolMaps.copy())
    if not settings.allow_boss_duping:
        return [x for x in boss_maps if x not in settings.krool_order and x in settings.bosses_selected]
    return [x for x in boss_maps if x in settings.bosses_selected]


def ShuffleBosses(boss_location_rando: bool, settings):
    """Shuffle boss locations."""
    boss_maps = getBosses(settings)
    if len(boss_maps) < 7:
        dupe_count = math.ceil(7 / len(boss_maps))
        original_maps = boss_maps.copy()
        for _ in range(dupe_count):
            boss_maps.extend(original_maps)
    if boss_location_rando:
        settings.random.shuffle(boss_maps)
    return boss_maps


def HardBossesEnabled(settings, check: HardBossesSelected) -> bool:
    """Return whether the hard bosses setting is on."""
    return IsDDMSSelected(settings.hard_bosses_selected, check)


def ShuffleBossKongs(settings, locked_levels=[]):
    """Shuffle the kongs required for the bosses."""
    vanillaBossKongs = {
        Maps.JapesBoss: Kongs.donkey,
        Maps.AztecBoss: Kongs.diddy,
        Maps.FactoryBoss: Kongs.tiny,
        Maps.GalleonBoss: Kongs.lanky,
        Maps.FungiBoss: Kongs.chunky,
        Maps.CavesBoss: Kongs.donkey,
        Maps.CastleBoss: Kongs.lanky,
        Maps.KroolDonkeyPhase: Kongs.donkey,
        Maps.KroolDiddyPhase: Kongs.diddy,
        Maps.KroolLankyPhase: Kongs.lanky,
        Maps.KroolTinyPhase: Kongs.tiny,
        Maps.KroolChunkyPhase: Kongs.chunky,
    }

    boss_kongs = []
    for level in range(7):
        if level in locked_levels:
            boss_kongs.append(settings.boss_kongs[level])
            continue
        boss_map = settings.boss_maps[level]
        if settings.boss_location_rando:
            kong = settings.random.choice(GetKongOptionsForBoss(boss_map, HardBossesEnabled(settings, HardBossesSelected.alternative_mad_jack_kongs)))
        else:
            kong = vanillaBossKongs[boss_map]
        boss_kongs.append(kong)

    return boss_kongs


def GetKongOptionsForBoss(boss_map: Maps, alt_mj_kongs: bool):
    """Randomly choses from the allowed list for the boss."""
    possibleKongs = []
    if boss_map == Maps.JapesBoss:
        possibleKongs = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
    elif boss_map == Maps.AztecBoss:
        possibleKongs = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
    elif boss_map == Maps.FactoryBoss:
        if alt_mj_kongs:
            possibleKongs = [Kongs.donkey, Kongs.tiny, Kongs.chunky]
        else:
            possibleKongs = [Kongs.tiny]
    elif boss_map == Maps.GalleonBoss:
        possibleKongs = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
    elif boss_map == Maps.FungiBoss:
        possibleKongs = [Kongs.chunky]
    elif boss_map == Maps.CavesBoss:
        possibleKongs = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
    elif boss_map == Maps.CastleBoss:
        possibleKongs = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
    elif boss_map in (
        Maps.KroolDonkeyPhase,
        Maps.KroolDiddyPhase,
        Maps.KroolLankyPhase,
        Maps.KroolTinyPhase,
        Maps.KroolChunkyPhase,
    ):
        # Not possible right now to make any other kong beat another's phase, however, if we were to do so:
        # DK Phase - Make all kongs enter cannon barrels
        # Other phases - ????????
        possibleKongs = [Kongs(Kongs.donkey + (boss_map - Maps.KroolDonkeyPhase))]
    return possibleKongs


def ShuffleKutoutKongs(random, boss_maps: array, boss_kongs: array, boss_rando: bool):
    """Shuffle the Kutout kong order."""
    vanillaKutoutKongs = [Kongs.lanky, Kongs.tiny, Kongs.chunky, Kongs.donkey, Kongs.diddy]
    kutout_kongs = []
    if boss_rando:
        if Maps.CastleBoss in boss_maps:
            kutoutLocation = boss_maps.index(Maps.CastleBoss)
            if kutoutLocation < 0 or kutoutLocation >= len(boss_kongs):
                starting_kong = random.choice(vanillaKutoutKongs)
            else:
                starting_kong = boss_kongs[kutoutLocation]
        else:
            starting_kong = random.choice(vanillaKutoutKongs)
        kongPool = vanillaKutoutKongs.copy()
        kongPool.remove(starting_kong)
        random.shuffle(kongPool)

        kutout_kongs.append(starting_kong)
        kutout_kongs.extend(kongPool)
    else:
        kutout_kongs = vanillaKutoutKongs
    return kutout_kongs


def ShuffleKKOPhaseOrder(settings):
    """Shuffle the phase order in King Kut Out."""
    kko_phases = [0, 1, 2, 3]
    settings.random.shuffle(kko_phases)
    return kko_phases.copy()


def ShuffleBossesBasedOnOwnedItems(spoiler, ownedKongs: dict, ownedMoves: dict):
    """Identify what levels can hold which bosses and place bosses accordingly, based on available Kongs and moves in each leve."""
    bossOptions = {
        Levels.JungleJapes: [],
        Levels.AngryAztec: [],
        Levels.FranticFactory: [],
        Levels.GloomyGalleon: [],
        Levels.FungiForest: [],
        Levels.CrystalCaves: [],
        Levels.CreepyCastle: [],
    }
    for level in bossOptions.keys():
        # Pufftoss is always accessible
        bossOptions[level].append(Maps.GalleonBoss)
        # King Kut Out is usually accessible but does care about lava water
        if not spoiler.LogicVariables.IsLavaWater() or ownedMoves[level].count(Items.ProgressiveInstrumentUpgrade) >= 3:
            bossOptions[level].append(Maps.CastleBoss)
        if Items.Barrels in ownedMoves[level]:
            # These bosses only care about barrels
            bossOptions[level].extend([Maps.JapesBoss, Maps.AztecBoss, Maps.CavesBoss])
            # Dogadon 2 also needs Hunky and Chunky
            if Kongs.chunky in ownedKongs[level] and Items.HunkyChunky in ownedMoves[level]:
                bossOptions[level].append(Maps.FungiBoss)
            # Lanky Phase also needs Lanky and Trombone
            is_beta_lanky = IsDDMSSelected(spoiler.settings.hard_bosses_selected, HardBossesSelected.beta_lanky_phase)
            required_additional_item_lankyphase = Items.Grape if is_beta_lanky else Items.Trombone
            if spoiler.settings.krool_in_boss_pool_v2 != KroolInBossPool.off and Kongs.lanky in ownedKongs[level] and required_additional_item_lankyphase in ownedMoves[level]:
                bossOptions[level].append(Maps.KroolLankyPhase)
        # Mad Jack always requires a slam
        if Items.ProgressiveSlam in ownedMoves[level]:
            # In hard bosses any of Donkey, Tiny, or Chunky is sufficient
            if HardBossesEnabled(spoiler.settings, HardBossesSelected.alternative_mad_jack_kongs) and any([kong for kong in ownedKongs[level] if kong in [Kongs.donkey, Kongs.tiny, Kongs.chunky]]):
                bossOptions[level].append(Maps.FactoryBoss)
            # Outside of hard bosses, you need exactly Tiny and Twirl
            elif Kongs.tiny in ownedKongs[level] and Items.PonyTailTwirl in ownedMoves[level]:
                bossOptions[level].append(Maps.FactoryBoss)
        if spoiler.settings.krool_in_boss_pool_v2 != KroolInBossPool.off:
            # Donkey Phase may or may not need Blast
            if Kongs.donkey in ownedKongs[level] and Items.Climbing in ownedMoves[level] and (not spoiler.settings.cannons_require_blast or Items.BaboonBlast in ownedMoves[level]):
                bossOptions[level].append(Maps.KroolDonkeyPhase)
            # Diddy Phase needs Peanut and Rocket
            if Kongs.diddy in ownedKongs[level] and Items.RocketbarrelBoost in ownedMoves[level] and Items.Peanut in ownedMoves[level]:
                bossOptions[level].append(Maps.KroolDiddyPhase)
            # Tiny Phase needs Mini and Feather (no Orange logic yet (or ever?))
            if Kongs.tiny in ownedKongs[level] and Items.MiniMonkey in ownedMoves[level] and Items.Feather in ownedMoves[level]:
                bossOptions[level].append(Maps.KroolTinyPhase)
            # Chunky Phase always needs Punch, Hunky, and Gorilla Gone
            if Kongs.chunky in ownedKongs[level] and Items.PrimatePunch in ownedMoves[level] and Items.HunkyChunky in ownedMoves[level] and Items.GorillaGone in ownedMoves[level]:
                # It also needs some number of slams - reference the settings for that number
                slamsRequired = 1
                spoiler.settings.chunky_phase_slam_req_internal
                if spoiler.settings.chunky_phase_slam_req_internal == SlamRequirement.blue:
                    slamsRequired = 2
                elif spoiler.settings.chunky_phase_slam_req_internal == SlamRequirement.red:
                    slamsRequired = 3
                if ownedMoves[level].count(Items.ProgressiveSlam) >= slamsRequired:
                    bossOptions[level].append(Maps.KroolChunkyPhase)
        # Quick filter to remove any boss options that we don't want to be added
        bossOptions[level] = [x for x in bossOptions[level] if x in spoiler.settings.bosses_selected]
    placedLevels = []
    placedBossMaps = []
    placedBossKongs = []
    clearedBossMaps = False
    while len(placedLevels) < 7:
        # The number of options are the boss options for each level not already placed
        levelsSortedByNumberOfOptions = [level for level in bossOptions.keys() if level not in placedLevels]
        # This can include endgame phases, and this is intentional. If you have to squeeze in every boss/phase into this, you need every inch of leeway you can get.
        # By sorting by the raw amount of available boss space, you won't ever place bosses in a bad order (outside of utterly egregious circumstances).
        levelsSortedByNumberOfOptions.sort(
            key=lambda x: len([map for map in bossOptions[x] if map not in placedBossMaps]) + spoiler.settings.random.random()
        )  # The random factor here is so there's randomness among tied counts (but never greater than 1)
        # Always pick the level with the least options - this guarantees we never orphan a level with no options (unless it was forced anyway)
        mostRestrictiveLevel = levelsSortedByNumberOfOptions[0]
        if spoiler.settings.allow_boss_duping:
            notTakenBossOptions = [map for map in bossOptions[mostRestrictiveLevel] if map not in placedBossMaps]
        else:
            notTakenBossOptions = [map for map in bossOptions[mostRestrictiveLevel] if map not in placedBossMaps and map not in spoiler.settings.krool_order]
        chosenBoss = None
        # If we don't have an option available for this very restrictive level
        # OR if we haven't placed many bosses yet, we'll take a peek at the endgame and see if any of those could fit
        if not any(notTakenBossOptions) and spoiler.settings.allow_boss_duping:
            if not clearedBossMaps:  # To prevent against potential inf loops
                placedBossMaps = []  # Clear placed bosses
                clearedBossMaps = True
                continue
        if not any(notTakenBossOptions) or (spoiler.settings.krool_in_boss_pool_v2 != KroolInBossPool.off and len(placedLevels) < 2):
            # If we don't have an option available, desperate times call for desperate measures
            # If T&S Bosses could be on endgame fights, we might have to go steal one
            if spoiler.settings.krool_in_boss_pool_v2 != KroolInBossPool.off:
                # It's possible we can take a boss out of the endgame rotation and put it here instead
                possibleEndgameBossSwaps = [map for map in bossOptions[mostRestrictiveLevel] if map in spoiler.settings.krool_order]
                # If we can't do that, then there exists no combination of bosses that could make this fill work
                if not any(possibleEndgameBossSwaps) and not any(notTakenBossOptions):
                    # I *really* hope this is infrequent or limited to lava water shenanigans
                    raise BossOutOfLocationsException("Fill has no valid boss/phase placement combinations.")
                expandedBossOptions = notTakenBossOptions + possibleEndgameBossSwaps
                chosenBoss = spoiler.settings.random.choice(expandedBossOptions)
                if chosenBoss in possibleEndgameBossSwaps:
                    spoiler.settings.krool_order.remove(chosenBoss)
                    updateKRoolSettings(spoiler, chosenBoss)
            else:
                # This is likely limited to lava water shenanigans
                raise BossOutOfLocationsException("Fill has no valid boss placement combinations.")
        else:
            chosenBoss = spoiler.settings.random.choice(notTakenBossOptions)
        kongOptions = [
            kong for kong in GetKongOptionsForBoss(chosenBoss, HardBossesEnabled(spoiler.settings, HardBossesSelected.alternative_mad_jack_kongs)) if kong in ownedKongs[mostRestrictiveLevel]
        ]
        # This should be impossible, as bossOptions is populated referencing the ownedKongs dict
        # This could become possible if a boss becomes beatable with unique combinations of Kong + move (e.g. a boss is beatable with (Kong A + Move B) OR (Kong C + Move D))
        if len(kongOptions) == 0:
            # I'll just hedge my bets anyway - remove this boss from eligiblility for this level and try again
            bossOptions[mostRestrictiveLevel].remove(chosenBoss)
            continue
        # These will be the same index which will be convenient later
        placedLevels.append(mostRestrictiveLevel)
        placedBossMaps.append(chosenBoss)
        placedBossKongs.append(Kongs(spoiler.settings.random.choice(kongOptions)))
        clearedBossMaps = False  # Clear flag
    # If we did steal a boss from the endgame, we need to put one back in.
    # Note that this has zero impact on logic: you should have all items by the time you reach the endgame
    while len(spoiler.settings.krool_order) < spoiler.settings.krool_phase_count:
        if spoiler.settings.allow_boss_duping:
            possibleBosses = [map for map in getBosses(spoiler.settings) if map not in placedBossMaps and map]
        else:
            possibleBosses = [map for map in getBosses(spoiler.settings) if map not in placedBossMaps and map not in spoiler.settings.krool_order]
        newEndgameBoss = spoiler.settings.random.choice(possibleBosses)
        spoiler.settings.krool_order.append(newEndgameBoss)
        updateKRoolSettings(spoiler, newEndgameBoss)
        spoiler.settings.random.shuffle(spoiler.settings.krool_order)
        # UHHHH does this fuck with kongs assigned to phases? SURE HOPE NOT!
    newBossMaps = [None, None, None, None, None, None, None]
    newBossKongs = [None, None, None, None, None, None, None]
    for level in bossOptions.keys():
        index = placedLevels.index(level)
        newBossMaps[level] = placedBossMaps[index]
        newBossKongs[level] = placedBossKongs[index]

    # Only apply this shuffle if the settings permit it
    # If kongs are random we have to shuffle bosses and locations or else we might break logic
    if spoiler.settings.kong_rando or spoiler.settings.boss_location_rando:
        spoiler.settings.boss_maps = newBossMaps
    else:
        spoiler.settings.boss_maps = getBosses(spoiler.settings)
    if spoiler.settings.kong_rando or spoiler.settings.boss_location_rando:
        # If we shuffle kongs but not locations, we must forcibly sort the array with the known valid kongs
        if not spoiler.settings.boss_location_rando:
            # This is outrageously niche, I sure hope it doesn't break
            spoiler.settings.boss_kongs = [
                spoiler.settings.random.choice([kong for kong in GetKongOptionsForBoss(Maps.JapesBoss, False) if kong in bossOptions[Levels.JungleJapes]]),
                spoiler.settings.random.choice([kong for kong in GetKongOptionsForBoss(Maps.AztecBoss, False) if kong in bossOptions[Levels.AngryAztec]]),
                spoiler.settings.random.choice(
                    [
                        kong
                        for kong in GetKongOptionsForBoss(
                            Maps.FactoryBoss,
                            HardBossesEnabled(spoiler.settings, HardBossesSelected.alternative_mad_jack_kongs),
                        )
                        if kong in bossOptions[Levels.FranticFactory]
                    ]
                ),
                spoiler.settings.random.choice([kong for kong in GetKongOptionsForBoss(Maps.GalleonBoss, False) if kong in bossOptions[Levels.GloomyGalleon]]),
                spoiler.settings.random.choice([kong for kong in GetKongOptionsForBoss(Maps.FungiBoss, False) if kong in bossOptions[Levels.FungiForest]]),
                spoiler.settings.random.choice([kong for kong in GetKongOptionsForBoss(Maps.CavesBoss, False) if kong in bossOptions[Levels.CrystalCaves]]),
                spoiler.settings.random.choice([kong for kong in GetKongOptionsForBoss(Maps.CastleBoss, False) if kong in bossOptions[Levels.CreepyCastle]]),
            ]
        else:
            spoiler.settings.boss_kongs = newBossKongs
    else:
        spoiler.settings.boss_kongs = ShuffleBossKongs(spoiler.settings)
    spoiler.settings.kutout_kongs = ShuffleKutoutKongs(spoiler.settings.random, spoiler.settings.boss_maps, spoiler.settings.boss_kongs, spoiler.settings.boss_location_rando)


def ShuffleTinyPhaseToes(random):
    """Generate random assortment of toes for Tiny Phase."""
    toe_sequence = []
    previous_toe = 1  # Use 1 as the index as it's within distance of all toes, so all toes for the first in the sequence will be valid
    for toe in range(10):
        mode = random.randint(0, 10)
        if (toe % 5) == 0:
            # Prevent player position mode on the first toe
            mode += 1
        if mode == 0:
            # Use player position
            toe_sequence.append(0xFF)
            previous_toe = 1
        else:
            # Determine random assortment
            toe_list = list(range(4))
            if (toe % 5) == 0:
                # First toe
                toe_list = [0, 2, 3]
            toe_list = [x for x in toe_list if abs(x - previous_toe) < 3]  # Prevent toes being selected that
            toe_count = random.randint(1, min(3, len(toe_list) - 1))
            if len(toe_list) <= 1:
                toe_bitfield = 0
            else:
                activated_toes = random.sample(toe_list, toe_count)
                unactivated_toes = [x for x in list(range(4)) if x not in activated_toes]
                picked_toe = False
                for t in (1, 2):
                    if t in unactivated_toes:
                        previous_toe = t
                        picked_toe = True
                if not picked_toe:
                    previous_toe = random.choice(unactivated_toes)
                toe_bitfield = 0
                for toe in activated_toes:
                    toe_bitfield |= 1 << toe
            toe_sequence.append(toe_bitfield)
    return toe_sequence.copy()


def CorrectBossKongLocations(spoiler):
    """Correct the Kong assigned to each boss Location for more accurate hints."""
    spoiler.LocationList[Locations.JapesKey].kong = spoiler.settings.boss_kongs[0]
    spoiler.LocationList[Locations.AztecKey].kong = spoiler.settings.boss_kongs[1]
    spoiler.LocationList[Locations.FactoryKey].kong = spoiler.settings.boss_kongs[2]
    spoiler.LocationList[Locations.GalleonKey].kong = spoiler.settings.boss_kongs[3]
    spoiler.LocationList[Locations.ForestKey].kong = spoiler.settings.boss_kongs[4]
    spoiler.LocationList[Locations.CavesKey].kong = spoiler.settings.boss_kongs[5]
    spoiler.LocationList[Locations.CastleKey].kong = spoiler.settings.boss_kongs[6]


def updateKRoolSettings(spoiler, phase):
    """Make sure the settings match the phases in the K. Rool order."""
    if phase == Maps.KroolDonkeyPhase:
        spoiler.settings.krool_donkey = not spoiler.settings.krool_donkey
    elif phase == Maps.KroolDiddyPhase:
        spoiler.settings.krool_diddy = not spoiler.settings.krool_diddy
    elif phase == Maps.KroolLankyPhase:
        spoiler.settings.krool_lanky = not spoiler.settings.krool_lanky
    elif phase == Maps.KroolTinyPhase:
        spoiler.settings.krool_tiny = not spoiler.settings.krool_tiny
    elif phase == Maps.KroolChunkyPhase:
        spoiler.settings.krool_chunky = not spoiler.settings.krool_chunky
    elif phase == Maps.JapesBoss:
        spoiler.settings.krool_dillo1 = not spoiler.settings.krool_dillo1
    elif phase == Maps.AztecBoss:
        spoiler.settings.krool_dog1 = not spoiler.settings.krool_dog1
    elif phase == Maps.FactoryBoss:
        spoiler.settings.krool_madjack = not spoiler.settings.krool_madjack
    elif phase == Maps.GalleonBoss:
        spoiler.settings.krool_pufftoss = not spoiler.settings.krool_pufftoss
    elif phase == Maps.FungiBoss:
        spoiler.settings.krool_dog2 = not spoiler.settings.krool_dog2
    elif phase == Maps.CavesBoss:
        spoiler.settings.krool_dillo2 = not spoiler.settings.krool_dillo2
    elif phase == Maps.CastleBoss:
        spoiler.settings.krool_kutout = not spoiler.settings.krool_kutout


def PlandoBosses(spoiler):
    """Fix bosses into their plando'd positions and then randomly fill the rest. This fill supercedes the standard boss placement algorithm."""
    if spoiler.settings.boss_plando:
        filledBosses = []
        filledLevels = []
        for level in range(7):
            # If we intend to plando this boss, send it in there
            if spoiler.settings.plandomizer_dict["plando_boss_order_" + str(level)] != -1:
                bossMap = Maps(spoiler.settings.plandomizer_dict["plando_boss_order_" + str(level)])
                plannedKong = spoiler.settings.plandomizer_dict["plando_boss_kong_" + str(level)]
                eligibleKongs = GetKongOptionsForBoss(bossMap, HardBossesEnabled(spoiler.settings, HardBossesSelected.alternative_mad_jack_kongs))
                if plannedKong != -1:
                    # If the planned Kong is incompatible with this boss, ship it back
                    if plannedKong not in eligibleKongs:
                        raise PlandoIncompatibleException(str(Kongs(plannedKong).name) + " is not eligible to fight " + str(bossMap.name))
                    spoiler.settings.boss_kongs[level] = Kongs(plannedKong)
                else:
                    spoiler.settings.boss_kongs[level] = spoiler.settings.random.choice(eligibleKongs)
                spoiler.settings.boss_maps[level] = bossMap
                filledBosses.append(bossMap)
                filledLevels.append(level)
        remainingBosses = [boss for boss in getBosses(spoiler.settings) if boss not in filledBosses]
        for level in range(7):
            if level in filledLevels:
                continue
            bossMap = spoiler.settings.random.choice(remainingBosses)
            spoiler.settings.boss_maps[level] = bossMap
            remainingBosses.remove(bossMap)
        spoiler.settings.boss_kongs = ShuffleBossKongs(spoiler.settings, locked_levels=filledLevels)
        spoiler.settings.kutout_kongs = ShuffleKutoutKongs(spoiler.settings.random, spoiler.settings.boss_maps, spoiler.settings.boss_kongs, spoiler.settings.boss_location_rando)
