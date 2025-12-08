from typing import NamedTuple, Optional
from BaseClasses import Location, Region
from .common import *


class LocInfo(NamedTuple):
    name: str
    region_id: RID
    index: int


class BKSim_Location(Location):
    game = game_name
    info: Optional[LocInfo]

    # override constructor to automatically mark event locations as such, and handle LocInfo
    def __init__(self, player: int, name: str, code: Optional[int], parent: Region, info: Optional[LocInfo] = None) -> None:
        super(BKSim_Location, self).__init__(player, name, code, parent)
        self.event = code is None
        self.info = info


location_table = [LocInfo("Sunny %d" % (idx + 1), RID.SUNNY, idx) for idx in range(0,100)]
location_table += [LocInfo("Rainy %d" % (idx + 1), RID.RAINY, idx) for idx in range(0,100)]
location_table += [LocInfo("Snowy %d" % (idx + 1), RID.SNOWY, idx) for idx in range(0,100)]

location_name_to_id = {loc.name: num for num,loc in enumerate(location_table,1)}
