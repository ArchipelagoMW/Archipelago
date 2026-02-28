from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, WorldType


# For our game to display correctly on the website, we need to define a WebWorld subclass.
class APQuestWebWorld(WebWorld):
    """
    APQuest is a minimal 8bit-era inspired adventure game with grid-like movement.
    Good games don't need more than six checks.
    """
    # The docstring should contain a description of the game, to be displayed on the WebHost.

    # We need to override the "game" field of the WebWorld superclass.
    # This must be the same string as the regular World class.
    game = "APQuest"

    # We need to tell WebHost what type of world we are. For normal games, this is WorldType.GAME
    # Other types are used to create webhost pages not related to a World class.
    world_type = WorldType.GAME

    # Your game pages will have a visual theme (affecting e.g. the background image).
    # You can choose between dirt, grass, grassFlowers, ice, jungle, ocean, partyTime, and stone.
    theme = "grassFlowers"

    # A WebWorld can have any number of tutorials, but should always have at least an English setup guide.
    # Many WebWorlds just have one setup guide, but some have multiple, e.g. for different languages.
    # We need to create a Tutorial object for every setup guide.
    # In order, we need to provide a title, a description, a language, a filepath, a link, and authors.
    # The filepath is relative to a "/docs/" directory in the root folder of your apworld.
    # The "link" parameter is unused, but we still need to provide it.
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up APQuest for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["NewSoupVi"],
    )
    # Let's have our setup guide in German as well.
    # Do not translate the title and description!
    # WebHost needs them to be the same to identify that it is the same tutorial.
    # This lets it display the tutorials more compactly.
    setup_de = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up APQuest for MultiWorld.",
        "German",
        "setup_de.md",
        "setup/de",
        ["NewSoupVi"],
    )

    # We add these tutorials to our WebWorld by overriding the "tutorials" field.
    tutorials = [setup_en, setup_de]
