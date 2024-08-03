from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.ItemReqEvalOr import ItemReqEvalOr


class SettingsShipwrecks:

    def __init__(self, any=0):
        self.any = any


class Shipwrecks(LocationsBase):
    L_SHIPWRECK = "Visit Shipwreck"

    def __init__(self, settings: SettingsShipwrecks):
        super().__init__()
        self.x = [1, 14, 0]
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_OPEN_SEA])
        lgc = ItemReqEvalOr([])

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_SHIPWRECK, wlc, settings.any > 0))
