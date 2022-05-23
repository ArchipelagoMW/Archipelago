from typing import Dict, Optional
from BaseClasses import MultiWorld, Region, RegionType, Location, Item, CollectionState
from zilliandomizer.logic_components.regions import Region as ZzRegion
from zilliandomizer.logic_components.locations import Location as ZzLocation
from zilliandomizer.logic_components.items import RESCUE
from zilliandomizer.randomizer import Randomizer as ZzRandomizer
from zilliandomizer.generator import some_options

from worlds.zillion.item import ZillionItem
from .config import base_id


class ZillionRegion(Region):
    zz_r: ZzRegion

    def __init__(self,
                 zz_r: ZzRegion,
                 name: str,
                 type_: RegionType,
                 hint: str,
                 player: int,
                 world: Optional[MultiWorld] = None) -> None:
        super().__init__(name, type_, hint, player, world)
        self.zz_r = zz_r


class ZillionLocation(Location):
    zz_loc: ZzLocation
    game: str = "Zillion"

    def __init__(self,
                 zz_loc: ZzLocation,
                 player: int,
                 name: str = '',
                 address: Optional[int] = None,
                 parent: Optional[Region] = None) -> None:
        super().__init__(player, name, address, parent)
        self.zz_loc = zz_loc

    # override
    def can_fill(self, state: CollectionState, item: Item, check_access: bool = True) -> bool:
        saved_gun_req = -1
        if isinstance(item, ZillionItem) \
                and item.zz_item.code == RESCUE \
                and self.player == item.player:
            # RESCUE removes the gun requirement from a location.
            saved_gun_req = self.zz_loc.req.gun
            self.zz_loc.req.gun = 0
        super_result = super().can_fill(state, item, check_access)
        if saved_gun_req != -1:
            self.zz_loc.req.gun = saved_gun_req
        return super_result


# TODO: remove this, replacing it with static resource
# that is verified in unit tests to match zilliandomizer
def make_location_map() -> Dict[str, int]:
    zz_randomizer = ZzRandomizer(some_options)

    location_name_to_id = {
        name: i
        for i, name in enumerate(zz_randomizer.locations, base_id)
    }

    return location_name_to_id
