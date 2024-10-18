from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.Items import Items
from ...Items.ItemReqEvalAnd import ItemReqEvalAnd
from ...Items.ItemReqEvalOr import ItemReqEvalOr
from ..ScreenData import ScreenData


class SettingsRogueQuestAll:

    def __init__(self, seaShanty=1, grog=1, sleeping=1, sitting=1):
        self.seaShanty = seaShanty
        self.grog = grog
        self.sleeping = sleeping
        self.sitting = sitting


class RogueQuestAll(LocationsBase):
    SHANTY = "Play music for 1 minute (ROUGE)"
    GROG = "Drink 1 grog (ROUGE)"
    SLEEP = "Sleep for 1 minute (ROUGE)"
    SIT = "Sit for 1 minute (ROUGE)"

    def __init__(self, settings: SettingsRogueQuestAll):
        super().__init__()
        self.x = [5, 0, 0]
        reg = RegionNameCollection()
        reg.addFromList([Regions.R_PLAYER_SHIP])
        lgc = ItemReqEvalOr([])

        # TODO we are forcing these to be true because there is not enough locations otherwise?

        web = WebItemJsonIdentifier(self.x[0], 0, self.x[2])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc, RogueQuestAll.SHANTY, ScreenData(["Becalmed"]))])
        self.locations.append(LocDetails(RogueQuestAll.SHANTY, wlc, settings.seaShanty > 0))

        web = WebItemJsonIdentifier(self.x[0], 1, self.x[2])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc, RogueQuestAll.GROG, ScreenData(["Refill"]))])
        self.locations.append(LocDetails(RogueQuestAll.GROG, wlc, settings.grog > 0))

        web = WebItemJsonIdentifier(self.x[0], 2, self.x[2])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc, RogueQuestAll.SLEEP, ScreenData(["Sleep", "Wake"]))])
        self.locations.append(LocDetails(RogueQuestAll.SLEEP, wlc, settings.sleeping > 0))

        web = WebItemJsonIdentifier(self.x[0], 3, self.x[2])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc, RogueQuestAll.SIT, ScreenData(["Take a Seat"]))])
        self.locations.append(LocDetails(RogueQuestAll.SIT, wlc, settings.sitting > 0))
