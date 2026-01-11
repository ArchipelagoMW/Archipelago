from enum import Enum

from .Requirement import Requirement
from ...Options import FinalFantasyTacticsIIOptions


class FFTLocation:
    name: str
    requirements: list[Requirement]
    battle_level: int

    def __init__(self, name: "LocationNames", requirements: list[Requirement] = None, battle_level: int = None):
        if requirements is None:
            requirements = list()
        self.name = name.value
        self.requirements = requirements
        assert battle_level is not None, self.name
        self.battle_level = battle_level

    def __repr__(self):
        return f"{self.__class__} -- {self.name}"

    def check_enabled(self, options: FinalFantasyTacticsIIOptions):
        return True

class SidequestLocation(FFTLocation):
    def check_enabled(self, options: FinalFantasyTacticsIIOptions):
        return options.sidequest_battles

class RareBattleLocation(FFTLocation):
    def check_enabled(self, options: FinalFantasyTacticsIIOptions):
        return options.rare_battles

class VanillaFinalFightsLocation(FFTLocation):
    def check_enabled(self, options: FinalFantasyTacticsIIOptions):
        return options.final_battles == options.final_battles.option_vanilla

class AltimaOnlyFinalFightLocation(FFTLocation):
    def check_enabled(self, options: FinalFantasyTacticsIIOptions):
        return options.final_battles == options.final_battles.option_altima_only

class LocationNames(Enum):
    GARILAND_STORY = "Gariland Magic City Story Battle"
    MANDALIA_STORY = "Mandalia Plains Story Battle"
    IGROS_STORY = "Igros Castle Story Battle"
    SWEEGY_STORY = "Sweegy Woods Story Battle"
    DORTER_1_STORY = "Dorter Slums Story Battle"
    DORTER_2_STORY = "Dorter City Story Battle"
    THIEVES_FORT_STORY = "Thieves' Fort Story Battle"
    LENALIA_STORY = "Lenalia Plateau Story Battle"
    ZEAKDEN_STORY = "Fort Zeakden Story Battle"
    GROG_STORY = "Grog Hill Story Battle"
    YARDOW_STORY = "Yardow Fort City Story Battle"
    YUGUO_STORY = "Yuguo Woods Story Battle"
    RIOVANES_1_STORY = "Gate of Riovanes Story Battle"
    RIOVANES_2_STORY = "Inside Riovanes Castle Story Battle"
    RIOVANES_3_STORY = "Roof of Riovanes Castle Story Battle"
    FOVOHAM_STORY = "Fovoham Plains Story Battle"
    ARAGUAY_STORY = "Araguay Woods Story Battle"
    ZIREKILE_STORY = "Zirekile Falls Story Battle"
    ZEKLAUS_STORY = "Zeklaus Desert Story Battle"
    LESALIA_STORY = "Back Gate of Lesalia Castle Story Battle"
    GOLAND_STORY = "Goland Coal City Story Battle"
    DOGUOLA_STORY = "Doguola Pass Story Battle"
    ZALAND_STORY = "Zaland Fort City Story Battle"
    BARIAUS_HILL_STORY = "Bariaus Hill Story Battle"
    LIONEL_1_STORY = "Gate of Lionel Castle Story Battle"
    LIONEL_2_STORY = "Inside of Lionel Castle Story Battle"
    ZIGOLIS_STORY = "Zigolis Swamp Story Battle"
    GOLGORAND_STORY = "Golgorand Execution Site Story Battle"
    BARIAUS_VALLEY_STORY = "Bariaus Valley Story Battle"
    BERVENIA_CITY_STORY = "Bervenia Free City Story Battle"
    FINATH_STORY = "Finath River Story Battle"
    ZELTENNIA_STORY = "Zeltennia Castle Story Battle"
    GERMINAS_STORY = "Germinas Peak Story Battle"
    BETHLA_NORTH_STORY = "Bethla Garrison North Wall Story Battle"
    BETHLA_SOUTH_STORY = "Bethla Garrison South Wall Story Battle"
    BETHLA_SLUICE_STORY = "Bethla Garrison Sluice Story Battle"
    BED_STORY = "Bed Desert Story Battle"
    LIMBERRY_1_STORY = "Limberry Castle Gates Story Battle"
    LIMBERRY_2_STORY = "Inside Limberry Castle Story Battle"
    LIMBERRY_3_STORY = "Limberry Castle Cemetary Story Battle"
    POESKAS_STORY = "Poeskas Lake Story Battle"
    MUROND_TEMPLE_1_STORY = "St. Murond Temple Story Battle"
    MUROND_TEMPLE_2_STORY = "St. Murond Temple Hall Story Battle"
    MUROND_TEMPLE_3_STORY = "Chapel of St. Murond Temple Story Battle"
    UBS_1_STORY = "Underground Book Storage 1 Story Battle"
    UBS_2_STORY = "Underground Book Storage 2 Story Battle"
    UBS_3_STORY = "Underground Book Storage 3 Story Battle"
    UBS_4_STORY = "Underground Book Storage 4 Story Battle"
    UBS_5_STORY = "Underground Book Storage 5 Story Battle"
    GOUG_STORY = "Slums of Goug Story Battle"
    MUROND_DEATH_CITY_STORY = "Murond Death City Story Battle"
    PRECINCTS_STORY = "Lost Sacred Precincts Story Battle"
    AIRSHIPS_1_STORY = "Graveyard of Airships 1 Story Battle"
    AIRSHIPS_2_STORY = "Graveyard of Airships 2 Story Battle"

    GOLAND_1_SIDEQUEST = "Goland Colliery Third Floor Sidequest Battle"
    GOLAND_2_SIDEQUEST = "Goland Colliery Second Floor Sidequest Battle"
    GOLAND_3_SIDEQUEST = "Goland Colliery First Floor Sidequest Battle"
    GOLAND_4_SIDEQUEST = "Goland Underground Passage Sidequest Battle"
    NELVESKA_SIDEQUEST = "Nelveska Temple Sidequest Battle"
    ZARGHIDAS_SIDEQUEST = "Zarghidas Trade City Sidequest Battle"
    NOGIAS_SIDEQUEST = "NOGIAS Sidequest Battle"
    TERMINATE_SIDEQUEST = "TERMINATE Sidequest Battle"
    DELTA_SIDEQUEST = "DELTA Sidequest Battle"
    VALKYRIES_SIDEQUEST = "VALKYRIES Sidequest Battle"
    MLAPAN_SIDEQUEST = "MLAPAN Sidequest Battle"
    TIGER_SIDEQUEST = "TIGER Sidequest Battle"
    BRIDGE_SIDEQUEST = "BRIDGE Sidequest Battle"
    VOYAGE_SIDEQUEST = "VOYAGE Sidequest Battle"
    HORROR_SIDEQUEST = "HORROR Sidequest Battle"
    END_SIDEQUEST = "END Sidequest Battle"

    MANDALIA_RARE = "Mandalia Plains Rare Battle"
    SWEEGY_RARE = "Sweegy Woods Rare Battle"
    LENALIA_RARE = "Lenalia Plateau Rare Battle"
    GROG_RARE = "Grog Hill Rare Battle"
    YUGUO_RARE = "Yuguo Woods Rare Battle"
    FOVOHAM_RARE = "Fovoham Plains Rare Battle"
    ARAGUAY_RARE = "Araguay Woods Rare Battle"
    ZIREKILE_RARE = "Zirekile Falls Rare Battle"
    ZEKLAUS_RARE = "Zeklaus Desert Rare Battle"
    BERVENIA_VOLCANO_RARE = "Bervenia Volvano Rare Battle"
    DOGUOLA_RARE = "Doguola Pass Rare Battle"
    BARIAUS_HILL_RARE = "Bariaus Hill Rare Battle"
    ZIGOLIS_RARE = "Zigolis Swamp Rare Battle"
    BARIAUS_VALLEY_RARE = "Bariaus Valley Rare Battle"
    FINATH_RARE = "Finath River Rare Battle"
    GERMINAS_RARE = "Germinas Peak Rare Battle"
    BED_RARE = "Bed Desert Rare Battle"
    DOLBODAR_RARE = "Dolbodar Swamp Rare Battle"
    POESKAS_RARE = "Poeskas Lake Rare Battle"

    RAD_RECRUIT = "Recruit Rad"
    ALICIA_RECRUIT = "Recruit Alicia"
    LAVIAN_RECRUIT = "Recruit Lavian"
    RAFA_RECRUIT = "Recruit Rafa"
    MALAK_RECRUIT = "Recruit Malak"
    BOCO_RECRUIT = "Recruit Boco"
    BEOWULF_RECRUIT = "Recruit Beowulf"
    WORKER_8_RECRUIT = "Recruit Worker 8"
    AGRIAS_RECRUIT = "Recruit Agrias"
    REIS_DRAGON_RECRUIT = "Recruit Reis (Dragon)"
    REIS_HUMAN_RECRUIT = "Recruit Reis (Human)"
    CLOUD_RECRUIT = "Recruit Cloud"
    ORLANDU_RECRUIT = "Recruit Orlandu"
    MELIADOUL_RECRUIT = "Recruit Meliadoul"
    MUSTADIO_RECRUIT = "Recruit Mustadio"
    BYBLOS_RECRUIT = "Recruit Byblos"

    SQUIRE_UNLOCK = "Squire Unlock"
    CHEMIST_UNLOCK = "Chemist Unlock"
    KNIGHT_UNLOCK = "Knight Unlock"
    ARCHER_UNLOCK = "Archer Unlock"
    THIEF_UNLOCK = "Thief Unlock"
    MONK_UNLOCK = "Monk Unlock"
    PRIEST_UNLOCK = "Priest Unlock"
    WIZARD_UNLOCK = "Wizard Unlock"
    TIME_MAGE_UNLOCK = "Time Mage Unlock"
    SUMMONER_UNLOCK = "Summoner Unlock"
    ORACLE_UNLOCK = "Oracle Unlock"
    MEDIATOR_UNLOCK = "Mediator Unlock"
    GEOMANCER_UNLOCK = "Geomancer Unlock"
    LANCER_UNLOCK = "Lancer Unlock"
    SAMURAI_UNLOCK = "Samurai Unlock"
    NINJA_UNLOCK = "Ninja Unlock"
    CALCULATOR_UNLOCK = "Calculator Unlock"
    BARD_UNLOCK = "Bard Unlock"
    DANCER_UNLOCK = "Dancer Unlock"
    MIME_UNLOCK = "Mime Unlock"

    MANDALIA_SHOP = "Mandalia Plains Shop Unlock"
    LENALIA_SHOP = "Lenalia Plateau Shop Unlock"
    ZEAKDEN_SHOP = "Fort Zeakden Shop Unlock"
    YARDOW_SHOP = "Yardow Fort City Shop Unlock"
    RIOVANES_SHOP = "Riovanes Castle Shop Unlock"
    ZIREKILE_SHOP = "Zirekile Falls Shop Unlock"
    ZEKLAUS_SHOP = "Zeklaus Desert Shop Unlock"
    LESALIA_SHOP = "Lesalia Imperial Capital Shop Unlock"
    BARIAUS_HILL_SHOP = "Bariaus Hill Shop Unlock"
    LIONEL_SHOP = "Lionel Castle Shop Unlock"
    BARIAUS_VALLEY_SHOP = "Bariaus Valley Shop Unlock"
    BETHLA_SHOP = "Bethla Garrison Shop Unlock"
    LIMBERRY_SHOP = "Limberry Castle Shop Unlock"
    ORBONNE_SHOP = "Orbonne Monastery Shop Unlock"

    RAMZA_CHAPTER_2_UNLOCK = "Chapter 2 Ramza Squire Job Unlock"
    RAMZA_CHAPTER_4_UNLOCK = "Chapter 4 Ramza Squire Job Unlock"