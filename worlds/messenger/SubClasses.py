from typing import TYPE_CHECKING, Optional

from BaseClasses import Region, Location, Item, ItemClassification, CollectionState
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
        locations = [loc for loc in REGIONS[self.name]]
        if self.name == "The Shop":
            if self.multiworld.goal[self.player] > Goal.option_open_music_box:
                locations.append("Shop Chest")
            shop_locations = {f"The Shop - {shop_loc}": world.location_name_to_id[f"The Shop - {shop_loc}"]
                              for shop_loc in SHOP_ITEMS}
            shop_locations.update(**{figurine: world.location_name_to_id[figurine] for figurine in FIGURINES})
            self.add_locations(shop_locations, MessengerShopLocation)
        elif self.name == "Tower HQ":
            locations.append("Money Wrench")
        if self.multiworld.shuffle_seals[self.player] and self.name in SEALS:
            locations += [seal_loc for seal_loc in SEALS[self.name]]
        if self.multiworld.shuffle_shards[self.player] and self.name in MEGA_SHARDS:
            locations += [shard for shard in MEGA_SHARDS[self.name]]
        loc_dict = {loc: world.location_name_to_id[loc] if loc in world.location_name_to_id else None for loc in locations}
        self.add_locations(loc_dict, MessengerLocation)
        world.multiworld.regions.append(self)


class MessengerLocation(Location):
    game = "The Messenger"

    def __init__(self, player: int, name: str, loc_id: Optional[int], parent: MessengerRegion) -> None:
        super().__init__(player, name, loc_id, parent)
        if loc_id is None:
            self.place_locked_item(MessengerItem(name, parent.player, None))


class MessengerShopLocation(MessengerLocation):
    def cost(self) -> int:
        name = self.name.replace("The Shop - ", "")  # TODO use `remove_prefix` when 3.8 finally gets dropped
        world: MessengerWorld = self.parent_region.multiworld.worlds[self.player]
        return world.shop_prices.get(name, world.figurine_prices.get(name))

    def can_afford(self, state: CollectionState) -> bool:
        world: MessengerWorld = state.multiworld.worlds[self.player]
        cost = self.cost() * 2
        if cost >= 1000:
            cost *= 2
        can_afford = state.has("Shards", self.player, min(cost, world.total_shards))
        if "Figurine" in self.name:
            return state.has("Money Wrench", self.player) and can_afford\
                and state.can_reach("Money Wrench", "Location", self.player)
        return can_afford


class MessengerItem(Item):
    game = "The Messenger"

    def __init__(self, name: str, player: int, item_id: Optional[int] = None, override_progression: bool = False,
                 count: int = 0) -> None:
        if count:
            item_class = ItemClassification.progression_skip_balancing
        elif item_id is None or override_progression or name in {*NOTES, *PROG_ITEMS, *PHOBEKINS, *PROG_SHOP_ITEMS}:
            item_class = ItemClassification.progression
        elif name in {*USEFUL_ITEMS, *USEFUL_SHOP_ITEMS}:
            item_class = ItemClassification.useful
        else:
            item_class = ItemClassification.filler
        super().__init__(name, item_class, item_id, player)

