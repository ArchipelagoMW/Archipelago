from typing import Dict

from Options import Option, Toggle


class HardMode(Toggle):
    """Only for masochists: requires 2 presses!"""
    display_name = "Hard Mode"


clique_options: Dict[str, type(Option)] = {
    "hard_mode": HardMode
}
