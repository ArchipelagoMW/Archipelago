from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.ItemReqEvalOr import ItemReqEvalOr


class SettingsDaysAtSea:

    def __init__(self, count=0):
        self.count = count


class DaysAtSea(LocationsBase):
    L_DAYS_AT_SEA = "Spend a Day at Sea"

    def __init__(self, settings: SettingsDaysAtSea):
        super().__init__()
        self.x = [1, 12, 0]
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_OPEN_SEA])
        lgc = ItemReqEvalOr([])

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_DAYS_AT_SEA, wlc, settings.count > 0))
