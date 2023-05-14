from typing import Set, TYPE_CHECKING, Optional, Dict

from BaseClasses import Region, Location, Item, ItemClassification, Entrance, CollectionState
from .Constants import NOTES, PROG_ITEMS, PHOBEKINS, USEFUL_ITEMS
from .Options import Goal
from .Regions import REGIONS, SEALS, MEGA_SHARDS
from .Shop import SHOP_ITEMS, PROG_SHOP_ITEMS, USEFUL_SHOP_ITEMS, FIGURINES

if TYPE_CHECKING:
    from . import MessengerWorld
else:
    MessengerWorld = object


class MessengerRegion(Region):
    def __init__(self, name: str, world: MessengerWorld) -> None:
        super().__init__(name, world.player, world.multiworld)
        self.add_locations(self.multiworld.worlds[self.player].location_name_to_id)
        world.multiworld.regions.append(self)

    def add_locations(self, name_to_id: Dict[str, int]) -> None:
        for loc in REGIONS[self.name]:
            self.locations.append(MessengerLocation(loc, self, name_to_id.get(loc, None)))
        if self.name == "The Shop":
            if self.multiworld.goal[self.player] > Goal.option_open_music_box:
                self.locations.append(MessengerLocation("Shop Chest", self, name_to_id.get("Shop Chest")))
            if self.multiworld.shop_shuffle[self.player]:
                self.locations += [MessengerShopLocation(f"The Shop - {shop_loc}", self,
                                                         name_to_id.get(f"The Shop - {shop_loc}", None))
                                   for shop_loc in SHOP_ITEMS]
                self.locations += [MessengerShopLocation(figurine, self, name_to_id.get(figurine, None))
                                   for figurine in FIGURINES]
        elif self.name == "Tower HQ":
            if self.multiworld.shop_shuffle[self.player]:
                self.locations.append(MessengerLocation("Money Wrench", self, name_to_id.get("Money Wrench")))
        # putting some dumb special case for searing crags and ToT so i can split them into 2 regions
        if self.multiworld.shuffle_seals[self.player] and self.name in SEALS:
            self.locations += [MessengerLocation(seal_loc, self, name_to_id.get(seal_loc, None))
                               for seal_loc in SEALS[self.name]]
        if self.multiworld.shuffle_shards[self.player] and self.name in MEGA_SHARDS:
            self.locations += [MessengerLocation(shard, self, name_to_id.get(shard, None))
                               for shard in MEGA_SHARDS[self.name]]

    def add_exits(self, exits: Set[str]) -> None:
        for exit in exits:
            ret = Entrance(self.player, f"{self.name} -> {exit}", self)
            self.exits.append(ret)
            ret.connect(self.multiworld.get_region(exit, self.player))


class MessengerLocation(Location):
    game = "The Messenger"

    def __init__(self, name: str, parent: MessengerRegion, loc_id: Optional[int]) -> None:
        super().__init__(parent.player, name, loc_id, parent)
        if loc_id is None:
            self.place_locked_item(MessengerItem(name, parent.player, None))


class MessengerShopLocation(MessengerLocation):
    def cost(self) -> int:
        name = self.name.replace("The Shop - ", "")  # TODO use `remove_prefix` when 3.8 finally gets dropped
        world = self.parent_region.multiworld.worlds[self.player]
        return world.shop_prices.get(name, world.figurine_prices.get(name))

    def can_afford(self, state: CollectionState) -> bool:
        world = state.multiworld.worlds[self.player]
        cost = self.cost() * 2
        if cost >= 1000:
            cost *= 2
        can_afford = state.has("Shards", self.player, cost) or state.has("Shards", self.player, world.total_shards)
        if "Figurine" in self.name:
            return state.has("Money Wrench", self.player) and can_afford
        return can_afford


class MessengerItem(Item):
    game = "The Messenger"

    def __init__(self, name: str, player: int, item_id: Optional[int] = None, override_progression: bool = False,
                 count: int = 0) -> None:
        if item_id is None or override_progression or name in {*NOTES, *PROG_ITEMS, *PHOBEKINS, *PROG_SHOP_ITEMS}:
            item_class = ItemClassification.progression
        elif name in {*USEFUL_ITEMS, *USEFUL_SHOP_ITEMS}:
            item_class = ItemClassification.useful
        else:
            item_class = ItemClassification.filler
        if count >= 100:
            item_class = ItemClassification.progression_skip_balancing
        super().__init__(name, item_class, item_id, player)

