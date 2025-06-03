from typing import TYPE_CHECKING
from ..Types import ExitData, RegionNames

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
    # TODO: in ER this should be the starting point
    RegionNames.MENU: [ExitData("New Game", RegionNames.CURSED_KAMIKI)]
}
events = {
}
locations = {
}
