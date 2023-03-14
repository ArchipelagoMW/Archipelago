import struct
from struct import pack

kirby_flavor_presets = {
    3: {
        "1": "a6a6ed",
        "2": "e6e6fa",
        "3": "bcbcf2",
        "4": "8484e6",
        "5": "2929ec",
        "6": "b5b5f0",
        "7": "847bd6",
        "8": "3232d6",
        "9": "d6d6ef",
        "10": "4a52ef",
        "11": "c6c6e6",
        "12": "4343ad",
        "13": "9494ea",
        "14": "f6f6fd",
        "15": "3139b6",
    }
}


def rgb888_to_bgr555(color: str) -> bytes:
    col = int(color, 16)
    red = (col & 0xFF0000) >> 19
    green = (col & 0x00FF00) >> 11
    blue = (col & 0x0000FF) >> 3
    print(red, green, blue)
    outcol = (blue << 10) + (green << 5) + red
    print(hex(outcol))
    return struct.pack("H", outcol)
