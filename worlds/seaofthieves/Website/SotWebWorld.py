
from worlds.AutoWorld import WebWorld
from BaseClasses import Tutorial


class SotWebWorld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Sea of Thieves for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Ethan Steidl"]
    )]