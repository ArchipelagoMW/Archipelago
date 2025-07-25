from typing import ClassVar

from worlds.AutoWorld import World

from . import Options

class GrinchWorld(World):
    game: ClassVar[str] = "The Grinch"
    options_dataclass = Options.GrinchOptions
    options = Options.GrinchOptions