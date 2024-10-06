from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.ItemReqEvalOr import ItemReqEvalOr


class SettingsCaptainShipSpotted:

    def __init__(self, any=0, sloop=0, brig=0, gall=0):
        self.any = any
        self.sloop = sloop
        self.brig = brig
        self.gall = gall


class CaptainShipSpotted(LocationsBase):
    L_CAPTAIN_SHIP_SPOTTED = "Spot Captain Ship"
    L_CAPTAIN_SHIP_SPOTTED_SLOOP = "Spot Captain Sloop"
    L_CAPTAIN_SHIP_SPOTTED_BRIG = "Spot Captain Brigantine"
    L_CAPTAIN_SHIP_SPOTTED_GALL = "Spot Captain Galleon"

    def __init__(self, settings: SettingsCaptainShipSpotted):
        super().__init__()
        self.x = [1, 11, 1]
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_OPEN_SEA])
        lgc = ItemReqEvalOr([])

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_CAPTAIN_SHIP_SPOTTED, wlc, settings.any > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 0)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_CAPTAIN_SHIP_SPOTTED_SLOOP, wlc, settings.sloop > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 1)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_CAPTAIN_SHIP_SPOTTED_BRIG, wlc, settings.brig > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 2)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_CAPTAIN_SHIP_SPOTTED_GALL, wlc, settings.gall > 0))
