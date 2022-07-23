from BaseClasses import Item, MultiWorld, Region, Location, Entrance, Tutorial, ItemClassification
from .Items import item_table
from .Rules import set_rules
from ..AutoWorld import World, WebWorld
from datetime import datetime


class ArchipIDLEWebWorld(WebWorld):
    theme = 'partyTime'
    tutorials = [
        Tutorial(
            tutorial_name='Setup Guide',
            description='A guide to playing Archipidle',
            language='English',
            file_name='guide_en.md',
            link='guide/en',
            authors=['Farrak Kilhn']
        )
    ]


class ArchipIDLEWorld(World):
    """
    An idle game which sends a check every thirty seconds, up to one hundred checks.
    """
    game = "ArchipIDLE"
    topology_present = False
    data_version = 3
    hidden = (datetime.now().month != 4)  # ArchipIDLE is only visible during April
    web = ArchipIDLEWebWorld()

    prog_items: set

    item_name_to_id = {}
    start_id = 9000
    for item in item_table:
        item_name_to_id[item] = start_id
        start_id += 1

    location_name_to_id = {}
    start_id = 9000
    for i in range(1, 101):
        location_name_to_id[f"IDLE for at least {int(i / 2)} minutes {30 if (i % 2) else 0} seconds"] = start_id
        start_id += 1

    def generate_basic(self):
        item_table_copy = list(item_table)
        self.world.random.shuffle(item_table_copy)
        self.prog_items = set()

        for i in range(100):
            item = Item(
                item_table_copy[i],
                ItemClassification.progression if i < 20 else ItemClassification.filler,
                self.item_name_to_id[item_table_copy[i]],
                self.player
            )
            if i < 20:
                self.prog_items.add(item_table_copy[i])
            item.game = 'ArchipIDLE'
            self.world.itempool.append(item)

    def set_rules(self):
        set_rules(self.world, self.player)

    def create_item(self, name: str) -> Item:
        return Item(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def create_regions(self):
        menu = create_region(self.world, self.player, 'Menu')
        entrance = Entrance(self.player, 'Entrance to IDLE Zone', menu)
        menu.exits.append(entrance)
        idle_zone = create_region(self.world, self.player, 'IDLE Zone', self.location_name_to_id)
        entrance.connect(idle_zone)

        self.world.regions += [menu, idle_zone]

    def get_filler_item_name(self) -> str:
        return self.world.random.choice(item_table)


def create_region(world: MultiWorld, player: int, name: str, locations=None):
    region = Region(name, player, world)
    if locations:
        for location_name in locations:
            location = ArchipIDLELocation(player, location_name, locations[location_name], region)
            region.locations.append(location)

    return region


class ArchipIDLELocation(Location):
    game: str = "ArchipIDLE"
