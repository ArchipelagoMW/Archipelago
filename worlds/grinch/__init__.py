from typing import ClassVar

from worlds.AutoWorld import World

from . import Options

class GrinchWorld(World):
    game: ClassVar[str] = "The Grinch"
    options_dataclass = Options.GrinchOptions
    options = Options.GrinchOptions
    topology_present = True #not an open world game, very linear
    item_name_to_id =
    location_name_to_id =