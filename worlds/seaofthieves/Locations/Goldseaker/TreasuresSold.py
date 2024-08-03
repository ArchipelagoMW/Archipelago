from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.Items import Items
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.ItemReqEvalOr import ItemReqEvalOr


class SettingsTreasuresSold:

    def __init__(self, allowAny=1, allowSimple=1, allowRare=0):
        self.allowAny = allowAny
        self.allowSimple = allowSimple
        self.allowRare = allowRare


class TreasuresSold(LocationsBase):
    L_GS_SELL_ANY = "Sell Anything"
    L_GS_SELL_CHEST = "Sell Chest"
    L_GS_SELL_SKULL = "Sell Skull"
    L_GS_SELL_DARK_RELIC = "Sell Dark Relic"
    L_GS_SELL_ARTIFACT = "Sell Artifact"
    L_GS_SELL_VAULT_KEY = "Sell Vault Key"
    L_GS_SELL_SIREN = "Sell Siren Gem"
    L_GS_SELL_MERMAID_GEM = "Sell Mermaid Gem"
    L_GS_SELL_BREATH_OF_THE_SEA = "Sell Breath of the Sea"
    L_GS_SELL_CHEST_ANIMAL_CRATE = "Sell Animal Crate"
    L_GS_SELL_CHEST_RESOURCE_CRATE = "Sell Resource Crate"
    L_GS_SELL_CHEST_TRADE_GOODS = "Sell Trade Goods"
    L_GS_SELL_CHEST_CARGO_GOODS = "Sell Cargo Goods"
    L_GS_SELL_FIREWORKS = "Sell Fireworks"
    L_GS_SELL_GIFTS = "Sell Reaper Gift"
    L_GS_SELL_EM_FLAG = "Sell Emissary Flag"
    L_GS_SELL_ASHEN_TOMB = "Sell Ashen Tomb"
    L_GS_SELL_REAPER_CHEST = "Sell Reaper's Chest"
    L_GS_SELL_BOX_OF_WONDERS = "Sell Box of Wondrous Secrets"

    def __init__(self, settings: SettingsTreasuresSold):
        super().__init__()
        self.x = [0, 1, 1]
        reg_gh = RegionNameCollection()
        reg_gh.addFromList([Regions.R_DOMAIN_GH, Regions.R_DOMAIN_GH_ASHEN])

        reg_oos = RegionNameCollection()
        reg_oos.addFromList([Regions.R_DOMAIN_GH, Regions.R_DOMAIN_GH_ASHEN])

        reg_ma = RegionNameCollection()
        reg_ma.addFromList([Regions.R_DOMAIN_GH, Regions.R_DOMAIN_GH_ASHEN])

        reg_rb = RegionNameCollection()
        reg_rb.addFromList([Regions.R_DOMAIN_RB, Regions.R_DOMAIN_RB_ASHEN])
        reg_rb_ashen = RegionNameCollection()
        reg_rb_ashen.addFromList([Regions.R_DOMAIN_RB_ASHEN])

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_ISLANDS])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])

        web = WebItemJsonIdentifier(self.x[0], self.x[1], 0)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_ANY, wlc, settings.allowAny > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 0)
        wlc = WebLocationCollection([WebLocation(web, reg_gh, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_CHEST, wlc, settings.allowSimple > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 1)
        wlc = WebLocationCollection([WebLocation(web, reg_oos, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_SKULL, wlc, settings.allowSimple > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 2)
        wlc = WebLocationCollection([WebLocation(web, reg_oos, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_DARK_RELIC, wlc, settings.allowRare > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 3)
        wlc = WebLocationCollection([WebLocation(web, reg_gh, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_ARTIFACT, wlc, settings.allowRare > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 4)
        wlc = WebLocationCollection([WebLocation(web, reg_gh, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_VAULT_KEY, wlc, settings.allowSimple > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 5)
        wlc = WebLocationCollection([WebLocation(web, reg_gh, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_SIREN, wlc, settings.allowRare > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 6)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_MERMAID_GEM, wlc, settings.allowSimple > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 7)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_BREATH_OF_THE_SEA, wlc, settings.allowRare > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 8)
        wlc = WebLocationCollection([WebLocation(web, reg_ma, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_CHEST_ANIMAL_CRATE, wlc, settings.allowSimple > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 9)
        wlc = WebLocationCollection([WebLocation(web, reg_ma, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_CHEST_RESOURCE_CRATE, wlc, settings.allowSimple > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 10)
        wlc = WebLocationCollection([WebLocation(web, reg_ma, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_CHEST_TRADE_GOODS, wlc, settings.allowSimple > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 11)
        wlc = WebLocationCollection([WebLocation(web, reg_ma, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_CHEST_CARGO_GOODS, wlc, settings.allowSimple > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 12)
        wlc = WebLocationCollection([WebLocation(web, reg_ma, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_FIREWORKS, wlc, settings.allowSimple > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 13)
        wlc = WebLocationCollection([WebLocation(web, reg_rb, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_GIFTS, wlc, settings.allowRare > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 14)
        wlc = WebLocationCollection([WebLocation(web, reg_rb, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_EM_FLAG, wlc, settings.allowRare > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 15)
        wlc = WebLocationCollection([WebLocation(web, reg_rb_ashen, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_ASHEN_TOMB, wlc, settings.allowRare > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 16)
        wlc = WebLocationCollection([WebLocation(web, reg_rb, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_REAPER_CHEST, wlc, settings.allowSimple > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 17)
        wlc = WebLocationCollection([WebLocation(web, reg_rb, lgc)])
        self.locations.append(LocDetails(self.L_GS_SELL_BOX_OF_WONDERS, wlc, settings.allowRare > 0))
