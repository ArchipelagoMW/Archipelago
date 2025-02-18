from ..backgroundEditor import BackgroundEditor
from .aesthetics import rgb_to_bin, bin_to_rgb, prepatch
import copy
CHAR_MAP = {'z': 0x3E, '-': 0x3F, '.': 0x39, ':': 0x42, '?': 0x3C, '!': 0x3D}

def _encode(s):
    result = bytearray()
    for char in s:
        if ord("A") <= ord(char) <= ord("Z"):
            result.append(ord(char) - ord("A"))
        elif ord("a") <= ord(char) <= ord("y"):
            result.append(ord(char) - ord("a") + 26)
        elif ord("0") <= ord(char) <= ord("9"):
            result.append(ord(char) - ord("0") + 0x70)
        else:
            result.append(CHAR_MAP.get(char, 0x7E))
    return result


def setRomInfo(rom, patch_data):
    seed_name = patch_data["seed_name"]
    try:
        seednr = int(patch_data["seed"], 16)
    except:
        import hashlib
        seednr = int(hashlib.md5(str(patch_data["seed"]).encode()).hexdigest(), 16)

    if patch_data["is_race"]:
        seed_name = "Race"
        if isinstance(patch_data["is_race"], str):
            seed_name += " " + patch_data["is_race"]
        rom.patch(0x00, 0x07, "00", "01")
    else:
        rom.patch(0x00, 0x07, "00", "52")

    line_1_hex = _encode(seed_name[:20])
    #line_2_hex = _encode(seed[16:])
    BASE_DRAWING_AREA = 0x98a0
    LINE_WIDTH = 0x20
    player_id_text = f"Player {patch_data['player']}:"
    for n in (3, 4):
        be = BackgroundEditor(rom, n)
        ba = BackgroundEditor(rom, n, attributes=True)

        for n, v in enumerate(_encode(player_id_text)):
            be.tiles[BASE_DRAWING_AREA + LINE_WIDTH * 5 + 2 + n] = v
            ba.tiles[BASE_DRAWING_AREA + LINE_WIDTH * 5 + 2 + n] = 0x00
        for n, v in enumerate(_encode(patch_data['player_name'])):
            be.tiles[BASE_DRAWING_AREA + LINE_WIDTH * 6 + 0x13 - len(patch_data['player_name']) + n] = v
            ba.tiles[BASE_DRAWING_AREA + LINE_WIDTH * 6 + 0x13 - len(patch_data['player_name']) + n] = 0x00
        for n, v in enumerate(line_1_hex):
            be.tiles[0x9a20 + n] = v
            ba.tiles[0x9a20 + n] = 0x00

        for n in range(0x09, 0x14):
            be.tiles[0x9820 + n] = 0x7F
            be.tiles[0x9840 + n] = 0xA0 + (n % 2)
            be.tiles[0x9860 + n] = 0xA2
        sn = seednr
        for n in range(0x0A, 0x14):
            tilenr = sn % 30
            sn //= 30
            if tilenr > 12:
                tilenr += 2
            if tilenr > 16:
                tilenr += 1
            if tilenr > 19:
                tilenr += 3
            if tilenr > 27:
                tilenr += 1
            if tilenr > 29:
                tilenr += 2
            if tilenr > 35:
                tilenr += 1
            be.tiles[0x9800 + n] = tilenr * 2
            be.tiles[0x9820 + n] = tilenr * 2 + 1
            pal = sn % 8
            sn //= 8
            ba.tiles[0x9800 + n] = 0x08 | pal
            ba.tiles[0x9820 + n] = 0x08 | pal
        be.store(rom)
        ba.store(rom)

def setTitleGraphics(rom):    
    BASE = 0x9800
    ROW_SIZE = 0x20

    be = BackgroundEditor(rom, 0x11, attributes=True)
    for tile in be.tiles:
        if be.tiles[tile] == 7:
            be.tiles[tile] = 3
        
    be.tiles[BASE + 10 * ROW_SIZE + 8] = 7
    be.tiles[BASE + 10 * ROW_SIZE + 10] = 2
    be.tiles[BASE + 10 * ROW_SIZE + 11] = 5
    be.tiles[BASE + 11 * ROW_SIZE + 10] = 6
    be.tiles[BASE + 11 * ROW_SIZE + 11] = 6
    be.tiles[BASE + 12 * ROW_SIZE + 11] = 6
    be.tiles[BASE + 11 * ROW_SIZE + 9] = 1
    be.tiles[BASE + 12 * ROW_SIZE + 9] = 1
    be.tiles[BASE + 12 * ROW_SIZE + 10] = 1
    be.tiles[BASE + 13 * ROW_SIZE + 9] = 1
    be.tiles[BASE + 13 * ROW_SIZE + 10] = 1
    
    be.store(rom)

    SKIP_INTRO = True
    if SKIP_INTRO:
        # Skip intro as it's causing problems
        rom.banks[1][0x2F5B : 0x2F5B + 3] = [0xC3, 0x39, 0x6E]
        # Disable initial music
        rom.banks[1][0x2F03 : 0x2F03 + 5] = [0] * 5
        # Disable music fade on reset
        rom.banks[1][0x3436 : 0x3436 + 3] = [0] * 3
    

    # Set egg palette
    BASE = 0x3DEE
    palettes = []
    BANK = 0x21
    for i in range(8):
        palette = []
        for c in range(4):
            address = BASE + i * 8 + c * 2
            packed = (rom.banks[BANK][address + 1] << 8) | rom.banks[BANK][address]
            r,g,b = bin_to_rgb(packed)
            palette.append([r, g, b])
        palettes.append(palette)

    for i in [1, 2, 5, 6, 7]:
        palettes[i] = copy.copy(palettes[3])
    
    def to_5_bit(r, g, b):
        return [r >> 3, g >> 3, b >> 3]

    palettes[1][3] = to_5_bit(0xFF, 0x80, 145)
    palettes[2][2] = to_5_bit(119, 198, 155)
    palettes[5][3] = to_5_bit(119, 198, 155)
    palettes[6][3] = to_5_bit(192, 139, 215)
    palettes[7][3] = to_5_bit(229, 196, 139)
    
    for i in range(8):
        for c in range(4):
            address = BASE + i * 8 + c * 2
            packed = rgb_to_bin(*palettes[i][c])
            rom.banks[BANK][address] = packed & 0xFF
            rom.banks[BANK][address + 1] = packed >> 8
