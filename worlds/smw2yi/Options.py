from typing import Dict, Union
from BaseClasses import MultiWorld
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, Option, OptionDict
from schema import Schema, And, Optional

class ExtrasEnabled(Toggle):
    """This will add the difficult and optional Extra stages into logic"""
    display_name = "Include Extra Stages"

class SplitExtras(Toggle):
    """This will split the Extra stages into individual unlocks. Does nothing if Extras are not enabled."""
    display_name = "Split Extra Stages"

class SplitBonus(Toggle):
    """This will split the Bonus stages into individual unlocks."""
    display_name = "Split Bonus Games"

class CoinVisibility(Choice):
    """This will determine the default visibility of hidden objects.
    Strict Logic will expect the Secret Lens or a Magnifying Glass to interact with hidden clouds."""
    display_name = "Hidden Object Visibility"
    option_none = 0
    option_coins_only = 1
    option_clouds_only = 2
    option_full = 3
    default = 1

class YoshiColors(Choice):
    """Sets the Yoshi level palettes. Normal will use the default colors,
    Shuffled will swap the default colors amongst each other,
    Singularity will force the same color for all of them."""
    display_name = "Yoshi Colors"
    option_normal = 0
    option_shuffled = 1
    option_singularity = 2
    default = 0

class StageLogic(Choice):
    """This determines what logic mode the stages will use.
    Strict: Best for casual players or those new to the AP implementation. Sticks close to the original level expectations.
    Loose: Recommended for veterans of the original. Won't expect anything too difficult, but may expect creative or unusual platforming or egg throws.
    Expert: Logic may expect advanced knowledge or memorization of level layouts, as well as jumps the player may only have one chance to make."""
    display_name = "Stage Logic"
    option_strict = 0
    option_loose = 1
    option_expert = 2
    #option_glitched = 3
    default = 1

class StartWithMidRings(Toggle):
    """Set this to start with Middle Rings/Checkpoints enabled by default."""
    display_name = "Start with Middle Rings"

class CastleOpenCon(Choice):
    """This will set the condition to open 6-8."""
    display_name = "6-8 Unlock"
    option_open = 0
    option_castles = 1
    option_bosses = 2
    #option_score = 3
    default = 1

class CastleDoor(Range):
    """This will set and force which of the 4 path"""
    display_name = "6-8 Door"
    range_start = 1
    range_end = 4
    default = 1
class CastleClearCon(Choice):
    """This will set the condition to open Bowser's boss door at the end of 6-8.
    This allows its goals to potentially be available earlier in logic."""
    display_name = "6-8 Clear Condition"
    option_open = 0
    option_castles = 1
    option_bosses = 2
    #option_score = 3
    default = 0

class FlagsForCastleOpen(Range):
    """This will set the minimum number of World Flags needed to open 6-8, if the 6-8 unlock is set to Castles."""
    display_name = "Flags Required for 6-8 Unlock"
    range_start = 1
    range_end = 5
    default = 3

class FlagsForCastleClear(Range):
    """This will set the minimum number of World Flags needed to beat 6-8, if the 6-8 clear condition is set to Castles."""
    display_name = "Flags Required for 6-8 Clear"
    range_start = 1
    range_end = 5
    default = 5

class BossesForCastleOpen(Range):
    """This will set the minimum number of bosses you need to defeat if the 6-8 goal is set to Bosses."""
    """You can check which bosses you must defeat in-game by pressing 'Select' in any level."""
    display_name = "Boss Required for 6-8 Unlock"
    range_start = 1
    range_end = 11
    default = 5

class ItemLogic(Toggle):
    """This will set logic to expect consumables to be used from the inventory in place of some standard objects.
    Logic will expect you to have access to an Overworld bonus game, or a bandit game to get the necessary items.
    Logic will NOT expect grinding end-of-level bonus games, or any inventory consumables received from checks."""
    display_name = "Items in Logic"

class MinigamesEnabled(Choice):
    """This will set minigame victories to give Archipelago checks.
    This will not randomize minigames amongst themselves, and is compatible with item logic.
    Bonus games will be expected to be cleared from the Overworld, not the end of levels.
    Additionally, 1-Up bonus games will accept any profit as a victory."""
    display_name = "Minigame Rewards in Pool"
    option_none = 0
    option_bandit_games = 1
    option_bonus_games = 2
    option_both = 3
    default = 0

class EggInventory(Range):
    """This sets the amount of eggs you can hold by default. Minimum is 1."""
    display_name = "Starting Egg Count"
    range_start = 1
    range_end = 6
    default = 1

class StartingWorld(Choice):
    """This sets the world you start in. Gates can be used to unlock other worlds.
    If the starting world was not 1, World 1 may appear visibile on the map, but still needs a Gate to be accessed."""
    display_name = "Starting World"
    option_world_1 = 0
    option_world_2 = 1
    option_world_3 = 2
    option_world_4 = 3
    option_world_5 = 4
    option_world_6 = 5
    default = 0

class StartingLives(Range):
    """This sets the amount of lives Yoshi will have upon loading the game."""
    display_name = "Starting Life Count"
    range_start = 1
    range_end = 255
    default = 3

yoshi_options: Dict[str, Option] ={
    "stage_logic": StageLogic,
    "item_logic": ItemLogic,
    "starting_world": StartingWorld,    
    "extras_enabled":  ExtrasEnabled,
    "minigames_enabled": MinigamesEnabled,
    "split_extra": SplitExtras,
    "split_bonus": SplitBonus,
    "start_with_middle_rings": StartWithMidRings,
    "starting_egg_capcity": EggInventory,
    "hidden_object_visibility": CoinVisibility,
    "castle_open_condition": CastleOpenCon,
    "castle_door_choice": CastleDoor,
    "castle_clear_condition": CastleClearCon,
    "flags_for_castle_open": FlagsForCastleOpen,
    "flags_for_castle_clear": FlagsForCastleClear,
    "bosses_for_unlock": BossesForCastleOpen,
    "yoshi_colors": YoshiColors,
    "starting_lives": StartingLives

    
}

def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(world, player, name) > 0


def get_option_value(world: MultiWorld, player: int, name: str) -> Union[int, dict]:
    option = getattr(world, name, None)
    if option == None:
        return 0

    return option[player].value