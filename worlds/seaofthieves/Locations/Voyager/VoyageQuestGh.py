from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.ItemReqEvalOr import ItemReqEvalOr
from ...Items.Items import Items


class SettingsVoyageQuestGh:

    def __init__(self, completeAny=1, xmarks=1, riddle=1, wayfinder=1, aXmarks=1, aRiddle=1, aWayfinder=1):
        self.completeAny = completeAny
        self.xmarks_req_cnt = xmarks
        self.riddle_req_cnt = riddle
        self.wayfinder_req_cnt = wayfinder
        self.aXmarks_req_cnt = aXmarks
        self.aRiddle_req_cnt = aRiddle
        self.aWayfinder_req_cnt = aWayfinder


class VoyageQuestGh(LocationsBase):
    L_VOYAGE_COMP_GH_X = "Complete X Marks The Spot Voyage (GH)"
    L_VOYAGE_COMP_GH_RID = "Complete Riddle Map Voyage (GH)"
    L_VOYAGE_COMP_GH_WAY = "Complete Wayfinder Voyage (GH)"
    L_VOYAGE_COMP_GH_AX = "Complete Ashen X Marks The Spot Voyage (GH)"
    L_VOYAGE_COMP_GH_ARID = "Complete Ashen Riddle Map Voyage (GH)"
    L_VOYAGE_COMP_GH_AWAY = "Complete Ashen Wayfinder Voyage (GH)"

    def __init__(self, settings: SettingsVoyageQuestGh):
        super().__init__()
        self.x = [1, 1, 1]

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_GH])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.voyages_gh])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 0), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_GH_X, wlc, settings.xmarks_req_cnt > 0))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_GH])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.voyages_gh])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 1), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_GH_RID, wlc, settings.riddle_req_cnt > 0))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_GH])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.voyages_gh])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 2), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_GH_WAY, wlc, settings.wayfinder_req_cnt > 0))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_GH_ASHEN])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.voyages_gh])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 3), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_GH_AX, wlc, settings.aXmarks_req_cnt > 0))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_GH_ASHEN])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.voyages_gh, Items.sail_inferno])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 4), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_GH_ARID, wlc, settings.aRiddle_req_cnt > 0))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_GH_ASHEN])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.voyages_gh, Items.sail_inferno])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 5), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_GH_AWAY, wlc, settings.aWayfinder_req_cnt > 0))
