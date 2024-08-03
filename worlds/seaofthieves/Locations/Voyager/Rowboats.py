from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..Locations import ScreenData
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.ItemReqEvalOr import ItemReqEvalOr


class SettingsRowboat:

    def __init__(self, any=0, lantern=0, harpoon=0, cannon=0):
        self.any = any
        self.lantern = lantern
        self.harpoon = harpoon
        self.cannon = cannon


class Rowboats(LocationsBase):
    L_ROW = "Dock Rowboat"
    L_ROW_LANTERN = "Dock Lantern Rowboat"
    L_ROW_HARP = "Dock Harpoon Rowboat"
    L_ROW_CANN = "Dock Cannon Rowboat"

    def __init__(self, settings: SettingsRowboat):
        super().__init__()
        self.x = [1, 15, 1]
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_ISLANDS])
        lgc = ItemReqEvalOr([])

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], -1, "Rowboat Types Docked Aboard (Ship)")
        wlc = WebLocationCollection([WebLocation(web, reg, lgc, Rowboats.L_ROW, ScreenData(["Dock"]))])
        self.locations.append(LocDetails(self.L_ROW, wlc, settings.any > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 0)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_ROW_LANTERN, wlc, settings.lantern > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 1)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_ROW_HARP, wlc, settings.harpoon > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 2)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_ROW_CANN, wlc, settings.cannon > 0))
