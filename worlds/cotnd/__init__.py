
# TODO:
# add more logic
# Write tutorial
# Increment data version

import logging
from typing import Dict, List, Any

from BaseClasses import Region, RegionType, Entrance, Item, Tutorial, ItemClassification
from Options import Option
from ..AutoWorld import World, WebWorld
from .Characters import all_chars
from .Items import item_table, always_available_items, junk_items, trap_items, get_normal_items
from .Locations import get_char_locations, CryptLocation
from .Options import cotnd_options


id_offset: int = 247000


class CotNDWebWorld(WebWorld):
    settings_page = True
    game_info_languages: ['en']
    tutorials: List[Tutorial] = []
    theme = "dirt"


class CotNDWorld(World):
    game: str                           = "Crypt of the NecroDancer"
    options: Dict[str, Option[Any]]     = cotnd_options
    item_name_to_id: Dict[str, int]     = {name: (id_offset + index) for index, name in enumerate(item_table)}
    location_name_to_id: Dict[str, int] = {name: (id_offset + index) for index, name in enumerate(
        [loc for char in all_chars for instance in range(1, 10) for loc in get_char_locations(char, instance, True)])}
    data_version: int                   = 0

    items: List[str]                    = []

    ### Autoworld Methods ###

    # make basic item list
    # decide characters and starting character
    # remove start_inventory dupes
    def generate_early(self) -> None:
        self.chars = sorted(list(set(self.world.available_characters[self.player].value) | 
            {self.world.starting_character[self.player].current_key.capitalize()}))
        self.items: List[str] = get_normal_items(self.chars, self.world.reduce_starting_items[self.player].value)
        self.give_starting_character()
        self.remove_start_items_from_pool()

    # create required regions
    # make enough locations for all the items
    def create_regions(self) -> None:
        menu = Region('Menu', RegionType.Generic, 'Menu', self.player, self.world)
        crypt = Region('The Crypt', RegionType.Generic, 'The Crypt', self.player, self.world)
        allzones = Entrance(self.player, 'All Zones Run', menu)
        allzones.connect(crypt)
        menu.exits.append(allzones)
        self.world.regions.extend([menu, crypt])

        # Generator for random characters in increasing instance order, starting at 2
        def char_generator(chars_base):
            instance = 2
            while True:
                chars = chars_base.copy()
                self.world.random.shuffle(chars)
                for c in chars:
                    yield c, instance
                instance += 1

        # Initial locations
        flawless = self.world.randomize_flawless[self.player].value
        # Add starting char if necessary, purge duplicates and ordering
        locations = [loc for char in self.chars for loc in get_char_locations(char, 1, flawless)]
        self.char_counts = {char: 1 for char in self.chars}

        # Add locations until enough are made
        gen = char_generator(self.chars)
        while len(locations) < len(self.items):
            char, instance = next(gen)
            locations += get_char_locations(char, instance, flawless)
            self.char_counts[char] += 1

        for name in locations:
            loc = CryptLocation(self.player, name, self.location_name_to_id[name], crypt)
            crypt.locations.append(loc)

        # Victory condition: clear all characters
        clears = list(filter(lambda s: 'Clear' in s, locations))
        self.world.completion_condition[self.player] = lambda state: all(state.can_reach(loc, 'Location', self.player) for loc in clears)

    # make junk items to fill up locations
    # turn item list into real items
    def create_items(self) -> None:
        crypt = self.world.get_region('The Crypt', self.player)
        while len(self.items) < len(crypt.locations):
            self.items.append(self.get_filler_item_name())

        for item in self.items:
            self.world.itempool.append(self.create_item(item))

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            'reduce_starting_items': self.world.reduce_starting_items[self.player].value,
            'randomize_flawless': self.world.randomize_flawless[self.player].value,
            'free_samples': self.world.free_samples[self.player].value,
            'prevent_bad_samples': self.world.prevent_bad_samples[self.player].value,
            'char_counts': self.char_counts,
        }

    def create_item(self, name: str) -> Item:
        try:
            data = item_table[name]
            ret = Item(name, ItemClassification(data[0]), self.item_name_to_id[name], self.player)
            ret.game = self.game
            ret.type = data[1]
            return ret
        except KeyError:
            logging.error(f"{name} not a valid item name for CotND")
            raise

    def get_filler_item_name(self) -> str:
        if self.world.random.random()*100 < self.world.trap_percentage[self.player]:
            return self.world.random.choice(trap_items)
        else:
            return self.world.random.choice(junk_items)

    ### End Autoworld Methods ###

    # give starting char to player
    def give_starting_character(self) -> None:
        starting_char = f"Unlock {self.world.starting_character[self.player].current_key.capitalize()}"
        self.world.push_precollected(self.create_item(starting_char))
        self.items.remove(starting_char)

    # remove items that we start with from the item list
    def remove_start_items_from_pool(self) -> None:
        start_inventory = self.world.start_inventory[self.player].value
        for item, count in start_inventory.items():
            if count > 0 and item in self.items:
                self.items.remove(item)

