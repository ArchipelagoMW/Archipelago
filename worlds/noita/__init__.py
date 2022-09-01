import string
from typing import Dict, List
from .Items import NoitaItem, item_table, item_pool_weights
from .Locations import NoitaLocation, item_pickups

from BaseClasses import Region, RegionType, Entrance, Item, ItemClassification, MultiWorld, Tutorial
from .Options import noita_options
from worlds.AutoWorld import World, WebWorld

client_version = 1


class NoitaWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Noita integration for Archipelago multiworld games.",
        "English",
        "setup_en.md",
        "setup/en",
        ["DaftBrit"]
    )]
    theme = "partyTime"


class NoitaWorld(World):
    """
    Noita is a magical action roguelite set in a world where every pixel is physically simulated. Fight, explore, melt,
    burn, freeze and evaporate your way through the procedurally generated world using spells you've created yourself.
    """
    game: str = "Noita"
    option_definitions = noita_options
    topology_present = False

    item_name_to_id = item_table
    location_name_to_id = item_pickups

    data_version = 5
    forced_auto_forfeit = True
    web = NoitaWeb()

    def generate_basic(self):

        if self.world.bad_affects[self.player].value:
            pool_option = 0
        else:
            pool_option = 1
        junk_pool: Dict[str, int] = {}
        junk_pool = item_pool_weights[pool_option].copy()
        # Generate item pool
        itempool: List = []

        for i in range(1, 1 + self.world.total_locations[self.player].value):
            itempool += self.world.random.choices(list(junk_pool.keys()), weights=list(junk_pool.values()))

        # Convert itempool into real items
        itempool = list(map(lambda name: self.create_item(name), itempool))

        self.world.itempool += itempool

    def create_regions(self) -> None:
        menu = create_region(self.world, self.player, "Menu")
        mines = create_region(self.world, self.player, "Mines",
                                  [f"Chest{i + 1}" for i in range(self.world.total_locations[self.player].value)])

        connection = Entrance(self.player, "Lobby", menu)
        menu.exits.append(connection)
        connection.connect(mines)

        self.world.regions += [menu, mines]

        create_events(self.world, self.player)

    def fill_slot_data(self):
        return {
            "seed": "".join(self.world.slot_seeds[self.player].choice(string.digits) for i in range(16)),
            "totalLocations": self.world.total_locations[self.player].value,
            "badAffects": self.world.bad_affects[self.player].value,
        }

    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        if name == "Heart":
            classification = ItemClassification.progression
        elif name.startswith("Wand"):
            classification = ItemClassification.useful
        else:
            classification = ItemClassification.filler
        item = NoitaItem(name, classification, item_id, self.player)
        return item


def create_events(world: MultiWorld, player: int) -> None:
    total_locations = world.total_locations[player].value
    world_region = world.get_region("Mines", player)
    for i in range(1, 1 + total_locations):
        event_loc = NoitaLocation(player, f"Pickup{(i + 1)}", None, world_region)
        event_loc.place_locked_item(NoitaItem(f"Pickup{(i + 1)}", ItemClassification.progression, None, player))
        event_loc.access_rule(lambda state, i=i: state.can_reach(f"Chest{(i + 1) - 1}", player))
        world_region.locations.append(event_loc)


def create_region(world: MultiWorld, player: int, name: str, locations: List[str] = None) -> Region:
    ret = Region(name, RegionType.Generic, name, player, world)
    if locations:
        for location in locations:
            loc_id = item_pickups[location]
            location = NoitaLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    return ret