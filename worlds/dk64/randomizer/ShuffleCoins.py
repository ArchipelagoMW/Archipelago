"""Select Coin Location selection."""

import js
import randomizer.CollectibleLogicFiles.AngryAztec
import randomizer.CollectibleLogicFiles.CreepyCastle
import randomizer.CollectibleLogicFiles.CrystalCaves
import randomizer.CollectibleLogicFiles.DKIsles
import randomizer.CollectibleLogicFiles.FranticFactory
import randomizer.CollectibleLogicFiles.FungiForest
import randomizer.CollectibleLogicFiles.GloomyGalleon
import randomizer.CollectibleLogicFiles.JungleJapes
import randomizer.Fill as Fill
import randomizer.Lists.Exceptions as Ex
from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Maps import Maps
from randomizer.Lists.BananaCoinLocations import BananaCoinGroupList
from randomizer.LogicClasses import Collectible

KONG_COIN_REQUIREMENT = 100
KONG_COIN_CAP = 125  # Can never exceed 175 due to overflow if you collect over 255 coins

level_data = {
    Levels.DKIsles: randomizer.CollectibleLogicFiles.DKIsles.LogicRegions,
    Levels.JungleJapes: randomizer.CollectibleLogicFiles.JungleJapes.LogicRegions,
    Levels.AngryAztec: randomizer.CollectibleLogicFiles.AngryAztec.LogicRegions,
    Levels.FranticFactory: randomizer.CollectibleLogicFiles.FranticFactory.LogicRegions,
    Levels.GloomyGalleon: randomizer.CollectibleLogicFiles.GloomyGalleon.LogicRegions,
    Levels.FungiForest: randomizer.CollectibleLogicFiles.FungiForest.LogicRegions,
    Levels.CrystalCaves: randomizer.CollectibleLogicFiles.CrystalCaves.LogicRegions,
    Levels.CreepyCastle: randomizer.CollectibleLogicFiles.CreepyCastle.LogicRegions,
    Levels.DKIsles: randomizer.CollectibleLogicFiles.DKIsles.LogicRegions,
}


def getCoinRequirement(random, level: Levels) -> int:
    """Get requirement for a kong's coin amount."""
    req = KONG_COIN_REQUIREMENT
    cap = KONG_COIN_CAP
    if level == Levels.FranticFactory:
        # Reduce burden on Factory
        req = 80
        cap = 110
    return int(random.randint(req, cap) / 8)


def ShuffleCoins(spoiler):
    """Shuffle Coins selected from location files."""
    retries = 0
    while True:
        try:
            total_coins = 0
            coin_data = []
            # First, remove all placed coins (excl. Rabbit Race R1)
            for region_id in spoiler.CollectibleRegions.keys():
                spoiler.CollectibleRegions[region_id] = [collectible for collectible in spoiler.CollectibleRegions[region_id] if collectible.type != Collectibles.coin or collectible.locked]
            for level in BananaCoinGroupList:
                for group in BananaCoinGroupList[level]:
                    if group.placed_type == Collectibles.coin:
                        group.placed_type = None
            for level_index, level in enumerate(level_data):
                level_placement = []
                global_divisor = 7 - level_index
                kong_specific_left = {
                    Kongs.donkey: getCoinRequirement(spoiler.settings.random, level),
                    Kongs.diddy: getCoinRequirement(spoiler.settings.random, level),
                    Kongs.lanky: getCoinRequirement(spoiler.settings.random, level),
                    Kongs.tiny: getCoinRequirement(spoiler.settings.random, level),
                    Kongs.chunky: getCoinRequirement(spoiler.settings.random, level),
                }
                coins_left = (KONG_COIN_CAP * 5) - total_coins
                coins_lower = max(int(coins_left / (8 - level_index)) - 10, 0)
                if global_divisor == 0:
                    coins_upper = min(coins_left, int((5 * ((5 * KONG_COIN_CAP) - total_coins) - sum(kong_specific_left)) / 4))  # Places a hard cap of 1127 total singles+bunches
                else:
                    coins_upper = min(int(coins_left / (8 - level_index)) + 10, int(coins_left / global_divisor))
                groupIds = list(range(1, len(BananaCoinGroupList[level]) + 1))
                spoiler.settings.random.shuffle(groupIds)
                selected_coin_count = spoiler.settings.random.randint(min(coins_lower, coins_upper), max(coins_lower, coins_upper))
                placed_coins = 0
                for groupId in groupIds:
                    group_weight = 0
                    coin_groups = [group for group in BananaCoinGroupList[level] if group.group == groupId]
                    coin_kongs = list(kong_specific_left.keys())
                    for group in coin_groups:
                        coin_kongs = list(set(coin_kongs) & set(group.kongs.copy()))
                        group_weight = len(group.locations)
                    if len(coin_kongs) > 0 and (selected_coin_count >= placed_coins + group_weight):
                        selected_kong = spoiler.settings.random.choice(coin_kongs)
                        kong_specific_left[selected_kong] -= group_weight  # Remove Coins for kong
                        # When a kong goes under/equal to 0 remaining in this level, we no longer need to consider it
                        if kong_specific_left[selected_kong] <= 0:
                            del kong_specific_left[selected_kong]
                        for group in coin_groups:
                            # Calculate the number of coins we have to place by lesser group so different coins in the same group can have different logic
                            coins_in_group = len(group.locations)
                            if coins_in_group > 0:
                                if group.region not in spoiler.CollectibleRegions:
                                    spoiler.CollectibleRegions[group.region] = []
                                spoiler.CollectibleRegions[group.region].append(
                                    Collectible(
                                        Collectibles.coin,
                                        selected_kong,
                                        group.logic,
                                        None,
                                        coins_in_group,
                                        name=group.name,
                                    )
                                )
                            level_placement.append(
                                {
                                    "group": group.group,
                                    "name": group.name,
                                    "kong": selected_kong,
                                    "level": level,
                                    "map": group.map,
                                    "locations": group.locations,
                                }
                            )
                            for group in BananaCoinGroupList[level]:
                                if group.group == groupId:
                                    group.placed_type = Collectibles.coin
                        placed_coins += group_weight
                    # If all kongs have 0 unplaced, we're done here
                    if len(kong_specific_left.keys()) == 0:
                        break

                # Placement is valid
                coin_data.extend(level_placement.copy())
            spoiler.Reset()
            if not Fill.VerifyWorld(spoiler):
                raise Ex.CoinFillFailureException
            spoiler.coin_placements = coin_data
            return
        except Ex.CoinFillFailureException:
            if retries >= 10:
                js.postMessage("Coin Randomizer failed to fill. REPORT THIS TO THE DEVS!!")
                raise Ex.CoinFillFailureException
            retries += 1
            js.postMessage("Coin Randomizer failed to fill. Tries: " + str(retries))


RACE_COINS_TO_PLACE = 97 + 71 + 25 + 19 + 87 + 77 + 68 + 17
BANNED_COIN_MAPS = [
    Maps.JapesMinecarts,
    Maps.AztecTinyRace,
    Maps.FactoryTinyRace,
    Maps.GalleonSealRace,
    Maps.ForestMinecarts,
    Maps.CavesLankyRace,
    Maps.CastleTinyRace,
    Maps.CastleMinecarts,
]


def shuffleRaceCoins(spoiler):
    """Shuffle race coins selected from location files."""
    retries = 0
    while True:
        try:
            race_coin_data = []
            # First, remove all placed race coins
            for region_id in spoiler.CollectibleRegions.keys():
                spoiler.CollectibleRegions[region_id] = [collectible for collectible in spoiler.CollectibleRegions[region_id] if collectible.type != Collectibles.racecoin or collectible.locked]
            for level in BananaCoinGroupList:
                for group in BananaCoinGroupList[level]:
                    if group.placed_type == Collectibles.racecoin:
                        group.placed_type = None
            coins_to_place_factory = RACE_COINS_TO_PLACE / (len(level_data) * 2)
            coins_to_place_in_level = (RACE_COINS_TO_PLACE - coins_to_place_factory) / (len(level_data) - 1)
            for level in level_data:
                level_placement = []
                coin_size = coins_to_place_in_level
                if level == Levels.FranticFactory:
                    coin_size = coins_to_place_factory
                groupIds = list(set([group.group for group in BananaCoinGroupList[level] if group.placed_type is None and group.map not in BANNED_COIN_MAPS]))
                spoiler.settings.random.shuffle(groupIds)
                for groupId in groupIds:
                    group_weight = 0
                    coin_groups = [group for group in BananaCoinGroupList[level] if group.group == groupId]
                    for group in coin_groups:
                        group_weight = len(group.locations)
                    if coin_size >= group_weight:
                        coin_size -= group_weight  # Remove Coins
                        for group in coin_groups:
                            # Calculate the number of coins we have to place by lesser group so different coins in the same group can have different logic
                            if len(group.locations) > 0:
                                if group.region not in spoiler.CollectibleRegions:
                                    spoiler.CollectibleRegions[group.region] = []
                                spoiler.CollectibleRegions[group.region].append(Collectible(Collectibles.racecoin, Kongs.any, group.logic, None, len(group.locations), name=group.name))
                            level_placement.append(
                                {
                                    "group": group.group,
                                    "name": group.name,
                                    "level": level,
                                    "map": group.map,
                                    "locations": group.locations,
                                }
                            )
                            for group in BananaCoinGroupList[level]:
                                if group.group == groupId:
                                    group.placed_type = Collectibles.racecoin
                    # If all kongs have 0 unplaced, we're done here
                    if coin_size < 1:
                        break
                # Placement is valid
                race_coin_data.extend(level_placement.copy())
            spoiler.Reset()
            if not Fill.VerifyWorld(spoiler):
                raise Ex.RaceCoinFillFailureException
            spoiler.race_coin_placements = race_coin_data
            return
        except Ex.RaceCoinFillFailureException:
            if retries >= 10:
                js.postMessage("Race Coin Randomizer failed to fill. REPORT THIS TO THE DEVS!!")
                raise Ex.RaceCoinFillFailureException
            retries += 1
            js.postMessage("Race Coin Randomizer failed to fill. Tries: " + str(retries))
