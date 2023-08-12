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


    def apply_qol_patches(self):
        #Gametickets no longer offered by shops, randomizer does not need them either
        self.rom_data[0xAFED4] = 0x70
        self.rom_data[0xAFED5] = 0x47

        #ship speed increased on overworld
        self.rom_data[0x285A4] = 0xF0

        #Trial Road inventory snapshotting fix
        self.rom_data[0xB10A4] = 0x8C
        self.rom_data[0xB10A5] = 0xE0

        # Remove "Update" option from main menu
        self.rom_data[0x4D62E] = 0x0
        self.rom_data[0x4D62F] = 0xE0

    def write_story_flags(self):
        flags = [0xf22, 0x873]

        if True: #Flagset for skipping many cutscenes. Some cutscenes still play and are tied to map data
            flags = [0xf22, 0x890, 0x891, 0x892, 0x893, 0x894, 0x895, 0x896, 0x848, 0x86c, 0x86d, 0x86e, 0x86f,
            0x916, 0x844, 0x863, 0x864, 0x865, 0x867, 0x872, 0x873, 0x84b, 0x91b, 0x91c, 0x91d, 0x8b2, 0x8b3, 0x8b4,
            0x8a9, 0x8ac, 0x904, 0x971, 0x973, 0x974, 0x924, 0x928, 0x929, 0x92a, 0x880, 0x8f1, 0x8f3, 0x8f5, 0xa6c,
            0x8f6, 0x8fc, 0x8fe, 0x910, 0x911, 0x913, 0x980, 0x981, 0x961, 0x964, 0x965, 0x966, 0x968, 0x962, 0x969,
            0x96a, 0xa8c, 0x88f, 0x8f0, 0x9b1, 0xa78, 0x90c, 0xa2e, 0x9c0, 0x9c1, 0x9c2, 0x908, 0x94F]

        if True: #Ship door unlocked, no need to do gabomba
            flags.extend([0x985])
            if True: #Ship is available from the start
                flags.extend([0x982, 0x983, 0x8de, 0x907])

        addr = 0xF4280
        for idx, flag in enumerate(flags):
            self.rom_data[addr] = flag & 0xFF
            self.rom_data[addr + 1] = flag >> 8
            addr += 2

    def write_to_file(self, out_path):
        with open(out_path, "wb") as rom:
            rom.write(self.rom_data)

    def write_item(self, location, item):
        loc_address = location.addresses[0]

        addr = loc_address
        contents = item.gstla_id
        event_type = self.fix_event_type(location, item)
        event_type = self.show_item_settings(item, event_type, True)

        if addr >= 0xFA0000:
            self.rom_data[addr] = contents & 0xFF
            self.rom_data[addr + 1] = contents >> 8
        else:
            self.rom_data[addr] = event_type & 0xFF
            self.rom_data[addr + 1] = event_type >> 8
            self.rom_data[addr + 6] = contents & 0xFF
            self.rom_data[addr + 7] = contents >> 8

    def write_djinn(self, location, djinn):
        loc_address = location.addresses[0]

        self.rom_data[loc_address] = djinn.gstla_id
        self.rom_data[loc_address + 1] = djinn.element

        for idx, value in enumerate(djinn.stats):
            self.rom_data[djinn.stats_addr + idx] = value

    def fix_event_type(self, location, item):
        event_type = item.event_type
        contents = item.gstla_id
        vanilla_event_type = location.event_type

        if vanilla_event_type < 0x80 and event_type != 0x81:
            event_type = vanilla_event_type

        if event_type != 0x81 and (vanilla_event_type <= 0x80 or vanilla_event_type == 0x83 or vanilla_event_type == 0x84 or vanilla_event_type == 0x85):
            return vanilla_event_type

        if 0xE00 <= contents <= 0xFFF:
            if vanilla_event_type != 0x83:
                return 0x84
            else:
                return 0x83

        if vanilla_event_type == 0x81:
            if 0xE00 <= contents <= 0xFFF:
                return 0x84
            elif event_type != 0x81:
                return 0x80

        return event_type


    def show_item_settings(self, item, event_type, stand_alone_items):
        if stand_alone_items:
            if event_type == 0x80 or event_type == 0x81 or event_type == 0x84:
                return 0x83
        else:
            if event_type == 0x80 or event_type == 0x84:
                if 0xE00 <= item.gstla_id <= 0xFFF:
                    return 0x84
                else:
                    return 0x80

        return event_type


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