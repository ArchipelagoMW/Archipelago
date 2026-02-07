from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .options import option_groups, option_presets



class TVRUHHWebWorld(WebWorld):
    game = "TVRUHH"

    theme = "grassFlowers"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up TVRUHH for a MultiWorld",
        "English",
        "setup_en.md",
        "setup/en",
        ["NulvWorks"],
    )

    tutorials = [setup_en]

    option_groups = option_groups
    options_presets = option_presets