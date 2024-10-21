from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.ItemReqEvalOr import ItemReqEvalOr


class SettingsTallTales:

    def __init__(self, count=0, include_unique=0):
        self.count = count
        self.include_unique = include_unique


class TallTales(LocationsBase):
    L_TT = "Complete A Tall Tale (TT)"

    L_TT_0 = "Complete The Shroudbreaker (TT)"
    L_TT_1 = "Complete The Cursed Rouge (TT)"
    L_TT_2 = "Complete The Legendary Storyteller (TT)"
    L_TT_3 = "Complete Stars of a Thief (TT)"
    L_TT_4 = "Complete Wild Rose (TT)"
    L_TT_5 = "Complete The Art of the Trickster (TT)"
    L_TT_6 = "Complete The Fate of the Morningstar (TT)"
    L_TT_7 = "Complete Revenge of the Morningstar (TT)"
    L_TT_8 = "Complete Shores of Gold (TT)"
    L_TT_9 = "Complete The Seabound Soul (TT)"
    L_TT_10 = "Complete Heart of Fire (TT)"

    L_TT_11 = "Complete A Pirate's Life (TT)"
    L_TT_12 = "Complete The Sunken Pearl (TT)"
    L_TT_13 = "Complete Captains of the Damned (TT)"
    L_TT_14 = "Complete Dark Brethren (TT)"
    L_TT_15 = "Complete Lords of the Sea (TT)"

    L_TT_16 = "Complete The Journey to Melee Island (TT)"
    L_TT_17 = "Complete The Quest for Guybrush (TT)"
    L_TT_18 = "Complete The Lair of LeChuck (TT)"

    def __init__(self, settings: SettingsTallTales):
        super().__init__()
        self.x = [1, 9, 1]
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_DOMAIN_TT])
        lgc = ItemReqEvalOr([])

        reg_ashen = RegionNameCollection()
        reg_ashen.addFromList([Regions.R_DOMAIN_TT_ASHEN])

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_TT, wlc, settings.count > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 0)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_TT_0, wlc, settings.include_unique > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 1)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_TT_1, wlc, settings.include_unique > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 2)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_TT_2, wlc, settings.include_unique > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 3)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_TT_3, wlc, settings.include_unique > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 4)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_TT_4, wlc, settings.include_unique > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 5)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_TT_5, wlc, settings.include_unique > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 6)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_TT_6, wlc, settings.include_unique > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 7)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_TT_7, wlc, settings.include_unique > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 8)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_TT_8, wlc, settings.include_unique > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 9)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_TT_9, wlc, settings.include_unique > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 10)
        wlc = WebLocationCollection([WebLocation(web, reg_ashen, lgc)])
        self.locations.append(LocDetails(self.L_TT_10, wlc, settings.include_unique > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 11)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_TT_11, wlc, settings.include_unique > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 12)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_TT_12, wlc, settings.include_unique > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 13)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_TT_13, wlc, settings.include_unique > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 14)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_TT_14, wlc, settings.include_unique > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 15)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_TT_15, wlc, settings.include_unique > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 16)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_TT_16, wlc, settings.include_unique > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 17)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_TT_17, wlc, settings.include_unique > 0))

        web = WebItemJsonIdentifier(self.x[0], self.x[1], self.x[2], 18)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_TT_18, wlc, settings.include_unique > 0))
