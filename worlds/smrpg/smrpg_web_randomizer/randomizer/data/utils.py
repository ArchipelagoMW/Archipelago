def color_to_bytes(color):
    color_int = int(color, 16)
    r = color_int >> 19
    g = (color_int >> 10) & 0x3E
    b = (color_int >> 1) & 0x7C

    byte_1 = r + ((g << 4) & 0xF0)
    byte_2 = b + (g >> 4)
    return [byte_1, byte_2]

def palette_to_bytes(colors):
    ret = []
    for color in colors:
        ret += color_to_bytes(color)
    return ret
