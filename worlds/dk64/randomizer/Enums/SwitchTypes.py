"""Switch Type enum."""

from enum import IntEnum, auto


class SwitchType(IntEnum):
    """Switch type enum."""

    PadMove = auto()
    GunSwitch = auto()
    InstrumentPad = auto()
    SlamSwitch = auto()
    MiscActivator = auto()
    PushableButton = auto()
    GunInstrumentCombo = auto()
