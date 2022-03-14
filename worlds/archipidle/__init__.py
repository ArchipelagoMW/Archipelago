from BaseClasses import Item, MultiWorld, Region, Location, Entrance
from .Items import item_table
from .Rules import set_rules
from ..AutoWorld import World


class ArchipIDLEWorld(World):
    game = "ArchipIDLE"
    topology_present = False
    data_version = 1

    item_name_to_id = {}
    start_id = 9000
    for item in item_table:
        item_name_to_id[item] = start_id
        start_id += 1

    location_name_to_id = {}
    start_id = 9000
    for i in range(1, 101):
        location_name_to_id[f"Location {i}"] = start_id
        start_id += 1

    def generate_basic(self):
        item_table_copy = list(item_table)
        self.world.random.shuffle(item_table_copy)

        item_pool = []
        for i in range(100):
            item = Item(
                item_table_copy[i],
                i < 20,
                self.item_name_to_id[item_table_copy[i]],
                self.player
            )
            item.game = 'ArchipIDLE'
            item_pool.append(item)

        self.world.itempool = item_pool

    def set_rules(self):
        set_rules(self.world, self.player)

    def create_item(self, name: str) -> Item:
        return Item(name, True, self.item_name_to_id[name], self.player)

    def create_regions(self):
        self.world.regions += [
            create_region(self.world, self.player, 'Menu', None, ['Entrance to IDLE Zone']),
            create_region(self.world, self.player, 'IDLE Zone', self.location_name_to_id)
        ]

        # link up our region with the entrance we just made
        self.world.get_entrance('Entrance to IDLE Zone', self.player)\
            .connect(self.world.get_region('IDLE Zone', self.player))


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    region = Region(name, None, name, player)
    region.world = world
    if locations:
        for location_name in locations.keys():
            location = ArchipIDLELocation(player, location_name, locations[location_name], region)
            region.locations.append(location)

    if exits:
        for _exit in exits:
            region.exits.append(Entrance(player, _exit, region))

    return region


class ArchipIDLELocation(Location):
    game: str = "ArchipIDLE"

    def __init__(self, player: int, name: str, address=None, parent=None):
        super(ArchipIDLELocation, self).__init__(player, name, address, parent)
