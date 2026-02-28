from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .options import option_groups, option_presets
from . import names

class SonicGensWebWorld(WebWorld):
    game = names.GameName

    theme = "partyTime"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Sonic Generations randomizer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["N/A"]
    )

    tutorials = [setup_en]
