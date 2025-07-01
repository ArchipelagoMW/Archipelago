from typing import TYPE_CHECKING
from ..Types import ExitData, EventData
from ..Enums.RegionNames import RegionNames

if TYPE_CHECKING:
    pass

exits = {
    RegionNames.CURSED_KAMIKI: [ExitData("Cursed Kamiki Torii", RegionNames.RIVER_OF_THE_HEAVENS_KAMIKI),
                                ExitData("Kamiki Restoration Cutscene", RegionNames.STONE_KAMIKI,
                                         has_events=["Cursed Kamiki - Cutting the peach"])]
}
events = {
    RegionNames.CURSED_KAMIKI: {
        "Cursed Kamiki - Cutting the peach": EventData(id=0x202,power_slash_level=1,precollected=lambda o:o.OpenGameStart),
    }
}
locations = {
}
