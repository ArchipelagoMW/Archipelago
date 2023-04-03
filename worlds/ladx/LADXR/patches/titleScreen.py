from ..backgroundEditor import BackgroundEditor
import subprocess
import binascii


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


def setRomInfo(rom, seed, seed_name, settings, player_name, player_id):
    try:
        seednr = int(seed, 16)
    except:
        import hashlib
        seednr = int(hashlib.md5(seed).hexdigest(), 16)

    if settings.race:
        seed_name = "Race"
        if isinstance(settings.race, str):
            seed_name += " " + settings.race
        rom.patch(0x00, 0x07, "00", "01")
    else:
        rom.patch(0x00, 0x07, "00", "52")

    line_1_hex = _encode(seed_name[:20])
    #line_2_hex = _encode(seed[16:])
    BASE_DRAWING_AREA = 0x98a0
    LINE_WIDTH = 0x20
    player_id_text = f"Player {player_id}:"
    for n in (3, 4):
        be = BackgroundEditor(rom, n)
        ba = BackgroundEditor(rom, n, attributes=True)

        for n, v in enumerate(_encode(player_id_text)):
            be.tiles[BASE_DRAWING_AREA + LINE_WIDTH * 5 + 2 + n] = v
            ba.tiles[BASE_DRAWING_AREA + LINE_WIDTH * 5 + 2 + n] = 0x00
        for n, v in enumerate(_encode(player_name)):
            be.tiles[BASE_DRAWING_AREA + LINE_WIDTH * 6 + 0x13 - len(player_name) + n] = v
            ba.tiles[BASE_DRAWING_AREA + LINE_WIDTH * 6 + 0x13 - len(player_name) + n] = 0x00
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
