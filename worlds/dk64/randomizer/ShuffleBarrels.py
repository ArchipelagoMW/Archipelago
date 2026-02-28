"""Module used to handle setting and randomizing bonus barrels."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, List
import math
import randomizer.Lists.Exceptions as Ex
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Minigames import Minigames
from randomizer.Enums.Settings import MinigameBarrels, MinigamesListSelected
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Maps import Maps
from randomizer.Lists.Minigame import BarrelMetaData, MinigameRequirements, MinigameLocationData
from randomizer.Settings import Settings


def Reset(shuffled_barrel_data: dict[Locations, MinigameLocationData], barrelLocations: List[Locations]) -> None:
    """Reset bonus barrel associations."""
    for key in barrelLocations:
        shuffled_barrel_data[key].minigame = Minigames.NoGame


def PreplacePlandoMinigames(settings: Settings, shuffled_barrel_data: dict[Locations, MinigameLocationData], barrelLocations: List[Locations]):
    """Apply plandomized minigame placement."""
    preplaced_minigame_locations = []
    for loc in barrelLocations:
        minigame_placed = False
        if str(loc.value) in settings.plandomizer_dict["plando_bonus_barrels"].keys():
            plando_minigame = settings.plandomizer_dict["plando_bonus_barrels"][str(loc.value)]
            if validate_minigame(loc, plando_minigame):
                shuffled_barrel_data[loc].minigame = plando_minigame
                minigame_placed = True
            else:
                raise Ex.PlandoIncompatibleException(f"Invalid minigame for {loc.name}: {MinigameRequirements[plando_minigame].name}")
        if minigame_placed:
            preplaced_minigame_locations.append(loc)
    for preplaced in preplaced_minigame_locations:
        barrelLocations.remove(preplaced)


def isValidBarrel(location: Locations, settings: Settings) -> bool:
    """Get whether a minigame can be placed in this barrel location."""
    if BarrelMetaData[location].map == Maps.HideoutHelm and settings.helm_barrels == MinigameBarrels.skip:
        return False
    elif BarrelMetaData[location].map == Maps.TrainingGrounds and settings.training_barrels_minigames == MinigameBarrels.skip:
        return False
    elif BarrelMetaData[location].map not in (Maps.HideoutHelm, Maps.TrainingGrounds) and settings.bonus_barrels == MinigameBarrels.skip:
        return False
    return True


def getRandomMinigame(location: Locations, pool: list[Minigames]) -> tuple:
    """Produce random minigame from a pool."""
    for index, minigame in enumerate(pool):
        # If this minigame isn't valid, don't use it
        if validate_minigame(location, minigame):
            # Place the minigame
            return minigame, True, index
    return None, False, None


def ShuffleBarrels(settings: Settings, shuffled_barrel_data: dict[Locations, MinigameLocationData], barrelLocations: List[Locations], minigamePool: List[Minigames]) -> None:
    """Shuffle minigames to different barrels."""
    settings.random.shuffle(barrelLocations)

    # Apply plandomized minigame placement
    if settings.enable_plandomizer and settings.plandomizer_dict["plando_bonus_barrels"] != {}:
        PreplacePlandoMinigames(settings, shuffled_barrel_data, barrelLocations)
    # Get barrel location count
    barrel_count = 0
    for barrel in barrelLocations:
        if isValidBarrel(barrel, settings):
            barrel_count += 1
    if len(minigamePool) == 0:
        raise Ex.BarrelOutOfMinigames
    # Get duplication Count - Add 10 barrels to allow for some wiggle room
    dupe_count = math.ceil((barrel_count + 10) / len(minigamePool))
    duped_minigame_pool = []
    for _ in range(dupe_count):
        duped_minigame_pool.extend(minigamePool)
    settings.random.shuffle(duped_minigame_pool)
    # Apply randomized minigame placement
    while len(barrelLocations) > 0:
        location = barrelLocations.pop()
        # Don't bother shuffling or validating barrel locations which are skipped
        if not isValidBarrel(location, settings):
            continue
        # Check each remaining minigame to see if placing it will produce a valid world
        minigame, success, index_to_remove = getRandomMinigame(location, duped_minigame_pool)
        if success:
            shuffled_barrel_data[location].minigame = minigame
            del duped_minigame_pool[index_to_remove]
        else:
            raise Ex.BarrelOutOfMinigames


def validate_minigame(location: Locations, minigame: Minigames):
    """Decide whether or not the given minigame is suitable for the given location."""
    # If this minigame isn't a minigame for the kong of this location, it's not valid
    req_kong = BarrelMetaData[location].kong
    kong_list = MinigameRequirements[minigame].kong_list
    if req_kong in kong_list or (req_kong == Kongs.any and len(kong_list) == 5):
        # If there is a minigame that can be placed in Helm, don't validate banned minigames, otherwise continue as normal
        return True
    return False


def BarrelShuffle(settings: Settings) -> dict[Locations, MinigameLocationData]:
    """Facilitate shuffling of barrels."""
    # First make master copies of locations and minigames
    barrelLocations = list(BarrelMetaData.keys())
    shuffled_barrel_data = deepcopy(BarrelMetaData)
    if (
        settings.bonus_barrels == MinigameBarrels.selected
        or (settings.helm_barrels == MinigameBarrels.random and settings.minigames_list_selected)
        or (settings.training_barrels_minigames == MinigameBarrels.random and settings.minigames_list_selected)
    ):
        minigame_dict = {
            MinigamesListSelected.batty_barrel_bandit: [
                Minigames.BattyBarrelBanditVEasy,
                Minigames.BattyBarrelBanditEasy,
                Minigames.BattyBarrelBanditNormal,
                Minigames.BattyBarrelBanditHard,
            ],
            MinigamesListSelected.big_bug_bash: [
                Minigames.BigBugBashVEasy,
                Minigames.BigBugBashEasy,
                Minigames.BigBugBashNormal,
                Minigames.BigBugBashHard,
            ],
            MinigamesListSelected.busy_barrel_barrage: [
                Minigames.BusyBarrelBarrageEasy,
                Minigames.BusyBarrelBarrageNormal,
                Minigames.BusyBarrelBarrageHard,
            ],
            MinigamesListSelected.mad_maze_maul: [
                Minigames.MadMazeMaulEasy,
                Minigames.MadMazeMaulNormal,
                Minigames.MadMazeMaulHard,
                Minigames.MadMazeMaulInsane,
            ],
            MinigamesListSelected.minecart_mayhem: [
                Minigames.MinecartMayhemEasy,
                Minigames.MinecartMayhemNormal,
                Minigames.MinecartMayhemHard,
            ],
            MinigamesListSelected.beaver_bother: [
                Minigames.BeaverBotherEasy,
                Minigames.BeaverBotherNormal,
                Minigames.BeaverBotherHard,
            ],
            MinigamesListSelected.teetering_turtle_trouble: [
                Minigames.TeeteringTurtleTroubleVEasy,
                Minigames.TeeteringTurtleTroubleEasy,
                Minigames.TeeteringTurtleTroubleNormal,
                Minigames.TeeteringTurtleTroubleHard,
            ],
            MinigamesListSelected.stealthy_snoop: [
                Minigames.StealthySnoopVEasy,
                Minigames.StealthySnoopEasy,
                Minigames.StealthySnoopNormal,
                Minigames.StealthySnoopHard,
            ],
            MinigamesListSelected.stash_snatch: [
                Minigames.StashSnatchEasy,
                Minigames.StashSnatchNormal,
                Minigames.StashSnatchHard,
                Minigames.StashSnatchInsane,
            ],
            MinigamesListSelected.splish_splash_salvage: [
                Minigames.SplishSplashSalvageEasy,
                Minigames.SplishSplashSalvageNormal,
                Minigames.SplishSplashSalvageHard,
            ],
            MinigamesListSelected.speedy_swing_sortie: [
                Minigames.SpeedySwingSortieEasy,
                Minigames.SpeedySwingSortieNormal,
                Minigames.SpeedySwingSortieHard,
            ],
            MinigamesListSelected.krazy_kong_klamour: [
                Minigames.KrazyKongKlamourEasy,
                Minigames.KrazyKongKlamourNormal,
                Minigames.KrazyKongKlamourHard,
                Minigames.KrazyKongKlamourInsane,
            ],
            MinigamesListSelected.searchlight_seek: [
                Minigames.SearchlightSeekVEasy,
                Minigames.SearchlightSeekEasy,
                Minigames.SearchlightSeekNormal,
                Minigames.SearchlightSeekHard,
            ],
            MinigamesListSelected.kremling_kosh: [
                Minigames.KremlingKoshVEasy,
                Minigames.KremlingKoshEasy,
                Minigames.KremlingKoshNormal,
                Minigames.KremlingKoshHard,
            ],
            MinigamesListSelected.peril_path_panic: [
                Minigames.PerilPathPanicVEasy,
                Minigames.PerilPathPanicEasy,
                Minigames.PerilPathPanicNormal,
                Minigames.PerilPathPanicHard,
            ],
            MinigamesListSelected.helm_minigames: [
                Minigames.DonkeyRambi,
                Minigames.DonkeyTarget,
                Minigames.DiddyKremling,
                Minigames.DiddyRocketbarrel,
                Minigames.LankyMaze,
                Minigames.LankyShooting,
                Minigames.TinyMushroom,
                Minigames.TinyPonyTailTwirl,
                Minigames.ChunkyHiddenKremling,
                Minigames.ChunkyShooting,
            ],
            MinigamesListSelected.arenas: [
                Minigames.RambiArena,
                Minigames.EnguardeArena,
            ],
            MinigamesListSelected.training_minigames: [
                Minigames.OrangeBarrel,
                Minigames.BarrelBarrel,
                Minigames.VineBarrel,
                Minigames.DiveBarrel,
            ],
            MinigamesListSelected.arcade: [
                Minigames.Arcade25,
                Minigames.Arcade50,
                Minigames.Arcade75,
                Minigames.Arcade100,
                Minigames.JetpacRocket,
            ],
        }
        # If Stealthy Snoop is not selected, don't include the Stash Snatch variant with Kops
        if MinigamesListSelected.stealthy_snoop not in settings.minigames_list_selected:
            minigame_dict[MinigamesListSelected.stash_snatch].remove(Minigames.StashSnatchHard)
        minigamePool = []
        for name, value in minigame_dict.items():
            if name in settings.minigames_list_selected:
                minigamePool.extend([x for x in MinigameRequirements.keys() if x in value])
    else:
        minigamePool = [x for x in MinigameRequirements.keys() if x != Minigames.NoGame]
    if settings.disable_hard_minigames:
        minigamePool = [game for game in minigamePool if not MinigameRequirements[game].is_hard]
    # Shuffle barrels
    Reset(shuffled_barrel_data, barrelLocations)
    ShuffleBarrels(settings, shuffled_barrel_data, barrelLocations.copy(), minigamePool.copy())
    return shuffled_barrel_data
