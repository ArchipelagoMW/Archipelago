from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, OptionGroup, PerGameCommonOptions, Range, Toggle

from .logics import story_routes

# In this file, we define the options the player can pick.
# The most common types of options are Toggle, Range and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.
# (Note: Options can also be made invisible from either of these places by overriding Option.visibility.
#  APQuest doesn't have an example of this, but this can be used for secret / hidden / advanced options.)

# For further reading on options, you can also read the Options API Document:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md

# Future idea
# class ShuffleSystems(Toggle):
#     """
#     Shuffle the locations of all explorable systems in the universe.
#     (Not Implemented)
#     """
#     display_name = "Shuffle Systems"

class IncludeOutfits(DefaultOnToggle):
    """
    Outfits will also need to be found and unlocked in order to purchase. Does not affect outfits ships come with naturally, but you may not be able to buy more ammo.
    NOTE: Balance was designed around this being on. Turning it off will add lots of money filler items and probably make things much easier overall.
    NOTE: When on, there will be additional checks added to the outfitter as custom shop items.
    """
    display_name = "Include Outfits in shuffle"

class AlwaysAvailableShops(Toggle):
    """
    When on, ships and outf will always show up in shops (if unlocked)
    """
    display_name = "Shops Always Stock"

class IgnoreTechReq(Toggle):
    """
    When on, tech level requirements are ignored. Any unlocked ships / outf will be available at any spob with shipyard / outfitters.
    Also ignores license requirements (ex: heavy weapons)
    """
    display_name = "Ignore Tech Requirements"

class ChosenString(Choice):
    """
    Pick which major story string the player will follow. Other story strings will be disabled.
    Surprise Me - this randomly picks a string during generation. Find out what it is in game!
    NOTE: The option name shows the path that has to be taken. Ex: vellos_polaris is the polaris story line coming from a refusal in the vellos string.

    default: Surprise Me
    """
    display_name = "Major Story String"

    # Extract our possible story routes from logics and create associated
    # options for them in this list.
    locals().update({f"option_{value["option_name"]}": int(f"{key}")
                     for key, value in story_routes.items()})

    # TODO: Pretty up the option names
    # @classmethod
    # def get_option_name(cls, value:int) -> str:
    #     # test value, get string and *return*
    #     return super().get_option_name(value) # returns default if not found above
    
    # TODO: confirm random as an option. Choice already supports a random option somehow, how do I use that?
    # I guess it is just the pattern option_random_[name]?
    # NOTE: Getting key errors. I don't think this is randomly rolling another option - so we'll manually handle in worlds

    option_random_surprise_me = 0 
    # option_vellos = 0
    # option_fed = 1
    # option_rebel = 2
    # option_pirate = 3
    # option_auroran = 4
    # option_polaris = 5

    default = option_random_surprise_me


# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class EVNOptions(PerGameCommonOptions):
    #shuffle_systems: ShuffleSystems
    include_outfits: IncludeOutfits
    #outfit_checks: OutfitChecks
    chosen_string: ChosenString
    always_avail_shops: AlwaysAvailableShops
    ignore_tech: IgnoreTechReq


# We could group options usingg option_groups. Review apquest's options.

# # Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets = {
    "standard": {
        "include_outfits": True,
        "chosen_string": ChosenString.option_random_surprise_me,
        "always_avail_shops": True,
        "ignore_tech": True,
    },
    "original": {
        "include_outfits": True,
        "chosen_string": ChosenString.option_random_surprise_me,
        "always_avail_shops": False,
        "ignore_tech": False,
    },
    "ships only": {
        "include_outfits": False,
        "chosen_string": ChosenString.option_random_surprise_me,
        "always_avail_shops": False,
        "ignore_tech": False,
    }
}
