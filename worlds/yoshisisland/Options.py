from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, PerGameCommonOptions


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
    Strict Logic will expect the Secret Lens or a Magnifying Glass to interact with hidden clouds containing stars if they are not set to visible by default."""
    display_name = "Hidden Object Visibility"
    option_none = 0
    option_coins_only = 1
    option_clouds_only = 2
    option_full = 3
    default = 1


class SoftlockPrevention(DefaultOnToggle):
    """If enabled, hold R + X to warp to the last used Middle Ring, or the start of the level if none have been activated."""
    display_name = "Softlock Prevention Code"


class StageLogic(Choice):
    """This determines what logic mode the stages will use.
    Strict: Best for casual players or those new to playing Yoshi's Island in AP. Level requirements won't expect anything too difficult of the player.
    Loose: Recommended for veterans of the original game. Won't expect anything too difficult, but may expect unusual platforming or egg throws.
    Expert: Logic may expect advanced knowledge or memorization of level layouts, as well as jumps the player may only have one chance to make without restarting."""
    display_name = "Stage Logic"
    option_strict = 0
    option_loose = 1
    option_expert = 2
    # option_glitched = 3
    default = 0


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
    Logic will NOT expect grinding end-of-level bonus games, or any inventory consumables received from checks.
    Casual logic will only expect consumables from Overworld games; Loose and Expert may expect them from bandit games."""
    display_name = "Consumable Logic"


class MinigameChecks(Choice):
    """This will set minigame victories to give Archipelago checks.
    This will not randomize minigames amongst themselves, and is compatible with item logic.
    Bonus games will be expected to be cleared from the Overworld, not the end of levels.
    Additionally, 1-Up bonus games will accept any profit as a victory."""
    display_name = "Minigame Reward Checks"
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


class PlayerGoal(Choice):
    """This sets the goal. Bowser goal requires defeating Bowser at the end of 6-8, while Luigi Hunt requires collecting all required Luigi Pieces."""
    display_name = "Goal"
    option_bowser = 0
    option_luigi_hunt = 1
    default = 0


class LuigiPiecesReq(Range):
    """This will set how many Luigi Pieces are required to trigger a victory."""
    display_name = "Luigi Pieces Required"
    range_start = 1
    range_end = 100
    default = 25


class LuigiPiecesAmt(Range):
    """This will set how many Luigi Pieces are in the item pool.
       If the number in the pool is lower than the number required,
       the amount in the pool will be randomized, with the minimum being the amount required."""
    display_name = "Amount of Luigi Pieces"
    range_start = 1
    range_end = 100
    default = 50


class FinalLevelBosses(Range):
    """This sets how many bosses need to be defeated to access 6-8.
       You can check this in-game by pressing SELECT while in any level."""
    display_name = "Bosses Required for 6-8 Unlock"
    range_start = 0
    range_end = 11
    default = 5


class FinalBossBosses(Range):
    """This sets how many bosses need to be defeated to access the boss of 6-8.
       You can check this in-game by pressing SELECT while in any level."""
    display_name = "Bosses Required for 6-8 Clear"
    range_start = 0
    range_end = 11
    default = 0


class BowserDoor(Choice):
    """This will set which route you take through 6-8.
    Manual: You go through the door that you hit with an egg, as normal.
    Doors: Route will be forced to be the door chosen here, regardless of which door you hit.
    Gauntlet: You will be forced to go through all 4 routes in order before the final hallway."""
    display_name = "Bowser's Castle Doors"
    option_manual = 0
    option_door_1 = 1
    option_door_2 = 2
    option_door_3 = 3
    option_door_4 = 4
    option_gauntlet = 5
    default = 0


class BossShuffle(Toggle):
    """This whill shuffle which boss each boss door will lead to. Each boss can only appear once, and Baby Bowser is left alone."""
    display_name = "Boss Shuffle"


class LevelShuffle(Choice):
    """Disabled: All levels will appear in their normal location.
    Bosses Guaranteed: All worlds will have a boss on -4 and -8.
    Full: Worlds may have more than 2 or no bosses in them.
    Regardless of the setting, 6-8 and Extra stages are not shuffled."""
    display_name = "Level Shuffle"
    option_disabled = 0
    option_bosses_guaranteed = 1
    option_full = 2
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
    option_cyan = 3
    option_yellow = 2
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
    """Will place traps into the item pool.
       Traps have a variety of negative effects, and will only replace filler items."""
    display_name = "Traps Enabled"


class TrapPercent(Range):
    """Percentage of the item pool that becomes replaced with traps."""
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 10

# class EnableScrets(Range):
    # """This sets the amount of lives Yoshi will have upon loading the game."""
    # display_name = "Starting Life Count"
    # range_start = 1
    # range_end = 255
    # default = 3

# class BackgroundColors(Range):
    # """This sets the amount of lives Yoshi will have upon loading the game."""
    # display_name = "Starting Life Count"
    # range_start = 1
    # range_end = 255
    # default = 3

# class Foreground Colors(Range):
    # """This sets the amount of lives Yoshi will have upon loading the game."""
    # display_name = "Starting Life Count"
    # range_start = 1
    # range_end = 255
    # default = 3

# class Music Shuffle(Range):
    # """This sets the amount of lives Yoshi will have upon loading the game."""
    # display_name = "Starting Life Count"
    # range_start = 1
    # range_end = 255
    # default = 3

# class Star Loss Rate(Range):
    # """This sets the amount of lives Yoshi will have upon loading the game."""
    # display_name = "Starting Life Count"
    # range_start = 1
    # range_end = 255
    # default = 3


@dataclass
class YoshisIslandOptions(PerGameCommonOptions):
    starting_world: StartingWorld
    starting_lives: StartingLives
    goal: PlayerGoal
    luigi_pieces_required: LuigiPiecesReq
    luigi_pieces_in_pool: LuigiPiecesAmt
    extras_enabled:  ExtrasEnabled
    minigame_checks: MinigameChecks
    split_extras: SplitExtras
    split_bonus: SplitBonus
    hidden_object_visibility: ObjectVis
    add_secretlens: ShuffleSecretLens
    shuffle_midrings: ShuffleMiddleRings
    stage_logic: StageLogic
    item_logic: ItemLogic
    disable_autoscroll: DisableAutoScrollers
    softlock_prevention: SoftlockPrevention
    castle_open_condition: FinalLevelBosses
    castle_clear_condition: FinalBossBosses
    bowser_door_mode: BowserDoor
    level_shuffle: LevelShuffle
    boss_shuffle: BossShuffle
    yoshi_colors: YoshiColors
    yoshi_singularity_color: SinguColor
    baby_mario_sound: BabySound
    traps_enabled: TrapsEnabled
    trap_percent: TrapPercent
    death_link: DeathLink
