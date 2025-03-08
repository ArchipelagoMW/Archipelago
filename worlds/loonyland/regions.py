from typing import NamedTuple

from BaseClasses import Region

from .flags import LLFlags
from .options import Badges, LoonylandOptions, Remix


class LoonylandRegion(Region):
    game = "Loonyland"


class LLRegion(NamedTuple):
    real: bool
    map: str = ""
    flags: LLFlags = LLFlags.NONE

    def can_create(self, options: LoonylandOptions) -> bool:
        if options.badges == Badges.option_none and LLFlags.MODE in self.flags:
            return False
        if options.remix == Remix.option_excluded and LLFlags.REMIX in self.flags:
            return False
        return True
