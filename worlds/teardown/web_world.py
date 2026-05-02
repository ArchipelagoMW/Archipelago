from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

#from .options import option_groups, option_presets


# This is probably useless, should look into it
class TeardownWebWorld(WebWorld):
    game = "Teardown"

# You can choose between dirt, grass, grassFlowers, ice, jungle, ocean, partyTime, and stone.
    theme = "dirt"

    # A WebWorld can have any number of tutorials, but should always have at least an English setup guide.
    # We need to create a Tutorial object for every setup guide.
    # In order, we need to provide a title, a description, a language, a filepath, a link, and authors.
    # The filepath is relative to a "/docs/" directory in the root folder of your apworld.
    # The "link" parameter is unused, but we still need to provide it.
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Teardown for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Evereliquest"],
    )

    # We add these tutorials to our WebWorld by overriding the "tutorials" field.
    tutorials = [setup_en]

    # If we have option groups and/or option presets, we need to specify these here as well.
    #option_groups = option_groups
    #options_presets = option_presets
