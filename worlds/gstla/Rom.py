from BaseClasses import ItemClassification
from Patch import APDeltaPatch

import Utils
import os
import hashlib
import bsdiff4
from .Names.ItemName import ItemName
#from .lz10 import gba_decompress, gba_compress

#from .BN3RomUtils import ArchiveToReferences, read_u16_le, read_u32_le, int16_to_byte_list_le, int32_to_byte_list_le,\
   # generate_progressive_undernet, ArchiveToSizeComp, ArchiveToSizeUncomp, generate_item_message, \
    #generate_external_item_message, generate_text_bytes

#from .Items import ItemType

CHECKSUM_BLUE = "8efe8b2aaed97149e897570cd123ff6e"


class LocalRom:
    def __init__(self, file, name=None):
        self.name = name
        self.changed_archives = {}

        self.rom_data = bytearray(get_patched_rom_bytes(file))

    def write_to_file(self, out_path):
        with open(out_path, "wb") as rom:
            rom.write(self.rom_data)

    def write_item(self, location, item):
        loc_address = location.addresses[0]

        addr = loc_address
        contents = 0

        match item.itemName:
            case ItemName.Herb:
                contents = 180
            case ItemName.Smoke_Bomb:
                contents = 226
            case ItemName.Sleep_Bomb:
                contents = 227
            case ItemName.Psy_Crystal:
                contents = 186
            case ItemName.Sea_Gods_Tear:
                contents = 458
            case ItemName.Mysterious_Card:
                contents = 443
            case ItemName.Lash_Pebble:
                contents = 198
            case ItemName.Nut:
                contents = 181
            case ItemName.Elixir:
                contents = 188
            case ItemName.Mint:
                contents = 195
            case ItemName.Themis_Axe:
                contents = 301
            case ItemName.Full_Metal_Vest:
                contents = 340
            case ItemName.Pound_Cube:
                contents = 199
            case ItemName.Antidote:
                contents = 187
            case ItemName.Cyclone_Chip:
                contents = 210
            case ItemName.Nurses_Cap:
                contents = 383
            case ItemName.Ruin_Key:
                contents = 459
            case ItemName.Tremor_Bit:
                contents = 208
            case ItemName.Apple:
                contents = 193
            case ItemName.Lucky_Medal:
                contents = 229
            case ItemName.Mist_Potion:
                contents = 190

        if addr >= 0xFA0000:
            self.rom_data[addr] = contents & 0xFF
            self.rom_data[addr + 1] = contents >> 8
        else:
            #self.rom_data[addr] = event_type & 0xFF
            #self.rom_data[addr + 1] = event_type >> 8
            self.rom_data[addr + 6] = contents & 0xFF
            self.rom_data[addr + 7] = contents >> 8

    def write_djinn(self, location, djinn):
        loc_address = location.addresses[0]

        match djinn.itemName:
            case ItemName.Echo:
                self.rom_data[loc_address] = 7
                self.rom_data[loc_address + 1] = 0
                pass
            case ItemName.Fog:
                self.rom_data[loc_address] = 7
                self.rom_data[loc_address + 1] = 1

                pass
            case ItemName.Iron:
                self.rom_data[loc_address] = 8
                self.rom_data[loc_address + 1] = 0

                pass
            case ItemName.Cannon:
                self.rom_data[loc_address] = 7
                self.rom_data[loc_address + 1] = 2

                pass
            case ItemName.Breath:
                self.rom_data[loc_address] = 7
                self.rom_data[loc_address + 1] = 3


class GSTLADeltaPatch(APDeltaPatch):
    hash = CHECKSUM_BLUE
    game = "Golden Sun: The Lost Age"
    patch_file_ending = ".apgstla"
    result_file_ending = ".gba"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        gstla_options = options.get("gstla_options", None)
        if gstla_options is None:
            file_name = "Golden Sun - The Lost Age (UE) [!].gba"
        else:
            file_name = gstla_options["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.local_path(file_name)
    return file_name


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_name, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        hexdigest = basemd5.hexdigest()
        if CHECKSUM_BLUE != hexdigest:
            raise Exception('Supplied Base Rom does not match US GBA Blue Version.'
                            'Please provide the correct ROM version')

        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_patched_rom_bytes(file_name: str = "") -> bytes:
    """
    Gets the patched ROM data generated from applying the ap-patch diff file to the provided ROM.
    Diff patch generated by https://github.com/digiholic/bn3-ap-patch
    Which should contain all changed text banks and assembly code
    """
    import pkgutil
    base_rom_bytes = get_base_rom_bytes(file_name)
    patch_bytes = pkgutil.get_data(__name__, "patches/gstla_base_patch.bsdiff")
    patched_rom_bytes = bsdiff4.patch(base_rom_bytes, patch_bytes)
    return patched_rom_bytes