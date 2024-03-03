import math
import re

from BaseClasses import ItemClassification
from worlds.generic.Rules import add_rule, item_name_in_locations, set_rule
from . import Options
from .Items import DLCQuestItem


def create_event(player, event: str) -> DLCQuestItem:
    return DLCQuestItem(event, ItemClassification.progression, None, player)


def has_enough_coin(player: int, coin: int):
    return lambda state: state.prog_items[player][" coins"] >= coin


def has_enough_coin_freemium(player: int, coin: int):
    return lambda state: state.prog_items[player][" coins freemium"] >= coin


def set_rules(world, player, World_Options: Options.DLCQuestOptions):
    set_basic_rules(World_Options, player, world)
    set_lfod_rules(World_Options, player, world)
    set_completion_condition(World_Options, player, world)


def set_basic_rules(World_Options, player, world):
    if World_Options.campaign == Options.Campaign.option_live_freemium_or_die:
        return
    set_basic_entrance_rules(player, world)
    set_basic_self_obtained_items_rules(World_Options, player, world)
    set_basic_shuffled_items_rules(World_Options, player, world)
    set_double_jump_glitchless_rules(World_Options, player, world)
    set_easy_double_jump_glitch_rules(World_Options, player, world)
    self_basic_coinsanity_funded_purchase_rules(World_Options, player, world)
    set_basic_self_funded_purchase_rules(World_Options, player, world)
    self_basic_win_condition(World_Options, player, world)


def set_basic_entrance_rules(player, world):
    set_rule(world.get_entrance("Moving", player),
             lambda state: state.has("Movement Pack", player))
    set_rule(world.get_entrance("Cloud", player),
             lambda state: state.has("Psychological Warfare Pack", player))
    set_rule(world.get_entrance("Forest Entrance", player),
             lambda state: state.has("Map Pack", player))
    set_rule(world.get_entrance("Forest True Double Jump", player),
             lambda state: state.has("Double Jump Pack", player))


def set_basic_self_obtained_items_rules(World_Options, player, world):
    if World_Options.item_shuffle != Options.ItemShuffle.option_disabled:
        return
    set_rule(world.get_entrance("Behind Ogre", player),
             lambda state: state.has("Gun Pack", player))

    if World_Options.time_is_money == Options.TimeIsMoney.option_required:
        set_rule(world.get_entrance("Tree", player),
                 lambda state: state.has("Time is Money Pack", player))
        set_rule(world.get_entrance("Cave Tree", player),
                 lambda state: state.has("Time is Money Pack", player))
        set_rule(world.get_location("Shepherd Sheep", player),
                 lambda state: state.has("Time is Money Pack", player))
        set_rule(world.get_location("North West Ceiling Sheep", player),
                 lambda state: state.has("Time is Money Pack", player))
        set_rule(world.get_location("North West Alcove Sheep", player),
                 lambda state: state.has("Time is Money Pack", player))
        set_rule(world.get_location("West Cave Sheep", player),
                 lambda state: state.has("Time is Money Pack", player))


def set_basic_shuffled_items_rules(World_Options, player, world):
    if World_Options.item_shuffle != Options.ItemShuffle.option_shuffled:
        return
    set_rule(world.get_entrance("Behind Ogre", player),
             lambda state: state.has("Gun", player))
    set_rule(world.get_entrance("Tree", player),
             lambda state: state.has("Sword", player) or state.has("Gun", player))
    set_rule(world.get_entrance("Cave Tree", player),
             lambda state: state.has("Sword", player) or state.has("Gun", player))
    set_rule(world.get_entrance("True Double Jump", player),
             lambda state: state.has("Double Jump Pack", player))
    set_rule(world.get_location("Shepherd Sheep", player),
             lambda state: state.has("Sword", player) or state.has("Gun", player))
    set_rule(world.get_location("North West Ceiling Sheep", player),
             lambda state: state.has("Sword", player) or state.has("Gun", player))
    set_rule(world.get_location("North West Alcove Sheep", player),
             lambda state: state.has("Sword", player) or state.has("Gun", player))
    set_rule(world.get_location("West Cave Sheep", player),
             lambda state: state.has("Sword", player) or state.has("Gun", player))
    set_rule(world.get_location("Gun", player),
             lambda state: state.has("Gun Pack", player))

    if World_Options.time_is_money == Options.TimeIsMoney.option_required:
        set_rule(world.get_location("Sword", player),
                 lambda state: state.has("Time is Money Pack", player))


def set_double_jump_glitchless_rules(World_Options, player, world):
    if World_Options.double_jump_glitch != Options.DoubleJumpGlitch.option_none:
        return
    set_rule(world.get_entrance("Cloud Double Jump", player),
             lambda state: state.has("Double Jump Pack", player))
    set_rule(world.get_entrance("Forest Double Jump", player),
             lambda state: state.has("Double Jump Pack", player))


def set_easy_double_jump_glitch_rules(World_Options, player, world):
    if World_Options.double_jump_glitch == Options.DoubleJumpGlitch.option_all:
        return
    set_rule(world.get_entrance("Behind Tree Double Jump", player),
             lambda state: state.has("Double Jump Pack", player))
    set_rule(world.get_entrance("Cave Roof", player),
             lambda state: state.has("Double Jump Pack", player))


def self_basic_coinsanity_funded_purchase_rules(World_Options, player, world):
    if World_Options.coinsanity != Options.CoinSanity.option_coin:
        return
    number_of_bundle = math.floor(825 / World_Options.coinbundlequantity)
    for i in range(number_of_bundle):

        item_coin = f"DLC Quest: {World_Options.coinbundlequantity * (i + 1)} Coin"
        set_rule(world.get_location(item_coin, player),
                 has_enough_coin(player, World_Options.coinbundlequantity * (i + 1)))
        if 825 % World_Options.coinbundlequantity != 0:
            set_rule(world.get_location("DLC Quest: 825 Coin", player),
                     has_enough_coin(player, 825))

    set_rule(world.get_location("Movement Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(4 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Animation Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(5 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Audio Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(5 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Pause Menu Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(5 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Time is Money Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(20 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Double Jump Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(100 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Pet Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(5 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Sexy Outfits Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(5 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Top Hat Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(5 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Map Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(140 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Gun Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(75 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("The Zombie Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(5 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Night Map Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(75 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Psychological Warfare Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(50 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Armor for your Horse Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(250 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Finish the Fight Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(5 / World_Options.coinbundlequantity)))


def set_basic_self_funded_purchase_rules(World_Options, player, world):
    if World_Options.coinsanity != Options.CoinSanity.option_none:
        return
    set_rule(world.get_location("Movement Pack", player),
             has_enough_coin(player, 4))
    set_rule(world.get_location("Animation Pack", player),
             has_enough_coin(player, 5))
    set_rule(world.get_location("Audio Pack", player),
             has_enough_coin(player, 5))
    set_rule(world.get_location("Pause Menu Pack", player),
             has_enough_coin(player, 5))
    set_rule(world.get_location("Time is Money Pack", player),
             has_enough_coin(player, 20))
    set_rule(world.get_location("Double Jump Pack", player),
             has_enough_coin(player, 100))
    set_rule(world.get_location("Pet Pack", player),
             has_enough_coin(player, 5))
    set_rule(world.get_location("Sexy Outfits Pack", player),
             has_enough_coin(player, 5))
    set_rule(world.get_location("Top Hat Pack", player),
             has_enough_coin(player, 5))
    set_rule(world.get_location("Map Pack", player),
             has_enough_coin(player, 140))
    set_rule(world.get_location("Gun Pack", player),
             has_enough_coin(player, 75))
    set_rule(world.get_location("The Zombie Pack", player),
             has_enough_coin(player, 5))
    set_rule(world.get_location("Night Map Pack", player),
             has_enough_coin(player, 75))
    set_rule(world.get_location("Psychological Warfare Pack", player),
             has_enough_coin(player, 50))
    set_rule(world.get_location("Armor for your Horse Pack", player),
             has_enough_coin(player, 250))
    set_rule(world.get_location("Finish the Fight Pack", player),
             has_enough_coin(player, 5))


def self_basic_win_condition(World_Options, player, world):
    if World_Options.ending_choice == Options.EndingChoice.option_any:
        set_rule(world.get_location("Winning Basic", player),
                 lambda state: state.has("Finish the Fight Pack", player))
    if World_Options.ending_choice == Options.EndingChoice.option_true:
        set_rule(world.get_location("Winning Basic", player),
                 lambda state: state.has("Armor for your Horse Pack", player) and state.has("Finish the Fight Pack",
                                                                                            player))


def set_lfod_rules(World_Options, player, world):
    if World_Options.campaign == Options.Campaign.option_basic:
        return
    set_lfod_entrance_rules(player, world)
    set_boss_door_requirements_rules(player, world)
    set_lfod_self_obtained_items_rules(World_Options, player, world)
    set_lfod_shuffled_items_rules(World_Options, player, world)
    self_lfod_coinsanity_funded_purchase_rules(World_Options, player, world)
    set_lfod_self_funded_purchase_rules(World_Options, has_enough_coin_freemium, player, world)


def set_lfod_entrance_rules(player, world):
    set_rule(world.get_entrance("Wall Jump Entrance", player),
             lambda state: state.has("Wall Jump Pack", player))
    set_rule(world.get_entrance("Harmless Plants", player),
             lambda state: state.has("Harmless Plants Pack", player))
    set_rule(world.get_entrance("Name Change Entrance", player),
             lambda state: state.has("Name Change Pack", player))
    set_rule(world.get_entrance("Cut Content Entrance", player),
             lambda state: state.has("Cut Content Pack", player))
    set_rule(world.get_entrance("Blizzard", player),
             lambda state: state.has("Season Pass", player))
    set_rule(world.get_location("I Get That Reference!", player),
             lambda state: state.has("Death of Comedy Pack", player))
    set_rule(world.get_location("Story is Important", player),
             lambda state: state.has("DLC NPC Pack", player))
    set_rule(world.get_entrance("Pickaxe Hard Cave", player),
             lambda state: state.has("Pickaxe", player))


def set_boss_door_requirements_rules(player, world):
    sword_1 = "Big Sword Pack"
    sword_2 = "Really Big Sword Pack"
    sword_3 = "Unfathomable Sword Pack"

    big_sword_location = world.get_location(sword_1, player)
    really_big_sword_location = world.get_location(sword_2, player)
    unfathomable_sword_location = world.get_location(sword_3, player)

    big_sword_valid_locations = [big_sword_location]
    really_big_sword_valid_locations = [big_sword_location, really_big_sword_location]
    unfathomable_sword_valid_locations = [big_sword_location, really_big_sword_location, unfathomable_sword_location]

    big_sword_during_boss_fight = item_name_in_locations(sword_1, player, big_sword_valid_locations)
    really_big_sword_during_boss_fight = item_name_in_locations(sword_2, player, really_big_sword_valid_locations)
    unfathomable_sword_during_boss_fight = item_name_in_locations(sword_3, player, unfathomable_sword_valid_locations)

    # For each sword, either already have received it, or be guaranteed to get it during the fight at a valid stage.
    # Otherwise, a player can get soft locked.
    has_3_swords = lambda state: ((state.has(sword_1, player) or big_sword_during_boss_fight) and
                                  (state.has(sword_2, player) or really_big_sword_during_boss_fight) and
                                  (state.has(sword_3, player) or unfathomable_sword_during_boss_fight))
    set_rule(world.get_entrance("Boss Door", player), has_3_swords)


def set_lfod_self_obtained_items_rules(World_Options, player, world):
    if World_Options.item_shuffle != Options.ItemShuffle.option_disabled:
        return
    set_rule(world.get_entrance("Vines", player),
             lambda state: state.has("Incredibly Important Pack", player))
    set_rule(world.get_entrance("Behind Rocks", player),
             lambda state: state.can_reach("Cut Content", 'region', player))
    set_rule(world.get_entrance("Pickaxe Hard Cave", player),
             lambda state: state.can_reach("Cut Content", 'region', player) and
                           state.has("Name Change Pack", player))


def set_lfod_shuffled_items_rules(World_Options, player, world):
    if World_Options.item_shuffle != Options.ItemShuffle.option_shuffled:
        return
    set_rule(world.get_entrance("Vines", player),
             lambda state: state.has("Wooden Sword", player) or state.has("Pickaxe", player))
    set_rule(world.get_entrance("Behind Rocks", player),
             lambda state: state.has("Pickaxe", player))

    set_rule(world.get_location("Wooden Sword", player),
             lambda state: state.has("Incredibly Important Pack", player))
    set_rule(world.get_location("Pickaxe", player),
             lambda state: state.has("Humble Indie Bindle", player))
    set_rule(world.get_location("Humble Indie Bindle", player),
             lambda state: state.has("Box of Various Supplies", player) and
                           state.can_reach("Cut Content", 'region', player))
    set_rule(world.get_location("Box of Various Supplies", player),
             lambda state: state.can_reach("Cut Content", 'region', player))


def self_lfod_coinsanity_funded_purchase_rules(World_Options, player, world):
    if World_Options.coinsanity != Options.CoinSanity.option_coin:
        return
    number_of_bundle = math.floor(889 / World_Options.coinbundlequantity)
    for i in range(number_of_bundle):

        item_coin_freemium = "Live Freemium or Die: number Coin"
        item_coin_loc_freemium = re.sub("number", str(World_Options.coinbundlequantity * (i + 1)),
                                        item_coin_freemium)
        set_rule(world.get_location(item_coin_loc_freemium, player),
                 has_enough_coin_freemium(player, World_Options.coinbundlequantity * (i + 1)))
        if 889 % World_Options.coinbundlequantity != 0:
            set_rule(world.get_location("Live Freemium or Die: 889 Coin", player),
                     has_enough_coin_freemium(player, 889))

    add_rule(world.get_entrance("Boss Door", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(889 / World_Options.coinbundlequantity)))

    set_rule(world.get_location("Particles Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(5 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Day One Patch Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(5 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Checkpoint Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(5 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Incredibly Important Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(15 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Wall Jump Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(35 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Health Bar Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(5 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Parallax Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(5 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Harmless Plants Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(130 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Death of Comedy Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(15 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Canadian Dialog Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(10 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("DLC NPC Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(15 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Cut Content Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(40 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Name Change Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(150 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Season Pass", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(199 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("High Definition Next Gen Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(20 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Increased HP Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(10 / World_Options.coinbundlequantity)))
    set_rule(world.get_location("Remove Ads Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(25 / World_Options.coinbundlequantity)))


def set_lfod_self_funded_purchase_rules(World_Options, has_enough_coin_freemium, player, world):
    if World_Options.coinsanity != Options.CoinSanity.option_none:
        return
    add_rule(world.get_entrance("Boss Door", player),
             has_enough_coin_freemium(player, 889))

    set_rule(world.get_location("Particles Pack", player),
             has_enough_coin_freemium(player, 5))
    set_rule(world.get_location("Day One Patch Pack", player),
             has_enough_coin_freemium(player, 5))
    set_rule(world.get_location("Checkpoint Pack", player),
             has_enough_coin_freemium(player, 5))
    set_rule(world.get_location("Incredibly Important Pack", player),
             has_enough_coin_freemium(player, 15))
    set_rule(world.get_location("Wall Jump Pack", player),
             has_enough_coin_freemium(player, 35))
    set_rule(world.get_location("Health Bar Pack", player),
             has_enough_coin_freemium(player, 5))
    set_rule(world.get_location("Parallax Pack", player),
             has_enough_coin_freemium(player, 5))
    set_rule(world.get_location("Harmless Plants Pack", player),
             has_enough_coin_freemium(player, 130))
    set_rule(world.get_location("Death of Comedy Pack", player),
             has_enough_coin_freemium(player, 15))
    set_rule(world.get_location("Canadian Dialog Pack", player),
             has_enough_coin_freemium(player, 10))
    set_rule(world.get_location("DLC NPC Pack", player),
             has_enough_coin_freemium(player, 15))
    set_rule(world.get_location("Cut Content Pack", player),
             has_enough_coin_freemium(player, 40))
    set_rule(world.get_location("Name Change Pack", player),
             has_enough_coin_freemium(player, 150))
    set_rule(world.get_location("Season Pass", player),
             has_enough_coin_freemium(player, 199))
    set_rule(world.get_location("High Definition Next Gen Pack", player),
             has_enough_coin_freemium(player, 20))
    set_rule(world.get_location("Increased HP Pack", player),
             has_enough_coin_freemium(player, 10))
    set_rule(world.get_location("Remove Ads Pack", player),
             has_enough_coin_freemium(player, 25))


def set_completion_condition(World_Options, player, world):
    if World_Options.campaign == Options.Campaign.option_basic:
        world.completion_condition[player] = lambda state: state.has("Victory Basic", player)
    if World_Options.campaign == Options.Campaign.option_live_freemium_or_die:
        world.completion_condition[player] = lambda state: state.has("Victory Freemium", player)
    if World_Options.campaign == Options.Campaign.option_both:
        world.completion_condition[player] = lambda state: state.has("Victory Basic", player) and state.has(
            "Victory Freemium", player)
