import hashlib
import os
import pkgutil
import bsdiff4

import Utils

from worlds.Files import APDeltaPatch
from settings import get_settings

from .rom_addresses import rom_addresses

# Enemy and Platform randomizer ported directly from SML2R
# https://github.com/slashinfty/sml2r-node/blob/862128c73d336d6cbfbf6290c09f3eff103688e8/src/index.ts#L284


def sprite_extract(a, b):
    x = ((0b00010000 & a) << 2)
    y = ((0b11100000 & a) >> 2)
    z = ((0b11100000 & b) >> 5)
    return x | y | z


def sprite_insert(a, b, s):
    x = ((s & 0b01000000) >> 2)
    y = ((s & 0b00111000) << 2)
    z = ((s & 0b00000111) << 5)
    return [(a & 0b00001111) | x | y, (b & 0b00011111) | z]


def copy_sprite(data, arr, pos):
    for i in range(2):
        data[pos + i] = arr[i]


def randomize_sprite(data, random, arr, i):
    selected_sprite = sprite_insert(data[i], data[i + 1], random.choice(arr))
    copy_sprite(data, selected_sprite, i)


def randomize_enemies(data, random):
    level_list = [
        {"enemies": [0x01, 0x08, 0x09, 0x3A], "start": 0xE077, "end": 0xE0BC},  # lv00
        {"enemies": [0x01, 0x08, 0x09, 0x3A], "start": 0xE955, "end": 0xE99D},  # lv17
        {"enemies": [0x08, 0x09, 0x3A], "start": 0xEA2F, "end": 0xEA7D},  # lv19
        {"enemies": [0x08, 0x09, 0x3A], "start": 0xEAA3, "end": 0xEACD},  # lv1B
        {"enemies": [0x1F, 0x20, 0x21, 0x22], "start": 0xE0BD, "end": 0xE123},  # lv01
        {"enemies": [0x44, 0x58], "start": 0xE124, "end": 0xE181},  # lv02
        {"enemies": [0x35, 0x3E, 0x40, 0x41, 0x42], "start": 0xE182, "end": 0xE1EE},  # lv03
        {"enemies": [0x33, 0x34, 0x5D], "start": 0xE1EF, "end": 0xE249},  # lv04
        {"enemies": [0x08, 0x39, 0x3A], "start": 0xE24A, "end": 0xE2A1},  # lv05
        {"enemies": [0x4D, 0x54, 0x55, 0x56, 0x5E, 0x5F], "start": 0xE30C, "end": 0xE384},  # lv07
        {"enemies": [0x4D, 0x57], "start": 0xE385, "end": 0xE3D3},  # lv08
        {"enemies": [0x01, 0x40, 0x4B], "start": 0xE432, "end": 0xE49B},  # lv0A
        {"enemies": [0x08, 0x09, 0x3A, 0x44, 0x4D], "start": 0xE49C, "end": 0xE4F9},  # lv0B
        {"enemies": [0x05, 0x06, 0x07, 0x08, 0x09, 0x0B, 0x3A, 0x3D], "start": 0xE5C2, "end": 0xE62B},  # lv0E
        {"enemies": [0x05, 0x39, 0x57, 0x5B], "start": 0xE706, "end": 0xE77B},  # lv11
        {"enemies": [0x5C, 0x5E, 0x5F], "start": 0xE7C8, "end": 0xE822},  # lv13
        {"enemies": [0x22, 0x23, 0x25, 0x27], "start": 0xE823, "end": 0xE88F},  # lv14
        {"enemies": [0x07, 0x33, 0x34, 0x3D, 0x5D], "start": 0xE890, "end": 0xE8F6},  # lv15
        {"enemies": [0x01, 0x08, 0x09, 0x34, 0x3A, 0x55], "start": 0xE8F7, "end": 0xE954},  # lv16
        {"enemies": [0x68, 0x69], "start": 0xE99E, "end": 0xEA2E},  # lv18a
        {"enemies": [0x6E, 0x6F], "start": 0xE99E, "end": 0xEA2E},  # lv18b
        {"enemies": [0x01, 0x09], "start": 0xEB55, "end": 0xEBB5}  # lv1F
    ]
    for level in level_list:
        i = level["start"]
        while i < level["end"]:
            sprite = sprite_extract(data[i], data[i+1])
            if data[i] == 0xFF:
                i -= 2
            elif sprite in level["enemies"]:
                randomize_sprite(data, random, level["enemies"], i)
            i += 3
    for i in range(0xE2A2, 0xE30B, 3):  # lvl06
        sprite = sprite_extract(data[i], data[i+1])
        if sprite == 0x4E:
            randomize_sprite(data, random, [0x4D, 0x4E, 0x51, 0x53], i)
        elif sprite == 0x4F:
            randomize_sprite(data, random, [0x4D, 0x4F, 0x51, 0x53], i)
        elif sprite in (0x4D, 0x51, 0x53):
            randomize_sprite(data, random, [0x4D, 0x51, 0x53], i)
    for i in range(0xE3D4, 0xE431, 3):  # lvl09
        sprite = sprite_extract(data[i], data[i + 1])
        if sprite == 0x4F:
            randomize_sprite(data, random, [0x4D, 0x4F, 0x53, 0x5A, 0x5C], i)
        elif sprite in (0x4D, 0x53, 0x5a, 0x5C):
            randomize_sprite(data, random, [0x4D, 0x53, 0x5A, 0x5C], i)
    for i in range(0xE4FA, 0xE560, 3):  # lvl0c
        sprite = sprite_extract(data[i], data[i + 1])
        if sprite == 0x49:
            randomize_sprite(data, random, [0x01, 0x47, 0x48, 0x49, 0x53], i)
        elif sprite in (0x01, 0x47, 0x48):
            randomize_sprite(data, random, [0x01, 0x47, 0x48, 0x53], i)
    for i in range(0xE561, 0xE5C1, 3):  # lvl0D
        sprite = sprite_extract(data[i], data[i + 1])
        if sprite == 0x43:
            randomize_sprite(data, random, [0x09, 0x43, 0x4D, 0x53], i)
        elif sprite == 0x4C:
            randomize_sprite(data, random, [0x09, 0x4C, 0x4D, 0x53], i)
        elif sprite in (0x09, 0x4D):
            randomize_sprite(data, random, [0x09, 0x4D, 0x53], i)
    for i in range(0xE6C0, 0xE705, 3):  # lvl10
        sprite = sprite_extract(data[i], data[i + 1])
        if sprite == 0x21:
            randomize_sprite(data, random, [0x01, 0x08, 0x20, 0x21, 0x3A, 0x55], i)
        elif sprite in (0x01, 0x08, 0x20, 0x3A, 0x55):
            randomize_sprite(data, random, [0x01, 0x08, 0x20, 0x3A, 0x55], i)
    for i in range(0xE77C, 0xE7C7, 3):  # lvl12
        sprite = sprite_extract(data[i], data[i + 1])
        if sprite == 0x4D:
            randomize_sprite(data, random, [0x4D, 0x58], i)
        elif sprite in (0x58, 0x5A):
            randomize_sprite(data, random, [0x4D, 0x58, 0x5A], i)
    # Thwomps in Wario's Castle
    for i in [0xE9D6, 0xE9D9, 0xE9DF, 0xE9E2, 0xE9E5]:
        data[i] = 0x34 if random.randint(0, 9) else 0x35
    # Piranha plants
    i = 0xE077
    while i < 0xEBB5:
        if i < 0xE30C or 0xE384 < i < 0xE3D4 or 0xE431 < i < 0xE8F7 or i > 0xE954:
            sprite = sprite_extract(data[i], data[i + 1])
            if data[i] == 0xFF:
                i -= 2
            elif sprite in (0x0C, 0x0D):
                copy_sprite(data, sprite_insert(data[i], data[i+1], random.choice([0x0C, 0x0D])), i)
        i += 3


def randomize_platforms(data, random):
    level_list = [
        {"platforms": [0x28, 0x29, 0x2A, 0x2B, 0x2D, 0x2E], "start": 0xE1EF, "end": 0xE249},
        {"platforms": [0x38, 0x3D], "start": 0xE24A, "end": 0xE2A1},
        {"platforms": [0x60, 0x61, 0x67], "start": 0xE99E, "end": 0xEA2E}
    ]
    for level in level_list:
        i = level["start"]
        while i < level["end"]:
            sprite = sprite_extract(data[i], data[i + 1])
            if sprite == 0xFF:
                i -= 2
            elif sprite in level["platforms"]:
                randomize_sprite(data, random, level["platforms"], i)
            i += 3
    for i in range(0xE9A3, 0xE9CE, 3):
        data[i] = (0x57 if data[i] == 0x5E else 0x38) + random.randint(0, 7)


def randomize_music(data, random):
    # overworld
    overworld_music_tracks = [0x05, 0x06, 0x0D, 0x0E, 0x10, 0x12, 0x1B, 0x1C, 0x1E]
    random.shuffle(overworld_music_tracks)
    for i, track in zip([0x3004F, 0x3EA9B, 0x3D186, 0x3D52B, 0x3D401, 0x3D297, 0x3D840, 0x3D694, 0x3D758],
                        overworld_music_tracks):
        data[i] = track
    # levels
    for i in range(0x5619, 0x5899, 0x14):
        data[i] = random.choice([0x01, 0x0B, 0x11, 0x13, 0x14, 0x17, 0x1D, 0x1F, 0x28])


def generate_output(self, output_directory: str):
    data = get_base_rom_bytes()
    base_patch = pkgutil.get_data(__name__, f'basepatch.bsdiff4')

    data = bytearray(bsdiff4.patch(data, base_patch))

    random = self.random

    if self.options.randomize_enemies:
        randomize_enemies(data, random)
    if self.options.randomize_platforms:
        randomize_platforms(data, random)
    if self.options.randomize_music:
        randomize_music(data, random)

    # if self.options.auto_scroll_trap:
    #     data[rom_addresses["Auto_Scroll_Disable"]] = 0xAF
    if self.options.shuffle_golden_coins:
        data[rom_addresses["Coin_Shuffle"]] = 0x40
    if self.options.shuffle_midway_bells:
        data[rom_addresses["Disable_Midway_Bell"]] = 0xC9

    if self.options.coinsanity:
        for section in ("A", "B"):
            for i in range(0, 30):
                data[rom_addresses[f"Coinsanity_{section}"] + i] = 0x00

    star_count = max(len([loc for loc in self.multiworld.get_filled_locations() if loc.item.player == self.player
                          and loc.item.name == "Super Star Duration Increase"]), 1)
    data[rom_addresses["Star_Count"]] = star_count // 256
    data[rom_addresses["Star_Count"] + 1] = star_count - (star_count // 256)
    if self.options.shuffle_golden_coins == "mario_coin_fragment_hunt":
        data[rom_addresses["Coins_Required"]] = self.coin_fragments_required // 256
        data[rom_addresses["Coins_Required"] + 1] = self.coin_fragments_required % 256
        data[rom_addresses["Required_Golden_Coins"]] = 6
    else:
        data[rom_addresses["Coins_Required"] + 1] = self.options.required_golden_coins.value
        data[rom_addresses["Required_Golden_Coins"]] = self.options.required_golden_coins.value
    data[rom_addresses["Midway_Bells"]] = self.options.shuffle_midway_bells.value
    data[rom_addresses["Energy_Link"]] = self.options.energy_link.value
    data[rom_addresses["Difficulty_Mode"]] = self.options.difficulty_mode.value
    data[rom_addresses["Coin_Mode"]] = self.options.shuffle_golden_coins.value

    for level, i in enumerate(self.auto_scroll_levels):
        # We set 0 if no auto scroll or auto scroll trap, so it defaults to no auto scroll. 1 if always or cancel items.
        data[rom_addresses["Auto_Scroll_Levels"] + level] = max(0, i - 1)
        data[rom_addresses["Auto_Scroll_Levels_B"] + level] = i

    if self.options.energy_link:
        # start with 1 life if Energy Link is on so that you don't deposit lives at the start of the game.
        data[rom_addresses["Starting_Lives"]] = 1

    rom_name = bytearray(f'AP{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}\0',
                         'utf8')[:21]
    rom_name.extend([0] * (21 - len(rom_name)))
    write_bytes(data, rom_name, 0x77777)

    outfilepname = f'_P{self.player}'
    outfilepname += f"_{self.multiworld.get_file_safe_player_name(self.player).replace(' ', '_')}" \
        if self.multiworld.player_name[self.player] != 'Player%d' % self.player else ''
    rompath = os.path.join(output_directory, f'AP_{self.multiworld.seed_name}{outfilepname}.gb')
    with open(rompath, 'wb') as outfile:
        outfile.write(data)
    patch = SuperMarioLand2DeltaPatch(os.path.splitext(rompath)[0] + SuperMarioLand2DeltaPatch.patch_file_ending,
                                      player=self.player, player_name=self.multiworld.player_name[self.player],
                                      patched_path=rompath)
    patch.write()
    os.unlink(rompath)


class SuperMarioLand2DeltaPatch(APDeltaPatch):
    hash = "a8413347d5df8c9d14f97f0330d67bce"
    patch_file_ending = ".apsml2"
    game = "Super Mario Land 2"
    result_file_ending = ".gb"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def get_base_rom_bytes():
    file_name = get_base_rom_path()
    with open(file_name, "rb") as file:
        base_rom_bytes = bytes(file.read())

    basemd5 = hashlib.md5()
    basemd5.update(base_rom_bytes)
    if SuperMarioLand2DeltaPatch.hash != basemd5.hexdigest():
        raise Exception("Supplied Base Rom does not match known MD5 for Super Mario Land 1.0. "
                        "Get the correct game and version, then dump it")
    return base_rom_bytes


def get_base_rom_path():
    file_name = get_settings()["sml2_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def write_bytes(data, byte_array, address):
    for byte in byte_array:
        data[address] = byte
        address += 1
