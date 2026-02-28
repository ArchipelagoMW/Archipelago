"""Options for MN64."""

import numbers
import typing
from dataclasses import dataclass
from typing import List

from BaseClasses import PlandoOptions
from worlds.AutoWorld import World

from Options import Choice, DeathLink, DefaultOnToggle, Option, OptionDict, OptionError, OptionGroup, OptionList, PerGameCommonOptions, Range, TextChoice, Toggle


class StartingRoomRando(DefaultOnToggle):
    """Determines if the starting spawn is randomized."""

    display_name = "Starting Room Rando"


class EnemyRando(DefaultOnToggle):
    """Determines if enemies are randomized."""

    display_name = "Enemy Rando"


class IncreasedPotRyo(DefaultOnToggle):
    """Determines if pots have an increased amount of ryo."""

    display_name = "Increase Pot Ryo"


class PotRando(Toggle):
    """Determines if pot locations are randomized."""

    display_name = "Pot Rando"


class HealthInPool(DefaultOnToggle):
    """Determines if Health Items are added into the pool."""

    display_name = "Health In Pool"


class RyoInPool(Toggle):
    """Determines if Ryo Items are added into the pool."""

    display_name = "Ryo In Pool"


class PreventOneWaySoftlocks(DefaultOnToggle):
    """Entrances that are normally one-way are now two-way."""

    display_name = "Prevent One-Way Softlocks"


class ChugokuDoorUnlocked(DefaultOnToggle):
    """Determines if the Chugoku door starts unlocked."""

    display_name = "Chugoku Door Unlocked"


class PreUnlockedWarps(Toggle):
    """Pre-unlock all flute warp destinations. You still need to get the flute and Yae to warp."""

    display_name = "Pre-Unlocked Warps"


class MusicRando(Choice):
    """Determines if and how music tracks are randomized.

    - Off: No music randomization
    - On: Full music randomization
    - On with Area Music: Music randomization with area-specific handling
    """

    display_name = "Music Rando"
    option_off = 0
    option_on = 1
    option_on_with_area_music = 2
    default = 0


class MajorHintCount(Range):
    """Number of hints for progression items in the player's world."""

    display_name = "Major Item Hint Count"
    range_start = 0
    range_end = 10
    default = 3


class LocationHintCount(Range):
    """Number of hints for tedious locations in the player's world."""

    display_name = "Location Hint Count"
    range_start = 0
    range_end = 10
    default = 5


class FastText(DefaultOnToggle):
    """Make text appear instantly instead of being typed out character by character."""

    display_name = "Fast Text"


class KeepIntroCutscene(Toggle):
    """Keep the intro cutscene at the start of the game."""

    display_name = "Keep Intro Cutscene"


@dataclass
class MN64Options(PerGameCommonOptions):
    """Options for MN64"""

    enemy_rando: EnemyRando
    starting_room_rando: StartingRoomRando
    increase_pot_ryo: IncreasedPotRyo
    pot_rando: PotRando
    randomize_health: HealthInPool
    randomize_ryo: RyoInPool
    prevent_oneway_softlocks: PreventOneWaySoftlocks
    chugoku_door_unlocked: ChugokuDoorUnlocked
    pre_unlocked_warps: PreUnlockedWarps
    music_rando: MusicRando
    major_hint_count: MajorHintCount
    location_hint_count: LocationHintCount
    fast_text: FastText
    keep_intro_cutscene: KeepIntroCutscene
    death_link: DeathLink
