from functools import cached_property
from typing import TYPE_CHECKING

from BaseClasses import CollectionState, Entrance, Item, ItemClassification, Location, Region
from .regions import LOCATIONS, MEGA_SHARDS
from .shop import FIGURINES, SHOP_ITEMS

if TYPE_CHECKING:
    from . import MessengerWorld


class MessengerEntrance(Entrance):
    world: "MessengerWorld | None" = None


class MessengerRegion(Region):
    parent: str
    entrance_type = MessengerEntrance

    def __init__(self, name: str, world: "MessengerWorld", parent: str | None = None) -> None:
        super().__init__(name, world.player, world.multiworld)
        self.parent = parent
        locations = []
        if name in LOCATIONS:
            locations = [loc for loc in LOCATIONS[name]]
        # portal event locations since portals can be opened from their exit regions
        if name.endswith("Portal"):
            locations.append(name.replace(" -", ""))

        if name == "The Shop":
            shop_locations = {f"The Shop - {shop_loc}": world.location_name_to_id[f"The Shop - {shop_loc}"]
                              for shop_loc in SHOP_ITEMS}
            self.add_locations(shop_locations, MessengerShopLocation)
        elif name == "The Craftsman's Corner":
            self.add_locations({figurine: world.location_name_to_id[figurine] for figurine in FIGURINES},
                               MessengerLocation)
        elif name == "Tower HQ":
            locations.append("Money Wrench")

        if world.options.shuffle_shards and name in MEGA_SHARDS:
            locations += MEGA_SHARDS[name]
        loc_dict = {loc: world.location_name_to_id.get(loc, None) for loc in locations}
        self.add_locations(loc_dict, MessengerLocation)

        self.multiworld.regions.append(self)


class MessengerLocation(Location):
    game = "The Messenger"

    def __init__(self, player: int, name: str, loc_id: int | None, parent: MessengerRegion) -> None:
        super().__init__(player, name, loc_id, parent)
        if loc_id is None:
            if name == "Rescue Phantom":
                name = "Do the Thing!"
            self.place_locked_item(MessengerItem(name, ItemClassification.progression, None, parent.player))


class MessengerShopLocation(MessengerLocation):
    @cached_property
    def cost(self) -> int:
        name = self.name.removeprefix("The Shop - ")
        world = self.parent_region.multiworld.worlds[self.player]
        shop_data = SHOP_ITEMS[name]
        if shop_data.prerequisite:
            prereq_cost = 0
            if isinstance(shop_data.prerequisite, set):
                for prereq in shop_data.prerequisite:
                    loc = world.multiworld.get_location(prereq, self.player)
                    assert isinstance(loc, MessengerShopLocation)
                    prereq_cost += loc.cost
            else:
                loc = world.multiworld.get_location(shop_data.prerequisite, self.player)
                assert isinstance(loc, MessengerShopLocation)
                prereq_cost += loc.cost
            return world.shop_prices[name] + prereq_cost
        return world.shop_prices[name]

    def access_rule(self, state: CollectionState) -> bool:
        world = state.multiworld.worlds[self.player]
        can_afford = state.has("Shards", self.player, min(self.cost, world.total_shards))
        return can_afford


class MessengerItem(Item):
    game = "The Messenger"
