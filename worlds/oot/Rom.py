import json
import os
import platform
import struct
import subprocess
import copy
import threading
from .Utils import subprocess_args, data_path, get_version_bytes, __version__
from Utils import user_path
from .ntype import BigStream
from .crc import calculate_crc

DMADATA_START = 0x7430

double_cache_prevention = threading.Lock()

class Rom(BigStream):
    original = None

    def __init__(self, file=None, force_use=False):
        super().__init__([])

        self.changed_address = {}
        self.changed_dma = {}
        self.force_patch = []

        if file is None:
            return

        decomp_file = user_path('ZOOTDEC.z64')

        with open(data_path('generated/symbols.json'), 'r') as stream:
            symbols = json.load(stream)
            self.symbols = {name: int(addr, 16) for name, addr in symbols.items()}

        # If decompressed file already exists, read from it
        if not force_use:
            if os.path.exists(decomp_file):
                file = decomp_file

            if file == '':
                # if not specified, try to read from the previously decompressed rom
                file = decomp_file
                try:
                    self.read_rom(file)
                except FileNotFoundError:
                    # could not find the decompressed rom either
                    raise FileNotFoundError('Must specify path to base ROM')
            else:
                self.read_rom(file)
        else:
            self.read_rom(file)

        # decompress rom, or check if it's already decompressed
        self.decompress_rom_file(file, decomp_file, force_use)

        # Add file to maximum size
        self.buffer.extend(bytearray([0x00] * (0x4000000 - len(self.buffer))))
        with double_cache_prevention:
            if not self.original:
                Rom.original = self.copy()

        # Add version number to header.
        self.write_bytes(0x35, get_version_bytes(__version__))
        self.force_patch.extend([0x35, 0x36, 0x37])

    def copy(self):
        new_rom = Rom()
        new_rom.buffer = copy.copy(self.buffer)
        new_rom.changed_address = copy.copy(self.changed_address)
        new_rom.changed_dma = copy.copy(self.changed_dma)
        new_rom.force_patch = copy.copy(self.force_patch)
        return new_rom

    def decompress_rom_file(self, file, decomp_file, skip_crc_check):
        validCRC = [
            [0xEC, 0x70, 0x11, 0xB7, 0x76, 0x16, 0xD7, 0x2B],  # Compressed
            [0x70, 0xEC, 0xB7, 0x11, 0x16, 0x76, 0x2B, 0xD7],  # Byteswap compressed
            [0x93, 0x52, 0x2E, 0x7B, 0xE5, 0x06, 0xD4, 0x27],  # Decompressed
        ]

        # Validate ROM file
        file_name = os.path.splitext(file)
        romCRC = list(self.buffer[0x10:0x18])
        if romCRC not in validCRC and not skip_crc_check:
            # Bad CRC validation
            raise RuntimeError('ROM file %s is not a valid OoT 1.0 US ROM.' % file)
        elif len(self.buffer) < 0x2000000 or len(self.buffer) > (0x4000000) or file_name[1].lower() not in ['.z64',
                                                                                                            '.n64']:
            # ROM is too big, or too small, or not a bad type
            raise RuntimeError('ROM file %s is not a valid OoT 1.0 US ROM.' % file)
        elif len(self.buffer) == 0x2000000:
            # If Input ROM is compressed, then Decompress it

            sub_dir = data_path("Decompress")

            if platform.system() == 'Windows':
                subcall = [sub_dir + "\\Decompress.exe", file, decomp_file]
            elif platform.system() == 'Linux':
                if platform.uname()[4] == 'aarch64' or platform.uname()[4] == 'arm64':
                    subcall = [sub_dir + "/Decompress_ARM64", file, decomp_file]
                else:
                    subcall = [sub_dir + "/Decompress", file, decomp_file]
            elif platform.system() == 'Darwin':
                subcall = [sub_dir + "/Decompress.out", file, decomp_file]
            else:
                raise RuntimeError(
                    'Unsupported operating system for decompression. Please supply an already decompressed ROM.')

            if not os.path.exists(subcall[0]):
                raise RuntimeError(f'Decompressor does not exist! Please place it at {subcall[0]}.')
            subprocess.call(subcall, **subprocess_args())
            self.read_rom(decomp_file)
        else:
            # ROM file is a valid and already uncompressed
            pass

    def write_byte(self, address, value):
        super().write_byte(address, value)
        self.changed_address[self.last_address - 1] = value

    def write_bytes(self, address, values):
        super().write_bytes(address, values)
        self.changed_address.update(zip(range(address, address + len(values)), values))

    def restore(self):
        self.buffer = copy.copy(self.original.buffer)
        self.changed_address = {}
        self.changed_dma = {}
        self.force_patch = []
        self.last_address = None
        self.write_bytes(0x35, get_version_bytes(__version__))
        self.force_patch.extend([0x35, 0x36, 0x37])

    def sym(self, symbol_name):
        return self.symbols.get(symbol_name)

    def write_to_file(self, file):
        self.verify_dmadata()
        self.update_header()
        with open(file, 'wb') as outfile:
            outfile.write(self.buffer)

    def update_header(self):
        crc = calculate_crc(self)
        self.write_bytes(0x10, crc)

    def read_rom(self, file):
        # "Reads rom into bytearray"
        try:
            with open(file, 'rb') as stream:
                self.buffer = bytearray(stream.read())
        except FileNotFoundError as ex:
            raise FileNotFoundError('Invalid path to Base ROM: "' + file + '"')

    # dmadata/file management helper functions

    def _get_dmadata_record(self, cur):
        start = self.read_int32(cur)
        end = self.read_int32(cur + 0x04)
        size = end - start
        return start, end, size

    def get_dmadata_record_by_key(self, key):
        cur = DMADATA_START
        dma_start, dma_end, dma_size = self._get_dmadata_record(cur)
        while True:
            if dma_start == 0 and dma_end == 0:
                return None
            if dma_start == key:
                return dma_start, dma_end, dma_size
            cur += 0x10
            dma_start, dma_end, dma_size = self._get_dmadata_record(cur)

    def verify_dmadata(self):
        cur = DMADATA_START
        overlapping_records = []
        dma_data = []

        while True:
            this_start, this_end, this_size = self._get_dmadata_record(cur)

            if this_start == 0 and this_end == 0:
                break

            dma_data.append((this_start, this_end, this_size))
            cur += 0x10

        dma_data.sort(key=lambda v: v[0])

        for i in range(0, len(dma_data) - 1):
            this_start, this_end, this_size = dma_data[i]
            next_start, next_end, next_size = dma_data[i + 1]

            if this_end > next_start:
                overlapping_records.append(
                    '0x%08X - 0x%08X (Size: 0x%04X)\n0x%08X - 0x%08X (Size: 0x%04X)' % \
                    (this_start, this_end, this_size, next_start, next_end, next_size)
                )

        if len(overlapping_records) > 0:
            raise Exception("Overlapping DMA Data Records!\n%s" % \
                            '\n-------------------------------------\n'.join(overlapping_records))

    # update dmadata record with start vrom address "key"
    # if key is not found, then attempt to add a new dmadata entry
    def update_dmadata_record(self, key, start, end, from_file=None):
        cur, dma_data_end = self.get_dma_table_range()
        dma_index = 0
        dma_start, dma_end, dma_size = self._get_dmadata_record(cur)
        while dma_start != key:
            if dma_start == 0 and dma_end == 0:
                break

            cur += 0x10
            dma_index += 1
            dma_start, dma_end, dma_size = self._get_dmadata_record(cur)

        if cur >= (dma_data_end - 0x10):
            raise Exception('dmadata update failed: key {0:x} not found in dmadata and dma table is full.'.format(key))
        else:
            self.write_int32s(cur, [start, end, start, 0])
            if from_file == None:
                if key == None:
                    from_file = -1
                else:
                    from_file = key
            self.changed_dma[dma_index] = (from_file, start, end - start)

    def get_dma_table_range(self):
        cur = DMADATA_START
        dma_start, dma_end, dma_size = self._get_dmadata_record(cur)
        while True:
            if dma_start == 0 and dma_end == 0:
                raise Exception('Bad DMA Table: DMA Table entry missing.')

            if dma_start == DMADATA_START:
                return (DMADATA_START, dma_end)

            cur += 0x10
            dma_start, dma_end, dma_size = self._get_dmadata_record(cur)

    # This will scan for any changes that have been made to the DMA table
    # This assumes any changes here are new files, so this should only be called
    # after patching in the new files, but before vanilla files are repointed
    def scan_dmadata_update(self):
        cur = DMADATA_START
        dma_data_end = None
        dma_index = 0
        dma_start, dma_end, dma_size = self._get_dmadata_record(cur)
        old_dma_start, old_dma_end, old_dma_size = self.original._get_dmadata_record(cur)

        while True:
            if (dma_start == 0 and dma_end == 0) and \
                    (old_dma_start == 0 and old_dma_end == 0):
                break

            # If the entries do not match, the flag the changed entry
            if not (dma_start == old_dma_start and dma_end == old_dma_end):
                self.changed_dma[dma_index] = (-1, dma_start, dma_end - dma_start)

            cur += 0x10
            dma_index += 1
            dma_start, dma_end, dma_size = self._get_dmadata_record(cur)
            old_dma_start, old_dma_end, old_dma_size = self.original._get_dmadata_record(cur)

    # gets the last used byte of rom defined in the DMA table
    def free_space(self):
        cur = DMADATA_START
        max_end = 0

        while True:
            this_start, this_end, this_size = self._get_dmadata_record(cur)

            if this_start == 0 and this_end == 0:
                break

            max_end = max(max_end, this_end)
            cur += 0x10
        max_end = ((max_end + 0x0F) >> 4) << 4
        return max_end


def compress_rom_file(input_file, output_file):
    compressor_path = "."

    if platform.system() == 'Windows':
        executable_path = "Compress.exe"
    elif platform.system() == 'Linux':
        if platform.uname()[4] == 'aarch64' or platform.uname()[4] == 'arm64':
            executable_path = "Compress_ARM64"
        else:
            executable_path = "Compress"
    elif platform.system() == 'Darwin':
        executable_path = "Compress.out"
    else:
        raise RuntimeError('Unsupported operating system for compression.')
    compressor_path = os.path.join(compressor_path, executable_path)
    if not os.path.exists(compressor_path):
        raise RuntimeError(f'Compressor does not exist! Please place it at {compressor_path}.')
    import logging
    logging.info(subprocess.check_output([compressor_path, input_file, output_file],
                                             **subprocess_args(include_stdout=False)))
