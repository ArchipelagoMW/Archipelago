from .Rules import SDRules, key, zone
from .Regions import SDRegionData, create_regions
from .Items import ItemData, item_table
from .Locations import location_table, SDLocationData
from .Options import SilverDazeOptions
from BaseClasses import ItemClassification, MultiWorld, Tutorial, LocationProgressType
from typing import Any, Set, List, Dict, Optional, Tuple, ClassVar, TextIO, Union
from worlds.AutoWorld import WebWorld, World
from Items import item_table
from Locations import SDLocationData
from Locations import location_table


class SDWorld(World):
    """
    This will describe Silver Daze eventually.
    """
    game = "Silver Daze"
    required_client_version = (0, 5, 4)
    options_dataclass = SilverDazeOptions

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

    item_name_to_id = {name: item_table.code.name for name, data in item_table.code}
    location_name_to_id = {name: SDLocationData.id for name, data in SDLocationData.id}


