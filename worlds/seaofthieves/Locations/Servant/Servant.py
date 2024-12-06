from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.Items import Items
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.ItemReqEvalOr import ItemReqEvalOr
from ...Locations.LocationSettingOption import LocationSettingOption


class SettingsVoyageQuestSv:
    class Any(LocationSettingOption):
        pass

    class Sloop(LocationSettingOption):
        pass

    class Brig(LocationSettingOption):
        pass

    class Gal(LocationSettingOption):
        pass

    def __init__(self, any=Any.DEFAULT, sloop=Sloop.DEFAULT, brig=Brig.DEFAULT, gal=Gal.DEFAULT):
        self.any = any
        self.sloop = sloop
        self.brig = brig
        self.gal = gal


class VoyageQuestSv(LocationsBase):
    L_SERV_GUARDIANS_SUNK = "As a Servant, sink a guardian"
    L_SERV_GUARDIANS_SUNK_SLOOP = "As a Servant, sink a Guardian Galleon (SV)"
    L_SERV_GUARDIANS_SUNK_BRIG = "As a Servant, Sink a Guardian Brigantine (SV)"
    L_SERV_GUARDIANS_SUNK_GALL = "As a Servant, Sink a Guardian Sloop (SV)"

    def __init__(self, settings: SettingsVoyageQuestSv):
        super().__init__()
        self.x = [8, 0, 1]
        self.settings = settings

        do_rand: bool = self.settings.any is not SettingsVoyageQuestSv.Any.OFF
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_SV])
        lgc = ItemReqEvalOr(
            [ItemReqEvalAnd([Items.ship_weapons, Items.personal_weapons, Items.sail, Items.emissary_rb])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], 0), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_SERV_GUARDIANS_SUNK_SLOOP, wlc, do_rand))

        do_rand: bool = self.settings.sloop is not SettingsVoyageQuestSv.Sloop.OFF
        lgc = ItemReqEvalOr(
            [ItemReqEvalAnd([Items.ship_weapons, Items.personal_weapons, Items.sail, Items.emissary_rb])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 2), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_SERV_GUARDIANS_SUNK_SLOOP, wlc, do_rand))

        do_rand: bool = self.settings.brig is not SettingsVoyageQuestSv.Brig.OFF
        lgc = ItemReqEvalOr(
            [ItemReqEvalAnd([Items.ship_weapons, Items.personal_weapons, Items.sail, Items.emissary_rb])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 1), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_SERV_GUARDIANS_SUNK_BRIG, wlc, do_rand))

        do_rand: bool = self.settings.gal is not SettingsVoyageQuestSv.Gal.OFF
        lgc = ItemReqEvalOr(
            [ItemReqEvalAnd([Items.ship_weapons, Items.personal_weapons, Items.sail, Items.emissary_rb])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 0), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_SERV_GUARDIANS_SUNK_GALL, wlc, do_rand))
