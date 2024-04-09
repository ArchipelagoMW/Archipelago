
import Utils
import logging
import json

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from typing import Dict, Optional, TYPE_CHECKING

import hashlib
import os
import pkgutil

from .data import patches
from .locations import get_location_info, get_all_location_names
from settings import get_settings

if TYPE_CHECKING:
    from . import CVCotMWorld

CVCOTM_CT_US_HASH = "50a1089600603a94e15ecf287f8d5a1f"  # GBA Cartridge version
CVCOTM_AC_US_HASH = "87a1bd6577b6702f97a60fc55772ad74"  # Castlevania Advance Collection version

AREA_LIST_START = 0xD9A40


class RomData:
    def __init__(self, file: bytes, name: Optional[str] = None) -> None:
        self.file = bytearray(file)
        self.name = name

    def read_byte(self, offset: int) -> int:
        return self.file[offset]

    def read_bytes(self, offset: int, length: int) -> bytes:
        return self.file[offset:offset + length]

    def write_byte(self, offset: int, value: int) -> None:
        self.file[offset] = value

    def write_bytes(self, offset: int, values) -> None:
        self.file[offset:offset + len(values)] = values

    def get_bytes(self) -> bytes:
        return bytes(self.file)

    def apply_ips(self, filename: str) -> None:
        ips_file = bytearray(pkgutil.get_data(__name__, "data/ips/" + filename))

        # Verify that the IPS patch is, indeed, an IPS patch.
        if ips_file[0:5].decode("ascii") != "PATCH":
            logging.error(filename + " does not appear to be an IPS patch...")
            return

        file_pos = 5
        while True:
            # Get the ROM offset bytes of the current record.
            rom_offset = int.from_bytes(ips_file[file_pos:file_pos + 3], "big")

            # If we've hit the "EOF" codeword (aka 0x454F46), stop iterating because we've hit the end of the file.
            if rom_offset == 0x454F46:
                return

            # Get the size bytes of the current record.
            bytes_size = int.from_bytes(ips_file[file_pos + 3:file_pos + 5], "big")

            if bytes_size != 0:
                # Write the data to the ROM.
                self.write_bytes(rom_offset, ips_file[file_pos + 5:file_pos + 5 + bytes_size])

                # Increase our position in the IPS patch to the start of the next record.
                file_pos += 5 + bytes_size
            else:
                # If the size is 0, we are looking at an RLE record.
                # Get the size of the RLE.
                rle_size = int.from_bytes(ips_file[file_pos + 5:file_pos + 7], "big")

                # Get the byte to be written over and over.
                rle_byte = ips_file[file_pos + 7:file_pos + 8]

                # Write the RLE byte to the ROM the RLE size times over.
                self.write_bytes(rom_offset, [rle_byte for _ in range(rle_size)])

                # Increase our position in the IPS patch to the start of the next record.
                file_pos += 8


class CVCotMPatchExtensions(APPatchExtension):
    game = "Castlevania - Circle of the Moon"

    @staticmethod
    def apply_ips_patches(caller: APProcedurePatch, rom: bytes, options_file: str) -> bytes:
        rom_data = RomData(rom)
        options = json.loads(caller.get_file(options_file).decode("utf-8"))

        # These patches get applied regardless of settings.
        rom_data.apply_ips("AutoDashBoots.ips")
        rom_data.apply_ips("CardUp_v3_Custom.ips")
        rom_data.apply_ips("NoDSSDrops.ips")
        rom_data.apply_ips("CardCombosRevealed.ips")
        rom_data.apply_ips("CandleFix.ips")
        rom_data.apply_ips("SoftlockBlockFix.ips")
        rom_data.apply_ips("MPComboFix.ips")
        rom_data.apply_ips("GameClearBypass.ips")
        rom_data.apply_ips("MapEdits.ips")
        rom_data.apply_ips("DemoForceFirst.ips")
        rom_data.apply_ips("AllowAlwaysDrop.ips")
        rom_data.apply_ips("SeedDisplayAPEdition.ips")

        # Write the 20-digit seed name.
        curr_seed_addr = 0x672152
        while options["seed_name"]:
            seed_digit = (options["seed_name"] % 10) + 0x511C
            rom_data.write_bytes(curr_seed_addr, int.to_bytes(seed_digit, 2, "little"))
            curr_seed_addr -= 2
            options["seed_name"] //= 10

        if options["auto_run"]:
            rom_data.apply_ips("PermanentDash.ips")

        if options["dss_patch"]:
            rom_data.apply_ips("DSSGlitchFix.ips")

        if options["break_iron_maidens"]:
            rom_data.apply_ips("BrokenMaidens.ips")

        if options["required_last_keys"] != 1:
            rom_data.apply_ips("MultiLastKey.ips")
            rom_data.write_byte(0x96C1E, options["required_last_keys"])
            rom_data.write_byte(0xDFB4, options["required_last_keys"])
            rom_data.write_byte(0xCB84, options["required_last_keys"])

        if options["buff_ranged_familiars"]:
            rom_data.apply_ips("BuffFamiliars.ips")

        if options["buff_sub_weapons"]:
            rom_data.apply_ips("BuffSubweapons.ips")

        if options["buff_shooter_strength"]:
            rom_data.apply_ips("ShooterStrength.ips")

        if options["always_allow_speed_dash"]:
            rom_data.apply_ips("AllowSpeedDash.ips")

        if options["countdown"]:
            rom_data.apply_ips("Countdown.ips")

        if options["disable_battle_arena_mp_drain"]:
            rom_data.apply_ips("NoMPDrain.ips")

        # Write the textbox messaging system code
        rom_data.write_bytes(0x6B1F8, [0x00, 0x48, 0x87, 0x46, 0x20, 0xFF, 0x7F, 0x08])
        rom_data.write_bytes(0x7FFF20, patches.remote_textbox_shower)

        return rom_data.get_bytes()

    @staticmethod
    def fix_item_graphics(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom_data = RomData(rom)
        for loc in get_all_location_names():
            offset = get_location_info(loc, "offset")
            if offset is None:
                continue
            item_category = rom_data.read_byte(offset)

            # Magic Items in Max Up locations should have their Y position decreased by 8.
            if item_category == 0xE8 and get_location_info(loc, "type") not in ["magic item", "boss"]:
                y_pos = int.from_bytes(rom_data.read_bytes(offset-2, 2), "little")
                y_pos -= 8
                rom_data.write_bytes(offset-2, int.to_bytes(y_pos, 2, "little"))

                # Fix the Magic Item's graphics if it's in a room it can be fixed in (the room graphics value is 0xFFFF,
                # meaning it's not loading any additional graphics)
                gfx_offset = get_location_info(loc, "room gfx")
                if gfx_offset is not None:
                    if rom_data.read_bytes(gfx_offset, 2) == b"\xFF\xFF":
                        rom_data.write_bytes(gfx_offset, b"\x0A\x00")

            # Max Ups in Magic Item locations should have their Y position increased by 8.
            if item_category != 0xE8 and get_location_info(loc, "type") in ["magic item", "boss"]:
                y_pos = int.from_bytes(rom_data.read_bytes(offset - 2, 2), "little")
                y_pos += 8
                rom_data.write_bytes(offset - 2, int.to_bytes(y_pos, 2, "little"))

        return rom_data.get_bytes()


class CVCotMProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [CVCOTM_CT_US_HASH, CVCOTM_AC_US_HASH]
    patch_file_ending: str = ".apcvcotm"
    result_file_ending: str = ".gba"

    game = "Castlevania - Circle of the Moon"

    procedure = [
        ("apply_tokens", ["token_data.bin"]),
        ("apply_ips_patches", ["options.json"]),
        ("fix_item_graphics", [])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def patch_rom(world: "CVCotMWorld", patch: CVCotMProcedurePatch, offset_data: Dict[int, bytes]) -> None:

    # Write all the new item values
    for offset, data in offset_data.items():
        patch.write_token(APTokenTypes.WRITE, offset, data)

    # Write the secondary name the client will use to distinguish a vanilla ROM from an AP one.
    patch.write_token(APTokenTypes.WRITE, 0x7FFF00, "ARCHIPELAG01".encode("utf-8"))
    # Write the slot authentication
    patch.write_token(APTokenTypes.WRITE, 0x7FFF10, bytes(world.auth))

    patch.write_file("token_data.bin", patch.get_token_binary())

    # Write these slot options to a JSON.
    options_dict = {
        "auto_run": world.options.auto_run.value,
        "dss_patch": world.options.dss_patch.value,
        "break_iron_maidens": world.options.break_iron_maidens.value,
        "required_last_keys": world.required_last_keys,
        "buff_ranged_familiars": world.options.buff_ranged_familiars.value,
        "buff_sub_weapons": world.options.buff_sub_weapons.value,
        "buff_shooter_strength": world.options.buff_shooter_strength.value,
        "always_allow_speed_dash": world.options.always_allow_speed_dash.value,
        "countdown": world.options.countdown.value,
        "disable_battle_arena_mp_drain": world.options.disable_battle_arena_mp_drain.value,
        "seed_name": int(world.multiworld.seed_name)
    }

    patch.write_file("options.json", json.dumps(options_dict).encode('utf-8'))


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_name, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in [CVCOTM_CT_US_HASH, CVCOTM_AC_US_HASH]:
            raise Exception("Supplied Base ROM does not match known MD5s for Castlevania: Circle of the Moon USA."
                            "Get the correct cartridge, or the Castlevania Advance Collection, then extract it.")
        setattr(get_base_rom_bytes, "base_rom_bytes", base_rom_bytes)
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    if not file_name:
        file_name = get_settings()["cvcotm_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
