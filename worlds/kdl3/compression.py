def hal_decompress(comp: bytes) -> bytes:
    """
    HAL decompression based on exhal by devinacker
    https://github.com/devinacker/exhal
    """
    inpos = 0

    inval = 0
    output = bytearray()
    while inval != 0xFF:
        remaining = 65536 - inpos
        if remaining < 1:
            return bytes()
        inval = comp[inpos]
        inpos += 1
        if inval == 0xFF:
            break
        if (inval & 0xE0) == 0xE0:
            command = (inval >> 2) & 0x07
            length = (((inval & 0x03) << 8) | comp[inpos]) + 1
            inpos += 1
        else:
            command = inval >> 5
            length = (inval & 0x1F) + 1
        if (command == 2 and ((len(output) + 2*length) > 65536)) or (len(output) + length) > 65536:
            return bytes()
        if command == 0:
            output.extend(comp[inpos:inpos+length])
            inpos += length
        elif command == 1:
            output.extend([comp[inpos] for _ in range(length)])
            inpos += 1
        elif command == 2:
            output.extend([comp[x] for _ in range(length) for x in (inpos, inpos+1)])
            inpos += 2
        elif command == 3:
            output.extend([comp[inpos] + i for i in range(length)])
            inpos += 1
        elif command == 4 or command == 7:
            offset = (comp[inpos] << 8) | comp[inpos + 1]
            if (offset + length) > 65536:
                return bytes()
            output.extend(output[offset:offset+length])
            inpos += 2
        elif command == 5:
            offset = (comp[inpos] << 8) | comp[inpos + 1]
            if (offset + length) > 65536:
                return bytes()
            output.extend([int('{:08b}'.format(x)[::-1], 2) for x in output[offset:offset+length]])
            inpos += 2
        elif command == 6:
            offset = (comp[inpos] << 8) | comp[inpos + 1]
            if offset < length - 1:
                return bytes()
            output.extend([output[offset - x] for x in range(length)])
            inpos += 2
    return bytes(output)
