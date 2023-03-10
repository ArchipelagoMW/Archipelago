from .Locations import DLCquestLocation
from ..generic.Rules import add_rule, set_rule
from .Items import DLCquestItem
from BaseClasses import ItemClassification
from . import Options


def create_event(player, event: str):
    return DLCquestItem(event, ItemClassification.progression, None, player)

def set_rules(world, player,World_Options: Options.DLCQuestOptions):
    if World_Options[Options.Campaign] == Options.Campaign.option_basic or World_Options[Options.Campaign] == Options.Campaign.option_both:
        set_rule(world.get_entrance("Moving", player),
                 lambda state: state.has("Movement Pack", player))
        set_rule(world.get_entrance("Cloud", player),
                 lambda state: state.has("Psychological Warfare Pack", player))
        set_rule(world.get_entrance("Forest Entrance", player),
                 lambda state: state.has("Map Pack", player))
        set_rule(world.get_entrance("Behind Ogre", player),
                 lambda state: state.has("Gun Pack", player))
        set_rule(world.get_entrance("Forest True Double Jump", player),
                 lambda state: state.has("Double Jump Pack", player))

        if World_Options[Options.TimeIsMoney] == Options.TimeIsMoney.option_I_want_speed :
            set_rule(world.get_entrance("Tree", player),
                     lambda state: state.has("Time is Money Pack", player))

        if World_Options[Options.FalseDoubleJump] == Options.FalseDoubleJump.option_none :
            set_rule(world.get_entrance("Cloud Double Jump", player),
                    lambda state: state.has("Double Jump Pack", player))
            set_rule(world.get_entrance("Forest Double Jump", player),
                    lambda state: state.has("Double Jump Pack", player))

        if World_Options[Options.FalseDoubleJump] == Options.FalseDoubleJump.option_none or World_Options[Options.FalseDoubleJump] == Options.FalseDoubleJump.option_simple:
            set_rule(world.get_entrance("Behind Tree Double Jump", player),
                    lambda state: state.has("Double Jump Pack", player))

        set_rule(world.get_location("Movement Pack", player),
                 lambda state: state.has("Coin", player, 4))
        set_rule(world.get_location("Animation Pack", player),
                 lambda state: state.has("Coin", player, 5))
        set_rule(world.get_location("Audio Pack", player),
                 lambda state: state.has("Coin", player, 5))
        set_rule(world.get_location("Pause Menu Pack", player),
                 lambda state: state.has("Coin", player, 5))
        set_rule(world.get_location("Time is Money Pack", player),
                 lambda state: state.has("Coin", player, 20))
        set_rule(world.get_location("Double Jump Pack", player),
                 lambda state: state.has("Coin", player, 100))
        set_rule(world.get_location("Pet Pack", player),
                 lambda state: state.has("Coin", player, 5))
        set_rule(world.get_location("Sexy Outfits Pack", player),
                 lambda state: state.has("Coin", player, 5))
        set_rule(world.get_location("Top Hat Pack", player),
                 lambda state: state.has("Coin", player, 5))
        set_rule(world.get_location("Map Pack", player),
                 lambda state: state.has("Coin", player, 140))
        set_rule(world.get_location("Gun Pack", player),
                 lambda state: state.has("Coin", player, 75))
        set_rule(world.get_location("The Zombie Pack", player),
                 lambda state: state.has("Coin", player, 5))
        set_rule(world.get_location("Night Map Pack", player),
                 lambda state: state.has("Coin", player, 75))
        set_rule(world.get_location("Psychological Warfare Pack", player),
                 lambda state: state.has("Coin", player, 50))
        set_rule(world.get_location("Armor for your Horse Pack", player),
                 lambda state: state.has("Coin", player, 250))
        set_rule(world.get_location("Finish the Fight Pack", player),
                 lambda state: state.has("Coin", player, 5))

        loc_win = DLCquestLocation(player,"Winning", None, world.get_region("The Final Boss Room", player))
        world.get_region("The Final Boss Room", player).locations.append(loc_win)
        loc_win.place_locked_item(create_event(player, "Victory Basic"))
        if World_Options[Options.EndingChoice] == Options.EndingChoice.option_any:
            set_rule(world.get_location("Winning", player), lambda state:
                     state.has("Finish The Fight Pack", player))
        if World_Options[Options.EndingChoice] == Options.EndingChoice.option_true:
            set_rule(world.get_location("Winning", player), lambda state:
                     state.has("Armor for your Horse Pack", player) and state.has("Finish The Fight Pack", player))


    if World_Options[Options.Campaign] == Options.Campaign.option_live_freemium_or_die or World_Options[Options.Campaign] == Options.Campaign.option_both:
        set_rule(world.get_entrance("Vines", player),
                 lambda state: state.has("Incredibly Important Pack", player))
        set_rule(world.get_entrance("Wall Jump Entrance", player),
                 lambda state: state.has("Wall Jump Pack,progression", player))
        set_rule(world.get_entrance("Harmless Plants", player),
                 lambda state: state.has("Harmless Plants Pack", player))
        set_rule(world.get_entrance("Pickaxe Hard Cave", player),
                 lambda state: state.has("Pickaxe", player))
        set_rule(world.get_entrance("Name Change Entrance", player),
                 lambda state: state.has("Name Change Pack", player))
        set_rule(world.get_entrance("Cut Content Entrance", player),
                 lambda state: state.has("Cut Content Pack", player))
        set_rule(world.get_entrance("Behind Rocks", player),
                 lambda state: state.has("Pickaxe", player))
        set_rule(world.get_entrance("Blizzard", player),
                 lambda state: state.has("Season Pass", player))
        set_rule(world.get_entrance("Boss Door", player),
                 lambda state: state.has("Coin_freemium", player, 889))

        set_rule(world.get_location("Particles Pack", player),
                 lambda state: state.has("Coin_Freemium", player, 5))
        set_rule(world.get_location("Day One Patch Pack", player),
                 lambda state: state.has("Coin_Freemium", player, 5))
        set_rule(world.get_location("Checkpoint Pack", player),
                 lambda state: state.has("Coin_Freemium", player, 5))
        set_rule(world.get_location("Incredibly Important Pack", player),
                 lambda state: state.has("Coin_Freemium", player, 15))
        set_rule(world.get_location("Wall Jump Pack", player),
                 lambda state: state.has("Coin_Freemium", player, 35))
        set_rule(world.get_location("Health Bar Pack", player),
                 lambda state: state.has("Coin_Freemium", player, 5))
        set_rule(world.get_location("Parallax Pack", player),
                 lambda state: state.has("Coin_Freemium", player, 5))
        set_rule(world.get_location("Harmless Plants Pack", player),
                 lambda state: state.has("Coin_Freemium", player, 130))
        set_rule(world.get_location("Death of Comedy Pack", player),
                 lambda state: state.has("Coin_Freemium", player, 15))
        set_rule(world.get_location("Canadian Dialog Pack", player),
                 lambda state: state.has("Coin_Freemium", player, 10))
        set_rule(world.get_location("DLC NPC Pack", player),
                 lambda state: state.has("Coin_Freemium", player, 15))
        set_rule(world.get_location("Cut Content Pack", player),
                 lambda state: state.has("Coin_Freemium", player, 40))
        set_rule(world.get_location("Name Change Pack", player),
                 lambda state: state.has("Coin_Freemium", player, 150))
        set_rule(world.get_location("Season Pass", player),
                 lambda state: state.has("Coin_Freemium", player, 199))
        set_rule(world.get_location("High Definition Next Gen Pack", player),
                 lambda state: state.has("Coin_Freemium", player, 20))
        set_rule(world.get_location("Increased HP Pack", player),
                 lambda state: state.has("Coin_Freemium", player, 10))
        set_rule(world.get_location("Remove Ads Pack", player),
                 lambda state: state.has("Coin_Freemium", player, 25))
        set_rule(world.get_location("Pickaxe", player), lambda state: state.can_reach("Cut Content", 'region', player))

        loc_wining = DLCquestLocation(player, "Winning Freemium", None, world.get_region("Final Boss", player))
        world.get_region("Final Boss", player).locations.append(loc_wining)
        loc_wining.place_locked_item(create_event(player, "Victory Freemium"))

    if World_Options[Options.Campaign] == Options.Campaign.option_basic:
        world.completion_condition[player] = lambda state: state.has("Victory Basic", player)

    if World_Options[Options.Campaign] == Options.Campaign.option_live_freemium_or_die:
        world.completion_condition[player] = lambda state: state.has("Victory Freemium", player)

    if World_Options[Options.Campaign] == Options.Campaign.option_both:
        world.completion_condition[player] = lambda state: state.has("Victory Basic", player) and state.has("Victory Freemium", player)
