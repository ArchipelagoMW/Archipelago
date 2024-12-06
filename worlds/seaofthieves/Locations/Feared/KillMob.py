import typing

from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.ItemReqEvalOr import ItemReqEvalOr
from ...Locations.LocationSettingOption import LocationSettingOption
from ...Locations.ScreenData import ScreenData
from ...Items.Items import Items

class SettingsKillMob:

    def __init__(self):
        pass


class KillMob(LocationsBase):
    L_ILL_KRAKEN = "Vanquish the Kraken"


    web_locs: typing.Dict[str, WebLocation] = {}

    def __init__(self, settings: SettingsKillMob):
        super().__init__()
        self.x = [4, 0, 0]
        self.settings = settings

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_OPEN_SEA])
        lgc = ItemReqEvalOr([ItemReqEvalAnd(Items.barrel_cannon)])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], 1, 0, -1, "Total Krakens Vanquished (Crew)"), reg, lgc)
        ])

        self.locations.append(LocDetails(self.L_ILL_KRAKEN, wlc, True))