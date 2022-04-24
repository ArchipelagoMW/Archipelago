from typing import Dict
from BaseClasses import MultiWorld
from Options import Toggle, DefaultOnToggle, Option

#class HardMode(Toggle):
#    "Play the randomizer in hardmode"
#    display_name = "Hard Mode"

#class UnlockSymbols(DefaultOnToggle):
#    "All Puzzle symbols of a specific panel need to be unlocked before the panel can be used"
#    display_name = "Unlock Symbols"

class DisableNonRandomizedPuzzles(DefaultOnToggle):
    """Disable puzzles that cannot be randomized.
    Non randomized puzzles are Shadows, Monastery, and Greenhouse.
    The lasers for those areas will be activated as you solve optional puzzles throughout the island."""
    display_name = "Disable non randomized puzzles"

class ShuffleDiscardedPanels(Toggle):
    """Discarded Panels will have items on them.
    Solving certain Discarded Panels may still be necessary!"""
    display_name = "Shuffle Discarded Panels"

class ShuffleVaultBoxes(Toggle):
    """Vault Boxes will have items on them."""
    display_name = "Shuffle Vault Boxes"

class ShuffleUncommonLocations(Toggle):
    """Adds the following checks to the pool:
    Mountaintop River Shape, Tutorial Patio Floor, Theater Videos"""
    display_name = "Shuffle Uncommon Locations"

class ShuffleHardLocations(Toggle):
    """Adds some harder locations into the game, e.g. Mountain Secret Area panels"""
    display_name = "Shuffle Hard Locations"

class ChallengeVictoryCondition(Toggle):
    """The victory condition now becomes beating the Challenge area,
    instead of the final elevator."""

    display_name = "Victory on beating the Challenge"

the_witness_options: Dict[str, Option] = {
    # "hard_mode": HardMode,
    # "unlock_symbols": UnlockSymbols,
    "disable_non_randomized_puzzles": DisableNonRandomizedPuzzles,
    "shuffle_discarded_panels": ShuffleDiscardedPanels,
    "shuffle_vault_boxes": ShuffleVaultBoxes,
    "shuffle_uncommon": ShuffleUncommonLocations,
    "shuffle_hard": ShuffleHardLocations,
    "challenge_victory": ChallengeVictoryCondition
}

def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(world, player, name) > 0

def get_option_value(world: MultiWorld, player: int, name: str) -> int:
    option = getattr(world, name, None)

    if option == None:
        return 0

    return int(option[player].value)