import settings
import typing
from .options import TrackmaniaOptions  # the options we defined earlier
from .items import trackmania_items, trackmania_item_groups  # data used below to add items to the World
from .locations import BuildLocationDict  # same as above
from worlds.AutoWorld import World
from BaseClasses import Region, Location, Entrance, Item, RegionType, ItemClassification


class TrackmaniaWorld(World):
    """monkaSteer"""
    game = "Trackmania"  # name of the game/world
    options_dataclass = TrackmaniaOptions  # options the player can set
    options: TrackmaniaOptions  # typing hints for option results

    item_name_to_id = trackmania_items
    location_name_to_id = BuildLocationDict()

    item_name_groups = trackmania_item_groups