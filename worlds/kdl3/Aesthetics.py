import struct
from struct import pack




def rgb888_to_bgr555(color:str) -> bytes:
    col = int(color, 16)
    red = (col & 0xFF0000) >> 19
    green = (col & 0x00FF00) >> 11
    blue = (col & 0x0000FF) >> 3
    print(red, green, blue)
    outcol = (blue << 10) + (green << 5) + red
    print(hex(outcol))
    return struct.pack("H", outcol)
