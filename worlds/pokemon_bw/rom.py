import os
import pathlib
import zipfile
from io import BytesIO

from .ndspy import rom as ndspy_rom

import Utils
from settings import get_settings
from worlds.Files import APAutoPatchInterface
from typing import TYPE_CHECKING, Any, Dict, Callable

from .patch.procedures import base_patch, season_patch, write_wild_pokemon, level_adjustments, write_trainer_pokemon, modify_rates

if TYPE_CHECKING:
    from . import PokemonBWWorld


class PokemonBlackPatch(APAutoPatchInterface):
    game = "Pokemon Black and White"
    patch_file_ending = ".apblack"
    result_file_ending = ".nds"

    def __init__(self, path: str, player=None, player_name="", world=None):
        self.world: "PokemonBWWorld" = world
        self.files: dict[str, bytes] = {}
        super().__init__(path, player, player_name, "")

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super().write_contents(opened_zipfile)
        PatchMethods.write_contents(self, opened_zipfile)

    def get_manifest(self) -> Dict[str, Any]:
        return PatchMethods.get_manifest(self, super().get_manifest())

    def patch(self, target: str) -> None:
        PatchMethods.patch(self, target, "black")

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> Dict[str, Any]:
        return PatchMethods.read_contents(self, opened_zipfile, super().read_contents(opened_zipfile))

    def get_file(self, file: str) -> bytes:
        return PatchMethods.get_file(self, file)


class PokemonWhitePatch(APAutoPatchInterface):
    game = "Pokemon Black and White"
    patch_file_ending = ".apwhite"
    result_file_ending = ".nds"

    def __init__(self, path: str, player=None, player_name="", world=None):
        self.world: "PokemonBWWorld" = world
        self.files: dict[str, bytes] = {}
        super().__init__(path, player, player_name, "")

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super().write_contents(opened_zipfile)
        PatchMethods.write_contents(self, opened_zipfile)

    def get_manifest(self) -> Dict[str, Any]:
        return PatchMethods.get_manifest(self, super().get_manifest())

    def patch(self, target: str) -> None:
        PatchMethods.patch(self, target, "white")

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> Dict[str, Any]:
        return PatchMethods.read_contents(self, opened_zipfile, super().read_contents(opened_zipfile))

    def get_file(self, file: str) -> bytes:
        return PatchMethods.get_file(self, file)


PokemonBWPatch = PokemonBlackPatch | PokemonWhitePatch


class PatchMethods:

    @staticmethod
    def write_contents(patch: PokemonBWPatch, opened_zipfile: zipfile.ZipFile) -> None:

        write_wild = False
        for encounter in patch.world.wild_encounter.values():
            if encounter.write:
                write_wild = True
                break

        procedures: list[str] = ["base_patch"]
        if patch.world.options.season_control != "vanilla":
            procedures.append("season_patch")
        if write_wild:
            procedures.append("write_wild_pokemon")
            write_wild_pokemon.write_patch(patch, opened_zipfile)
        if "Randomize" in patch.world.options.randomize_trainer_pokemon:
            procedures.append("write_trainer_pokemon")
            write_trainer_pokemon.write_species(patch, opened_zipfile)
        if "Wild" in patch.world.options.adjust_levels:
            procedures.append("adjust_wild_levels")
        if "Trainer" in patch.world.options.adjust_levels:
            procedures.append("adjust_trainer_levels")
        if patch.world.options.modify_encounter_rates != "vanilla":
            procedures.append("modify_rates")
            modify_rates.write_patch(patch, opened_zipfile)

        opened_zipfile.writestr("procedures.txt", "\n".join(procedures))

    @staticmethod
    def get_manifest(patch: PokemonBWPatch, manifest: dict[str, Any]) -> Dict[str, Any]:
        from .data import version

        manifest["bw_patch_format"] = version.patch_file()
        return manifest

    @staticmethod
    def patch(patch: PokemonBWPatch, target: str, version_name: str) -> None:
        from .data import version

        patch.read()

        if pathlib.Path(target).exists():
            with open(target, "rb") as f:
                header_part = f.read(0xA0)
                found_rom_version = tuple(header_part[0x9D:0xA0])
                if version.rom() == found_rom_version:
                    return

        with BytesIO() as bytes_io, zipfile.ZipFile(bytes_io, "w", zipfile.ZIP_DEFLATED, True, 9) as files_dump:
            base_data = get_base_rom_bytes(version_name)
            rom = ndspy_rom.NintendoDSRom(base_data)
            procedures: list[str] = str(patch.get_file("procedures.txt"), "utf-8").splitlines()
            for prod in procedures:
                patch_procedures[prod](rom, __name__, patch, files_dump)
            with open(target, 'wb') as f:
                f.write(rom.save(updateDeviceCapacity=True))
            if get_settings()["pokemon_bw_settings"]["dump_patched_files"]:
                with open(target.replace(".nds", "_files_dump.zip"), "wb") as dump:
                    bytes_io.flush()
                    dump.write(bytes_io.getvalue())

    @staticmethod
    def read_contents(patch: PokemonBWPatch, opened_zipfile: zipfile.ZipFile,
                      manifest: Dict[str, Any]) -> Dict[str, Any]:
        from .data import version

        for file in opened_zipfile.namelist():
            if file not in ["archipelago.json"]:
                patch.files[file] = opened_zipfile.read(file)

        if tuple(manifest["bw_patch_format"]) > version.patch_file():
            raise Exception(f"File (BW patch version: {'.'.join(str(i) for i in manifest['bw_patch_format'])}) too new "
                            f"for this handler (BW patch version: {version.patch_file()}). "
                            f"Please update your apworld.")
        elif tuple(manifest["bw_patch_format"]) < version.patch_file():
            raise Exception(f"File (BW patch version: {'.'.join(str(i) for i in manifest['bw_patch_format'])}) too old "
                            f"for this handler (BW patch version: {version.patch_file()}). "
                            f"Either re-generate your world or downgrade to an older apworld version.")

        return manifest

    @staticmethod
    def get_file(patch: PokemonBWPatch, file: str) -> bytes:
        if file not in patch.files:
            patch.read()
        return patch.files[file]


patch_procedures: dict[str, Callable[[ndspy_rom.NintendoDSRom, str, PokemonBWPatch, zipfile.ZipFile], None]] = {
    "base_patch": base_patch.patch,
    "season_patch": season_patch.patch,
    "write_wild_pokemon": write_wild_pokemon.patch,
    "write_trainer_pokemon": write_trainer_pokemon.patch_species,
    "adjust_wild_levels": level_adjustments.patch_wild,
    "adjust_trainer_levels": level_adjustments.patch_trainer,
    "modify_rates": modify_rates.patch,
}


def get_base_rom_bytes(version: str, file_name: str = "") -> bytes:
    if not file_name:
        file_name = get_base_rom_path(version, file_name)
    with open(file_name, "rb") as file:
        base_rom_bytes = bytes(file.read())
    if version == "black" and base_rom_bytes[:18] != b'POKEMON\x20B\0\0\0IRBO01':
        raise Exception(f"Supplied Base Rom appears to not be an english copy of Pokémon Black Version: "
                        f"{base_rom_bytes[:18]}")
    if version == "white" and base_rom_bytes[:18] != b'POKEMON\x20W\0\0\0IRAO01':
        raise Exception(f"Supplied Base Rom appears to not be an english copy of Pokémon White Version: "
                        f"{base_rom_bytes[:18]}")
    return base_rom_bytes


def get_base_rom_path(version: str, file_name: str = "") -> str:
    if not file_name:
        file_name = get_settings()["pokemon_bw_settings"][f"{version}_rom"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
