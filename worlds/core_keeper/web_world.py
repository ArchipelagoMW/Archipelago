from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .options import option_groups


class CoreKeeperWebWorld(WebWorld):
    game = "Core Keeper"
    theme = "dirt"
    rich_text_options_doc = True
    option_groups = option_groups
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "How to install the Core Keeper mod and connect to an Archipelago room.",
            "English",
            "setup_en.md",
            "setup/en",
            ["URAQTDev"],
        )
    ]
