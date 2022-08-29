import re
import threading

double_cache_prevention = threading.Lock()


def checkval(val):
    if re.fullmatch(r"(?s)[\x00-\xff]?", str(val)) and not type(val) == int:
        return ord(val)
    return int(val)


def read_byte(offset):
    global rom_data
    return checkval(rom_data[offset])


def read_halfword(offset):
    global rom_data
    s = list(map(checkval, rom_data[offset:offset + 2]))
    result = 0
    for i in range(len(s)):
        result += s[i] << (i * 8)
    return result


def read_word(offset):
    global rom_data
    s = list(map(checkval, rom_data[offset:offset + 4]))
    result = 0
    for i in range(len(s)):
        result += s[i] << (i * 8)
    return result


def read_dblword(offset):
    global rom_data
    s = list(map(checkval, rom_data[offset:offset + 8]))
    result = 0
    for i in range(len(s)):
        result += s[i] << (i * 8)
        return result


def decompress_data(offset):
    global compressed_data_end
    decompressed_size = read_word(offset) >> 8;
    offset += 4
    output = []
    while len(output) < decompressed_size:
        flags = read_byte(offset)
        offset += 1
        for i in range(8):
            is_special = bool(flags & 0x80)
            if is_special:
                a = read_byte(offset)
                b = read_byte(offset+1)
                x_len = (a >> 4) + 3
                x_offset = (b + ((a & 0xf) << 8))
                start = len(output) - 1 - x_offset
                for j in range(x_len):
                    output.append(output[start + j])
                offset += 2
            else:
                output.append(read_byte(offset))
                offset += 1
            flags <<= 1;
    output = output[:decompressed_size]
    compressed_data_end = offset
    return ''.join(list(map(lambda x : chr(x), output)))


def compress_data(raw_data):
    ops = []
    i = 0
    data_len = len(raw_data)
    while i < data_len:
        lo = 2
        hi = min(18, len(raw_data) - i)
        start = max(0, i - 4096)
        last_match_ind = -1
        while lo < hi:
            mid = int((lo + hi + 1) / 2)
            ss = raw_data[i : i + mid]
            t = raw_data.find(ss, start)
            if t < i:
                # match found
                last_match_ind = t
                lo = mid
            else:
                hi = mid - 1
        if lo < 3:
            ops.append((0, ord(raw_data[i])))
            i += 1
        else:
            ops.append((i - last_match_ind, lo))
            i += lo
    # Add some padding
    n_padding = (8 - (len(ops) % 8)) % 8
    for i in range(n_padding):
        ops.append((0, 0))
    # Encode the string
    output = [0x10, data_len & 0xff, (data_len >> 8) & 0xff, (data_len >> 16) & 0xff]
    for i in range(0, len(ops), 8):
        flags = 0
        for j in range(8):
            flags <<= 1
            if ops[i + j][0] > 0:
                flags |= 1
        output.append(flags)
        for j in range(8):
            if ops[i + j][0] == 0:
                output.append(ops[i + j][1])
            else:
                o, l = ops[i + j]
                o -= 1
                l -= 3
                output.append( ((l & 0xf) << 4) + ((o >> 8) & 0xf) )
                output.append(o & 0xff)
    return ''.join(list(map(chr, output)))
