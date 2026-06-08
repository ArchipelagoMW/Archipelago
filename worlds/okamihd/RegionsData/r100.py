from typing import TYPE_CHECKING
from ..Types import ExitData, EventData
from ..Enums.RegionNames import RegionNames

if TYPE_CHECKING:
   from .. import OkamiWorld

exits = {
    RegionNames.CURSED_KAMIKI: [ExitData(RegionNames.RIVER_OF_THE_HEAVENS_KAMIKI),
                                ExitData(RegionNames.STONE_KAMIKI, required_items_events=["Cursed Kamiki - Cutting the peach"],one_way=True)
    ]
}
events = {
    RegionNames.CURSED_KAMIKI: {
        "Cursed Kamiki - Cutting the peach": EventData(id=0x202,power_slash_level=1,precollected=lambda o:o.OpenGameStart),
    }
}
locations = {
}
