from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.Items import Items
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.ItemReqEvalOr import ItemReqEvalOr


class SettingsMenuQuestAll:

    def __init__(self, fodSealRequirement=3):
        self.fodSealRequirement = fodSealRequirement


class MenuQuestAll(LocationsBase):
    L_PIRATE_POCKET = "Item in your pocket"
    L_PIRATE_FOD = "Defeat Graymarrow"
    descriptor = "MenuQuestAll"

    def __init__(self):
        super().__init__()
        self.x = [0, 0, 0, 0]

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_MENU])
        lgc = ItemReqEvalOr([])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], self.x[3], None, False), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_PIRATE_POCKET, wlc, True))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_FORT_OF_THE_DAMNED])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.voyage_of_destiny])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], -1, None, False), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_PIRATE_FOD, wlc, True))

