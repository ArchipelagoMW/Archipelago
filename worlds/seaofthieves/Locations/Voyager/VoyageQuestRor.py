from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionDetails import Regions
from ...Items.Items import Items
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.ItemReqEvalOr import ItemReqEvalOr
from ...Regions.RegionCollection import RegionNameCollection


class SettingsVoyageQuestRor:

    def __init__(self, completeAny=1, xmarks=1, riddle=1, wayfinder=1, bounty=1, athena=1):
        self.completeAny = completeAny
        self.xmarks = xmarks
        self.riddle = riddle
        self.wayfinder = wayfinder
        self.bounty = bounty
        self.athena = athena

    def getSettingForLocName(self, name: str):
        if name == VoyageQuestRor.L_VOYAGE_COMP_ROR_TOTAL:
            return self.completeAny

        if name == VoyageQuestRor.L_VOYAGE_COMP_ROR_X:
            return self.xmarks

        if name == VoyageQuestRor.L_VOYAGE_COMP_ROR_RIDDLE:
            return self.riddle

        if name == VoyageQuestRor.L_VOYAGE_COMP_ROR_WAY:
            return self.wayfinder

        if name == VoyageQuestRor.L_VOYAGE_COMP_ROR_BOUNTY:
            return self.bounty

        if name == VoyageQuestRor.L_VOYAGE_COMP_ROR_ATHENA:
            return self.athena

        # default for it to be enabled
        return 1


class VoyageQuestRor(LocationsBase):
    L_VOYAGE_COMP_ROR_TOTAL = "Complete Voyage (ROAR)"
    L_VOYAGE_COMP_ROR_X = "Complete Ashen X Marks the Spot Voyage (ROAR)"
    L_VOYAGE_COMP_ROR_RIDDLE = "Complete Ashen Riddle Map Voyage (ROAR)"
    L_VOYAGE_COMP_ROR_WAY = "Complete Ashen Wayfinder Voyage (ROAR)"
    L_VOYAGE_COMP_ROR_BOUNTY = "Complete Ashen Bounty Voyage (ROAR)"
    L_VOYAGE_COMP_ROR_ATHENA = "Complete Ashen Athena Voyage (ROAR)"

    def __init__(self, settings: SettingsVoyageQuestRor):
        super().__init__()
        self.x = [1, 5, 1]

        reg: RegionNameCollection = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_EM_ASHEN])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.sail_inferno])])
        web = WebItemJsonIdentifier(self.x[0], self.x[1], 0)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_ROR_TOTAL, wlc, settings.completeAny > 0))

        reg: RegionNameCollection = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_GH_ASHEN])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.sail_inferno])])
        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 0)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_ROR_X, wlc, settings.xmarks > 0))

        reg: RegionNameCollection = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_GH_ASHEN])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.sail_inferno])])
        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 1)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_ROR_RIDDLE, wlc, settings.riddle > 0))

        reg: RegionNameCollection = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_GH_ASHEN])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.sail_inferno])])
        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 2)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_ROR_WAY, wlc, settings.wayfinder > 0))

        # logic changes here

        reg: RegionNameCollection = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_OOS_ASHEN])
        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 3)
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.sail_inferno, Items.personal_weapons])])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_ROR_BOUNTY, wlc, settings.bounty > 0))

        reg: RegionNameCollection = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_AF_ASHEN])
        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 4)
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.sail_inferno, Items.voyages_af])])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_ROR_ATHENA, wlc, settings.athena > 0))
