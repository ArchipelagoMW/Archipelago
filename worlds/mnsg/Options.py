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


class HealthInPool(DefaultOnToggle):
    """Determines if Health Items are added into the pool."""

    display_name = "Health In Pool"


class PreventOneWaySoftlocks(DefaultOnToggle):
    """Entrances that are normally one-way are now two-way."""

    display_name = "Prevent One-Way Softlocks"


class ChugokuDoorUnlocked(DefaultOnToggle):
    """Determines if the Chugoku door starts unlocked."""

    display_name = "Chugoku Door Unlocked"


class PreUnlockedWarps(Toggle):
    """Pre-unlock all flute warp destinations. You still need to get the flute and Yae to warp."""

    display_name = "Pre-Unlocked Warps"


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


@dataclass
class MN64Options(PerGameCommonOptions):
    """Options for MN64"""

    enemy_rando: EnemyRando
    starting_room_rando: StartingRoomRando
    increase_pot_ryo: IncreasedPotRyo
    randomize_health: HealthInPool
    prevent_oneway_softlocks: PreventOneWaySoftlocks
    chugoku_door_unlocked: ChugokuDoorUnlocked
    pre_unlocked_warps: PreUnlockedWarps
    major_hint_count: MajorHintCount
    location_hint_count: LocationHintCount
    death_link: DeathLink
