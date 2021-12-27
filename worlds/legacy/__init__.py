from BaseClasses import Region, MultiWorld, Entrance, Item
from .Items import LegacyItem, item_table, item_frequencies, item_repeatable, \
    required_items_count
from .Locations import LegacyLocation, location_table, base_location_table
from .Options import legacy_options
from .Regions import create_regions
from .Constants import DEBUG, TOTAL_LOCATIONS
from ..AutoWorld import World
import random
import typing


class LegacyWorld(World):
    """
    Rogue Legacy is a genealogical rogue-"LITE" where anyone can be a hero. Each
    time you die, your child will succeed you. Every child is unique. One child
    might be colorblind, another might have vertigo-- they could even be a
    dwarf. But that's OK, because no one is perfect, and you don't have to be to
    succeed.
    """
    game: str = "Rogue Legacy"
    options = legacy_options
    topology_present = False
    data_version = 0

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table

    def _get_slot_data(self):
        return {
            "starting_gender": self.world.starting_gender[self.player],
            "new_game_plus": self.world.new_game_plus[self.player],
            "death_link": self.world.death_link[self.player],
        }

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in legacy_options:
            option = getattr(self.world, option_name)[self.player]
            slot_data[option_name] = option.value

        return slot_data

    def generate_basic(self):
        itempool: typing.List[LegacyItem] = []

        # Print these tables, so I can easily copy it into RL. Used during dev.
        if DEBUG:
            LegacyItem.print_item_table()
            LegacyLocation.print_location_table()

        # Fill item pool with all runes, blueprints, and skill unlocks.
        for item in item_table:
            # Ignore filler items, we'll add those later.
            if item in item_repeatable:
                continue
            elif item in item_frequencies:
                itempool += [self.create_item(item)] * item_frequencies[item]
            else:
                itempool += [self.create_item(item)]

        # Fill remaining locations with random stuff.
        extra = TOTAL_LOCATIONS - required_items_count
        for i in range(0, extra):
            item = random.choice(item_repeatable)
            itempool += [self.create_item(item)]

        self.world.itempool += itempool

        # Victory stuff.
        self.world.get_location("Victory", self.player)\
            .place_locked_item(self.create_event("Victory"))
        self.world.completion_condition[self.player] = \
            lambda state: state.has("Victory", self.player)

    def create_regions(self):
        create_regions(self.world, self.player)

    def create_item(self, name: str) -> Item:
        return LegacyItem(name, self.player)

    def create_event(self, event: str):
        return LegacyItem(event, self.player, True)


def create_region(world: MultiWorld, player: int, name: str, locations=None,
                  exits=None):
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = location_table.get(location, 0)
            location = LegacyLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret
