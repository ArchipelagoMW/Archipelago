import hashlib
import os
import re
import io
import struct
import random
from tkinter import filedialog
from pathlib import Path
import yaml
from pkgutil import get_data

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
    def __init__(self, clean_iso_path: str, randomized_output_file_path: str, ap_output_data=None,
                 export_disc_to_folder=False, debug_flag=False):
        # Takes note of the provided Randomized Folder path and if files should be exported instead of making an ISO.
        select_aplm_path = ap_output_data
        self.debug = debug_flag
        if self.debug:
            self.clean_iso_path = filedialog.askopenfilename(title="Select your NA iso file",
                                                             filetypes=[("ISO Files", ".iso")])
            self.randomized_output_file_path = os.path.join(
                Path(os.path.dirname(self.clean_iso_path)).parent, "%s Randomized.iso" % RANDOMIZER_NAME)
            if ap_output_data is None:
                select_aplm_path = filedialog.askopenfilename(title="Select your APLM File",
                                                              filetypes=[("APLM Files", ".aplm")])
        else:
            self.clean_iso_path = clean_iso_path
            self.randomized_output_file_path = randomized_output_file_path

        try:
            if os.path.isfile(randomized_output_file_path):
                temp_file = open(randomized_output_file_path, "r+")  # or "a+", whatever you need
                temp_file.close()
        except IOError:
            raise Exception("'" + randomized_output_file_path + "' is currently in use by another program.")

        with open(os.path.abspath(select_aplm_path)) as stream:
            self.output_data = yaml.safe_load(stream)

        self.export_disc_to_folder = export_disc_to_folder

        # Verifies we have a valid installation of Luigi's Mansion USA. There are some regional file differences.
        # After verifying, this will also read the entire iso, including system files and the content files
        self.__verify_supported_version()
        self.gcm = GCM(self.clean_iso_path)
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
        self.jmp_obj_info_table = self.load_maptwo_info_table("objinfo")
        self.jmp_generator_info_table = self.load_maptwo_info_table("generatorinfo")
        self.jmp_enemy_info_table = self.load_maptwo_info_table("enemyinfo")
        self.jmp_boo_table = self.load_maptwo_info_table("telesa")
        if self.output_data["Options"]["speedy_spirits"]:
            self.jmp_teiden_enemy_info_table = self.load_maptwo_info_table("teidenenemyinfo")
            self.jmp_teiden_observer_info_table = self.load_maptwo_info_table("teidenobserverinfo")
        self.jmp_teiden_character_info_table = self.load_maptwo_info_table("teidencharacterinfo")

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
        update_event_info(self.jmp_event_info_table, bool_boo_checks)
        update_observer_info(self.jmp_observer_info_table)
        update_key_info(self.jmp_key_info_table, self.output_data)
        update_obj_info(self.jmp_obj_info_table)
        update_generator_info(self.jmp_generator_info_table)
        update_enemy_info(self.jmp_enemy_info_table, self.output_data)
        if self.output_data["Options"]["speedy_spirits"]:
            update_teiden_enemy_info(self.jmp_enemy_info_table, self.jmp_teiden_enemy_info_table)
            update_teiden_observer_info(self.jmp_observer_info_table, self.jmp_teiden_observer_info_table)
        update_boo_table(self.jmp_boo_table)

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

    def save_randomized_iso(self):
        random.seed(self.output_data["Seed"])
        # Save the changes of main.dol
        self.update_dol_offsets()
        self.dol.save_changes()
        self.gcm.changed_files["sys/main.dol"] = self.dol.data

        # TODO Move into its own function?
        # Get Output data required information
        bool_boo_checks: bool = True if self.output_data["Options"]["boo_gates"] == 1 else False
        required_mario_item_count: int = int(self.output_data["Options"]["mario_items"])
        bool_randomize_music: bool = True if self.output_data["Options"]["random_music"] == 1 else False
        bool_portrait_hints: bool = True if self.output_data["Options"]["portrait_hints"] == 1 else False
        washroom_boo_count: int = int(self.output_data["Options"]["washroom_boo_count"])
        balcony_boo_count: int = int(self.output_data["Options"]["balcony_boo_count"])
        final_boo_count: int = int(self.output_data["Options"]["final_boo_count"])

        # Update all custom events
        list_events = ["03", "12", "22", "24", "29", "33", "35", "38", "50", "61", "64", "65",
                       "66", "67", "68", "71", "72", "74", "75", "82", "86", "87", "88", "89", "90"]
        for custom_event in list_events:
            self.update_custom_event(custom_event, True)

        lines = get_data(__name__, "data/custom_events/event48.txt").decode('utf-8')

        if self.output_data["Options"]["hidden_mansion"] == 1:
            mansion_type = "<URALUIGI>"
        else:
            mansion_type = "<OMOTELUIGI>"
        lines = lines.replace("{MANSION_TYPE}", mansion_type)

        include_radar = ""
        if any("Boo Radar" in key for key in self.output_data["Options"]["start_inventory"]):
            include_radar = "<FLAGON>(73)" + os.linesep + "<FLAGON>(75)"
        lines = lines.replace("{BOO RADAR}", include_radar)

        event_door_list: list[str] = []
        door_list: dict[int, int] = self.output_data["Entrances"]

        for event_door in door_list:
            if door_list.get(event_door) == 0:
                event_door_list.append(f"<KEYLOCK>({event_door})" + os.linesep)
            else:
                event_door_list.append(f"<KEYUNLOCK>({event_door})" + os.linesep)

        lines = lines.replace("{DOOR_LIST}", ''.join(event_door_list))

        self.update_custom_event("48", False, lines)

        if bool_boo_checks:
            boo_list_events = ["16", "47", "96"]
            for event_no in boo_list_events:
                lines = get_data(__name__, "data/custom_events/event" + event_no + ".txt").decode('utf-8')
                if event_no == "16":
                    required_boo_count = final_boo_count
                elif event_no == "47":
                    required_boo_count = washroom_boo_count
                else:
                    required_boo_count = balcony_boo_count

                if required_boo_count == 0:
                    self.jmp_event_info_table.info_file_field_entries = list(filter(lambda info_entry:
                        not (info_entry["EventNo"] == int(event_no)), self.jmp_event_info_table.info_file_field_entries))
                    continue

                str_not_enough = "not_enough"
                str_boo_captured = "boos_captured"

                match required_boo_count:
                    case 1:
                        lines = lines.replace("{Count0}", "0")
                        lines = lines.replace("{Count1}", str(required_boo_count))
                        lines = lines.replace("{Count2}", str(required_boo_count))
                        lines = lines.replace("{Count3}", str(required_boo_count))
                        lines = lines.replace("{Count4}", str(required_boo_count))
                        lines = lines.replace("{Case0}", str_not_enough)
                        lines = lines.replace("{Case1}", str_boo_captured)
                        lines = lines.replace("{Case2}", str_boo_captured)
                        lines = lines.replace("{Case3}", str_boo_captured)
                        lines = lines.replace("{Case4}", str_boo_captured)
                    case 2:
                        lines = lines.replace("{Count0}", "0")
                        lines = lines.replace("{Count1}", "1")
                        lines = lines.replace("{Count2}", str(required_boo_count))
                        lines = lines.replace("{Count3}", str(required_boo_count))
                        lines = lines.replace("{Count4}", str(required_boo_count))
                        lines = lines.replace("{Case0}", str_not_enough)
                        lines = lines.replace("{Case1}", str_not_enough)
                        lines = lines.replace("{Case2}", str_boo_captured)
                        lines = lines.replace("{Case3}", str_boo_captured)
                        lines = lines.replace("{Case4}", str_boo_captured)
                    case 3:
                        lines = lines.replace("{Count0}", "0")
                        lines = lines.replace("{Count1}", "1")
                        lines = lines.replace("{Count2}", "2")
                        lines = lines.replace("{Count3}", str(required_boo_count))
                        lines = lines.replace("{Count4}", str(required_boo_count))
                        lines = lines.replace("{Case0}", str_not_enough)
                        lines = lines.replace("{Case1}", str_not_enough)
                        lines = lines.replace("{Case2}", str_not_enough)
                        lines = lines.replace("{Case3}", str_boo_captured)
                        lines = lines.replace("{Case4}", str_boo_captured)
                    case _:
                        lines = lines.replace("{Count0}", str(required_boo_count-4))
                        lines = lines.replace("{Count1}", str(required_boo_count-3))
                        lines = lines.replace("{Count2}", str(required_boo_count-2))
                        lines = lines.replace("{Count3}", str(required_boo_count-1))
                        lines = lines.replace("{Count4}", str(required_boo_count))
                        lines = lines.replace("{Case0}", str_not_enough)
                        lines = lines.replace("{Case1}", str_not_enough)
                        lines = lines.replace("{Case2}", str_not_enough)
                        lines = lines.replace("{Case3}", str_not_enough)
                        lines = lines.replace("{Case4}", str_boo_captured)

                self.update_custom_event(event_no, False, lines)

        in_game_hint_events = ["04", "17", "32", "44", "45", "63", "92", "93", "94"]
        for event_no in in_game_hint_events:
            hintfo: str = ""
            match event_no:
                case "04":
                    hintfo = self.output_data["Hints"]["Courtyard Toad"]
                case "17":
                    hintfo = self.output_data["Hints"]["Foyer Toad"]
                case "32":
                    hintfo = self.output_data["Hints"]["Wardrobe Balcony Toad"]
                case "63":
                    hintfo = self.output_data["Hints"]["1F Washroom Toad"]
                case "92":
                    hintfo = self.output_data["Hints"]["Center Telephone"]
                case "93":
                    hintfo = self.output_data["Hints"]["Left Telephone"]
                case "94":
                    hintfo = self.output_data["Hints"]["Right Telephone"]
            lines = get_data(__name__, "data/custom_events/event" + event_no + ".txt").decode('utf-8')
            lines = lines.replace("{HintText}", str(hintfo))
            self.update_custom_event(event_no, False, lines, replace_old_csv=True)

        # Update Madame Clairvoya's event to check mario items.
        lines = get_data(__name__, "data/custom_events/event36.txt").decode('utf-8')
        lines = lines.replace("{MarioCount}", str(required_mario_item_count))
        lines = lines.replace("{HintText}", str(self.output_data["Hints"]["Madame Clairvoya"]))

        cases_to_replace = ["{CaseZero}", "{CaseOne}", "{CaseTwo}", "{CaseThree}", "{CaseFour}", "{CaseFive}"]
        str_good_end = "GoodEnd"
        str_bad_end = "MissingItems"

        for i in range(0, 6):
            if i >= required_mario_item_count:
                lines = lines.replace(cases_to_replace[i], str_good_end)
            else:
                lines = lines.replace(cases_to_replace[i], str_bad_end)

        self.update_custom_event("36", False, lines, replace_old_csv=True)

        # Copy in our newly custom events for hallway light changes
        # Update all custom events

        if bool_randomize_music:
            list_ignore_events = ["event00.szp"]
            event_dir = self.gcm.get_or_create_dir_file_entry("files/Event")
            for lm_event in event_dir.children:
                if (lm_event.is_dir or lm_event.name in list_ignore_events or
                        not re.match(r"event\d+\.szp", lm_event.name)):
                    continue

                if lm_event.file_path in self.gcm.changed_files:
                    lm_event_bytes = self.gcm.get_changed_file_data(lm_event.file_path)
                else:
                    lm_event_bytes = self.gcm.read_file_data(lm_event.file_path)

                event_arc = RARC(lm_event_bytes)  # Automatically decompresses Yay0
                event_arc.read()

                name_to_find = lm_event.name.replace(".szp", ".txt")

                if not any(info_files for info_files in event_arc.file_entries if info_files.name == name_to_find):
                    continue

                event_text_data = next((info_files for info_files in event_arc.file_entries if
                                        info_files.name == name_to_find)).data
                event_str = event_text_data.getvalue().decode('utf-8', errors='replace')
                music_to_replace = re.findall(r'\<BGM\>\(\d+\)', event_str)

                if music_to_replace:
                    for music_match in music_to_replace:
                        list_of_bad_music = [-1, 13, 17, 21, 24, 28, 41]
                        int_music_selection: int = -1
                        while int_music_selection in list_of_bad_music:
                            int_music_selection = random.randint(0, 52)
                        event_str = event_str.replace(music_match, "<BGM>(" + str(int_music_selection) + ")")

                updated_event = io.BytesIO(event_str.encode('utf-8'))

                next((info_files for info_files in event_arc.file_entries if
                      info_files.name == name_to_find)).data = updated_event
                event_arc.save_changes()
                self.gcm.changed_files[lm_event.file_path] = Yay0.compress(event_arc.data)

        self.update_maptwo_jmp_tables()

        # Save the map two file changes
        # As mentioned before, these szp files need to be compressed again in order to be properly read by Dolphin/GC.
        # If you forget this, you will get an Invalid read error on a certain memory address typically.
        self.map_two_file.save_changes()
        self.gcm.changed_files["files/Map/map2.szp"] = Yay0.compress(self.map_two_file.data)

        # Generator function to combine all necessary files into an ISO file.
        # Returned information is ignored. # Todo Maybe there is something better to put here?
        for _, _ in self.export_files_from_memory():  # next_progress_text, files_done
            continue  # percentage_done = files_done/len(self.gcm.files_by_path)

    # Updates various DOL Offsets per the desired changes of the AP user
    def update_dol_offsets(self):
        # Walk Speed
        if self.output_data["Options"]["walk_speed"] == 0:
            walk_speed = 16784
        elif self.output_data["Options"]["walk_speed"] == 1:
            walk_speed = 16850
        else:
            walk_speed = 16950
        self.dol.data.seek(0x396538)
        self.dol.data.write(struct.pack(">H", walk_speed))

        # Vacuum Speed
        if any("Poltergust 4000" in key for key in self.output_data["Options"]["start_inventory"]):
            vac_speed = [0x38, 0x00, 0x00, 0x0F]
        else:
            vac_speed = [0x80, 0x0D, 0x01, 0x60]
        self.dol.data.seek(0x7EA28)
        self.dol.data.write(struct.pack(">BBBB", *vac_speed))

        # Fix Boos to properly spawn
        self.dol.data.seek(0x12DCC9)
        boo_data = [0x00, 0x00, 0x05]
        self.dol.data.write(struct.pack(">BBB", *boo_data))

        # Turn off pickup animations
        if self.output_data["Options"]["pickup_animation"] == 1:
            pickup_val = [0x01]
            # gem_val = [0x05]
        else:
            pickup_val = [0x02]
            # gem_val = [0x06]

        # Keys and important animations
        self.dol.data.seek(0xCD39B)
        self.dol.data.write(struct.pack(">B", *pickup_val))

        # Diamonds and other treasure animations
        # TODO this breaks king boo boss fight currently
        # self.dol.data.seek(0xCE8D3)
        # self.dol.data.write(struct.pack(">B", *gem_val))

        # Turn off luigi scare animations
        if self.output_data["Options"]["fear_animation"] == 1:
            scare_val = [0x00]
        else:
            scare_val = [0x44]
        self.dol.data.seek(0x396578)
        self.dol.data.write(struct.pack(">B", *scare_val))

        lm_player_name = str(self.output_data["Name"]).strip()
        self.dol.data.seek(0x311660)
        self.dol.data.write(struct.pack(str(len(lm_player_name)) + "s", lm_player_name.encode()))

        king_boo_health = int(self.output_data["Options"]["king_boo_health"])
        self.dol.data.seek(0x399228)
        self.dol.data.write(struct.pack(">H", king_boo_health))

    def update_custom_event(self, event_number: str, check_local_folder: bool, non_local_str="",
                            custom_made: bool = False, replace_old_csv: bool = False):
        # TODO Update custom events to remove any camera files or anything else related.
        if not check_local_folder and not non_local_str:
            raise Exception("If the custom event does not exist in the local data folder, an event string must be " +
                            "provided to overwrite an existing event.")
        if not custom_made:
            custom_event = self.get_arc("files/Event/event" + event_number + ".szp")
            name_to_find = "event" + event_number + ".txt"
        else:
            custom_event = self.get_arc("files/Event/event64.szp")
            name_to_find = "event64.txt"
            next((info_files for info_files in custom_event.file_entries if
                  info_files.name == name_to_find)).name = "event" + event_number + ".txt"
            name_to_find = "event" + event_number + ".txt"

        if not any(info_files for info_files in custom_event.file_entries if info_files.name == name_to_find):
            raise Exception(f"Unable to find an info file with name '{name_to_find}' in provided RARC file.")

        if check_local_folder:
            lines = io.BytesIO(get_data(__name__, f"data/custom_events/{name_to_find}"))
        else:
            lines = io.BytesIO(non_local_str.encode('utf-8'))

        next((info_files for info_files in custom_event.file_entries if info_files.name == name_to_find)).data = lines

        # Some events don't have a CSV, so no need to set it to blank lines
        # TODO update this to not use a template CSV, as it is now blank.
        updated_event_number = event_number if not event_number.startswith("0") else event_number[1:]
        if replace_old_csv:
            name_to_find = "message" + updated_event_number + ".csv"
            lines = io.BytesIO(get_data(__name__, f"data/custom_csvs/{name_to_find}"))
            next((info_files for info_files in custom_event.file_entries if
                  info_files.name == name_to_find)).data = lines
        else:
            bool_csv_lines = any((info_files for info_files in custom_event.file_entries if
                                  info_files.name == "message" + updated_event_number + ".csv"))

            if bool_csv_lines:
                csv_lines = io.BytesIO(get_data(__name__, "data/custom_events/TemplateCSV.csv"))
                next((info_files for info_files in custom_event.file_entries if
                      info_files.name == "message" + updated_event_number + ".csv")).data = csv_lines

        custom_event.save_changes()
        self.gcm.changed_files["files/Event/event" + event_number + ".szp"] = (
            Yay0.compress(custom_event.data))

    def copy_existing_event(self, new_event_number: str):
        event_path = "files/Event/event" + new_event_number + ".szp"
        data = self.gcm.read_file_data("files/Event/event64.szp")
        self.gcm.add_new_file(event_path, data)
        return

    # If Export to disc is true, Exports the entire file/directory contents of the ISO to specified folder
    # Otherwise, creates a direct ISO file.
    def export_files_from_memory(self):
        if self.export_disc_to_folder:
            output_folder_path = os.path.join(
                Path(self.randomized_output_file_path).parent, "%s Randomized Exported" % RANDOMIZER_NAME)
            yield from self.gcm.export_disc_to_folder_with_changed_files(output_folder_path)
        else:
            yield from self.gcm.export_disc_to_iso_with_changed_files(self.randomized_output_file_path)


if __name__ == '__main__':
    unpacked_iso = LuigisMansionRandomizer("", "", None, False, True)
