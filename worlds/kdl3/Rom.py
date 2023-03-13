import Utils
from typing import Optional
import hashlib
import os
import struct
from worlds.Files import APDeltaPatch

KDL3UHASH = "201e7658f6194458a3869dde36bf8ec2"

animal_friends = {  # individual spawn addresses for each animal friend
    0x770010: [  # Rick
        2960854, 2973713, 3047772, 3109906, 3072123, 2971412, 3164056, 2956485, 3057740, 3315310, 2977125,
        3397478, 2994412, 3604390, 3132841, 3068643, 3038404, 3072609, 3022489, 3015498, 3197815
    ],
    0x770011: [  # Kine
        2979317, 2966655, 3084295, 3072115, 3042583, 3026835, 3207394, 2977117, 3039009, 2994404, 3038412, 3022481,
        3040192, 3198638
    ],
    0x770012: [  # Coo
        2979325, 2966663, 3023113, 3109914, 2954719, 2952942, 2965879, 2977109, 3039001, 3075075, 3604398, 3132833,
        3019973, 3370321, 3070133, 3040200, 3197823
    ],
    0x770013: [  # Nago
        2960846, 3043722, 2973705, 3023105, 2956052, 3042591, 2971396, 2956501, 2976367, 3063027, 2984649, 3132825,
        3058280, 3019981, 3197831
    ],
    0x770014: [  # ChuChu
        3059881, 3043714, 3047780, 3084303, 3042575, 2952934, 2965887, 3044296, 2976359, 2954276, 2984665, 2994420,
        3075091, 3370313, 3026223, 3015506, 3198646
    ],
    0x770015: [  # Pitch
        3059889, 2956044, 3044878, 2971404, 3164064, 2965871, 2956493, 2976375, 3078817, 2984657, 3068635, 3058288,
        3019965, 3370329, 3026215, 3198654
    ],
}


class KDL3DeltaPatch(APDeltaPatch):
    hash = KDL3UHASH
    game = "Kirby's Dream Land 3"
    patch_file_ending = ".apkdl3"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


class RomData:
    def __init__(self, file, name=None):
        self.file = bytes()
        self.read_from_file(file)
        self.name = name

    def read_bytes(self, offset, length):
        return self.file[offset:offset+length]

    def write_byte(self, offset, value):
        self.file[offset] = value

    def write_bytes(self, offset, values):
        self.file[offset:offset+len(values)] = values

    def write_to_file(self, file):
        with open(file, 'wb') as outfile:
            outfile.write(self.file)

    def read_from_file(self, file):
        with open(file, 'rb') as stream:
            self.file = bytearray(stream.read())


def handle_animal_friends(rom):
    for friend in animal_friends:
        for address in animal_friends[friend]:
            rom.write_byte(address, 3)


def patch_rom(multiworld, player, rom, boss_requirements):
    # handle animal friends first
    handle_animal_friends(rom)

    # Copy Ability
    rom.write_bytes(0x399A0, [0xB9, 0xF3, 0x54, 0x48, 0x0A, 0xAA, 0x68, 0xDD, 0x50, 0x7F, 0xEA, 0xEA, 0xF0, 0x03, 0xA9,
    0x00, 0x00, 0x99, 0xA9, 0x54, 0x6B, 0xEA, 0xEA, 0xEA, 0xEA, 0x48, 0x0A, 0xA8, 0x68, 0xD9, 0x50, 0x7F,
    0xEA, 0xF0, 0x03, 0xA9, 0x00, 0x00, 0x9D, 0xA9, 0x54, 0x9D, 0xDF, 0x39, 0x6B, ])

    # Kirby/Gooey Copy Ability
    rom.write_bytes(0xAFC8, [0x22, 0x00, 0x9A, 0x07,
                             0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, ])

    # Animal Copy Ability
    rom.write_bytes(0x507E8, [0x22, 0xB9, 0x99, 0x07, 0xEA, 0xEA, ])

    # Allow Purification
    rom.write_bytes(0x30518, [0x22, 0xA0, 0x99, 0xC3, 0xEA, 0xEA, ])

    # Check Purification
    rom.write_bytes(0x39A00, [0x8A, 0xC9, 0x00, 0x00, 0xF0, 0x03, 0x4A, 0x4A, 0x1A, 0xAA, 0xBF, 0x00, 0xD0, 0x07, 0xCD,
                              0x80, 0x7F, 0x10, 0x02, 0x38, 0x6B, 0x18, 0x6B, ])

    # base patch done, write relevant slot info

    # boss requirements
    rom.write_bytes(0x3D000, struct.pack("HHHHH", boss_requirements[0], boss_requirements[1], boss_requirements[2],
                                         boss_requirements[3], boss_requirements[4]))
    rom.write_byte(0x3D010, multiworld.death_link[player].value)
    rom.write_byte(0x3D012, multiworld.goal[player].value)

    from Main import __version__
    rom.name = bytearray(f'KDL3{__version__.replace(".", "")[0:3]}_{player}_{multiworld.seed:11}\0', 'utf8')[:21]
    rom.name.extend([0] * (21 - len(rom.name)))
    rom.write_bytes(0x7FC0, rom.name)
    rom.write_byte(0x7FD9, multiworld.game_language[player].value)


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes: Optional[bytes] = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name: str = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if KDL3UHASH != basemd5.hexdigest():
            raise Exception("Supplied Base Rom does not match known MD5 for US release. "
                            "Get the correct game and version, then dump it")
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: Utils.OptionsType = Utils.get_options()
    if not file_name:
        file_name = options["kdl3_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
