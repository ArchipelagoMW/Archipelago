import hashlib
import io
import os
from io import BytesIO

from .JMP_Info_File import JMPInfoFile
from .Patching import *

from gclib import fs_helpers as fs
from gclib.gcm import GCM
from gclib.dol import DOL
from gclib.rarc import RARC
from gclib.yaz0_yay0 import Yay0

RANDOMIZER_NAME = "Luigi's Mansion"
CLEAN_LUIGIS_MANSION_ISO_MD5 = 0x6e3d9ae0ed2fbd2f77fa1ca09a60c494  # Based on the USA version of Luigi's Mansion

class InvalidCleanISOError(Exception): pass

class LuigisMansionRandomizer:
    def __init__(self, clean_iso_path, randomized_output_folder, export_disc_to_folder, output_data):
        # Takes note of the provided Randomized Folder path and if files should be exported instead of making an ISO.
        self.randomized_output_folder = randomized_output_folder
        self.export_disc_to_folder = export_disc_to_folder

        # Verifies we have a valid installation of Luigi's Mansion USA. There are some regional file differences.
        # After verifying, this will also read the entire iso, including system files and the content files
        self.verify_supported_version(clean_iso_path)
        self.gcm = GCM(clean_iso_path)
        self.gcm.read_entire_disc()

        # Find the main DOL file, which is the main file used for GC and Wii games.
        dol_data = self.gcm.read_file_data("sys/main.dol")
        self.dol = DOL()
        self.dol.read(dol_data)

        # Important note: SZP are just RARC / Arc files that are yay0 compressed, at least for Luigi's Mansion
        # Get Arc automatically handles decompressing RARC data from yay0, but compressing is on us later.
        main_mansion_file = self.get_arc("files/Map/map2.szp")

        # Uses custom class to load in JMP Info file entry (see more details in JMP_Info_File.py)

        # keyinfo
        key_info_entry = JMPInfoFile(main_mansion_file, 'keyinfo')
        update_key_info(key_info_entry, output_data)
        key_info_entry.update_info_file_bytes()
        main_mansion_file = self.update_rarc_info_entry(main_mansion_file, 'keyinfo', key_info_entry.info_file_entry.data)

        # iteminfotable
        item_info_table_entry = JMPInfoFile(main_mansion_file, 'iteminfotable')
        update_item_info_table(item_info_table_entry, output_data)
        item_info_table_entry.update_info_file_bytes()
        main_mansion_file = self.update_rarc_info_entry(main_mansion_file, 'iteminfotable', item_info_table_entry.info_file_entry.data)

        # itemappeartable
        item_appear_table_entry = JMPInfoFile(main_mansion_file, 'itemappeartable')
        update_item_appear_table(item_appear_table_entry, output_data)
        item_appear_table_entry.update_info_file_bytes()
        main_mansion_file = self.update_rarc_info_entry(main_mansion_file, 'itemappeartable', item_appear_table_entry.info_file_entry.data)

        # treasuretable
        treasure_table_entry = JMPInfoFile(main_mansion_file, 'treasuretable')
        update_treasure_table(treasure_table_entry, output_data)
        treasure_table_entry.update_info_file_bytes()
        main_mansion_file = self.update_rarc_info_entry(main_mansion_file, 'treasuretable', treasure_table_entry.info_file_entry.data)

        # furnitureinfo
        furniture_info_entry = JMPInfoFile(main_mansion_file, 'furnitureinfo')
        furniture_info_entry.update_info_file_bytes()
        main_mansion_file = self.update_rarc_info_entry(main_mansion_file, 'furnitureinfo', furniture_info_entry.info_file_entry.data)

        # characterinfo
        character_info_entry = JMPInfoFile(main_mansion_file, 'characterinfo')
        update_character_info(character_info_entry)
        character_info_entry.update_info_file_bytes()
        main_mansion_file = self.update_rarc_info_entry(main_mansion_file, 'characterinfo', character_info_entry.info_file_entry.data)

        # eventinfo
        event_info_entry = JMPInfoFile(main_mansion_file, 'eventinfo')
        update_event_info(event_info_entry)
        event_info_entry.update_info_file_bytes()
        main_mansion_file = self.update_rarc_info_entry(main_mansion_file, 'eventinfo', event_info_entry.info_file_entry.data)

        # observerinfo
        observer_info_entry = JMPInfoFile(main_mansion_file, 'observerinfo')
        update_observer_info(observer_info_entry)
        observer_info_entry.update_info_file_bytes()
        main_mansion_file = self.update_rarc_info_entry(main_mansion_file, 'observerinfo', observer_info_entry.info_file_entry.data)

        # generatorinfo
        generator_info_entry = JMPInfoFile(main_mansion_file, 'generatorinfo')
        update_generator_info(generator_info_entry)
        generator_info_entry.update_info_file_bytes()
        main_mansion_file = self.update_rarc_info_entry(main_mansion_file, 'generatorinfo', generator_info_entry.info_file_entry.data)

        # objinfo
        obj_info_entry = JMPInfoFile(main_mansion_file, 'objinfo')
        update_obj_info(obj_info_entry)
        obj_info_entry.update_info_file_bytes()
        main_mansion_file = self.update_rarc_info_entry(main_mansion_file, 'objinfo', obj_info_entry.info_file_entry.data)

        # Save the changes of the ARC / RARC file.
        main_mansion_file.save_changes()

        # As mentioned before, these szp files need to be compressed again in order to be properly read by Dolphin.
        # If you forget this, you will get an Invalid read error on a certain memory address typically.
        compressed_mansion_data = Yay0.compress(main_mansion_file.data, 0, False)
        self.gcm.changed_files["files/Map/map2.szp"] = compressed_mansion_data

        # Generator function to combine all necessary files into an ISO file.
        # Returned information is ignored. //Todo Maybe there is something better to put here?
        for next_progress_text, files_done in self.save_randomized_iso():
            continue
            # percentage_done = files_done/len(self.gcm.files_by_path)

    # Verify if the provided ISO file is a valid file extension and contains a valid Game ID.
    # Based on some similar code from (MIT License): https://github.com/LagoLunatic/wwrando
    def verify_supported_version(self, clean_iso_path):
        with open(clean_iso_path, "rb") as f:
            magic = fs.try_read_str(f, 0, 4)
            game_id = fs.try_read_str(f, 0, 6)
        print("Magic: " + str(magic) + "; Game ID: " + str(game_id))
        if magic == "CISO":
            raise InvalidCleanISOError(
                "The provided ISO is in CISO format. The %s randomizer only supports ISOs in ISO format." % RANDOMIZER_NAME)
        if game_id != "GLME01":
            if game_id and game_id.startswith("GLM"):
                raise InvalidCleanISOError(
                    "Invalid version of %s. Only the North American version is supported by this randomizer." % RANDOMIZER_NAME)
            else:
                raise InvalidCleanISOError(
                    "Invalid game given as the vanilla ISO. You must specify a %s ISO (North American version)." % RANDOMIZER_NAME)

    # Verify the MD5 hash matches the expectation of a USA-based ISO.
    # Based on some similar code from (MIT License): https://github.com/LagoLunatic/wwrando
    def verify_correct_clean_iso_md5(self, clean_iso_path):
        md5 = hashlib.md5()

        with open(clean_iso_path, "rb") as f:
            while True:
                chunk = f.read(1024 * 1024)
                if not chunk:
                    break
                md5.update(chunk)

        integer_md5 = int(md5.hexdigest(), 16)
        if integer_md5 != CLEAN_LUIGIS_MANSION_ISO_MD5:
            raise InvalidCleanISOError(
                f"Invalid vanilla {RANDOMIZER_NAME} ISO. Your ISO may be corrupted.\n\n" +
                f"Correct ISO MD5 hash: {CLEAN_LUIGIS_MANSION_ISO_MD5:x}\nYour ISO's MD5 hash: {integer_md5:x}"
            )

    # If Export to disc is true, Exports the entire file/directory contents of the ISO to specified folder
    # Otherwise, creates a direct ISO file.
    def save_randomized_iso(self):
        if self.export_disc_to_folder:
            output_folder_path = os.path.join(self.randomized_output_folder, "%s Randomized" % RANDOMIZER_NAME)
            yield from self.gcm.export_disc_to_folder_with_changed_files(output_folder_path)
        else:
            output_file_path = os.path.join(self.randomized_output_folder, "%s Randomized.iso" % RANDOMIZER_NAME)
            yield from self.gcm.export_disc_to_iso_with_changed_files(output_file_path)

    # Get an ARC / RARC / SZP file from within the ISO / ROM
    def get_arc(self, arc_path):
        arc_path = arc_path.replace("\\", "/")
        data = self.gcm.read_file_data(arc_path)
        arc = RARC(data)  # Automatically decompresses Yay0
        arc.read()
        return arc

    # Updates the existing ARC / RARC file with the provided data for a given info file entry.
    def update_rarc_info_entry(self, main_rarc_file: RARC, info_file_name: str, info_file_data: BytesIO):
        old_byte_data = io.BytesIO()

        for info_file in main_rarc_file.file_entries:
            if info_file.name == info_file_name:
                old_byte_data = info_file.data
                info_file.data = info_file_data
                break

        if old_byte_data.getvalue() == info_file_data.getvalue():
            print("No data update was performed for info file: " + info_file_name)

        return main_rarc_file