from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .options import option_groups#, option_presets

class GatoRobotoWebWorld(WebWorld):
    game = "Gato Roboto B-Side"

    theme = "grass"

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Gato Roboto Archipelago",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["Nitroxy"]
    )

    tutorials = [setup_en]
    #options_presets = options_presets
    option_groups = option_groups