import string

from BaseClasses import Item, MultiWorld, Region, Location, Entrance
from .Items import item_table, starter_melee_weapons, starter_spells
from .Locations import location_table
from .Regions import create_regions
from .Rules import set_rules
from ..AutoWorld import World
from .Options import timespinner_options


class TimespinnerWorld(World):
    options = timespinner_options
    game = "Timespinner"
    topology_present = False
    data_version = 1

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table

    def _get_slot_data(self):
        return {
            'seed': "".join(self.world.slot_seeds[self.player].choice(string.ascii_letters) for i in range(16)),
            'start_with_jewerlybox': self.world.start_with_jewerlybox[self.player],
            'start_with_meyef': self.world.start_with_meyef[self.player],
            'quickseed': self.world.quickseed[self.player]
        }

    def generate_basic(self):
        self.world.random.shuffle(starter_melee_weapons)
        self.world.random.shuffle(starter_spells)

        melee_weapon = TimespinnerWorldItem(starter_melee_weapons.pop(), self.player)
        spell = TimespinnerWorldItem(starter_spells.pop(), self.player)
     
        self.world.get_location('Tutorial - Yo Momma 1', self.player).place_locked_item(melee_weapon)
        self.world.get_location('Tutorial - Yo Momma 2', self.player).place_locked_item(spell)
        
        # Fill out our pool with our items from item_pool, assuming 1 item if not present in item_pool
        pool = []
        for name, data in item_table.items():
            item = TimespinnerWorldItem(name, self.player)
            pool.append(item)

        self.world.itempool += pool



        # Pair up our event locations with our event items
        #for event, item in event_item_pairs.items():
        #    event_item = TimespinnerWorldItem(item, self.player)
        #    self.world.get_location(event, self.player).place_locked_item(event_item)

        #if self.world.logic[self.player] != 'no logic':
        #    self.world.completion_condition[self.player] = lambda state: state.has("Victory", self.player)


    def set_rules(self):
        set_rules(self.world, self.player)

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        return Item(name, item_data.progression, item_data.code, self.player)

    def create_regions(self):
        create_regions(self.world, self.player)

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in timespinner_options:
            option = getattr(self.world, option_name)[self.player]
            slot_data[option_name] = int(option.value)
        return slot_data


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = location_table.get(location, 0)
            location = TimespinnerWorldLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret


class TimespinnerWorldLocation(Location):
    game: str = "Timespinner"

    def __init__(self, player: int, name: str, address=None, parent=None):
        super(TimespinnerWorldLocation, self).__init__(player, name, address, parent)
        if address is None:
            self.event = True
            self.locked = True


class TimespinnerWorldItem(Item):
    game = "Timespinner"

    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        super(TimespinnerWorldItem, self).__init__(name, item_data.progression, item_data.code, player)
