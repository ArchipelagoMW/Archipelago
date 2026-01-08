import hashlib
import os
import Utils
import typing
import struct
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from typing import TYPE_CHECKING, Optional
from logging import warning
from .game_data import world_version

if TYPE_CHECKING:
    from . import Z2World

md5 = "88c0493fb1146834836c0ff4f3e06e45"


class LocalRom(object):

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


def patch_rom(world, rom, player: int):

    if world.options.random_tunic_color:
        shield_color = world.random.randint(0x10, 0x3E)
        tunic_color = world.random.randint(0x10, 0x3E)

        rom.write_bytes(0x00E9E, bytearray([shield_color])) #Shield palette
        rom.write_bytes(0x040B1, bytearray([tunic_color])) # Normal palette
        rom.write_bytes(0x040C1, bytearray([tunic_color])) # Normal palette
        rom.write_bytes(0x040D1, bytearray([tunic_color])) # Normal palette
        rom.write_bytes(0x040D1, bytearray([tunic_color])) # Normal palette
        rom.write_bytes(0x17C1B, bytearray([tunic_color])) # File select
        rom.write_bytes(0x1C466, bytearray([tunic_color])) # Loading
        rom.write_bytes(0x1C47E, bytearray([tunic_color])) # Map palette
        rom.write_bytes(0xC0B1, bytearray([tunic_color]))
        rom.write_bytes(0xC0C1, bytearray([tunic_color]))
        rom.write_bytes(0xC0D1, bytearray([tunic_color]))
        rom.write_bytes(0xC0E1, bytearray([tunic_color]))
        rom.write_bytes(0xC0F1, bytearray([tunic_color]))
        rom.write_bytes(0x100B1, bytearray([tunic_color]))
        rom.write_bytes(0x100C1, bytearray([tunic_color]))
        rom.write_bytes(0x100D1, bytearray([tunic_color]))
        rom.write_bytes(0x100E1, bytearray([tunic_color]))
        rom.write_bytes(0x80B1, bytearray([tunic_color]))
        rom.write_bytes(0x80C1, bytearray([tunic_color]))
        rom.write_bytes(0x80D1, bytearray([tunic_color]))
        rom.write_bytes(0x80E1, bytearray([tunic_color]))

    if world.options.random_palace_graphics:
        for i in range(6):
            base_color = world.random.randint(0x00, 0x0C)
            secondary_color = base_color + 0x20
            if base_color >= 0x10:
                tertiary_color = base_color - 0x10
            else:
                tertiary_color = 0x0F
            rom.write_bytes(0x10486 + (16 * i), bytearray([base_color, secondary_color]))
            rom.write_bytes(0x13F16 + (16 * i), bytearray([base_color, secondary_color]))
            rom.write_bytes(0x13F05 + (16 * i), bytearray([tertiary_color]))
            rom.write_bytes(0x13F19 + (16 * i), bytearray([base_color]))

        palace_tilesets = [0, 1, 2, 5, 6, 7, 8]
        base_tilesets = palace_tilesets.copy()
        world.random.shuffle(palace_tilesets)
        for i in range(9):
            rom.copy_bytes(0x29650 + (i * 0x2000), 0xC0, 0x3AB00 + (i * 0xC0)) # Bricks

        for i in range(9):
            rom.copy_bytes(0x298F0 + (i * 0x2000), 0x40, 0x3B1C0 + (i * 0x40)) # Pillar head

        for i in range(9):
            rom.copy_bytes(0x29A60 + (i * 0x2000), 0x20, 0x3B400 + (i * 0x20)) # Pillar Body

        for index, tileset in enumerate(base_tilesets):
            rom.copy_bytes(0x3AB00 + (palace_tilesets[index] * 0xC0), 0xC0, 0x29650 + (tileset * 0x2000))
            rom.copy_bytes(0x3B1C0 + (palace_tilesets[index] * 0x40), 0x40, 0x298F0 + (tileset * 0x2000))
            rom.copy_bytes(0x3B400 + (palace_tilesets[index] * 0x20), 0x20, 0x29A60 + (tileset * 0x2000))

    rom.write_bytes(0x17B10, bytearray([world.options.required_crystals.value]))
    rom.write_bytes(0x17AF3, bytearray([world.options.starting_attack.value]))
    rom.write_bytes(0x17AF4, bytearray([world.options.starting_magic.value]))
    rom.write_bytes(0x17AF5, bytearray([world.options.starting_life.value]))
    rom.write_bytes(0x2B70, bytearray([world.options.palace_respawn.value]))
    rom.write_bytes(0x2B70, bytearray([world.options.palace_respawn.value]))
    rom.write_bytes(0x17DB3, bytearray([world.options.starting_lives.value]))

    if world.options.fast_great_palace:
        rom.write_bytes(0x1472C, bytearray([0xAA]))
        rom.write_bytes(0x147D5, bytearray([0x03]))

    if world.options.keep_exp:
        rom.write_bytes(0x2C40, bytearray([0x01]))

    if world.options.remove_early_boulder:
        rom.write_bytes(0x05199, bytearray([0x09])) #Remove the boulder blocking the west coast

    if world.options.better_boots:
        rom.write_bytes(0x052F0, bytearray([0x7D]))
        rom.write_bytes(0x052FE, bytearray([0xFD]))
        rom.write_bytes(0x052F3, bytearray([0xFD]))
        rom.write_bytes(0x052E4, bytearray([0x7D]))
        rom.write_bytes(0x052F4, bytearray([0x0D]))
        rom.write_bytes(0x052FF, bytearray([0xBD]))
        rom.write_bytes(0x05309, bytearray([0x3D]))
        rom.write_bytes(0x0530B, bytearray([0xFD]))
        rom.write_bytes(0x05315, bytearray([0xBD]))
        rom.write_bytes(0x0531E, bytearray([0xAD]))
        rom.write_bytes(0x05327, bytearray([0xAD]))
        rom.write_bytes(0x05330, bytearray([0x9D]))
        rom.write_bytes(0x0533B, bytearray([0x8D]))
        rom.write_bytes(0x052CB, bytearray([0x1D]))
        rom.write_bytes(0x05277, bytearray([0x2D]))
        rom.write_bytes(0x05281, bytearray([0x1D]))
        rom.write_bytes(0x0528B, bytearray([0x1D]))
        rom.write_bytes(0x05294, bytearray([0x2D]))
        rom.write_bytes(0x0529E, bytearray([0x9D]))
        rom.write_bytes(0x052A0, bytearray([0x0D]))
        rom.write_bytes(0x052B5, bytearray([0x3D]))
        rom.write_bytes(0x052AA, bytearray([0x3D]))
        rom.write_bytes(0x052C0, bytearray([0x2D]))

    # if not world.options.encounter_rate:
        # rom.write_bytes(0x0573, bytearray([0xEA, 0xEA, 0xEA])) # Prevent the game from calling the encounter check
        # rom.write_bytes(0x02A3, bytearray([0x4C, 0xAF, 0x82]))
    
    rom.write_bytes(0x3A2B0, world.world_version.encode("ascii"))
    rom.write_bytes(0x3A2E0, bytearray([world.options.encounter_rate.value]))


    from Main import __version__
    rom.name = bytearray(f'ZELDA2AP{__version__.replace(".", "")[0:3]}_{player}_{world.multiworld.seed:11}\0', "utf8")[:21]
    rom.name.extend([0] * (21 - len(rom.name)))
    rom.write_bytes(0x3A290, rom.name)

    player_name_length = 0
    for i, byte in enumerate(world.multiworld.player_name[player].encode("utf-8")):
        rom.write_byte(0x3A2C1 + i, byte)
        player_name_length += 1
    rom.write_byte(0x3A2C0, player_name_length)

    rom.write_file("token_patch.bin", rom.get_token_binary())


class Z2ProcPatch(APProcedurePatch, APTokenMixin):
    hash = md5
    game = "Zelda II: The Adventure of Link"
    patch_file_ending = ".apz2"
    result_file_ending = ".nes"
    name: bytearray
    procedure = [
        ("apply_bsdiff4", ["z2_base.bsdiff4"]),
        ("apply_tokens", ["token_patch.bin"]),
        ("repoint_vanilla_tables", [])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset, value):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset, value: typing.Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))
    
    def copy_bytes(self, source, amount, destination):
        self.write_token(APTokenTypes.COPY, destination, (amount, source))


class Z2PatchExtensions(APPatchExtension):
    game = "Zelda II: The Adventure of Link"

    @staticmethod
    def repoint_vanilla_tables(caller: APProcedurePatch, rom: LocalRom) -> bytes:
        rom = LocalRom(rom)
        version_check = rom.read_bytes(0x3A2B0, 16)
        version_check = version_check.split(b'\xFF', 1)[0]
        version_check_str = version_check.decode("ascii")
        client_version = world_version
        if client_version != version_check_str and version_check_str != "":
            raise Exception(f"Error! Patch generated on Zelda II APWorld version {version_check_str} doesn't match client version {client_version}! " +
                            f"Please use Zelda II APWorld version {version_check_str} for patching.")
        multipliers = [2.5, 2, 1, 0.5, 0.3]
        new_time_table = []
        encounter_rate = multipliers[int.from_bytes(rom.read_bytes(0x3A2E0, 1))]
        enemy_timer_table = list(rom.read_bytes(0x250, 6))
        for timer in enemy_timer_table:
            new_time_table.append(int(timer * encounter_rate))
        rom.write_bytes(0x250, bytearray(new_time_table))
        rom.write_bytes(0x088A, bytearray([int(encounter_rate * 8)]))
        return rom.get_bytes()

header = b"\x4E\x45\x53\x1A\x08\x10\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00"


def read_headerless_nes_rom(rom: bytes) -> bytes:
    if rom[:4] == b"NES\x1A":
        return rom[16:]
    else:
        return rom


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = read_headerless_nes_rom(bytes(open(file_name, "rb").read()))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        rom_hash = basemd5.hexdigest
        if basemd5.hexdigest() != md5:
            print(basemd5.hexdigest())
            raise Exception('Supplied Base Rom does not match known MD5 for US(1.0) release. '
                            'Get the correct game and version, then dump it')
        headered_rom = bytearray(base_rom_bytes)
        headered_rom[0:0] = header
        setattr(get_base_rom_bytes, "base_rom_bytes", bytes(headered_rom))
        return bytes(headered_rom)
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: Utils.OptionsType = Utils.get_options()
    if not file_name:
        file_name = options["zelda2_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


# Fix hint text, I have a special idea where I can give it info on a random region
