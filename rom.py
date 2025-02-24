from __future__ import annotations

import itertools
import random
from pathlib import Path
import struct
from typing import Dict, List, NamedTuple, Optional, TYPE_CHECKING

import Utils
from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin, APTokenTypes

from .data import Passage, ap_id_offset, encode_str, get_symbol
from .items import ItemType, WL4Item, filter_items
from .options import Difficulty, Goal, MusicShuffle, OpenDoors, Portal, SmashThroughHardBlocks

if TYPE_CHECKING:
    from . import WL4World


# The Japanese and international versions have the same ROM mapping and in fact
# only differ by 25 bytes, so either version is acceptable.
MD5_US_EU = '5fe47355a33e3fabec2a1607af88a404'
MD5_JP = '99c8ad779a16be513a9fdff502b6f5c2'


def get_rom_address(name, offset=0):
    address = get_symbol(name, offset)
    if not address & 0x8000000:
        raise ValueError(f"{name}+{offset} is not in ROM (address: {address:07x})")
    return address & 0x8000000 - 1


def patch_instructions(patch: WL4ProcedurePatch, address: int, *instructions: int):
    patch.write_token(
        APTokenTypes.WRITE,
        address,
        b"".join(inst.to_bytes(2, 'little') for inst in instructions)
    )


class WL4PatchExtensions(APPatchExtension):
    game = 'Wario Land 4'

    @staticmethod
    def update_header(caller: APProcedurePatch, rom: bytes) -> bytes:
        rombuffer = bytearray(rom)

        # Change game name
        game_name = rombuffer[0xA0:0xAC].decode('ascii')
        if game_name == 'WARIOLANDE\0\0':
            game_name = 'WARIOLANDAPE'
        elif game_name == 'WARIOLAND\0\0\0':
            game_name = 'WARIOLANDAPJ'
        else:
            raise ValueError(f'Unrecognized game name: {game_name}')
        rombuffer[0xA0:0xAC] = game_name.encode('ascii')

        # Recalculate checksum
        checksum = 0
        for i in range(0xA0, 0xBD):
            checksum -= rombuffer[i]
        checksum -= 0x19
        rombuffer[0xBD] = checksum & 0xFF

        return bytes(rombuffer)

    @staticmethod
    def shuffle_music_and_wario_voice(caller: APProcedurePatch, rom: bytes, music: int, voices: int) -> bytes:
        local_rom = LocalRom(rom)
        shuffle_music(local_rom, music)
        shuffle_wario_voice_sets(local_rom, voices)
        return bytes(local_rom)

    @staticmethod
    def copy_medal_gfx(caller: APProcedurePatch, rom: bytes) -> bytes:
        local_rom = LocalRom(rom)
        top_tiles = local_rom.read_bytes(0x6E561C + 32 * 645, 32 * 2)
        bottom_tiles = local_rom.read_bytes(0x6E561C + 32 * 677, 32 * 2)
        tiles = bytearray()
        for tile in top_tiles + bottom_tiles:
            upper = tile & 0xF0
            lower = tile & 0x0F
            if upper != 0:
                upper += 10 << 4
            if lower != 0:
                lower += 10
            tiles.append(upper | lower)
        local_rom.write_bytes(get_rom_address("MinigameCoinTiles"), tiles)
        return bytes(local_rom)


class WL4ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = MD5_US_EU
    game = 'Wario Land 4'
    patch_file_ending = '.apwl4'
    result_file_ending = '.gba'

    def __init__(self, *args, **kwargs):
        super(WL4ProcedurePatch, self).__init__(*args, **kwargs)
        self.procedure = [
            ('apply_bsdiff4', ['basepatch.bsdiff']),
            ('apply_tokens', ['token_data.bin']),
            ('update_header', []),
            ('copy_medal_gfx', []),
        ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_base_rom_path(), 'rb') as stream:
            return stream.read()


def get_base_rom_path(file_name: str = '') -> Path:
    from . import WL4World
    if not file_name:
        file_name = WL4World.settings.rom_file

    file_path = Path(file_name)
    if file_path.exists():
        return file_path
    else:
        return Path(Utils.user_path(file_name))


def write_tokens(world: WL4World, patch: WL4ProcedurePatch):
    fill_items(world, patch)

    # Write player name and number
    player_name = world.multiworld.player_name[world.player].encode('utf-8')
    seed_name = world.multiworld.seed_name.encode('utf-8')[:64]
    patch.write_token(
        APTokenTypes.WRITE,
        get_rom_address('PlayerName'),
        player_name
    )
    patch.write_token(
        APTokenTypes.WRITE,
        get_rom_address('PlayerID'),
        world.player.to_bytes(2, 'little'),
    )
    patch.write_token(
        APTokenTypes.WRITE,
        get_rom_address('SeedName'),
        seed_name
    )

    set_goal(patch, world.options.goal)
    patch.write_token(
        APTokenTypes.WRITE,
        get_rom_address('GoldenTreasuresNeeded'),
        world.options.golden_treasure_count.value.to_bytes(1, 'little')
    )
    set_difficulty_level(patch, world.options.difficulty)

    # TODO: Maybe make it stay open so it looks cleaner
    if (world.options.portal == Portal.option_open):
        patch_instructions(patch, 0x02AC56, 0x46C0)  # nop  ; EntityAI_Tmain_docodoor_uzu_small()
        patch_instructions(patch, 0x02ACB2, 0x46C0)  # nop  ; EntityAI_Tmain_docodoor_uzu_small()
        patch_instructions(patch, 0x02AE56, 0x46C0)  # nop  ; EntityAI_Tmain_docodoor_uzu_mid()
        patch_instructions(patch, 0x02B052, 0x46C0)  # nop  ; EntityAI_Tmain_docodoor_uzu_big()
        patch_instructions(patch, 0x02B0BE, 0x46C0)  # nop  ; EntityAI_Tmain_docodoor_uzu_big()

    # Break hard blocks without stopping
    if (world.options.smash_through_hard_blocks == SmashThroughHardBlocks.option_true):
        patch_instructions(patch, 0x06ED5A, 0x46C0)  # nop            ; WarSidePanel_Attack()
        patch_instructions(patch, 0x06EDD0, 0xD00E)  # beq 0x806EDF0  ; WarDownPanel_Attack()
        patch_instructions(patch, 0x06EE68, 0xE010)  # b 0x806EE8C    ; WarUpPanel_Attack()

    patch.write_token(
        APTokenTypes.WRITE,
        get_rom_address('SendMultiworldItemsImmediately'),
        world.options.send_locations_to_server.value.to_bytes(1, 'little')
    )
    patch.write_token(
        APTokenTypes.WRITE,
        get_rom_address('TrapBehavior'),
        world.options.trap_behavior.value.to_bytes(1, 'little')
    )
    patch.write_token(
        APTokenTypes.WRITE,
        get_rom_address('DiamondShuffle'),
        world.options.diamond_shuffle.value.to_bytes(1, 'little')
    )

    patch.write_file('token_data.bin', patch.get_token_binary())


class MultiworldData(NamedTuple):
    receiver: str
    name: str


def fill_items(world: WL4World, patch: WL4ProcedurePatch):
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
            if location.item.trap:
                classification = 3
            elif location.item.advancement:
                classification = 1
            elif location.item.useful:
                classification = 2
            else:
                classification = 0
            itemid = 0xF0 | classification
        itemname = location.item.name

        if playerid == world.player:
            playername = None
        else:
            playername = world.multiworld.player_name[playerid]

        location_offset = location.level_offset() + location.entry_offset()
        patch.write_token(
            APTokenTypes.WRITE,
            get_rom_address('ItemLocationTable', location_offset),
            itemid.to_bytes(1, 'little')
        )

        multiworld_data_location = get_rom_address('MultiworldDataTable', 4 * location_offset)
        if playername is not None:
            multiworld_items[multiworld_data_location] = MultiworldData(playername, itemname)
        else:
            multiworld_items[multiworld_data_location] = None

    create_starting_inventory(world, patch)

    strings = create_strings(patch, multiworld_items)
    write_multiworld_table(patch, multiworld_items, strings)


class StartInventory:
    level_table: List[List[int]]
    abilities: int
    junk_counts: List[int]

    def __init__(self):
        self.level_table = [[0] * 6 for _ in Passage]
        self.abilities = 0
        self.junk_counts = [0] * 6

    def add(self, item: WL4Item):
        if item.type == ItemType.JEWEL:
            for level in range(4):
                if not self.level_table[item.passage][level] & item.flag:
                    self.level_table[item.passage][level] |= item.flag
                    break
        elif item.type == ItemType.CD:
            self.level_table[item.passage][item.level] |= 1 << 4
        elif item.type == ItemType.ABILITY:
            ability = item.code - (ap_id_offset + 0x40)
            flag = 1 << ability
            if ability in (1, 3) and self.abilities & flag:
                if ability == 1:
                    ability = 6
                else:
                    ability = 7
                flag = 1 << ability
            self.abilities |= flag
        elif item.type == ItemType.ITEM:
            junk_type = item.code - (ap_id_offset + 0x80)
            self.junk_counts[junk_type] += 1
        elif item.type == ItemType.TREASURE:
            treasure_type = item.code - (ap_id_offset + 0x70)
            flag = 1 << (treasure_type % 3)
            self.level_table[treasure_type // 3 + 1][4] |= flag

    def write(self, patch: WL4ProcedurePatch):
        patch.write_token(
            APTokenTypes.WRITE,
            get_rom_address('StartingInventoryItemStatus'),
            struct.pack('<36B', *(level
                                  for passage in self.level_table
                                  for level in passage))
        )
        patch.write_token(
            APTokenTypes.WRITE,
            get_rom_address('StartingInventoryWarioAbilities'),
            int.to_bytes(self.abilities, 1, 'little')
        )
        patch.write_token(
            APTokenTypes.WRITE,
            get_rom_address('StartingInventoryJunkCounts'),
            struct.pack('<6B', *(min(255, item) for item in self.junk_counts))
        )

    def __repr__(self):
        return (f'{type(self).__name__} {{ '
                f'level_table: {repr(self.level_table)}, '
                f'abilities: {repr(self.abilities)}, '
                f'junk_counts: {repr(self.junk_counts)}'
                f' }}')

    def __str__(self):
        return repr(self)


def create_starting_inventory(world: WL4World, patch: WL4ProcedurePatch):
    start_inventory = StartInventory()

    # Precollected items
    for item in world.multiworld.precollected_items[world.player]:
        start_inventory.add(item)

    # Removed gem pieces
    required_jewels = world.options.required_jewels.value
    required_jewels_entry = min(1, required_jewels)
    for name, item in filter_items(type=ItemType.JEWEL):
        if item.passage() in (Passage.ENTRY, Passage.GOLDEN):
            copies = 1 - required_jewels_entry
        else:
            copies = 4 - required_jewels

        for _ in range(copies):
            start_inventory.add(WL4Item(name, world.player))

    # Free Keyzer
    def set_keyzer(passage, level):
        start_inventory.level_table[passage][level] |= 0x20

    if world.options.open_doors != OpenDoors.option_off:
        set_keyzer(Passage.ENTRY, 0)
        for passage, level in itertools.product(range(1, 5), range(4)):
            set_keyzer(passage, level)

    if world.options.open_doors.value == OpenDoors.option_open:
        set_keyzer(Passage.GOLDEN, 0)

    start_inventory.write(patch)


def create_strings(patch: WL4ProcedurePatch,
                   multiworld_items: Dict[int, Optional[MultiworldData]]
                   ) -> Dict[Optional[str], int]:
    receivers = set()
    items = set()
    address = get_rom_address('MultiworldStringDump')
    for item in filter(lambda i: i is not None, multiworld_items.values()):
        receivers.add(item.receiver)
        items.add(item.name)
        address += 8

    strings = {None: 0}  # Map a string to its address in game
    for string in itertools.chain(receivers, items):
        if string not in strings:
            strings[string] = address | 0x8000000
            encoded = encode_str(string) + b'\xFE'
            patch.write_token(
                APTokenTypes.WRITE,
                address,
                encoded
            )
            address += len(encoded)
    return strings


def write_multiworld_table(patch: WL4ProcedurePatch,
                           multiworld_items: Dict[int, Optional[MultiworldData]],
                           strings: Dict[Optional[str], int]):
    entry_address = get_rom_address('MultiworldStringDump')
    for location_address, item in multiworld_items.items():
        if item is None:
            patch.write_token(
                APTokenTypes.WRITE,
                location_address,
                (0).to_bytes(4, 'little')
            )
        else:
            patch.write_token(
                APTokenTypes.WRITE,
                location_address,
                (entry_address | 0x8000000).to_bytes(4, 'little')
            )
            patch.write_token(
                APTokenTypes.WRITE,
                entry_address,
                struct.pack("<II", strings[item.receiver], strings[item.name])
            )
            entry_address += 8


def set_goal(patch: WL4ProcedurePatch, _goal: Goal):
    if _goal == Goal.option_local_golden_treasure_hunt:
        goal = Goal.option_golden_treasure_hunt
    elif _goal == Goal.option_local_golden_diva_treasure_hunt:
        goal = Goal.option_golden_diva_treasure_hunt
    else:
        goal = _goal.value

    patch.write_token(
        APTokenTypes.WRITE,
        get_rom_address('GoalType'),
        goal.to_bytes(1, 'little')
    )

    if goal == Goal.option_golden_treasure_hunt:
        # SelectBossDoorInit01() - Check for golden passage instead of boss defeated
        patch_instructions(
            patch,
            0x0863C2,
            0x46C0,  # nop
            0x4660,  # mov r0, r12
            0x7800,  # ldrb r0, [r0]  ; Passage ID
            0x2805,  # cmp r0, #5  ; Golden Passage
            0xD10D,  # bne 0x80863E8
        )
        patch_instructions(
            patch,
            0x08640A,
            0x1C03,  # mov r3, r0
            0x0688,  # lsl r0, r1, #26
            0x2B05,  # cmp r3, #5
            0xD101,  # beq 0x8086416
        )

    if goal == Goal.option_golden_diva_treasure_hunt:
        # SelectBossDoorInit01() - Always allow into boss room
        patch_instructions(patch, 0x0863CA, 0xE00D)  # b 0x80863E8
        patch_instructions(patch, 0x08640C, 0x2300)  # mov r3, #0


def set_difficulty_level(patch: WL4ProcedurePatch, difficulty: Difficulty):
    # SramtoWork_Load()
    hardcode_difficulty = 0x2000 | difficulty.value  # mov r0, #difficulty
    patch_instructions(patch, 0x091558, hardcode_difficulty)
    patch_instructions(patch, 0x091590, hardcode_difficulty)

    # Difficulty graphics tiles
    for i in range(3):
        english_addr = 0x742992 + 2 * i
        japanese_addr = 0x742992 + 2 * (3 + i)
        patch.write_token(
            APTokenTypes.WRITE,
            english_addr,
            (0x2C0 + 5 * difficulty.value).to_bytes(2, 'little')
        )
        patch.write_token(
            APTokenTypes.WRITE,
            japanese_addr,
            (0x2CF + 5 * difficulty.value).to_bytes(2, 'little')
        )


class LocalRom():
    def __init__(self, rom: bytes):
        self.buffer = bytearray(rom)

    def read_bit(self, address: int, bit_number: int) -> bool:
        bitflag = (1 << bit_number)
        return ((self.buffer[address] & bitflag) != 0)

    def read_byte(self, address: int) -> int:
        return self.buffer[address]

    def read_bytes(self, startaddress: int, length: int) -> bytes:
        return self.buffer[startaddress:startaddress + length]

    def read_halfword(self, address: int) -> int:
        assert address % 2 == 0, f'Misaligned halfword address: {address:x}'
        halfword = self.read_bytes(address, 2)
        return int.from_bytes(halfword, 'little')

    def read_word(self, address: int) -> int:
        assert address % 4 == 0, f'Misaligned word address: {address:x}'
        word = self.read_bytes(address, 4)
        return int.from_bytes(word, 'little')

    def write_byte(self, address: int, value: int):
        self.buffer[address] = value

    def write_bytes(self, startaddress: int, values):
        self.buffer[startaddress:startaddress + len(values)] = values

    def write_halfword(self, address: int, value: int):
        assert address % 2 == 0, f'Misaligned halfword address: {address:x}'
        halfword = value.to_bytes(2, 'little')
        self.write_bytes(address, halfword)

    def write_word(self, address: int, value: int):
        assert address % 4 == 0, f'Misaligned word address: {address:x}'
        word = value.to_bytes(4, 'little')
        self.write_bytes(address, word)

    def __bytes__(self):
        return bytes(self.buffer)


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


def shuffle_music(rom: LocalRom, music_shuffle: int):
    if music_shuffle == MusicShuffle.option_none:
        return
    # music_shuffle >= MusicShuffle.option_levels_only
    music_pool = [*level_songs]
    if music_shuffle >= MusicShuffle.option_levels_and_extras:
        music_pool += level_adjacent_songs
    if music_shuffle >= MusicShuffle.option_full:
        music_pool += other_songs

    music_table_address = 0x098028
    # Only change the header pointers; leave the music player numbers alone
    music_info_table = [rom.read_word(music_table_address + 8 * i) for i in range(819)]

    if music_shuffle == MusicShuffle.option_disabled:
        shuffled_music = [0] * len(music_pool)
    else:
        shuffled_music = list(music_pool)
        random.shuffle(shuffled_music)
    for vanilla, shuffled in zip(music_pool, shuffled_music):
        rom.write_word(music_table_address + 8 * vanilla, music_info_table[shuffled])

    # Remove horizontal mixing in Palm Tree Paradise and Mystic Lake

    palm_tree_paradise_doors = range(0x3F30F0, 0x3F3240, 12)
    # Set most doors' music IDs to 0 (no change)
    for addr in palm_tree_paradise_doors[1:23]:
        rom.write_halfword(addr + 10, 0)
    # Set pink pipes to the same as the portal
    rom.write_halfword(palm_tree_paradise_doors[23] + 10, 0x28B)
    rom.write_halfword(palm_tree_paradise_doors[25] + 10, 0x28B)
    # 2A1 and 2A2 are both the pink room theme, but for some reason it only
    # crossfades like it should if I change 2A1 to 2A2
    rom.write_halfword(palm_tree_paradise_doors[24] + 10, 0x2A2)

    mystic_lake_doors = range(0x3F3420, 0x3F3570, 12)
    for addr in mystic_lake_doors[1:23]:
        rom.write_halfword(addr + 10, 0)
    rom.write_halfword(mystic_lake_doors[23] + 10, 0x28F)
    rom.write_halfword(mystic_lake_doors[25] + 10, 0x28F)
    rom.write_halfword(mystic_lake_doors[26] + 10, 0x2A2)


def shuffle_wario_voice_sets(rom: LocalRom, shuffle: int):
    if not shuffle:
        return

    voice_set_pointer_address = 0x6D3648
    voice_set_pointers = [rom.read_word(voice_set_pointer_address + 4 * i) for i in range(12)]
    voice_set_length_address = 0x6D3394
    voice_set_lengths = [rom.read_word(voice_set_length_address + 4 * i) for i in range(12)]
    voice_sets = list(zip(voice_set_pointers, voice_set_lengths))

    random.shuffle(voice_sets)
    for i, (pointer, length) in enumerate(voice_sets):
        rom.write_word(voice_set_pointer_address + 4 * i, pointer)
        rom.write_word(voice_set_length_address + 4 * i, length)
