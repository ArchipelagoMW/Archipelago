# id1Common - Common library for Doom/Heretic/derived games in Archipelago
#
# This file is copyright (C) Kay "Kaito" Sinclaire,
# and is released under the terms of the zlib license.
# See "LICENSE" for more details
#
# Brief:
#   Options common to all id1 games.

# Options docstrings may exceed the line length limit.
# ruff: noqa: E501

import random
from dataclasses import dataclass
from typing import ClassVar

from Options import (
    Choice,
    DeathLink,
    DefaultOnToggle,
    FreeText,
    PerGameCommonOptions,
    Range,
    StartInventoryPool,
    Toggle,
)


class Placeholder(FreeText):
    """Used to designated an option class that is expected to exist but is not provided.
    Unconditionally errors if left in place.
    """
    def __init__(self, value: str):
        raise Exception("Placeholder option was not overridden.\n"
                        "This is an error with the world, not the yaml.")


class BoundedRandomRange(Range):
    """Used to provide a Range option with a more tightly bounded random than what the ranges actually allow."""
    random_start: ClassVar[int | None] = None
    random_end: ClassVar[int | None] = None

    @classmethod
    def weighted_range(cls, text) -> Range:
        range_min = cls.range_start if cls.random_start is None else max(cls.range_start, cls.random_start)
        range_max = cls.range_end if cls.random_end is None else min(cls.range_end, cls.random_end)

        if text == "random-low":
            return cls(cls.triangular(range_min, range_max, 0.0))
        if text == "random-high":
            return cls(cls.triangular(range_min, range_max, 1.0))
        if text == "random-middle":
            return cls(cls.triangular(range_min, range_max))
        if text.startswith("random-range-"):
            return cls.custom_range(text)
        if text == "random":
            return cls(random.randint(range_min, range_max))
        raise Exception(f'random text "{text}" did not resolve to a recognized pattern. '
                        f'Acceptable values are: random, random-high, random-middle, random-low, '
                        f'random-range-low-<min>-<max>, random-range-middle-<min>-<max>, '
                        f'random-range-high-<min>-<max>, or random-range-<min>-<max>.')


####################
# Standard options #
####################
# There shouldn't be a need to ever extend these options, just use them as is.

class Goal(Choice):
    """Choose the goal of the game.

    - **Complete All Levels**: Complete every level to win.
    - **Complete Some Levels**: Complete some number of total levels to win.
    - **Complete Random Levels**: Complete a set of randomly chosen levels to win.
    - **Complete Specific Levels**: Complete a specific set of levels to win.
    """
    display_name = "Goal"
    option_complete_all_levels = 0
    option_complete_some_levels = 1
    option_complete_random_levels = 2
    option_complete_specific_levels = 3
    default = 0


class RandomMonsters(Choice):
    """Choose how monsters are randomized.

    - **Off**: Monsters are left unchanged.
    - **Shuffle**: Monsters in the level are shuffled around.
    - **Same Type**: Each "small" monster in the level is replaced with a different "small" monster; same for "medium" and "big" monsters.
    - **Balanced**: All monsters in the level are randomized. The ratio of "small", "medium", and "big" monsters in the level will be preserved.
    - **Chaotic**: All monsters in the level are completely randomized. This can make levels *significantly* harder!
    """
    display_name = "Random Monsters"
    option_off = 0
    option_shuffle = 1
    option_same_type = 2
    option_balanced = 3
    option_chaotic = 4
    alias_vanilla = 0
    alias_random_balanced = 3
    alias_random_chaotic = 4
    default = 0


class RandomPickups(Choice):
    """Choose how pickups (medkits, ammo, etc.) are randomized.

    - **Off**: Pickups are left unchanged.
    - **Shuffle**: Pickups in the level are shuffled around.
    - **Same Type**: Each "small" pickup in the level is replaced with a different "small" pickup; same for "medium" and "big" pickups.
    - **Balanced**: All pickups in the level are randomized. The ratio of "small", "medium", and "big" pickups in the level will be preserved.
    - **Chaotic**: All pickups in the level are completely randomized.
    """
    display_name = "Random Pickups"
    option_off = 0
    option_shuffle = 1
    option_same_type = 2
    option_balanced = 3
    option_chaotic = 4
    alias_vanilla = 0
    alias_random_balanced = 3
    alias_random_chaotic = 4
    default = 0


class RandomMusic(Choice):
    """Choose how music will be randomized.

    - **Off**: The music tracks will be left unchanged.
    - **Shuffle Selected**: All music tracks within the episodes you have selected will be shuffled together.
    - **Shuffle Game**: All music in the entire game will be shuffled together.
    """
    display_name = "Random Music"
    option_off = 0
    option_shuffle_selected = 1
    option_shuffle_game = 2
    alias_vanilla = 0
    default = 0


class FlipLevels(Choice):
    """Choose if levels should be randomly flipped (mirrored).

    - **Off**: Levels won't be flipped.
    - **On**: All levels will be flipped.
    - **Random Mix**: Each level has a random chance of being flipped.
    """
    display_name = "Flip Levels"
    option_off = 0
    option_on = 1
    option_random_mix = 2
    alias_vanilla = 0
    alias_flipped = 1
    alias_randomly_flipped = 2
    default = 0


class AllowDeathLogic(Toggle):
    """Allow or disallow death logic locations and tricks.

    Some locations can only be attempted once, and can become unreachable if the player fails to get them. Once this has happened, the player must die or otherwise reset the level to attempt to reach the location again.
    If death logic is disabled, these locations will never contain any progression items.

    On higher trick difficulty settings, this setting may also enable some tricks that put the player in a position where they are stuck and must die/reset the map afterwards.
    """
    display_name = "Allow Death Logic"


class TrickDifficulty(Choice):
    """Choose which tricks, if any, can be logically expected.

    - **None**: Assumes vanilla progression through levels.
    - **Basic**: Some minor unintended strategies may be required.
    - **Pro**: More advanced speedrunning strategies like wallruns, SR40/SR50 straferunning, and exploiting the Z axis may be required.
    - **Extreme**: If it's feasible in real time, it's in logic. Includes tricks that require enabling vertical mouse movement, tricks that punish failure with death, or out-of-bounds movement.
    """
    display_name = "Trick Difficulty"
    option_none = 0
    option_basic = 1
    option_pro = 2
    option_extreme = 3
    default = 0


class ResetLevelOnDeath(DefaultOnToggle):
    """If enabled, when the player dies, the level is reset, respawning all pickups and monsters.

    Turning this setting off is considered easy mode. Good for new players that don't know the levels well.
    Note that regardless of this setting, your inventory and checks made are never lost on death.
    """
    display_name = "Reset Level on Death"


class CheckSanity(Toggle):
    """If enabled, restores redundant location checks that are normally removed.

    By default, to lower the location count slightly, some redundant locations are removed.
    For example, in a room with three items right next to each other, two might be removed.
    Enabling Check Sanity restores these locations.
    """
    display_name = "Check Sanity"


######################
# Difficulty options #
######################
# Pick one based on what's appropriate for your game, and assign it to 'difficulty'.
# If the game changes the name for skill levels, feel free to make a new Choice option instead.

class DifficultyDoom(Choice):
    """Choose the game difficulty (skill level).

    - **Baby**: (I'm too young to die.) - Damage taken is halved. Ammo received from pickups is doubled.
    - **Easy**: (Hey, not too rough.) - Lesser number or strength of monsters, and more pickups.
    - **Medium**: (Hurt me plenty.) - The default skill. Balanced monsters and pickups.
    - **Hard**: (Ultra-Violence.) - Greater number or strength of monsters, and less pickups.
    - **Nightmare**: (Nightmare!) - Monsters are faster, more aggressive, and respawn.
    """
    display_name = "Difficulty"
    skill_5_warning = "Are you sure? This skill level isn't even remotely fair."
    option_baby = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_nightmare = 4
    alias_itytd = 0
    alias_hntr = 1
    alias_hmp = 2
    alias_uv = 3
    alias_nm = 4
    default = 2


class DifficultyHeretic(Choice):
    """Choose the game difficulty (skill level).

    - **Wet nurse**: (Thou needeth a wet-nurse) - Damage taken is halved. Ammo received from pickups is doubled. Quartz Flasks and Mystic Urns are automatically used when the player nears death.
    - **Easy**: (Yellowbellies-r-us) - Lesser number or strength of monsters, and more pickups.
    - **Medium**: (Bringest them oneth) - The default skill. Balanced monsters and pickups.
    - **Hard**: (Thou art a smite-meister) - Greater number or strength of monsters, and less pickups.
    - **Black plague**: (Black plague possesses thee) - Monsters are faster and more aggressive.
    """
    display_name = "Difficulty"
    option_wet_nurse = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_black_plague = 4
    alias_wn = 0
    alias_yru = 1
    alias_bto = 2
    alias_sm = 3
    alias_bp = 4
    default = 2


###################
# Episode options #
###################
# Extend these options to create your episode list.

class Episode(Toggle):
    """This is an example episode that is disabled by default.

    This episode contains the following maps:

    (list)
    """
    is_major_episode = True

    @property
    def is_minor_episode(self):
        return not self.is_major_episode


class MinorEpisode(Episode):
    """This is an example episode that is disabled by default.

    This is a minor episode. Another episode must be played alongside this one.
    This episode contains the following maps:

    (list)
    """
    is_major_episode = False


class DefaultEpisode(Episode):
    """This is an example episode that is enabled by default.

    This episode contains the following maps:

    (list)
    """
    is_major_episode = True
    default = 1


class MinorDefaultEpisode(Episode):
    """This is an example episode that is enabled by default.

    This is a minor episode. Another episode must be played alongside this one.
    This episode contains the following maps:

    (list)
    """
    is_major_episode = False
    default = 1


########################
# Item-centric options #
########################
# Item-centric options have a doom_type for the code to reference.

class PartialInvisibilityAsTrap(Toggle):
    """If enabled, Partial invisibility will be classified as a trap, rather than just filler.
    This does not change how the item behaves, only how Archipelago sees it.
    """
    display_name = "Partial Invisibility as Trap"
    doom_type = 2024


class StartWithComputerAreaMaps(Toggle):
    """If enabled, all Computer Area Maps will be given to the player from the start."""
    display_name = "Start With Computer Area Maps"
    doom_type = 2026


class StartWithMapScrolls(StartWithComputerAreaMaps):
    """If enabled, all Map Scrolls will be given to the player from the start."""
    display_name = "Start With Map Scrolls"
    doom_type = 35


class SplitBackpack(Toggle):
    """Split the Backpack into four individual items, each one increasing ammo capacity for one type of weapon only."""
    display_name = "Split Backpack"
    split_doom_types: tuple[int, ...] = (65001, 65002, 65003, 65004)
    doom_type = 8


class SplitBagOfHolding(SplitBackpack):
    """Split the Bag of Holding into six individual items, each one increasing ammo capacity for one type of weapon only."""
    display_name = "Split Bag of Holding"
    split_doom_types = (65001, 65002, 65003, 65004, 65005, 65006)


#################
# Other options #
#################

class BackpackCount(Range):
    """How many Backpacks will be available.
    If Split Backpack is set, this will be the number of each capacity upgrade available."""
    display_name = "Backpack Count"
    range_start = 0
    range_end = 10
    default = 1


class BagOfHoldingCount(BackpackCount):
    """How many Bags of Holding will be available.
    If Split Bag of Holding is set, this will be the number of each capacity upgrade available."""
    display_name = "Bag of Holding Count"


@dataclass
class id1CommonOptions(PerGameCommonOptions):  # noqa: N801
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink

    # Global goal settings
    goal: Goal
    goal_num_levels: Placeholder  # Must exist for above Goal option
    goal_specific_levels: Placeholder  # Must exist for above Goal option

    # Global game difficulty and randomizer settings
    difficulty: DifficultyDoom  # Must exist, though should be overridden
    reset_level_on_death: ResetLevelOnDeath
    random_monsters: RandomMonsters
    random_pickups: RandomPickups
    random_music: RandomMusic
    flip_levels: FlipLevels

    # Global trick settings
    allow_death_logic: AllowDeathLogic
    trick_difficulty: TrickDifficulty
