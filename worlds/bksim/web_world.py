from worlds.AutoWorld import WebWorld
from . import options
from BaseClasses import Tutorial


class BKSimWebWorld(WebWorld):
    options_presets = options.options_presets
    setup_en = Tutorial(
        "BKSim Setup",
        "How to set up BK Simulator for Archipelago",
        "English",
        "setup_en.md",
        "setup/en",
        ["Emily"]
    )
    tutorials = [setup_en]
