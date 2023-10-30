import settings

from BaseClasses import Tutorial
from ..AutoWorld import World, WebWorld


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
    # option_definitions = pokemon_rb_options
    # settings: typing.ClassVar[PokemonSettings]

    data_version = 0
    required_client_version = (0, 4, 3)

    topology_present = True

    # item_name_to_id = {name: data.id for name, data in item_table.items()}
    # location_name_to_id = {location.name: location.address for location in location_data if location.type == "Item"
    # and location.address is not None}
    # item_name_groups = item_groups

    web = PokemonCrystalWebWorld()
