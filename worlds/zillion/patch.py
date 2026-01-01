import os
from typing import Any, BinaryIO
import zipfile

from typing_extensions import override

import Utils
from worlds.Files import APAutoPatchInterface

from zilliandomizer.patch import Patcher

from .gen_data import GenData

US_HASH = "d4bf9e7bcf9a48da53785d2ae7bc4270"


class ZillionPatch(APAutoPatchInterface):
    hash = US_HASH
    game = "Zillion"
    patch_file_ending = ".apzl"
    result_file_ending = ".sms"

    gen_data_str: str
    """ JSON encoded """

    def __init__(self,
                 path: str | None = None,
                 player: int | None = None,
                 player_name: str = "",
                 server: str = "",
                 *,
                 gen_data_str: str = "") -> None:
        super().__init__(path=path, player=player, player_name=player_name, server=server)
        self.gen_data_str = gen_data_str

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_base_rom_path(), "rb") as stream:
            return read_rom(stream)

    @override
    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super().write_contents(opened_zipfile)
        opened_zipfile.writestr("gen_data.json",
                                self.gen_data_str,
                                compress_type=zipfile.ZIP_DEFLATED)

    @override
    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> dict[str, Any]:
        manifest = super().read_contents(opened_zipfile)
        self.gen_data_str = opened_zipfile.read("gen_data.json").decode()
        return manifest

    @override
    def patch(self, target: str) -> None:
        self.read()
        write_rom_from_gen_data(self.gen_data_str, target)


def get_base_rom_path(file_name: str | None = None) -> str:
    from . import ZillionSettings, ZillionWorld
    settings: ZillionSettings = ZillionWorld.settings
    if not file_name:
        file_name = settings.rom_file
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def read_rom(stream: BinaryIO) -> bytes:
    """ reads rom into bytearray """
    data = stream.read()
    # I'm not aware of any sms header.
    return data


def write_rom_from_gen_data(gen_data_str: str, output_rom_file_name: str) -> None:
    """ take the output of `GenData.to_json`, and create rom from it """
    gen_data = GenData.from_json(gen_data_str)

    base_rom_path = get_base_rom_path()
    zz_patcher = Patcher(base_rom_path)

    zz_patcher.write_locations(gen_data.zz_game.regions, gen_data.zz_game.char_order[0])
    zz_patcher.all_fixes_and_options(gen_data.zz_game)
    zz_patcher.set_external_item_interface(gen_data.zz_game.char_order[0], gen_data.zz_game.options.max_level)
    zz_patcher.set_multiworld_items(gen_data.multi_items)
    zz_patcher.set_rom_to_ram_data(gen_data.game_id)

    patched_rom_bytes = zz_patcher.get_patched_bytes()
    with open(output_rom_file_name, "wb") as binary_file:
        binary_file.write(patched_rom_bytes)
