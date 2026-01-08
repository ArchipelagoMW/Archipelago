FILE_SIZE = 3145728

HEADER_SIZE = 0x200
HEADER_FILE_SIZE = FILE_SIZE + HEADER_SIZE

def get_sha256_hex(file_path):
    import hashlib
    BUFFER_SIZE = 65536

    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as rom_file:
        data = rom_file.read(BUFFER_SIZE)
        while data:
            sha256.update(data)
            data = rom_file.read(BUFFER_SIZE)

    return sha256.hexdigest()

def valid_rom_file(file_path):
    expected_sha256 = "0f51b4fca41b7fd509e4b8f9d543151f68efa5e97b08493e4b2a0c06f5d8d5e2"
    return get_sha256_hex(file_path) == expected_sha256
