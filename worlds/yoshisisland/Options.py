from typing import Dict, Union
from BaseClasses import MultiWorld
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, Option, OptionDict
from schema import Schema, And, Optional

class ExtrasEnabled(Toggle):
    """If enabled, the more difficult Extra stages will be added into logic. Otherwise, they will be inaccessible."""
    display_name = "Include Extra Stages"

class SplitExtras(Toggle):
    """If enabled, Extra stages will be unlocked individually. Otherwise, there will be a single 'Extra Panels' item that unlocks all of them."""
    display_name = "Split Extra Stages"

class SplitBonus(Toggle):
    """If enabled, Bonus Games will be unlocked individually. Otherwise, there will be a single 'Bonus Panels' item that unlocks all of them."""
    display_name = "Split Bonus Games"

class ObjectVis(Choice):
    """This will determine the default visibility of objects revealed by the Magnifying Glass.
    Strict Logic will expect the Secret Lens or a Magnifying Glass to interact with hidden clouds if they are not set to visible by default."""
    display_name = "Hidden Object Visibility"
    option_none = 0
    option_coins_only = 1
    option_clouds_only = 2
    option_full = 3
    default = 1

class SoftlockPrevention(DefaultOnToggle):
    """If enabled, holding R + X to warp to the last used Middle Ring, or the start of the level if none have been activated."""
    display_name = "Softlock Prevention Code"

class StageLogic(Choice):
    """This determines what logic mode the stages will use.
    Strict: Best for casual players or those new to the AP implementation. Requirements won't be too demanding.
    Loose: Recommended for veterans of the original. Won't expect anything too difficult, but may expect unusual platforming or egg throws.
    Expert: Logic may expect advanced knowledge or memorization of level layouts, as well as jumps the player may only have one chance to make without restarting."""
    display_name = "Stage Logic"
    option_strict = 0
    option_loose = 1
    option_expert = 2
    #option_glitched = 3
    default = 1

class ShuffleMiddleRings(Toggle):
    """If enabled, Middle Rings will be added to the item pool."""
    display_name = "Shuffle Middle Rings"

class ShuffleSecretLens(Toggle):
    """If enabled, the Secret Lens will be added to the item pool.
    The Secret Lens will act as a permanent Magnifying Glass."""
    display_name = "Add Secret Lens"

class DisableAutoScrollers(Toggle):
    """If enabled, will disable autoscrolling during levels, except during levels which cannot function otherwise."""
    display_name = "Disable Autoscrolling"

class ItemLogic(Toggle):
    """This will enable logic to expect consumables to be used from the inventory in place of some major items.
    Logic will expect you to have access to an Overworld bonus game, or a bandit game to get the necessary items.
    Logic will NOT expect grinding end-of-level bonus games, or any inventory consumables received from checks."""
    display_name = "Items in Logic"

class MinigameChecks(Choice):
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

class StartingWorld(Choice):
    """This sets which world you start in. Other worlds can be accessed by receiving a Gate respective to that world."""
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
    range_end = 999
    default = 3

class FinalLevelBosses(Range):
    """This sets how many bosses need to be defeated to access 6-8. You can check this in-game by pressing SELECT while in any level."""
    display_name = "Boss Required for 6-8 Unlock"
    range_start = 0
    range_end = 11
    default = 5

class FinalBossBosses(Range):
    """This sets how many bosses need to be defeated to access the boss of 6-8. You can check this in-game by pressing SELECT while in any level."""
    display_name = "Boss Required for 6-8 Clear"
    range_start = 0
    range_end = 11
    default = 0

class BossShuffle(Choice):
    """This will randomize which boss room each boss door connects to. Baby Bowser will only appear in 6-8, and no other boss can appear there.
        Normal: All bosses will be in their normal level.
        Shuffled: Bosses will be shuffled amongst each other, with each guranteed to appear once.
        Randomized: Bosses will be shuffled, possibly duplicating bosses.
        Singularity: All bosses will be replaced with the same boss."""
    display_name = "Boss Randomization"
    option_none = 0
    option_shuffled = 1
    option_randomized = 2
    option_singularity = 3
    default = 0

class YoshiColors(Choice):
    """Sets the Yoshi color for each level.
    Normal will use the vanilla colors.
    Random order will generate a random order of colors that will be used in each level. The stage 1 color will be used for Extra stages, and 6-8.
    Random color will generate a random color for each stage.
    Singularity will use a single color defined under 'Singularity Yoshi Color' for use in all stages."""
    display_name = "Yoshi Colors"
    option_normal = 0
    option_random_order = 1
    option_random_color = 2
    option_singularity = 3
    default = 0

class SinguColor(Choice):
    """Sets which color Yoshi will be if Yoshi Colors is set to singularity."""
    display_name = "Singularity Yoshi Color"
    option_green = 0
    option_pink = 1
    option_cyan = 2
    option_yellow = 3
    option_purple = 4
    option_brown = 5
    option_red = 6
    option_blue = 7
    default = 0

class BabySound(Choice):
    """Change the sound that Baby Mario makes when not on Yoshi."""
    display_name = "Mario Sound Effect"
    option_normal = 0
    option_disabled = 1
    option_random_sound_effect = 2
    default = 0

class TrapsEnabled(Toggle):
    """Will place traps into the item pool. Traps have a variety of negative effects, and will only replace filler items."""
    display_name = "Traps Enabled"

class TrapPercent(Range):
    """Percentage of the item pool that becomes replaced with traps."""
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 10

#class EnableScrets(Range):
 #   """This sets the amount of lives Yoshi will have upon loading the game."""
  #  display_name = "Starting Life Count"
   # range_start = 1
    #range_end = 255
    #default = 3



yoshi_options: Dict[str, Option] ={
    "starting_world": StartingWorld,
    "starting_lives": StartingLives,
    "extras_enabled":  ExtrasEnabled,
    "minigame_checks": MinigameChecks,
    "split_extras": SplitExtras,
    "split_bonus": SplitBonus,
    "hidden_object_visibility": ObjectVis,
    "add_secretlens": ShuffleSecretLens,
    "shuffle_midrings": ShuffleMiddleRings,
    "stage_logic": StageLogic,
    "item_logic": ItemLogic,
    "disable_autoscroll": DisableAutoScrollers,
    "softlock_prevention": SoftlockPrevention,
    "castle_open_condition": FinalLevelBosses,
    "castle_clear_condition": FinalBossBosses,
    "boss_randomizer": BossShuffle,
    "yoshi_colors": YoshiColors,
    "yoshi_singularity_color": SinguColor,
    "baby_mario_sound": BabySound,
    "traps_enabled": TrapsEnabled,
    "trap_percent": TrapPercent,
    "death_link": DeathLink

    
}

def get_option_value(world: MultiWorld, player: int, name: str) -> Union[int, dict]:
    option = getattr(world, name, None)
    if option == None:
        return 0

    return option[player].value