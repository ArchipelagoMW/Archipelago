from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from . import constants


class APQuestWebWorld(WebWorld):
    game = constants.GAME
    theme = "grass"

    TUTORIAL_NAME = "Multiworld Setup Guide"
    DESCRIPTION = "A guide to setting up Tomba! for MultiWorld."

    setup_en = Tutorial(
        TUTORIAL_NAME,
        DESCRIPTION,
        "English",
        "setup_en.md",
        "setup/en",
        ["T4g1", "Laufral"],
    )

    setup_fr = Tutorial(
        TUTORIAL_NAME,
        DESCRIPTION,
        "French",
        "setup_fr.md",
        "setup/fr",
        ["T4g1", "Laufral"],
    )

    tutorials = [setup_en, setup_fr]
