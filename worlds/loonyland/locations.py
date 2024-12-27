from enum import Enum
from typing import NamedTuple

from BaseClasses import Location

from worlds.loonyland.options import Badges, LongChecks, LoonylandOptions, MonsterDolls, MultipleSaves, Remix


class LoonylandLocation(Location):
    game = "Loonyland"


class LLLocCat(Enum):
    PICKUP = 0
    QUEST = 1
    BADGE = 2
    EVENT = 4
    REWARD = 5
    DOLL = 6


class LLLocation(NamedTuple):
    id: int
    category: LLLocCat
    map_id: int
    region: str
    flags: list[str] = []
    base_item: str = ""

    def can_create(self, options: LoonylandOptions) -> bool:
        if self.category == LLLocCat.BADGE and options.badges == Badges.option_none:
            return False
        if options.dolls == MonsterDolls.option_none and (self.category == LLLocCat.DOLL or "DOLL" in self.flags):
            return False
        if options.long_checks == LongChecks.option_excluded and (
            "LONG" in self.flags or ("LONG_VANILLA_BADGES" in self.flags and options.badges == Badges.option_vanilla)
        ):
            return False
        if options.remix == Remix.option_excluded and ("REMIX" in self.flags):
            return False
        if options.multisave == MultipleSaves.option_disabled and ("MULTISAVE" in self.flags):
            return False
        return True

    def in_logic(self, options: LoonylandOptions) -> bool:
        if (self.category == LLLocCat.BADGE and (options.badges == Badges.option_vanilla)) or (
            self.category == LLLocCat.DOLL and (options.dolls == MonsterDolls.option_vanilla)
        ):
            return False
        return True
