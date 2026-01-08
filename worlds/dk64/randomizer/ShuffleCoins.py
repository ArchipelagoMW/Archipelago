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


def getCoinRequirement(random) -> int:
    """Get requirement for a kong's coin amount."""
    return int(random.randint(KONG_COIN_REQUIREMENT, KONG_COIN_CAP) / 8)


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
            for level_index, level in enumerate(level_data):
                level_placement = []
                global_divisor = 7 - level_index
                kong_specific_left = {
                    Kongs.donkey: getCoinRequirement(spoiler.settings.random),
                    Kongs.diddy: getCoinRequirement(spoiler.settings.random),
                    Kongs.lanky: getCoinRequirement(spoiler.settings.random),
                    Kongs.tiny: getCoinRequirement(spoiler.settings.random),
                    Kongs.chunky: getCoinRequirement(spoiler.settings.random),
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
