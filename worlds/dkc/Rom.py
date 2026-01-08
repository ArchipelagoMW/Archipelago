import typing
import Utils
import hashlib
import os
import json

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from . import DKCWorld

from .Items import item_groups
from .Names import ItemName
from .Aesthetics import get_palette_bytes, diddy_palettes, donkey_palettes, player_palette_set_offsets

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension

HASH_US = '30c5f292ff4cbbfcc00fd8fa96c2de3b'

STARTING_ID = 0xBF1000

rom_start_inventory = {
    ItemName.carry: 0x3BF793,
    ItemName.climb: 0x3BF794,
    ItemName.roll: 0x3BF795,
    ItemName.slap: 0x3BF796,
    ItemName.swim: 0x3BF797,
    ItemName.rambi: 0x3BF798,
    ItemName.expresso: 0x3BF799,
    ItemName.winky: 0x3BF79A,
    ItemName.enguarde: 0x3BF79B,
    ItemName.squawks: 0x3BF79C,
    ItemName.kannons: 0x3BF79D,
    ItemName.switches: 0x3BF79E,
    ItemName.minecart: 0x3BF79F,
    ItemName.tires: 0x3BF7A0,
    ItemName.platforms: 0x3BF7A1,
    ItemName.kongo_jungle: 0x3BF7A2,
    ItemName.monkey_mines: 0x3BF7A3,
    ItemName.vine_valley: 0x3BF7A4,
    ItemName.gorilla_glacier: 0x3BF7A5,
    ItemName.kremkroc_industries: 0x3BF7A6,
    ItemName.chimp_caverns: 0x3BF7A7,
}

unlock_data = {
    STARTING_ID + 0x0000: [0x14, 0x0A], # Jungle
    STARTING_ID + 0x0001: [0x15, 0x0A], # Mines
    STARTING_ID + 0x0002: [0x16, 0x0A], # Valley
    STARTING_ID + 0x0003: [0x17, 0x0A], # Glacier
    STARTING_ID + 0x0004: [0x18, 0x0A], # Industries
    STARTING_ID + 0x0005: [0x19, 0x0A], # Caverns

    STARTING_ID + 0x0010: [0x00, 0x3F], # Donkey
    STARTING_ID + 0x0011: [0x00, 0x3E], # Diddy

    STARTING_ID + 0x0012: [0x01, 0x4F], # Carry
    STARTING_ID + 0x0013: [0x02, 0x4F], # Swim
    STARTING_ID + 0x0014: [0x03, 0x4F], # Roll
    STARTING_ID + 0x0015: [0x04, 0x4F], # Climb
    STARTING_ID + 0x0016: [0x05, 0x4F], # Slap
    STARTING_ID + 0x0017: [0x07, 0x14], # Kannons
    STARTING_ID + 0x0018: [0x08, 0x2C], # Switches
    STARTING_ID + 0x0019: [0x09, 0x02], # Minecart
    STARTING_ID + 0x001A: [0x0A, 0x5F], # Winky
    STARTING_ID + 0x001B: [0x0B, 0x58], # Expresso
    STARTING_ID + 0x001C: [0x0C, 0x56], # Rambi
    STARTING_ID + 0x001D: [0x0D, 0x57], # Enguarde
    STARTING_ID + 0x001E: [0x0E, 0x11], # Squawks
    STARTING_ID + 0x001F: [0x0F, 0x01], # Tires
    STARTING_ID + 0x0020: [0x10, 0x31], # Platforms
}

currency_data = {
    STARTING_ID + 0x000F: [0x801E, 0x0A], # Big Bananas
    STARTING_ID + 0x0031: [0x0575, 0x73], # Red Balloon
}

trap_data = {
    STARTING_ID + 0x0080: [0x28, 0x67], # Nut Trap
    STARTING_ID + 0x0081: [0x2C, 0x63], # Army Trap
    STARTING_ID + 0x0082: [0x30, 0x63], # Jump Trap
    STARTING_ID + 0x0083: [0x38, 0x63], # Animal Bonus Trap
    STARTING_ID + 0x0084: [0x40, 0x63], # Sticky Floor Trap
    STARTING_ID + 0x0085: [0x48, 0x63], # Stun Trap
    STARTING_ID + 0x0086: [0x44, 0x63], # Ice Trap
    STARTING_ID + 0x0032: [0x24, 0x6C], # Instant DK Barrel (not a trap, but this system works better lol)
    STARTING_ID + 0x0033: [0x22, 0x2F], # Banana Extractinator (not a trap, but this system works better lol)
    STARTING_ID + 0x0034: [0x11, 0x2F], # Cache Radar (not a trap, but this system works better lol)
}

letter_addr = {
    "A": 0x347519,
    "B": 0x3475A3,
    "C": 0x34762D,
    "D": 0x3476B7,
    "E": 0x347741,
    "F": 0x3477CB,
    "G": 0x347855,
    "H": 0x3478DF,
    "I": 0x347969,
    "J": 0x3479F3,
    "K": 0x347A7D,
    "L": 0x347B07,
    "M": 0x347B91,
    "N": 0x347C1B,
    "O": 0x347CA5,
    "P": 0x347D2F,
    "Q": 0x347DB9,
    "R": 0x347E43,
    "S": 0x347ECD,
    "T": 0x347F57,
    "U": 0x347FE1,
    "V": 0x34806B,
    "W": 0x3480F5,
    "X": 0x34817F,
    "Y": 0x348209,
    "Z": 0x348293,
}

# DKC1_NorSpr16_KongLetter_Main

class DKCPatchExtension(APPatchExtension):
    game = "Donkey Kong Country"

    @staticmethod
    def swap_kong_letters(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = bytearray(rom)
        json_data = json.loads(caller.get_file("data.json").decode("UTF-8"))
        offset = 0x39E465
        ptr = 0x3BE5EC
        for letter in json_data["kong"]:
            if letter not in letter_addr.keys():
                letter = "A"
            # Copy asset
            addr = letter_addr[letter] + 10
            rom[offset:offset+0x40] = rom[addr:addr+0x40]
            rom[offset+0x200:offset+0x240] = rom[addr+0x40:addr+0x80]
            offset += 0x40

            # Repoint data
            addr = letter_addr[letter]
            rom[ptr:ptr+4] = (addr | 0xF00000).to_bytes(4,"little")
            ptr += 4
        
        return bytes(rom)

class DKCProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [HASH_US]
    game = "Donkey Kong Country"
    patch_file_ending = ".apdkc"
    result_file_ending = ".sfc"
    name: bytearray
    procedure = [
        ("apply_tokens", ["token_patch.bin"]),
        ("apply_bsdiff4", ["dkc_basepatch.bsdiff4"]),
        ("swap_kong_letters", []),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset: int, value: int):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset: int, value: typing.Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))

def patch_rom(world: "DKCWorld", patch: DKCProcedurePatch):
    # Write additional data for generation
    data_dict = {
        "seed": world.random.getrandbits(64),
        "kong": world.options.kong_letters.value[:4].upper(),
    }
    patch.write_file("data.json", json.dumps(data_dict).encode("UTF-8"))

    # Edit the ROM header
    from Utils import __version__
    patch.name = bytearray(f'DKC1{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
    patch.name.extend([0] * (21 - len(patch.name)))
    patch.write_bytes(0xFFC0, patch.name)

    patch.write_byte(0x3BF790, world.options.starting_life_count.value)

    # Starting inventory
    patch.write_byte(0x3BF791, world.options.gangplank_tokens.value)
    patch.write_byte(0x3BF792, world.options.starting_kong.value)

    for item in item_groups["Abilities"]:
        addr = rom_start_inventory[item]
        if item in world.options.shuffle_abilities.value:
            patch.write_byte(addr, 0x00)
        else:
            patch.write_byte(addr, 0x01)
    for item in item_groups["Animals"]:
        addr = rom_start_inventory[item]
        if item in world.options.shuffle_animals.value:
            patch.write_byte(addr, 0x00)
        else:
            patch.write_byte(addr, 0x01)
    for item in item_groups["Objects"]:
        addr = rom_start_inventory[item]
        if item in world.options.shuffle_objects.value:
            patch.write_byte(addr, 0x00)
        else:
            patch.write_byte(addr, 0x01)

    adjust_palettes(world, patch)

    patch.write_byte(0x3BF7A8, world.options.energy_link.value)
    patch.write_byte(0x3BF7A9, world.options.trap_link.value)
    #patch.write_byte(0x3BF7AA, world.options.death_link.value)
    
    patch.write_byte(0x3BF7AB, world.options.required_jungle_levels.value)
    patch.write_byte(0x3BF7AC, world.options.required_mines_levels.value)
    patch.write_byte(0x3BF7AD, world.options.required_valley_levels.value)
    patch.write_byte(0x3BF7AE, world.options.required_glacier_levels.value)
    patch.write_byte(0x3BF7AF, world.options.required_industries_levels.value)
    patch.write_byte(0x3BF7B0, world.options.required_caverns_levels.value)

    patch.write_file("token_patch.bin", patch.get_token_binary())


def adjust_palettes(world: "DKCWorld", patch: DKCProcedurePatch):
    palette_options = {
        "Donkey": world.options.palette_donkey_active.current_key,
        "Donkey Inactive":  world.options.palette_donkey_inactive.current_key,
        "Diddy": world.options.palette_diddy_active.current_key,
        "Diddy Inactive": world.options.palette_diddy_inactive.current_key,
    }
    player_custom_palettes = world.options.player_palettes
    player_palette_filters = world.options.player_palette_filters
    for palette_set, offset in player_palette_set_offsets.items():
        palette_option = palette_options[palette_set]
        if "Diddy" in palette_set:
            palette = diddy_palettes[palette_option]
        else:
            palette = donkey_palettes[palette_option]

        if palette_set in player_custom_palettes.keys():
            if len(player_custom_palettes[palette_set]) == 0x0F:
                palette = player_custom_palettes[palette_set]
            else:
                print (f"[{world.multiworld.player_name[world.player]}] Custom palette set for {palette_set} doesn't have exactly 15 colors. Falling back to the selected preset ({palette_option})")
        
        if palette_set in player_palette_filters:
            filter_option = player_palette_filters[palette_set]
        else:
            filter_option = 0
        data = get_palette_bytes(palette, filter_option)
        patch.write_bytes(offset, data)


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {HASH_US}:
            raise Exception('Supplied Base Rom does not match known MD5 for US 1.0 release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["dkc_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
