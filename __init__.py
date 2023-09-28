from pathlib import Path
import settings
from typing import ClassVar

from BaseClasses import Item, Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, Type, components, SuffixIdentifier, launch_subprocess

from .items import WL4Item, ap_id_from_wl4_data, filter_item_names, filter_items, item_table
from .locations import location_name_to_id, setup_locations
from .logic import WL4Logic
from .options import wl4_options
from .regions import connect_regions, create_regions
from .rom import LocalRom, WL4DeltaPatch, get_base_rom_path, patch_rom
from .types import ItemType, Passage


def launch_client(*args):
    from .client import launch
    launch_subprocess(launch, name='WL4Client')


components.append(Component('Wario Land 4 Client', 'WL4Client', component_type=Type.CLIENT,
                            func=launch_client, file_identifier=SuffixIdentifier('.apwl4'))),


class WL4Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        '''File name of the Wario Land 4 NA/EU ROM'''
        description = 'Wario Land 4 (U/E) ROM File'
        copy_to = 'Wario Land 4 (UE) [!].gba'
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
    out to rob it. But to make off with its legendary treasure, he has to first
    defeat the five passage bosses and the pyramid's evil ruler, the Golden Diva.
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
        if self.multiworld.early_entry_jewels[self.player]:
            for item in filter_item_names(type=ItemType.JEWEL, passage=Passage.ENTRY):
                self.multiworld.local_early_items[self.player][item] = 1

    def create_regions(self):
        location_table = setup_locations(self.multiworld, self.player)
        create_regions(self.multiworld, self.player, location_table)
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
        diamond_pieces = 18 * 4
        cds = 16
        full_health_items = (9, 7, 5)[self.multiworld.difficulty[self.player].value]
        total_required_locations = diamond_pieces + cds + full_health_items

        itempool = []

        required_jewels = self.multiworld.required_jewels[self.player]
        required_jewels_entry = min(1, required_jewels)
        for name, item in filter_items(type=ItemType.JEWEL):
            if item.passage() in (Passage.ENTRY, Passage.GOLDEN):
                copies = required_jewels_entry
                start = 1 - required_jewels_entry
            else:
                copies = required_jewels
                start = 4 - required_jewels

            for _ in range(copies):
                itempool.append(self.create_item(name))
            for _ in range(start):
                self.multiworld.push_precollected(self.create_item(name))

        for name in filter_item_names(type=ItemType.CD):
            itempool.append(self.create_item(name))

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
        data = item_table[name]
        created_item = WL4Item(name, self.player, data, force_non_progression)
        return created_item

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = (
            lambda state: state.has('Escape the Pyramid', self.player))
