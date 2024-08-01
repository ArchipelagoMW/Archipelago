import settings
import typing
from .items import item_descriptions  # data used below to add items to the World
from .locations import location_descriptions  # same as above
from .presets import options_presets
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, Location, Entrance, Item, ItemClassification, Tutorial


class ShapezSettings(settings.Group):
    game = "Shapez"


class ShapezWeb(WebWorld):
    options_presets = options_presets
    rich_text_options_doc = True
    theme = "stone"
    bug_report_page = "https://github.com/BlastSlimey/ShapezArchipelago/issues"
    game_info_languages = ['en', 'de']
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Shapez with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["BlastSlimey"]
    )
    setup_de = Tutorial(
        "Multiworld-Setup-Anleitung",
        "Eine Anleitung zum Spielen von Shapez in Archipelago",
        "Deutsch",
        "setup_de.md",
        "setup/de",
        ["BlastSlimey"]
    )
    tutorials = [setup_en, setup_de]
    location_descriptions = location_descriptions
    item_descriptions = item_descriptions


class ShapezWorld(World):
    """Insert description of the world/game here."""
    game = "Shapez"  # name of the game/world
    options_dataclass = ShapezOptions  # options the player can set
    options: ShapezOptions  # typing hints for option results
    settings: typing.ClassVar[ShapezSettings]  # will be automatically assigned from type hint
    topology_present = True  # show path to required location checks in spoiler

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a property.
    base_id = 200107
    # instead of dynamic numbering, IDs could be part of data

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {name: id for
                       id, name in enumerate(shapez_items, base_id)}
    location_name_to_id = {name: id for
                           id, name in enumerate(shapez_locations, base_id)}

    # Items can be grouped using their names to allow easy checking if any item
    # from that group has been collected. Group names can also be used for !hint
    item_name_groups = {
        "Upgrades": {"Big Belt Upgrade", "Small Belt Upgrade"},
    }