from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.Items import Items
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.ItemReqEvalOr import ItemReqEvalOr

class SettingsFearedQuestSeaForts:

    def __init__(self, completeAny=1, royal=1, imp=1, gold=1, brine=1, traitor=1, mercy=1):
        self.completeAny = completeAny
        self.royal = royal
        self.imp = imp
        self.gold = gold
        self.brine = brine
        self.traitor = traitor
        self.mercy = mercy

    def getSettingForLocName(self, name: str):
        if (name == FearedQuestSeaForts.L_FEARED_COMP_FORTRESS):
            return self.completeAny
        if (name == FearedQuestSeaForts.L_FEARED_COMP_FORTRESS_ROYAL):
            return self.royal
        if (name == FearedQuestSeaForts.L_FEARED_COMP_FORTRESS_IMP):
            return self.imp
        if (name == FearedQuestSeaForts.L_FEARED_COMP_FORTRESS_GOLD):
            return self.gold
        if (name == FearedQuestSeaForts.L_FEARED_COMP_FORTRESS_BRINE):
            return self.brine
        if (name == FearedQuestSeaForts.L_FEARED_COMP_FORTRESS_TRAITOR):
            return self.traitor
        if (name == FearedQuestSeaForts.L_FEARED_COMP_FORTRESS_MERCY):
            return self.mercy

        # default for it to be enabled
        return 1


class FearedQuestSeaForts(LocationsBase):
    L_FEARED_COMP_FORTRESS = "Defeat Sea Fortress"
    L_FEARED_COMP_FORTRESS_ROYAL = "Defeat Royal Crest Fortress"
    L_FEARED_COMP_FORTRESS_IMP = "Defeat Imperial Crown Fortress"
    L_FEARED_COMP_FORTRESS_GOLD = "Defeat Ancient Gold Fortress"
    L_FEARED_COMP_FORTRESS_BRINE = "Defeat Old Brinestone Fortress"
    L_FEARED_COMP_FORTRESS_TRAITOR = "Defeat Traitor's Fate Fortress"
    L_FEARED_COMP_FORTRESS_MERCY = "Defeat Mercy's End Fortress"

    def __init__(self, settings: SettingsFearedQuestSeaForts):
        super().__init__()
        self.x = [4, 17, 1]

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_FORTRESSES])
        lgc = ItemReqEvalOr([ItemReqEvalAnd([Items.sail, Items.voyage_fortress])])

        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2]), reg, lgc)
        ])
        do_rand: bool = settings.completeAny > 0
        self.locations.append(LocDetails(self.L_FEARED_COMP_FORTRESS, wlc, do_rand, do_rand))

        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 0), reg, lgc)
        ])
        do_rand: bool = settings.royal > 0
        self.locations.append(LocDetails(self.L_FEARED_COMP_FORTRESS_ROYAL, wlc, do_rand))

        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 1), reg, lgc)
        ])
        do_rand: bool = settings.imp > 0
        self.locations.append(LocDetails(self.L_FEARED_COMP_FORTRESS_IMP, wlc, do_rand))

        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 2), reg, lgc)
        ])
        do_rand: bool = settings.gold > 0
        self.locations.append(LocDetails(self.L_FEARED_COMP_FORTRESS_GOLD, wlc, do_rand))

        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 3), reg, lgc)
        ])
        do_rand: bool = settings.brine > 0
        self.locations.append(LocDetails(self.L_FEARED_COMP_FORTRESS_BRINE, wlc, do_rand))

        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 4), reg, lgc)
        ])
        do_rand: bool = settings.traitor > 0
        self.locations.append(LocDetails(self.L_FEARED_COMP_FORTRESS_TRAITOR, wlc, do_rand))

        wlc = WebLocationCollection([
            WebLocation(WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 5), reg, lgc)
        ])
        do_rand: bool = settings.mercy > 0
        self.locations.append(LocDetails(self.L_FEARED_COMP_FORTRESS_MERCY, wlc, do_rand))
