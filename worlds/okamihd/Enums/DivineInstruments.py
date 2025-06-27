from typing import TYPE_CHECKING, NamedTuple
from enum import Enum

from BaseClasses import ItemClassification

if TYPE_CHECKING:
    from .. import OkamiWorld

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
