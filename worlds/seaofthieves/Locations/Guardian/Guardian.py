from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.Items import Items
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.ItemReqEvalOr import ItemReqEvalOr
from ...Locations.LocationSettingOption import LocationSettingOption


class SettingsVoyageQuestGa:
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


class VoyageQuestGa(LocationsBase):
    L_SERV_GUARDIANS_SUNK = "As a Guardian, sink a Servant"
    L_SERV_GUARDIANS_SUNK_SLOOP = "As a Guardian, sink a Servant Galleon (SV)"
    L_SERV_GUARDIANS_SUNK_BRIG = "As a Guardian, Sink a Servant Brigantine (SV)"
    L_SERV_GUARDIANS_SUNK_GALL = "As a Guardian, Sink a Servant Sloop (SV)"

    def __init__(self, settings: SettingsVoyageQuestGa):
        super().__init__()
        self.x = [7, 0, 1]
        self.settings = settings

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_GF])
        lgc = ItemReqEvalOr(
            [ItemReqEvalAnd([Items.ship_weapons, Items.personal_weapons, Items.sail, Items.emissary_af])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], 0), reg, lgc)
        ])
        self.locations.append(
            LocDetails(self.L_SERV_GUARDIANS_SUNK_SLOOP, wlc, self.settings.any is not SettingsVoyageQuestGa.Any.OFF))

        lgc = ItemReqEvalOr(
            [ItemReqEvalAnd([Items.ship_weapons, Items.personal_weapons, Items.sail, Items.emissary_af])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 2), reg, lgc)
        ])
        self.locations.append(LocDetails(self.L_SERV_GUARDIANS_SUNK_SLOOP, wlc,
                                         self.settings.sloop is not SettingsVoyageQuestGa.Sloop.OFF))

        lgc = ItemReqEvalOr(
            [ItemReqEvalAnd([Items.ship_weapons, Items.personal_weapons, Items.sail, Items.emissary_af])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 1), reg, lgc)
        ])
        self.locations.append(
            LocDetails(self.L_SERV_GUARDIANS_SUNK_BRIG, wlc, self.settings.brig is not SettingsVoyageQuestGa.Brig.OFF))

        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.ship_weapons, Items.personal_weapons, Items.sail])])
        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 0), reg, lgc)
        ])
        self.locations.append(
            LocDetails(self.L_SERV_GUARDIANS_SUNK_GALL, wlc, self.settings.gal is not SettingsVoyageQuestGa.Gal.OFF))
