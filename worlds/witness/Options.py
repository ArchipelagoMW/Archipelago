from typing import Dict, Union
from BaseClasses import MultiWorld
from Options import Toggle, DefaultOnToggle, Option, Range, Choice


# class HardMode(Toggle):
#    "Play the randomizer in hardmode"
#    display_name = "Hard Mode"

# class UnlockSymbols(DefaultOnToggle):
#    "All Puzzle symbols of a specific panel need to be unlocked before the panel can be used"
#    display_name = "Unlock Symbols"

class DisableNonRandomizedPuzzles(DefaultOnToggle):
    """Disable puzzles that cannot be randomized.
    Non randomized puzzles are Shadows, Monastery, and Greenhouse.
    The lasers for those areas will be activated as you solve optional puzzles throughout the island."""
    display_name = "Disable non randomized puzzles"


class EarlySecretArea(Toggle):
    """The Mountainside shortcut to the Mountain Secret Area is open from the start.
    (Otherwise known as "UTM", "Caves" or the "Challenge Area")"""
    display_name = "Early Secret Area"


class ShuffleSymbols(DefaultOnToggle):
    """You will need to unlock puzzle symbols as items to be able to solve the panels that contain those symbols."""
    display_name = "Shuffle Symbols"


class ShuffleDoors(Toggle):
    """Many doors around the island will have their panels turned off initially.
    You will need to find the items that power the panels to open those doors."""
    display_name = "Shuffle Doors"


class ShuffleDiscardedPanels(Toggle):
    """Discarded Panels will have items on them.
    Solving certain Discarded Panels may still be necessary!"""
    display_name = "Shuffle Discarded Panels"


class ShuffleVaultBoxes(Toggle):
    """Vault Boxes will have items on them."""
    display_name = "Shuffle Vault Boxes"


class ShuffleUncommonLocations(Toggle):
    """Adds some optional puzzles that are somewhat difficult or out of the way.
    Examples: Mountaintop River Shape, Tutorial Patio Floor, Theater Videos"""
    display_name = "Shuffle Uncommon Locations"


class ShuffleHardLocations(Toggle):
    """Adds some harder locations into the game, e.g. Mountain Secret Area panels"""
    display_name = "Shuffle Hard Locations"


class VictoryCondition(Choice):
    """Change the victory condition from the original game's ending (elevator) to beating the Challenge
    or solving the mountaintop box, either using the short solution
    (7 lasers or whatever you've changed it to) or the long solution (11 lasers or whatever you've changed it to)."""
    display_name = "Victory Condition"
    option_elevator = 0
    option_challenge = 1
    option_mountain_box_short = 2
    option_mountain_box_long = 3


class MountainLasers(Range):
    """Sets the amount of beams required to enter the final area."""
    display_name = "Required Lasers for Mountain Entry"
    range_start = 1
    range_end = 7
    default = 7


class ChallengeLasers(Range):
    """Sets the amount of beams required to enter the secret area through the Mountain Bottom Layer Discard."""
    display_name = "Required Lasers for Challenge"
    range_start = 1
    range_end = 11
    default = 11


class TrapPercentage(Range):
    """Replaces junk items with traps, at the specified rate."""
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 20


class PuzzleSkipAmount(Range):
    """Adds this number of Puzzle Skips into the pool, if there is room. Puzzle Skips let you skip one panel.
    Works on most panels in the game - The only big exception is The Challenge."""
    display_name = "Puzzle Skips"
    range_start = 0
    range_end = 20
    default = 5


the_witness_options: Dict[str, type] = {
    # "hard_mode": HardMode,
    "disable_non_randomized_puzzles": DisableNonRandomizedPuzzles,
    "shuffle_discarded_panels": ShuffleDiscardedPanels,
    "shuffle_vault_boxes": ShuffleVaultBoxes,
    "shuffle_uncommon": ShuffleUncommonLocations,
    "shuffle_hard": ShuffleHardLocations,
    "victory_condition": VictoryCondition,
    "trap_percentage": TrapPercentage,
    "early_secret_area": EarlySecretArea,
    # "shuffle_symbols": ShuffleSymbols,
    # "shuffle_doors": ShuffleDoors,
    "mountain_lasers": MountainLasers,
    "challenge_lasers": ChallengeLasers,
    "puzzle_skip_amount": PuzzleSkipAmount,
}


def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(world, player, name) > 0


def get_option_value(world: MultiWorld, player: int, name: str) -> Union[bool, int]:
    option = getattr(world, name, None)

    if option is None:
        return 0

    if issubclass(the_witness_options[name], Toggle) or issubclass(the_witness_options[name], DefaultOnToggle):
        return bool(option[player].value)
    return option[player].value
