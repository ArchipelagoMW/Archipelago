import logging
from typing import Dict, List, Set, Any

from BaseClasses import Region, RegionType, Entrance, Item, Tutorial, ItemClassification
from Options import Option
from ..AutoWorld import World, WebWorld
from .Characters import all_chars
from .Items import build_item_table, always_available_items, get_normal_items
from .Locations import get_char_locations, CryptLocation
from .Options import cotnd_options


id_offset: int = 247000


class CotNDWebWorld(WebWorld):
    theme = "dirt"
    game_info_languages = ['en']

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Crypt of the NecroDancer for Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Espeon"],
    )

    tutorials: List[Tutorial] = [setup_en]


class CotNDWorld(World):
    """
    Crypt of the NecroDancer is a roguelike rhythm game. Move to the beat in an ever-changing dungeon while fighting
    skeletons, dragons, and rapping moles. Descend into the crypt to defeat the NecroDancer and claim the Golden Lute!
    """
    game: str                           = "Crypt of the NecroDancer"
    options: Dict[str, Option[Any]]     = cotnd_options
    item_name_to_id: Dict[str, int]     = {name: (id_offset + index) for index, name in enumerate(build_item_table())}
    location_name_to_id: Dict[str, int] = {name: (id_offset + index) for index, name in enumerate(
        [loc for char in all_chars for instance in range(1, 18) for loc in get_char_locations(char, instance, True, True)])}
    data_version: int                   = 1

    item_name_groups: Dict[str, Set[str]] = {t: {k for k, v in build_item_table().items() if v['Type'] == t} for t in {v['Type'] for v in build_item_table().values()}}
    junk_items: List[str] = list(item_name_groups['Junk'])
    trap_items: List[str] = list(item_name_groups['Trap'])

    web = CotNDWebWorld()

    ### Autoworld Methods ###

    # make basic item list
    # decide characters and starting character
    # remove start_inventory dupes
    def generate_early(self) -> None:
        self.chars = sorted(list(set(self.world.available_characters[self.player].value) | 
            {self.world.starting_character[self.player].current_key.capitalize()}))

        self.dlc_packs = ['base']
        if self.world.dlc[self.player].current_key in ['both', 'amplified']:
            self.dlc_packs.append('amp')
        if self.world.dlc[self.player].current_key in ['both', 'synchrony']:
            self.dlc_packs.append('sync')
        self.amplified = 'amp' in self.dlc_packs

        self.item_table = build_item_table(self.world.split_weapons[self.player])

        self.items: List[str] = get_normal_items(self.chars, self.dlc_packs,
            self.world.reduce_starting_items[self.player].value,
            self.world.split_weapons[self.player].value)

        # give starting character
        starting_char = f"Unlock {self.world.starting_character[self.player].current_key.capitalize()}"
        self.world.push_precollected(self.create_item(starting_char))
        self.items.remove(starting_char)

        # remove items that we started with
        start_inventory = self.world.start_inventory[self.player].value
        for item, count in start_inventory.items():
            if count > 0 and item in self.items:
                self.items.remove(item)

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
        reduce_logic = self.world.reduce_logic[self.player].value
        # Add starting char if necessary, purge duplicates and ordering
        locations = [loc for char in self.chars for loc in get_char_locations(char, 1, flawless, self.amplified)]
        self.char_counts = {char: 1 for char in self.chars}

        # Add locations until enough are made
        gen = char_generator(self.chars)
        while len(locations) < len(self.items):
            char, instance = next(gen)
            locations += get_char_locations(char, instance, flawless, self.amplified)
            self.char_counts[char] += 1

        for name in locations:
            loc = CryptLocation(self.player, name, self.location_name_to_id[name], crypt, reduce_logic, self.amplified)
            crypt.locations.append(loc)

        # Victory condition: clear all characters
        clears = list(filter(lambda s: 'Clear' in s, locations))
        self.world.completion_condition[self.player] = lambda state: all(state.can_reach(loc, 'Location', self.player)
            for loc in clears)

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
            'keep_inventory': self.world.keep_inventory_on_death[self.player].value,
            'split_weapons': self.world.split_weapons[self.player].value,
        }

    def create_item(self, name: str) -> Item:
        try:
            data = self.item_table[name]
            ret = Item(name, ItemClassification(data['AP Item Class']), self.item_name_to_id[name], self.player)
            ret.game = self.game
            ret.type = data['Type']
            return ret
        except KeyError:
            logging.error(f"{name} not a valid item name for CotND")
            raise

    def get_filler_item_name(self) -> str:
        if self.world.random.random()*100 < self.world.trap_percentage[self.player]:
            return self.world.random.choice(self.trap_items)
        else:
            return self.world.random.choice(self.junk_items)
