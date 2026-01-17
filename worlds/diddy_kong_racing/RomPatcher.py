import asyncio
import hashlib
import os
import pathlib
import sys
import zipfile

import bsdiff4

from CommonClient import logger
from Utils import open_filename

patched_rom_filename_template: str = "Diddy-Kong-Racing-AP-{}.z64"
vanilla_rom_md5: str = "4f0e07f0eeac7e5d7ce3a75461888d03"
vanilla_swapped_rom_md5: str = "e00c0e6bfb0ce740e3e1c50ba82bc01a"
patched_rom_md5: str = "0868b4f2d20734863af43ddb22c61486"


async def apply_patch(version_number: str) -> None:
    fpath = pathlib.Path(__file__)
    archipelago_root = None
    for i in range(0, 5, +1):
        if fpath.parents[i].stem == "Archipelago":
            archipelago_root = pathlib.Path(__file__).parents[i]
            break

    patched_rom_filename = patched_rom_filename_template.format(version_number)
    patched_rom_path = None
    if archipelago_root:
        patched_rom_path = os.path.join(archipelago_root, patched_rom_filename)

    if not patched_rom_path or get_file_md5(patched_rom_path) != patched_rom_md5:
        await asyncio.sleep(0.01)
        rom = open_filename("Select your Diddy Kong Racing US 1.0 ROM",
                            (("Rom Files", (".z64", ".n64")), ("All Files", "*")))
        if not rom:
            logger.error(
                "ERROR: No ROM selected. Please restart the Diddy Kong Racing client and select your Diddy Kong Racing US 1.0 ROM."
            )
            raise Exception

        if not patched_rom_path:
            base_dir = os.path.dirname(rom)
            patched_rom_path = os.path.join(base_dir, patched_rom_filename)

        patch_rom(rom, patched_rom_path, "Diddy_Kong_Racing.patch")

    if patched_rom_path:
        logger.info("Patched Diddy Kong Racing is located in " + patched_rom_path)
        logger.info("Please open the patched Diddy Kong Racing ROM in Bizhawk and run connector_diddy_kong_racing.lua")


def get_file_md5(patched_rom: str) -> str | None:
    if os.path.isfile(patched_rom):
        patched_rom_file = read_file(patched_rom)
        return hashlib.md5(patched_rom_file).hexdigest()

    return None


def patch_rom(vanilla_rom_path: str, output_path: str, patch_path: str) -> None:
    rom = read_file(vanilla_rom_path)
    rom_md5 = hashlib.md5(rom).hexdigest()
    if rom_md5 == vanilla_swapped_rom_md5:
        rom = swap(rom)
    elif rom_md5 != vanilla_rom_md5:
        logger.error(
            "ERROR: Unknown ROM selected. Please restart the Diddy Kong Racing client and select your Diddy Kong Racing US 1.0 ROM."
        )
        raise Exception

    patch_file = open_file(patch_path).read()
    write_file(output_path, bsdiff4.patch(rom, patch_file))


def read_file(file_path: str) -> bytes:
    with open(file_path, "rb") as fi:
        data = fi.read()

    return data


def write_file(file_path: str, data: bytes) -> None:
    with open(file_path, "wb") as fi:
        fi.write(data)


def swap(data: bytes) -> bytes:
    swapped_data = bytearray(b'\0' * len(data))
    for i in range(0, len(data), 2):
        swapped_data[i] = data[i + 1]
        swapped_data[i + 1] = data[i]

    return bytes(swapped_data)


def open_file(resource: str):
    filename = sys.modules[__name__].__file__
    apworld_extension = ".apworld"
    if apworld_extension in filename:
        zip_path = pathlib.Path(filename[:filename.index(apworld_extension) + len(apworld_extension)])
        with zipfile.ZipFile(zip_path) as zf:
            zip_file_path = "diddy_kong_racing/" + resource

            return zf.open(zip_file_path, "r")
    else:
        return open(os.path.join(pathlib.Path(__file__).parent, resource), "rb")
