from typing import Dict, FrozenSet, Union
from Options import Choice, Option, DefaultOnToggle
from BaseClasses import MultiWorld


class LobbyAccess(Choice):
    """Chooses how keys needed to reach the lobby are placed.
    - Normal: Keys are placed anywhere
    - Early: Keys are placed early 
    - Local: Keys are placed locally"""
    display_name = "Lobby Access"
    option_normal = 0
    option_early = 1
    option_local = 2

class PuzzleHintsRequired(DefaultOnToggle):
    """If turned on puzzle hints will be available before the corresponding puzzle is required. For example: The Tiki
    Drums puzzle will be placed after access to the security cameras which give you the solution. Turning this off
    allows for greater randomization."""
    display_name = "Puzzle Hints Required"

Shivers_options: Dict[str, Option] = {
    "lobby_access": LobbyAccess,

    "puzzle_hints_required": PuzzleHintsRequired
}

def get_option_value(multiworld: MultiWorld, player: int, name: str) -> Union[int,  FrozenSet]:
    if multiworld is None:
        return Shivers_options[name].default

    player_option = getattr(multiworld, name)[player]

    return player_option.value