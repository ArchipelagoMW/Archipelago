

def write_bytes(data, byte_array, address):
    for byte in byte_array:
        data[address] = byte
        address += 1
