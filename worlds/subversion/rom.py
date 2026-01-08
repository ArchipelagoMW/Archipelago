import hashlib
from logging import getLogger
import os
from typing import Any, Optional
from typing_extensions import override
import zipfile

import Utils
from Utils import read_snes_rom
from worlds.Files import APContainer, APDeltaPatch

from .patch_utils import (
    LOGIC_LENGTH, LOGIC_LOCATION,
    ItemRomData, get_gen_data, get_multi_patch_path, ips_patch_from_file, offset_from_symbol, patch_item_sprites
)

from subversion_rando.logic_presets import custom_logic_str_from_tricks
from subversion_rando.main_generation import apply_rom_patches
from subversion_rando.romWriter import RomWriter


SMJUHASH = '21f3e98df4780ee1c667b84e57d88675'


# SNIClient assumes that the patch it gets is an APDeltaPatch
# Otherwise, it might be better to inherit from APContainer instead of APDeltaPatch.
# So in some places, instead of calling `super()`, we jump over APDeltaPatch to APContainer
# because we don't have a bs4diff.

class SubversionDeltaPatch(APDeltaPatch):
    hash = SMJUHASH
    game = "Subversion"
    patch_file_ending = ".apsv"

    gen_data: str
    """ JSON encoded """

    def __init__(self, *args: Any, patched_path: str = "", gen_data: str = "", **kwargs: Any) -> None:
        super().__init__(*args, patched_path=patched_path, **kwargs)
        self.gen_data = gen_data

    @override
    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    @override
    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        APContainer.write_contents(self, opened_zipfile)
        opened_zipfile.writestr("rom_data.json",
                                self.gen_data,
                                compress_type=zipfile.ZIP_DEFLATED)

    @override
    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        APContainer.read_contents(self, opened_zipfile)
        self.gen_data = opened_zipfile.read("rom_data.json").decode()

    @override
    def patch(self, target: str) -> None:
        self.read()
        write_rom_from_gen_data(self.gen_data, target)


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes: Optional[bytes] = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if SMJUHASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for Japan+US release. '
                            'Get the correct game and version, then dump it')
        setattr(get_base_rom_bytes, "base_rom_bytes", base_rom_bytes)
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["sm_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def write_rom_from_gen_data(gen_data_str: str, output_rom_file_name: str) -> None:
    """ take the output of `make_gen_data`, and create rom from it """
    from Utils import user_path

    gen_data = get_gen_data(gen_data_str)

    base_rom_path = get_base_rom_path()
    RomWriter.patch_cache_dir = user_path('lib')
    rom_writer = RomWriter.fromFilePaths(base_rom_path)  # this patches SM to Subversion 1.2
    logger = getLogger("Subversion")
    logger.debug("patched Super Metroid to Subversion")

    multi_patch_path = get_multi_patch_path()
    rom_writer.rom_data = ips_patch_from_file(multi_patch_path, rom_writer.rom_data)

    rom_writer.rom_data = patch_item_sprites(rom_writer.rom_data)

    rom_writer.rom_data = ItemRomData.patch_from_json(rom_writer.rom_data, gen_data.item_rom_data)

    apply_rom_patches(gen_data.sv_game, rom_writer)

    # TODO: deathlink
    # self.multiworld.death_link[self.player].value
    offset_from_symbol("config_deathlink")

    remote_items_offset = offset_from_symbol("config_remote_items")
    remote_items_value = 0b101
    # TODO: if remote items: |= 0b10
    rom_writer.writeBytes(remote_items_offset, remote_items_value.to_bytes(1, "little"))

    player_id_offset = offset_from_symbol("config_player_id")
    rom_writer.writeBytes(player_id_offset, gen_data.player.to_bytes(2, "little"))

    rom_writer.writeBytes(0x7fc0, gen_data.game_name_in_rom)

    logic = custom_logic_str_from_tricks(gen_data.sv_game.options.logic).encode()
    assert len(logic) == LOGIC_LENGTH
    rom_writer.writeBytes(LOGIC_LOCATION, logic)

    rom_writer.finalizeRom(output_rom_file_name)  # writes rom file
