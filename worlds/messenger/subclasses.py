from functools import cached_property
from typing import Optional, TYPE_CHECKING, cast

from BaseClasses import CollectionState, Item, ItemClassification, Location, Region
from .constants import NOTES, PHOBEKINS, PROG_ITEMS, USEFUL_ITEMS
from .options import Goal
from .regions import MEGA_SHARDS, REGIONS, SEALS
from .shop import FIGURINES, PROG_SHOP_ITEMS, SHOP_ITEMS, USEFUL_SHOP_ITEMS

if TYPE_CHECKING:
    from . import MessengerWorld


class MessengerRegion(Region):
    
    def __init__(self, name: str, world: "MessengerWorld") -> None:
        super().__init__(name, world.player, world.multiworld)
        locations = [loc for loc in REGIONS[self.name]]
        if self.name == "The Shop":
            shop_locations = {f"The Shop - {shop_loc}": world.location_name_to_id[f"The Shop - {shop_loc}"]
                              for shop_loc in SHOP_ITEMS}
            shop_locations.update(**{figurine: world.location_name_to_id[figurine] for figurine in FIGURINES})
            self.add_locations(shop_locations, MessengerShopLocation)
        elif self.name == "Tower HQ":
            locations.append("Money Wrench")
        if world.options.shuffle_seals and self.name in SEALS:
            locations += [seal_loc for seal_loc in SEALS[self.name]]
        if world.options.shuffle_shards and self.name in MEGA_SHARDS:
            locations += [shard for shard in MEGA_SHARDS[self.name]]
        loc_dict = {loc: world.location_name_to_id.get(loc, None) for loc in locations}
        self.add_locations(loc_dict, MessengerLocation)
        world.multiworld.regions.append(self)


class MessengerLocation(Location):
    game = "The Messenger"

    def __init__(self, player: int, name: str, loc_id: Optional[int], parent: MessengerRegion) -> None:
        super().__init__(player, name, loc_id, parent)
        if loc_id is None:
            self.place_locked_item(MessengerItem(name, parent.player, None))


class MessengerShopLocation(MessengerLocation):
    @cached_property
    def cost(self) -> int:
        name = self.name.replace("The Shop - ", "")  # TODO use `remove_prefix` when 3.8 finally gets dropped
        world = cast("MessengerWorld", self.parent_region.multiworld.worlds[self.player])
        # short circuit figurines which all require demon's bane be purchased, but nothing else
        if "Figurine" in name:
            return world.figurine_prices[name] +\
                cast(MessengerShopLocation, world.multiworld.get_location("The Shop - Demon's Bane", self.player)).cost
        shop_data = SHOP_ITEMS[name]
        if shop_data.prerequisite:
            prereq_cost = 0
            if isinstance(shop_data.prerequisite, set):
                for prereq in shop_data.prerequisite:
                    prereq_cost +=\
                        cast(MessengerShopLocation,
                             world.multiworld.get_location(prereq, self.player)).cost
            else:
                prereq_cost +=\
                    cast(MessengerShopLocation,
                         world.multiworld.get_location(shop_data.prerequisite, self.player)).cost
            return world.shop_prices[name] + prereq_cost
        return world.shop_prices[name]

    def can_afford(self, state: CollectionState) -> bool:
        world = cast("MessengerWorld", state.multiworld.worlds[self.player])
        can_afford = state.has("Shards", self.player, min(self.cost, world.total_shards))
        if "Figurine" in self.name:
            can_afford = state.has("Money Wrench", self.player) and can_afford\
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
