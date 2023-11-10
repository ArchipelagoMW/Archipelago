import settings
import typing
import os
import sys

from BaseClasses import Tutorial
from worlds.AutoWorld import World, WebWorld
if "worlds._bizhawk" not in sys.modules:
    bh_apworld_path = os.path.join(os.path.dirname(
        sys.modules["worlds"].__file__), "_bizhawk.apworld")
    if not os.path.isfile(bh_apworld_path) and not os.path.isdir(os.path.splitext(bh_apworld_path)[0]):
        logging.warning(
            "Did not find _bizhawk.apworld required to play Pokemon Crystal. Still able to generate.")
    else:
        # Unused, but required to register with BizHawkClient
        from .client import PokemonCrystalClient
else:
    # Unused, but required to register with BizHawkClient
    from .client import PokemonCrystalClient
from .options import pokemon_crystal_options
from .regions import create_regions
from .items import PokemonCrystalItem, create_item_label_to_code_map, get_item_classification
from .rules import set_rules
from .data import data as crystal_data
from .rom import generate_output
from .locations import create_locations, PokemonCrystalLocation, create_location_label_to_id_map


class PokemonCrystalSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        description = "Pokemon Crystal (UE) (V1.0) ROM File"
        copy_to = "Pokemon - Crystal Version (UE) (V1.0) [C][!].gbc"
        md5s = ["9f2922b235a5eeb78d65594e82ef5dde"]

    class RomStart(str):
        """
        Set this to false to never autostart a rom (such as after patching)
        True for operating system default program
        Alternatively, a path to a program to open the .gb file with
        """

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: typing.Union[RomStart, bool] = True


class PokemonCrystalWebWorld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Pokemon Crystal with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["AliceMousie"]
    )]


class PokemonCrystalWorld(World):
    """the only good pokemon game"""
    game = "Pokemon Crystal"
    option_definitions = pokemon_crystal_options
    settings: typing.ClassVar[PokemonCrystalSettings]
    topology_present = True

    settings_key = "pokemon_crystal_settings"
    settings: typing.ClassVar[PokemonCrystalSettings]

    data_version = 0
    required_client_version = (0, 4, 3)

    item_name_to_id = create_item_label_to_code_map()
    location_name_to_id = create_location_label_to_id_map()
    item_name_groups = {}  # item_groups

    web = PokemonCrystalWebWorld()

    def create_regions(self) -> None:
        regions = create_regions(self)
        create_locations(self, regions, self.options.randomize_hidden_items)
        self.multiworld.regions.extend(regions.values())

    def create_items(self) -> None:
        item_locations: List[PokemonEmeraldLocation] = [
            location
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ]

        default_itempool = [self.create_item_by_code(
            location.default_item_code) for location in item_locations]
        self.multiworld.itempool += default_itempool

    def set_rules(self) -> None:
        set_rules(self)

    def generate_output(self, output_directory: str) -> None:
        generate_output(self, output_directory)

    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:
        slot_data = self.options.as_dict(
            "randomize_hidden_items",
            "randomize_starters",
            "randomize_wilds",
            "randomize_learnsets",
            "full_tmhm_compatibility",
            "blind_trainers",
            "better_marts",
            "goal"
        )
        return slot_data

    def create_item(self, name: str) -> PokemonCrystalItem:
        return self.create_item_by_code(self.item_name_to_id[name])

    def create_item_by_code(self, item_code: int) -> PokemonCrystalItem:
        return PokemonCrystalItem(
            self.item_id_to_name[item_code],
            get_item_classification(item_code),
            item_code,
            self.player
        )
