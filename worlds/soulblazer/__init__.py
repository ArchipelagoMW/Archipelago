import settings
import copy
import os
from hashlib import blake2b
from typing import Any, List, Dict, Optional, ClassVar
from .Client import SoulBlazerSNIClient
from .Options import SoulBlazerOptions  # the options we defined earlier
from .Items import (
    SoulBlazerItem,
    SoulBlazerItemData,
    all_items_table,
    repeatable_items_table,
    create_itempool,
    swords_table,
)  # data used below to add items to the World
from .Locations import SoulBlazerLocation, all_locations_table  # same as above
from .Names import ItemName, ChestName, Addresses
from .Regions import create_regions as region_create_regions
#from .Rules import set_rules as rules_set_rules
from .Rom import SoulBlazerDeltaPatch, LocalRom, patch_rom, get_base_rom_path
from worlds.AutoWorld import WebWorld, World
from BaseClasses import MultiWorld, Region, Location, Entrance, Item, ItemClassification, Tutorial

class SoulBlazerSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the Soul Blazer US rom"""

        copy_to = "Soul Blazer (USA).sfc"
        description = "Soul blazer (US) ROM File"
        md5s = [SoulBlazerDeltaPatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class SoulBlazerWeb(WebWorld):
    theme = "grass"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Soul Blazer randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Tranquilite"],
    )

    tutorials = [setup_en]


class SoulBlazerWorld(World):
    """Insert description of the world/game here."""

    game = "Soul Blazer"  # name of the game/world
    options_dataclass = SoulBlazerOptions  # options the player can set
    options: SoulBlazerOptions  # typing hints for option results
    settings: ClassVar[SoulBlazerSettings]  # will be automatically assigned from type hint
    # topology_present = True  # show path to required location checks in spoiler

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {name: data.code for name, data in all_items_table.items()}
    location_name_to_id = {name: data.address for name, data in all_locations_table.items()}

    # Items can be grouped using their names to allow easy checking if any item
    # from that group has been collected. Group names can also be used for !hint
    # TODO: Define groups?
    # item_name_groups = {
    #    "weapons": {"sword", "lance"},
    # }

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.exp_items: List[SoulBlazerItem]
        self.gem_items: List[SoulBlazerItem]
        self.pre_fill_items: List[Item] = []
        self.rom_name: bytes
        # self.set_rules = set_rules
        # self.create_regions = create_regions

    def create_item(self, item: str) -> SoulBlazerItem:
        if item in repeatable_items_table:
            # Create shallow copy of repeatable items so we can change the operand if needed.
            data = copy.copy(repeatable_items_table[item])
        else:
            data = all_items_table[item]
        return SoulBlazerItem(item, self.player, data)

    def get_pre_fill_items(self) -> List[Item]:
        return self.pre_fill_items

    def create_victory_event(self, region: Region) -> Location:
        """Creates the `"Victory"` item/location event pair"""
        victory_loc = Location(self.player, "Victory", None, region)
        victory_loc.place_locked_item(Item("Victory", ItemClassification.progression, None, self.player))
        return victory_loc

    @classmethod
    def stage_assert_generate(cls, multiworld: "MultiWorld") -> None:
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def generate_early(self) -> None:
        from Utils import __version__
        data = bytes(f'SoulBlazer_{__version__}_{self.player}_{self.multiworld.seed}', 'ascii')
       
        hash = blake2b(data, digest_size=9, key=bytes(str(self.multiworld.seed), 'ascii'))
        self.rom_name = b'SB_' + bytes(hash.hexdigest(), 'ascii')
        # Should already be the correct length of 21 bytes, but ensure anyway.
        self.rom_name = self.rom_name[:Addresses.ROMNAME_SIZE]

    # def create_regions(self) -> None:
    #    pass
    create_regions = region_create_regions

    def create_items(self) -> None:
        itempool = create_itempool(self)

        if self.options.starting_sword == "randomized":
            starting_sword_name = self.random.choice(list(swords_table.keys()))
        else:
            starting_sword_name = ItemName.LIFESWORD

        starting_sword = next(x for x in itempool if x.name == starting_sword_name)
        self.pre_fill_items.append(starting_sword)
        itempool.remove(starting_sword)
        self.multiworld.get_location(ChestName.TRIAL_ROOM, self.player).place_locked_item(starting_sword)

        # TODO: anything else to pre-fill?

        self.multiworld.itempool += itempool

    def set_rules(self) -> None:
        pass

    #set_rules = rules_set_rules

    def generate_basic(self) -> None:
        pass

    def pre_fill(self) -> None:
        pass

    def fill_hook(
        self,
        progitempool: List["Item"],
        usefulitempool: List["Item"],
        filleritempool: List["Item"],
        fill_locations: List["Location"],
    ) -> None:
        pass

    def post_fill(self) -> None:
        pass

    def generate_output(self, output_directory: str):
        try:
            rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.sfc")

            rom = LocalRom(get_base_rom_path(), name=self.rom_name)
            patch_rom(self, rom)

            rom.write_to_file(rompath)

            patch = SoulBlazerDeltaPatch(
                os.path.splitext(rompath)[0] + SoulBlazerDeltaPatch.patch_file_ending,
                player=self.player,
                player_name=self.multiworld.player_name[self.player],
                patched_path=rompath,
            )
            patch.write()
        except:
            raise
        finally:
            if os.path.exists(rompath):
                os.unlink(rompath)

    def fill_slot_data(self) -> Dict[str, Any]:
        gem_data = {
            f"{item.code}:{item.location.address}:{item.location.player}": item.operand_for_id
            for item in self.gem_items
        }
        exp_data = {
            f"{item.code}:{item.location.address}:{item.location.player}": item.operand_for_id
            for item in self.exp_items
        }
        return {'gem_data': gem_data, 'exp_data': exp_data}

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        pass

    def modify_multidata(self, multidata: Dict[str, Any]) -> None:
        import base64
        new_name = base64.b64encode(self.rom_name).decode()
        multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]
