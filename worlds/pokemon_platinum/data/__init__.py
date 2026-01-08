# THIS IS AN AUTO-GENERATED FILE. DO NOT MODIFY.
# data_gen_templates/__init__.py
#
# Copyright (C) 2025 James Petersen <m@jamespetersen.ca>
# Licensed under MIT. See LICENSE

from enum import StrEnum

class Hm(StrEnum):
    CUT = "HM01 Cut"
    FLY = "HM02 Fly"
    SURF = "HM03 Surf"
    STRENGTH = "HM04 Strength"
    DEFOG = "HM05 Defog"
    ROCK_SMASH = "HM06 Rock Smash"
    WATERFALL = "HM07 Waterfall"
    ROCK_CLIMB = "HM08 Rock Climb"
    FLASH = "TM70 Flash"

    def badge_item(self) -> str | None:
        match self:
            case Hm.CUT: return "Forest Badge"
            case Hm.FLY: return "Cobble Badge"
            case Hm.SURF: return "Fen Badge"
            case Hm.STRENGTH: return "Mine Badge"
            case Hm.DEFOG: return "Relic Badge"
            case Hm.ROCK_SMASH: return "Coal Badge"
            case Hm.WATERFALL: return "Beacon Badge"
            case Hm.ROCK_CLIMB: return "Icicle Badge"
            case _: return None
