from pathlib import Path
import settings
from typing import ClassVar

from BaseClasses import Item, Tutorial
from worlds.AutoWorld import WebWorld, World

from .client import WL4Client
from .items import WL4Item, ap_id_from_wl4_data, filter_item_names, filter_items, item_table
from .locations import location_name_to_id, setup_locations
from .options import wl4_options
from .regions import connect_regions, create_regions
from .rom import LocalRom, WL4DeltaPatch, get_base_rom_path, patch_rom
from .rules import set_access_rules
from .types import ItemType, Passage


class WL4Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        '''File name of the Wario Land 4 ROM'''
        description = 'Wario Land 4 ROM File'
        copy_to = 'Wario Land 4.gba'
        md5s = [WL4DeltaPatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True


class WL4Web(WebWorld):
    theme = 'jungle'

    setup_en = Tutorial(
        'Multiworld Setup Guide',
        'A guide to setting up the Wario Land 4 randomizer connected to an Archipelago Multiworld.',
        'English',
        'setup_en.md',
        'setup/en',
        ['lil David']
    )

    tutorials = [setup_en]


class WL4World(World):
    '''
    A golden pyramid has been discovered deep in the jungle, and Wario has set
    out to rob it. But when he enters, he finds the Golden Diva's curse has
    taken away his moves! To escape with his life and more importantly, the
    treasure, Wario must find his abilities to defeat the passage bosses and
    the Golden Diva.
    '''

    game: str = 'Wario Land 4'
    option_definitions = wl4_options
    settings: ClassVar[WL4Settings]
    topology_present = False

    data_version = 0

    item_name_to_id = {item_name: ap_id_from_wl4_data(data) for item_name, data in item_table.items()
                       if data[1] is not None}
    location_name_to_id = location_name_to_id

    web = WL4Web()

    def generate_early(self):
        options = self.multiworld.worlds[self.player].options
        if options.required_jewels > options.pool_jewels:
            options.pool_jewels = options.required_jewels
            self.multiworld.pool_jewels[self.player] = options.required_jewels
        if options.required_jewels >= 1 and options.golden_jewels == 0:
            options.golden_jewels = 1
            self.multiworld.golden_jewels[self.player] = options.golden_jewels

    def create_regions(self):
        location_table = setup_locations(self.multiworld, self.player)
        create_regions(self.multiworld, self.player, location_table)
        set_access_rules(self.multiworld, self.player)
        connect_regions(self.multiworld, self.player)

        passages = ('Entry', 'Emerald', 'Ruby', 'Topaz', 'Sapphire')
        for passage in passages:
            location = self.multiworld.get_region(f'{passage} Passage Boss', self.player).locations[0]
            location.place_locked_item(self.create_item(f'{passage} Passage Clear'))
            location.show_in_spoiler = False

        golden_diva = self.multiworld.get_location('Golden Diva', self.player)
        golden_diva.place_locked_item(self.create_item('Escape the Pyramid'))
        golden_diva.show_in_spoiler = False

    def create_items(self):
        difficulty = self.multiworld.difficulty[self.player].value
        gem_pieces = 18 * 4
        cds = 16
        full_health_items = (9, 7, 6)[difficulty]
        total_required_locations = gem_pieces + cds + full_health_items

        itempool = []

        required_jewels = self.multiworld.required_jewels[self.player].value
        pool_jewels = self.multiworld.pool_jewels[self.player].value
        for name, item in filter_items(type=ItemType.JEWEL):
            if item.passage() == Passage.ENTRY:
                copies = min(pool_jewels, 1)
            elif item.passage() == Passage.GOLDEN:
                copies = self.multiworld.golden_jewels[self.player]
            else:
                copies = pool_jewels

            for _ in range(copies):
                itempool.append(self.create_item(name, required_jewels == 0))

        for name in filter_item_names(type=ItemType.CD):
            itempool.append(self.create_item(name))

        for name in filter_item_names(type=ItemType.ABILITY):
            itempool.append(self.create_item(name))
            if name.startswith('Progressive'):
                itempool.append(self.create_item(name))

        # Remove full health items to make space for abilities
        if required_jewels == 4:
            if difficulty == 0:
                full_health_items -= 8
            else:
                raise ValueError('Not enough locations to place abilities for '
                                 f'{self.multiworld.player_name[self.player]}. '
                                 'Set the "Required Jewels" setting to a lower '
                                 'value and try again.')

        for _ in range(full_health_items):
            itempool.append(self.create_item('Full Health Item'))

        junk_count = total_required_locations - len(itempool)
        junk_item_pool = tuple(filter_item_names(type=ItemType.ITEM))
        for _ in range(junk_count):
            item_name = self.multiworld.random.choice(junk_item_pool)
            itempool.append(self.create_item(item_name))

        self.multiworld.itempool += itempool

    def generate_output(self, output_directory: str):
        output_path = Path(output_directory)

        try:
            world = self.multiworld
            player = self.player

            rom = LocalRom(get_base_rom_path())
            patch_rom(rom, self.multiworld, self.player)

            rompath = output_path / f'{world.get_out_file_name_base(player)}.gba'
            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = WL4DeltaPatch(
                rompath.with_suffix(WL4DeltaPatch.patch_file_ending),
                player=player,
                player_name = world.player_name[player],
                patched_path = rompath
            )
            patch.write()
        finally:
            if rompath.exists():
                rompath.unlink()

    def create_item(self, name: str, force_non_progression=False) -> Item:
        return WL4Item.from_name(name, self.player, force_non_progression)

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = (
            lambda state: state.has('Escape the Pyramid', self.player))
