from typing import NamedTuple

from BaseClasses import Entrance

from worlds.generic.Rules import CollectionRule

from .flags import LLFlags
from .options import Badges, LoonylandOptions, Remix


class LoonylandEntrance(Entrance):
    game = "Loonyland"


class LLEntrance(NamedTuple):
    source_region: str
    target_region: str
    is_real_loading_zone: bool
    rule: CollectionRule = lambda state: True
    flags: LLFlags = LLFlags.NONE

    def can_create(self, options: LoonylandOptions) -> bool:
        if options.badges == Badges.option_none and LLFlags.MODE in self.flags:
            return False
        if options.remix == Remix.option_excluded and LLFlags.REMIX in self.flags:
            return False
        return True
