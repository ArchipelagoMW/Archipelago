import hashlib
import os

from JMP_Info_File import JMPInfoFile

from gclib import fs_helpers as fs
from gclib.gcm import GCM
from gclib.dol import DOL
from gclib.rarc import RARC
from gclib.yaz0_yay0 import Yay0

RANDOMIZER_NAME = "Luigis Mansion"
CLEAN_LUIGIS_MANSION_ISO_MD5 = 0x6e3d9ae0ed2fbd2f77fa1ca09a60c494 # Based on the USA version of Luigi's Mansion

class InvalidCleanISOError(Exception): pass

class LuigisMansionRandomizer:

    def __init__(self, clean_iso_path, randomized_output_folder, export_disc_to_folder):
        # Takes note of the provided Randomized Folder path and if files should be exported instead of making an ISO.
        self.clean_iso_path = clean_iso_path
        self.randomized_output_folder = randomized_output_folder
        self.export_disc_to_folder = export_disc_to_folder

        # Verifies we have a valid installation of Luigi's Mansion USA. There are some regional file differences.
        # After verifying, this will also read the entire iso, including system files and the content files
        self.__verify_supported_version()
        self.gcm = GCM(clean_iso_path)
        self.gcm.read_entire_disc()

        # Collections of GC file types
        self.arcs_by_path: dict[str, RARC] = {}

        # Find the main DOL file, which is the main file used for GC and Wii games.
        dol_data = self.gcm.read_file_data("sys/main.dol")
        self.dol = DOL()
        self.dol.read(dol_data)

        # Important note: SZP are just RARC / Arc files that are yay0 compressed, at least for Luigi's Mansion
        # Get Arc automatically handles decompressing RARC data from yay0, but compressing is on us later.
        self.map_two_file = self.get_arc("files/Map/map2.szp")

        self.jmp_item_info_table = self.load_maptwo_info_table("iteminfotable")
        self.jmp_item_appear_table = self.load_maptwo_info_table("itemappeartable")
        self.jmp_treasure_table = self.load_maptwo_info_table("treasuretable")
        self.jmp_furniture_info_table = self.load_maptwo_info_table("furnitureinfo")
        self.jmp_character_info_table = self.load_maptwo_info_table("characterinfo")
        self.jmp_event_info_table = self.load_maptwo_info_table("eventinfo")
        self.jmp_observer_info_table = self.load_maptwo_info_table("observerinfo")

    # Verify if the provided ISO file is a valid file extension and contains a valid Game ID.
    # Based on some similar code from (MIT License): https://github.com/LagoLunatic/wwrando
    def __verify_supported_version(self):
        with open(self.clean_iso_path, "rb") as f:
            magic = fs.try_read_str(f, 0, 4)
            game_id = fs.try_read_str(f, 0, 6)
        print("Magic: " + str(magic) + "; Game ID: " + str(game_id))
        if magic == "CISO":
            raise InvalidCleanISOError("The provided ISO is in CISO format. The %s randomizer only supports ISOs in ISO format." % RANDOMIZER_NAME)
        if game_id != "GLME01":
            if game_id and game_id.startswith("GLM"):
                raise InvalidCleanISOError("Invalid version of %s. Only the North American version is supported by this randomizer." % RANDOMIZER_NAME)
            else:
                raise InvalidCleanISOError("Invalid game given as the vanilla ISO. You must specify a %s ISO (North American version)." % RANDOMIZER_NAME)
        self.__verify_correct_clean_iso_md5()

    # Verify the MD5 hash matches the expectation of a USA-based ISO.
    # Based on some similar code from (MIT License): https://github.com/LagoLunatic/wwrando
    def __verify_correct_clean_iso_md5(self):
        md5 = hashlib.md5()
        with open(self.clean_iso_path, "rb") as f:
            while True:
                chunk = f.read(1024*1024)
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

        if arc_path in self.arcs_by_path:
            return self.arcs_by_path[arc_path]
        else:
            data = self.gcm.read_file_data(arc_path)
            arc = RARC(data) # Automatically decompresses Yay0
            arc.read()
            self.arcs_by_path[arc_path] = arc
            return arc

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

    # If Export to disc is true, Exports the entire file/directory contents of the ISO to specified folder
    # Otherwise, creates a direct ISO file.
    def save_randomized_iso(self):
        self.update_maptwo_info_table(self.jmp_item_info_table)
        self.update_maptwo_info_table(self.jmp_item_appear_table)
        self.update_maptwo_info_table(self.jmp_treasure_table)
        self.update_maptwo_info_table(self.jmp_furniture_info_table)
        self.update_maptwo_info_table(self.jmp_character_info_table)
        self.update_maptwo_info_table(self.jmp_event_info_table)
        self.update_maptwo_info_table(self.jmp_observer_info_table)

        self.arcs_by_path["files/Map/map2.szp"] = self.map_two_file

        # Save the changes of main.dol
        self.dol.save_changes()
        self.gcm.changed_files["sys/main.dol"] = self.dol.data

        # As mentioned before, these szp files need to be compressed again in order to be properly read by Dolphin.
        # If you forget this, you will get an Invalid read error on a certain memory address typically.
        for arc_path, arc in self.arcs_by_path.items():
            arc.save_changes()
            self.gcm.changed_files[arc_path] = Yay0.compress(arc.data)

        # Generator function to combine all necessary files into an ISO file.
        # Returned information is ignored. //Todo Maybe there is something better to put here?
        for _, _ in self.export_files_from_memory(): # next_progress_text, files_done
            continue

    def export_files_from_memory(self):
        if self.export_disc_to_folder:
            output_folder_path = os.path.join(self.randomized_output_folder, "%s Randomized" % RANDOMIZER_NAME)
            yield from self.gcm.export_disc_to_folder_with_changed_files(output_folder_path)
        else:
            output_file_path = os.path.join(self.randomized_output_folder, "%s Randomized.iso" % RANDOMIZER_NAME)
            yield from self.gcm.export_disc_to_iso_with_changed_files(output_file_path)

if __name__ == '__main__':
    unpacked_iso = LuigisMansionRandomizer("D:\\ROMs\\GameCube\\Luigis Mansion (USA).iso", "D:\\ROMs\\GameCube\\", False)