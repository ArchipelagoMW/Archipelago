from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World

from .Options import VoidSolsOptions

class VoidSolsWeb(WebWorld):
    theme = "party"
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Void Sols"
        "for Archipelago on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Cookie966507"],
    )
    tutorials = [setup]


class VoidSolsWorld(World):
    """ Void Sols is a top-down, 2D, minimalist souls-like RPG."""

    game = "Void Sols"

    options = VoidSolsOptions
    options_dataclass = VoidSolsOptions