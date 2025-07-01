from typing import TYPE_CHECKING
from ..Enums.RegionNames import RegionNames
from ..Types import ExitData

if TYPE_CHECKING:
    pass

exits = {
    # TODO: in ER this should be the starting point
    RegionNames.MENU: [ExitData("New Game", RegionNames.CURSED_KAMIKI)]
}
events = {
}
locations = {
}
