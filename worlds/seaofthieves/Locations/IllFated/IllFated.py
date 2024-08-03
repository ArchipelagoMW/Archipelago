from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.Items import Items
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.ItemReqEvalOr import ItemReqEvalOr
from ...Locations.LocationSettingOption import LocationSettingOption


class SettingsIllFated:
    class Any(LocationSettingOption):
        pass

    def __init__(self, any=Any.DEFAULT):
        self.any = any


class IllFated(LocationsBase):
    L_ILL_DAMAGE_SHP = "Damage your ship"
    L_ILL_DAMAGE_STORM = "Spend a minute in the storm"
    L_ILL_DAMAGE_FIRE = "Spend a minute on fire"
    L_ILL_DAMAGE_REPAIR = "Repair Ship"
    L_ILL_DAMAGE_BAIL = "Bail Ship"
    L_ILL_DAMAGE_SINK = "Sink"

    def __init__(self, settings: SettingsIllFated):
        super().__init__()
        self.x = [6, 0, 0]
        self.settings = settings

        do_rand: bool = int(self.settings.any) is not SettingsIllFated.Any.OFF
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_PLAYER_SHIP])
        lgc = ItemReqEvalOr([])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2]), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_ILL_DAMAGE_SHP, wlc, do_rand))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_OPEN_SEA])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], 1, self.x[2]), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_ILL_DAMAGE_STORM, wlc, do_rand))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_OPEN_SEA])
        lgc = ItemReqEvalOr([])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], 2, self.x[2]), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_ILL_DAMAGE_FIRE, wlc, do_rand))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_PLAYER_SHIP])
        lgc = ItemReqEvalOr([])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], 3, self.x[2]), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_ILL_DAMAGE_REPAIR, wlc, do_rand))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_PLAYER_SHIP])
        lgc = ItemReqEvalOr([])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], 4, self.x[2]), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_ILL_DAMAGE_BAIL, wlc, do_rand))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_OPEN_SEA])
        lgc = ItemReqEvalOr([])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], 5, self.x[2]), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_ILL_DAMAGE_SINK, wlc, do_rand))
