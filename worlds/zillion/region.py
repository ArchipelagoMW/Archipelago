from typing import Optional
from BaseClasses import MultiWorld, Region, RegionType, Location, Item, CollectionState
from zilliandomizer.logic_components.regions import Region as ZzRegion
from zilliandomizer.logic_components.locations import Location as ZzLocation
from zilliandomizer.logic_components.items import RESCUE
from zilliandomizer.utils import parse_loc_name

from worlds.zillion.item import ZillionItem


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


horizontals = [
    "in left wall",
    "far left",
    "left",
    "left",
    "left-center",  # in split rooms, this col is often occupied by a wall
    "left-center",
    "center-left",
    "center",
    "center",
    "center-right",
    "right-center",
    "right-center",
    "right",
    "right",
    "far right",
    "in right wall",
]


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
        self.hint_text

        # make more readable hint name
        row, col, y, x = parse_loc_name(name)
        vertical = "top" if y <= 0x20 \
            else "top-mid" if y <= 0x40 \
            else "mid" if y <= 0x60 \
            else "bottom-mid" if y <= 0x80 \
            else "bottom"
        horizontal = horizontals[x >> 4]
        self._hint_text = f"row {row} col {col} {vertical} {horizontal}"

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
