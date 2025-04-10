import csv
import hashlib
import os
import io
import struct
import yaml

from .iso_helper.Update_GameUSA import update_game_usa
from . import data
from .Hints import PORTRAIT_HINTS
from .JMP_Info_File import JMPInfoFile
from .Patching import *
from .Helper_Functions import StringByteFunction as sbf
from .iso_helper.Events import *

from gclib import fs_helpers as fs
from gclib.gcm import GCM
from gclib.dol import DOL, DOLSection
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
        # TODO Move into its own function?
        # Get Output data required information
        bool_boo_checks: bool = True if self.output_data["Options"]["boo_gates"] == 1 else False
        bool_boo_rando_on: bool = True if self.output_data["Options"]["boosanity"] == 1 else False
        req_mario_count: str = str(self.output_data["Options"]["mario_items"])
        bool_randomize_music: bool = True if self.output_data["Options"]["random_music"] == 1 else False
        # bool_portrait_hints: bool = True if self.output_data["Options"]["portrait_hints"] == 1 else False
        washroom_boo_count: int = int(self.output_data["Options"]["washroom_boo_count"])
        balcony_boo_count: int = int(self.output_data["Options"]["balcony_boo_count"])
        final_boo_count: int = int(self.output_data["Options"]["final_boo_count"])
        luigi_max_health: int = int(self.output_data["Options"]["luigi_max_health"])
        hint_dist: int = int(self.output_data["Options"]["hint_distribution"])
        madam_hint_dict: dict[str, str] = self.output_data["Hints"]["Madame Clairvoya"] if (
            self.output_data["Hints"]["Madame Clairvoya"]) else None

        self.update_dol_offsets(bool_boo_rando_on)

        # Update all custom events
        list_events = ["03", "22", "24", "29", "33", "35", "38", "50", "61", "64", "65",
                       "66", "67", "68", "71", "72", "74", "75", "82", "86", "87", "88", "89", "90"]
        if self.output_data["Options"]["gold_mice"] == 1:
            list_events += ["95", "97", "98", "99", "100"]
        for custom_event in list_events:
            self.update_custom_event(custom_event, True)

        lines = get_data(__name__, "data/custom_events/event08.txt").decode('utf-8')
        lines = lines.replace("{LUIGIMAXHP}", str(luigi_max_health))
        self.update_custom_event("08", False, lines, replace_old_csv=True)

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
        lines = lines.replace("{LUIGIMAXHP}", str(luigi_max_health))

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

                # TODO optimize this?
                if not bool_boo_rando_on:
                    str_not_enough = "not_enough"
                    str_boo_captured = "boos_captured"
                    str_begin_case = "CheckBoos"

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
                else:
                    str_begin_case = "not_enough"

                lines = lines.replace("{Count4}", str(required_boo_count))
                lines = lines.replace("{CaseBegin}", str_begin_case)
                self.update_custom_event(event_no, False, lines)

        # Update Toad events with hints
        """in_game_hint_events = ["04", "17", "32", "44", "63", "92", "93", "94"]
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

        # Update Portrait Ghost heart scans if those hints are turned on
        if self.output_data["Options"]["portrait_hints"] == 1:
            portrait_scan_event = self.get_arc("files/Event/event78.szp")
            portrait_csv = get_data(__name__, "data/custom_csvs/message78.csv").decode('utf-8')
            for name in PORTRAIT_HINTS:
                hintfo = self.output_data["Hints"][name]
                portrait_csv = portrait_csv.replace(f"{name}", str(hintfo))
            portrait_csv = io.BytesIO(portrait_csv.encode('utf-8'))
            next(info_files for info_files in portrait_scan_event.file_entries if
                  info_files.name == "message78.csv").data = portrait_csv
            portrait_scan_event.save_changes()
            self.gcm.changed_files["files/Event/event78.szp"] = (
                Yay0.compress(portrait_scan_event.data))"""

        self.gcm = randomize_clairvoya(self.gcm, req_mario_count, hint_dist, madam_hint_dict, self.seed)

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

    # Updates various DOL Offsets per the desired changes of the AP user
    def update_dol_offsets(self, boo_rand_on: bool):
        # Find the main DOL file, which is the main file used for GC and Wii games.
        dol_data = self.gcm.read_file_data("sys/main.dol")
        self.dol.read(dol_data)

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
            vac_speed = "3800000F"
        else:
            vac_speed = "800D0160"
        self.dol.data.seek(0x7EA28)
        self.dol.data.write(bytes.fromhex(vac_speed))

        # Fix Boos to properly spawn
        self.dol.data.seek(0x12DCC9)
        boo_data = "000005"
        self.dol.data.write(bytes.fromhex(boo_data))

        # Turn on custom code handler for boo display counter only if Boo Rando is on.
        if boo_rand_on:
            self.dol.data.seek(0x04DB50)
            boo_custom_code_one = "93C1FFF0"
            self.dol.data.write(bytes.fromhex(boo_custom_code_one))

            self.dol.data.seek(0x04DBB0)
            boo_custom_code_two = "4848CDE5"
            self.dol.data.write(bytes.fromhex(boo_custom_code_two))

            self.dol.data.seek(0x04DC10)
            boo_custom_code_three = "4848CD85"
            self.dol.data.write(bytes.fromhex(boo_custom_code_three))

        # Turn off pickup animations
        if self.output_data["Options"]["pickup_animation"] == 1:
            pickup_val = [0x01]
            gem_val = [0x05]

            # Write additional code to enable Custom Pickup animations when animations are turned off.
            self.dol.data.seek(0xAD625)
            self.dol.data.write(bytes.fromhex("42D0F5"))
        else:
            pickup_val = [0x02]
            gem_val = [0x06]

        # Keys and important animations
        self.dol.data.seek(0xCD39B)
        self.dol.data.write(struct.pack(">B", *pickup_val))

        # Diamonds and other treasure animations
        # TODO this breaks king boo boss fight currently
        self.dol.data.seek(0xCE8D3)
        self.dol.data.write(struct.pack(">B", *gem_val))

        # Turn off luigi scare animations
        if self.output_data["Options"]["fear_animation"] == 1:
            scare_val = [0x00]
        else:
            scare_val = [0x44]
        self.dol.data.seek(0x396578)
        self.dol.data.write(struct.pack(">B", *scare_val))

        # Store Player name
        lm_player_name = str(self.output_data["Name"]).strip()
        self.dol.data.seek(0x311660)
        self.dol.data.write(struct.pack(str(len(lm_player_name)) + "s", lm_player_name.encode()))

        # Change King Boo's Health
        king_boo_health = int(self.output_data["Options"]["king_boo_health"])
        self.dol.data.seek(0x399228)
        self.dol.data.write(struct.pack(">H", king_boo_health))

        # Replace section two with our own custom section, which is about 1000 hex bytes long.
        new_dol_size = 0x1000
        new_dol_sect = DOLSection(0x39FA20, 0x804DD940, new_dol_size)
        self.dol.sections[2] = new_dol_sect

        # Append the extra bytes we expect, to ensure we can write to them in memory.
        self.dol.data.seek(len(self.dol.data.getvalue()))
        blank_data = b"\x00" * new_dol_size
        self.dol.data.write(blank_data)

        # Read in all the other custom DOL changes and update their values to the new value as expected.
        from importlib.resources import files
        with files(data).joinpath("dol_diff.csv").open() as file:
            hex_reader = csv.DictReader(file)
            for line in hex_reader:
                new_dol_offset, hex_val = int(line["addr"], 16), bytes.fromhex(line["val"])
                if self.debug:
                    print(f"Updating DOL Offset {new_dol_offset} with hex value: {str(hex_val)}")
                self.dol.data.seek(new_dol_offset)
                self.dol.data.write(hex_val)

        # Save all changes to the DOL itself.
        self.dol.save_changes()
        self.gcm.changed_files["sys/main.dol"] = self.dol.data


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
        event_data = self.gcm.read_file_data("files/Event/event64.szp")
        self.gcm.add_new_file(event_path, event_data)
        return

    # If Export to disc is true, Exports the entire file/directory contents of the ISO to specified folder
    # Otherwise, creates a direct ISO file.
    def export_files_from_memory(self):
        yield from self.gcm.export_disc_to_iso_with_changed_files(self.randomized_output_file_path)


if __name__ == '__main__':
    print("Run this from Launcher.py instead.")
