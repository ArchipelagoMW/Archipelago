'''


This data is redudnant with the other pages, so i am leaving it here just in case

from ...Items import Items
from ..Locations import LocDetails
from BaseClasses import Location
class VoyageQuestSettings:

    def __init__(self, playerNumber, gh = 1, oos = 1, ma = 1, af = 1, gilded = 0, mercenary = 0):
        self.playerNumber: int = playerNumber
        self.GH_voyage_req = gh
        self.OOS_voyage_req = oos
        self.MA_voyage_req = ma
        self.AF_voyage_req = af
        self.GILDED_voyage_req = gilded
        self.MERCENARY_voyage_req = mercenary


class VoyageQuest():

    locations = []

    L_VOYAGE_COMP_GH = "Complete Gold Hoarders Voyage"
    L_VOYAGE_COMP_OOS = "Complete Order of Souls Voyage"
    L_VOYAGE_COMP_MA = "Complete Merchant Alliance Voyage"
    L_VOYAGE_COMP_AF = "Complete Athena's Fortune Voyage"
    L_VOYAGE_COMP_GILDED = "Complete Gilded Voyage"
    L_VOYAGE_COMP_MERCENARY = "Complete Mercenary Voyage"

    def __init__(self, voyageQuestSettings: VoyageQuestSettings):

        if(voyageQuestSettings.GH_voyage_req > 0):
            self.locations.append(LocDetails(self.L_VOYAGE_COMP_GH))
        if (voyageQuestSettings.OOS_voyage_req > 0):
            self.locations.append(LocDetails(self.L_VOYAGE_COMP_OOS))
        if (voyageQuestSettings.MA_voyage_req > 0):
            self.locations.append(LocDetails(self.L_VOYAGE_COMP_MA))
        if (voyageQuestSettings.AF_voyage_req > 0):
            self.locations.append(LocDetails(self.L_VOYAGE_COMP_AF))
        if (voyageQuestSettings.GILDED_voyage_req > 0):
            self.locations.append(LocDetails(self.L_VOYAGE_COMP_GILDED))
        if (voyageQuestSettings.MERCENARY_voyage_req > 0):
            self.locations.append(LocDetails(self.L_VOYAGE_COMP_MERCENARY))

    def getLocations(self):
        return self.locations'''
