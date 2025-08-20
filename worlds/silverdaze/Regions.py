from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Tuple

from BaseClasses import CollectionState, ItemClassification, Region

from BaseClasses import MultiWorld

from .Items import item_table
from .Locations import location_table, SDLocation, SDLocationData
from .Options import SilverDazeOptions

if TYPE_CHECKING:
    from . import SDWorld

def link_sd_areas(world: MultiWorld, player: int):
    for (exit, region) in mandatory_connections:
        world.get_entrance(exit, player).connect(world.get_region(region, player))


sd_regions = [
    #Name of region, any exits (exits are Entrance types)
    ("Menu", ["New_Game"]),
    ("Geo_Room", ["Leave_Geo_Room"]),
    ("Cotton",  ["Door_To_Hub2"]),
    ("GreyHub2", ["Red_Demo_Entrance"]),
    ("Red", ["Red2_Demo_Entrance","Red_Demo_Entrance"]),
    ("Red2", []),
    ]
#Sawyer: Add new regions when the time comes
mandatory_connections = [
    #Name of Entrance, Region where it leads
    ("New_Game", "Geo_Room"),
    ("Leave_Geo_Room", "Cotton"),
    ("Door_To_Hub2", "GreyHub2"),
    ("Red_Demo_Entrance", "Red"),
    ("Red2_Demo_Entrance", "Red2"),

]


    
    