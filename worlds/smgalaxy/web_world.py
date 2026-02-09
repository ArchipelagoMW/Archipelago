from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

#from .Options import option_groups, option_presets


# For our game to display correctly on the website, we need to define a WebWorld subclass.
class SMGWebWorld(WebWorld):
    game = "Super Mario Galaxy"
    theme = "ice"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Super Mario Galaxy for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Squidy"],
        # This is mostly placeholder till someone writes the full guide
    )
    tutorials = [setup_en]
    #option_groups = option_groups