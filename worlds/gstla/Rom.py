from __future__ import annotations
from typing import List, Optional

import settings
from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin

import Utils
import os
import hashlib

SCRIPT_DIR = os.path.join(os.path.dirname(__file__))

CHECKSUM_GSTLA = "8efe8b2aaed97149e897570cd123ff6e"

class GSTLADeltaPatch(APProcedurePatch, APTokenMixin):
    hash = CHECKSUM_GSTLA
    game = "Golden Sun The Lost Age"
    patch_file_ending = ".apgstla"
    result_file_ending = ".gba"
    procedure = [
        ("apply_gstla_rando", ["ap_settings.gstlarando"]),
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def add_settings(self, data: bytes, debug_data: Optional[bytes]):
        self.files["ap_settings.gstlarando"] = data
        if debug_data:
            self.files["ap_settings.debug.txt"] = debug_data

    def apply_ups(self, rom: bytes, patch_data: List[int]) -> bytes:
        """
        Patches a rom from a GBA UPS File.  Shamelessly modeled after the GS TLA Rando code
        """
        target = bytearray(rom)
        data = patch_data[4:-12]
        patch_offset = 0

        def read_offset() -> int:
            nonlocal patch_offset
            local_offset = 0
            shift = 1
            while True:
                byte = data[patch_offset]
                patch_offset += 1
                local_offset += (byte & 0x7F) * shift
                if (byte & 0x80) > 0:
                    break
                shift <<= 7
                local_offset += shift

            return local_offset

        source_len = read_offset()
        target_len = read_offset()
        if target_len > source_len:
            target.extend(bytearray(target_len - source_len))

        byte_offset = 0
        data_len = len(data)
        while patch_offset < data_len:
            offset = read_offset()
            byte_offset += offset
            while True:
                datum = data[patch_offset]
                patch_offset += 1
                target[byte_offset] ^= datum
                byte_offset += 1
                if datum == 0:
                    break
        return bytes(target)


class GSTLAPatchExtension(APPatchExtension):
    game = "Golden Sun The Lost Age"

    @staticmethod
    def apply_gstla_rando(caller: GSTLADeltaPatch, rom: bytes, patch_file: str) -> bytes:
        import requests
        ap_settings = caller.get_file(patch_file)
        # response = requests.post("http://localhost:3000/import_ap_ajax",
        response = requests.post("https://gs2randomiser.com/import_ap_ajax",
                                 data=ap_settings,
                                 allow_redirects=False,
                                 headers={
                                     # Rando expects XHR
                                     "X-Requested-With": "XMLHttpRequest",
                                     "Content-Type": "application/octet-stream"
                                 })
        if response.status_code != 200:
            raise Exception(f"Failed to patch ROM using GS TLA Randomizer Website; http code: {response.status_code}")
        data = response.json()
        if not data['success']:
            raise Exception(f"Failed to patch ROM using GS TLA Randomizer Website; response: {data}")
        return caller.apply_ups(rom, data['patch'])

def get_base_rom_path(file_name: str = "") -> str:
    options = settings.get_settings()
    if not file_name:
        gstla_options = options.get("gstla_options", None)
        if gstla_options is None:
            file_name = "Golden Sun - The Lost Age (UE) [!].gba"
        else:
            file_name = gstla_options["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_name, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        hexdigest = basemd5.hexdigest()
        if CHECKSUM_GSTLA != hexdigest:
            raise Exception('Supplied Base Rom does not match UE GBA Golden Sun TLA Version.'
                            'Please provide the correct ROM version')

        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes
