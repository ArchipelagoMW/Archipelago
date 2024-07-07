import math

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


def set_rules(world, player, world_options: Options.DLCQuestOptions):
    set_basic_rules(world_options, player, world)
    set_lfod_rules(world_options, player, world)
    set_completion_condition(world_options, player, world)


def set_basic_rules(world_options, player, world):
    if world_options.campaign == Options.Campaign.option_live_freemium_or_die:
        return
    set_basic_entrance_rules(player, world)
    set_basic_self_obtained_items_rules(world_options, player, world)
    set_basic_shuffled_items_rules(world_options, player, world)
    set_double_jump_glitchless_rules(world_options, player, world)
    set_easy_double_jump_glitch_rules(world_options, player, world)
    self_basic_coinsanity_funded_purchase_rules(world_options, player, world)
    set_basic_self_funded_purchase_rules(world_options, player, world)
    self_basic_win_condition(world_options, player, world)


def set_basic_entrance_rules(player, world):
    set_rule(world.get_entrance("Moving", player),
             lambda state: state.has("Movement Pack", player))
    set_rule(world.get_entrance("Cloud", player),
             lambda state: state.has("Psychological Warfare Pack", player))
    set_rule(world.get_entrance("Forest Entrance", player),
             lambda state: state.has("Map Pack", player))
    set_rule(world.get_entrance("Forest True Double Jump", player),
             lambda state: state.has("Double Jump Pack", player))


def set_basic_self_obtained_items_rules(world_options, player, world):
    if world_options.item_shuffle != Options.ItemShuffle.option_disabled:
        return
    set_rule(world.get_entrance("Behind Ogre", player),
             lambda state: state.has("Gun Pack", player))

    if world_options.time_is_money == Options.TimeIsMoney.option_required:
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


def set_basic_shuffled_items_rules(world_options, player, world):
    if world_options.item_shuffle != Options.ItemShuffle.option_shuffled:
        return
    set_rule(world.get_entrance("Behind Ogre", player),
             lambda state: state.has("DLC Quest: Progressive Weapon", player, 2))
    set_rule(world.get_entrance("Tree", player),
             lambda state: state.has("DLC Quest: Progressive Weapon", player))
    set_rule(world.get_entrance("Cave Tree", player),
             lambda state: state.has("DLC Quest: Progressive Weapon", player))
    set_rule(world.get_entrance("True Double Jump", player),
             lambda state: state.has("Double Jump Pack", player))
    set_rule(world.get_location("Shepherd Sheep", player),
             lambda state: state.has("DLC Quest: Progressive Weapon", player))
    set_rule(world.get_location("North West Ceiling Sheep", player),
             lambda state: state.has("DLC Quest: Progressive Weapon", player))
    set_rule(world.get_location("North West Alcove Sheep", player),
             lambda state: state.has("DLC Quest: Progressive Weapon", player))
    set_rule(world.get_location("West Cave Sheep", player),
             lambda state: state.has("DLC Quest: Progressive Weapon", player))
    set_rule(world.get_location("Gun", player),
             lambda state: state.has("Gun Pack", player))

    if world_options.time_is_money == Options.TimeIsMoney.option_required:
        set_rule(world.get_location("Sword", player),
                 lambda state: state.has("Time is Money Pack", player))


def set_double_jump_glitchless_rules(world_options, player, world):
    if world_options.double_jump_glitch != Options.DoubleJumpGlitch.option_none:
        return
    set_rule(world.get_entrance("Cloud Double Jump", player),
             lambda state: state.has("Double Jump Pack", player))
    set_rule(world.get_entrance("Forest Double Jump", player),
             lambda state: state.has("Double Jump Pack", player))


def set_easy_double_jump_glitch_rules(world_options, player, world):
    if world_options.double_jump_glitch == Options.DoubleJumpGlitch.option_all:
        return
    set_rule(world.get_entrance("Behind Tree Double Jump", player),
             lambda state: state.has("Double Jump Pack", player))
    set_rule(world.get_entrance("Cave Roof", player),
             lambda state: state.has("Double Jump Pack", player))


def self_basic_coinsanity_funded_purchase_rules(world_options, player, world):
    if world_options.coinsanity != Options.CoinSanity.option_coin:
        return
    if world_options.coinbundlequantity == -1:
        self_basic_coinsanity_piece_rules(player, world)
        return
    number_of_bundle = math.floor(825 / world_options.coinbundlequantity)
    for i in range(number_of_bundle):

        item_coin = f"DLC Quest: {world_options.coinbundlequantity * (i + 1)} Coin"
        set_rule(world.get_location(item_coin, player),
                 has_enough_coin(player, world_options.coinbundlequantity * (i + 1)))
        if 825 % world_options.coinbundlequantity != 0:
            set_rule(world.get_location("DLC Quest: 825 Coin", player),
                     has_enough_coin(player, 825))

    set_rule(world.get_location("Movement Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(4 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Animation Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(5 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Audio Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(5 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Pause Menu Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(5 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Time is Money Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(20 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Double Jump Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(100 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Pet Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(5 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Sexy Outfits Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(5 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Top Hat Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(5 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Map Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(140 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Gun Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(75 / world_options.coinbundlequantity)))
    set_rule(world.get_location("The Zombie Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(5 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Night Map Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(75 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Psychological Warfare Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(50 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Armor for your Horse Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(250 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Finish the Fight Pack", player),
             lambda state: state.has("DLC Quest: Coin Bundle", player,
                                     math.ceil(5 / world_options.coinbundlequantity)))


def set_basic_self_funded_purchase_rules(world_options, player, world):
    if world_options.coinsanity != Options.CoinSanity.option_none:
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


def self_basic_win_condition(world_options, player, world):
    if world_options.ending_choice == Options.EndingChoice.option_any:
        set_rule(world.get_location("Winning Basic", player),
                 lambda state: state.has("Finish the Fight Pack", player))
    if world_options.ending_choice == Options.EndingChoice.option_true:
        set_rule(world.get_location("Winning Basic", player),
                 lambda state: state.has("Armor for your Horse Pack", player) and state.has("Finish the Fight Pack",
                                                                                            player))


def set_lfod_rules(world_options, player, world):
    if world_options.campaign == Options.Campaign.option_basic:
        return
    set_lfod_entrance_rules(player, world)
    set_boss_door_requirements_rules(player, world)
    set_lfod_self_obtained_items_rules(world_options, player, world)
    set_lfod_shuffled_items_rules(world_options, player, world)
    self_lfod_coinsanity_funded_purchase_rules(world_options, player, world)
    set_lfod_self_funded_purchase_rules(world_options, has_enough_coin_freemium, player, world)


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


def set_lfod_self_obtained_items_rules(world_options, player, world):
    if world_options.item_shuffle != Options.ItemShuffle.option_disabled:
        return
    set_rule(world.get_entrance("Vines", player),
             lambda state: state.has("Incredibly Important Pack", player))
    set_rule(world.get_entrance("Behind Rocks", player),
             lambda state: state.can_reach("Cut Content", 'region', player))
    set_rule(world.get_entrance("Pickaxe Hard Cave", player),
             lambda state: state.can_reach("Cut Content", 'region', player) and
                           state.has("Name Change Pack", player))


def set_lfod_shuffled_items_rules(world_options, player, world):
    if world_options.item_shuffle != Options.ItemShuffle.option_shuffled:
        return
    set_rule(world.get_entrance("Vines", player),
             lambda state: state.has("Live Freemium or Die: Progressive Weapon", player))
    set_rule(world.get_entrance("Behind Rocks", player),
             lambda state: state.has("Live Freemium or Die: Progressive Weapon", player, 2))
    set_rule(world.get_entrance("Pickaxe Hard Cave", player),
             lambda state: state.has("Live Freemium or Die: Progressive Weapon", player, 2))

    set_rule(world.get_location("Wooden Sword", player),
             lambda state: state.has("Incredibly Important Pack", player))
    set_rule(world.get_location("Pickaxe", player),
             lambda state: state.has("Humble Indie Bindle", player))
    set_rule(world.get_location("Humble Indie Bindle", player),
             lambda state: state.has("Box of Various Supplies", player) and
                           state.can_reach("Cut Content", 'region', player))
    set_rule(world.get_location("Box of Various Supplies", player),
             lambda state: state.can_reach("Cut Content", 'region', player))


def self_lfod_coinsanity_funded_purchase_rules(world_options, player, world):
    if world_options.coinsanity != Options.CoinSanity.option_coin:
        return
    if world_options.coinbundlequantity == -1:
        self_lfod_coinsanity_piece_rules(player, world)
        return
    number_of_bundle = math.floor(889 / world_options.coinbundlequantity)
    for i in range(number_of_bundle):

        item_coin_freemium = f"Live Freemium or Die: {world_options.coinbundlequantity * (i + 1)} Coin"
        set_rule(world.get_location(item_coin_freemium, player),
                 has_enough_coin_freemium(player, world_options.coinbundlequantity * (i + 1)))
        if 889 % world_options.coinbundlequantity != 0:
            set_rule(world.get_location("Live Freemium or Die: 889 Coin", player),
                     has_enough_coin_freemium(player, 889))

    add_rule(world.get_entrance("Boss Door", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(200 / world_options.coinbundlequantity)))

    set_rule(world.get_location("Particles Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(5 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Day One Patch Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(5 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Checkpoint Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(5 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Incredibly Important Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(15 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Wall Jump Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(35 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Health Bar Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(5 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Parallax Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(5 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Harmless Plants Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(130 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Death of Comedy Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(15 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Canadian Dialog Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(10 / world_options.coinbundlequantity)))
    set_rule(world.get_location("DLC NPC Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(15 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Cut Content Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(40 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Name Change Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(150 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Season Pass", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(199 / world_options.coinbundlequantity)))
    set_rule(world.get_location("High Definition Next Gen Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(20 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Increased HP Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(10 / world_options.coinbundlequantity)))
    set_rule(world.get_location("Remove Ads Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                     math.ceil(25 / world_options.coinbundlequantity)))


def set_lfod_self_funded_purchase_rules(world_options, has_enough_coin_freemium, player, world):
    if world_options.coinsanity != Options.CoinSanity.option_none:
        return
    add_rule(world.get_entrance("Boss Door", player),
             has_enough_coin_freemium(player, 200))

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


def set_completion_condition(world_options, player, world):
    if world_options.campaign == Options.Campaign.option_basic:
        world.completion_condition[player] = lambda state: state.has("Victory Basic", player)
    if world_options.campaign == Options.Campaign.option_live_freemium_or_die:
        world.completion_condition[player] = lambda state: state.has("Victory Freemium", player)
    if world_options.campaign == Options.Campaign.option_both:
        world.completion_condition[player] = lambda state: state.has("Victory Basic", player) and state.has(
            "Victory Freemium", player)


def self_basic_coinsanity_piece_rules(player, world):
    for i in range(1,8251):

        item_coin = f"DLC Quest: {i} Coin Piece"
        set_rule(world.get_location(item_coin, player),
                 has_enough_coin(player, math.ceil(i / 10)))

    set_rule(world.get_location("Movement Pack", player),
             lambda state: state.has("DLC Quest: Coin Piece", player, 40))
    set_rule(world.get_location("Animation Pack", player),
             lambda state: state.has("DLC Quest: Coin Piece", player, 50))
    set_rule(world.get_location("Audio Pack", player),
             lambda state: state.has("DLC Quest: Coin Piece", player, 50))
    set_rule(world.get_location("Pause Menu Pack", player),
             lambda state: state.has("DLC Quest: Coin Piece", player, 50))
    set_rule(world.get_location("Time is Money Pack", player),
             lambda state: state.has("DLC Quest: Coin Piece", player, 200))
    set_rule(world.get_location("Double Jump Pack", player),
             lambda state: state.has("DLC Quest: Coin Piece", player, 100))
    set_rule(world.get_location("Pet Pack", player),
             lambda state: state.has("DLC Quest: Coin Piece", player, 50))
    set_rule(world.get_location("Sexy Outfits Pack", player),
             lambda state: state.has("DLC Quest: Coin Piece", player, 50))
    set_rule(world.get_location("Top Hat Pack", player),
             lambda state: state.has("DLC Quest: Coin Piece", player, 50))
    set_rule(world.get_location("Map Pack", player),
             lambda state: state.has("DLC Quest: Coin Piece", player, 1400))
    set_rule(world.get_location("Gun Pack", player),
             lambda state: state.has("DLC Quest: Coin Piece", player, 750))
    set_rule(world.get_location("The Zombie Pack", player),
             lambda state: state.has("DLC Quest: Coin Piece", player, 50))
    set_rule(world.get_location("Night Map Pack", player),
             lambda state: state.has("DLC Quest: Coin Piece", player, 750))
    set_rule(world.get_location("Psychological Warfare Pack", player),
             lambda state: state.has("DLC Quest: Coin Piece", player, 500))
    set_rule(world.get_location("Armor for your Horse Pack", player),
             lambda state: state.has("DLC Quest: Coin Piece", player, 2500))
    set_rule(world.get_location("Finish the Fight Pack", player),
             lambda state: state.has("DLC Quest: Coin Piece", player, 50))


def self_lfod_coinsanity_piece_rules(player, world):
    for i in range(1, 8891):

        item_coin_freemium = f"Live Freemium or Die: {i} Coin Piece"
        set_rule(world.get_location(item_coin_freemium, player),
                 has_enough_coin_freemium(player, math.ceil(i / 10)))

    add_rule(world.get_entrance("Boss Door", player),
             lambda state: state.has("Live Freemium or Die: Coin Piece", player, 2000))

    set_rule(world.get_location("Particles Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Piece", player, 50))
    set_rule(world.get_location("Day One Patch Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Piece", player, 50))
    set_rule(world.get_location("Checkpoint Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Piece", player, 50))
    set_rule(world.get_location("Incredibly Important Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Piece", player, 150))
    set_rule(world.get_location("Wall Jump Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Piece", player, 350))
    set_rule(world.get_location("Health Bar Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Piece", player, 50))
    set_rule(world.get_location("Parallax Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Piece", player, 50))
    set_rule(world.get_location("Harmless Plants Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Piece", player, 1300))
    set_rule(world.get_location("Death of Comedy Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Piece", player, 150))
    set_rule(world.get_location("Canadian Dialog Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Piece", player, 100))
    set_rule(world.get_location("DLC NPC Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Piece", player, 150))
    set_rule(world.get_location("Cut Content Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Piece", player, 400))
    set_rule(world.get_location("Name Change Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Piece", player, 1500))
    set_rule(world.get_location("Season Pass", player),
             lambda state: state.has("Live Freemium or Die: Coin Piece", player, 199))
    set_rule(world.get_location("High Definition Next Gen Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Piece", player, 20))
    set_rule(world.get_location("Increased HP Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Piece", player, 100))
    set_rule(world.get_location("Remove Ads Pack", player),
             lambda state: state.has("Live Freemium or Die: Coin Piece", player, 250))
