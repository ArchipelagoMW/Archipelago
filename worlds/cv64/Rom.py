import Utils
import hashlib
import os
# import math

# from BaseClasses import Location
from Patch import read_rom, APDeltaPatch
from .Names import PatchName

USHASH = '1cc5cf3b4d29d8c3ade957648b529dc1'
ROM_PLAYER_LIMIT = 65535


rom_loc_offsets = {
    0xC64001: 0x10C67B,  # Forest of Silence
    0xC64002: 0x10C71B,
    0xC64003: 0x10C6BB,
    0xC64004: 0x10C68B,
    0xC64005: 0x10C693,
    0xC64006: 0x10C6C3,
    0xC64007: 0x10C6E3,
    0xC64008: 0x10C6CB,
    0xC64009: 0x10C683,
    0xC6400A: 0x10C743,
    0xC6400B: 0x10C6A3,
    0xC6400C: 0x10C69B,
    0xC6400D: 0x10C6D3,
    0xC6400E: 0x10C6AB,
    0xC6400F: 0x10C76B,
    0xC64010: 0x10C75B,
    0xC64011: 0x10C713,
    0xC64012: 0x10C733,
    0xC64013: 0x10C6B3,
    0xC64014: 0x10C72B,

    0xC64015: 0x10C7F7,  # Castle Wall
    0xC64016: 0x10C807,
    0xC64017: 0x10C7FF,
    0xC64018: 0x10C817,
    0xC64019: 0x10C80F,
    0xC6401A: 0x10C7E7,
    0xC6401B: 0x10C7DF,
    0xC6401C: 0x10C7EF,

    0xC6401D: 0x10C87F,  # Villa
    0xC6401E: 0x10C887,
    0xC6401F: 0x10C89F,
    0xC64020: 0x10C8A7,
    0xC64021: 0x10C897,
    0xC64022: 0x10C8AF,
    0xC64023: 0x10C8B7,
    0xC64024: 0x10C8C7,
    0xC64025: 0x10C8CF,
    0xC64026: 0x10C8D7,
    0xC64027: 0x10C8DF,
    0xC64028: 0x10C8E7,
    0xC64029: 0x10C8EF,
    0xC6402A: 0x10C927,
    0xC6402B: 0x10C90F,
    0xC6402C: 0x10C917,
    0xC6402D: 0x10C91F,
    0xC6402E: 0x106A07,  # Vincent
    0xC6402F: 0x10C967,
    0xC64030: 0x10C947,
    0xC64031: 0x10C9A7,
    0xC64032: 0x10C96F,
    0xC64033: 0x10C977,
    0xC64034: 0x10C95F,
    0xC64035: 0x10C97F,
    0xC64036: 0x10C94F,
    0xC64037: 0x10C957,
    0xC64038: 0x10C92F,
    0xC64039: 0x10C93F,
    0xC6403A: 0x10C937,
    0xC6403B: 0x10CF4B,
    0xC6403C: 0x10CF63,
    0xC6403D: 0x10CF6B,
    0xC6403E: 0x10CF5B,
    0xC6403F: 0x10C8BF,
    0xC64040: 0x10CF53,

    0xC64041: 0x10C9AF,  # Tunnel
    0xC64042: 0x10C9B7,
    0xC64043: 0x10CA9F,
    0xC64044: 0x10C9DF,
    0xC64045: 0x10C9E7,
    0xC64046: 0x10C9D7,
    0xC64047: 0x10C9CF,
    0xC64048: 0x10CA27,
    0xC64049: 0x10CAA7,
    0xC6404A: 0x10CAB7,
    0xC6404B: 0x10C9C7,
    0xC6404C: 0x10CA2F,
    0xC6404D: 0x10C9F7,
    0xC6404E: 0x10CA37,
    0xC6404F: 0x10C9FF,
    0xC64050: 0x10CA07,
    0xC64051: 0x10CA0F,
    0xC64052: 0x10CA3F,
    0xC64053: 0x10CA17,
    0xC64054: 0x10CA47,
    0xC64055: 0x10CA4F,
    0xC64056: 0x10CAAF,

    0xC64057: 0x10CB03,  # Underground Waterway
    0xC64058: 0x10CAF3,
    0xC64059: 0x10CAFB,
    0xC6405A: 0x10CB23,
    0xC6405B: 0x10CB0B,
    0xC6405C: 0x10CB13,
    0xC6405D: 0x10CB33,
    0xC6405E: 0x10CB2B,

    0xC6405F: 0x10CB67,  # Castle Center
    0xC64060: 0x10CBD7,
    0xC64061: 0x10CB6F,
    0xC64062: 0x10CB77,
    0xC64063: 0x10CBA7,
    0xC64064: 0x10CB7F,
    0xC64065: 0x10CBAF,
    0xC64066: 0x10CBB7,
    0xC64067: 0x10CB87,
    0xC64068: 0x10CBBF,
    0xC64069: 0x10CB8F,
    0xC6406A: 0x1069E7,  # Mandragora shelf
    0xC6406B: 0x10CBF7,
    0xC6406C: 0x10CC17,
    0xC6406D: 0x10CC07,
    0xC6406E: 0x10CBFF,
    0xC6406F: 0x10CC33,
    0xC64070: 0x10CC3B,
    0xC64071: 0x10CC43,
    0xC64072: 0x10CC4B,
    0xC64073: 0x10CC53,
    0xC64074: 0x10CC8F,
    0xC64075: 0x10CC87,
    0xC64076: 0x10CC97,
    0xC64077: 0x10CC77,
    0xC64078: 0x10CC7F,
    0xC64079: 0x10CC9F,
    0xC6407A: 0x10CCA7,
    0xC6407B: 0x10CCAF,
    0xC6407C: 0x10CCB7,
    0xC6407D: 0x106A13,  # Blue lizard man
    0xC6407E: 0x1069C7,  # Nitro shelf
    0xC6407F: 0x10CCD7,
    0xC64080: 0x10CCDF,
    0xC64081: 0x10CCE7,
    0xC64082: 0x10CCFF,
    0xC64083: 0x10CD07,

    0xC64084: 0x10CE73,  # Duel Tower
    0xC64085: 0x10CE7B,
    0xC64086: 0x10CE8B,
    0xC64087: 0x10CE93,

    0xC64088: 0x10CD1F,  # Tower of Execution
    0xC64089: 0x10CD27,
    0xC6408A: 0x10CD17,
    0xC6408B: 0x10CD47,
    0xC6408C: 0x10CD4F,
    0xC6408D: 0x10CD37,

    0xC6408E: 0x10CE0B,  # Tower of Science
    0xC6408F: 0x10CDF3,
    0xC64090: 0x10CE13,
    0xC64091: 0x10CDFB,
    0xC64092: 0x10CE3B,
    0xC64093: 0x10CE33,
    0xC64094: 0x10CE03,
    0xC64095: 0x10CE1B,
    0xC64096: 0x10CE23,

    0xC64097: 0x10CDB3,  # Tower of Sorcery
    0xC64098: 0x10CDBB,
    0xC64099: 0x10CDD3,
    0xC6409A: 0x10CDDB,
    0xC6409B: 0x10CDC3,
    0xC6409C: 0x10CDCB,
    0xC6409D: 0x10CDE3,

    0xC6409E: 0x10CF7B,  # Room of Clocks
    0xC6409F: 0x10CFB3,
    0xC640A0: 0x10CFBB,

    0xC640A1: 0x10CEB3,  # Clock Tower
    0xC640A2: 0x10CEC3,
    0xC640A3: 0x10CEBB,

    0xC640A4: 0x10CE9B,  # Castle Keep
    0xC640A5: 0x10CEA3,
}

rom_item_bytes = {
    "White jewel": 0x01,
    "Red jewel(S)": 0x02,
    "Red jewel(L)": 0x03,
    "Special1": 0x04,
    "Special2": 0x05,
    "Roast chicken": 0x06,
    "Roast beef": 0x07,
    "Healing kit": 0x08,
    "Purifying": 0x09,
    "Cure ampoule": 0x0A,
    "pot-pourri": 0x0B,
    "PowerUp": 0x0C,
    "Holy water": 0x0D,
    "Cross": 0x0E,
    "Axe": 0x0F,
    "Knife": 0x10,
    "Wooden stake": 0x11,
    "Rose": 0x12,
    "The contract": 0x13,
    "engagement ring": 0x14,
    "Magical Nitro": 0x15,
    "Mandragora": 0x16,
    "Sun card": 0x17,
    "Moon card": 0x18,
    "Incandescent gaze": 0x19,
    "500 GOLD": 0x1A,
    "300 GOLD": 0x1B,
    "100 GOLD": 0x1C,
    "Archives key": 0x1D,
    "Left Tower Key": 0x1E,
    "Storeroom Key": 0x1F,
    "Garden Key": 0x20,
    "Copper Key": 0x21,
    "Chamber Key": 0x22,
    "Execution Key": 0x23,
    "Science Key1": 0x24,
    "Science Key2": 0x25,
    "Science Key3": 0x26,
    "Clocktower Key1": 0x27,
    "Clocktower Key2": 0x28,
    "Clocktower Key3": 0x29,
}


class LocalRom(object):

    def __init__(self, file, patch=True, vanilla_rom=None, name=None, hash=None):
        self.name = name
        self.hash = hash
        self.orig_buffer = None

        with open(file, 'rb') as stream:
            self.buffer = read_rom(stream)
        # if patch:
        #    self.patch_rom()
        #    self.orig_buffer = self.buffer.copy()
        # if vanilla_rom:
        #    with open(vanillaRom, 'rb') as vanillaStream:
        #        self.orig_buffer = read_rom(vanillaStream)
        
    def read_bit(self, address: int, bit_number: int) -> bool:
        bitflag = (1 << bit_number)
        return (self.buffer[address] & bitflag) != 0

    def read_byte(self, address: int) -> int:
        return self.buffer[address]

    def read_bytes(self, startaddress: int, length: int) -> bytes:
        return self.buffer[startaddress:startaddress + length]

    def write_byte(self, address: int, value: int):
        self.buffer[address] = value

    def write_bytes(self, startaddress: int, values):
        self.buffer[startaddress:startaddress + len(values)] = values

    def write_to_file(self, file):
        with open(file, 'wb') as outfile:
            outfile.write(self.buffer)

    def read_from_file(self, file):
        with open(file, 'rb') as stream:
            self.buffer = bytearray(stream.read())


def patch_rom(world, rom, player, offsets_to_ids):
    # local_random = world.slot_seeds[player]

    # NOP out the CRC BNEs
    rom.write_bytes(0x66C, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0x678, [0x00, 0x00, 0x00, 0x00])

    # Disable Easy Mode cutoff point
    rom.write_bytes(0xD9E18, [0x24, 0x0D, 0x00, 0x00])

    # Fix both elevator bridges for both characters
    rom.write_bytes(0x6CEAA0, [0x24, 0x0B, 0x00, 0x01])
    rom.write_bytes(0x6CEAA4, [0x24, 0x0D, 0x00, 0x01])

    # Enable being able to carry multiple Special jewels
    rom.write_bytes(0xBF1F4, [0x3C, 0x03, 0x80, 0x39])  # LUI V1, 0x8039
    # Special1
    rom.write_bytes(0xBF210, [0x80, 0x65, 0x9C, 0x4B])  # LB A1, 0x9C4B (V1)
    rom.write_bytes(0xBF214, [0x24, 0xA5, 0x00, 0x01])  # ADDIU A1, A1, 0x0001
    rom.write_bytes(0xBF21C, [0xA0, 0x65, 0x9C, 0x4B])  # SB A1, 0x9C4B (V1)
    # Special2
    rom.write_bytes(0xBF230, [0x80, 0x65, 0x9C, 0x4C])  # LB A1, 0x9C4C (V1)
    rom.write_bytes(0xBF234, [0x24, 0xA5, 0x00, 0x01])  # ADDIU A1, A1, 0x0001
    rom.write_bytes(0xbf23C, [0xA0, 0x65, 0x9C, 0x4C])  # SB A1, 0x9C4C (V1)

    # Disable vampire Vincent cutscene
    if world.fight_vincent[player] == "never":
        rom.write_bytes(0xAACC0, [0x24, 0x01, 0x00, 0x01])

    # Increase item capacity to 100
    if world.increase_item_limit[player] == "true":
        rom.write_byte(0xBF30B, 0x64)

    # Custom warp menu, remote item rewarding, and DeathLink code injection
    rom.write_bytes(0x19B98, [0x08, 0x06, 0x0D, 0x8B])  # J 0x8018362C
    rom.write_bytes(0x10681C, PatchName.remote_item_and_warp)

    # NPC item textbox hack hook
    rom.write_bytes(0xBF1DC, [0x08, 0x06, 0x0D, 0xEC])  # J 0x8013BFEC
    rom.write_bytes(0xBF1E0, [0x27, 0xBD, 0xFF, 0xE0])  # ADDIU SP, SP, -0x20

    # Subweapon check function hook
    rom.write_bytes(0xBF32C, [0x00, 0x00, 0x00, 0x00])  # NOP
    rom.write_bytes(0xBF330, [0x08, 0x06, 0x0D, 0xE5])  # J	0x80183794

    # Custom warp menu code
    rom.write_bytes(0xADD68, [0x0C, 0x04, 0xAB, 0x12])  # JAL 0x8012AC48
    rom.write_bytes(0xADE28, PatchName.stage_select_overwrite)
    rom.write_byte(0xADD6F, world.special2s_per_warp[player])

    # Fix locked doors to check the key counters instead of their vanilla key locations' flags
    # Pickup flag check modifications:
    rom.write_bytes(0x10B2D8, [0x00, 0x00, 0x00, 0x02])  # Left Tower Door
    rom.write_bytes(0x10B2F0, [0x00, 0x00, 0x00, 0x03])  # Storeroom Door
    rom.write_bytes(0x10B2FC, [0x00, 0x00, 0x00, 0x01])  # Archives Door
    rom.write_bytes(0x10B314, [0x00, 0x00, 0x00, 0x04])  # Maze Gate
    rom.write_bytes(0x10B350, [0x00, 0x00, 0x00, 0x05])  # Copper Door
    rom.write_bytes(0x10B3A4, [0x00, 0x00, 0x00, 0x06])  # Torture Chamber Door
    rom.write_bytes(0x10B3B0, [0x00, 0x00, 0x00, 0x07])  # ToE Gate
    rom.write_bytes(0x10B3BC, [0x00, 0x00, 0x00, 0x08])  # Science Door1
    rom.write_bytes(0x10B3C8, [0x00, 0x00, 0x00, 0x09])  # Science Door2
    rom.write_bytes(0x10B3D4, [0x00, 0x00, 0x00, 0x0A])  # Science Door3
    rom.write_bytes(0x6F0094, [0x00, 0x00, 0x00, 0x0B])  # CT Door 1
    rom.write_bytes(0x6F00A4, [0x00, 0x00, 0x00, 0x0C])  # CT Door 2
    rom.write_bytes(0x6F00B4, [0x00, 0x00, 0x00, 0x0D])  # CT Door 3
    # Item counter decrement check modifications:
    rom.write_bytes(0xEDA84, [0x00, 0x00, 0x00, 0x01])   # Archives Door
    rom.write_bytes(0xEDA8C, [0x00, 0x00, 0x00, 0x02])   # Left Tower Door
    rom.write_bytes(0xEDA94, [0x00, 0x00, 0x00, 0x03])   # Storeroom Door
    rom.write_bytes(0xEDA9C, [0x00, 0x00, 0x00, 0x04])   # Maze Gate
    rom.write_bytes(0xEDAA4, [0x00, 0x00, 0x00, 0x05])   # Copper Door
    rom.write_bytes(0xEDAAC, [0x00, 0x00, 0x00, 0x06])   # Torture Chamber Door
    rom.write_bytes(0xEDAB4, [0x00, 0x00, 0x00, 0x07])   # ToE Gate
    rom.write_bytes(0xEDABC, [0x00, 0x00, 0x00, 0x08])   # Science Door1
    rom.write_bytes(0xEDAC4, [0x00, 0x00, 0x00, 0x09])   # Science Door2
    rom.write_bytes(0xEDACC, [0x00, 0x00, 0x00, 0x0A])   # Science Door3
    rom.write_bytes(0xEDAD4, [0x00, 0x00, 0x00, 0x0B])   # CT Door 1
    rom.write_bytes(0xEDADC, [0x00, 0x00, 0x00, 0x0C])   # CT Door 2
    rom.write_bytes(0xEDAE4, [0x00, 0x00, 0x00, 0x0D])   # CT Door 3

    rom.write_bytes(0x10AB2C, [0x80, 0x15, 0xFB, 0xD4])  # Maze Gate check code pointer adjustment
    rom.write_bytes(0xE2E14, PatchName.normal_door_hook)
    rom.write_bytes(0x106780, PatchName.normal_door_code)
    rom.write_bytes(0x6EF298, PatchName.ct_door_hook)
    rom.write_bytes(0x1067B0, PatchName.ct_door_code)

    # Nitro and Mandragora patches
    # Prevent "can explode" flag from setting
    rom.write_bytes(0xB5D7AA, [0x00, 0x00, 0x00, 0x00])
    # Prevent tossing Nitro in Hazardous Waste Disposers
    # rom.write_bytes(0xBF648, [0x24, 0x02, 0x00, 0x01])  # ADDIU	V0, R0, 0x0001
    # Prevent setting the "can explode" bitflag

    # Write the new item bytes
    for offset, item_id in offsets_to_ids.items():
        rom.write_byte(offset, item_id)


class CV64DeltaPatch(APDeltaPatch):
    hash = USHASH
    game = "Castlevania 64"
    patch_file_ending = ".apcv64"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(read_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if USHASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for US(1.0) release. '
                            'Get the correct game and version, then dump it.')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["cv64_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.local_path(file_name)
    return file_name
