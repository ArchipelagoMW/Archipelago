# Item/shop randomization logic

import random
import math

from inspect import isclass

from ...randomizer.data import items
from ...randomizer.data.characters import Mario, Mallow, Geno, Bowser, Peach
from . import flags, utils


def _randomize_item(item):
    """Perform randomization for an item.  Non-equipment will not be shuffled (price is done in the shop logic).

    Args:
        item(randomizer.data.items.Item):
    """
    if not item.is_equipment:
        return

    if item.world.settings.is_flag_enabled(flags.EquipmentStats):
        # Randomize number of attributes to go up or down. Guarantee >= 1 attribute goes up, but none go down.
        # For each set, 1/3 chance all non-zero ones go up/down.  Otherwise, weighted random number of stats.
        # ...attributes going up
        ups = []
        if random.randint(1, 3) == 1:
            ups = [attr for attr in item.EQUIP_STATS if getattr(item, attr) > 0]

        if not ups:
            num_up = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 10, 5, 1])[0]
            while True:
                ups = random.sample(item.EQUIP_STATS, num_up)
                if set(ups) & set(item.primary_stats):
                    break

        # ...attributes going down
        if random.randint(1, 3) == 1:
            downs = [attr for attr in item.EQUIP_STATS if getattr(item, attr) >= 128]
        else:
            num_down = random.choices([0, 1, 2, 3, 4, 5], weights=[1, 5, 10, 10, 5, 1])[0]
            downs = random.sample(item.EQUIP_STATS, num_down)

        # Give priority to going up if a stat was picked to go up.
        downs = [d for d in downs if d not in ups]

        # Track increases and decreases for each stat.
        score = item.stat_point_value
        if item.effect_type == "extra stats":
            score = max((score + 15), round(score * 1.5))
        up_vals = dict([(u, 0) for u in ups])
        down_vals = dict([(d, 0) for d in downs])

        # For attributes going down, randomize a number of points to decrease based on the total item score.
        # Distribution is weighted towards the lower half of the range.
        if downs:
            if score != 0:
                down_points = random.randint(0, random.randint(0, score))
            else:
                down_points = random.randint(0, random.randint(0, random.randint(0, 100)))

            # Spread number of "down points" randomly across stats being decreased.  Add this number of points to
            # the "score" of the item so we add stat increases to compensate.
            score += down_points
            for _ in range(down_points):
                attr = random.choice(downs)
                down_vals[attr] += 1

        # Spread number of "up points" randomly across stats being increased.  Treat non-primary stat increase as
        # two points to match the item score calculation.
        while score > 0:
            attr = random.choice(ups)
            up_vals[attr] += 1
            if attr in item.primary_stats:
                score -= 1
            else:
                score -= 2

        # Zero all stats.
        for attr in item.EQUIP_STATS:
            setattr(item, attr, 0)

        # Perform standard mutation on new non-zero stats.
        for attr in up_vals:
            setattr(item, attr, utils.mutate_normal(up_vals[attr], minimum=1, maximum=127))

        for attr in down_vals:
            value = utils.mutate_normal(down_vals[attr], minimum=1, maximum=127)
            setattr(item, attr, -value)

        # If this is a weapon with a variance value, shuffle that too.
        if item.variance:
            item.variance = utils.mutate_normal(item.variance, minimum=1, maximum=127)

    if item.world.settings.is_flag_enabled(flags.EquipmentCharacters):
        # Randomize which characters can equip this item.
        # Old linear mode logic: Geno can only equip his own weapons, and nobody else can equip his due to softlocks!
        # This is fixed in open mode.
        if item.world.open_mode or (not item.is_weapon or Geno not in item.equip_chars):
            # Pick random number of characters with lower numbers weighted heavier.
            new_chars = set()
            num_equippable = random.randint(1, random.randint(1, 5))

            for _ in range(num_equippable):
                char_choices = {Mario, Mallow, Geno, Bowser, Peach} - new_chars

                # Linear mode: Geno can only equip his own weapons (we checked if this was one of his above).
                if not item.world.open_mode and item.is_weapon and Geno in char_choices:
                    char_choices.remove(Geno)

                if not char_choices:
                    break

                # Now choose a random character to be equipable.
                char_choices = sorted(char_choices, key=lambda c: c.index)
                new_chars.add(random.choice(char_choices))

            item.equip_chars = list(new_chars)

    # Shuffle special properties.
    if item.world.settings.is_flag_enabled(flags.EquipmentBuffs):
        if item.tier == 1:
            odds = 2 / 3
        elif item.tier == 2:
            odds = 1 / 2
        elif item.tier == 3:
            odds = 1 / 4
        elif item.tier == 4:
            odds = 1 / 8
        elif item.tier == 5:
            odds = 3 / 32
        else:
            odds = 0

        # 7.1.3 update: trying lower odds for special properties and buffs, they're too frequent...
        odds /= 2

        if odds > 0:
            # Instant KO protection.
            KO_odds_factor = 1
            if item.is_weapon:
                KO_odds_factor /= 2
            if item.effect_type in ["extra stats", "few effects"]:
                KO_odds_factor /= 3
            if item.effect_type in ["buffs", "elemental immunity"]:
                KO_odds_factor *= 1.5
            item.prevent_ko = utils.coin_flip(odds * KO_odds_factor)

            # Elemental immunities.
            item.elemental_immunities = []
            item.elemental_resistances = []
            if item.effect_type in ["normal", "buffs", "status protection"]:
                elemental_multiplier = 0.5
                if item.effect_type == "normal":
                    elemental_multiplier = 1
                if random.randint(1, 2) == 1:
                    for i in range(4, 7):
                        if utils.coin_flip(odds * elemental_multiplier):
                            item.elemental_immunities.append(i)
                        elif utils.coin_flip(odds * elemental_multiplier):
                            item.elemental_resistances.append(i)
                else:
                    for i in range(4, 7):
                        if utils.coin_flip(odds * elemental_multiplier):
                            item.elemental_resistances.append(i)
                        elif utils.coin_flip(odds * elemental_multiplier):
                            item.elemental_immunities.append(i)
            elif item.effect_type in ["extra stats", "few effects", "elemental resistance"]:
                elemental_multiplier1 = 0.5
                elemental_multiplier2 = 0.5
                if item.effect_type == "elemental resistance":
                    elemental_multiplier1 = 2.5
                    elemental_multiplier2 = 1
                for i in range(4, 7):
                    if utils.coin_flip(odds * elemental_multiplier1):
                        item.elemental_resistances.append(i)
                    elif utils.coin_flip(odds * elemental_multiplier2):
                        item.elemental_immunities.append(i)
            else:
                for i in range(4, 7):
                    if utils.coin_flip(odds * 2):
                        item.elemental_immunities.append(i)
                    elif utils.coin_flip(odds * 2):
                        item.elemental_resistances.append(i)

            # For certain namesake items, keep their status immunities so people don't get confused for safety.
            guaranteed_immunities = []
            if (isinstance(item, (items.FearlessPin, items.AntidotePin, items.TrueformPin, items.WakeUpPin)) and
                    not item.world.settings.is_flag_enabled(flags.EquipmentNoSafetyChecks)):
                guaranteed_immunities = item.status_immunities

            # Status immunities.
            item.status_immunities = []
            status_multiplier = 1
            if item.effect_type == "status protection":
                status_multiplier = 2
            elif item.effect_type in ["buffs", "extra stats", "few effects"]:
                status_multiplier = 0.5
            for i in range(0, 7):
                # Skip berserk status if the safety checks on enemy shuffle is not enabled.
                if i == 4 and not item.world.settings.is_flag_enabled(flags.EnemyNoSafetyChecks):
                    continue

                if utils.coin_flip(odds * status_multiplier):
                    item.status_immunities.append(i)

            # Add guaranteed immunities back.
            for i in guaranteed_immunities:
                if i not in item.status_immunities:
                    item.status_immunities.append(i)

            # Weight weapons more toward buffs than armors. Accessories weight based on their stat totals.
            buff_odds = 1
            if item.is_weapon or item.index in [74, 77, 92]:
                buff_odds = 1 / 2
            elif item.is_armor or item.index in [78, 81, 82, 90, 91]:
                buff_odds = 1 / 5
            if item.effect_type == "buffs":
                buff_odds *= 2.5
            elif item.effect_type == "normal":
                pass
            else:
                buff_odds *= 0.25

            # Status buffs.
            item.status_buffs = []
            for i in range(3, 7):
                if utils.coin_flip(odds * buff_odds):
                    item.status_buffs.append(i)


def randomize_all(world, ap_data):
    """Randomize everything for items for a single seed.

    :type world: randomizer.logic.main.GameWorld
    """
    weapon_stats = []
    weapon_tiers = []
    armor_tiers = []
    mega_armor = []
    happy_armor = []
    sailor_armor = []
    fuzzy_armor = []
    fire_armor = []
    endgame_armor = []
    pins_costs = []
    mid_accessory_costs = []
    high_accessory_costs = []

    # Base Shuffle for equipment to set up for further shuffling
    for item in world.items:
        if not item.is_equipment or not item.world.settings.is_flag_enabled(flags.EquipmentStats):
            continue
        if random.randint(1, 10) == 1:
            item.effect_type = random.choice(["normal", "buffs", "status protection", "elemental resistance", "elemental immunity", "extra stats", "few effects"])
        if item.is_weapon:
            temp_weapon_stat = (item.attack, item.price)
            weapon_stats.append(temp_weapon_stat)
            weapon_tiers.append(item.tier)
        elif item.is_armor:
            armor_tiers.append(item.tier)
            if item.index in [41, 42, 44]:
                temp_armor_stat = (item.defense, item.magic_defense)
                mega_armor.append(temp_armor_stat)
            elif item.index in [45, 46, 47, 48, 49]:
                temp_armor_stat = (item.defense, item.magic_defense)
                happy_armor.append(temp_armor_stat)
            elif item.index in [50, 51, 52, 53, 54]:
                temp_armor_stat = (item.defense, item.magic_defense)
                sailor_armor.append(temp_armor_stat)
            elif item.index in [55, 56, 57, 58]:
                temp_armor_stat = (item.defense, item.magic_defense)
                fuzzy_armor.append(temp_armor_stat)
            elif item.index in [59, 60, 61, 62, 63]:
                temp_armor_stat = (item.defense, item.magic_defense)
                fire_armor.append(temp_armor_stat)
            elif item.index in [64, 65, 66, 67, 68]:
                temp_armor_stat = (item.defense, item.magic_defense)
                endgame_armor.append(temp_armor_stat)
        elif item.index in [84, 85, 86, 87]:
            pins_costs.append(item.price)
        # Zoom Shoes, Safety Badge, Jump Shoes, Amulet, Rare Scarf, B'Tub Ring, Feather, Signal Ring
        elif item.index in [74, 75, 76, 78, 82, 83, 91, 93]:
            mid_accessory_costs.append(item.price)
        # Safety Ring, Attack Scarf, Ghost Medal, Jinx Belt, Troopa Pin
        elif item.index in [77, 81, 89, 90, 92]:
             high_accessory_costs.append(item.price)
        # Scrooge Ring, EXP Booster, Coin Trick
        elif item.index in [79, 80, 88]:
             high_accessory_costs.append(round(item.price * 62.5))

    random.shuffle(weapon_stats)
    random.shuffle(weapon_tiers)
    random.shuffle(armor_tiers)
    random.shuffle(mega_armor)
    random.shuffle(happy_armor)
    random.shuffle(sailor_armor)
    random.shuffle(fuzzy_armor)
    random.shuffle(fire_armor)
    random.shuffle(endgame_armor)
    random.shuffle(pins_costs)
    random.shuffle(mid_accessory_costs)
    random.shuffle(high_accessory_costs)
    mega_count = 0
    happy_count = 0
    sailor_count = 0
    fuzzy_count = 0
    fire_count = 0
    endgame_count = 0

    for item in world.items:
        if not item.is_equipment or not item.world.settings.is_flag_enabled(flags.EquipmentStats):
            continue
        if item.is_weapon:
            temp_weapon_stats = weapon_stats[(item.index - 5)]
            item.attack = temp_weapon_stats[0]
            item.price = temp_weapon_stats[1]
            item.tier = weapon_tiers.pop()
        elif item.is_armor:
            item.tier = armor_tiers.pop()
            if item.index in [41, 42, 44]:
                temp_armor_stat = mega_armor[mega_count]
                item.defense = temp_armor_stat[0]
                item.magic_defense = temp_armor_stat[1]
                mega_count += 1
            elif item.index in [45, 46, 47, 48, 49]:
                temp_armor_stat = happy_armor[happy_count]
                item.defense = temp_armor_stat[0]
                item.magic_defense = temp_armor_stat[1]
                happy_count += 1
            elif item.index in [50, 51, 52, 53, 54]:
                temp_armor_stat = sailor_armor[sailor_count]
                item.defense = temp_armor_stat[0]
                item.magic_defense = temp_armor_stat[1]
                sailor_count += 1
            elif item.index in [55, 56, 57, 58]:
                temp_armor_stat = fuzzy_armor[fuzzy_count]
                item.defense = temp_armor_stat[0]
                item.magic_defense = temp_armor_stat[1]
                fuzzy_count += 1
            elif item.index in [59, 60, 61, 62, 63]:
                temp_armor_stat = fire_armor[fire_count]
                item.defense = temp_armor_stat[0]
                item.magic_defense = temp_armor_stat[1]
                fire_count += 1
            elif item.index in [64, 65, 66, 67, 68]:
                temp_armor_stat = endgame_armor[endgame_count]
                item.defense = temp_armor_stat[0]
                item.magic_defense = temp_armor_stat[1]
                endgame_count += 1
        elif item.index in [84, 85, 86, 87]:
            item.price = pins_costs.pop()
        # Zoom Shoes, Safety Badge, Jump Shoes, Amulet, Rare Scarf, B'Tub Ring, Feather, Signal Ring
        elif item.index in [74, 75, 76, 78, 82, 83, 91, 93]:
            item.price = mid_accessory_costs.pop()
        # Safety Ring, Attack Scarf, Ghost Medal, Jinx Belt, Troopa Pin
        elif item.index in [77, 81, 89, 90, 92]:
             item.price = high_accessory_costs.pop()
        # Scrooge Ring, EXP Booster, Coin Trick
        elif item.index in [79, 80, 88]:
             item.price = round(high_accessory_costs.pop() / 62.5)

    # Designate 1-4 magic weapons
    if world.settings.is_flag_enabled(flags.EquipmentStats):
        magic_weapon_count = random.randint(1, 4)
        magic_weapon_candidates = []
        for item in world.items:
            if item.is_weapon and item.attack < 40:
                magic_weapon_candidates.append(item)
        for item in random.sample(magic_weapon_candidates, magic_weapon_count):
            item.magic_weapon = True

    # Shuffle equipment stats and equip characters.
    for item in world.items:
        _randomize_item(item)

    # Safety check that at least four tier equips have instant death protection for safety.
    if (world.settings.is_flag_enabled(flags.EquipmentBuffs) and
            not world.settings.is_flag_enabled(flags.EquipmentNoSafetyChecks)):
        instant_ko_items = len([item for item in world.items if item.prevent_ko])
        if instant_ko_items < 4:
            top_armor = [item for item in world.items if (item.is_armor or item.is_accessory) and item.tier == 1 and
                         not item.prevent_ko]
            for item in random.sample(top_armor, 4 - instant_ko_items):
                item.prevent_ko = True

    for item in world.items:
        if item.is_equipment:
            if item.index in (83, 148, 93):
                item.arbitrary_value = 1
            elif item.index == 88:
                item.arbitrary_value = 2
            elif item.index in (76, 79):
                item.arbitrary_value = 1
            elif item.index == 80:
                item.arbitrary_value = 10
            item.rank_value = (item.attack * max(0, min(2, (item.attack + item.variance) /
                                                        (1 if (item.attack - item.variance == 0) else
                                                         (item.attack - item.variance)))) +
                               max(0, (item.magic_attack / (2 if item.magic_attack < 0 else 1)) +
                                   (item.magic_defense / (2 if item.magic_defense < 0 else 1)) +
                                   (item.defense / (2 if item.defense < 0 else 1)) +
                                   min(20, item.speed / 2)) +
                               10 * len(item.status_immunities) +
                               15 * len(item.elemental_immunities) +
                               7.5 * len(item.elemental_resistances) +
                               50 * (1 if item.prevent_ko else 0) +
                               30 * len(item.status_buffs) + 10 *
                               item.arbitrary_value)

    # Calculate list position (used as a factor in pricing)
    ranks = [item for item in world.items if item.is_equipment]
    ranks.sort(key=lambda x: x.rank_value, reverse=True)
    ranks_reverse = sorted(ranks, key=lambda x: x.rank_value)

    for item in world.items:
        if item.is_equipment:
            item.rank_order = (ranks.index(item) + 1 if item in ranks else 0)
            item.rank_order_reverse = (ranks_reverse.index(item) + 1 if item in ranks_reverse else 0)
            if item.rank_order <= 15:
                item.hard_tier = 4
            elif item.rank_order <= 35:
                item.hard_tier = 3
            elif item.rank_order <= 55:
                item.hard_tier = 2
            else:
                item.hard_tier = 1

    # Useful debug function to print equipment property table.
    """
    for item in world.items:
        if item.is_equipment:
            print(item.name + " " * (19 - len(item.name)) + ": Sp:" + str(item.speed) + ", At:" + str(item.attack) + ", Df:" + str(item.defense) + ", MA:" + str(item.magic_attack) + ", MD:" + str(item.magic_defense) + "; "
                  + ("KO" if item.prevent_ko else "") + (", " if (item.prevent_ko and item.status_immunities != []) else "") + ("Psn" if (2 in item.status_immunities) else "") + ("Mute" if (0 in item.status_immunities) else "")
                  + ("Slp" if (1 in item.status_immunities) else "")  + ("SCrow" if (6 in item.status_immunities) else "") + ("Mush" if (5 in item.status_immunities) else "") + ("Fear" if (3 in item.status_immunities) else "")
                  + ("Bsrk" if (4 in item.status_immunities) else "") + ("; " if (item.prevent_ko or item.status_immunities != []) else "") + ("Imm: " if item.elemental_immunities != [] else "")
                  + ("Ic" if (4 in item.elemental_immunities) else "") + ("Fi" if (5 in item.elemental_immunities) else "") + ("Th" if (6 in item.elemental_immunities) else "") + ("Ju" if (7 in item.elemental_immunities) else "")
                  + ("; " if item.elemental_immunities != [] else "") + ("Res: " if item.elemental_resistances != [] else "") + ("Ic" if (4 in item.elemental_resistances) else "") + ("Fi" if (5 in item.elemental_resistances) else "")
                  + ("Th" if (6 in item.elemental_resistances) else "") + ("Ju" if (7 in item.elemental_resistances) else "")+ ("; " if item.elemental_resistances != [] else "") + ("Buffs: " if item.status_buffs != [] else "")
                  + ("At" if (3 in item.status_buffs) else "") + ("Df" if (4 in item.status_buffs) else "") + ("MA" if (5 in item.status_buffs) else "") + ("MD" if (6 in item.status_buffs) else ""))
    """

    # Shuffle shop contents and prices.
    free_shops = world.settings.is_flag_enabled(flags.FreeShops)

    if world.settings.is_flag_enabled(flags.ShopShuffle):
        assignments = {}

        # ************************ Phase 0: Calculate raw value to use as basis for pricing as well as Sb, Tb assignment

        # Calculate raw rank value

        # Exclude wallet, shiny stone, carbo cookie
        excluded_items = [129, 137, 138]

        # Check for Sx - Goodie Bag only
        if world.settings.is_flag_enabled(flags.ShopTierX):
            for shop in world.shops:
                shop.items = [world.get_item_instance(items.GoodieBag)]
        else:
            tiers_allowed = 4
            if world.settings.is_flag_enabled(flags.ShopTier1):
                tiers_allowed = 1
            elif world.settings.is_flag_enabled(flags.ShopTier2):
                tiers_allowed = 2
            elif world.settings.is_flag_enabled(flags.ShopTier3):
                tiers_allowed = 3

            # Always exclude special equips from shops if Mx is set
            if world.settings.is_flag_enabled(flags.MonstroExcludeElsewhere):
                for item in world.items:
                    if world.settings.is_flag_enabled(flags.MonstroTownLite):
                        if item.index in [69, 81, 89, 94, 90]:
                            item.hard_tier = 5
                    elif world.settings.is_flag_enabled(flags.MonstroTownHard):
                        if item.index in [69, 70, 74, 81, 89, 94, 90, 6, 11, 33]:
                            item.hard_tier = 5

            # Establish an array for each shop's items
            for shop in world.shops:
                assignments[shop.index] = []

            done_already = set()

            # Function determining what can go in a shop, based on flags selected
            def get_valid_items(base, shop, exclude=None):
                if exclude is None:
                    exclude = []
                valid_items = []

                # Sb and Sv - obsolete
                if (world.settings.is_flag_enabled(flags.ShopShuffleBalanced) and
                        world.settings.is_flag_enabled(flags.ShopShuffleVanilla) and
                        not world.settings.is_flag_enabled(flags.ShopTier1)):
                    # Open shops
                    if (shop.index in [0, 1, 2, 4, 5, 7, 17, 20, 21] or
                            (shop.index == 22 and world.settings.is_flag_enabled(flags.BowsersKeepOpen))):
                        valid_items = [i for i in base if i not in done_already and i.vanilla_shop and
                                       i not in exclude and shop.is_item_allowed(i) and
                                       (((tiers_allowed == 1 or tiers_allowed == 2) and i.hard_tier == 1) or
                                        ((tiers_allowed == 3 or tiers_allowed == 4) and i.hard_tier <= 2))]
                        # In case the equip shuffle logic works out so that nothing belongs in a tiered shop,
                        # pick any item of the appropriate class, ignoring tier
                        # if not valid_items:
                        #     valid_items = [i for i in base if i not in done_already and i.vanilla_shop and
                        #                    i not in exclude and shop.is_item_allowed(i)]
                    # Locked shops
                    elif (shop.index in [12, 13, 14, 15, 16, 18, 19, 23, 24] or
                          (shop.index == 22 and not world.settings.is_flag_enabled(flags.BowsersKeepOpen))):
                        valid_items = [i for i in base if i not in done_already and i.vanilla_shop and
                                       shop.is_item_allowed(i) and
                                       ((3 >= tiers_allowed == i.hard_tier) or
                                        (tiers_allowed == 4 and 2 < i.hard_tier <= 4))]
                        # if not valid_items:
                        #     valid_items = [i for i in base if i not in done_already and i.vanilla_shop and
                        #                    i not in exclude and shop.is_item_allowed(i)]
                    # Missable shop
                    elif shop.index == 8:
                        valid_items = [i for i in base if shop.is_item_allowed(i) and i.vanilla_shop and
                                       i not in exclude and i.hard_tier <= tiers_allowed and not i.reuseable]
                # Sv only
                elif world.settings.is_flag_enabled(flags.ShopShuffleVanilla):
                    if shop.index == 8:
                        valid_items = [i for i in base if shop.is_item_allowed(i) and i.vanilla_shop and
                                       i not in exclude and i.hard_tier <= tiers_allowed and not i.reuseable]
                    else:
                        valid_items = [i for i in base if i not in done_already and shop.is_item_allowed(i) and
                                       i.vanilla_shop and i not in exclude and i.hard_tier <= tiers_allowed]

                # Sb only
                elif (world.settings.is_flag_enabled(flags.ShopShuffleBalanced) and
                      not world.settings.is_flag_enabled(flags.ShopTier1)):
                    # Open shops
                    if (shop.index in [0, 1, 2, 4, 5, 7, 17, 20, 21] or
                            (shop.index == 22 and world.settings.is_flag_enabled(flags.BowsersKeepOpen))):
                        valid_items = [i for i in base if i not in done_already and i not in exclude and
                                       shop.is_item_allowed(i) and
                                       (((tiers_allowed == 1 or tiers_allowed == 2) and i.hard_tier == 1) or
                                        ((tiers_allowed == 3 or tiers_allowed == 4) and i.hard_tier <= 2))]
                        # if not valid_items:
                        #     valid_items = [i for i in base if i not in done_already and i not in exclude and
                        #                    i.vanilla_shop and shop.is_item_allowed(i)]
                    # Locked shops
                    elif (shop.index in [12, 13, 14, 15, 16, 18, 19, 23, 24] or
                          (shop.index == 22 and not world.settings.is_flag_enabled(flags.BowsersKeepOpen))):
                        valid_items = [i for i in base if i not in done_already and i not in exclude and
                                       shop.is_item_allowed(i) and
                                       ((3 >= tiers_allowed == i.hard_tier) or
                                        (tiers_allowed == 4 and 2 < i.hard_tier <= 4))]
                        # if not valid_items:
                        #     valid_items = [i for i in base if i not in done_already and i not in exclude and
                        #                    i.vanilla_shop and shop.is_item_allowed(i)]
                    # Missable shop
                    elif shop.index == 8:
                        valid_items = [i for i in base if shop.is_item_allowed(i) and i not in exclude and
                                       i.hard_tier <= tiers_allowed and not i.reuseable]
                # Neither Sb nor Sv
                else:
                    if shop.index == 8:
                        valid_items = [i for i in base if shop.is_item_allowed(i) and i not in exclude and
                                       i.hard_tier <= tiers_allowed and not i.reuseable]
                    else:
                        valid_items = [i for i in base if i not in done_already and i not in exclude and
                                       shop.is_item_allowed(i) and i.hard_tier <= tiers_allowed]
                return valid_items

            # Do juice bar before frog coin shops. Frog coin shops dont leave enough items for juice bar in Sv1.

            # Juice bar gets "first dibs"
            jpshop = None
            for shop1 in world.shops:
                if shop1.index == items.JuiceBarFull.index:
                    jpshop = shop1
            # pick full juice bar
            assignments[12] = []
            possible_jb3 = get_valid_items(world.items, jpshop)
            partial4 = random.sample(possible_jb3, random.randint(4, min(len(possible_jb3), 15)))
            for item in partial4:
                assignments[12].append(item)
            partial3 = random.sample(partial4, random.randint(3, (len(partial4)-1)))
            for item in partial3:
                assignments[11].append(item)
            partial2 = random.sample(partial3, random.randint(2, (len(partial3)-1)))
            for item in partial2:
                assignments[10].append(item)
            partial1 = random.sample(partial2, random.randint(1, (len(partial2)-1)))
            for item in partial1:
                assignments[9].append(item)

            # ******************************* Phase 1: Frog coin shops

            # Sv
            if world.settings.is_flag_enabled(flags.ShopShuffleVanilla):
                # Sv and Sb - only allow the chosen highest tiers of items here - obsolete
                if world.settings.is_flag_enabled(flags.ShopShuffleBalanced):
                    frog_candidates = [i for i in world.items if i.price and i.vanilla_shop and i not in assignments[12] and
                                       ((3 >= tiers_allowed == i.hard_tier) or
                                        (tiers_allowed == 4 and 2 < i.hard_tier <= 4)) and i not in excluded_items]
                # Sv only - allow any item here, as long as permitted by tier exclusion flag
                else:
                    frog_candidates = [i for i in world.items if i.price and i.vanilla_shop and i not in assignments[12] and
                                       i.hard_tier <= tiers_allowed and i not in excluded_items]
            # Sb only
            elif world.settings.is_flag_enabled(flags.ShopShuffleBalanced):
                # Only allow the chosen highest tiers of items here
                frog_candidates = [i for i in world.items if i.price and i not in assignments[12] and
                                   ((3 >= tiers_allowed == i.hard_tier) or
                                    (tiers_allowed == 4 and 2 < i.hard_tier <= 4)) and i not in excluded_items]
            # Allow anything within tier exclusion flag
            else:
                frog_candidates = [i for i in world.items if i.price and i not in assignments[12] and i.hard_tier <= tiers_allowed and i not in excluded_items]
            # Pick 25 items to be in the frog coin shops total.
            frog_chosen = random.sample(frog_candidates, min(len(frog_candidates), 25))
            disciple_shop = 3
            frog_coin_emporium = 6

            # Get list of items where only one is needed for disciple shop:
            # only one character can equip, or it's reuseable.
            one_only = [i for i in frog_chosen if
                        (i.is_equipment and len(i.equip_chars) == 1) or
                        (i.consumable and i.reuseable)]

            # Choose 5-10.
            num_choose = min(10, len(one_only))
            num_choose = random.randint(min(1, num_choose), num_choose)
            chosen = random.sample(one_only, num_choose)

            # If we have less than 10 items chosen, include other equipment in the mix and choose some more.
            choose_again = [i for i in frog_chosen if i not in chosen and (i in one_only or i.is_equipment)]
            num_choose = 10 - len(chosen)
            num_choose = random.randint(0, num_choose)
            num_choose = min(num_choose, len(choose_again))
            if num_choose and choose_again:
                chosen += random.sample(choose_again, num_choose)

            # Put the chosen in the disciple shop and up to 15 remaining in the Emporium
            assignments[items.DiscipleShop.index] = chosen
            num_emporium = random.randint(random.randint(1, 15), 15)
            frog_remaining = [i for i in frog_chosen if i not in chosen]
            num_emporium = min(num_emporium, len(frog_remaining))
            assignments[items.FrogCoinEmporiumShop.index] = random.sample(frog_remaining, num_emporium)

            # ******************************* Phase 2: Non-frog coin shops

            # Collect remaining items that aren't in frog coin shops and aren't key items.

            if world.settings.is_flag_enabled(flags.ShopShuffleVanilla):
                shop_items = [i for i in world.items if
                              i not in assignments[items.DiscipleShop.index] and
                              i not in assignments[items.FrogCoinEmporiumShop.index] and
                              i.price
                              and i.hard_tier <= tiers_allowed
                              and i.index not in excluded_items
                              and i.vanilla_shop]
            else:
                shop_items = [i for i in world.items if
                              i not in assignments[items.DiscipleShop.index] and
                              i not in assignments[items.FrogCoinEmporiumShop.index] and
                              i.price
                              and i.hard_tier <= tiers_allowed
                              and i.index not in excluded_items]

            # First, we want every item to wind up in a shop.
            # But we need a backup reserve of items to pull from in case the logic doesnt work out
            # i.e. Sb is enabled but there are no accessories in the upper tiers
            item_reserve = shop_items

            # Unique items will first be split among the shops (anything except basic healing items)
            unique_items = [i for i in shop_items if not (i.consumable and not i.reuseable and i.basic)]
            basic_items = [i for i in shop_items if (i.consumable and not i.reuseable and i.basic)]

            # Randomly assign anything to Yaridovich shop
            for shop in world.shops:
                if shop.index == 8:
                    valid_items = get_valid_items(item_reserve, shop)
                    yarid_items = random.sample(valid_items, random.randint(1, min(len(valid_items), 15)))
                    for item in yarid_items:
                        assignments[shop.index].append(item)

            if not world.settings.is_flag_enabled(flags.ShopNotGuaranteed):
                # guarantee pick me up in toad shop if not full
                for item in world.items:
                    for shop in world.shops:
                        if item.index == 102 and shop.index == 24:
                            if item not in assignments[24] and item in shop_items:
                                assignments[shop.index].append(item)
                # Assign each item to one shop by default
                for item in item_reserve:
                    if item not in assignments[12]:
                        eligible_shops = [s for s in world.shops if len(assignments[s.index]) < 15 and s.index not in [3, 6, 8, 9, 10, 11, 12] and item in get_valid_items(item_reserve, s, assignments[s.index])]
                        if eligible_shops:
                            shop = random.choice(eligible_shops)
                            if item not in assignments[shop.index]:
                                assignments[shop.index].append(item)


            # Randomly assign anything to shops with space remaining
            done_already.clear()
            for shop in world.shops:
                if shop.index not in [3, 6, 8, 9, 10, 11, 12]:
                    if len(assignments[shop.index]) < 15:
                        valid_items = get_valid_items(unique_items, shop, assignments[shop.index])
                        if valid_items:
                            max_remaining = min(15 - len(assignments[shop.index]), len(valid_items))
                            if max_remaining > 0:
                                if not world.settings.is_flag_enabled(flags.ShopNotGuaranteed):
                                    append_items = random.sample(valid_items, random.randint(1, random.randint(1, random.randint(1, random.randint(1, max_remaining)))))
                                else:
                                    append_items = random.sample(valid_items, random.randint(1, random.randint(1, max_remaining)))
                                for item in append_items:
                                    assignments[shop.index].append(item)

            # Loop through shops to find any that are empty, and just add Pick Me Up
            pmu = world.get_item_instance(items.PickMeUp)
            for shop in world.shops:
                if not (isinstance(shop, items.PartialJuiceBarShop) or
                        shop.index in [disciple_shop, frog_coin_emporium]):
                    if not assignments[shop.index]:
                        assignments[shop.index].append(pmu)

            # ******************************* Phase 3: Repricing

            for shop in world.shops:
                assigned_items = assignments[shop.index]
                for item in assigned_items:

                    # Turn the item into a frog coin price if it's in one of those shops.

                    # #######Set new regular-coin prices for FC items

                    if free_shops:
                        if shop.frog_coin_shop:
                            item.frog_coin_item = True
                            item.price = 1
                        else:
                            item.price = 1
                    else:
                        if item.is_equipment:
                            if shop.frog_coin_shop:
                                item.frog_coin_item = True
                                item.price = min(item.max_price, max(math.ceil(item.rank_value / 5), 1))
                            else:
                                # Change constant to a lower value if items seem generally too expensive, or increase it
                                # if too cheap. Will affect better items more than bad ones
                                price = math.ceil(item.rank_value *
                                                  (2 + (item.rank_order_reverse / len(ranks_reverse))))
                                price = min(item.max_price, max(2, price))
                                price = utils.mutate_normal(price, minimum=price*0.9, maximum=price*1.1)
                                item.price = price
                        else:
                            if shop.frog_coin_shop:
                                item.frog_coin_item = True
                                price = utils.mutate_normal(item.price, minimum=item.price*0.9, maximum=item.price*1.1)
                                item.price = min(item.max_price, max(math.ceil(price / 25), 1))
                            else:
                                # muku cooki price should never change
                                if item.index != 120:
                                    price = min(item.max_price, max(2, item.price))
                                    price = utils.mutate_normal(price, minimum=item.price*0.9, maximum=item.price*1.1)
                                    item.price = price

            # Sort the list of items by the ordering rank for display, and assign to the shop.
            for shop in world.shops:
                shop.items = sorted(assignments[shop.index], key=lambda i: i.order)

    # Check for free shops, and make sure item prices don't go above 9999 or below 1 as a general rule.
    for shop in world.shops:
        for item in shop.items:
            item.price = max(1, min(item.max_price, item.price))
            if free_shops:
                if shop.frog_coin_shop:
                    item.frog_coin_item = True
                item.price = 1

    if world.settings.is_flag_enabled(flags.PoisonMushroom):
        for item in world.items:
            if item.index == 175:
                item.status_immunities = [random.randint(0, 7)]


def get_spoiler(world):
    acc = {}
    for location in world.key_locations + world.chest_locations:
        if location.item.shuffle_type != items.ItemShuffleType.Required:
            continue
        if isinstance(location.item, items.Item):
            item_str = location.item.name
        elif isclass(location.item):
            item_str = location.item.__name__
        else:
            item_str = str(location.item)

        acc[location.name] = item_str

    return acc
