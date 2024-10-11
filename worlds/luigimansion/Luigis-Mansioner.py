import hashlib
import os
import re
import io

from gclib import fs_helpers as fs
from gclib.gcm import GCM
from gclib.dol import DOL
from gclib.rarc import RARC
from gclib.yaz0_yay0 import Yay0

RANDOMIZER_NAME = "Luigis Mansion"

INTEGER_BYTE_LENGTH = 4
IMPORTANT_HEADER_BYTE_LENGTH = 16
ITEM_INFO_STRING_SIZE = 16

class InvalidCleanISOError(Exception): pass

class LuigisMansionRandomizer:
    CLEAN_LUIGIS_MANSION_ISO_MD5 = 0x6e3d9ae0ed2fbd2f77fa1ca09a60c494 # Based on the USA version of Luigi's Mansion

    def __init__(self, clean_iso_path, randomized_output_folder, export_disc_to_folder):
        self.randomized_output_folder = randomized_output_folder
        self.export_disc_to_folder = export_disc_to_folder

        self.arcs_by_path: dict[str, RARC] = {}

        # Verifies we have a valid installation of Luigi's Mansion USA. There are some regional file differences,
        # however I didn't read too much into it.
        # Additionally, Reads the entire iso, including system files and the content files
        self.verify_supported_version(clean_iso_path)
        self.gcm = GCM(clean_iso_path)
        self.gcm.read_entire_disc()

        # Find the mail DOL file, which is the main file used for GC and Wii games.
        dol_data = self.gcm.read_file_data("sys/main.dol")
        self.dol = DOL()
        self.dol.read(dol_data)

        # Important note: SZP are just RARC / Arc files that are yay0 compressed, at least for Luigi's Mansion
        # Get Arc automatically handles decompressing RARC data from yay0, but compressing it back is on you.
        main_mansion_file = self.get_arc("files/Map/map2.szp")

        # Typically infofiles have a series of bytes that provide metadata about the file itself. Some of that data interpretation is currently unknown
        # First 4 bytes (integer) give the total lines available in the file.
        # Second 4 bytes (integer) give us the number of fields per data line.
        # The next 4 bytes (integer) give us the header size of the file, in bytes
        # The next 4 bytes (integer) tell us the size of the data lines themselves in bytes.
        # Based on the data line size, the bytes would need to be split into their logical fields.
        # Based on review of the files manually, info table for instance is 16 bytes long for strings, and 4 bytes for the integers.
        # There are two string fields, 3 integer fields, totalling 44 bytes per data line.
        item_infofile_fileentry = next((info_files for info_files in main_mansion_file.file_entries if info_files.name == 'iteminfotable'), None)

        mapdata = item_infofile_fileentry.data.read()
        line_count, field_count, header_size, line_size = (int.from_bytes(mapdata[i:i+INTEGER_BYTE_LENGTH]) for i in range(0, IMPORTANT_HEADER_BYTE_LENGTH, INTEGER_BYTE_LENGTH))

        print("Line Count: " + str(line_count) + "; Field Count: " + str(field_count) + "; Header Byte Length: " + str(header_size) + "; Data Line Length: " + str(line_size))

        # These are bytes I didn't bother trying to decompile. For our purposes, they largely seem irrevelant and do not need to be updated.
        extra_header_bytes = mapdata[IMPORTANT_HEADER_BYTE_LENGTH:header_size]

        # Stores the actual data lines (and their properties), along with the end file terminator.
        # For ItemInfoTable I just saw that there was @ signs and at least 10 near each other at a minimum, so that's what I chose to use to capture. Could be changed to something more concrete.
        items_data_lines = []
        end_info_string_terminator = ""

        for data_line in range(header_size, len(mapdata), line_size):
            current_line = mapdata[data_line:data_line+line_size]
            if bool(re.search("@{10,}", str(current_line))):
                end_info_string_terminator = current_line
                break

            # First 32 bits are strings that are utf8 encoded, along with most strings in these szp files.
            # Through testing, I figured out that char_name is not just a model that is used to display when the item appears (thats what it looks like when you view everything because so many things define charactername as key01).
            # Instead, this is a reference to the actual item as well. Changing a key for instance to "mletter" made the model change AND act as Mario's actual letter, thus ignoring any other effects of the key.
            name, char_name = (current_line[i:i+16].decode('utf-8').rstrip('\x00').split("\x00")[0] for i in range(0, ITEM_INFO_STRING_SIZE*2, ITEM_INFO_STRING_SIZE))
            open_door_no, hp_amt, is_escape =(int.from_bytes(current_line[i:i + INTEGER_BYTE_LENGTH]) for i in range(ITEM_INFO_STRING_SIZE*2, len(current_line), INTEGER_BYTE_LENGTH))

            # Add all of these data points to the collection
            items_data_lines.append({
                'name': name,
                'char_name': char_name,
                'open_door_no': open_door_no,
                'hp_amt': hp_amt,
                'is_escape': is_escape
            })

        # Iterate through a provided dict and append to table. Need to determine best method to change treasure/furniture/ghost tables
        # Make a function for each table we will need to touch (iteminfotable, itemappeartable, furnitureinfo, treasuretable, keyinfo(?), iyapootable)
        # For demo purposes I added two new lines.
        items_data_lines.append({
            'name': "boots_test",
            'char_name': "key01",
            'open_door_no': 0,
            'hp_amt': 0,
            'is_escape': 0
        })

        items_data_lines.append({
            'name': "jake_test",
            'char_name': "key01",
            'open_door_no': 0,
            'hp_amt': 0,
            'is_escape': 0
        })

        # Ensure that the original line count we extracted from the header gets updated as well. Could just use the collection size/count variable but its the same result here.
        line_count += 2

        # Confirms we have the same amount of lines extracted vs the amount we were told by the file header.
        # print("Header data line amount: '" + str(line_count) + "' vs data line count extracted: '" + str(len(items_data_lines)) + "'")

        # Begin concatinating all of the bytes back together, to prepare writing back to the SZP file.
        # Include the extra, unmodified header bits, as they contain other important information other files may be using.
        # Ensure everything is converted to bytes though, as that was the original format the file contained. I changed it from bytes mostly for readability / debugging purposes.
        items_byte_data_updated = line_count.to_bytes(INTEGER_BYTE_LENGTH) + field_count.to_bytes(INTEGER_BYTE_LENGTH) + header_size.to_bytes(INTEGER_BYTE_LENGTH) + line_size.to_bytes(INTEGER_BYTE_LENGTH) + extra_header_bytes

        for data_line in items_data_lines:
            items_byte_data_updated += self.string_to_bytes(str(data_line['name']), ITEM_INFO_STRING_SIZE)
            items_byte_data_updated += self.string_to_bytes(str(data_line['char_name']), ITEM_INFO_STRING_SIZE)
            items_byte_data_updated += data_line['open_door_no'].to_bytes(INTEGER_BYTE_LENGTH)
            items_byte_data_updated += data_line['hp_amt'].to_bytes(INTEGER_BYTE_LENGTH)
            items_byte_data_updated += data_line['is_escape'].to_bytes(INTEGER_BYTE_LENGTH)

        # This indicates the file is complete and no new data will appear afterwords.
        items_byte_data_updated += end_info_string_terminator

        # Updates the original data of the file entry back to a BytesIO object, as thats what the data started as and the data property expects.
        next((info_files for info_files in main_mansion_file.file_entries if info_files.name == 'iteminfotable'), None).data = io.BytesIO(items_byte_data_updated)
        # print(next((info_files for info_files in main_mansion_file.file_entries if info_files.name == 'iteminfotable'), None).data.read())

        # Save the changes of the ARC / RARC file.
        main_mansion_file.save_changes()

        # As mentioned before, these szp files need to be compressed again in order to be properly read by Dolphin.
        # If you forget this, you will get a Invalid read error on a certain memory address typically.
        compressed_mainsion_data = Yay0.compress(main_mansion_file.data)
        self.gcm.changed_files["files/Map/map2.szp"] = compressed_mainsion_data

        # Not quite sure how this works, but I understand it is a generator function. Without this being a loop, an ISO will not be created.
        # I don't do any information with next progress text or percentage done variable I created. Maybe there is something better to put here.
        for next_progress_text, files_done in self.save_randomized_iso():
            percentage_done = files_done/len(self.gcm.files_by_path)

        # Unimplemented Code was just there for checking other files
        # treasureInfoFileEntry = next((info_files for info_files in main_mansion_file.file_entries if info_files.name == 'treasuretable'), None)

    def verify_supported_version(self, clean_iso_path):
        with open(clean_iso_path, "rb") as f:
            magic = fs.try_read_str(f, 0, 4)
            game_id = fs.try_read_str(f, 0, 6)
        print("Magic: " + str(magic) + "; game_id: " + str(game_id))
        if magic == "CISO":
            raise InvalidCleanISOError("The provided ISO is in CISO format. The %s randomizer only supports ISOs in ISO format." % RANDOMIZER_NAME)
        if game_id != "GLME01":
            if game_id and game_id.startswith("GLM"):
                raise InvalidCleanISOError("Invalid version of %s. Only the North American version is supported by this randomizer." % RANDOMIZER_NAME)
            else:
                raise InvalidCleanISOError("Invalid game given as the vanilla ISO. You must specify a %s ISO (North American version)." % RANDOMIZER_NAME)

    def verify_correct_clean_iso_md5(self, clean_iso_path):
        md5 = hashlib.md5()
    
        with open(clean_iso_path, "rb") as f:
            while True:
                chunk = f.read(1024*1024)
                if not chunk:
                    break
                md5.update(chunk)
    
        integer_md5 = int(md5.hexdigest(), 16)
        if integer_md5 != self.CLEAN_LUIGIS_MANSION_ISO_MD5:
            raise InvalidCleanISOError(
                "Invalid vanilla {RANDOMIZER_NAME} ISO. Your ISO may be corrupted.\n\n"
                f"Correct ISO MD5 hash: {self.CLEAN_LUIGIS_MANSION_ISO_MD5:x}\nYour ISO's MD5 hash: {integer_md5:x}"
            )

    def save_randomized_iso(self):
        # Exports the entire contents of both the system files and content files to a folder on your machine, where you specified. Otherwise, creates an ISO file.
        if self.export_disc_to_folder:
            output_folder_path = os.path.join(self.randomized_output_folder, "%s Randomized" % RANDOMIZER_NAME)
            yield from self.gcm.export_disc_to_folder_with_changed_files(output_folder_path)
        else:
            output_file_path = os.path.join(self.randomized_output_folder, "%s Randomized.iso" % RANDOMIZER_NAME)
            yield from self.gcm.export_disc_to_iso_with_changed_files(output_file_path)

    def get_arc(self, arc_path):
        arc_path = arc_path.replace("\\", "/")

        if arc_path in self.arcs_by_path:
            return self.arcs_by_path[arc_path]
        else:
            data = self.gcm.read_file_data(arc_path)
            arc = RARC(data) # Automatically decompresses Yay0
            arc.read()
            self.arcs_by_path[arc_path] = arc
            return arc

    def string_to_bytes(self, user_string, n):
        # Encode the string using UTF-8 encoding
        encoded_string = user_string.encode('utf-8')

        # If the encoded string is smaller than n, pad it with null bytes
        if len(encoded_string) < n:
            encoded_string += b'\x00' * (n - len(encoded_string))

        # If the encoded string is larger than n, truncate it
        elif len(encoded_string) > n:
            encoded_string = encoded_string[:n]

        return encoded_string


if __name__ == '__main__':
    unpacked_iso = LuigisMansionRandomizer("Full\\Path\\To\\Clean\\Luigis Mansion (USA).iso", "Desired\\Output\\Path", False)
