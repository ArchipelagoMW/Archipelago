import hashlib
import os
import yaml

from worlds.luigismansion.iso_helper.DOL_Updater import update_dol_offsets
from .iso_helper.Update_GameUSA import update_game_usa
from .JMP_Info_File import JMPInfoFile
from .Patching import *
from .Helper_Functions import StringByteFunction as sbf
from .iso_helper.Events import *

from gclib import fs_helpers as fs
from gclib.gcm import GCM
from gclib.dol import DOL
from gclib.rarc import RARC
from gclib.yaz0_yay0 import Yay0

RANDOMIZER_NAME = "Luigi's Mansion"
CLEAN_LUIGIS_MANSION_ISO_MD5 = 0x6e3d9ae0ed2fbd2f77fa1ca09a60c494  # Based on the USA version of Luigi's Mansion


class InvalidCleanISOError(Exception): pass


class LuigisMansionRandomizer:
    def __init__(self, clean_iso_path: str, randomized_output_file_path: str, ap_output_data=None, debug_flag=False):
        # Takes note of the provided Randomized Folder path and if files should be exported instead of making an ISO.
        self.debug = debug_flag
        self.clean_iso_path = clean_iso_path
        self.randomized_output_file_path = randomized_output_file_path

        try:
            if os.path.isfile(randomized_output_file_path):
                temp_file = open(randomized_output_file_path, "r+")  # or "a+", whatever you need
                temp_file.close()
        except IOError:
            raise Exception("'" + randomized_output_file_path + "' is currently in use by another program.")

        with open(os.path.abspath(ap_output_data)) as stream:
            self.output_data = yaml.safe_load(stream)

        # Verifies we have a valid installation of Luigi's Mansion USA. There are some regional file differences.
        self.__verify_supported_version()

        # After verifying, this will also read the entire iso, including system files and their content
        self.gcm = GCM(self.clean_iso_path)
        self.gcm.read_entire_disc()
        self.dol = DOL()

        # Change game ID so save files are different
        self.seed = self.output_data["Seed"]
        magic_seed = str(self.seed)
        bin_data = self.gcm.read_file_data("sys/boot.bin")
        bin_data.seek(0x01)
        bin_data.write(sbf.string_to_bytes(magic_seed, len(magic_seed)))
        self.gcm.changed_files["sys/boot.bin"] = bin_data

        # Updates the Game USA folder to have the correct ghost file we expect.
        self.gcm = update_game_usa(self.gcm)

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
        self.jmp_obj_info_table = self.load_maptwo_info_table("objinfo")
        self.jmp_generator_info_table = self.load_maptwo_info_table("generatorinfo")
        self.jmp_enemy_info_table = self.load_maptwo_info_table("enemyinfo")
        self.jmp_boo_table = self.load_maptwo_info_table("telesa")
        if self.output_data["Options"]["speedy_spirits"]:
            self.jmp_teiden_enemy_info_table = self.load_maptwo_info_table("teidenenemyinfo")
            self.jmp_teiden_observer_info_table = self.load_maptwo_info_table("teidenobserverinfo")
        self.jmp_teiden_character_info_table = self.load_maptwo_info_table("teidencharacterinfo")
        self.jmp_iyapoo_table = self.load_maptwo_info_table("iyapootable")

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
        arc = RARC(self.gcm.read_file_data(arc_path))  # Automatically decompresses Yay0
        arc.read()
        return arc

    # Uses custom class to load in JMP Info file entry (see more details in JMP_Info_File.py)
    def load_maptwo_info_table(self, jmp_table_name: str):
        jmp_table_entry = JMPInfoFile(self.map_two_file, jmp_table_name)
        if self.debug:
            jmp_table_entry.print_header_info()
        return jmp_table_entry

    # Updates the existing ARC / RARC file with the provided data for a given info file entry.
    def update_maptwo_info_table(self, jmp_info_file: JMPInfoFile):
        jmp_info_file.update_info_file_bytes()

        for jmp_file in self.map_two_file.file_entries:
            if jmp_file.name == jmp_info_file.info_file_entry.name:
                jmp_file.data = jmp_info_file.info_file_entry.data
                break

    # Updates all jmp tables in the map2.szp file.
    def update_maptwo_jmp_tables(self):
        # Get Output data required information
        bool_boo_checks = True if self.output_data["Options"]["boo_gates"] == 1 else False

        # Updates all data entries for each jmp table in memory first.
        update_character_info(self.jmp_character_info_table, self.output_data)
        update_item_info_table(self.jmp_item_info_table, self.output_data)
        update_item_appear_table(self.jmp_item_appear_table, self.output_data)
        update_treasure_table(self.jmp_treasure_table, self.jmp_character_info_table, self.output_data)
        update_treasure_table(self.jmp_treasure_table, self.jmp_teiden_character_info_table, self.output_data, True)
        update_furniture_info(self.jmp_furniture_info_table, self.jmp_item_appear_table, self.output_data)
        update_event_info(self.jmp_event_info_table, bool_boo_checks, self.output_data)
        update_observer_info(self.jmp_observer_info_table)
        update_key_info(self.jmp_key_info_table, self.output_data)
        update_obj_info(self.jmp_obj_info_table)
        update_generator_info(self.jmp_generator_info_table)
        update_enemy_info(self.jmp_enemy_info_table, self.output_data)
        if self.output_data["Options"]["speedy_spirits"]:
            update_teiden_enemy_info(self.jmp_enemy_info_table, self.jmp_teiden_enemy_info_table)
            update_teiden_observer_info(self.jmp_observer_info_table, self.jmp_teiden_observer_info_table)
        update_boo_table(self.jmp_boo_table, self.output_data)
        update_iyapoo_table(self.jmp_iyapoo_table, self.output_data)

        # Updates all the data entries in each jmp table in the szp file.
        self.update_maptwo_info_table(self.jmp_character_info_table)
        self.update_maptwo_info_table(self.jmp_teiden_character_info_table)
        self.update_maptwo_info_table(self.jmp_item_info_table)
        self.update_maptwo_info_table(self.jmp_item_appear_table)
        self.update_maptwo_info_table(self.jmp_treasure_table)
        self.update_maptwo_info_table(self.jmp_furniture_info_table)
        self.update_maptwo_info_table(self.jmp_event_info_table)
        self.update_maptwo_info_table(self.jmp_observer_info_table)
        self.update_maptwo_info_table(self.jmp_key_info_table)
        self.update_maptwo_info_table(self.jmp_obj_info_table)
        self.update_maptwo_info_table(self.jmp_generator_info_table)
        self.update_maptwo_info_table(self.jmp_enemy_info_table)
        if self.output_data["Options"]["speedy_spirits"]:
            self.update_maptwo_info_table(self.jmp_teiden_enemy_info_table)
            self.update_maptwo_info_table(self.jmp_teiden_observer_info_table)
        self.update_maptwo_info_table(self.jmp_boo_table)
        self.update_maptwo_info_table(self.jmp_iyapoo_table)

    def save_randomized_iso(self):
        # Get Output data required information
        bool_boo_rando_enabled: bool = True if self.output_data["Options"]["boosanity"] == 1 else False
        req_mario_count: str = str(self.output_data["Options"]["mario_items"])
        max_health: str = str(self.output_data["Options"]["luigi_max_health"])
        door_to_close_list: dict[int, int] = dict(self.output_data["Entrances"])
        start_inv_list: list[str] = list(self.output_data["Options"]["start_inventory"])
        bool_randomize_music: bool = True if int(self.output_data["Options"]["random_music"]) == 1 else False
        bool_randomize_mice: bool = True if int(self.output_data["Options"]["gold_mice"]) == 1 else False
        bool_hidden_mansion: bool = True if int(self.output_data["Options"]["hidden_mansion"]) == 1 else False
        walk_speed: int = int(self.output_data["Options"]["walk_speed"])
        bool_pickup_anim_enabled: bool = True if int(self.output_data["Options"]["pickup_animation"]) == 1 else False
        bool_fear_anim_disabled: bool = True if int(self.output_data["Options"]["fear_animation"]) == 1 else False
        player_name: str = str(self.output_data["Name"])
        king_boo_health: int = int(self.output_data["Options"]["king_boo_health"])
        random_spawn: str = str(self.output_data["Options"]["spawn"])

        # Boo related options
        bool_boo_checks: bool = True if self.output_data["Options"]["boo_gates"] == 1 else False
        washroom_boo_count: int = int(self.output_data["Options"]["washroom_boo_count"])
        balcony_boo_count: int = int(self.output_data["Options"]["balcony_boo_count"])
        final_boo_count: int = int(self.output_data["Options"]["final_boo_count"])

        # Hint options
        hint_dist: int = int(self.output_data["Options"]["hint_distribution"])
        hint_list: dict[str, dict[str, str]] = self.output_data["Hints"]
        madam_hint_dict: dict[str, str] = hint_list["Madame Clairvoya"] if "Madame Clairvoya" in hint_list else None
        bool_portrait_hints: bool = True if self.output_data["Options"]["portrait_hints"] == 1 else False

        self.gcm, self.dol = update_dol_offsets(self.gcm, self.dol, start_inv_list, walk_speed, player_name,
            random_spawn, king_boo_health, bool_fear_anim_disabled, bool_pickup_anim_enabled, bool_boo_rando_enabled)

        self.gcm = update_common_events(self.gcm, bool_randomize_mice)
        self.gcm = update_intro_and_lab_events(self.gcm, bool_hidden_mansion, max_health, start_inv_list, door_to_close_list)

        if bool_boo_checks:
            boo_list_events = ["16", "47", "96"]
            for event_no in boo_list_events:
                if event_no == "16":
                    required_boo_count = final_boo_count
                elif event_no == "47":
                    required_boo_count = washroom_boo_count
                else:
                    required_boo_count = balcony_boo_count

                if required_boo_count == 0:
                    self.jmp_event_info_table.info_file_field_entries = list(filter(lambda info_entry: not (
                        info_entry["EventNo"] == int(event_no)), self.jmp_event_info_table.info_file_field_entries))
                    continue
                self.gcm = update_boo_gates(self.gcm, event_no, required_boo_count, bool_boo_rando_enabled)

        self.gcm = update_blackout_event(self.gcm)

        self.gcm = randomize_clairvoya(self.gcm, req_mario_count, hint_dist, madam_hint_dict, self.seed)
        self.gcm = write_in_game_hints(self.gcm, hint_dist, hint_list, self.seed)

        if bool_portrait_hints:
            self.gcm = write_portrait_hints(self.gcm, hint_dist, hint_list, self.seed)

        if bool_randomize_music:
            self.gcm = randomize_music(self.gcm, self.seed)

        self.update_maptwo_jmp_tables()

        # Save the map two file changes
        # As mentioned before, these szp files need to be compressed again in order to be properly read by Dolphin/GC.
        # If you forget this, you will get an Invalid read error on a certain memory address typically.
        self.map_two_file.save_changes()
        self.gcm.changed_files["files/Map/map2.szp"] = Yay0.compress(self.map_two_file.data)

        # Generator function to combine all necessary files into an ISO file.
        # Returned information is ignored.
        for _, _ in self.export_files_from_memory():
            continue

    # If Export to disc is true, Exports the entire file/directory contents of the ISO to specified folder
    # Otherwise, creates a direct ISO file.
    def export_files_from_memory(self):
        yield from self.gcm.export_disc_to_iso_with_changed_files(self.randomized_output_file_path)


if __name__ == '__main__':
    print("Run this from Launcher.py instead.")
