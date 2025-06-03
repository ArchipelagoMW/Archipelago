from enum import IntEnum, Enum, StrEnum
from typing import NamedTuple, Optional, List
from BaseClasses import Location, Item, ItemClassification


class OkamiLocation(Location):
    game = "Okami"


class OkamiItem(Item):
    game = "Okami"


class ItemData(NamedTuple):
    code: Optional[int]
    classification: ItemClassification


class RegionNames(StrEnum):
    MENU = "Menu"

    # Eastern Nippon

    ## Cursed Kamiki
    CURSED_KAMIKI = "Cursed Kamiki"

    ## River of the Heavens
    RIVER_OF_THE_HEAVENS_KAMIKI = "River of the Heavens (Kamiki side)"
    RIVER_OF_THE_HEAVENS_NAGI = "River of the Heavens (Nagi side)"

    ## Cave of Nagi
    CAVE_OF_NAGI = "Cave of Nagi"
    CAVE_OF_NAGI_TACHIGAMI = "Cave of Nagi (Tachigami sequence)"

    ## Kamiki Village Exteriors
    STONE_KAMIKI = "Kamiki Village (Stone state)"
    KAMIKI_VILLAGE = "Kamiki Village"
    KAMIKI_ISLANDS = "Kamiki Village Islands"


class BrushTechniqueData(NamedTuple):
    code: int
    item_name: str
    item_count: int = 1
    ## Most powers are progression, except a few ones
    item_classification: ItemClassification = ItemClassification.progression


class BrushTechniques(Enum):
    # MAIN
    SUNRISE = BrushTechniqueData(0x100, "Sunrise",item_classification=ItemClassification.progression)
    REJUVENATION = BrushTechniqueData(0x101, "Rejuvenation",item_classification=ItemClassification.progression)
    POWER_SLASH = BrushTechniqueData(0x102, "Progressive Power Slash", item_count=1,item_classification=ItemClassification.progression)
    #CHERRY_BOMB = BrushTechniqueData(0x103, "Progressive Cherry Bomb", item_count=3)
    #GREENSPROUT_BLOOM = BrushTechniqueData(0x104, "Greensprout (Bloom)")
    GREENSPROUT_WATERLILY = BrushTechniqueData(0x105, "Greensprout (Waterlily)",item_classification=ItemClassification.progression)
    #GREENSPROUT_VINE = BrushTechniqueData(0x106, "Greensprout (Vine)")
    #WATERSPROUT = BrushTechniqueData(0x107, "Watersprout")
    CRESCENT = BrushTechniqueData(0x108, "Crescent",item_classification=ItemClassification.progression)
    #GALESTROM = BrushTechniqueData(0x109, "Galestrom")
    #INFERNO = BrushTechniqueData(0x110, "Inferno")
    #VEIL_OF_MIST = BrushTechniqueData(0x111, "Veil of Mist")
    #CATWALK = BrushTechniqueData(0x112, "Cawalk")
    #THUNDERSTORM = BrushTechniqueData(0x113, "Thunderstorm")
    #BLIZZARD = BrushTechniqueData(0x114, "Blizzard")
    ## UPGRADES/SECRET
    #MIST_WARP = BrushTechniqueData(0x115, "Mist Warp")
    #FIREBURST = BrushTechniqueData(0x116, "Fireburst")
    #WHIRLWIND = BrushTechniqueData(0x117, "Whirlwind")
    #DELUGE = BrushTechniqueData(0x118, "Deluge")
    #FOUNTAIN = BrushTechniqueData(0x119, "Fountain")
    #THUNDERBOLT = BrushTechniqueData(0x120, "Thunderbolt")
    ## VERY SECRET ONE
    ## I think this is the only "optional" one, every other one is required at least to clear its tutorial ?
    #ICESTORM = BrushTechniqueData(0x121, "Icestorm", item_classification=ItemClassification.filler)

    @staticmethod
    def list():
        return list(map(lambda b: b.value, BrushTechniques))


class LocData(NamedTuple):
    id: int
    required_brush_techniques: List[BrushTechniques] = []
    power_slash_level: int = 0
    cherry_bomb_level: int = 0
    # 0 => No, 1=> Yes, 2=> Iron Claws
    buried_chest: int = 0


class EventData(NamedTuple):
    id:int  = 0
    required_brush_techniques: List[BrushTechniques] = []
    power_slash_level: int = 0
    cherry_bomb_level: int = 0
    # 0 => No, 1=> Yes, 2=> Iron Claws
    buried_chest: int = 0
    override_event_item_name: str | None = None


class ExitData(NamedTuple):
    name: str
    destination: str
    has_events: [str] = []
    doesnt_have_events: [str] = []
    needs_swim: bool = False
