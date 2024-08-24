
'''
Translates a provided list of boolean values into a bitmask.
Booleans are ordered from least-significant-bit to most-significant.
'''
def bitmask(*bools):
    result = 0
    for i,b in enumerate(bools):
        if b:
            result |= (1 << i)
    return result


'''
Unpacks the data in a byte into a tuple according to the provided
format string.

The format string is written in order from least-significant-bit
to most-significant.

Format chars:
    1-8   : a numeric value with the given number of bits
    b     : True if the bit is set, False otherwise
    x     : ignore this bit in the return data
'''
def unpack_byte(format, byte):
    result = []
    for f in format.lower():
        if f == 'x':
            byte = byte >> 1
        elif f == 'b':
            result.append(bool(byte & 1))
            byte = byte >> 1
        elif f >= '1' and f <= '8':
            size = ord(f) - ord('0')
            result.append(byte & ((1 << size) - 1))
            byte = byte >> size
        else:
            raise ValueError("Invalid format character '{}'".format(f))

    return tuple(result)

'''
Packs the given data into a byte according to the provided
format string; see unpack_byte for format description.
'''
def pack_byte(format, *values):
    values = list(values)
    result = 0
    shift = 0
    for f in format.lower():
        if f == 'x':
            shift += 1
        elif f == 'b':
            if values.pop(0):
                result |= (1 << shift)
            shift += 1
        elif f >= '1' and f <= '8':
            size = ord(f) - ord('0')
            result |= (values.pop(0) & ((1 << size) - 1)) << shift
            shift += size
        else:
            raise ValueError("Invalid format character '{}'".format(f))

    return result
