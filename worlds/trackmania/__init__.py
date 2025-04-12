import settings
import typing
from .options import TrackmaniaOptions  # the options we defined earlier
from .items import trackmania_items, trackmania_item_groups, create_itempool, create_item  # data used below to add items to the World
from .locations import build_locations, create_regions  # same as above
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, Location, Entrance, Item, ItemClassification, Tutorial

class Webmania(WebWorld):
    theme = "ice"
    # option_groups = create_option_groups()
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide for setting up Trackmania to be played in Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["SerialBoxes"]
    )]

class TrackmaniaWorld(World):
    """Trackmania is a mechanically deep arcade racing game that is easy to pick up and addicting to master!
    Zoom through hundreds of thousands of user-made tracks as fast as you can!"""
    game = "Trackmania"  # name of the game/world
    options_dataclass = TrackmaniaOptions  # options the player can set
    options: TrackmaniaOptions  # typing hints for option results

    item_name_to_id = trackmania_items
    location_name_to_id = build_locations()

    item_name_groups = trackmania_item_groups

    def create_item(self, name: str) -> Item:
        return create_item(self, name)

    def create_items(self):
        self.multiworld.itempool += create_itempool(self)

    def create_regions(self):
        create_regions(self)
