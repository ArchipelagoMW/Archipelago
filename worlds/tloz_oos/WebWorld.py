from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld
from .Options import oos_option_groups


class OracleOfSeasonsWeb(WebWorld):
    theme = "grass"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Oracle of Seasons for Archipelago on your computer.",
        "English",
        "oos_setup_en.md",
        "oos_setup/en",
        ["Dinopony"]
    )

    setup_fr = Tutorial(
        "Guide de configuration MultiWorld",
        "Un guide pour configurer Oracle of Seasons d'Archipelago sur votre PC.",
        "Français",
        "oos_setup_fr.md",
        "oos_setup/fr",
        ["Deoxis"]
    )
    tutorials = [setup_en, setup_fr]
    option_groups = oos_option_groups
