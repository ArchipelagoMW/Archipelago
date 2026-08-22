from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .options import option_presets
GAME_NAME = "EV Nova"

# For our game to display correctly on the website, we need to define a WebWorld subclass.
class EVNWebWorld(WebWorld):
    # We need to override the "game" field of the WebWorld superclass.
    # This must be the same string as the regular World class.
    game = GAME_NAME

    # Your game pages will have a visual theme (affecting e.g. the background image).
    # You can choose between dirt, grass, grassFlowers, ice, jungle, ocean, partyTime, and stone.
    theme = "jungle"

    # A WebWorld can have any number of tutorials, but should always have at least an English setup guide.
    # Many WebWorlds just have one setup guide, but some have multiple, e.g. for different languages.
    # We need to create a Tutorial object for every setup guide.
    # In order, we need to provide a title, a description, a language, a filepath, a link, and authors.
    # The filepath is relative to a "/docs/" directory in the root folder of your apworld.
    # The "link" parameter is unused, but we still need to provide it.
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up EV Nova for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Dorrulf"],
    )

    # We add these tutorials to our WebWorld by overriding the "tutorials" field.
    # tutorials = [setup_en, setup_de]
    tutorials = [setup_en]

    # docs folder will be scanned for game info pages using this list in the format '{language}_{game_name}.md'
    game_info_languages = ["en"]

    # display a link to a bug report page, most likely a link to a GitHub issue page.
    bug_report_page = "https://github.com/Dorrulf/EVNovaAP/issues"

    # If we have option groups and/or option presets, we need to specify these here as well.
    options_presets = option_presets

    # Huh, we could add further location and item descriptions here...
    # With EVN, they're pretty descriptive already. Mostly would be clarifying IDs w/ duplicate names.
    # location_descriptions = {}     # dict[str, str]
    # item_descriptions = {}        # dict[str, str]