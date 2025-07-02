from typing import TYPE_CHECKING, NamedTuple
from enum import Enum

from BaseClasses import ItemClassification

if TYPE_CHECKING:
    from .. import OkamiWorld

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
    INFERNO = BrushTechniqueData(0x10a, "Inferno")
    VEIL_OF_MIST = BrushTechniqueData(0x10b, "Veil of Mist")
    CATWALK = BrushTechniqueData(0x10c, "Catwalk")
    THUNDERSTORM = BrushTechniqueData(0x10d, "Thunderstorm")
    BLIZZARD = BrushTechniqueData(0x10e, "Blizzard")
    ## UPGRADES/SECRET
    MIST_WARP = BrushTechniqueData(0x10f, "Mist Warp")
    FIREBURST = BrushTechniqueData(0x110, "Fireburst")
    WHIRLWIND = BrushTechniqueData(0x111, "Whirlwind")
    DELUGE = BrushTechniqueData(0x112, "Deluge")
    FOUNTAIN = BrushTechniqueData(0x113, "Fountain")
    THUNDERBOLT = BrushTechniqueData(0x114, "Thunderbolt")
    ## VERY SECRET ONE
    ## I think this is the only "optional" one, every other one is required at least to clear its tutorial ?
    ICESTORM = BrushTechniqueData(0x115, "Icestorm", item_classification=ItemClassification.filler)

    @staticmethod
    def list():
        return list(map(lambda b: b.value, BrushTechniques))
