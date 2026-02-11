def copy_gfx_tiles(original: bytearray, order: list[int], size: list[int]) -> bytearray:
    result = bytearray([])
    for x in range(len(order)):
        z = order[x] << size[0]
        result += bytearray([original[z+y] for y in range(size[1])])
    return result


def convert_rgb_to_snes(original: bytearray) -> bytearray:
    result = bytearray([])
    for i in range(int(len(original)/3)):
        red = original[i*3]>>3
        green = original[1+i*3]>>3
        blue = original[2+i*3]>>3
        color = red | (green<<5) | (blue<<10)
        result += bytearray([color & 0xFF, (color>>8) & 0xFF])
    return result


def convert_3bpp(decompressed_gfx: bytearray) -> bytearray:
    i = 0
    converted_gfx = bytearray([])
    while i < len(decompressed_gfx):
        converted_gfx += bytearray([decompressed_gfx[i+j] for j in range(16)])
        i += 16
        for j in range(8):
            converted_gfx += bytearray([decompressed_gfx[i]])
            converted_gfx += bytearray([0x00])
            i += 1
    return converted_gfx


def convert_name_to_4bpp(decompressed_gfx: bytearray) -> bytearray:
    i = 0
    converted_gfx = bytearray()
    while i < len(decompressed_gfx):
        converted_gfx += bytearray([decompressed_gfx[i+j] for j in range(16)])
        converted_gfx += bytearray([0x00 for _ in range(16)])
        i += 16

    # Decode GFX and swap palettes
    edited_gfx = bytearray([0x00 for _ in range(len(converted_gfx))])
    for i in range(len(converted_gfx)>>5):
        for j in range(8):
            for h in range(8):
                pixel = 0
                for l in range(2):
                    for k in range(2):
                        idx = (i*0x20)+(l*0x10)+(j*2)+k
                        if converted_gfx[idx] & (1<<(7-h)) != 0:
                            pixel = pixel|(1<<(l*2+k))
                if pixel:
                    pixel += 0x0A
                for l in range(2):
                    for k in range(2):
                        plane = l*2+k
                        bit = (pixel >> plane) & 0x01
                        if bit:
                            idx = (i*0x20)+(l*0x10)+(j*2)+k
                            edited_gfx[idx] |= (1<<(7-h))
    
    return edited_gfx


def copy_sprite_tiles(original, order, data_size, px_size = [5, 32]) -> bytearray:
    result = bytearray([0x00 for _ in range(data_size * 0x400)])
    offset = 0
    for x in range(len(order)):
        if x != 0 and x & 0x7 == 0:
            offset += 0x0200

        if type(order[x]) is int:
            z = order[x] << px_size[0]
            result[offset:offset+0x20] = original[z:z+px_size[1]]
            offset += 0x20
            z = order[x]+0x01 << px_size[0]
            result[offset:offset+0x20] = original[z:z+px_size[1]]
            offset += 0x1E0
            z = order[x]+0x10 << px_size[0]
            result[offset:offset+0x20] = original[z:z+px_size[1]]
            offset += 0x20
            z = order[x]+0x11 << px_size[0]
            result[offset:offset+0x20] = original[z:z+px_size[1]]
            offset -= 0x1E0
        else:
            z = order[x][0] << px_size[0]
            result[offset:offset+0x20] = original[z:z+px_size[1]]
            offset += 0x20
            z = order[x][1] << px_size[0]
            result[offset:offset+0x20] = original[z:z+px_size[1]]
            offset += 0x1E0
            z = order[x][2] << px_size[0]
            result[offset:offset+0x20] = original[z:z+px_size[1]]
            offset += 0x20
            z = order[x][3] << px_size[0]
            result[offset:offset+0x20] = original[z:z+px_size[1]]
            offset -= 0x1E0

    return result


def decompress_gfx(compressed_graphics: bytearray) -> bytearray:
    # This code decompresses graphics in LC_LZ2 format in order to be able to swap player and yoshi's graphics with ease.
    decompressed_gfx = bytearray([])
    i = 0
    while True:
        cmd = compressed_graphics[i]
        i += 1
        if cmd == 0xFF:
            break
        else:
            if (cmd >> 5) == 0x07:
                size = ((cmd & 0x03) << 8) + compressed_graphics[i] + 1
                cmd = (cmd & 0x1C) >> 2
                i += 1
            else:
                size = (cmd & 0x1F) + 1
                cmd = cmd >> 5
            if cmd == 0x00:
                decompressed_gfx += bytearray([compressed_graphics[i+j] for j in range(size)])
                i += size
            elif cmd == 0x01:
                byte_fill = compressed_graphics[i]
                i += 1
                decompressed_gfx += bytearray([byte_fill for j in range(size)])
            elif cmd == 0x02:
                byte_fill_1 = compressed_graphics[i]
                i += 1
                byte_fill_2 = compressed_graphics[i]
                i += 1
                for j in range(size):
                    if (j & 0x1) == 0x00:
                        decompressed_gfx += bytearray([byte_fill_1])
                    else:
                        decompressed_gfx += bytearray([byte_fill_2])
            elif cmd == 0x03:
                byte_read = compressed_graphics[i]
                i += 1
                decompressed_gfx += bytearray([(byte_read + j) for j in range(size)])
            elif cmd == 0x04:
                position = (compressed_graphics[i] << 8) + compressed_graphics[i+1]
                i += 2
                for j in range(size):
                    copy_byte = decompressed_gfx[position+j]
                    decompressed_gfx += bytearray([copy_byte])
    return decompressed_gfx
