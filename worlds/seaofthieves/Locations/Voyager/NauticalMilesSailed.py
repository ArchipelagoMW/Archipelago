from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.ItemReqEvalOr import ItemReqEvalOr


class SettingsNauticalMiles:

    def __init__(self, cnt=0):
        self.cnt = cnt


class NauticalMiles(LocationsBase):
    L_NAUTICAL_MILE = "Sail Nautical Miles"

    def __init__(self, settings: SettingsNauticalMiles):
        super().__init__()
        self.x = [1, 10, 0]
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_OPEN_SEA])
        lgc = ItemReqEvalOr([])

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_NAUTICAL_MILE, wlc, settings.cnt > 0))
