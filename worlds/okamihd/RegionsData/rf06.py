from typing import TYPE_CHECKING

from ..Rules import moon_cave_access
from ..Types import ExitData, EventData
from ..Enums.RegionNames import RegionNames

if TYPE_CHECKING:
    from .. import OkamiWorld

exits = {
        RegionNames.MOON_CAVE_OUTSIDE:[ExitData('Enter Moon Cave',RegionNames.MOON_CAVE_BROKEN_STAIRS,has_events=["Moon Cave - Open entrance"])]
}
events = {
    RegionNames.MOON_CAVE_OUTSIDE: {
        "Moon Cave - Open entrance": EventData(special_rule=moon_cave_access())
    }
}
locations = {
}
