import Rules
import Regions
import Items
import Locations
from BaseClasses import ItemClassification, MultiWorld, Tutorial, LocationProgressType
from typing import Any, Set, List, Dict, Optional, Tuple, ClassVar, TextIO, Union
from worlds.AutoWorld import WebWorld, World

class SDWorld(World):
    """
    This will describe Silver Daze eventually.
    """
    game = "Silver Daze"
    required_client_version = (0, 5, 4)

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
