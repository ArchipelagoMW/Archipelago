import typing

from BaseClasses import Item, ItemClassification, Tutorial
from worlds.AutoWorld import WebWorld, World

from .Items import WL4Item, item_table
from .Locations import all_locations
from .Logic import WL4Logic
from .Names import ItemName, LocationName
from .Options import wl4_options
from .Regions import connect_regions, create_regions
from .Rom import LocalRom, WL4DeltaPatch, get_base_rom_path, patch_rom 


class WL4Web(WebWorld):
    theme = "grass"

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
    game: str = "Wario Land 4"
    option_definitions = wl4_options
    topology_present = False

    data_version = 0

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations

    web = WL4Web()

    def generate_basic(self) -> None:
        itempool: typing.List[WL4Item] = []

        connect_regions(self.multiworld, self.player)

        diamond_pieces = 18 * 4
        cds = 16
        full_health_items = 17
        total_required_locations = diamond_pieces + cds + full_health_items

        for item, data in Items.box_table.items():
            for _ in range(data.quantity):
                itempool.append(self.create_item(item))

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
            self.multiworld.get_location(location_name, self.player).place_locked_item(
                self.create_event(ItemName.defeated_boss)
            )

        self.multiworld.get_location(
            LocationName.golden_diva, self.player
        ).place_locked_item(self.create_event(ItemName.victory))

        self.multiworld.itempool += itempool

        self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.victory, self.player)
    
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

    def create_regions(self):
        create_regions(self.multiworld, self.player)

    def create_item(self, name: str, force_non_progression=False) -> Item:
        data = item_table[name]

        if force_non_progression:
            classification = ItemClassification.filler
        elif data.progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        created_item = WL4Item(name, classification, data.code, self.player)

        return created_item
    
    def create_event(self, name: str):
        return WL4Item(name, ItemClassification.progression, None, self.player)
