from ndspy import lz10
from Patch import APDeltaPatch, read_rom

import Utils
import os
import hashlib
import bsdiff4

from .BN3RomUtils import *  # We are literally going to use every single function from this

from .Items import ItemType

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
        self.references = ArchiveToReferences[offset]
        self.unused_indices = []  # A list of places it's okay to inject new scripts
        self.progressive_undernet_indices = []  # If this archive has progressive undernet, here they are in order

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
        self.scriptCount = (read_u16_le(self.uncompressedData, 0)) >> 1

        for i in range(0, self.scriptCount):
            start_offset = read_u16_le(self.uncompressedData, i * 2)
            next_offset = read_u16_le(self.uncompressedData, (i + 1) * 2)
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
            header.extend(int16_to_byte_list_le(byte_offset))
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

        return bytearray(byte_data)

    def inject_item_message(self, script_index, message_index, new_bytes):
        # First step, if the old message had any flag sets or flag clears, we need to keep them.
        # Mystery data has a flag set to actually remove the mystery data, and jobs often have a completion flag
        oldbytes = self.scripts[script_index].messageBoxes[message_index]
        for i in range(len(oldbytes)-3):
            # F2 00 is the code for "flagSet", with the two bytes after it being the flag to set.
            # F2 04 is the code for "flagClear", which also needs to come along for the ride
            # Add those to the message box after the other text.
            if oldbytes[i] == 0xF2 and (oldbytes[i+1] == 0x00 or oldbytes[i+1] == 0x04):
                flag = oldbytes[i:i+4]
                new_bytes.extend(flag)
        # Then, overwrite the existing script with the new one
        self.scripts[script_index].messageBoxes[message_index] = new_bytes

    def inject_into_rom(self, modified_rom_data):
        original_size = self.compressedSize if self.compressed else self.uncompressedSize

        working_data = self.generate_data(self.compressed)
        """
        with open("C:/Users/digiholic/Projects/BN3AP/randomized-archives/"+hex(self.startOffset)+".bin", "wb") as tempFile:
            tempFile.write(working_data)
        return modified_rom_data
        """
        if len(working_data) < original_size:
            # If it's shorter than the original data, we can pad the difference with FF and directrly replace
            working_data.extend([0x00] * (original_size - len(working_data)))
            modified_rom_data[self.startOffset:self.startOffset+len(working_data)] = working_data
        else:
            # It needs to start on a byte divisible by 4. If the rom data is not, add an FF
            while len(modified_rom_data) % 4 != 0:
                modified_rom_data.append(0xFF)
            new_start_offset = 0x08000000 + len(modified_rom_data)
            offset_byte = int32_to_byte_list_le(new_start_offset)
            modified_rom_data.extend(working_data)
            print("Archive "+hex(self.startOffset)+" is now at "+hex(new_start_offset)+" and is now length "+hex(len(working_data)))
            for offset in self.references:
                modified_rom_data[offset:offset+4] = offset_byte
        return modified_rom_data

    def add_progression_scripts(self):
        if len(self.unused_indices) < 9:
            # As far as I know, this should literally not be possible.
            # Every script I've looked at has dozens of unused indices, so finding 9 (8 plus one "ending" script)
            # should be no problem. We re-use these so we don't have to worry about an area getting tons of these
            raise "Error in generation -- not enough room for progressive undernet in archive "+self.startOffset
        for i in range(8): # There are 8 progressive undernet ranks
            new_script_index = self.unused_indices[i]
            new_script = ArchiveScript(new_script_index, generate_progressive_undernet(i, self.unused_indices[i+1]))
            self.scripts[new_script_index] = new_script
            self.progressive_undernet_indices.append(new_script_index)
        self.unused_indices = self.unused_indices[8:]  # Remove the first eight elements


class LocalRom:
    def __init__(self, file, patch=True, vanillaRom=None, name=None, hash=None):
        self.name = name
        self.hash = hash
        self.orig_buffer = None
        self.changed_archives = {}

        self.rom_data = bytearray(get_patched_rom_bytes(file))

    def get_data_chunk(self, start_offset, size):
        return self.rom_data[start_offset:start_offset + size]

    def replace_item(self, location, item):
        print("Replacing item at location "+location.name+" with "+item.itemName)
        offset = location.text_archive_address
        # If the archive is already loaded, use that
        if offset in self.changed_archives:
            archive = self.changed_archives[offset]
        else:
            is_compressed = offset in CompressedArchives
            size = ArchiveToSizeComp[offset] if is_compressed\
                else ArchiveToSizeUncomp[offset]
            data = self.get_data_chunk(offset, size)
            archive = TextArchive(data, offset, size, is_compressed)
            self.changed_archives[offset] = archive

        if item.type == ItemType.Undernet:
            if len(archive.progressive_undernet_indices) == 0:
                archive.add_progression_scripts() # Generate the new scripts
            # Replace the item text box as normal. We just also add a new jump at the end of the script
            item_bytes = generate_item_message(item)
            changed_script = archive.scripts[location.text_script_index]
            # There isn't a "Jump unconditional", so we fake one. Check flag 0 and jump
            # to the start of our progression regardless of outcome
            jump_to_first_undernet_bytes = [0xF3, 0x00,
                                            0x00, 0x00,
                                            archive.progressive_undernet_indices[0],
                                            archive.progressive_undernet_indices[0]]
            # Insert the new message second-to-last (the last index should be an end all by itself)
            changed_script.messageBoxes.insert(-1, jump_to_first_undernet_bytes)
            # item_bytes = jump_to_first_undernet_bytes
        elif item.type == ItemType.External:
            item_bytes = generate_external_item_message(item.name, item.recipient)
        else:
            item_bytes = generate_item_message(item)
        archive.inject_item_message(location.text_script_index, location.text_box_index,
                                    item_bytes)

    def write_changed_rom(self):
        for archive in self.changed_archives.values():
            self.rom_data = archive.inject_into_rom(self.rom_data)

    def write_to_file(self, out_path):
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


def get_patched_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = get_base_rom_bytes(file_name)
    patch_path = os.path.join(os.path.dirname(__file__), "data", "bn3-ap-patch.bsdiff")
    with open(patch_path, 'rb') as patch_file:
        patch_bytes = patch_file.read()
        patched_rom_bytes = bsdiff4.patch(base_rom_bytes, patch_bytes)
    return patched_rom_bytes
