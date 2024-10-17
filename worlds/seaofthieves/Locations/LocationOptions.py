from .Feared import FearedQuestSeaForts
from .Hunter.ProvisionsCooked import BurntAboard, CookedAboard, Total
from .Hunter.ProvisionsEaten import EatenAboard
from .Menu import QuestMenu
from .Rouge import RogueQuestAll

from .Voyager import VoyageQuestAthena, VoyageQuestGh, VoyageQuestMa, VoyageQuestOos, VoyageQuestRor
from ..Options import SOTOptions
from .Seals import Seals


class LocationOptions:

    def __init__(self, o: SOTOptions):
        self.SettingsFearedQuestSeaForts: FearedQuestSeaForts.SettingsFearedQuestSeaForts = FearedQuestSeaForts.SettingsFearedQuestSeaForts(
            o.fortressSanity
        )

        self.SettingsHunterBurntAboard: BurntAboard.SettingsHunterBurntAboard = BurntAboard.SettingsHunterBurntAboard(
            o.burnSanity,
            o.includeFish and o.burnSanity,
            o.includeFarm and o.burnSanity,
            o.includeSeaMonster and o.burnSanity
        )
        self.SettingsHunterCookedAboard: CookedAboard.SettingsHunterCookedAboard = CookedAboard.SettingsHunterCookedAboard(
            o.cookSanity,
            o.includeFish and o.cookSanity,
            o.includeFarm and o.cookSanity,
            o.includeSeaMonster and o.cookSanity
        )
        self.SettingsHunterTotalCooked: Total.SettingsHunterTotalCooked = Total.SettingsHunterTotalCooked(
            o.cookSanity
        )

        self.SettingsHunterEatenAboard: EatenAboard.SettingsHunterEatenAboard = EatenAboard.SettingsHunterEatenAboard(
            o.foodSanity,
            o.includeFish and o.foodSanity,
            o.includeFarm and o.foodSanity,
            o.includeSeaMonster and o.foodSanity,
            o.foodSanity,
            o.foodSanity
        )

        self.SettingsMenuQuestAll: QuestMenu.SettingsMenuQuestAll = QuestMenu.SettingsMenuQuestAll()

        self.SettingsRogueQuestAll: RogueQuestAll.SettingsRogueQuestAll = RogueQuestAll.SettingsRogueQuestAll(
            o.playerShipSanity,
            o.playerShipSanity,
            o.playerShipSanity,
            o.playerShipSanity
        )

        self.SettingsVoyageQuestAthena: VoyageQuestAthena.SettingsVoyageQuestAthena = VoyageQuestAthena.SettingsVoyageQuestAthena(
            o.voyageOnceAf
        )
        self.SettingsVoyageQuestGh: VoyageQuestGh.SettingsVoyageQuestGh = VoyageQuestGh.SettingsVoyageQuestGh(
            o.voyageOnceGh
        )
        self.SettingsVoyageQuestMa: VoyageQuestMa.SettingsVoyageQuestMa = VoyageQuestMa.SettingsVoyageQuestMa(
            o.voyageOnceMa
        )
        self.SettingsVoyageQuestOos: VoyageQuestOos.SettingsVoyageQuestOos = VoyageQuestOos.SettingsVoyageQuestOos(
            o.voyageOnceOos
        )
        self.SettingsVoyageQuestRor: VoyageQuestRor.SettingsVoyageQuestRor = VoyageQuestRor.SettingsVoyageQuestRor()

        self.SettingsSeals: Seals.SettingsSeals = Seals.SettingsSeals(
            o.emGhPrice,
            o.emMaPrice,
            o.emOosPrice,
            o.emAfPrice,
            o.emRbPrice
        )
