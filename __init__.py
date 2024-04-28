from pathlib import Path
import settings
from typing import Any, ClassVar, Mapping

from BaseClasses import Item, Tutorial
from worlds.AutoWorld import WebWorld, World

from .client import WL4Client
from .items import WL4Item, ap_id_from_wl4_data, filter_item_names, filter_items, item_table
from .locations import location_name_to_id, location_table
from .options import Goal, GoldenJewels, PoolJewels, WL4Options
from .regions import connect_regions, create_regions
from .rom import LocalRom, WL4DeltaPatch, get_base_rom_path, patch_rom
from .rules import set_access_rules
from .types import ItemType, LocationType, Passage


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
    options_dataclass = WL4Options
    options: WL4Options
    settings: ClassVar[WL4Settings]
    topology_present = False

    data_version = 1

    item_name_to_id = {item_name: ap_id_from_wl4_data(data) for item_name, data in item_table.items()
                       if data[1] is not None}
    location_name_to_id = location_name_to_id

    item_name_groups = {
        'Golden Treasure': {
            'Golden Tree Pot',
            'Golden Apple',
            'Golden Fish',
            'Golden Candle Holder',
            'Golden Lamp',
            'Golden Crescent Moon Bed',
            'Golden Teddy Bear',
            'Golden Lollipop',
            'Golden Game Boy Advance',
            'Golden Robot',
            'Golden Rocket',
            'Golden Rocking Horse',
        },
    }

    web = WL4Web()

    def generate_early(self):
        if self.options.goal in (Goal.option_local_golden_treasure_hunt, Goal.option_local_golden_diva_treasure_hunt):
            self.options.local_items.value.update(self.item_name_groups['Golden Treasure'])
        if self.options.required_jewels > self.options.pool_jewels:
            self.options.pool_jewels = PoolJewels(self.options.required_jewels)
        if self.options.required_jewels >= 1 and self.options.golden_jewels == 0:
            self.options.golden_jewels = GoldenJewels(1)

    def create_regions(self):
        location_table = self.setup_locations()
        create_regions(self, location_table)
        set_access_rules(self)
        connect_regions(self)

        passages = ('Emerald', 'Ruby', 'Topaz', 'Sapphire')
        for passage in passages:
            location = self.multiworld.get_region(f'{passage} Passage Boss', self.player).locations[0]
            location.place_locked_item(self.create_item(f'{passage} Passage Clear'))
            location.show_in_spoiler = False

        if self.options.goal.needs_diva():
            goal = 'Golden Diva'
        if self.options.goal.is_treasure_hunt():
            goal = 'Sound Room - Emergency Exit'

        goal = self.multiworld.get_location(goal, self.player)
        goal.place_locked_item(self.create_item('Escape the Pyramid'))
        goal.show_in_spoiler = False

    def create_items(self):
        difficulty = self.options.difficulty
        treasure_hunt = self.options.goal.needs_treasure_hunt()

        gem_pieces = 18 * 4
        cds = 16
        full_health_items = (9, 7, 6)[difficulty.value]
        treasures = 12 * treasure_hunt
        total_required_locations = gem_pieces + cds + full_health_items + treasures

        itempool = []

        required_jewels = self.options.required_jewels.value
        pool_jewels = self.options.pool_jewels.value
        for name, item in filter_items(type=ItemType.JEWEL):
            force_non_progression = required_jewels == 0
            if item.passage() == Passage.ENTRY:
                copies = min(pool_jewels, 1)
            elif item.passage() == Passage.GOLDEN:
                copies = self.options.golden_jewels.value
                if self.options.goal.is_treasure_hunt():
                    force_non_progression = True
            else:
                copies = pool_jewels

            for _ in range(copies):
                itempool.append(self.create_item(name, force_non_progression))

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

        if (treasure_hunt):
            for name in filter_item_names(type=ItemType.TREASURE):
                itempool.append(self.create_item(name))

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
            patch_rom(rom, self)

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

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(
            'goal',
            'difficulty',
            'logic',
            'required_jewels',
            'open_doors',
            'portal',
        )

    def create_item(self, name: str, force_non_progression=False) -> Item:
        return WL4Item.from_name(name, self.player, force_non_progression)

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = (
            lambda state: state.has('Escape the Pyramid', self.player))

    def setup_locations(self):
        checks = filter(lambda p: self.options.difficulty in p[1].difficulties, location_table.items())
        if not self.options.goal.needs_treasure_hunt():
            checks = filter(lambda p: p[1].source != LocationType.CHEST, checks)
        checks = {name for name, _ in checks}

        if self.options.goal.needs_diva():
            checks.remove('Sound Room - Emergency Exit')
        else:
            checks.remove('Golden Diva')
        return checks
