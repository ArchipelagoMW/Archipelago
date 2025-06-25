import typing
from enum import IntEnum, Enum, StrEnum
from typing import NamedTuple, Optional, List
from BaseClasses import Location, Item, ItemClassification
from .Options import OkamiOptions


class OkamiLocation(Location):
    game = "Ōkami HD"


class OkamiItem(Item):
    game = "Ōkami HD"


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

    ## Kamiki Village
    ### Exteriors
    STONE_KAMIKI = "Kamiki Village (Stone state)"
    KAMIKI_VILLAGE = "Kamiki Village"
    KAMIKI_ISLANDS = "Kamiki Village Islands"
    ### Interiors
    KUSHIS_HOUSE = "Kushi's house"
    SUSANOS_HOUSE = "Susano's house"
    SUSANOS_UNDERGROUD = "Susano's Secret Underground Meditation Chamber"
    ORANGES_HOUSE = "Mr and Mrs Orange's house"


    ## Shinshu Field
    CURSED_SHINSHU_FIELD = "Cursed Shinshu Field"
    SHINSHU_FIELD = "Shinshu Field"
    SHINSHU_FIELD_AGATA_CAVE="Shinshu Field (Cave to Agata Forest)"
    TAMA_HOUSE="Tama's house"

    ## HANA VALLEY
    CURSED_HANA_VALLEY = "Cursed Hana Valley"
    HANA_VALLEY = "Hana Valley"
    HANA_VALLEY_SAKIGAMI =" Hana Valley - Sakigami sequence"

    ## AGATA FOREST
    CURSED_AGATA_FOREST="Cursed Agata Forest"
    AGATA_FOREST_WAKA="Agata Forest (Pre-waka fight)"
    AGATA_FOREST="Agata Forest"

    ## TUSTA RUINS
    ###
    TSUTA_RUINS="Tsuta Ruins"

    ## TAKA PASS
    CURSED_TAKA_PASS="Curesd Taka pass"


class DivineInstrumentData(NamedTuple):
    code: int
    item_name: str
    tier: int


class DivineInstruments(Enum):
    # MIRRORS
    DIVINE_RETRIBUTION = DivineInstrumentData(0x10, "Divine Retribution", 1)
    SNARLING_BEAST = DivineInstrumentData(0x11, "Snarling Beast", 2)
    INFINITY_JUDGE = DivineInstrumentData(0x12, "Infinity Judge", 3)
    TRINITY_MIRROR = DivineInstrumentData(0x13, "Trinity Mirror", 4)
    SOLAR_FLARE = DivineInstrumentData(0x14, "Solar Flare", 5)

    # ROSARIES
    DEVOUT_BEADS = DivineInstrumentData(0x15, "Devout Beads", 1)
    LIFE_BEADS = DivineInstrumentData(0x16, "Life Beads", 2)
    EXORCISM_BEADS = DivineInstrumentData(0x17, "Exorcism Beads", 3)
    RESURRECTION_BEADS = DivineInstrumentData(0x18, "Resurrection Beads", 4)
    TUNDRA_BEADS = DivineInstrumentData(0x19, "Tundra Beads", 5)

    # SWORDS
    TSUMUGARI = DivineInstrumentData(0x1A, "Tsumugari", 1)
    SEVEN_STRIKE = DivineInstrumentData(0x1B, "Seven Strike", 2)
    BLADE_OF_KUSANAGI = DivineInstrumentData(0x1C, "Blade of Kusanagi", 3)
    EIGHT_WONDER = DivineInstrumentData(0x1D, "Eight Wonder", 4)
    THUNDER_EDGE = DivineInstrumentData(0x1E, "Thunder Edge", 5)

    @staticmethod
    def list():
        return list(map(lambda d: d.value, DivineInstruments))


class BrushTechniqueData(NamedTuple):
    code: int
    item_name: str
    item_count: int = 1
    ## Most powers are progression, except a few ones
    item_classification: ItemClassification = ItemClassification.progression


class BrushTechniques(Enum):
    # MAIN
    SUNRISE = BrushTechniqueData(0x100, "Sunrise", item_classification=ItemClassification.progression)
    REJUVENATION = BrushTechniqueData(0x101, "Rejuvenation", item_classification=ItemClassification.progression)
    POWER_SLASH = BrushTechniqueData(0x102, "Progressive Power Slash", item_count=3,
                                     item_classification=ItemClassification.progression)
    CHERRY_BOMB = BrushTechniqueData(0x103, "Progressive Cherry Bomb", item_count=3,item_classification=ItemClassification.progression)
    GREENSPROUT_BLOOM = BrushTechniqueData(0x104, "Greensprout (Bloom)")
    GREENSPROUT_WATERLILY = BrushTechniqueData(0x105, "Greensprout (Waterlily)",
                                               item_classification=ItemClassification.progression)
    GREENSPROUT_VINE = BrushTechniqueData(0x106, "Greensprout (Vine)")
    WATERSPROUT = BrushTechniqueData(0x107, "Watersprout")
    CRESCENT = BrushTechniqueData(0x108, "Crescent", item_classification=ItemClassification.progression)
    GALESTROM = BrushTechniqueData(0x109, "Galestrom")
    INFERNO = BrushTechniqueData(0x110, "Inferno")
    VEIL_OF_MIST = BrushTechniqueData(0x111, "Veil of Mist")
    CATWALK = BrushTechniqueData(0x112, "Cawalk")
    THUNDERSTORM = BrushTechniqueData(0x113, "Thunderstorm")
    BLIZZARD = BrushTechniqueData(0x114, "Blizzard")
    ## UPGRADES/SECRET
    # MIST_WARP = BrushTechniqueData(0x115, "Mist Warp")
    # FIREBURST = BrushTechniqueData(0x116, "Fireburst")
    # WHIRLWIND = BrushTechniqueData(0x117, "Whirlwind")
    # DELUGE = BrushTechniqueData(0x118, "Deluge")
    # FOUNTAIN = BrushTechniqueData(0x119, "Fountain")
    # THUNDERBOLT = BrushTechniqueData(0x120, "Thunderbolt")
    ## VERY SECRET ONE
    ## I think this is the only "optional" one, every other one is required at least to clear its tutorial ?
    # ICESTORM = BrushTechniqueData(0x121, "Icestorm", item_classification=ItemClassification.filler)

    @staticmethod
    def list():
        return list(map(lambda b: b.value, BrushTechniques))


class EnnemyData(NamedTuple):
    code: int
    name: str
    required_weapon_tier: int
    floral_finisher: BrushTechniques | None = None
    required_techniques: List[BrushTechniques] = []


class OkamiEnnemies(Enum):
    GREEN_IMP = EnnemyData(0x03, "Green Imp", 0, BrushTechniques.POWER_SLASH)
    RED_IMP = EnnemyData(0x00, "Red Imp", 0, BrushTechniques.POWER_SLASH)
    YELLOW_IMP = EnnemyData(0x02, "Yellow Imp", 0, BrushTechniques.POWER_SLASH)
    #Not sure if this is the code for waka 1 or 2
    WAKA_1 = EnnemyData(0x7e, "Waka (Agata Forest)",1)
    BUD_OGRE = EnnemyData(0x4d, "Bud Ogre",1,BrushTechniques.GREENSPROUT_BLOOM,required_techniques=[BrushTechniques.GREENSPROUT_BLOOM])

    @staticmethod
    def list():
        return list(map(lambda b: b.value, BrushTechniques))


class LocData(NamedTuple):
    id: int
    required_brush_techniques: List[BrushTechniques] = []
    power_slash_level: int = 0
    cherry_bomb_level: int = 0
    # 0 => No, 1=> Yes, 2=> Iron Claws
    buried: int = 0
    has_events: [str] = []
    required_items: [str] = []
    mandatory_enemies: List[OkamiEnnemies] = []
    needs_swim: bool = False
    praise_sanity:int=0


class EventData(NamedTuple):
    id: int | None = None
    required_brush_techniques: List[BrushTechniques] = []
    power_slash_level: int = 0
    cherry_bomb_level: int = 0
    # 0 => No, 1=> Yes, 2=> Iron Claws
    buried: int = 0
    override_event_item_name: str | None = None
    has_events: [str] = []
    required_items: [str] = []
    mandatory_enemies: List[OkamiEnnemies] = []
    needs_swim: bool = False
    is_event_item: bool | typing.Callable[[OkamiOptions], bool] = False
    precollected: bool | typing.Callable[[OkamiOptions], bool] = False

class ExitData(NamedTuple):
    name: str
    destination: str
    has_events: [str] = []
    doesnt_have_events: [str] = []
    needs_swim: bool = False
