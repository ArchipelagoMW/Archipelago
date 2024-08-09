import typing

from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.ItemReqEvalOr import ItemReqEvalOr
from ...Locations.LocationSettingOption import LocationSettingOption
from ...Locations.ScreenData import ScreenData


class SettingsCannonsFired:
    class Balls(LocationSettingOption):
        pass

    class CursedBalls(LocationSettingOption):
        pass

    class PhantomBalls(LocationSettingOption):
        pass

    def __init__(self, defaultBalls=Balls.DEFAULT, cursedBalls=CursedBalls.DEFAULT, phantomBalls=PhantomBalls.DEFAULT):
        self.defaultBalls = defaultBalls
        self.cursedBalls = cursedBalls
        self.phantomBalls = phantomBalls


class CannonsFired(LocationsBase):
    L_ILL_CANN_DEFAULT = "Fire any Cannonball"
    L_ILL_CANN_CURSED = "Fire any Cursed Cannonball"
    L_ILL_CANN_PHANT = "Fire any Phantom Cannonball"

    ANCHOR = "Fire Anchorball"
    BALLAST = "Fire Ballastball"
    BARREL = "Fire Barrelball"
    BLUNDERBOMB = "Fire Blunderbomb"
    CANNONBALL = "Fire Cannonball"
    CHAINSHOT = "Fire Chainshot"
    FIREBOMB = "Fire Firebomb"
    FLAMEPHANTOM = "Fire Flame Phantom Cannonball"
    GROG = "Fire Grogball from ship"
    HELM = "Fire Helmball from ship"
    JIG = "Fire Jigball from ship"
    LIMP = "Fire Limpball from ship"
    PEACE = "Fire Peaceball from ship"
    PET = "Fire Pets from ship"
    PHANTOM = "Fire Phantom Cannonball"
    PLAYER = "Fire Players from ship"
    RIG = "Fire Riggingball from ship"
    VENOM = "Fire Venomball from ship"
    WEARY = "Fire Wearyball from ship"
    WRAITH = "Fire Wraith Cannonball"
    BONE_CALLER = "Fire Bone Caller"
    SCATTERSHOT = "Fire Scattershot"

    web_locs: typing.Dict[str, WebLocation] = {}

    def __init__(self, settings: SettingsCannonsFired):
        super().__init__()
        self.x = [4, 0, 1]
        self.settings = settings

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_CANNONS])
        lgc = ItemReqEvalOr([])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 3), reg, lgc, CannonsFired.BLUNDERBOMB,
                        ScreenData(["Unload Blunderbomb"])),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 4), reg, lgc, CannonsFired.BONE_CALLER,
                        ScreenData(["Unload Bone Caller"])),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 5), reg, lgc, CannonsFired.CANNONBALL,
                        ScreenData(["Unload Cannonball"])),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 6), reg, lgc, CannonsFired.CHAINSHOT,
                        ScreenData(["Unload Chainshot"])),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 7), reg, lgc, CannonsFired.FIREBOMB,
                        ScreenData(["Unload Firebomb"])),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 18), reg, lgc, CannonsFired.SCATTERSHOT,
                        ScreenData(["Unload Scattershot"]))
        ])

        do_rand: bool = self.settings.defaultBalls is SettingsCannonsFired.Balls.ON
        self.locations.append(LocDetails(self.L_ILL_CANN_DEFAULT, wlc, do_rand))

        do_rand: bool = self.settings.defaultBalls is SettingsCannonsFired.Balls.UNIQUE
        self.addUniques(self.L_ILL_CANN_DEFAULT, wlc, do_rand)

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_CANNONS])
        lgc = ItemReqEvalOr([])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 8), reg, lgc, CannonsFired.FLAMEPHANTOM,
                        ScreenData(["Unload Flame"])),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 15), reg, lgc, CannonsFired.PHANTOM,
                        ScreenData(["Unload Phant"])),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 21), reg, lgc, CannonsFired.WRAITH,
                        ScreenData(["Unload Wraith"]))
        ])

        do_rand: bool = self.settings.phantomBalls is SettingsCannonsFired.PhantomBalls.ON
        self.locations.append(LocDetails(self.L_ILL_CANN_PHANT, wlc, do_rand))

        do_rand: bool = self.settings.phantomBalls is SettingsCannonsFired.PhantomBalls.UNIQUE
        self.addUniques(self.L_ILL_CANN_PHANT, wlc, do_rand)

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHIP_CANNONS])
        lgc = ItemReqEvalOr([])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 0), reg, lgc, CannonsFired.ANCHOR,
                        ScreenData(["Unload Anch"])),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 1), reg, lgc, CannonsFired.BALLAST,
                        ScreenData(["Unload Ball"])),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 2), reg, lgc, CannonsFired.BARREL,
                        ScreenData(["Unload Barr"])),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 9), reg, lgc, CannonsFired.GROG,
                        ScreenData(["Unload Grog"])),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 10), reg, lgc, CannonsFired.HELM,
                        ScreenData(["Unload Helm"])),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 11), reg, lgc, CannonsFired.JIG,
                        ScreenData(["Unload Jig"])),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 12), reg, lgc, CannonsFired.LIMP,
                        ScreenData(["Unload Limp"])),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 13), reg, lgc, CannonsFired.PEACE,
                        ScreenData(["Unload Peace"])),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 17), reg, lgc, CannonsFired.RIG,
                        ScreenData(["Unload Rig"])),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 19), reg, lgc, CannonsFired.VENOM,
                        ScreenData(["Unload Ven"])),
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 19), reg, lgc, CannonsFired.WEARY,
                        ScreenData(["Unload Wea"])),
        ])

        do_rand: bool = self.settings.cursedBalls is SettingsCannonsFired.CursedBalls.ON
        self.locations.append(LocDetails(self.L_ILL_CANN_CURSED, wlc, do_rand))

        do_rand: bool = self.settings.cursedBalls is SettingsCannonsFired.CursedBalls.UNIQUE
        self.addUniques(self.L_ILL_CANN_CURSED, wlc, do_rand)
