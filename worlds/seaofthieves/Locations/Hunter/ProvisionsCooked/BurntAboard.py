from ...Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ...LocationsBase import LocationsBase
from ....Regions.RegionCollection import RegionNameCollection
from ....Regions.RegionDetails import Regions
from ....Items.Items import Items
from ....Locations.LocationSettingOption import LocationSettingOption
from ....Items.ItemReqEvalOr import ItemReqEvalOr
from ....Items.ItemReqEvalAnd import ItemReqEvalAnd
from enum import Enum


class SettingsHunterBurntAboard:
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
        if name == HunterBurntAboard.L_H_BURN:
            return self.completeAny

        if (name == HunterBurntAboard.L_H_CAT_BURN_SPLASHTAIL or
                name == HunterBurntAboard.L_H_CAT_BURN_PONDIE or
                name == HunterBurntAboard.L_H_CAT_BURN_ISLEHOPPER or
                name == HunterBurntAboard.L_H_CAT_BURN_ANCIENTSCALE or
                name == HunterBurntAboard.L_H_CAT_BURN_PLENTIFIN or
                name == HunterBurntAboard.L_H_CAT_BURN_WILDSPLASH or
                name == HunterBurntAboard.L_H_CAT_BURN_DEVILFISH or
                name == HunterBurntAboard.L_H_CAT_BURN_BATTLEGILL or
                name == HunterBurntAboard.L_H_CAT_BURN_WRECKER or
                name == HunterBurntAboard.L_H_CAT_BURN_STORMFISH):
            return self.fishCategory

        if name == HunterBurntAboard.L_H_CAT_BURN_LAND:
            return self.landMeat

        if name == HunterBurntAboard.L_H_CAT_BURN_BIG:
            return self.bigFish

        # default for it to be enabled
        return 1


class HunterBurntAboard(LocationsBase):
    L_H_BURN = "Burn Anything (H)"

    # cat names
    L_H_CAT_BURN_SPLASHTAIL = "Burn Splashtail (H)"
    L_H_CAT_BURN_PONDIE = "Burn Pondie (H)"
    L_H_CAT_BURN_ISLEHOPPER = "Burn Islehopper (H)"
    L_H_CAT_BURN_ANCIENTSCALE = "Burn Ancientscale (H)"
    L_H_CAT_BURN_PLENTIFIN = "Burn Plentifin (H)"
    L_H_CAT_BURN_WILDSPLASH = "Burn Wildsplash (H)"
    L_H_CAT_BURN_DEVILFISH = "Burn Devilfish (H)"
    L_H_CAT_BURN_BATTLEGILL = "Burn Battlegill (H)"
    L_H_CAT_BURN_WRECKER = "Burn Wrecker (H)"
    L_H_CAT_BURN_STORMFISH = "Burn Stormfish (H)"
    L_H_CAT_BURN_LAND = "Burn Land Creature (H)"
    L_H_CAT_BURN_BIG = "Burn Shark, Megalodon, or Kraken (H)"

    def __init__(self, settings: SettingsHunterBurntAboard):
        super().__init__()
        self.x = [3, 0, 2]
        self.settings = settings

        self.add_any_sets()
        self.add_fish_sets()
        self.add_meat_set_land()
        self.add_fish_set_big()

    def add_any_sets(self):
        do_rand: bool = self.settings.completeAny is not self.settings.Any.OFF
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2]), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_H_BURN, wlc, do_rand))

    def add_fish_sets(self):
        self.add_fish_set_pondie()
        self.add_fish_set_splashtail()
        self.add_fish_set_islehopper()
        self.add_fish_set_ancientscale()
        self.add_fish_set_plentifin()
        self.add_fish_set_wildsplash()
        self.add_fish_set_devilfish()
        self.add_fish_set_battlegill()
        self.add_fish_set_wrecker()

    def add_land_sets(self):
        self.add_meat_set_land()

    def addFishSetLoc(self, name: str, wlc: WebLocationCollection):
        setting = int(self.settings.fishCategory)

        do_rand: bool = setting == SettingsHunterBurntAboard.Fish.ON
        # TODO not implemented

        do_rand: bool = setting == SettingsHunterBurntAboard.Fish.CATEGORICAL_NAME
        self.locations.append(LocDetails(name, wlc, do_rand))

        do_rand: bool = setting == SettingsHunterBurntAboard.Fish.UNIQUE
        self.addUniques(name, wlc, do_rand)

    def addLandMeatSetLoc(self, name: str, wlc: WebLocationCollection):
        setting = int(self.settings.landMeat)
        do_rand: bool = setting == SettingsHunterBurntAboard.LandMeat.ON
        self.locations.append(LocDetails(name, wlc, do_rand))

        do_rand: bool = setting == SettingsHunterBurntAboard.LandMeat.UNIQUE
        self.addUniques(name, wlc, do_rand)

    def addBigFishLoc(self, name: str, wlc: WebLocationCollection):
        setting = int(self.settings.bigFish)
        do_rand: bool = setting == SettingsHunterBurntAboard.BigFish.ON
        self.locations.append(LocDetails(name, wlc, do_rand))

        do_rand: bool = setting == SettingsHunterBurntAboard.BigFish.UNIQUE
        self.addUniques(name, wlc, do_rand)

    def add_fish_set_pondie(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 6), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 7), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 8), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 9), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 10), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 11), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_BURN_PONDIE, wlc)

    def add_fish_set_splashtail(self) -> None:
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 0), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 1), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 2), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 3), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 4), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 5), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_BURN_SPLASHTAIL, wlc)

    def add_fish_set_islehopper(self) -> None:
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 12), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 13), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 14), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 15), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 16), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 17), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_BURN_ISLEHOPPER, wlc)

    def add_fish_set_ancientscale(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 19), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 20), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 21), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 22), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 23), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 24), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_BURN_ANCIENTSCALE, wlc)

    def add_fish_set_plentifin(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 24), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 25), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 26), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 27), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 28), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 29), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_BURN_PLENTIFIN, wlc)

    def add_fish_set_wildsplash(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 30), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 31), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 32), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 33), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 34), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 35), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_BURN_WILDSPLASH, wlc)

    def add_fish_set_devilfish(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 36), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 37), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 38), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 39), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 40), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 41), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_BURN_DEVILFISH, wlc)

    def add_fish_set_battlegill(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 42), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 43), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 44), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 45), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 46), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 47), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_BURN_BATTLEGILL, wlc)

    def add_fish_set_wrecker(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 48), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 49), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 50), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 51), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 52), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 53), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_BURN_WRECKER, wlc)

    def add_fish_set_stormfish(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 54), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 55), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 56), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 57), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 58), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 59), reg, lgc),
        ])
        self.addFishSetLoc(self.L_H_CAT_BURN_STORMFISH, wlc)

    def add_meat_set_land(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 60), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 61), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 62), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 57), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 58), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 59), reg, lgc),
        ])
        self.addLandMeatSetLoc(self.L_H_CAT_BURN_LAND, wlc)

    def add_fish_set_big(self):
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_COOKER])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.fishing_rod])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 63), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 64), reg, lgc),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 65), reg, lgc)
        ])
        self.addBigFishLoc(self.L_H_CAT_BURN_BIG, wlc)
