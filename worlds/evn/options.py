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


# The first type of Option we'll discuss is the Toggle.
# A toggle is an option that can either be on or off. This will be represented by a checkbox on the website.
# The default for a toggle is "off".
# If you want a toggle to be on by default, you can use the "DefaultOnToggle" class instead of the "Toggle" class.
# class HardMode(Toggle):
#     """
#     In hard mode, the basic enemy and the final boss will have more health.
#     The Health Upgrades become progression, as they are now required to beat the final boss.
#     """

#     # The docstring of an option is used as the description on the website and in the template yaml.

#     # You'll also want to set a display name, which will determine what the option is called on the website.
#     display_name = "Hard Mode"

class ShuffleSystems(Toggle):
    """
    Shuffle the locations of all explorable systems in the universe.
    (Not Implemented)
    """
    display_name = "Shuffle Systems"

class IncludeOutfits(DefaultOnToggle):
    """
    Outfits will also need to be found and unlocked in order to purchase. Does not affect outfits ships come with naturally, but you may not be able to buy more ammo.
    """
    display_name = "Include Outfits in shuffle"

# We basically *have* to do this, so not going to bother with on/off
# class OutfitChecks(Toggle):
#     """
#     Will add Outfits that are purely checks. Purchasing them will unlock items for players.
#     (Not Implemented)
#     """
#     display_name = "Include Outfits as Checks"

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


# class Hammer(Toggle):
#     """
#     Adds another item to the itempool: The Hammer.
#     The top middle chest will now be locked behind a breakable wall, requiring the Hammer.
#     """

#     display_name = "Hammer"


# class ExtraStartingChest(Toggle):
#     """
#     Adds an extra chest in the bottom left, making room for an extra Confetti Cannon.
#     """

#     display_name = "Extra Starting Chest"


# class TrapChance(Range):
#     """
#     Percentage chance that any given Confetti Cannon will be replaced by a Math Trap.
#     """

#     display_name = "Trap Chance"

#     range_start = 0
#     range_end = 100
#     default = 0


# class StartWithOneConfettiCannon(Toggle):
#     """
#     Start with a confetti cannon already in your inventory.
#     Why? Because you deserve it. You get to celebrate yourself without doing any work first.
#     """

#     display_name = "Start With One Confetti Cannon"


# # A Range is a numeric option with a min and max value. This will be represented by a slider on the website.
# class ConfettiExplosiveness(Range):
#     """
#     How much confetti each use of a confetti cannon will fire.
#     """

#     display_name = "Confetti Explosiveness"

#     range_start = 0
#     range_end = 10

#     # Range options must define an explicit default value.
#     default = 3


# # A Choice is an option with multiple discrete choices. This will be represented by a dropdown on the website.
# class PlayerSprite(Choice):
#     """
#     The sprite that the player will have.
#     """

#     display_name = "Player Sprite"

#     option_human = 0
#     option_duck = 1
#     option_horse = 2
#     option_cat = 3

#     # Choice options must define an explicit default value.
#     default = option_human

#     # For choices, you can also define aliases.
#     # For example, we could make it so "player_sprite: kitty" resolves to "player_sprite: cat" like this:
#     alias_kitty = option_cat

class ChosenString(Choice):
    """
    Pick which major story string the player will follow. Other story strings will be disabled.
    Surprise Me - this randomly picks a string. Find out what it is in game!
    NOTE: The option name shows the path that has to be taken. Ex: vellos_polaris is the polaris story line coming from a refusal in the vellos string.

    default: Surprise Me
    """
    display_name = "Major Story String"

    # dynamically add the options with setattr()
    # def __init__(self, value: int):
    #     super().__init__(value) # super's init expects a value
    #     setattr(self, "option_test", 100)
    #     for key, value in story_routes.items():
    #         setattr(self, f"option_{value["option_name"]}", key) # TODO: extract option name from the key
    # for key, value in story_routes.items():
    #     locals().update(f"option_{value["option_name"]}", key)
    locals().update({f"option_{value["option_name"]}": int(f"{key}")
                     for key, value in story_routes.items()})

    # TODO: Pretty up the option names
    # @classmethod
    # def get_option_name(cls, value:int) -> str:
    #     # test value, get string and *return*
    #     return super().get_option_name(value) # returns default if not found above
    
    # TODO: confirm random as an option. Choice already supports a random option somehow, how do I use that?
    # I guess it is just the pattern option_random_[name]?

    #option_surprise_me = 0
    option_random_surprise_me = 0 # NOTE: Getting key errors. I don't think this is randomly rolling another option - so we'll manually handle in worlds
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
    shuffle_systems: ShuffleSystems
    include_outfits: IncludeOutfits
    #outfit_checks: OutfitChecks
    chosen_string: ChosenString
    always_avail_shops: AlwaysAvailableShops
    ignore_tech: IgnoreTechReq


# # If we want to group our options by similar type, we can do so as well. This looks nice on the website.
# option_groups = [
#     OptionGroup(
#         "Gameplay Options",
#         [HardMode, Hammer, ExtraStartingChest, StartWithOneConfettiCannon, TrapChance],
#     ),
#     OptionGroup(
#         "Aesthetic Options",
#         [ConfettiExplosiveness, PlayerSprite],
#     ),
# ]

# # Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
# option_presets = {
#     "boring": {
#         "hard_mode": False,
#         "hammer": False,
#         "extra_starting_chest": False,
#         "start_with_one_confetti_cannon": False,
#         "trap_chance": 0,
#         "confetti_explosiveness": ConfettiExplosiveness.range_start,
#         "player_sprite": PlayerSprite.option_human,
#     },
#     "the true way to play": {
#         "hard_mode": True,
#         "hammer": True,
#         "extra_starting_chest": True,
#         "start_with_one_confetti_cannon": True,
#         "trap_chance": 50,
#         "confetti_explosiveness": ConfettiExplosiveness.range_end,
#         "player_sprite": PlayerSprite.option_duck,
#     },
# }
