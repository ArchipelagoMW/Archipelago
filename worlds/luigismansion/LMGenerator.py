import os, yaml

from collections import Counter
from CommonClient import logger

from gclib.gcm import GCM
from gclib.dol import DOL
from gclib.rarc import RARC
from gclib.yaz0_yay0 import Yay0

def counter_constructor(loader, node):
    args = loader.construct_sequence(node)
    return Counter(*args)

# Core implemented custom collection counters which yaml.safe_load cannot serialize by default.
yaml.SafeLoader.add_constructor(
    'tag:yaml.org,2002:python/object/apply:collections.Counter',
    counter_constructor
)
from .iso_helper.DOL_Updater import update_dol_offsets
from .iso_helper.Update_GameUSA import update_game_usa
from .iso_helper.JMP_Info_File import JMPInfoFile
from .Patching import *
from .Helper_Functions import StringByteFunction as sbf
from .iso_helper.Events import *

RANDOMIZER_NAME = "Luigi's Mansion"

class LuigisMansionRandomizer:
    def __init__(self, clean_iso_path: str, randomized_output_file_path: str, ap_output_data: bytes, debug_flag=False):
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

        self.output_data = yaml.safe_load(ap_output_data)

        # After verifying, this will also read the entire iso, including system files and their content
        self.gcm = GCM(self.clean_iso_path)
        self.gcm.read_entire_disc()
        self.dol = DOL()

        # Change game ID so save files are different
        logger.info("Updating the ISO game id with the AP generated seed.")
        self.seed = self.output_data["Seed"]
        magic_seed = str(self.seed)
        bin_data = self.gcm.read_file_data("sys/boot.bin")
        bin_data.seek(0x01)
        bin_data.write(sbf.string_to_bytes(magic_seed, len(magic_seed)))
        self.gcm.changed_files["sys/boot.bin"] = bin_data

        # Updates the Game USA folder to have the correct ghost file we expect.
        logger.info("Updating game_usa.szp to import the ghost files as we expect.")
        self.gcm = update_game_usa(self.gcm)

        # Important note: SZP are just RARC / Arc files that are yay0 compressed, at least for Luigi's Mansion
        # Get Arc automatically handles decompressing RARC data from yay0, but compressing is on us later.
        logger.info("Loading all of the main mansion map files into memory.")
        self.map_two_file = self.get_arc("files/Map/map2.szp")
        self.map_three_file = self.get_arc("files/Map/map3.szp")

        # Loads all the specific JMP tables AP may potentially change / update.
        # Although some events are not changed by AP directly, they are changed here to remove un-necessary cutscenes,
        # set certain flag values, and remove un-necessary script tags.
        self.jmp_item_info_table = self.load_map_info_table(self.map_two_file,"iteminfotable")
        self.jmp_item_appear_table = self.load_map_info_table(self.map_two_file,"itemappeartable")
        self.jmp_treasure_table = self.load_map_info_table(self.map_two_file,"treasuretable")
        self.jmp_furniture_info_table = self.load_map_info_table(self.map_two_file,"furnitureinfo")
        self.jmp_character_info_table = self.load_map_info_table(self.map_two_file,"characterinfo")
        self.jmp_event_info_table = self.load_map_info_table(self.map_two_file,"eventinfo")
        self.jmp_observer_info_table = self.load_map_info_table(self.map_two_file,"observerinfo")
        self.jmp_key_info_table = self.load_map_info_table(self.map_two_file,"keyinfo")
        self.jmp_obj_info_table = self.load_map_info_table(self.map_two_file,"objinfo")
        self.jmp_generator_info_table = self.load_map_info_table(self.map_two_file,"generatorinfo")
        self.jmp_enemy_info_table = self.load_map_info_table(self.map_two_file,"enemyinfo")
        self.jmp_boo_table = self.load_map_info_table(self.map_two_file,"telesa")
        self.jmp_teiden_observer_info_table = self.load_map_info_table(self.map_two_file,"teidenobserverinfo")
        if self.output_data["Options"]["speedy_spirits"]:
            self.jmp_teiden_enemy_info_table = self.load_map_info_table(self.map_two_file,"teidenenemyinfo")
        self.jmp_teiden_character_info_table = self.load_map_info_table(self.map_two_file,"teidencharacterinfo")
        self.jmp_iyapoo_table = self.load_map_info_table(self.map_two_file,"iyapootable")
        self.jmp_map3_event_info_table = self.load_map_info_table(self.map_three_file,"eventinfo")

        # Saves the randomized iso file, with all files updated.
        self.save_randomized_iso()

    # Get an ARC / RARC / SZP file from within the ISO / ROM
    def get_arc(self, arc_path):
        arc_path = arc_path.replace("\\", "/")
        arc = RARC(self.gcm.read_file_data(arc_path))  # Automatically decompresses Yay0
        arc.read()
        return arc

    # Uses custom class to load in JMP Info file entry (see more details in JMP_Info_File.py)
    def load_map_info_table(self, map_file, jmp_table_name: str):
        jmp_table_entry = JMPInfoFile(map_file, jmp_table_name)
        if self.debug:
            jmp_table_entry.print_header_info()
        return jmp_table_entry

    # Updates the existing ARC / RARC file with the provided data for a given info file entry.
    def update_map_info_table(self, map_file, jmp_info_file: JMPInfoFile):
        jmp_info_file.update_info_file_bytes()

        for jmp_file in map_file.file_entries:
            if jmp_file.name == jmp_info_file.info_file_entry.name:
                jmp_file.data = jmp_info_file.info_file_entry.data
                break

    # Updates all jmp tables in the map2.szp and map3.szp file.
    def update_map_jmp_tables(self):
        # Get Output data required information
        bool_boo_checks = True if self.output_data["Options"]["boo_gates"] == 1 else False
        bool_speedy_spirits = True if self.output_data["Options"]["speedy_spirits"] == 1 else False

        # Updates all data entries for each jmp table in memory first.
        update_character_info(self.jmp_character_info_table, self.output_data)
        update_item_info_table(self.jmp_item_info_table, self.output_data)
        update_item_appear_table(self.jmp_item_appear_table, self.output_data)
        update_treasure_table(self.jmp_treasure_table, self.jmp_character_info_table, self.output_data)
        update_treasure_table(self.jmp_treasure_table, self.jmp_teiden_character_info_table, self.output_data)
        update_furniture_info(self.jmp_furniture_info_table, self.jmp_item_appear_table, self.output_data)
        update_event_info(self.jmp_event_info_table, bool_boo_checks, self.output_data)
        update_observer_info(self.jmp_observer_info_table)
        update_key_info(self.jmp_key_info_table, self.output_data)
        update_obj_info(self.jmp_obj_info_table)
        update_generator_info(self.jmp_generator_info_table)
        update_enemy_info(self.jmp_enemy_info_table, self.output_data)
        update_teiden_observer_info(self.jmp_observer_info_table,
            self.jmp_teiden_observer_info_table, bool_speedy_spirits)
        if bool_speedy_spirits:
            update_teiden_enemy_info(self.jmp_enemy_info_table, self.jmp_teiden_enemy_info_table)
        update_boo_table(self.jmp_boo_table, self.output_data)
        update_iyapoo_table(self.jmp_iyapoo_table, self.output_data)
        update_event_info(self.jmp_map3_event_info_table, bool_boo_checks, self.output_data)

        # Updates all the data entries in each jmp table in the szp file.
        self.update_map_info_table(self.map_two_file,self.jmp_character_info_table)
        self.update_map_info_table(self.map_two_file,self.jmp_teiden_character_info_table)
        self.update_map_info_table(self.map_two_file,self.jmp_item_info_table)
        self.update_map_info_table(self.map_two_file,self.jmp_item_appear_table)
        self.update_map_info_table(self.map_two_file,self.jmp_treasure_table)
        self.update_map_info_table(self.map_two_file,self.jmp_furniture_info_table)
        self.update_map_info_table(self.map_two_file,self.jmp_event_info_table)
        self.update_map_info_table(self.map_two_file,self.jmp_observer_info_table)
        self.update_map_info_table(self.map_two_file,self.jmp_key_info_table)
        self.update_map_info_table(self.map_two_file,self.jmp_obj_info_table)
        self.update_map_info_table(self.map_two_file,self.jmp_generator_info_table)
        self.update_map_info_table(self.map_two_file,self.jmp_enemy_info_table)
        self.update_map_info_table(self.map_two_file,self.jmp_teiden_observer_info_table)
        if self.output_data["Options"]["speedy_spirits"]:
            self.update_map_info_table(self.map_two_file,self.jmp_teiden_enemy_info_table)
        self.update_map_info_table(self.map_two_file,self.jmp_boo_table)
        self.update_map_info_table(self.map_two_file,self.jmp_iyapoo_table)
        self.update_map_info_table(self.map_three_file, self.jmp_map3_event_info_table)

    def save_randomized_iso(self):
        # Get Output data required information
        bool_boo_rando_enabled: bool = bool(self.output_data["Options"]["boosanity"])
        req_mario_count: str = str(self.output_data["Options"]["mario_items"])
        max_health: str = str(self.output_data["Options"]["luigi_max_health"])
        door_to_close_list: dict[int, int] = dict(self.output_data["Entrances"])
        start_inv_list: list[str] = list(self.output_data["Options"]["start_inventory"])
        bool_start_vacuum: bool = bool(self.output_data["Options"]["vacuum_start"])
        bool_randomize_music: bool = bool(self.output_data["Options"]["random_music"])
        bool_randomize_mice: bool = bool(self.output_data["Options"]["gold_mice"])
        bool_hidden_mansion: bool = bool(self.output_data["Options"]["hidden_mansion"])
        bool_start_boo_radar: bool = not bool(self.output_data["Options"]["boo_radar"])
        walk_speed: int = int(self.output_data["Options"]["walk_speed"])
        bool_pickup_anim_enabled: bool =  bool(self.output_data["Options"]["enable_fear_animation"])
        bool_fear_anim_enabled: bool = bool(self.output_data["Options"]["enable_pickup_animation"])
        player_name: str = str(self.output_data["Name"])
        king_boo_health: int = int(self.output_data["Options"]["king_boo_health"])
        random_spawn: str = str(self.output_data["Options"]["spawn"])
        door_model_rando_on: bool = bool(self.output_data["Options"]["door_model_rando"])
        bool_start_extra_vacuum: bool = not bool(self.output_data["Options"]["good_vacuum"])

        # Boo related options
        bool_boo_checks: bool = True if self.output_data["Options"]["boo_gates"] == 1 else False
        #washroom_boo_count: int = int(self.output_data["Options"]["washroom_boo_count"])
        balcony_boo_count: int = int(self.output_data["Options"]["balcony_boo_count"])
        final_boo_count: int = int(self.output_data["Options"]["final_boo_count"])

        # Hint options
        hint_dist: int = int(self.output_data["Options"]["hint_distribution"])
        hint_list: dict[str, dict[str, str]] = self.output_data["Hints"]
        madam_hint_dict: dict[str, str] = hint_list["Madame Clairvoya"] if "Madame Clairvoya" in hint_list else None
        bool_portrait_hints: bool = True if self.output_data["Options"]["portrait_hints"] == 1 else False

        logger.info("Updating all the main.dol offsets with their appropriate values.")
        self.gcm, self.dol = update_dol_offsets(self.gcm, self.dol, self.seed, bool_start_extra_vacuum, bool_start_vacuum,
            start_inv_list, walk_speed, player_name, random_spawn, king_boo_health, bool_fear_anim_enabled,
            bool_pickup_anim_enabled, bool_boo_rando_enabled, door_model_rando_on)

        logger.info("Updating all of the common events with the customized version.")
        self.gcm = update_common_events(self.gcm, bool_randomize_mice)

        logger.info("Updating the intro and lab events with the customized version.")
        self.gcm = update_intro_and_lab_events(self.gcm, bool_hidden_mansion, max_health, start_inv_list, bool_start_boo_radar,
            door_to_close_list, bool_start_vacuum)

        if bool_boo_checks:
            logger.info("Boo Gates was enabled, updating all of the common events with the customized version.")
            boo_list_events = ["16", "96"]
            str_move_type = None
            for event_no in boo_list_events:
                if event_no == "16":
                    required_boo_count = final_boo_count
                else:
                    required_boo_count = balcony_boo_count
                    str_move_type = "MOVEOUTSIDE" if str(self.output_data["Options"]["spawn"]) in \
                        FLIP_BALCONY_BOO_EVENT_LIST else "MOVEINSIDE"

                if required_boo_count == 0:
                    self.jmp_event_info_table.info_file_field_entries = list(filter(lambda info_entry: not (
                        info_entry["EventNo"] == int(event_no)), self.jmp_event_info_table.info_file_field_entries))
                    continue
                self.gcm = update_boo_gates(self.gcm, event_no, required_boo_count,
                    bool_boo_rando_enabled, str_move_type)

        logger.info("Updating the blackout event with the customized version.")
        self.gcm = update_blackout_event(self.gcm)

        logger.info("Updating Clairvoya's event with the customized version.")
        self.gcm = randomize_clairvoya(self.gcm, req_mario_count, hint_dist, madam_hint_dict, self.seed)

        logger.info("Updating common events with the generated in-game hints.")
        self.gcm = write_in_game_hints(self.gcm, hint_dist, hint_list, max_health, self.seed)

        logger.info("Updating the spawn event...")
        self.gcm = update_spawn_events(self.gcm)

        if bool_portrait_hints:
            logger.info("Portrait Hints are enabled, updating portrait ghost hearts with the generated in-game hints.")
            self.gcm = write_portrait_hints(self.gcm, hint_dist, hint_list, self.seed)

        if bool_randomize_music:
            logger.info("Randomized Music is enabled, updating all events with various in-game music.")
            self.gcm = randomize_music(self.gcm, self.seed)

        logger.info("Updating the in-game tables for chests, furniture, ghosts, etc.")
        self.update_map_jmp_tables()

        # Save the map two file changes
        # As mentioned before, these szp files need to be compressed again in order to be properly read by Dolphin/GC.
        # If you forget this, you will get an Invalid read error on a certain memory address typically.
        logger.info("Saving all files back into the main mansion file, then generating the new ISO file...")
        self.map_two_file.save_changes()
        logger.info("map2.szp Yay0 check...")
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
