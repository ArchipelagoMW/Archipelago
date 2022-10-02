from ndspy import lz10
from Patch import APDeltaPatch, read_rom

import BN3RomUtils
import Utils
import os
import hashlib

CHECKSUM_BLUE = "6fe31df0144759b34ad666badaacc442"

def list_contains_subsequence(lst, sublist) -> bool:
    sub_index = 0
    for index, item in enumerate(lst):
        if item == sublist[sub_index]:
            sub_index += 1
            if sub_index >= len(sublist):
                return True
        else:
            sub_index = 0
    return False


class ArchiveScript:
    def __init__(self, index, message_bytes):
        self.index = index
        self.messageBoxes = []

        message_box = []

        command_index = 0
        for byte in message_bytes:
            if command_index <= 0 and (byte == 0xE9 or byte == 0xE7):
                if byte == 0xE9:  # More textboxes to come, don't end it yet
                    message_box.append(byte)
                    self.messageBoxes.append(message_box)
                else:  # It's the end of the script, add another message to end it after this one
                    self.messageBoxes.append(message_box)
                    self.messageBoxes.append([0xE7])
                message_box = []

            else:
                # We can hit a command that might contain an E9 or an E7. If we do, skip checking the next 6 bytes
                if byte == 0xF6:
                    command_index = 7
                command_index -= 1
                message_box.append(byte)
        # If there's still bytes left over, add them even if we didn't hit an end
        if len(message_box) > 0:
            self.messageBoxes.append(message_box)

    def get_bytes(self):
        data = []
        for message in self.messageBoxes:
            data.extend(message)
        return data

    def __str__(self):
        s = str(self.index)+' - \n'
        for messageBox in self.messageBoxes:
            s += '  '+str(["{:02x}".format(x) for x in messageBox])+'\n'


class TextArchive:
    def __init__(self, data, offset, size, compressed=True):
        self.startOffset = offset
        self.compressed = compressed
        self.scripts = {}
        self.scriptCount = 0xFF
        self.references = BN3RomUtils.ArchiveToReferences[offset]
        self.unused_indices = []  # A list of places it's okay to inject new scripts

        if compressed:
            self.compressedSize = size
            self.compressedData = data
            self.uncompressedData = lz10.decompress(self.compressedData)
            self.uncompressedSize = len(self.uncompressedData)
        else:
            self.uncompressedSize = size
            self.uncompressedData = data
            self.compressedData = lz10.compress(self.uncompressedData)
            self.compressedSize = len(self.compressedData)
        self.scriptCount = (BN3RomUtils.read_u16_le(self.uncompressedData, 0)) >> 1

        for i in range(0, self.scriptCount):
            start_offset = BN3RomUtils.read_u16_le(self.uncompressedData, i * 2)
            next_offset = BN3RomUtils.read_u16_le(self.uncompressedData, (i + 1) * 2)
            if start_offset != next_offset:
                message_bytes = list(self.uncompressedData[start_offset:next_offset])
                message = ArchiveScript(i, message_bytes)
                self.scripts[i] = message
            else:
                self.unused_indices.append(i)

    def generate_data(self, compressed=True):
        header = []
        scripts = []
        byte_offset = self.scriptCount * 2
        for i in range(0, self.scriptCount):
            header.extend(BN3RomUtils.int16_to_byte_list_le(byte_offset))
            if i in self.scripts:
                script = self.scripts[i]
                scriptbytes = script.get_bytes()
                scripts.extend(scriptbytes)
                byte_offset += len(scriptbytes)

        data = []
        data.extend(header)
        data.extend(scripts)
        byte_data = bytes(data)
        if compressed:
            byte_data = lz10.compress(byte_data)

        return byte_data

    def inject_item_message(self, script_index, message_index, new_bytes):
        # First step, if the old message had any flag sets, we need to keep them.
        # Mystery data has a flag set to actually remove the mystery data, and jobs often have a completion flag
        oldbytes = self.scripts[script_index].messageBoxes[message_index]
        for i in range(len(oldbytes)-3):
            # F2 00 is the code for "flagSet", with the two bytes after it being the flag to set.
            # Add those to the message box after the other text.
            if oldbytes[i] == 0xF2 and oldbytes[i+1] == 0x00:
                flag = oldbytes[i:i+4]
                new_bytes.extend(flag)
        # Then, overwrite the existing script with the new one
        self.scripts[script_index].messageBoxes[message_index] = new_bytes

    def inject_into_rom(self, modified_rom_data):
        original_size = self.compressedSize if self.compressed else self.uncompressedSize

        working_data = self.generate_data(self.compressed)

        if len(working_data) < original_size:
            # If it's shorter than the original data, we can pad the difference with FF and directrly replace
            working_data.extend([0xFF] * (original_size - len(working_data)))
            modified_rom_data[self.startOffset:self.startOffset+len(working_data)] = working_data
        else:
            # It needs to start on an even byte. If the rom data is odd, add an FF
            if len(modified_rom_data) % 2 != 0:
                modified_rom_data.append(0xFF)
            new_start_offset = 0x08000000 + len(modified_rom_data)
            offset_byte = BN3RomUtils.int32_to_byte_list_le(new_start_offset)
            modified_rom_data.extend(working_data)
            for offset in self.references:
                modified_rom_data[offset:offset+4] = offset_byte
        return modified_rom_data

class LocalRom:
    def __init__(self, file, patch=True, vanillaRom=None, name=None, hash=None):
        self.name = name
        self.hash = hash
        self.orig_buffer = None
        self.changed_archives = {}

        # This should be the post-base-patch rom
        with open(file, 'rb') as stream:
            self.rom_data = read_rom(stream)

    def get_data_chunk(self, start_offset, size):
        return self.rom_data[start_offset:start_offset + size]

    def replace_item(self, location, item):
        offset = location.text_archive_address
        # If the archive is already loaded, use that
        if offset in self.changed_archives:
            archive = self.changed_archives[offset]
        else:
            is_compressed = offset in BN3RomUtils.CompressedArchives
            size = BN3RomUtils.ArchiveToSizeComp[offset] if is_compressed\
                else BN3RomUtils.ArchiveToSizeUncomp[offset]
            data = self.get_data_chunk(offset, size)
            archive = TextArchive(data, offset, size, is_compressed)
            self.changed_archives[offset] = archive

        if item.type == "External":
            item_bytes = BN3RomUtils.generate_external_item_message(item.name, item.recipient)
        else:
            item_bytes = BN3RomUtils.generate_item_message(item)
        archive.inject_item_message(location.text_script_index, location.text_box_index,
                                    item_bytes)

    def write_changed_rom(self):
        for archive in self.changed_archives.values():
            self.rom_data = archive.inject_into_rom(self.rom_data)

    def write_rom(self, out_path):
        with open(out_path, "wb") as rom:
            rom.write(self.rom_data)


class MMBN3DeltaPatch(APDeltaPatch):
    hash = CHECKSUM_BLUE
    game = "MegaMan Battle Network 3"
    patch_file_ending = ".bn3ap"
    result_file_ending = ".gba"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["mmbn3_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.local_path(file_name)
    return file_name


def get_base_rom_bytes(file_name: str = "") -> bytes:
    global rom_data
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(read_rom(open(file_name, "rb")))
        rom_data = base_rom_bytes

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if CHECKSUM_BLUE != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match US GBA Blue Version.'
                            'Please provide the correct ROM version')

        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes

"""
def read_rom(path: str = "") -> bytes:
    global rom_data
    global modified_rom_data

    with open(path, "rb") as rom:
        rom_bytes = rom.read()
        rom_data = bytearray(rom_bytes)
        modified_rom_data = bytearray(rom_data[:])
    return rom_bytes
"""