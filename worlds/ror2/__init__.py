import string
from .Items import RiskOfRainItem, item_table, junk_weights
from .Locations import location_table, RiskOfRainLocation, base_location_table
from .Rules import set_rules

from BaseClasses import Region, Entrance, Item, MultiWorld
from .Options import ror2_options
from ..AutoWorld import World

client_version = 1


class RiskOfRainWorld(World):
    """
     Escape a chaotic alien planet by fighting through hordes of frenzied monsters – with your friends, or on your own.
     Combine loot in surprising ways and master each character until you become the havoc you feared upon your
     first crash landing.
    """
    game: str = "Risk of Rain 2"
    options = ror2_options
    topology_present = False

    item_name_to_id = {name: data for name, data in item_table.items()}
    location_name_to_id = {name: data for name, data in location_table.items()}

    data_version = 1
    forced_auto_forfeit = True

    def generate_basic(self):
        # shortcut for starting_inventory... The start_with_revive option lets you start with a Dio's Best Friend
        if self.world.start_with_revive[self.player].value:
            self.world.push_precollected(self.world.create_item("Dio's Best Friend", self.player))

        # Generate item pool
        itempool = []
        junk_pool = junk_weights.copy()

        # Add revive items for the player
        itempool += ["Dio's Best Friend"] * self.world.total_revivals[self.player]

        if not self.world.enable_lunar[self.player]:
            junk_pool.pop("Lunar Item")

        # Fill remaining items with randomly generated junk
        itempool += self.world.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()),
                                              k=self.world.total_items[self.player] -
                                                self.world.total_revivals[self.player])

        # Convert itempool into real items
        itempool = [item for item in map(lambda name: self.create_item(name), itempool)]

        self.world.itempool += itempool

    def set_rules(self):
        set_rules(self.world, self.player)

    def create_regions(self):
        create_regions(self.world, self.player)

    def fill_slot_data(self):
        return {
            "itemPickupStep": self.world.item_pickup_step[self.player].value,
            "seed": "".join(self.world.slot_seeds[self.player].choice(string.digits) for i in range(16)),
            "totalLocations": self.world.total_items[self.player].value,
            "totalRevivals": self.world.total_revivals[self.player].value
        }

    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        item = RiskOfRainItem(name, True, item_id, self.player)
        return item


def create_regions(world, player: int):
    world.regions += [
        create_region(world, player, 'Menu', None, ['Lobby']),
        create_region(world, player, 'Petrichor V',
                      [location for location in base_location_table] +
                      [f"ItemPickup{i}" for i in range(1, world.total_locations[player])])
    ]

    world.get_entrance("Lobby", player).connect(world.get_region("Petrichor V", player))
    world.get_location("Level One", player).place_locked_item(RiskOfRainItem("Beat Level One", True, None, player))
    world.get_location("Level Two", player).place_locked_item(RiskOfRainItem("Beat Level Two", True, None, player))
    world.get_location("Level Three", player).place_locked_item(RiskOfRainItem("Beat Level Three", True, None, player))
    world.get_location("Level Four", player).place_locked_item(RiskOfRainItem("Beat Level Four", True, None, player))
    world.get_location("Level Five", player).place_locked_item(RiskOfRainItem("Beat Level Five", True, None, player))
    world.get_location("Victory", player).place_locked_item(RiskOfRainItem("Victory", True, None, player))


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = location_table.get(location, 0)
            location = RiskOfRainLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret
