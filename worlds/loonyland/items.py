from enum import Enum
from typing import NamedTuple

from BaseClasses import Item, ItemClassification

from worlds.loonyland.options import Badges, LongChecks, LoonylandOptions, MonsterDolls, Remix


class LoonylandItem(Item):
    """
    Item from the game Loonyland
    """

    game: str = "Loonyland"


class LLItemCat(Enum):
    ITEM = 0
    CHEAT = 1
    FILLER = 2
    TRAP = 3
    EVENT = 4
    ACCESS = 5
    DOLL = 6


class LLItem(NamedTuple):
    id: int
    category: LLItemCat
    classification: ItemClassification
    frequency: int = 1
    flags: list[str] = []

    def can_create(self, options: LoonylandOptions) -> bool:
        if (
            self.category == LLItemCat.CHEAT
            and (options.badges == Badges.option_none or options.badges == Badges.option_vanilla)
        ) or (
            self.category == LLItemCat.DOLL
            and (options.dolls == MonsterDolls.option_none or options.dolls == MonsterDolls.option_vanilla)
        ):
            return False
        if options.long_checks == LongChecks.option_excluded and ("OP" in self.flags):
            return False
        if options.remix == Remix.option_excluded and ("REMIX" in self.flags):
            return False
        return True
