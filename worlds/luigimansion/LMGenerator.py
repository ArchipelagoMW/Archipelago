import hashlib
import os
import io

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
        self.clean_iso_path = clean_iso_path
        self.randomized_output_folder = randomized_output_folder
        self.export_disc_to_folder = export_disc_to_folder
        self.output_data = output_data

        # Verifies we have a valid installation of Luigi's Mansion USA. There are some regional file differences.
        # After verifying, this will also read the entire iso, including system files and the content files
        self.__verify_supported_version()
        self.gcm = GCM(clean_iso_path)
        self.gcm.read_entire_disc()

        # Find the main DOL file, which is the main file used for GC and Wii games.
        dol_data = self.gcm.read_file_data("sys/main.dol")
        self.dol = DOL()
        self.dol.read(dol_data)

        # Important note: SZP are just RARC / Arc files that are yay0 compressed, at least for Luigi's Mansion
        # Get Arc automatically handles decompressing RARC data from yay0, but compressing is on us later.
        self.map_two_file = self.get_arc("files/Map/map2.szp")

        # Loads all the specific JMP tables AP may potentially change / update.
        # Although some events are not changed by AP directly, they are changed here to remove un-necessary cutscenes,
        # set certain flag values, and remove un-necessary script tags.
        self.jmp_item_info_table = self.load_maptwo_info_table("iteminfotable")
        self.jmp_item_appear_table = self.load_maptwo_info_table("itemappeartable")
        self.jmp_treasure_table = self.load_maptwo_info_table("treasuretable")
        self.jmp_furniture_info_table = self.load_maptwo_info_table("furnitureinfo")
        self.jmp_character_info_table = self.load_maptwo_info_table("characterinfo")
        self.jmp_event_info_table = self.load_maptwo_info_table("eventinfo")
        self.jmp_observer_info_table = self.load_maptwo_info_table("observerinfo")
        self.jmp_key_info_table = self.load_maptwo_info_table("keyinfo")

        # Saves the randomized iso file, with all files updated.
        self.save_randomized_iso()

    # Verify if the provided ISO file is a valid file extension and contains a valid Game ID.
    # Based on some similar code from (MIT License): https://github.com/LagoLunatic/wwrando
    def __verify_supported_version(self):
        with open(self.clean_iso_path, "rb") as f:
            magic = fs.try_read_str(f, 0, 4)
            game_id = fs.try_read_str(f, 0, 6)
        print("Magic: " + str(magic) + "; Game ID: " + str(game_id))
        if magic == "CISO":
            raise InvalidCleanISOError(f"The provided ISO is in CISO format. The {RANDOMIZER_NAME} randomizer " +
                                       "only supports ISOs in ISO format.")
        if game_id != "GLME01":
            if game_id and game_id.startswith("GLM"):
                raise InvalidCleanISOError(f"Invalid version of {RANDOMIZER_NAME}. " +
                                           "Only the North American version is supported by this randomizer.")
            else:
                raise InvalidCleanISOError("Invalid game given as the vanilla ISO. You must specify a " +
                      "%s ISO (North American version)." % RANDOMIZER_NAME)
        self.__verify_correct_clean_iso_md5()

    # Verify the MD5 hash matches the expectation of a USA-based ISO.
    # Based on some similar code from (MIT License): https://github.com/LagoLunatic/wwrando
    def __verify_correct_clean_iso_md5(self):
        md5 = hashlib.md5()
        with open(self.clean_iso_path, "rb") as f:
            while True:
                chunk = f.read(1024 * 1024)
                if not chunk:
                    break
                md5.update(chunk)

        integer_md5 = int(md5.hexdigest(), 16)
        if integer_md5 != CLEAN_LUIGIS_MANSION_ISO_MD5:
            raise InvalidCleanISOError(
                f"Invalid vanilla {RANDOMIZER_NAME} ISO. Your ISO may be corrupted.\n" +
                f"Correct ISO MD5 hash: {CLEAN_LUIGIS_MANSION_ISO_MD5:x}\nYour ISO's MD5 hash: {integer_md5:x}")

    # Get an ARC / RARC / SZP file from within the ISO / ROM
    def get_arc(self, arc_path):
        arc_path = arc_path.replace("\\", "/")
        data = self.gcm.read_file_data(arc_path)
        arc = RARC(data)  # Automatically decompresses Yay0
        arc.read()
        return arc

    # Uses custom class to load in JMP Info file entry (see more details in JMP_Info_File.py)
    def load_maptwo_info_table(self, jmp_table_name: str):
        jmp_table_entry = JMPInfoFile(self.map_two_file, jmp_table_name)
        jmp_table_entry.print_header_info()
        return jmp_table_entry

    # Updates the existing ARC / RARC file with the provided data for a given info file entry.
    def update_maptwo_info_table(self, jmp_info_file: JMPInfoFile):
        jmp_info_file.update_info_file_bytes()

        for jmp_file in self.map_two_file.file_entries:
            if jmp_file.name == jmp_info_file.info_file_entry.name:
                jmp_file.data = jmp_info_file.info_file_entry.data
                break

    # Updates various DOL Offsets per the desired changes of the AP user
    def update_dol_offsets(self):
        return
        # Walk Speed
        # self.dol.data.seek(0x396538)
        # self.dol.data.write(struct.pack(">H", 16850))

        # Vac Speed
        # data_test = [0x38, 0x00, 0x00, 0x0F]
        # self.dol.data.seek(0x7EA28)
        # self.dol.data.write(struct.pack(">BBBB", *data_test))

        # Turn off pickup animations
        # self.dol.seek(0xCD39B)
        # self.dol.write_data(struct.pack(">B", [0x01])

    # Updates all jmp tables in the map2.szp file.
    def update_maptwo_jmp_tables(self):
        update_item_info_table(self.jmp_item_info_table, self.output_data)
        self.update_maptwo_info_table(self.jmp_item_info_table)

        update_item_appear_table(self.jmp_item_appear_table, self.output_data)
        self.update_maptwo_info_table(self.jmp_item_appear_table)

        update_treasure_table(self.jmp_treasure_table, self.output_data)
        self.update_maptwo_info_table(self.jmp_treasure_table)

        update_furniture_info(self.jmp_furniture_info_table, self.jmp_item_appear_table, self.output_data)
        self.update_maptwo_info_table(self.jmp_furniture_info_table)

        update_character_info(self.jmp_character_info_table)
        self.update_maptwo_info_table(self.jmp_character_info_table)

        update_event_info(self.jmp_event_info_table)
        self.update_maptwo_info_table(self.jmp_event_info_table)

        update_observer_info(self.jmp_observer_info_table)
        self.update_maptwo_info_table(self.jmp_observer_info_table)

        update_key_info(self.jmp_key_info_table, self.output_data)
        self.update_maptwo_info_table(self.jmp_key_info_table)

    def save_randomized_iso(self):
        self.update_maptwo_jmp_tables()

        # Save the map two file changes
        # As mentioned before, these szp files need to be compressed again in order to be properly read by Dolphin/GC.
        # If you forget this, you will get an Invalid read error on a certain memory address typically.
        self.map_two_file.save_changes()
        self.gcm.changed_files["files/Map/map2.szp"] = Yay0.compress(self.map_two_file.data, 0)

        # Save the changes of main.dol
        self.update_dol_offsets()
        self.dol.save_changes()
        self.gcm.changed_files["sys/main.dol"] = self.dol.data

        # Update all custom events
        list_events = [4, 17, 22, 32, 48, 50, 64]
        for custom_event in list_events:
            self.update_custom_event(str(custom_event), True)

        # Generator function to combine all necessary files into an ISO file.
        # Returned information is ignored. //Todo Maybe there is something better to put here?
        for _, _ in self.export_files_from_memory():  # next_progress_text, files_done
            continue # percentage_done = files_done/len(self.gcm.files_by_path)

    # If Export to disc is true, Exports the entire file/directory contents of the ISO to specified folder
    # Otherwise, creates a direct ISO file.
    def export_files_from_memory(self):
        if self.export_disc_to_folder:
            output_folder_path = os.path.join(self.randomized_output_folder, "%s Randomized" % RANDOMIZER_NAME)
            yield from self.gcm.export_disc_to_folder_with_changed_files(output_folder_path)
        else:
            output_file_path = os.path.join(self.randomized_output_folder, "%s Randomized.iso" % RANDOMIZER_NAME)
            yield from self.gcm.export_disc_to_iso_with_changed_files(output_file_path)

    def update_custom_event(self, event_number: str, check_local_folder: bool, non_local_str=""):
        if check_local_folder and not non_local_str:
            raise Exception("If the custom event does not exist in the local data folder, an event string must be " +
                            "provided to overwrite an existing event.")

        custom_event = self.get_arc("files/Event/event" + event_number + ".szp")

        custom_event_entry = next((info_files for info_files in custom_event.file_entries if
                                        info_files.name == "event" + event_number + ".txt"), None)

        if custom_event_entry is None:
            raise Exception("Unable to find an info file with name 'event48.txt' in provided RAC file.")

        if check_local_folder:
            with open('data/custom_events/event' + event_number + '.txt', 'rb') as file:
                lines = io.BytesIO(file.read())
        else:
            lines = io.BytesIO(non_local_str.encode('utf-8'))

        next((info_files for info_files in custom_event.file_entries if
              info_files.name == "event" + event_number + ".txt")).data = lines

        custom_event.save_changes()
        self.gcm.changed_files["files/Event/event" + event_number + ".szp"] = (
            Yay0.compress(custom_event.data, 0))