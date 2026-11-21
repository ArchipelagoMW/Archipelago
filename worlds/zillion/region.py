from typing_extensions import override

from zilliandomizer.logic_components.regions import Region as ZzRegion
from zilliandomizer.logic_components.locations import Location as ZzLocation
from zilliandomizer.logic_components.items import RESCUE

from BaseClasses import MultiWorld, Region, Location, Item, CollectionState

from .id_maps import loc_name_to_id
from .item import ZillionItem


class ZillionRegion(Region):
    zz_r: ZzRegion

    def __init__(self, zz_r: ZzRegion,
                 name: str,
                 hint: str,
                 player: int,
                 multiworld: MultiWorld) -> None:
        super().__init__(name, player, multiworld, hint)
        self.zz_r = zz_r


class ZillionLocation(Location):
    zz_loc: ZzLocation
    game: str = "Zillion"

    def __init__(self,
                 zz_loc: ZzLocation,
                 player: int,
                 name: str,
                 parent: Region | None = None) -> None:
        loc_id = loc_name_to_id[name]
        super().__init__(player, name, loc_id, parent)
        self.zz_loc = zz_loc

    @override
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
