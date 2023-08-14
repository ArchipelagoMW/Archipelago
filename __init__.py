import typing
import settings

from BaseClasses import Item, ItemClassification, Tutorial
from worlds.AutoWorld import WebWorld, World

from .items import WL4Item, item_table
from .locations import all_locations, setup_locations
from .logic import WL4Logic
from .names import ItemName, LocationName
from .options import wl4_options
from .regions import connect_regions, create_regions
from .rom import LocalRom, WL4DeltaPatch, get_base_rom_path, patch_rom


class WL4Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Wario Land 4 NA/EU ROM"""
        description = "Wario Land 4 (U/E) ROM File"
        copy_to = "Wario Land 4 (UE) [!].gba"
        md5s = [WL4DeltaPatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True


class WL4Web(WebWorld):
    theme = "jungle"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Wario Land 4 randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["lil David"]
    )

    tutorials = [setup_en]


class WL4World(World):
    """
    A golden pyramid has been discovered deep in the jungle, and Wario, has set
    out to rob it. But to make off with its legendary treasure, he has to first
    defeat the five passage bosses and the pyramid's evil ruler, the Golden Diva.
    """

    game: str = "Wario Land 4"
    option_definitions = wl4_options
    settings: typing.ClassVar[WL4Settings]
    topology_present = False

    data_version = 0

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations

    web = WL4Web()

    def generate_early(self):
        if self.multiworld.early_entry_jewels[self.player]:
            self.multiworld.local_early_items[self.player][ItemName.entry_passage_jewel.ne] = 1
            self.multiworld.local_early_items[self.player][ItemName.entry_passage_jewel.se] = 1
            self.multiworld.local_early_items[self.player][ItemName.entry_passage_jewel.sw] = 1
            self.multiworld.local_early_items[self.player][ItemName.entry_passage_jewel.nw] = 1

    def create_regions(self):
        location_table = setup_locations(self.multiworld, self.player)
        create_regions(self.multiworld, self.player, location_table)

        itempool: typing.List[WL4Item] = []

        connect_regions(self.multiworld, self.player)

        diamond_pieces = 18 * 4
        cds = 16
        full_health_items = (9, 7, 5)[self.multiworld.difficulty[self.player].value]
        total_required_locations = diamond_pieces + cds + full_health_items

        for item, data in items.box_table.items():
            for _ in range(data.quantity):
                itempool.append(self.create_item(item))

        for _ in range(full_health_items):
            itempool.append(self.create_item(ItemName.full_health))

        junk_count = total_required_locations - len(itempool)
        assert junk_count == 0, f"Mismatched location counts: {junk_count} empty checks"

        boss_location_names = [
            LocationName.spoiled_rotten,
            LocationName.cractus,
            LocationName.cuckoo_condor,
            LocationName.aerodent,
            LocationName.catbat,
        ]
        for location_name in boss_location_names:
            (self.multiworld
                .get_location(location_name, self.player)
                .place_locked_item(self.create_event(ItemName.defeated_boss)))

        (self.multiworld
            .get_location(LocationName.golden_diva, self.player)
            .place_locked_item(self.create_event(ItemName.victory)))

        self.multiworld.itempool += itempool

    def generate_output(self, output_directory: str):
        from pathlib import Path
        output_directory: Path = Path(output_directory)

        try:
            world = self.multiworld
            player = self.player

            rom = LocalRom(get_base_rom_path())
            patch_rom(rom, self.multiworld, self.player)

            rompath = output_directory / f"{world.get_out_file_name_base(player)}.gba"
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

        if force_non_progression:
            classification = ItemClassification.filler
        else:
            classification = data.classification

        created_item = WL4Item(name, classification, data.code, self.player)

        return created_item

    def create_event(self, name: str):
        return WL4Item(name, ItemClassification.progression, None, self.player)

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = (
            lambda state: state.has(ItemName.victory, self.player))
