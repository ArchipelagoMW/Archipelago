from ...Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ...LocationsBase import LocationsBase
from ....Regions.RegionCollection import RegionNameCollection
from ....Regions.RegionDetails import Regions
from ....Items.Items import Items
from ....Items.ItemReqEvalOr import ItemReqEvalOr
from ....Items.ItemReqEvalAnd import ItemReqEvalAnd
from ....Locations.LocationSettingOption import LocationSettingOption


class SettingsHunterCookedAboard:
    class Any(LocationSettingOption):
        pass

    class Fish(LocationSettingOption):
        CATEGORICAL_NAME = 4
        pass

    class LandMeat(LocationSettingOption):
        pass

    class BigFish(LocationSettingOption):
        pass

    def __init__(self, completeAny=Any.DEFAULT, fishCategory=Fish.DEFAULT, landMeat=LandMeat.DEFAULT,
                 bigFish=BigFish.DEFAULT):
        self.completeAny = completeAny
        self.fishCategory = fishCategory
        self.landMeat = landMeat
        self.bigFish = bigFish

    def getSettingForLocName(self, name: str):
        if name == HunterCookedAboard.L_H_COOK:
            return self.completeAny

        if (name == HunterCookedAboard.L_H_CAT_COOK_SPLASHTAIL or
                name == HunterCookedAboard.L_H_CAT_COOK_PONDIE or
                name == HunterCookedAboard.L_H_CAT_COOK_ISLEHOPPER or
                name == HunterCookedAboard.L_H_CAT_COOK_ANCIENTSCALE or
                name == HunterCookedAboard.L_H_CAT_COOK_PLENTIFIN or
                name == HunterCookedAboard.L_H_CAT_COOK_WILDSPLASH or
                name == HunterCookedAboard.L_H_CAT_COOK_DEVILFISH or
                name == HunterCookedAboard.L_H_CAT_COOK_BATTLEGILL or
                name == HunterCookedAboard.L_H_CAT_COOK_WRECKER or
                name == HunterCookedAboard.L_H_CAT_COOK_STORMFISH):
            return self.fishCategory

        if name == HunterCookedAboard.L_H_CAT_COOK_LAND:
            return self.landMeat

        if name == HunterCookedAboard.L_H_CAT_COOK_BIG:
            return self.bigFish

        # default for it to be enabled
        return 1


class HunterCookedAboard(LocationsBase):
    # cat names
    L_H_CAT_COOK_SPLASHTAIL = "Cook Splashtail (H)"
    L_H_CAT_COOK_PONDIE = "Cook Pondie (H)"
    L_H_CAT_COOK_ISLEHOPPER = "Cook Islehopper (H)"
    L_H_CAT_COOK_ANCIENTSCALE = "Cook Ancientscale (H)"
    L_H_CAT_COOK_PLENTIFIN = "Cook Plentifin (H)"
    L_H_CAT_COOK_WILDSPLASH = "Cook Wildsplash (H)"
    L_H_CAT_COOK_DEVILFISH = "Cook Devilfish (H)"
    L_H_CAT_COOK_BATTLEGILL = "Cook Battlegill (H)"
    L_H_CAT_COOK_WRECKER = "Cook Wrecker (H)"
    L_H_CAT_COOK_STORMFISH = "Cook Stormfish (H)"
    L_H_CAT_COOK_LAND = "Cook Land Creature (H)"
    L_H_CAT_COOK_BIG = "Cook Shark, Megalodon, or Kraken (H)"

    # INDIVIDUAL_NAMES
    L_H_COOK = "Cook Anything (H)"
    L_H_COOK_RubySplashtail = "Cook Ruby Splashtail (H)"
    L_H_COOK_SunnySplashtail = "Cook Sunny Splashtail (H)"
    L_H_COOK_INDS = "Cook Indigo Splashtail (H)"
    L_H_COOK_UMBS = "Cook Umber Splashtail (H)"
    L_H_COOK_SEAS = "Cook Seafoam Splashtail (H)"
    L_H_COOK_TROS = "Cook Trophy Splashtail (H)"
    L_H_COOK_CHAP = "Cook Charcoal Pondie (H)"

    L_H_COOK_OP = "Cook Orchid Pondie (H)"
    L_H_COOK_BROP = "Cook Bronze Pondie (H)"
    L_H_COOK_BRIP = "Cook Bright Pondie (H)"
    L_H_COOK_MOOP = "Cook Moonsky Pondie (H)"
    L_H_COOK_TROP = "Cook Trophy Pondie (H)"
    L_H_COOK_STOI = "Cook Stone Islehopper (H)"
    L_H_COOK_MOSI = "Cook Moss Islehopper (H)"
    L_H_COOK_HONI = "Cook Honey Islehopper (H)"
    L_H_COOK_RAVI = "Cook Raven Islehopper (H)"
    L_H_COOK_AMEI = "Cook Amethyst Islehopper (H)"
    L_H_COOK_TORI = "Cook Trophy Islehopper (H)"
    L_H_COOK_ALMA = "Cook Almond Ancientscale (H)"
    L_H_COOK_SAPA = "Cook Sapphire Ancientscale (H)"
    L_H_COOK_SMOA = "Cook Smoke Ancientscale (H)"
    L_H_COOK_BONA = "Cook Bone Ancientscale (H)"
    L_H_COOK_STAA = "Cook Starshine Ancientscale (H)"
    L_H_COOK_TROA = "Cook Trophy Ancientscale (H)"
    L_H_COOK_OLIP = "Cook Olive Plentifin (H)"
    L_H_COOK_AMBP = "Cook Amber Plentifin (H)"
    L_H_COOK_CLOP = "Cook Cloudy Plentifin (H)"

    def __init__(self, settings: SettingsHunterCookedAboard):
        super().__init__()
        self.x = [3, 0, 1]
        self.settings = settings

        self.add_any_sets()
        self.add_fish_sets()
        self.add_meat_set_land()
        self.add_fish_set_big()

    def add_any_sets(self):
        do_rand: bool = self.settings.completeAny is not self.settings.Any.OFF
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2]), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_H_COOK, wlc, do_rand))

    def add_fish_sets(self):
        self.add_fish_set_pondie()
        self.add_fish_set_splashtail()
        self.add_fish_set_islehopper()
        self.add_fish_set_ancientscale()
        self.add_fish_set_plentifin()
        self.add_fish_set_wildsplash()
        self.add_fish_set_devilfish()
        self.add_fish_set_battlegill()

    def add_land_sets(self):
        self.add_meat_set_land()

    def addFishSetLoc(self, name: str, wlc: WebLocationCollection):
        do_rand: bool = self.settings.fishCategory == SettingsHunterCookedAboard.Fish.ON
        # TODO not implemented

        do_rand: bool = self.settings.fishCategory == SettingsHunterCookedAboard.Fish.CATEGORICAL_NAME
        self.locations.append(LocDetails(name, wlc, do_rand))

        do_rand: bool = self.settings.fishCategory == SettingsHunterCookedAboard.Fish.UNIQUE
        self.addUniques(name, wlc, do_rand)

    def addLandMeatSetLoc(self, name: str, wlc: WebLocationCollection):
        do_rand: bool = self.settings.landMeat == SettingsHunterCookedAboard.LandMeat.ON
        self.locations.append(LocDetails(name, wlc, do_rand))

        do_rand: bool = self.settings.landMeat == SettingsHunterCookedAboard.LandMeat.UNIQUE
        self.addUniques(name, wlc, do_rand)

    def addBigFishLoc(self, name: str, wlc: WebLocationCollection):
        do_rand: bool = self.settings.bigFish == SettingsHunterCookedAboard.BigFish.ON
        self.locations.append(LocDetails(name, wlc, do_rand))

        do_rand: bool = self.settings.bigFish == SettingsHunterCookedAboard.BigFish.UNIQUE
        self.addUniques(name, wlc, do_rand)

    def add_fish_set_pondie(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 6), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 7), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 8), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 9), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 10), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 11), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_COOK_PONDIE, wlc)

    def add_fish_set_splashtail(self) -> None:
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 0), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 1), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 2), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 3), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 4), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 5), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_COOK_SPLASHTAIL, wlc)

    def add_fish_set_islehopper(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 12), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 13), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 14), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 15), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 16), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 17), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_COOK_ISLEHOPPER, wlc)

    def add_fish_set_ancientscale(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 19), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 20), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 21), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 22), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 23), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 24), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_COOK_ANCIENTSCALE, wlc)

    def add_fish_set_plentifin(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 24), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 25), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 26), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 27), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 28), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 29), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_COOK_PLENTIFIN, wlc)

    def add_fish_set_wildsplash(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 30), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 31), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 32), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 33), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 34), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 35), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_COOK_WILDSPLASH, wlc)

    def add_fish_set_devilfish(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 36), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 37), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 38), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 39), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 40), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 41), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_COOK_DEVILFISH, wlc)

    def add_fish_set_battlegill(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 42), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 43), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 44), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 45), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 46), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 47), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_COOK_BATTLEGILL, wlc)

    def add_fish_set_wrecker(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 48), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 49), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 50), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 51), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 52), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 53), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_COOK_WRECKER, wlc)

    def add_fish_set_stormfish(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 54), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 55), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 56), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 57), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 58), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 59), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_COOK_STORMFISH, wlc)

    def add_meat_set_land(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 60), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 61), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 62), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 57), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 58), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 59), reg, lgc),
        ])
        self.addLandMeatSetLoc(self.L_H_CAT_COOK_LAND, wlc)

    def add_fish_set_big(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 63), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 64), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 65), reg, lgc)
        ])
        self.addBigFishLoc(self.L_H_CAT_COOK_BIG, wlc)
