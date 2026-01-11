# Chest randomization logic.

import math
import random

from .keys import Inventory
from ...randomizer.data import items, locations, chests
from ...randomizer.data.keys import KeyItemLocation
from ...randomizer.logic import flags, keys
from . import utils


def _intershuffle_chests(chest_locations):
    """Shuffle the contents of the provided list of chests between each other.

    Args:
        chest_locations(list[randomizer.data.chests.Chest]):

    """
    chests_to_shuffle = chest_locations[:]
    random.shuffle(chests_to_shuffle)

    for chest in chests_to_shuffle:
        # Get other chests in this group that are able to swap items and pick one.
        options = [swap for swap in chest_locations if swap != chest and chest.item_allowed(swap.item) and
                   swap.item_allowed(chest.item)]
        if options:
            swap = random.choice(options)
            chest.item, swap.item = swap.item, chest.item


def randomize_all(world, ap_data):
    """

    Args:
        world (randomizer.logic.main.GameWorld): Game world to randomize.
        ap_data (dict[str, str]): Archipelago placement data.
    """

    # Get limitation of items allowed first
    tiers_allowed = 4
    if world.settings.is_flag_enabled(flags.ChestTier1):
        tiers_allowed = 1
    elif world.settings.is_flag_enabled(flags.ChestTier2):
        tiers_allowed = 2
    elif world.settings.is_flag_enabled(flags.ChestTier3):
        tiers_allowed = 3


    coins_allowed = not world.settings.is_flag_enabled(flags.ChestExcludeCoins)
    flowers_allowed = not world.settings.is_flag_enabled(flags.ChestExcludeFlowers)
    frogcoins_allowed = not world.settings.is_flag_enabled(flags.ChestExcludeFrogCoins)
    mushrooms_allowed = not world.settings.is_flag_enabled(flags.ChestExcludeMushrooms)
    stars_allowed = not world.settings.is_flag_enabled(flags.ChestExcludeStars)

    biased = world.settings.is_flag_enabled(flags.ChestShuffleBiased)
    include_key_items = world.settings.is_flag_enabled(flags.ChestIncludeKeyItems)

    coins = [items.Coins5, items.Coins8, items.Coins10, items.Coins150, items.Coins100, items.Coins50,
             items.CoinsDoubleBig]
    stars = [items.BanditsWayStar, items.KeroSewersStar, items.MolevilleMinesStar, items.SeaStar,
             items.LandsEndVolcanoStar, items.NimbusLandStar, items.LandsEndStar2, items.LandsEndStar3]

    # Items allowed for leftover chests where there is no valid item remaining for them (coins or mushroom).
    leftovers = coins[:]
    leftovers += [items.FrogCoin, items.RecoveryMushroom]

    forceCoinsInBanditsWay = False
    # special case: coins only if countdown in BW5 -- pre-set it in case B is set but T is not
    for location in world.boss_locations:
        if location.name in ["Croco1"]:
            for enemy in location.pack.common_enemies:
                if enemy.overworld_sprite != None:
                    shuffled_boss = enemy
                    if shuffled_boss.name == "CountDown":
                        forceCoinsInBanditsWay = True
                        forced_coins = [chest for chest in world.chest_locations if isinstance(chest, chests.BanditsWayCroco)]
                        forced_coins[0].item = random.choice([i for i in coins])

    # Open mode-specific shuffles.
    if world.open_mode:
        # Same area shuffle.
        if world.settings.is_flag_enabled(flags.ChestArchipelago):
            chest_locations: list = world.chest_locations + world.key_locations
            for chest in [location for location in chest_locations if ap_data[location.name].name == "InvincibilityStar"]:
                chest.item = random.choice([star for star in stars])
                chest_locations.remove(chest)
            keys.fill_locations(world, chest_locations, Inventory(), Inventory(), ap_data)

        elif world.settings.is_flag_enabled(flags.ChestShuffle1):
            for area in locations.Area:
                group = [chest for chest in world.chest_locations if chest.area == area]
                if group:
                    _intershuffle_chests(group)
            for chest in world.chest_locations:
                tiered_item = None
                for i in world.items:
                    if chest.item.index == i.index:
                        tiered_item = i
                if ((chest.item in coins and not coins_allowed) or (chest.item in stars and not stars_allowed) or
                        (chest.item == items.Flower and not flowers_allowed) or
                        (chest.item == items.RecoveryMushroom and not mushrooms_allowed) or
                        (chest.item == items.FrogCoin and not frogcoins_allowed) or
                        (tiered_item and tiered_item.hard_tier > tiers_allowed)):
                    # Put "You Missed!" empty item if allowed, otherwise just put some coins if this spot is empty.
                    if chest.item_allowed(items.YouMissed):
                        chest.item = items.YouMissed
                    elif chest.item_allowed(items.Mushroom):
                        chest.item = items.Mushroom
            if forceCoinsInBanditsWay:
                forced_coins = [chest for chest in world.chest_locations if isinstance(chest, chests.BanditsWayCroco)]
                forced_coins[0].item = random.choice([i for i in coins])

        # Empty chests.
        elif world.settings.is_flag_enabled(flags.ChestShuffleEmpty):
            for chest in world.chest_locations:
                if chest.item_allowed(items.YouMissed):
                    chest.item = items.YouMissed

        elif (world.settings.is_flag_enabled(flags.ChestShuffleBiased) or
              world.settings.is_flag_enabled(flags.ChestShuffleChaos)):
            finished_chests = []
            items_already_in_chests = []

            # Here I'm just figuring out the rough distribution of each type to target.
            # We can consider mutating these probabilities.
            ratio_coins = len([chest for chest in world.chest_locations if
                               not isinstance(chest, chests.Reward) and chest.item in coins])
            ratio_frogcoins = len([chest for chest in world.chest_locations if
                                   not isinstance(chest, chests.Reward) and chest.item == items.FrogCoin]) - 2
            ratio_mushrooms = len([chest for chest in world.chest_locations if
                                   not isinstance(chest, chests.Reward) and chest.item == items.RecoveryMushroom])
            ratio_flowers = len([chest for chest in world.chest_locations if
                                 not isinstance(chest, chests.Reward) and chest.item == items.Flower]) - 8
            ratio_stars = len([chest for chest in world.chest_locations if
                               not isinstance(chest, chests.Reward) and chest.item in stars])
            ratio_items = len([chest for chest in world.chest_locations if
                               not isinstance(chest, chests.Reward) and chest.item not in coins and
                               chest.item not in stars and chest.item not in
                               [items.FrogCoin, items.RecoveryMushroom, items.Flower, items.YouMissed]])
            denominator = ratio_items

            # These are the relative ratios used to calculate distribution properties.
            # This is where we build the denominator.
            if coins_allowed:
                denominator += ratio_coins
            if flowers_allowed:
                denominator += ratio_flowers
            if mushrooms_allowed:
                denominator += ratio_mushrooms
            if stars_allowed:
                denominator += ratio_stars
            if frogcoins_allowed:
                denominator += ratio_frogcoins

            # factor in KIs allowed here
            total_chests = ratio_coins + ratio_frogcoins + ratio_mushrooms + ratio_flowers + ratio_stars + ratio_items

            # How should items vs non-items be balanced?
            # Do stars first
            if stars_allowed:
                if world.settings.is_flag_enabled(flags.ChestRandomizeStars):
                    eligible_chests = [chest for chest in world.chest_locations if
                                       chest.item_allowed(items.BanditsWayStar)]
                    # randomize how many stars there will be - usually close to vanilla #
                    num_stars = utils.mutate_normal(min(
                        len(eligible_chests), math.floor(ratio_stars / denominator * total_chests)),
                        minimum=1, maximum=len(eligible_chests))
                    if num_stars > len(eligible_chests):
                        num_stars = len(eligible_chests)
                    while len(finished_chests) < num_stars:
                        chest = random.choice(eligible_chests)
                        if biased:
                            chest.item = random.choice([star for star in stars if star.hard_tier == chest.access])
                        else:
                            chest.item = random.choice([star for star in stars])
                        finished_chests.append(chest)
                        eligible_chests.remove(chest)
                        # Don't allow 2 stars in same bandits way room
                        if (isinstance(chest, chests.BanditsWayStarChest) or
                                isinstance(chest, chests.BanditsWayDogJump)):
                            for c in eligible_chests:
                                if (isinstance(c, chests.BanditsWayStarChest) or
                                        isinstance(c, chests.BanditsWayDogJump)):
                                    eligible_chests.remove(c)
                                    num_stars -= 1
                else:
                    eligible_chests = [chest for chest in world.chest_locations if 201 <= chest.item.index <= 208]
                    for chest in eligible_chests:
                        finished_chests.append(chest)
                    for chest in eligible_chests:
                        eligible_chests.remove(chest)
                denominator -= ratio_stars

            if forceCoinsInBanditsWay:
                forced_coins = [chest for chest in world.chest_locations if isinstance(chest, chests.BanditsWayCroco)]
                forced_coins[0].item = random.choice([i for i in coins])
                finished_chests.append(forced_coins[0])

            # then do the rest
            # biasing of items for chest
            def get_eligible_tier(chest_tier):
                selector = random.randint(1, 100)
                if chest_tier == 4:
                    if tiers_allowed == 4:
                        if selector < 88:
                            return 4
                        elif selector < 94:
                            return 3
                        elif selector < 98:
                            return 2
                        else:
                            return 1
                    elif tiers_allowed == 3:
                        if selector < 85:
                            return 3
                        elif selector < 96:
                            return 2
                        else:
                            return 1
                    elif tiers_allowed == 2:
                        if selector < 90:
                            return 2
                        else:
                            return 1
                    elif tiers_allowed == 1:
                        return 1
                elif chest_tier == 3:
                    if tiers_allowed == 4:
                        if selector < 85:
                            return 3
                        elif selector < 91:
                            return 2
                        elif selector < 97:
                            return 4
                        else:
                            return 1
                    elif tiers_allowed == 3:
                        if selector < 85:
                            return 3
                        elif selector < 96:
                            return 2
                        else:
                            return 1
                    elif tiers_allowed == 2:
                        if selector < 90:
                            return 2
                        else:
                            return 1
                    elif tiers_allowed == 1:
                        return 1
                elif chest_tier == 2:
                    if tiers_allowed == 4:
                        if selector < 85:
                            return 2
                        elif selector < 91:
                            return 3
                        elif selector < 97:
                            return 1
                        else:
                            return 4
                    elif tiers_allowed == 3:
                        if selector < 85:
                            return 2
                        elif selector < 96:
                            return 3
                        else:
                            return 1
                    elif tiers_allowed == 2:
                        if selector < 90:
                            return 1
                        else:
                            return 2
                    elif tiers_allowed == 1:
                        return 1
                elif chest_tier == 1:
                    if tiers_allowed == 4:
                        if selector < 85:
                            return 1
                        elif selector < 93:
                            return 2
                        elif selector < 98:
                            return 3
                        else:
                            return 4
                    elif tiers_allowed == 3:
                        if selector < 85:
                            return 1
                        elif selector < 96:
                            return 2
                        else:
                            return 3
                    elif tiers_allowed == 2:
                        if selector < 90:
                            return 1
                        else:
                            return 2
                    elif tiers_allowed == 1:
                        return 1

            excluded_items = [129, 137, 138]
            # Always exclude special equips from shops if Mx is set
            if world.settings.is_flag_enabled(flags.MonstroTownLite):
                monstro = [items.QuartzCharm, items.JinxBelt, items.SuperSuit, items.AttackScarf, items.GhostMedal]
                monstro_locations = [i for i in world.chest_locations if
                                     isinstance(i, (chests.CulexReward, chests.JinxDojoReward, chests.SuperJumps30,
                                                    chests.SuperJumps100, chests.ThreeMustyFears)) and
                                     i not in finished_chests]
            elif world.settings.is_flag_enabled(flags.MonstroTownHard):
                monstro = [items.QuartzCharm, items.JinxBelt, items.SuperSuit, items.AttackScarf, items.GhostMedal,
                           items.FroggieStick, items.Chomp, items.ZoomShoes, items.LazyShellWeapon,
                           items.LazyShellArmor]
                monstro_locations = [i for i in world.chest_locations if
                                     isinstance(i, (chests.CulexReward, chests.JinxDojoReward, chests.SuperJumps30,
                                                    chests.SuperJumps100, chests.ThreeMustyFears,
                                                    chests.CricketPieReward, chests.BoosterTowerChomp,
                                                    chests.BoosterTowerZoomShoes, chests.GardenerCloud1,
                                                    chests.GardenerCloud2)) and
                                     i not in finished_chests]
            else:
                monstro = []
                monstro_locations = []

            chance = random.randint(1, 10)
            # 30% chance that 100 super jump will have the best of the 10 items
            if chance <= 3 and len(monstro) > 0:
                monstro.sort(key=lambda x: x.rank_value, reverse=True)
                item = monstro[1]
                location = [i for i in monstro_locations if isinstance(i, chests.SuperJumps100)][0]
                location.item = item
                monstro.remove(item)
                monstro_locations.remove(location)
                finished_chests.append(location)
                if world.settings.is_flag_enabled(flags.MonstroExcludeElsewhere):
                    excluded_items.append(item.index)
                items_already_in_chests.append(item)

            while len(monstro) > 0:
                item = random.choice(monstro)
                location = random.choice(monstro_locations)
                location.item = item
                monstro.remove(item)
                monstro_locations.remove(location)
                finished_chests.append(location)
                if world.settings.is_flag_enabled(flags.MonstroExcludeElsewhere):
                    excluded_items.append(item.index)
                items_already_in_chests.append(item)

            # Then do key items....
            leftover_key_locations = []
            if include_key_items:
                key_item_locations = [l for l in world.key_locations if keys.item_location_filter(world, l)]

                # Get items to place only from vanilla key item locations, not including other chests/rewards.
                required_items = keys.Inventory([l.item for l in key_item_locations if
                                                l.item.shuffle_type == items.ItemShuffleType.Required])
                extra_items = keys.Inventory([l.item for l in key_item_locations if
                                             l.item.shuffle_type == items.ItemShuffleType.Extra])

                # Now add all the chest/reward spots to the location list if they haven't been done yet.
                # This excludes the Monstro Town locations if the M flag is on above.
                if not world.settings.is_flag_enabled(flags.ChestExcludeRewards):
                    chest_locations = [l for l in world.chest_locations if l not in finished_chests and
                                       keys.item_location_filter(world, l)]
                else:
                    chest_locations = [l for l in world.chest_locations if l not in finished_chests and
                                       keys.item_location_filter(world, l) and not isinstance(l, chests.Reward)]

                eligible_key_locations = key_item_locations + chest_locations

                # Do the fill, and mark any selected chests as done.
                keys.fill_locations(world, eligible_key_locations, required_items, extra_items, ap_data)
                for location in eligible_key_locations:
                    if location.has_item:
                        finished_chests.append(location)
                    else:
                        leftover_key_locations.append(location)

            # Chest/reward list plus leftover key item locations from mixing shuffle.
            # Use this for all logic past this point!
            chests_plus_leftovers = world.chest_locations + leftover_key_locations

            # Then make sure wallet is found in exactly 1 chest
            if not world.settings.is_flag_enabled(flags.ChestExcludeRewards):
                eligible_wallet_locations = [chest for chest in chests_plus_leftovers if chest not in finished_chests]
                chest = random.choice(eligible_wallet_locations)
                chest.item = items.Wallet
                finished_chests.append(chest)

            # Then make sure "You Missed" is found in exactly 1 chest
            eligible_empty_locations = [chest for chest in chests_plus_leftovers if chest not in finished_chests and
                                        not isinstance(chest, chests.Reward) and chest.item_allowed(items.YouMissed)]
            chest = random.choice(eligible_empty_locations)
            chest.item = items.YouMissed
            finished_chests.append(chest)

            # Then do the rest
            eligible_chests = [chest for chest in chests_plus_leftovers if
                               not isinstance(chest, (chests.Reward, chests.BowserDoorReward, KeyItemLocation)) and
                               chest not in finished_chests]
            eligible_rewards = [chest for chest in chests_plus_leftovers if
                                isinstance(chest, (chests.Reward, chests.BowserDoorReward, KeyItemLocation)) and
                                chest not in finished_chests]
            eligible_items = [i for i in world.items if i.index not in excluded_items and not i.is_key and
                              i.hard_tier <= tiers_allowed]

            while len(eligible_chests) > 0:
                chest = random.choice(eligible_chests)
                items_for_chest = [i for i in eligible_items if chest.item_allowed(i)]

                if biased:
                    selected_tier = get_eligible_tier(chest.access)
                    adjusted_denominator = ratio_items
                    if coins_allowed and chest.item_allowed(items.Coins150):
                        adjusted_ratio_coins = ratio_coins
                    else:
                        adjusted_ratio_coins = 0

                    if flowers_allowed and chest.item_allowed(items.Flower):
                        adjusted_ratio_flowers = math.floor(ratio_flowers / 1.5 / selected_tier)
                    else:
                        adjusted_ratio_flowers = 0

                    if mushrooms_allowed and chest.item_allowed(items.RecoveryMushroom):
                        adjusted_ratio_mushrooms = math.floor(ratio_mushrooms / 1.5 / selected_tier)
                    else:
                        adjusted_ratio_mushrooms = 0

                    if frogcoins_allowed and chest.item_allowed(items.FrogCoin):
                        adjusted_ratio_frogcoins = math.floor(ratio_frogcoins / 1.5 / selected_tier)
                    else:
                        adjusted_ratio_frogcoins = 0

                    adjusted_denominator += (adjusted_ratio_coins + adjusted_ratio_flowers + adjusted_ratio_mushrooms +
                                             adjusted_ratio_frogcoins)
                    selection = random.randint(1, adjusted_denominator)
                    if flowers_allowed and chest.item_allowed(items.Flower) and selection < adjusted_ratio_flowers:
                        chest.item = items.Flower
                    elif (mushrooms_allowed and chest.item_allowed(items.RecoveryMushroom) and
                          selection < adjusted_ratio_flowers + adjusted_ratio_mushrooms):
                        chest.item = items.RecoveryMushroom
                    elif (frogcoins_allowed and chest.item_allowed(items.FrogCoin) and
                          selection < adjusted_ratio_flowers + adjusted_ratio_mushrooms + adjusted_ratio_frogcoins):
                        chest.item = items.FrogCoin
                    elif (coins_allowed and selected_tier <= 2 and chest.item_allowed(items.Coins150) and
                          selection < adjusted_ratio_flowers + adjusted_ratio_mushrooms + adjusted_ratio_frogcoins +
                          adjusted_ratio_coins):
                        chest.item = random.choice([i for i in coins if i.hard_tier == selected_tier])
                    else:
                        # 50% chance of rerolling if item is an equip
                        proceed_repeat_item = False
                        while not proceed_repeat_item:
                            # If no possible items are allowed in this chest, make it coins instead.
                            possible_items = [i for i in items_for_chest if i.hard_tier == selected_tier]
                            if not possible_items:
                                possible_items = [i for i in leftovers if chest.item_allowed(i)]
                            check_item = random.choice(possible_items)
                            if check_item.is_equipment:
                                fifty = random.choice([0, 1])
                                if fifty == 0:
                                    chest.item = check_item
                                    proceed_repeat_item = True
                            else:
                                chest.item = check_item
                                proceed_repeat_item = True
                else:
                    selection = random.randint(1, denominator)
                    if flowers_allowed and chest.item_allowed(items.Flower) and selection < ratio_flowers / 1.5:
                        chest.item = items.Flower
                    elif (mushrooms_allowed and chest.item_allowed(items.RecoveryMushroom) and
                          selection < ratio_flowers / 1.5 + ratio_mushrooms / 1.5):
                        chest.item = items.RecoveryMushroom
                    elif (frogcoins_allowed and chest.item_allowed(items.FrogCoin) and
                          selection < ratio_flowers / 1.5 + ratio_mushrooms / 1.5 + ratio_frogcoins / 1.5):
                        chest.item = items.FrogCoin
                    elif (coins_allowed and chest.item_allowed(items.Coins150) and
                          selection < ratio_flowers / 1.5 + ratio_mushrooms / 1.5 + ratio_frogcoins / 1.5 +
                          ratio_coins):
                        chest.item = random.choice(coins)
                    else:
                        tier_selection = random.randint(1, 100)
                        proceed_repeat_item = False
                        while not proceed_repeat_item:
                            if tiers_allowed == 4:
                                if tier_selection <= 40:
                                    possible_items = [i for i in items_for_chest if i.hard_tier == 1]
                                elif tier_selection <= 70:
                                    possible_items = [i for i in items_for_chest if i.hard_tier == 2]
                                elif tier_selection <= 90:
                                    possible_items = [i for i in items_for_chest if i.hard_tier == 3]
                                else:
                                    possible_items = [i for i in items_for_chest if i.hard_tier == 4]
                            elif tiers_allowed == 3:
                                if tier_selection <= 40:
                                    possible_items = [i for i in items_for_chest if i.hard_tier == 1]
                                elif tier_selection <= 75:
                                    possible_items = [i for i in items_for_chest if i.hard_tier == 2]
                                else:
                                    possible_items = [i for i in items_for_chest if i.hard_tier == 3]
                            elif tiers_allowed == 2:
                                if tier_selection <= 50:
                                    possible_items = [i for i in items_for_chest if i.hard_tier == 1]
                                else:
                                    possible_items = [i for i in items_for_chest if i.hard_tier == 2]
                            else:
                                possible_items = [i for i in items_for_chest if i.hard_tier == 1]

                            # If no possible items are allowed in this chest, make it coins instead.
                            if not possible_items:
                                possible_items = [i for i in leftovers if chest.item_allowed(i)]
                            check_item = random.choice(possible_items)

                            # 50% chance of rerolling if item is an equip
                            if check_item.is_equipment:
                                fifty = random.choice([0, 1])
                                if fifty == 0:
                                    chest.item = check_item
                                    proceed_repeat_item = True
                            else:
                                chest.item = check_item
                                proceed_repeat_item = True

                finished_chests.append(chest)
                eligible_chests.remove(chest)

            # If we excluded rewards, remove any reward spots that still have items.  Keep those that are empty because
            # they are left over key item locations from the shuffle above and do need items placed there!
            if world.settings.is_flag_enabled(flags.ChestExcludeRewards):
                eligible_rewards = [r for r in eligible_rewards if not r.has_item]

            if eligible_rewards:
                while len(eligible_rewards) > 0:
                    chest = random.choice(eligible_rewards)
                    items_for_chest = [i for i in eligible_items if chest.item_allowed(i)]

                    # For Cricket Jam reward, always give frog coins for now!  Just randomize the number.
                    if isinstance(chest, chests.CricketJamReward):
                        chest.item = items.FrogCoin
                        chest.num_frog_coins = random.randint(5, random.randint(10, 20))
                    else:
                        proceed_repeat_item = False
                        while not proceed_repeat_item:
                            if biased:
                                selected_tier = get_eligible_tier(chest.access)
                                possible_items = [i for i in items_for_chest if i.hard_tier == selected_tier]
                            else:
                                tier_selection = random.randint(1, 100)
                                if tiers_allowed == 4:
                                    if tier_selection <= 35:
                                        possible_items = [i for i in items_for_chest if i.hard_tier == 3]
                                    elif tier_selection <= 60:
                                        possible_items = [i for i in items_for_chest if i.hard_tier == 2]
                                    elif tier_selection <= 85:
                                        possible_items = [i for i in items_for_chest if i.hard_tier == 4]
                                    else:
                                        possible_items = [i for i in items_for_chest if i.hard_tier == 1]
                                elif tiers_allowed == 3:
                                    if tier_selection <= 30:
                                        possible_items = [i for i in items_for_chest if i.hard_tier == 1]
                                    elif tier_selection <= 60:
                                        possible_items = [i for i in items_for_chest if i.hard_tier == 2]
                                    else:
                                        possible_items = [i for i in items_for_chest if i.hard_tier == 3]
                                elif tiers_allowed == 2:
                                    if tier_selection <= 50:
                                        possible_items = [i for i in items_for_chest if i.hard_tier == 1]
                                    else:
                                        possible_items = [i for i in items_for_chest if i.hard_tier == 2]
                                else:
                                    possible_items = [i for i in items_for_chest if i.hard_tier == 1]

                            # If no possible items are allowed in this chest, make it coins instead.
                            if not possible_items:
                                possible_items = [i for i in leftovers if chest.item_allowed(i)]
                            check_item = random.choice(possible_items)

                            if check_item not in items_already_in_chests or not check_item.is_equipment:
                                items_already_in_chests.append(check_item)
                                chest.item = check_item
                                proceed_repeat_item = True
                            else:
                                fifty = random.choice([0, 1])
                                if fifty == 0:
                                    chest.item = check_item
                                    proceed_repeat_item = True

                    finished_chests.append(chest)
                    eligible_rewards.remove(chest)



        # Replace any sellable items with closest coin equivalent.
        if world.settings.is_flag_enabled(flags.ReplaceItems):

            def closest_coins(n):
                num = n / 2
                diff = abs(num - 5)
                rv = items.Coins5
                if diff > abs(num - 8):
                    diff = abs(num - 8)
                    rv = items.Coins8
                if diff > abs(num - 10):
                    diff = abs(num - 10)
                    rv = items.Coins10
                if diff > abs(num - 20):
                    diff = abs(num - 20)
                    rv = items.CoinsDoubleBig
                if diff > abs(num - 50):
                    diff = abs(num - 50)
                    rv = items.Coins50
                if diff > abs(num - 100):
                    diff = abs(num - 100)
                    rv = items.Coins100
                if diff > abs(num - 150):
                    rv = items.Coins150
                return rv

            for chest in [i for i in world.chest_locations if not isinstance(i, chests.Reward)]:
                if chest.item.hard_tier == 1 and not chest.item.is_key and chest.item.price > 0:
                    if chest.item_allowed(items.Coins150) and not chest.item.frog_coin_item:
                        chest.item = closest_coins(chest.item.price)
                    elif chest.item_allowed(items.FrogCoin) and chest.item.frog_coin_item:
                        chest.item = items.FrogCoin
