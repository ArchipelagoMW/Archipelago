from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.Items import Items
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.ItemReqEvalOr import ItemReqEvalOr

class SettingsVoyageQuestOos:

    def __init__(self, completeAny=1, bounty=1, ashenBounty=1, ghostShip=1):
        self.completeAny = completeAny
        self.bounty = bounty
        self.ashenBounty = ashenBounty
        self.ghostShip = ghostShip


class VoyageQuestOos(LocationsBase):
    locations = []

    L_VOYAGE_COMP_OOS_BOUNTY = "Complete Bounty Voyage (OOS)"
    L_VOYAGE_COMP_OOS_ABOUNTY = "Complete Ashen Bounty Voyage (OOS)"
    L_VOYAGE_COMP_OOS_GHOSTSHIP = "Complete Ghost Ship Voyage (OOS)"

    def __init__(self, settings: SettingsVoyageQuestOos):
        super().__init__()
        self.x = [1, 3, 1]

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_OOS])
        lgc = ItemReqEvalOr(
            [ItemReqEvalAnd([Items.voyages_oos, Items.sail, Items.ship_weapons, Items.personal_weapons])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 0), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_OOS_BOUNTY, wlc, settings.bounty > 0))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_OOS_ASHEN])
        lgc = ItemReqEvalOr(
            [ItemReqEvalAnd(
                [Items.voyages_oos, Items.sail, Items.ship_weapons, Items.personal_weapons, Items.sail_inferno])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 1), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_OOS_ABOUNTY, wlc, settings.ashenBounty > 0))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_OOS])
        lgc = ItemReqEvalOr(
            [ItemReqEvalAnd([Items.voyages_oos, Items.sail, Items.ship_weapons])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 2), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_OOS_GHOSTSHIP, wlc, settings.ghostShip > 0))
