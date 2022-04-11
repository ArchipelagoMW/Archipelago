from typing import Dict
from BaseClasses import MultiWorld
from Options import Toggle, DefaultOnToggle, Option

#class HardMode(Toggle):
#    "Play the randomizer in hardmode"
#    display_name = "Hard Mode"

class UnlockSymbols(DefaultOnToggle):
    "All Puzzle symbols of a specific panel need to be unlocked before the panel can be used"
    display_name = "Unlock Symbols"

class DisableNonRandomizedPuzzles(DefaultOnToggle):
    """Disable puzzles that cannot be randomized.
    Non randomized puzzles are Shadows, Monastery, and Greenhouse.
    The lasers for those areas will be activated as you solve optional puzzles throughout the island."""
    display_name = "Disable non randomized puzzles"

the_witness_options: Dict[str, Option] = {
    #"hard_mode": HardMode,
    "unlock_symbols": UnlockSymbols,
    "disable_non_randomized_puzzles": DisableNonRandomizedPuzzles,
}

def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(world, player, name) > 0

def get_option_value(world: MultiWorld, player: int, name: str) -> int:
    option = getattr(world, name, None)

    if option == None:
        return 0

    return int(option[player].value)