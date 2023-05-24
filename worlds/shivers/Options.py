from typing import Dict, FrozenSet, Union
from Options import Choice, Option
from BaseClasses import MultiWorld


class LobbyAccess(Choice):
    """Normal places keys need to access the lobby into the item pool normally. Early places the keys as early. Local places the keys locally."""
    display_name = "Lobby Access"
    option_normal = 0
    option_early = 1
    option_local = 2

Shivers_options: Dict[str, Option] = {
    "lobby_access": LobbyAccess
}

def get_option_value(multiworld: MultiWorld, player: int, name: str) -> Union[int,  FrozenSet]:
    if multiworld is None:
        return Shivers_options[name].default

    player_option = getattr(multiworld, name)[player]

    return player_option.value