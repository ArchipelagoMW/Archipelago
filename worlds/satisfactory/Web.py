from BaseClasses import Tutorial
from .Options import option_groups, option_presets
from ..AutoWorld import WebWorld


class SatisfactoryWebWorld(WebWorld):
    theme = "dirt"
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Satisfactory Archipelago mod and connecting it to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Robb", "Jarno"]
    )
    tutorials = [setup]
    rich_text_options_doc = True

    option_groups = option_groups
    options_presets = option_presets
