from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld
from .options import option_groups, option_presets

class NothingWebWorld(WebWorld):
    game = "nothing_archipelago"
    theme= "ice"
    setup_en = Tutorial(
        "Multiword Setup Guide",
        "A guide to setting up Nothing Archipelago fro multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["PhllyPhl"],
    )

    tutorials = [setup_en]
    option_groups = option_groups
    option_presets = option_presets