from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.ItemReqEvalOr import ItemReqEvalOr
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.Items import Items
import random
from ..Shop.Balance import Balance


class SettingsShops:
    SHOP_MAX = 4

    class MinMax:
        min: int = 0
        max: int = 0

        def __init__(self):
            self.min = 0
            self.max = 0

    def __init__(self, shop_count=7, shop_item_number=4, cost_low=Balance(), cost_high=Balance()):
        self.shop_count: int = shop_count
        self.shop_item_number: int = shop_item_number
        self.cost_low: Balance = cost_low
        self.cost_high: Balance = cost_high


class Shops(LocationsBase):
    L_SHOP_AS_OUTPOST = "Ancient Spire Outpost Shop"
    L_SHOP_DT_OUTPOST = "Dagger Tooth Outpost Shop"
    L_SHOP_GG_OUTPOST = "Galleon's Grave Outpost Shop"
    L_SHOP_MP_OUTPOST = "Morrow's Peak Outpost Shop"
    L_SHOP_P_OUTPOST = "Plunder Outpost Shop"
    L_SHOP_S_OUTPOST = "Sanctuary Outpost Shop"

    def __init__(self, settings: SettingsShops, random: random.Random):
        super().__init__()
        self.x = [0, 0, 0, -1]
        self.settings = settings
        self.random = random

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHOP_ANCIENT_SPIRE])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.cat_as])])

        web = WebItemJsonIdentifier(0, 0, 0, 0, None, False)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])

        for i in range(self.settings.SHOP_MAX):
            doRand: bool = (i < self.settings.shop_item_number)
            self.locations.append(
                LocDetails(self.L_SHOP_AS_OUTPOST + " " + str(i + 1), wlc, doRand, cost=self.get_balance()))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHOP_DAGGER_TOOTH])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.cat_dt])])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        for i in range(self.settings.SHOP_MAX):
            doRand: bool = (i < self.settings.shop_item_number)
            self.locations.append(
                LocDetails(self.L_SHOP_DT_OUTPOST + " " + str(i + 1), wlc, doRand, doRand, cost=self.get_balance()))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHOP_GALLEONS_GRAVE])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.cat_gg])])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        for i in range(self.settings.SHOP_MAX):
            doRand: bool = (i < self.settings.shop_item_number)
            self.locations.append(
                LocDetails(self.L_SHOP_GG_OUTPOST + " " + str(i + 1), wlc, doRand, cost=self.get_balance()))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHOP_MORROWS_PEAK])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.cat_mp])])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        for i in range(self.settings.SHOP_MAX):
            doRand: bool = (i < self.settings.shop_item_number)
            self.locations.append(
                LocDetails(self.L_SHOP_MP_OUTPOST + " " + str(i + 1), wlc, doRand, cost=self.get_balance()))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHOP_PLUNDER_OUTPOST])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.cat_p])])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        for i in range(self.settings.SHOP_MAX):
            doRand: bool = (i < self.settings.shop_item_number)
            self.locations.append(
                LocDetails(self.L_SHOP_P_OUTPOST + " " + str(i + 1), wlc, doRand, cost=self.get_balance()))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHOP_SANCTUARY_OUTPOST])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.cat_s])])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        for i in range(self.settings.SHOP_MAX):
            doRand: bool = (i < self.settings.shop_item_number)
            self.locations.append(
                LocDetails(self.L_SHOP_S_OUTPOST + " " + str(i + 1), wlc, doRand, cost=self.get_balance()))

    def roundPrice(self, low_val: int, high_val: int):
        val = self.random.randint(low_val, high_val)
        if val > 500:
            val -= val // 100
        elif val > 100:
            val -= val // 50
        elif val > 50:
            val -= val // 25
        else:
            val -= val // 5
        return val

    def get_balance(self):
        balance = Balance(self.roundPrice(self.settings.cost_low.ancient_coins, self.settings.cost_high.ancient_coins),
                    self.roundPrice(self.settings.cost_low.dabloons, self.settings.cost_high.dabloons),
                    self.roundPrice(self.settings.cost_low.gold, self.settings.cost_high.gold))
        return balance
