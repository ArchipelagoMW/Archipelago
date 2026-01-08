# __init__.py
#
# Copyright (C) 2025 James Petersen <m@jamespetersen.ca>
# Licensed under MIT. See LICENSE

from BaseClasses import ItemClassification, Tutorial
from collections.abc import Iterable, Mapping
import pkgutil
import settings
from typing import ClassVar, Any
from worlds.AutoWorld import WebWorld, World

from .client import PokemonPlatinumClient
from .data import items as itemdata
from .data.locations import RequiredLocations
from .items import create_item_label_to_code_map, get_item_classification, PokemonPlatinumItem, get_item_groups
from .locations import PokemonPlatinumLocation, create_location_label_to_code_map, create_locations
from .options import PokemonPlatinumOptions, UnownsOption
from .regions import create_regions
from .rom import generate_output, PokemonPlatinumPatch
from .rules import set_rules

class PokemonPlatinumSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        description = "Pokemon Platinum US (Rev 0 or 1) ROM File"
        copy_to = "pokeplatinum.nds"
        md5s = PokemonPlatinumPatch.hashes

    rom_file: RomFile = RomFile(RomFile.copy_to)

class PokemonPlatinumWebWorld(WebWorld):
    theme = 'ocean'

    setup_en = Tutorial(
        'Multiworld Setup Guide',
        'A guide to playing Pokémon Platinum with Archipelago',
        'English',
        'setup_en.md',
        'setup/en',
        ['ljtpetersen']
    )

    tutorials = [setup_en]

class PokemonPlatinumWorld(World):
    game = "Pokemon Platinum"
    web = PokemonPlatinumWebWorld()
    topology_present = True

    settings_key = "pokemon_platinum_settings"
    settings: ClassVar[PokemonPlatinumSettings] # type: ignore

    options_dataclass = PokemonPlatinumOptions
    options: PokemonPlatinumOptions # type: ignore

    item_name_to_id = create_item_label_to_code_map()
    location_name_to_id = create_location_label_to_code_map()
    item_name_groups = get_item_groups()

    required_locations: RequiredLocations

    def generate_early(self) -> None:
        self.required_locations = RequiredLocations(self.options)
        self.options.validate()

    def get_filler_item_name(self) -> str:
        # TODO
        return "Great Ball"

    def create_regions(self) -> None:
        regions = create_regions(self)

        create_locations(self, regions)
        self.multiworld.regions.extend(regions.values())

    def create_items(self) -> None:
        locations: Iterable[PokemonPlatinumLocation] = self.multiworld.get_locations(self.player) # type: ignore
        item_locations = filter(
            lambda loc : loc.address is not None and loc.is_enabled and not loc.locked,
            locations)

        add_items: list[str] = []
        for item in ["master_repel", "s_s_ticket", "marsh_pass", "storage_key"]:
            if getattr(self.options, item).value == 1:
                add_items.append(item)
        if self.options.bag.value == 1:
            add_items.append("bag")
        else:
            self.multiworld.push_precollected(self.create_item(itemdata.items["bag"].label))

        itempool = []
        for loc in item_locations:
            item_id: int = loc.default_item_id # type: ignore
            if item_id > 0 and get_item_classification(item_id) != ItemClassification.filler:
                itempool.append(self.create_item_by_code(item_id))
            elif add_items:
                itempool.append(self.create_item(itemdata.items[add_items.pop()].label))
            else:
                itempool.append(self.create_item_by_code(item_id))

        self.multiworld.itempool += itempool
        for item in add_items:
            self.multiworld.push_precollected(self.create_item(itemdata.items[item].label))

    def create_item(self, name: str) -> PokemonPlatinumItem:
        return self.create_item_by_code(self.item_name_to_id[name])

    def create_item_by_code(self, item_code: int):
        return PokemonPlatinumItem(
            self.item_id_to_name[item_code],
            get_item_classification(item_code),
            item_code,
            self.player)

    def set_rules(self) -> None:
        set_rules(self)

    def generate_output(self, output_directory: str) -> None:
        patch = PokemonPlatinumPatch(player=self.player, player_name=self.player_name)
        base_patches = ["us_rev0", "us_rev1"]
        for name in base_patches:
            name = "base_patch_" + name
            patch.write_file(f"{name}.bsdiff4", pkgutil.get_data(__name__, f"patches/{name}.bsdiff4")) # type: ignore
        generate_output(self, output_directory, patch)

    def create_event(self, name: str) -> PokemonPlatinumItem:
        return PokemonPlatinumItem(
            name,
            ItemClassification.progression,
            None,
            self.player)

    def fill_slot_data(self) -> Mapping[str, Any]:
        ret = self.options.as_dict("goal", "remote_items")
        return ret
