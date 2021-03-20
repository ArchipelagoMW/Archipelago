import logging

logger = logging.getLogger("Hollow Knight")

from .Locations import lookup_name_to_id
from .Items import item_table
from .Regions import create_regions
from .Rules import set_rules

from BaseClasses import Region, Entrance, Location, MultiWorld, Item


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = lookup_name_to_id.get(location, 0)
            location = HKLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret

class HKLocation(Location):
    game: str = "Hollow Knight"

    def __init__(self, player: int, name: str, address=None, parent=None):
        super(HKLocation, self).__init__(player, name, address, parent)

class HKItem(Item):
    game = "Hollow Knight"

    def __init__(self, name, advancement, code, type, player: int = None):
        super(HKItem, self).__init__(name, advancement, code, player)
        self.type = type


def gen_hollow(world: MultiWorld, player: int):
    link_regions(world, player)
    gen_items(world, player)
    set_rules(world, player)




def link_regions(world: MultiWorld, player: int):
    world.get_entrance('Hollow Nest S&Q', player).connect(world.get_region('Hollow Nest', player))

not_shufflable_types = {"Essence_Boss"}

option_to_type_lookup = {
    "Root": "RandomizeWhisperingRoots",
    "Dreamer": "RandomizeDreamers",
    "Geo": "RandomizeGeoChests",
    "Skill": "RandomizeSkills",
    "Map": "RandomizeMaps",
    "Relic": "RandomizeRelics",
    "Charm": "RandomizeCharms",
    "Notch": "RandomizeCharmNotches",
    "Key": "RandomizeKeys",
    "Stag": "RandomizeStags",
    "Flame": "RandomizeFlames",
    "Grub": "RandomizeGrubs",
    "Cocoon": "RandomizeLifebloodCocoons",
    "Mask": "RandomizeMaskShards",
    "Ore": "RandomizePaleOre",
    "Egg": "RandomizeRancidEggs",
    "Vessel": "RandomizeVesselFragments",
}

def gen_items(world: MultiWorld, player: int):
    pool = []
    for item_name, item_data in item_table.items():

        item = HKItem(item_name, item_data.advancement, item_data.id, item_data.type, player=player)

        if item_data.type == "Event":
            event_location = world.get_location(item_name, player)
            world.push_item(event_location, item)
            event_location.event = True
            event_location.locked = True
            if item.name == "King's_Pass":
                world.push_precollected(item)
        elif item_data.type == "Cursed":
            if world.CURSED[player]:
                raise Exception("Cursed is not implemented yet.")
                # implement toss_junk for HK first
            else:
                event_location = world.get_location(item_name, player)
                world.push_item(event_location, item)
                event_location.event = True
                event_location.locked = True
                world.push_precollected(item)

        elif item_data.type == "Fake":
            pass
        elif item_data.type in not_shufflable_types:
            location = world.get_location(item_name, player)
            world.push_item(location, item)
            location.event = item.advancement
            location.locked = True
        else:
            target = option_to_type_lookup[item.type]
            shuffle_it = getattr(world, target)
            if shuffle_it[player]:
                pool.append(item)
            else:
                location = world.get_location(item_name, player)
                world.push_item(location, item)
                location.event = item.advancement
                location.locked = True
                logger.debug(f"Placed {item_name} to vanilla for player {player}")

    world.itempool += pool



