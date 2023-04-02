import math
import re
from .Locations import DLCQuestLocation
from ..generic.Rules import add_rule, set_rule
from .Items import DLCQuestItem
from BaseClasses import ItemClassification
from . import Options


def create_event(player, event: str):
    return DLCQuestItem(event, ItemClassification.progression, None, player)


def set_rules(world, player, World_Options: Options.DLCQuestOptions):
    def has_enough_coin(player: int, coin: int):
        def has_coin(state, player: int, coins: int):
            coin_possessed = 0
            for i in [4, 7, 9, 10, 46, 50, 60, 76, 89, 100, 169, 203]:
                name_coin = f"{i} coins"
                if state.has(name_coin, player):
                    coin_possessed += i

            return coin_possessed >= coins

        return lambda state: has_coin(state, player, coin)

    def has_enough_coin_freemium(player: int, coin: int):
        def has_coin(state, player: int, coins: int):
            coin_possessed = 0
            for i in [20, 50, 90, 95, 130, 150, 154, 200]:
                name_coin = f"{i} coins freemium"
                if state.has(name_coin, player):
                    coin_possessed += i

            return coin_possessed >= coins

        return lambda state: has_coin(state, player, coin)

    if World_Options[Options.Campaign] == Options.Campaign.option_basic or World_Options[
        Options.Campaign] == Options.Campaign.option_both:
        set_rule(world.get_entrance("Moving", player),
                 lambda state: state.has("Movement Pack", player))
        set_rule(world.get_entrance("Cloud", player),
                 lambda state: state.has("Psychological Warfare Pack", player))
        set_rule(world.get_entrance("Forest Entrance", player),
                 lambda state: state.has("Map Pack", player))
        set_rule(world.get_entrance("Forest True Double Jump", player),
                 lambda state: state.has("Double Jump Pack", player))

        if World_Options[Options.ItemShuffle] == Options.ItemShuffle.option_disabled:
            set_rule(world.get_entrance("Behind Ogre", player),
                     lambda state: state.has("Gun Pack", player))

            if World_Options[Options.TimeIsMoney] == Options.TimeIsMoney.option_required:
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

        if World_Options[Options.ItemShuffle] == Options.ItemShuffle.option_shuffled:
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

            if World_Options[Options.TimeIsMoney] == Options.TimeIsMoney.option_required:
                set_rule(world.get_location("Sword", player),
                         lambda state: state.has("Time is Money Pack", player))

        if World_Options[Options.FalseDoubleJump] == Options.FalseDoubleJump.option_none:
            set_rule(world.get_entrance("Cloud Double Jump", player),
                     lambda state: state.has("Double Jump Pack", player))
            set_rule(world.get_entrance("Forest Double Jump", player),
                     lambda state: state.has("Double Jump Pack", player))

        if World_Options[Options.FalseDoubleJump] == Options.FalseDoubleJump.option_none or World_Options[
            Options.FalseDoubleJump] == Options.FalseDoubleJump.option_simple:
            set_rule(world.get_entrance("Behind Tree Double Jump", player),
                     lambda state: state.has("Double Jump Pack", player))
            set_rule(world.get_entrance("Cave Roof", player),
                     lambda state: state.has("Double Jump Pack", player))

        if World_Options[Options.CoinSanity] == Options.CoinSanity.option_coin:
            number_of_bundle = math.floor(825 / World_Options[Options.CoinSanityRange])
            for i in range(number_of_bundle):

                item_coin = "DLC Quest: number Coin"
                item_coin_loc = re.sub("number", str(World_Options[Options.CoinSanityRange] * (i + 1)), item_coin)
                set_rule(world.get_location(item_coin_loc, player),
                         has_enough_coin(player, World_Options[Options.CoinSanityRange] * (i + 1)))
                if 825 % World_Options[Options.CoinSanityRange] != 0:
                    set_rule(world.get_location("DLC Quest: 825 Coin", player),
                             has_enough_coin(player, 825))

            set_rule(world.get_location("Movement Pack", player),
                     lambda state: state.has("DLC Quest: Coin Bundle", player,
                                             math.ceil(4 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Animation Pack", player),
                     lambda state: state.has("DLC Quest: Coin Bundle", player,
                                             math.ceil(5 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Audio Pack", player),
                     lambda state: state.has("DLC Quest: Coin Bundle", player,
                                             math.ceil(5 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Pause Menu Pack", player),
                     lambda state: state.has("DLC Quest: Coin Bundle", player,
                                             math.ceil(5 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Time is Money Pack", player),
                     lambda state: state.has("DLC Quest: Coin Bundle", player,
                                             math.ceil(20 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Double Jump Pack", player),
                     lambda state: state.has("DLC Quest: Coin Bundle", player,
                                             math.ceil(100 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Pet Pack", player),
                     lambda state: state.has("DLC Quest: Coin Bundle", player,
                                             math.ceil(5 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Sexy Outfits Pack", player),
                     lambda state: state.has("DLC Quest: Coin Bundle", player,
                                             math.ceil(5 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Top Hat Pack", player),
                     lambda state: state.has("DLC Quest: Coin Bundle", player,
                                             math.ceil(5 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Map Pack", player),
                     lambda state: state.has("DLC Quest: Coin Bundle", player,
                                             math.ceil(140 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Gun Pack", player),
                     lambda state: state.has("DLC Quest: Coin Bundle", player,
                                             math.ceil(75 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("The Zombie Pack", player),
                     lambda state: state.has("DLC Quest: Coin Bundle", player,
                                             math.ceil(5 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Night Map Pack", player),
                     lambda state: state.has("DLC Quest: Coin Bundle", player,
                                             math.ceil(75 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Psychological Warfare Pack", player),
                     lambda state: state.has("DLC Quest: Coin Bundle", player,
                                             math.ceil(50 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Armor for your Horse Pack", player),
                     lambda state: state.has("DLC Quest: Coin Bundle", player,
                                             math.ceil(250 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Finish the Fight Pack", player),
                     lambda state: state.has("DLC Quest: Coin Bundle", player,
                                             math.ceil(5 / World_Options[Options.CoinSanityRange])))

        if World_Options[Options.CoinSanity] == Options.CoinSanity.option_none:
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


        if World_Options[Options.EndingChoice] == Options.EndingChoice.option_any:
            set_rule(world.get_location("Winning Basic", player),
                     lambda state: state.has("Finish the Fight Pack", player))
        if World_Options[Options.EndingChoice] == Options.EndingChoice.option_true:
            set_rule(world.get_location("Winning Basic", player),
                     lambda state: state.has("Armor for your Horse Pack", player) and state.has("Finish the Fight Pack",
                                                                                                player))

    if World_Options[Options.Campaign] == Options.Campaign.option_live_freemium_or_die or World_Options[
        Options.Campaign] == Options.Campaign.option_both:
        set_rule(world.get_entrance("Wall Jump Entrance", player),
                 lambda state: state.has("Wall Jump Pack", player))
        set_rule(world.get_entrance("Harmless Plants", player),
                 lambda state: state.has("Harmless Plants Pack", player))
        set_rule(world.get_entrance("Pickaxe Hard Cave", player),
                 lambda state: state.has("Pickaxe", player))
        set_rule(world.get_entrance("Name Change Entrance", player),
                 lambda state: state.has("Name Change Pack", player))
        set_rule(world.get_entrance("Cut Content Entrance", player),
                 lambda state: state.has("Cut Content Pack", player))
        set_rule(world.get_entrance("Blizzard", player),
                 lambda state: state.has("Season Pass", player))
        set_rule(world.get_entrance("Boss Door", player),
                 lambda state: state.has("Big Sword Pack", player) and state.has("Really Big Sword Pack",
                                                                                 player) and state.has(
                     "Unfathomable Sword Pack", player))
        set_rule(world.get_location("I Get That Reference!", player),
                 lambda state: state.has("Death of Comedy Pack", player))
        set_rule(world.get_location("Story is Important", player),
                 lambda state: state.has("DLC NPC Pack", player))

        if World_Options[Options.ItemShuffle] == Options.ItemShuffle.option_disabled:
            set_rule(world.get_entrance("Vines", player),
                     lambda state: state.has("Incredibly Important Pack", player))
            set_rule(world.get_entrance("Behind Rocks", player),
                     lambda state: state.can_reach("Cut Content", 'region', player))

        if World_Options[Options.ItemShuffle] == Options.ItemShuffle.option_shuffled:
            set_rule(world.get_entrance("Vines", player),
                     lambda state: state.has("Wooden Sword", player) or state.has("Pickaxe", player))
            set_rule(world.get_entrance("Behind Rocks", player),
                     lambda state: state.has("Pickaxe", player))

            set_rule(world.get_location("Wooden Sword", player),
                     lambda state: state.has("Incredibly Important Pack", player))
            set_rule(world.get_location("Pickaxe", player),
                     lambda state: state.has("Humble Indie Bindle", player))
            set_rule(world.get_location("Humble Indie Bindle", player),
                     lambda state: state.has("Box of Various Supplies", player) and state.can_reach("Cut Content",
                                                                                                    'region', player))
            set_rule(world.get_location("Box of Various Supplies", player),
                     lambda state: state.can_reach("Cut Content", 'region', player))

        if World_Options[Options.CoinSanity] == Options.CoinSanity.option_coin:
            number_of_bundle = math.floor(889 / World_Options[Options.CoinSanityRange])
            for i in range(number_of_bundle):

                item_coin_freemium = "Live Freemium or Die: number Coin"
                item_coin_loc_freemium = re.sub("number", str(World_Options[Options.CoinSanityRange] * (i + 1)),
                                                item_coin_freemium)
                set_rule(world.get_location(item_coin_loc_freemium, player),
                         has_enough_coin_freemium(player, World_Options[Options.CoinSanityRange] * (i + 1)))
                if 889 % World_Options[Options.CoinSanityRange] != 0:
                    set_rule(world.get_location("Live Freemium or Die: 889 Coin", player),
                             has_enough_coin_freemium(player, 889))

            set_rule(world.get_entrance("Boss Door", player),
                     lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                             math.ceil(889 / World_Options[Options.CoinSanityRange])))

            set_rule(world.get_location("Particles Pack", player),
                     lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                             math.ceil(5 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Day One Patch Pack", player),
                     lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                             math.ceil(5 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Checkpoint Pack", player),
                     lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                             math.ceil(5 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Incredibly Important Pack", player),
                     lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                             math.ceil(15 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Wall Jump Pack", player),
                     lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                             math.ceil(35 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Health Bar Pack", player),
                     lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                             math.ceil(5 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Parallax Pack", player),
                     lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                             math.ceil(5 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Harmless Plants Pack", player),
                     lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                             math.ceil(130 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Death of Comedy Pack", player),
                     lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                             math.ceil(15 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Canadian Dialog Pack", player),
                     lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                             math.ceil(10 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("DLC NPC Pack", player),
                     lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                             math.ceil(15 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Cut Content Pack", player),
                     lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                             math.ceil(40 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Name Change Pack", player),
                     lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                             math.ceil(150 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Season Pass", player),
                     lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                             math.ceil(199 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("High Definition Next Gen Pack", player),
                     lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                             math.ceil(20 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Increased HP Pack", player),
                     lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                             math.ceil(10 / World_Options[Options.CoinSanityRange])))
            set_rule(world.get_location("Remove Ads Pack", player),
                     lambda state: state.has("Live Freemium or Die: Coin Bundle", player,
                                             math.ceil(25 / World_Options[Options.CoinSanityRange])))

        if World_Options[Options.CoinSanity] == Options.CoinSanity.option_none:
            set_rule(world.get_entrance("Boss Door", player),
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



    if World_Options[Options.Campaign] == Options.Campaign.option_basic:
        world.completion_condition[player] = lambda state: state.has("Victory Basic", player)

    if World_Options[Options.Campaign] == Options.Campaign.option_live_freemium_or_die:
        world.completion_condition[player] = lambda state: state.has("Victory Freemium", player)

    if World_Options[Options.Campaign] == Options.Campaign.option_both:
        world.completion_condition[player] = lambda state: state.has("Victory Basic", player) and state.has(
            "Victory Freemium", player)
