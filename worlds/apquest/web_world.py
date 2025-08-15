from BaseClasses import Tutorial

from worlds.AutoWorld import WebWorld

from .options import option_groups, option_presets


# TODO: Explain what a webworld is
class APQuestWebWorld(WebWorld):
    game = "APQuest"

    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up APQuest for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["NewSoupVi"],
    )

    tutorials = [setup]  # noqa: RUF012

    option_groups = option_groups
    options_presets = option_presets
