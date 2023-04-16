from typing import Dict

from Options import Option, Toggle


class HardMode(Toggle):
    """Only for the most masochistically inclined... Requires button activation!"""
    display_name = "Hard Mode"


clique_options: Dict[str, type(Option)] = {
    "hard_mode": HardMode
}
