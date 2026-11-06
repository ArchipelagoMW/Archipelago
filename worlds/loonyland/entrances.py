from typing import NamedTuple

from BaseClasses import Entrance

from worlds.generic.Rules import CollectionRule

from .flags import LLFlags
from .options import Badges, LoonylandOptions, Remix

class LLEntrance(NamedTuple):
    entrance_name: str
    source_region: str
    target_exit: str
    rule: CollectionRule = lambda state: True
    flags: LLFlags = LLFlags.NONE
    id: int = 0

    def can_create(self, options: LoonylandOptions) -> bool:
        if options.badges == Badges.option_none and LLFlags.MODE in self.flags:
            return False
        if options.remix == Remix.option_excluded and LLFlags.REMIX in self.flags:
            return False
        return True

class LoonylandEntrance(Entrance):
    game = "Loonyland"
    llData: LLEntrance