from typing import Dict, FrozenSet, Union
from Options import Choice, Option, DefaultOnToggle, Toggle
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

class InformationPlaques(Toggle):
    """Adds Information Plaques as checks."""
    display_name = "Include Information Plaques"

class FrontDoorUsable(Toggle):
    """Adds a key to unlock the front door of the museum."""
    display_name = "Front Door Usable"

class ElevatorsStaySolved(DefaultOnToggle):
    """Adds elevators as checks and will remain open upon solving them."""
    display_name = "Elevators Stay Solved"

class EarlyBeth(DefaultOnToggle):
    """Beth's body is open at the start of the game. This allows any pot piece to be placed in the slide and early checks on the second half of the final riddle."""
    display_name = "Early Beth"

class EarlyLightning(Toggle):
    """Allows lightning to be captured at any point in the game. You will still need to capture all ten Ixupi for victory."""
    display_name = "Early Lightning"

Shivers_options: Dict[str, Option] = {
    "lobby_access": LobbyAccess,
    "puzzle_hints_required": PuzzleHintsRequired,
    "include_information_plaques": InformationPlaques,
    "front_door_usable": FrontDoorUsable,
    "elevators_stay_solved": ElevatorsStaySolved,
    "early_beth": EarlyBeth,
    "early_lightning": EarlyLightning
}

def get_option_value(multiworld: MultiWorld, player: int, name: str) -> Union[int,  FrozenSet]:
    if multiworld is None:
        return Shivers_options[name].default

    player_option = getattr(multiworld, name)[player]

    return player_option.value