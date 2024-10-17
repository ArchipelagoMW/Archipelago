from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.Items import Items
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.ItemReqEvalOr import ItemReqEvalOr


class SettingsVoyageQuestMa:

    def __init__(self, completeAny=1, tradeGoods=1, shipment=1):
        self.completeAny = completeAny
        self.tradeGoods = tradeGoods
        self.shipment = shipment


class VoyageQuestMa(LocationsBase):
    L_VOYAGE_COMP_MA_TRADE = "Complete Trade Good Voyage (MA)"
    L_VOYAGE_COMP_MA_SHIPMENT = "Complete Lost Shipment Voyage (MA)"

    def __init__(self, settings: SettingsVoyageQuestMa):
        super().__init__()
        self.x = [1, 2, 1]

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_MA])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.voyages_ma, Items.sail])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 0), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_MA_TRADE, wlc, settings.tradeGoods > 0))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_MA])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.voyages_ma, Items.sail])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 1), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_VOYAGE_COMP_MA_SHIPMENT, wlc, settings.shipment > 0))
