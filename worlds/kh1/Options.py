from typing import Dict

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionSet

class Sephiroth(Toggle):
    """
    Toggle whether the win condition should be changed to defeating Sephiroth.
    """
    display_name = "Sephiroth"

kh1_options: Dict[str, type(Option)] = {
    "sephiroth": Sephiroth,
}
