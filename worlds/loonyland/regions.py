from typing import NamedTuple, Optional

from BaseClasses import Region, MultiWorld
from .entrances import LoonylandEntrance

from .flags import LLFlags
from .options import Badges, LoonylandOptions, Remix

class LLRegion(NamedTuple):
    real: bool
    map: str = ""
    flags: LLFlags = LLFlags.NONE
    map_id: int = -1

    def can_create(self, options: LoonylandOptions) -> bool:
        if options.badges == Badges.option_none and LLFlags.MODE in self.flags:
            return False
        if options.remix == Remix.option_excluded and LLFlags.REMIX in self.flags:
            return False
        return True


class LoonylandRegion(Region):
    game = "Loonyland"
    llregion: LLRegion
    entrance_type = LoonylandEntrance

    def __init__(self, name: str, player: int, multiworld: MultiWorld, llregion: LLRegion, hint: Optional[str] = None):
        super().__init__(name, player, multiworld)
        self.llregion = llregion



