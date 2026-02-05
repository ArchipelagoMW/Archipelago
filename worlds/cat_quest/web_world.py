from BaseClasses import Tutorial

from worlds.AutoWorld import WebWorld

class CatQuestWebWorld(WebWorld):
    game = "Cat Quest"
    theme = "grassFlowers"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Cat Quest randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Nikkilite"]
    )
    
    tutorials = [setup_en]
