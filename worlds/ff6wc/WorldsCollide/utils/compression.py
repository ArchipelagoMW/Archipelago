WINDOW_SIZE = 0x800
WINDOW_START = 0x7de # why start here?

MIN_MULTI_LENGTH = 3
MAX_MULTI_LENGTH = 34
MAX_COMPRESS_SIZE = 2 ** 16 - 1

def compress(data):
    result = []
    data_index = 0

    group = []
    control_byte = 0
    control_bit = 1

    byte_positions = {} # lists of sorted positions each byte occurs at
    window_indices = {} # start indices of byte_positions within current window
    for index, byte in enumerate(data):
        if byte in byte_positions:
            byte_positions[byte].append(index)
        else:
            byte_positions[byte] = [index]
            window_indices[byte] = 0

    while data_index < len(data):
        longest_length = 0
        longest_start = 0

        start_byte = data[data_index]
        for x in range(window_indices[start_byte], len(byte_positions[start_byte])):
            position = byte_positions[start_byte][x]

            if position >= data_index:
                # window has not reached position yet, skip the rest of the positions
                break
            if position < data_index - WINDOW_SIZE:
                # position is no longer within the window, increment window index for this byte and go to next position
                window_indices[start_byte] += 1
                continue

            try:
                length = 1
                while length < MAX_MULTI_LENGTH and data[data_index + length] == data[position + length]:
                    length += 1
            except IndexError:
                pass

            if length > longest_length:
                longest_length = length
                longest_start = position
                if length == MAX_MULTI_LENGTH:
                    break

        if longest_length >= MIN_MULTI_LENGTH:
            length_start = ((longest_start + WINDOW_START) % WINDOW_SIZE) | ((longest_length - MIN_MULTI_LENGTH) << 11)
            group.extend(list(length_start.to_bytes(2, "little")))
            data_index += longest_length
        else:
            control_byte = control_byte | control_bit
            group.append(data[data_index])
            data_index += 1

        control_bit <<= 1
        if control_bit > 0xff:
            result.append(control_byte)
            result.extend(group)
            control_byte = 0
            control_bit = 1
            group = []

    result.append(control_byte)
    result.extend(group)

    size = len(result) + 2
    if size > MAX_COMPRESS_SIZE:
        print(f"Error: compress: data too large (compressed size {size} > 65535)")
        size = MAX_COMPRESS_SIZE
    return list(size.to_bytes(2, "little")) + result

def decompress(data):
    window = [0] * WINDOW_SIZE
    window_index = WINDOW_START

    result = []
    data_index = 2 # first two bytes should be len(data)
    assert int.from_bytes(data[ : data_index], byteorder = "little") == len(data)
    while data_index < len(data):
        control_byte = data[data_index]
        data_index += 1

        control_bit = 1
        while control_bit <= 0xff and data_index < len(data):
            if control_bit & control_byte:
                # copy single value from data
                value = data[data_index]
                data_index += 1
                result.append(value)
                window[window_index] = value
                window_index = (window_index + 1) % WINDOW_SIZE
            else:
                # copy multiple values from window
                length_start = int.from_bytes(data[data_index : data_index + 2], byteorder = "little")
                data_index += 2

                length = (length_start >> 11) + MIN_MULTI_LENGTH
                start = length_start % WINDOW_SIZE
                for position in range(start, start + length):
                    value = window[position % WINDOW_SIZE]
                    result.append(value)
                    window[window_index] = value
                    window_index = (window_index + 1) % WINDOW_SIZE
            control_bit <<= 1
    return result
