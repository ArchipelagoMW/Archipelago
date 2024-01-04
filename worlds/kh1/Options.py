from typing import Dict

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionSet

class Sephiroth(Toggle):
    """
    Toggle whether the win condition should be changed to defeating Sephiroth.
    """
    display_name = "Sephiroth"

class Atlantica(Toggle):
    """
    Toggle whether Atlantica locations/items should be included.
    """
    display_name = "Atlantica"

kh1_options: Dict[str, type(Option)] = {
    "sephiroth": Sephiroth,
    "atlantica": Atlantica,
}
