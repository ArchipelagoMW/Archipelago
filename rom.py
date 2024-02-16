from __future__ import annotations

import hashlib
import itertools
import random
from pathlib import Path
from typing import Dict, NamedTuple, Optional, TYPE_CHECKING

import bsdiff4
from Options import PerGameCommonOptions

import Utils
from Patch import APDeltaPatch

from .data import ap_id_offset, data_path, Domain, encode_str, get_symbol
from .items import WL4Item, filter_items
from .types import ItemType, Passage
from .options import Difficulty, MusicShuffle, OpenDoors, WarioVoiceShuffle

if TYPE_CHECKING:
    from . import WL4World


# The Japanese and international versions have the same ROM mapping and in fact
# only differ by 25 bytes, so either version is acceptable.
MD5_US_EU = '5fe47355a33e3fabec2a1607af88a404'
MD5_JP = '99c8ad779a16be513a9fdff502b6f5c2'


class WL4DeltaPatch(APDeltaPatch):
    hash = MD5_US_EU
    game = 'Wario Land 4'
    patch_file_ending = '.apwl4'
    result_file_ending = '.gba'

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


class LocalRom():
    def __init__(self, file: Path, name=None, hash=None):
        self.name = name
        self.hash = hash

        with open(file, "rb") as rom_file:
            rom_bytes = rom_file.read()
        patch_bytes = data_path("basepatch.bsdiff")
        self.buffer = bytearray(bsdiff4.patch(rom_bytes, patch_bytes))

    def read_bit(self, address: int, bit_number: int, space: Domain = Domain.SYSTEM_BUS) -> bool:
        address = Domain.ROM.convert_from(space, address)
        bitflag = (1 << bit_number)
        return ((self.buffer[address] & bitflag) != 0)

    def read_byte(self, address: int, space: Domain = Domain.SYSTEM_BUS) -> int:
        address = Domain.ROM.convert_from(space, address)
        return self.buffer[address]

    def read_bytes(self, startaddress: int, length: int, space: Domain = Domain.SYSTEM_BUS) -> bytes:
        startaddress = Domain.ROM.convert_from(space, startaddress)
        return self.buffer[startaddress:startaddress + length]

    def read_halfword(self, address: int, space: Domain = Domain.SYSTEM_BUS) -> int:
        assert address % 2 == 0, f'Misaligned halfword address: {address:x}'
        halfword = self.read_bytes(address, 2, space)
        return int.from_bytes(halfword, 'little')

    def read_word(self, address: int, space: Domain = Domain.SYSTEM_BUS) -> int:
        assert address % 4 == 0, f'Misaligned word address: {address:x}'
        word = self.read_bytes(address, 4, space)
        return int.from_bytes(word, 'little')

    def write_byte(self, address: int, value: int, space: Domain = Domain.SYSTEM_BUS):
        address = Domain.ROM.convert_from(space, address)
        self.buffer[address] = value

    def write_bytes(self, startaddress: int, values, space: Domain = Domain.SYSTEM_BUS):
        startaddress = Domain.ROM.convert_from(space, startaddress)
        self.buffer[startaddress:startaddress + len(values)] = values

    def write_halfword(self, address: int, value: int, space: Domain = Domain.SYSTEM_BUS):
        assert address % 2 == 0, f'Misaligned halfword address: {address:x}'
        halfword = value.to_bytes(2, 'little')
        self.write_bytes(address, halfword, space)

    def write_word(self, address: int, value: int, space: Domain = Domain.SYSTEM_BUS):
        assert address % 4 == 0, f'Misaligned word address: {address:x}'
        word = value.to_bytes(4, 'little')
        self.write_bytes(address, word, space)

    def write_to_file(self, file: Path):
        with open(file, 'wb') as stream:
            stream.write(self.buffer)


class MultiworldExtData(NamedTuple):
    receiver: str
    name: str


def fill_items(rom: LocalRom, world: WL4World):
    # Place item IDs and collect multiworld entries
    multiworld_items = {}
    for location in world.multiworld.get_locations(world.player):
        itemid = location.item.code if location.item is not None else ...
        locationid = location.address
        playerid = location.item.player
        if itemid is None or locationid is None:
            continue

        if location.native_item:
            itemid = itemid - ap_id_offset
        else:
            itemid = 0xF0 | location.item.classification.as_flag()
        itemname = location.item.name

        if playerid == world.player:
            playername = None
        else:
            playername = world.multiworld.player_name[playerid]

        location_offset = location.level_offset() + location.entry_offset()
        item_location = get_symbol('ItemLocationTable', location_offset)
        rom.write_byte(item_location, itemid)

        ext_data_location = get_symbol('ItemExtDataTable', 4 * location_offset)
        if playername is not None:
            multiworld_items[ext_data_location] = MultiworldExtData(playername, itemname)
        else:
            multiworld_items[ext_data_location] = None

    create_starting_inventory(rom, world)

    strings = create_strings(rom, multiworld_items)
    write_multiworld_table(rom, multiworld_items, strings)


def create_starting_inventory(rom: LocalRom, world: WL4World):
    # Precollected items
    for item in world.multiworld.precollected_items[world.player]:
        give_item(rom, item)

    # Removed gem pieces
    required_jewels = world.options.required_jewels.value
    required_jewels_entry = min(1, required_jewels)
    for name, item in filter_items(type=ItemType.JEWEL):
        if item.passage() in (Passage.ENTRY, Passage.GOLDEN):
            copies = 1 - required_jewels_entry
        else:
            copies = 4 - required_jewels

        for _ in range(copies):
            give_item(rom, WL4Item.from_name(name, world.player))

    # Free Keyzer
    def set_keyzer(passage, level):
        address = level_to_start_inventory_address(passage, level)
        rom.write_byte(address, rom.read_byte(address) | 0x20)

    if world.options.open_doors != OpenDoors.option_off:
        set_keyzer(Passage.ENTRY, 0)
        for passage, level in itertools.product(range(1, 5), range(4)):
            set_keyzer(passage, level)

    if world.options.open_doors.value == OpenDoors.option_open:
        set_keyzer(Passage.GOLDEN, 0)


def give_item(rom: LocalRom, item: WL4Item):
    if item.type == ItemType.JEWEL:
        for level in range(4):
            address = level_to_start_inventory_address(item.passage, level)
            status = rom.read_byte(address)
            if not status & item.flag:
                status |= item.flag
                rom.write_byte(address, status)
                break
    elif item.type == ItemType.CD:
        address = level_to_start_inventory_address(item.passage, item.level)
        status = rom.read_byte(address)
        status |= 1 << 4
        rom.write_byte(address, status)
    elif item.type == ItemType.ABILITY:
        ability = item.code - (ap_id_offset + 0x40)
        flag = 1 << ability
        address = get_symbol('StartingInventoryWarioAbilities')
        abilities = rom.read_byte(address)
        abilities |= flag
        rom.write_byte(address, abilities)
    elif item.type == ItemType.ITEM:
        junk_type = item.code - (ap_id_offset + 0x80)
        address = get_symbol('StartingInventoryJunkCounts', junk_type)
        count = rom.read_byte(address)
        count += 1
        rom.write_byte(address, count)


def level_to_start_inventory_address(passage: Passage, level: int):
    index = 6 * passage + level
    return get_symbol('StartingInventoryItemStatus', index)


def create_strings(rom: LocalRom,
                   multiworld_items: Dict[int, Optional[MultiworldExtData]]
                   ) -> Dict[Optional[str], int]:
    receivers = set()
    items = set()
    address = get_symbol('MultiworldStringDump')
    for item in filter(lambda i: i is not None, multiworld_items.values()):
        receivers.add(item.receiver)
        items.add(item.name)
        address += 8

    strings = {None: 0}  # Map a string to its address in game
    for string in itertools.chain(receivers, items):
        if string not in strings:
            strings[string] = address
            encoded = encode_str(string) + b'\xFE'
            rom.write_bytes(address, encoded)
            address += len(encoded)
    return strings


def write_multiworld_table(rom: LocalRom,
                           multiworld_items: Dict[int, Optional[MultiworldExtData]],
                           strings: Dict[Optional[str], int]):
    entry_address = get_symbol('MultiworldStringDump')
    for location_address, item in multiworld_items.items():
        if item is None:
            rom.write_word(location_address, 0)
        else:
            rom.write_word(location_address, entry_address)
            rom.write_word(entry_address, strings[item.receiver])
            rom.write_word(entry_address + 4, strings[item.name])
            entry_address += 8


def set_difficulty_level(rom: LocalRom, difficulty: Difficulty):
    mov_r0 = 0x2000 | difficulty.value     # mov r0, #difficulty
    cmp_r0 = 0x2800 | difficulty.value     # cmp r0, #difficulty

    # SramtoWork_Load()
    rom.write_halfword(0x8091558, mov_r0)  # Force difficulty (anti-cheese)

    # ReadySub_Level()
    rom.write_halfword(0x8091F8E, 0x2001)  # movs r0, r1  ; Allow selecting S-Hard
    rom.write_halfword(0x8091FCC, 0x46C0)  # nop  ; Force cursor to difficulty
    rom.write_halfword(0x8091FD2, 0xE007)  # b 0x8091FE4
    rom.write_halfword(0x8091FE4, cmp_r0)

    # ReadyObj_Win1Set()
    rom.write_halfword(0x8092268, 0x2001)  # movs r0, #1  ; Display S-Hard


# https://github.com/wario-land/Toge-Docs/blob/master/Steaks/music_and_sound_effects.md#sfx-indices

level_songs = [
    0x2A0,  # Hall of Hieroglyphs
    0x28B,  # Palm Tree Paradise
    0x28E,  # Wildflower Fields
    0x28F,  # Mystic Lake
    0x292,  # Monsoon Jungle
    0x293,  # The Curious Factory
    0x294,  # The Toxic Landfill
    0x296,  # 40 Below Fridge
    0x295,  # Pinball Zone
    0x297,  # Toy Block Tower
    0x298,  # The Big Board
    0x299,  # Doodle Woods
    0x29A,  # Domino Row
    0x29B,  # Crescent Moon Village
    0x29C,  # Arabian Night
    0x29E,  # Fiery Cavern
    0x29D,  # Hotel Horror
    0x29F,  # Golden Passage
]

level_adjacent_songs = [  # Play in levels but aren't a level's main theme
    0x269,  # Wario's workout
    0x280,  # Boss corridor
    0x2A2,  # Bonus Room
    0x2A9,  # Hurry Up!
    0x2AF,  # Passage Boss
    0x2B0,  # Golden Diva
]

other_songs = [  # Not made to play in levels
    0x26A,  # Sound Room
    0x27C,  # Intro
    0x27F,  # Level select screen
    0x2AA,  # Item Shop
    0x2BD,  # Mini-Game Shop
]


def shuffle_music(rom: LocalRom, music_shuffle: MusicShuffle):
    if music_shuffle == MusicShuffle.option_none:
        return
    # music_shuffle >= MusicShuffle.option_levels_only
    music_pool = [*level_songs]
    if music_shuffle >= MusicShuffle.option_levels_and_extras:
        music_pool += level_adjacent_songs
    if music_shuffle >= MusicShuffle.option_full:
        music_pool += other_songs

    music_table_address = 0x8098028
    # Only change the header pointers; leave the music player numbers alone
    music_info_table = [rom.read_word(music_table_address + 8 * i) for i in range(819)]

    shuffled_music = list(music_pool)
    random.shuffle(shuffled_music)
    for vanilla, shuffled in zip(music_pool, shuffled_music):
        rom.write_word(music_table_address + 8 * vanilla, music_info_table[shuffled])

    # Remove horizontal mixing in Palm Tree Paradise and Mystic Lake

    palm_tree_paradise_doors = range(0x83F30F0, 0x83F3240, 12)
    # Set most doors' music IDs to 0 (no change)
    for addr in palm_tree_paradise_doors[1:23]:
        rom.write_halfword(addr + 10, 0)
    # Set pink pipes to the same as the portal
    rom.write_halfword(palm_tree_paradise_doors[23] + 10, 0x28B)
    rom.write_halfword(palm_tree_paradise_doors[25] + 10, 0x28B)
    # 2A1 and 2A2 are both the pink room theme, but for some reason it only
    # crossfades like it should if I change 2A1 to 2A2
    rom.write_halfword(palm_tree_paradise_doors[24] + 10, 0x2A2)

    mystic_lake_doors = range(0x83F3420, 0x83F3570, 12)
    for addr in mystic_lake_doors[1:23]:
        rom.write_halfword(addr + 10, 0)
    rom.write_halfword(mystic_lake_doors[23] + 10, 0x28F)
    rom.write_halfword(mystic_lake_doors[25] + 10, 0x28F)
    rom.write_halfword(mystic_lake_doors[26] + 10, 0x2A2)


def shuffle_wario_voice_sets(rom: LocalRom, shuffle: WarioVoiceShuffle):
    if not shuffle.value:
        return

    voice_set_pointer_address = 0x86D3648
    voice_set_pointers = [rom.read_word(voice_set_pointer_address + 4 * i) for i in range(12)]
    voice_set_length_address = 0x86D3394
    voice_set_lengths = [rom.read_word(voice_set_length_address + 4 * i) for i in range(12)]
    voice_sets = list(zip(voice_set_pointers, voice_set_lengths))

    random.shuffle(voice_sets)
    for i, (pointer, length) in enumerate(voice_sets):
        rom.write_word(voice_set_pointer_address + 4 * i, pointer)
        rom.write_word(voice_set_length_address + 4 * i, length)


def patch_rom(rom: LocalRom, world: WL4World):
    fill_items(rom, world)

    # Write player name and number
    player_name = world.multiworld.player_name[world.player].encode('utf-8')
    rom.write_bytes(get_symbol('PlayerName'), player_name)
    rom.write_byte(get_symbol('PlayerID'), world.player)

    # Set deathlink
    rom.write_byte(get_symbol('DeathLinkFlag'), world.options.death_link.value)

    set_difficulty_level(rom, world.options.difficulty)

    # TODO: Maybe make it stay open so it looks cleaner
    if (world.options.portal.value):
        rom.write_halfword(0x802AC56, 0x46C0)  # nop  ; EntityAI_Tmain_docodoor_uzu_small()
        rom.write_halfword(0x802ACB2, 0x46C0)  # nop  ; EntityAI_Tmain_docodoor_uzu_small()
        rom.write_halfword(0x802AE56, 0x46C0)  # nop  ; EntityAI_Tmain_docodoor_uzu_mid()
        rom.write_halfword(0x802B052, 0x46C0)  # nop  ; EntityAI_Tmain_docodoor_uzu_big()
        rom.write_halfword(0x802B0BE, 0x46C0)  # nop  ; EntityAI_Tmain_docodoor_uzu_big()

    # Break hard blocks without stopping
    if (world.options.smash_through_hard_blocks.value):
        rom.write_halfword(0x806ED5A, 0x46C0)  # nop            ; WarSidePanel_Attack()
        rom.write_halfword(0x806EDD0, 0xD00E)  # beq 0x806EDF0  ; WarDownPanel_Attack()
        rom.write_halfword(0x806EE68, 0xE010)  # b 0x806EE8C    ; WarUpPanel_Attack()

    # Multiworld send
    rom.write_byte(get_symbol('SendMultiworldItemsImmediately'),
                   world.options.send_multiworld_items.value)

    shuffle_music(rom, world.options.music_shuffle)
    shuffle_wario_voice_sets(rom, world.options.wario_voice_shuffle)


def get_base_rom_bytes(file_name: str = '') -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, 'base_rom_bytes', None)
    if not base_rom_bytes:
        file_path = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_path, 'rb').read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in (MD5_US_EU, MD5_JP):
            raise Exception('Supplied base ROM does not match the US/EU or '
                            'Japanese version of Wario Land 4. Please provide '
                            'the correct ROM version')

        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = '') -> Path:
    options = Utils.get_options()
    if not file_name:
        file_name = options['wl4_options']['rom_file']

    file_path = Path(file_name)
    if file_path.exists():
        return file_path
    else:
        return Path(Utils.user_path(file_name))
