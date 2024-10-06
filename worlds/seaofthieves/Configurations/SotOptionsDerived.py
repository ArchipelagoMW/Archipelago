import typing

from ..Options import SOTOptions
from ..Locations.Feared import FearedQuestSeaForts, CannonsFired
from ..Locations.Hunter.ProvisionsCooked import BurntAboard
from ..Locations.Hunter.ProvisionsCooked import CookedAboard
from ..Locations.Hunter.ProvisionsEaten import EatenAboard
from ..Locations.Servant import Servant
from ..Locations.Seals import Seals
from ..Locations.Menu import QuestMenu
from ..Locations.Guardian import Guardian
from ..Locations.IllFated import IllFated
from ..Locations.Goldseaker import Chests
from ..Locations.Goldseaker import TreasuresSold
from ..Locations.Voyager import VoyageQuestAthena, VoyageQuestGh, VoyageQuestMa, VoyageQuestOos, VoyageQuestRor
from ..Locations.Rouge import RogueQuestAll
from ..Configurations import Trapsoptions
from ..Locations.Voyager import CaptainShipSpotted, DaysAtSea, NauticalMilesSailed, Rowboats, Shipwrecks, TallTales
from ..Locations.Shops import Shops
from ..Locations.Shop import Balance


class SotOptionsDerived:

    def __init__(self, sotOptions: typing.Optional[SOTOptions] = None):
        self.burntAboardSettings: BurntAboard.SettingsHunterBurntAboard
        self.cookedAboardSettings: CookedAboard.SettingsHunterCookedAboard
        self.eatenAboardSettings: EatenAboard.SettingsHunterEatenAboard
        self.servantSettings: Servant.SettingsVoyageQuestSv
        self.fortressSettings: FearedQuestSeaForts.SettingsFearedQuestSeaForts
        self.sealsSettings: Seals.SettingsSeals
        self.menuSettings: QuestMenu.SettingsMenuQuestAll
        self.guardianSettings: Guardian.SettingsVoyageQuestGa
        self.illFatedSettings: IllFated.SettingsIllFated
        self.cannonsFiredSettings: CannonsFired.SettingsCannonsFired
        self.chestSettings: Chests.SettingsChest

        self.treasureSoldSettings: TreasuresSold.SettingsTreasuresSold
        self.voyageQuestGhSettings: VoyageQuestGh.SettingsVoyageQuestGh
        self.voyageQuestMaSettings: VoyageQuestMa.SettingsVoyageQuestMa
        self.voyageQuestOosSettings: VoyageQuestOos.SettingsVoyageQuestOos
        self.voyageQuestAthenaSettings: VoyageQuestAthena.SettingsVoyageQuestAthena
        self.voyageQuestRorSettings: VoyageQuestRor.SettingsVoyageQuestRor
        self.rougeSettings: RogueQuestAll.SettingsRogueQuestAll

        self.captainShipSettings: CaptainShipSpotted.SettingsCaptainShipSpotted
        self.daysAtSeaSettings: DaysAtSea.SettingsDaysAtSea
        self.nauticalMilesSailedSettings: NauticalMilesSailed.SettingsNauticalMiles
        self.rowboatSettings: Rowboats.SettingsRowboat
        self.shipreckSettings: Shipwrecks.SettingsShipwrecks
        self.tallTaleSettings: TallTales.SettingsTallTales
        self.shopsSettings: Shops.SettingsShops

        self.trapsPercentage: int
        self.player_name: str

        if (sotOptions == None):
            self.burntAboardSettings = BurntAboard.SettingsHunterBurntAboard()
            self.cookedAboardSettings = CookedAboard.SettingsHunterCookedAboard()
            self.eatenAboardSettings = EatenAboard.SettingsHunterEatenAboard()
            self.servantSettings = Servant.SettingsVoyageQuestSv()
            self.fortressSettings = FearedQuestSeaForts.SettingsFearedQuestSeaForts()
            self.sealsSettings = Seals.SettingsSeals()
            self.menuSettings = QuestMenu.SettingsMenuQuestAll()
            self.guardianSettings = Guardian.SettingsVoyageQuestGa()
            self.illFatedSettings = IllFated.SettingsIllFated()
            self.rougeSettings = RogueQuestAll.SettingsRogueQuestAll()
            self.cannonsFiredSettings = CannonsFired.SettingsCannonsFired()
            self.chestSettings = Chests.SettingsChest()
            self.treasureSoldSettings = TreasuresSold.SettingsTreasuresSold()
            self.voyageQuestGhSettings = VoyageQuestGh.SettingsVoyageQuestGh()
            self.voyageQuestMaSettings = VoyageQuestMa.SettingsVoyageQuestMa()
            self.voyageQuestOosSettings = VoyageQuestOos.SettingsVoyageQuestOos()
            self.voyageQuestAthenaSettings = VoyageQuestAthena.SettingsVoyageQuestAthena()
            self.voyageQuestRorSettings = VoyageQuestRor.SettingsVoyageQuestRor()

            self.captainShipSettings = CaptainShipSpotted.SettingsCaptainShipSpotted()
            self.daysAtSeaSettings = DaysAtSea.SettingsDaysAtSea()
            self.nauticalMilesSailedSettings = NauticalMilesSailed.SettingsNauticalMiles()
            self.rowboatSettings = Rowboats.SettingsRowboat()
            self.shipreckSettings = Shipwrecks.SettingsShipwrecks()
            self.tallTaleSettings = TallTales.SettingsTallTales()
            self.shopsSettings = Shops.SettingsShops()

            self.trapsPercentage = 3  # put this in a better place?
            self.experimentals: bool = False
            self.screenCapture: bool = False
            self.player_name = ""
        else:
            self.burntAboardSettings = self.__getBurntAboardSettings(sotOptions)
            self.cookedAboardSettings = self.__getCookedAboardSettings(sotOptions)
            self.eatenAboardSettings = self.__getEatenAboardSettings(sotOptions)
            self.servantSettings = self.__getServantSettings(sotOptions)
            self.fortressSettings = self.__getFortressSettings(sotOptions)
            self.sealsSettings = self.__getSealsSettings(sotOptions)
            self.menuSettings = self.__getMenuSettings(sotOptions)
            self.guardianSettings = self.__getGuadianSettings(sotOptions)
            self.illFatedSettings = self.__getIllFatedSettings(sotOptions)
            self.rougeSettings = self.__getRougeSettings(sotOptions)
            self.cannonsFiredSettings = self.__getCannonsFiredSettings(sotOptions)
            self.chestSettings = self.__getChestSettings(sotOptions)
            self.treasureSoldSettings = TreasuresSold.SettingsTreasuresSold()
            self.voyageQuestGhSettings = self.__getVoyageEmGhSettings(sotOptions)
            self.voyageQuestMaSettings = self.__getVoyageEmMaSettings(sotOptions)
            self.voyageQuestOosSettings = self.__getVoyageEmOosSettings(sotOptions)
            self.voyageQuestAthenaSettings = self.__getVoyageEmAfSettings(sotOptions)
            self.voyageQuestRorSettings = self.__getVoyageEmRorSettings(sotOptions)

            self.captainShipSettings = self.__getCaptainShipSpottedSettings(sotOptions)
            self.daysAtSeaSettings = self.__getDaysAtSeaSettings(sotOptions)
            self.nauticalMilesSailedSettings = self.__getNauticalMilesSettings(sotOptions)
            self.rowboatSettings = self.__getRowboatSettings(sotOptions)
            self.shipreckSettings = self.__getShipwreckSettings(sotOptions)
            self.tallTaleSettings = self.__getTallTaleSettings(sotOptions)
            self.shopsSettings = self.__getShopSettings(sotOptions)

            self.trapsPercentage = sotOptions.trapsPercentage.value
            self.experimentals = bool(sotOptions.experimentals.value)
            self.screenCapture = bool(sotOptions.screenCapture.value)
            self.player_name = ""

            # options without a ui element created

    def __getCaptainShipSpottedSettings(self, sotOptions: SOTOptions):

        any: int = int((sotOptions.captainShipSpotted.value == 1))
        sloop: int = int((sotOptions.captainShipSpotted.value == 2))
        brig: int = int((sotOptions.captainShipSpotted.value == 2))
        gal: int = int((sotOptions.captainShipSpotted.value == 2))

        return CaptainShipSpotted.SettingsCaptainShipSpotted(any, sloop, brig, gal)

    def __getNauticalMilesSettings(self, sotOptions: SOTOptions):

        any: int = int((sotOptions.captainShipSpotted.value == 1))

        return NauticalMilesSailed.SettingsNauticalMiles(any)

    def __getDaysAtSeaSettings(self, sotOptions: SOTOptions):

        count: int = int((sotOptions.daysAtSea.value == 1))

        return DaysAtSea.SettingsDaysAtSea(count)

    def __getRowboatSettings(self, sotOptions: SOTOptions):

        count: int = int((sotOptions.rowboats.value == 1))
        lantern: int = int((sotOptions.rowboats.value == 2))
        harpoon: int = int((sotOptions.rowboats.value == 2))
        cannon: int = int((sotOptions.rowboats.value == 2))

        return Rowboats.SettingsRowboat(count, lantern, harpoon, cannon)

    def __getShipwreckSettings(self, sotOptions: SOTOptions):

        count: int = int((sotOptions.shipwrecks.value == 1))

        return Shipwrecks.SettingsShipwrecks(count)

    def __getTallTaleSettings(self, sotOptions: SOTOptions):

        any: int = int((sotOptions.tallTales.value == 1))
        uniques: int = int((sotOptions.tallTales.value == 2))

        return TallTales.SettingsTallTales(any, uniques)

    def __getShopSettings(self, sotOptions: SOTOptions):

        count: int = int(sotOptions.shopSanity.value)
        low_cost: Balance.Balance = Balance.Balance(0, 0, 0)
        high_cost: Balance.Balance = Balance.Balance(0, 50, 10000)

        return Shops.SettingsShops(shop_item_number=count, cost_low=low_cost, cost_high=high_cost)

    def __getChestSettings(self, sotOptions: SOTOptions):
        # gh_count: int = sotOptions.sellSettingsGh
        # ma_count: int = sotOptions.sellSettingsMa
        # oos_count: int = sotOptions.sellSettingsOos
        # af_count: int = sotOptions.sellSettingsAf
        # rb_count: int = sotOptions.sellSettingsRb

        # return Chests.SettingsChest(gh_count, ma_count, oos_count, rb_count, af_count)
        return Chests.SettingsChest(0, 0, 0, 0, 0)

    def __getRougeSettings(self, sotOptions: SOTOptions):
        should_include: int = int(sotOptions.playerShip.value)

        if should_include >= 1:
            return RogueQuestAll.SettingsRogueQuestAll(1, 1, 1, 1)
        else:
            return RogueQuestAll.SettingsRogueQuestAll(0, 0, 0, 0)

    def __getVoyageEmGhSettings(self, sotOptions: SOTOptions):
        voyage_count: int = int(sotOptions.voyageEmGh.value)

        if voyage_count == -1:
            return VoyageQuestGh.SettingsVoyageQuestGh(1, 0, 0, 0, 0, 0, 0)
        elif voyage_count == 0:
            return VoyageQuestGh.SettingsVoyageQuestGh(0, 0, 0, 0, 0, 0, 0)

        a = voyage_count >= 1
        b = voyage_count >= 2
        c = voyage_count >= 3
        d = voyage_count >= 4
        e = voyage_count >= 5
        f = voyage_count >= 6
        return VoyageQuestGh.SettingsVoyageQuestGh(0, a, b, c, d, e, f)

    def __getVoyageEmRorSettings(self, sotOptions: SOTOptions):
        voyage_count: int = int(sotOptions.voyageEmRoar.value)

        if voyage_count == -1:
            return VoyageQuestRor.SettingsVoyageQuestRor(1, 0, 0)
        elif voyage_count == 0:
            return VoyageQuestRor.SettingsVoyageQuestRor(0, 0, 0)

        a = voyage_count >= 1
        b = voyage_count >= 2
        c = voyage_count >= 3
        d = voyage_count >= 4
        e = voyage_count >= 5
        return VoyageQuestRor.SettingsVoyageQuestRor(0, a, b, c, d, e)

    def __getVoyageEmMaSettings(self, sotOptions: SOTOptions):
        voyage_count: int = int(sotOptions.voyageEmMa.value)

        if voyage_count == -1:
            return VoyageQuestMa.SettingsVoyageQuestMa(1, 0, 0)
        elif voyage_count == 0:
            return VoyageQuestMa.SettingsVoyageQuestMa(0, 0, 0)

        a = voyage_count >= 1
        b = voyage_count >= 2
        return VoyageQuestMa.SettingsVoyageQuestMa(0, a, b)

    def __getVoyageEmOosSettings(self, sotOptions: SOTOptions):
        voyage_count: int = int(sotOptions.voyageEmOos.value)

        if voyage_count == -1:
            return VoyageQuestOos.SettingsVoyageQuestOos(1, 0, 0, 0)
        elif voyage_count == 0:
            return VoyageQuestOos.SettingsVoyageQuestOos(0, 0, 0, 0)

        a = voyage_count >= 1
        b = voyage_count >= 2
        c = voyage_count >= 3
        return VoyageQuestOos.SettingsVoyageQuestOos(0, a, b, c)

    def __getVoyageEmAfSettings(self, sotOptions: SOTOptions):
        voyage_count: int = int(sotOptions.voyageEmAf.value)

        # we are including the skull of destiny in here always
        if voyage_count == -1:
            return VoyageQuestAthena.SettingsVoyageQuestAthena(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        elif voyage_count == 0:
            return VoyageQuestAthena.SettingsVoyageQuestAthena(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        a = voyage_count >= 1
        b = voyage_count >= 2
        c = voyage_count >= 3
        d = voyage_count >= 4
        e = voyage_count >= 5
        f = voyage_count >= 6
        g = voyage_count >= 7
        h = voyage_count >= 8
        i = voyage_count >= 9
        j = voyage_count >= 10  # Always include skull? TODO

        return VoyageQuestAthena.SettingsVoyageQuestAthena(0, a, b, c, d, e, f, g, h, i, j)

    def __getCannonsFiredSettings(self, sotOptions: SOTOptions):

        balls: int = int(sotOptions.cannonSanityBalls)
        cursed: int = int(sotOptions.cannonSanityCursed)
        phantom: int = int(sotOptions.cannonSanityPhantom)

        return CannonsFired.SettingsCannonsFired(balls, cursed, phantom)

    def __getIllFatedSettings(self, sotOptions: SOTOptions):
        return IllFated.SettingsIllFated(sotOptions.illFated)

    def __getGuadianSettings(self, sotOptions: SOTOptions):
        compAny: int
        sloop: int
        brig: int
        gal: int

        if (sotOptions.guardianSanity == 2):
            compAny = 0
            sloop = 1
            brig = 1
            gal = 1
        elif (sotOptions.guardianSanity == 1):
            compAny = 1
            sloop = 0
            brig = 0
            gal = 0
        else:
            compAny = 0
            sloop = 0
            brig = 0
            gal = 0

        return Guardian.SettingsVoyageQuestGa(compAny, sloop, brig, gal)

    def __getMenuSettings(self, sotOptions: SOTOptions):
        sealCount: int = sotOptions.sealCount
        return QuestMenu.SettingsMenuQuestAll(sealCount)

    def __getSealsSettings(self, sotOptions: SOTOptions):
        return Seals.SettingsSeals()

    def __getFortressSettings(self, sotOptions: SOTOptions):
        completeAny: int = 0
        royal: int = 0
        imp: int = 0
        gold: int = 0
        brine: int = 0
        traitor: int = 0
        mercy: int = 0

        if (sotOptions.fortressSanity == 0):
            pass
        elif (sotOptions.fortressSanity == 1):
            completeAny = 1
        elif (sotOptions.fortressSanity == 2):
            royal = 1
            imp = 1
            gold = 1
            brine = 1
            traitor = 1
            mercy = 1

        return FearedQuestSeaForts.SettingsFearedQuestSeaForts(completeAny, royal, imp, gold, brine, traitor, mercy)

    def __getBurntAboardSettings(self, sotOptions: SOTOptions):
        compAny: int = 1
        fish: int = int(sotOptions.burnSanityFish)
        seamonster: int = int(sotOptions.burnSanitySeamonster)
        landAnimal: int = int(sotOptions.burnSanityLandAnimal)

        # if we have foodsanity on, we dont want a generic check if we want specific things
        if (fish + seamonster + landAnimal > 0):
            compAny = 0

        return BurntAboard.SettingsHunterBurntAboard(compAny, fish, landAnimal, seamonster)

    def __getCookedAboardSettings(self, sotOptions: SOTOptions):
        compAny: int = 1
        fish: int = int(sotOptions.cookSanityFish)
        seamonster: int = int(sotOptions.cookSanitySeamonster)
        landAnimal: int = int(sotOptions.cookSanityLandAnimal)

        # if we have foodsanity on, we dont want a generic check if we want specific things
        if (fish + seamonster + landAnimal > 0):
            compAny = 0

        return CookedAboard.SettingsHunterCookedAboard(compAny, fish, landAnimal, seamonster)

    def __getEatenAboardSettings(self, sotOptions: SOTOptions):
        compAny: int = 1
        fish: int = int(sotOptions.foodSanityFish)
        seamonster: int = int(sotOptions.foodSanitySeamonster)
        landAnimal: int = int(sotOptions.foodSanityLandAnimal)
        bug: int = int(sotOptions.foodSanityBug)
        fruit: int = int(sotOptions.foodSanityFruit)

        # if we have foodsanity on, we dont want a generic check if we want specific things
        if (fish + seamonster + landAnimal + bug + fruit > 0):
            compAny = 0

        return EatenAboard.SettingsHunterEatenAboard(compAny, fish, landAnimal, seamonster, fruit, bug)

    def __getServantSettings(self, sotOptions: SOTOptions):
        compAny: int
        sloop: int
        brig: int
        gal: int

        if (sotOptions.servantSanity == 2):
            compAny = 0
            sloop = 1
            brig = 1
            gal = 1
        elif (sotOptions.servantSanity == 1):
            compAny = 1
            sloop = 0
            brig = 0
            gal = 0
        else:
            compAny = 0
            sloop = 0
            brig = 0
            gal = 0

        return Servant.SettingsVoyageQuestSv(compAny, sloop, brig, gal)
