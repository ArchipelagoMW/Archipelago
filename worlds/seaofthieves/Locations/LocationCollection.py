import random

from .Voyager.IslandVisited import VoyageIslandVisited
from .Voyager.VoyageQuestGh import VoyageQuestGh
from .Voyager.VoyageQuestOos import VoyageQuestOos
from .Voyager.VoyageQuestMa import VoyageQuestMa
from .Voyager.VoyageQuestRor import VoyageQuestRor
from .Voyager.VoyageQuestAthena import VoyageQuestAthena
from .Rouge.RogueQuestAll import RogueQuestAll
from .Feared.FearedQuestSeaForts import FearedQuestSeaForts
from .Menu.QuestMenu import MenuQuestAll
from .Locations import SOTLocation, LocDetails
from .Hunter.ProvisionsCooked import BurntAboard, CookedAboard, Total
from .Hunter.ProvisionsEaten import EatenAboard
from .Seals import Seals
from .Goldseaker import TreasuresSold, Chests
from ..Configurations import SotOptionsDerived
from .Servant import Servant
from .Guardian import Guardian
from .IllFated import IllFated
from .Feared import CannonsFired
from ..Items.Items import Item
from ..Regions.RegionConnectionRules import RegionDiver
from ..Regions.ConnectionDetails import ConnectionDetails
from .Voyager.CaptainShipSpotted import CaptainShipSpotted
from .Voyager import DaysAtSea
from .Voyager import NauticalMilesSailed
from .Voyager import Rowboats
from .Voyager import Shipwrecks
from .Voyager import TallTales
from .Shops import Shops
from .Shop import ShopLocation, Balance
import typing
from .Shop import ShopWarehouse, ShopLocationList, ShopLocation


class LocationDetailsCollection:

    SHOP_DESCRIPTOR = "shop"
    def __init__(self):
        LocDetails.resetSeedId()
        self.options: SotOptionsDerived.SotOptionsDerived = SotOptionsDerived.SotOptionsDerived()

        # this maps Settings Class -> [locName -> LocDets]
        self.checkTypeToLocDetail: typing.Dict[str, typing.Dict[str, LocDetails]] = {}

        self.hintWebLocations: [LocDetails] = []

        self.regionDiver: RegionDiver | None = None

        # TODO this may cause bugs.. we should move the prices out of the shops here somehow to decouple this?
        self.random: random.Random | None = None

        self.shops: typing.Optional[ShopWarehouse] = None


    def applyRegionDiver(self, connection_details: typing.List[ConnectionDetails]):
        self.regionDiver = RegionDiver()
        self.regionDiver.create_from_rules(connection_details)

    def toDict(self) -> typing.Dict[str, int]:
        dic: typing.Dict[str, int] = {}
        for checkTypeKey in self.checkTypeToLocDetail.keys():
            for loc_name in self.checkTypeToLocDetail[checkTypeKey].keys():
                dic[self.checkTypeToLocDetail[checkTypeKey][loc_name].name] = self.checkTypeToLocDetail[checkTypeKey][
                    loc_name].id

        return dic

    def get_accessible_regions_for_items(self, items: typing.Set[str]):
        return self.regionDiver.get_regions_accessbile(items)

    def findDetailsCheckable(self, itemSet: typing.Set[str], forceAll: bool = False) -> typing.List[LocDetails]:

        ret_list: typing.List[LocDetails] = []

        # checks only location requirements, does not include region reqs
        for checkTypeKey in self.checkTypeToLocDetail.keys():
            for loc_name in self.checkTypeToLocDetail[checkTypeKey].keys():

                loc_details = self.checkTypeToLocDetail[checkTypeKey][loc_name]

                # first check if we have access to the region
                accessibleRegions = self.get_accessible_regions_for_items(itemSet)
                loc_region = loc_details.webLocationCollection.getFirstRegion()

                if (forceAll) or (loc_region in accessibleRegions):
                    # then check item logic
                    if (forceAll or loc_details.webLocationCollection.isAnyReachable(itemSet)):
                        ret_list.append(loc_details)

        return ret_list

    def addLocationToSelf(self, location_detail: LocDetails, settingsClass: str):
        if settingsClass not in self.checkTypeToLocDetail.keys():
            self.checkTypeToLocDetail[settingsClass] = {}

        self.checkTypeToLocDetail[settingsClass][location_detail.name] = location_detail

        # if we have a shop item, then we need to inform the shop warehouse
        #if settingsClass == self.SHOP_DESCRIPTOR:
            #self.shops.add_location_detail(location_detail)

    def addHintToSelf(self, location_detail: LocDetails, settingsClass: str):
        self.hintWebLocations.append(location_detail)

    def addLocationsToSelf(self, lst: typing.List[LocDetails], settingsClass: str):
        for i in range(len(lst)):
            self.addLocationToSelf(lst[i], settingsClass)

    def addHintsToSelf(self, lst: typing.List[LocDetails], settingsClass: str):
        for i in range(len(lst)):
            self.addHintToSelf(lst[i], settingsClass)

    def getLocationsForRegion(self, regName: str, player: int) -> typing.List[SOTLocation]:

        if self.shops == None:
            self.shops = ShopWarehouse.ShopWarehouse()



        lst: typing.List[SOTLocation] = []
        for settingString in self.checkTypeToLocDetail.keys():

            for locName in self.checkTypeToLocDetail[settingString].keys():

                loc_det: LocDetails = self.checkTypeToLocDetail[settingString][locName]

                if loc_det.webLocationCollection.getFirstRegion() == regName:
                    if settingString == self.SHOP_DESCRIPTOR:
                        loc: ShopLocation.ShopLocation = ShopLocation.ShopLocation(loc_det, player, regName,
                                                                                   loc_det.cost)
                        self.shops.add_location(loc)
                    else:
                        loc: SOTLocation = SOTLocation(loc_det, player, regName)
                    if not loc_det.doRandomize:
                        loc.progress_type = 3  # excluded
                    lst.append(loc)
        return lst

    def applyOptions(self, options: SotOptionsDerived.SotOptionsDerived, random: random.Random):
        self.options = options
        self.random = random
        return

    def addAll(self) -> None:
        self.addLocationsToSelf(MenuQuestAll().getLocations(), "SettingsMenuQuestAll")
        self.addLocationsToSelf(VoyageQuestGh(self.options.voyageQuestGhSettings).getLocations(),
                                "SettingsVoyageQuestGh")
        self.addLocationsToSelf(VoyageQuestMa(self.options.voyageQuestMaSettings).getLocations(),
                                "SettingsVoyageQuestMa")
        self.addLocationsToSelf(VoyageQuestOos(self.options.voyageQuestOosSettings).getLocations(),
                                "SettingsVoyageQuestOos")
        self.addLocationsToSelf(VoyageQuestRor(self.options.voyageQuestRorSettings).getLocations(),
                                "SettingsVoyageQuestRor")
        self.addLocationsToSelf(VoyageQuestAthena(self.options.voyageQuestAthenaSettings).getLocations(),
                                "SettingsVoyageQuestAthena")

        self.addLocationsToSelf(TreasuresSold.TreasuresSold(self.options.treasureSoldSettings).getLocations(),
                                "SettingsTreasuresSold")
        self.addLocationsToSelf(BurntAboard.HunterBurntAboard(self.options.burntAboardSettings).getLocations(),
                                "SettingsHunterBurntAboard")
        self.addLocationsToSelf(CookedAboard.HunterCookedAboard(self.options.cookedAboardSettings).getLocations(),
                                "SettingsHunterCookedAboard")
        self.addLocationsToSelf(EatenAboard.HunterEatenAboard(self.options.eatenAboardSettings).getLocations(),
                                "SettingsHunterEatenAboard")
        # TODO buggy self.addLocationsToSelf(Total.HunterTotal().getLocations(), "SettingsHunterTotalCooked")
        self.addLocationsToSelf(FearedQuestSeaForts(self.options.fortressSettings).getLocations(),
                                "SettingsFearedQuestSeaForts")
        self.addLocationsToSelf(CannonsFired.CannonsFired(self.options.cannonsFiredSettings).getLocations(),
                                "SettingsCannonsFired")
        self.addLocationsToSelf(RogueQuestAll(self.options.rougeSettings).getLocations(), "SettingsRogueQuestAll")
        self.addLocationsToSelf(Guardian.VoyageQuestGa(self.options.guardianSettings).getLocations(),
                                "SettingsVoyageQuesGa")
        self.addLocationsToSelf(Servant.VoyageQuestSv(self.options.servantSettings).getLocations(),
                                "SettingsVoyageQuesSv")
        self.addLocationsToSelf(IllFated.IllFated(self.options.illFatedSettings).getLocations(), "SettingsIllFated")
        self.addLocationsToSelf(Chests.Chests(self.options.chestSettings).getLocations(), "SettingsChests")
        self.addLocationsToSelf(Seals.Seals().getLocations(), "SettingsSeals")
        self.addLocationsToSelf(CaptainShipSpotted(self.options.captainShipSettings).getLocations(), "cap_ship")
        self.addLocationsToSelf(DaysAtSea.DaysAtSea(self.options.daysAtSeaSettings).getLocations(), "days_at_sea")
        self.addLocationsToSelf(
            NauticalMilesSailed.NauticalMiles(self.options.nauticalMilesSailedSettings).getLocations(), "days_at_sea")
        self.addLocationsToSelf(Rowboats.Rowboats(self.options.rowboatSettings).getLocations(), "rowboats")
        self.addLocationsToSelf(Shipwrecks.Shipwrecks(self.options.shipreckSettings).getLocations(), "shipwrecks")
        self.addLocationsToSelf(TallTales.TallTales(self.options.tallTaleSettings).getLocations(), "tallTales")
        self.addLocationsToSelf(Shops.Shops(self.options.shopsSettings, self.random).getLocations(), self.SHOP_DESCRIPTOR)

        # hints?
        self.addHintsToSelf(VoyageIslandVisited().getLocations(), "HintsIslandsVisited")

        LocDetails.resetSeedId()
        return
