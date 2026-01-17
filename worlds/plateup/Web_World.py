from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld


class PlateUpWebWorld(WebWorld):
    game="plateup"

    # You can choose between dirt, grass, grassFlowers, ice, jungle, ocean, partyTime, and stone.
    theme="dirt"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up PlateUp for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["CazIsABoi"],
    )

    # We add these tutorials to our WebWorld by overriding the "tutorials" field.
    tutorials = [setup_en]

    # If we have option groups and/or option presets, we need to specify these here as well.
    # option_groups = option_groups
    # options_presets = option_presets