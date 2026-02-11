"""This module contains the Webpage World class for Ratchet and Clank 3"""
from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.rac3options import rac3_option_groups


class RaC3Web(WebWorld):
    theme = "ocean"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        f"A guide to setting up {RAC3OPTION.GAME_TITLE_FULL}: Up Your Arsenal for Archipelago. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        ["TheBreadstick", "Taoshi", "Myth197"]
    )]
    bug_report_page = "https://github.com/Taoshix/Archipelago-RaC3/issues"
    rich_text_options_doc = True
    option_groups = rac3_option_groups
