import hashlib
import os

import Utils
from Patch import read_rom, APDeltaPatch

NA10HASH = 'e986575b98300f721ce27c180264d890'
ROM_PLAYER_LIMIT = 65535
ROM_NAME = 0x303F00
event_flag_base_address = 0xF51e80
bit_positions = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
esper_bit_base_address = 0xF51A69
character_intialized_bit_base_address = 0xF51EDC
character_recruited_bit_base_address = 0xf51EDE
espers = [ # This is the internal order of the Espers in the game. Editing this will break things.
    "Ramuh", "Ifrit", "Shiva",
    "Siren", "Terrato", "Shoat",
    "Maduin", "Bismark", "Stray",
    "Palidor", "Tritoch", "Odin",
    "Raiden", "Bahamut", "Alexandr",
    "Crusader", "Ragnarok", "Kirin",
    "ZoneSeek", "Carbunkl", "Phantom",
    "Sraphim", "Golem", "Unicorn",
    "Fenrir", "Starlet", "Phoenix"
]

characters = [ # Same here.
    "TERRA", "LOCKE", "CYAN", "SHADOW", "EDGAR", "SABIN", "CELES", "STRAGO",
    "RELM", "SETZER", "MOG", "GAU", "GOGO", "UMARO"
]


event_flag_location_names = {
    'Whelk': 0x135,
    'Lete River': 0x1a,
    'Sealed Gate': 0x471,
    'Zozo': 0x52,
    'Mobliz': 0x0bf,
    'South Figaro Cave': 0x0b1,
    'Narshe Weapon Shop 1': 0x0b7,
    "Narshe Weapon Shop 2": 0x0b6,
    'Phoenix Cave': 0x0d7,
    'Red Dragon': 0x120,
    'Doma Castle Siege': 0x040,
    'Dream Stooges': 0x0d8,
    'Wrexsoul': 0x0da,
    'Doma Castle Throne': 0x0db,
    'Mt. Zozo': 0x0d2,
    'Storm Dragon': 0x11b,
    'Gau Father House': 0x162,
    'Imperial Air Force': 0x02a,
    'AtmaWeapon': 0x0a1,
    'Nerapa': 0x0a5,
    'Veldt Cave': 0x199,
    'Figaro Castle Throne': 0x004,
    'Figaro Castle Basement': 0x0c6,
    'Ancient Castle': 0x2dd,
    'Blue Dragon': 0x11f,
    'Mt. Kolts': 0x010,
    'Collapsing House': 0x28a,
    'Baren Falls': 0x03f,
    'Imperial Camp': 0x037,
    'Phantom Train': 0x192,
    'South Figaro': 0x01d,
    'Ifrit and Shiva': 0x061,
    'Number 024': 0x05f,
    'Cranes': 0x06b,
    'Opera House': 0x5b,
    'Burning House': 0x090,
    "Ebot's Rock": 0x19c,
    'MagiMaster': 0x2db,
    'Gem Box': 0x0ba,
    'Esper Mountain': 0x095,
    "Owzer Mansion": 0x253,
    'Kohlingen': 0x18e,
    "Daryl's Tomb": 0x2b2,
    'Lone Wolf 1': 0x29f,
    "Lone Wolf 2": 0x241,
    'Veldt': 0x1bc,
    'Serpent Trench': 0x050,
    "Gogo's Cave": 0x0d4,
    "Umaro's Cave": 0x07e,
    'Kefka at Narshe': 0x046,
    'Tzen Thief': 0x27c,
    'Doom Gaze': 0x2a1,
    'Tritoch': 0x29e,
    'Auction House 10kGP': 0x16c,
    'Auction House 20kGP': 0x16d,
    'Dirt Dragon': 0x11c,
    'White Dragon': 0x121,
    'Ice Dragon': 0x11a,
    'Atma': 0x0a2,
    "Skull Dragon": 0x11e,
    "Gold Dragon": 0x11d
}


class FF6WCDeltaPatch(APDeltaPatch):
    hash = NA10HASH
    game = "Final Fantasy 6 Worlds Collide"
    patch_file_ending = "apff6wc"

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
        if NA10HASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for NA (1.0) release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["ff6wc_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.local_path(file_name)
    return file_name


def get_event_flag_value(event_id):
    event_byte = event_flag_base_address + (event_id // 8)
    event_bit = event_id % 8
    hbyte = hex(event_byte)
    bbyte = bin(event_byte)
    hbit = hex(bit_positions[event_bit])
    bbit = bin(bit_positions[event_bit])
    return event_byte, bit_positions[event_bit]


def get_obtained_esper_bit(esper_name):
    esper_index = esper_name
    esper_byte = esper_bit_base_address + (esper_index // 8)
    esper_bit = esper_index % 8
    return esper_byte, bit_positions[esper_bit]


def get_character_bit(character, address):
    character_index = character
    character_byte = address + character_index // 8
    character_bit = character_index % 8
    return character_byte, bit_positions[character_bit]


def get_character_initialized_bit(character_name):
    return get_character_bit(character_name, character_intialized_bit_base_address)


def get_character_recruited_bit(character_name):
    return get_character_bit(character_name, character_recruited_bit_base_address)