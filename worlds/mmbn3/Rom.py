from BaseClasses import ItemClassification
from worlds.Files import APDeltaPatch

import Utils
import os
import hashlib
import bsdiff4
from .lz10 import gba_decompress, gba_compress

from .BN3RomUtils import ArchiveToReferences, read_u16_le, read_u32_le, int16_to_byte_list_le, int32_to_byte_list_le, \
    generate_progressive_undernet, ArchiveToSizeComp, ArchiveToSizeUncomp, generate_item_message, \
    generate_external_item_message, generate_text_bytes, dictChar

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

        self.set_bytes(message_bytes)

    def get_bytes(self):
        data = []
        for message in self.messageBoxes:
            data.extend(message)
        return data

    def set_bytes(self, message_bytes):
        self.messageBoxes = []

        message_box = []
        # message_box_chars = []

        command_index = 0
        byte_index = 0
        for byte in message_bytes:
            byte_index += 1
            if command_index <= 0 and (byte == 0xE9 or byte == 0xE7):
                if byte == 0xE9:  # More textboxes to come, don't end it yet
                    message_box.append(byte)
                    # message_box_chars.append(hex(byte))
                    self.messageBoxes.append(message_box)
                else:  # It's the end of the script, add another message to end it after this one
                    self.messageBoxes.append(message_box)
                    self.messageBoxes.append([0xE7])

                message_box = []
                message_box_chars = []

            else:
                if command_index <= 0:
                    # We can hit a command that might contain an E9 or an E7. If we do, skip checking the next few bytes
                    if byte == 0xF6:  # CheckItem
                        command_index = 7
                    if byte == 0xF3:  # CheckFlag
                        # For whatever reason, the "Check Navi Customizer" command is one byte shorter than the other
                        # Check flags. If the next byte is 0x28, our command is only 5 bytes long.
                        if message_bytes[byte_index] == 0x28:
                            command_index = 5
                        else:
                            command_index = 6
                    if byte == 0xF2:  # FlagSet
                        command_index = 4
                command_index -= 1
                message_box.append(byte)
                # message_box_chars.append(dictChar[byte] if byte in dictChar else hex(byte))

        # If there's still bytes left over, add them even if we didn't hit an end
        if len(message_box) > 0:
            self.messageBoxes.append(message_box)

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

        self.text_changed = False

        if compressed:
            self.compressedSize = size
            self.compressedData = data
            self.uncompressedData = gba_decompress(self.compressedData)
            self.uncompressedSize = len(self.uncompressedData)
        else:
            self.uncompressedSize = size
            self.uncompressedData = data
            self.compressedData = gba_compress(self.uncompressedData)
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
            byte_data = gba_compress(byte_data)

        return bytearray(byte_data)

    def inject_item_message(self, script_index, message_indices, new_bytes):
        # First step, if the old message had any flag sets or flag clears, we need to keep them.
        # Mystery data has a flag set to actually remove the mystery data, and jobs often have a completion flag
        for message_index in message_indices:
            # print(hex(self.startOffset) + ": " + str(script_index) + " " + str(message_indices))
            oldbytes = self.scripts[script_index].messageBoxes[message_index]
            for i in range(len(oldbytes)-3):
                # F2 00 is the code for "flagSet", with the two bytes after it being the flag to set.
                # F2 04 is the code for "flagClear", which also needs to come along for the ride
                # Add those to the message box after the other text.
                if oldbytes[i] == 0xF2 and (oldbytes[i+1] == 0x00 or oldbytes[i+1] == 0x04):
                    flag = oldbytes[i:i+4]
                    new_bytes.extend(flag)

        first_message_index = message_indices[0]
        # Then, overwrite the existing script with the new one
        self.scripts[script_index].messageBoxes[first_message_index] = new_bytes
        for index in message_indices[1:]:
            self.scripts[script_index].messageBoxes[index] = []

    def inject_into_rom(self, modified_rom_data):
        working_data = self.generate_data(self.compressed)

        # It needs to start on a byte divisible by 4. If the rom data is not, add an FF
        while len(modified_rom_data) % 4 != 0:
            modified_rom_data.append(0xFF)
        new_start_offset = 0x08000000 + len(modified_rom_data)
        offset_byte = int32_to_byte_list_le(new_start_offset)
        modified_rom_data.extend(working_data)
        for offset in self.references:
            modified_rom_data[offset:offset+4] = offset_byte
        return modified_rom_data

    def add_progression_scripts(self):
        if len(self.unused_indices) < 9:
            # As far as I know, this should literally not be possible.
            # Every script I've looked at has dozens of unused indices, so finding 9 (8 plus one "ending" script)
            # should be no problem. We re-use these so we don't have to worry about an area getting tons of these
            raise AssertionError(f"Error in generation -- not enough room for progressive undernet in archive {self.startOffset} ({hex(self.startOffset)})")
        for i in range(9):  # There are 8 progressive undernet ranks
            new_script_index = self.unused_indices[i]
            new_script = ArchiveScript(new_script_index, generate_progressive_undernet(i, self.unused_indices[i+1]))
            self.scripts[new_script_index] = new_script
            self.progressive_undernet_indices.append(new_script_index)
        self.unused_indices = self.unused_indices[9:]  # Remove the first eight elements

    def inject_item_text(self, item_text, next_message=""):
        item_text_bytes = generate_text_bytes(item_text)
        next_message_bytes = generate_text_bytes(next_message)
        for script_index in self.scripts:
            script = self.scripts[script_index]
            # Loop through the bytes
            for message_index in range(0, len(script.messageBoxes)):
                oldbytes = self.scripts[script_index].messageBoxes[message_index]
                for i in range(0, len(oldbytes)-1):
                    if oldbytes[i] == 0x68 and oldbytes[i+1] == 0x68:
                        oldbytes[i:i+2] = item_text_bytes
                        self.text_changed = True

                        # If there's another text box to display, add it to the message bytes before setting them back
                        if len(next_message) > 0:
                            oldbytes.extend(next_message_bytes)
                            # TODO append end message nextline etc.
                            # I think this is "wait for button press" then "clearmessage"
                            oldbytes.extend([0xEB, 0xE9])
                        self.scripts[script_index].messageBoxes[message_index] = oldbytes


class LocalRom:
    def __init__(self, file, name=None):
        self.name = name
        self.changed_archives = {}

        self.rom_data = bytearray(get_patched_rom_bytes(file))

    def get_data_chunk(self, start_offset, size):
        if start_offset+size > len(self.rom_data):
            print("Attempting to get data chunk beyond the size of the ROM: "+hex(start_offset)+", ROM size ends at: "+hex(len(self.rom_data)))
        return self.rom_data[start_offset:start_offset + size]

    def replace_item(self, location, item):
        offset = location.text_archive_address
        # If the archive is already loaded, use that
        if offset in self.changed_archives:
            archive = self.changed_archives[offset]
        else:
            is_compressed = offset in ArchiveToSizeComp.keys()
            size = ArchiveToSizeComp[offset] if is_compressed\
                else ArchiveToSizeUncomp[offset]
            data = self.get_data_chunk(offset, size)
            # Check if the archive we want to load has been moved by the patch. This is indicated by a 0xFF 0xFF
            # as the first two bytes of the chunk

            if data[0] == 0xFF and data[1] == 0xFF:
                new_size_bytes = data[2:4]
                new_address_le = data[4:8]
                # Last byte should be zero since we're dealing with purely ROM address space
                new_address_le[3] = 0x0
                size = read_u16_le(new_size_bytes, 0)
                data = self.get_data_chunk(read_u32_le(new_address_le, 0), size)


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
            item_bytes = generate_external_item_message(item.itemName, item.recipient)
        else:
            item_bytes = generate_item_message(item)
        archive.inject_item_message(location.text_script_index, location.text_box_indices,
                                    item_bytes)


    def insert_hint_text(self, location, short_text, long_text = ""):
        """
        Replaces the placeholder text in this location's archive with short_text,
        gives another text box for long_text if it's present
        """

        # Replace item name placeholders
        if location.inject_name:
            offset = location.text_archive_address
            # If the archive is already loaded, use that
            if offset in self.changed_archives:
                archive = self.changed_archives[offset]
            else:
                # It should be theoretically impossible to call insert_hint_text before actually injecting the item.
                raise AssertionError("Inserting a hint at a location that doesn't have an item!")
            archive.inject_item_text(short_text, long_text)


    def inject_name(self, player):
        authname = player
        authname = authname+('\x00' * (63 - len(player)))
        self.rom_data[0x7FFFC0:0x7FFFFF] = bytes(authname, 'utf8')

    def write_changed_rom(self):
        for archive in self.changed_archives.values():
            self.rom_data = archive.inject_into_rom(self.rom_data)

    def write_to_file(self, out_path):
        with open(out_path, "wb") as rom:
            rom.write(self.rom_data)


class MMBN3DeltaPatch(APDeltaPatch):
    hash = CHECKSUM_BLUE
    game = "MegaMan Battle Network 3"
    patch_file_ending = ".apbn3"
    result_file_ending = ".gba"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def get_base_rom_path(file_name: str = "") -> str:
    if not file_name:
        from worlds.mmbn3 import MMBN3World
        bn3_options = MMBN3World.settings

        if bn3_options is None:
            file_name = "Mega Man Battle Network 3 - Blue Version (USA).gba"
        else:
            file_name = bn3_options["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_name, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if CHECKSUM_BLUE != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match US GBA Blue Version.'
                            'Please provide the correct ROM version')

        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_patched_rom_bytes(file_name: str = "") -> bytes:
    """
    Gets the patched ROM data generated from applying the ap-patch diff file to the provided ROM.
    Diff patch generated by https://github.com/digiholic/bn3-ap-patch
    Which should contain all changed text banks and assembly code
    """
    import pkgutil
    base_rom_bytes = get_base_rom_bytes(file_name)
    patch_bytes = pkgutil.get_data(__name__, "data/bn3-ap-patch.bsdiff")
    patched_rom_bytes = bsdiff4.patch(base_rom_bytes, patch_bytes)
    return patched_rom_bytes
