import re
from io import BytesIO
import random
from pkgutil import get_data
from typing import Optional

from gclib.gcm import GCM
from gclib.rarc import RARC, RARCNode, RARCFileEntry
from gclib.yaz0_yay0 import Yay0

from .. import ALWAYS_HINT
from .. Hints import PORTRAIT_HINTS

MAIN_PKG_NAME = "worlds.luigismansion.LMGenerator"

# Get an ARC / RARC / SZP file from within the ISO / ROM
def get_arc(gcm: GCM, arc_path):
    arc_path = arc_path.replace("\\", "/")
    if arc_path in gcm.changed_files:
        arc = RARC(gcm.get_changed_file_data(arc_path))
    else:
        arc = RARC(gcm.read_file_data(arc_path))  # Automatically decompresses Yay0
    arc.read()
    return arc


def update_boo_gates(gcm: GCM, event_no: str, req_boo_count: int, boo_rando_enabled: bool,
    move_luigi: Optional[str]) -> GCM:

    lines = get_data(MAIN_PKG_NAME, "data/custom_events/event" + event_no + ".txt").decode('utf-8')
    if move_luigi:
        lines = lines.replace("{MoveType}", move_luigi)
    if boo_rando_enabled:
        str_begin_case = "not_enough"
        lines = lines.replace("{Count0}", str(0)).replace("{Count1}", str(0))
        lines = lines.replace("{Count2}", str(0)).replace("{Count3}", str(0))
        lines = lines.replace("{Count4}", str(req_boo_count)).replace("{CaseBegin}", str_begin_case)
        return __update_custom_event(gcm, event_no, True, lines, None)

    str_begin_case = "CheckBoos"
    lines = lines.replace("{CaseBegin}", str_begin_case)

    str_not_enough = "not_enough"
    str_boo_captured = "boos_captured"
    match req_boo_count:
        case 1:
            lines = lines.replace("{Count0}", "0")
            lines = lines.replace("{Count1}", str(req_boo_count))
            lines = lines.replace("{Count2}", str(req_boo_count))
            lines = lines.replace("{Count3}", str(req_boo_count))
            lines = lines.replace("{Count4}", str(req_boo_count))
            lines = lines.replace("{Case0}", str_not_enough)
            lines = lines.replace("{Case1}", str_boo_captured)
            lines = lines.replace("{Case2}", str_boo_captured)
            lines = lines.replace("{Case3}", str_boo_captured)
            lines = lines.replace("{Case4}", str_boo_captured)
        case 2:
            lines = lines.replace("{Count0}", "0")
            lines = lines.replace("{Count1}", "1")
            lines = lines.replace("{Count2}", str(req_boo_count))
            lines = lines.replace("{Count3}", str(req_boo_count))
            lines = lines.replace("{Count4}", str(req_boo_count))
            lines = lines.replace("{Case0}", str_not_enough)
            lines = lines.replace("{Case1}", str_not_enough)
            lines = lines.replace("{Case2}", str_boo_captured)
            lines = lines.replace("{Case3}", str_boo_captured)
            lines = lines.replace("{Case4}", str_boo_captured)
        case 3:
            lines = lines.replace("{Count0}", "0")
            lines = lines.replace("{Count1}", "1")
            lines = lines.replace("{Count2}", "2")
            lines = lines.replace("{Count3}", str(req_boo_count))
            lines = lines.replace("{Count4}", str(req_boo_count))
            lines = lines.replace("{Case0}", str_not_enough)
            lines = lines.replace("{Case1}", str_not_enough)
            lines = lines.replace("{Case2}", str_not_enough)
            lines = lines.replace("{Case3}", str_boo_captured)
            lines = lines.replace("{Case4}", str_boo_captured)
        case _:
            lines = lines.replace("{Count0}", str(req_boo_count - 4))
            lines = lines.replace("{Count1}", str(req_boo_count - 3))
            lines = lines.replace("{Count2}", str(req_boo_count - 2))
            lines = lines.replace("{Count3}", str(req_boo_count - 1))
            lines = lines.replace("{Count4}", str(req_boo_count))
            lines = lines.replace("{Case0}", str_not_enough)
            lines = lines.replace("{Case1}", str_not_enough)
            lines = lines.replace("{Case2}", str_not_enough)
            lines = lines.replace("{Case3}", str_not_enough)
            lines = lines.replace("{Case4}", str_boo_captured)

    return __update_custom_event(gcm, event_no, True, lines, None)

# Updates the event txt and csv for blackout
def update_blackout_event(gcm: GCM) -> GCM:
    lines = get_data(MAIN_PKG_NAME, "data/custom_events/event44.txt").decode('utf-8')
    csv_lines = get_data(MAIN_PKG_NAME, "data/custom_csvs/message44.csv").decode('utf-8')
    return __update_custom_event(gcm, "44", True, lines, csv_lines)

# Updates all common events
def update_common_events(gcm: GCM, randomize_mice: bool) -> GCM:
    list_custom_events = ["03", "22", "24", "29", "33", "35", "38", "50", "61", "64", "65",
     "66", "67", "68", "71", "72", "74", "75", "82", "86", "87", "88", "89", "90"]
    if randomize_mice:
        list_custom_events += ["95", "97", "98", "99", "100"]

    for custom_event in list_custom_events:
        lines = get_data(MAIN_PKG_NAME, "data/custom_events/event" + custom_event +".txt").decode('utf-8')
        gcm = __update_custom_event(gcm, custom_event, True, lines, None)

    return gcm

# Update the intro event and E. Gadd event as needed.
def update_intro_and_lab_events(gcm: GCM, hidden_mansion: bool, max_health: str, start_inv: list[str],
    doors_to_open: dict[int, int]) -> GCM:
    lines = get_data(MAIN_PKG_NAME, "data/custom_events/event08.txt").decode('utf-8')
    lines = lines.replace("{LUIGIMAXHP}", max_health)
    csv_lines = get_data(MAIN_PKG_NAME, "data/custom_csvs/message8.csv").decode('utf-8')
    gcm = __update_custom_event(gcm, "08", True, lines, csv_lines)

    lines = get_data(MAIN_PKG_NAME, "data/custom_events/event48.txt").decode('utf-8')
    lines = lines.replace("{MANSION_TYPE}", "<URALUIGI>" if hidden_mansion else "<OMOTELUIGI>")

    include_radar = ""
    if any("Boo Radar" in key for key in start_inv):
        include_radar = "<FLAGON>(73)\n<FLAGON>(75)"
    lines = lines.replace("{BOO RADAR}", include_radar)

    event_door_list: list[str] = []
    door_list: dict[int, int] = doors_to_open

    for event_door in door_list:
        event_door_list.append(("<KEYLOCK>" if door_list.get(event_door) == 0 else "<KEYUNLOCK>")+f"({event_door})\n")

    lines = lines.replace("{DOOR_LIST}", ''.join(event_door_list))
    lines = lines.replace("{LUIGIMAXHP}", max_health)

    return __update_custom_event(gcm, "48", False, lines, None)

# Randomizes all the music in all the event.txt files.
def randomize_music(gcm: GCM, seed: str) -> GCM:
    list_ignore_events = ["event00.szp"]
    event_dir = gcm.get_or_create_dir_file_entry("files/Event")
    random.seed(seed)

    for lm_event in [event_file for event_file in event_dir.children if not event_file.is_dir]:
        if lm_event.name in list_ignore_events or not re.match(r"event\d+\.szp", lm_event.name):
            continue

        event_arc = get_arc(gcm, lm_event.file_path)
        name_to_find = lm_event.name.replace(".szp", ".txt")

        if not any(event_file for event_file in event_arc.file_entries if event_file.name == name_to_find):
            continue

        event_text_data = next(event_file for event_file in event_arc.file_entries if
                                event_file.name == name_to_find).data
        event_str = event_text_data.getvalue().decode('utf-8', errors='replace')
        music_to_replace = re.findall(r'<BGM>\(\d+\)', event_str)

        if music_to_replace:
            for music_match in music_to_replace:
                list_of_bad_music = [-1, 13, 17, 21, 24, 28, 41]
                int_music_selection: int = -1
                while int_music_selection in list_of_bad_music:
                    int_music_selection = random.randint(0, 52)
                event_str = event_str.replace(music_match, "<BGM>(" + str(int_music_selection) + ")")

        updated_event = BytesIO(event_str.encode('utf-8'))

        next(event_file for event_file in event_arc.file_entries if
             event_file.name == name_to_find).data = updated_event

        event_arc.save_changes()
        gcm.changed_files[lm_event.file_path] = Yay0.compress(event_arc.data)
    return gcm

# Updates all portrait ghost hints, if the option is turned on.
def write_portrait_hints(gcm: GCM, hint_distribution_choice: int, all_hints: dict[str, dict[str,str]],
                        seed: str) -> GCM:
    csv_lines = get_data(MAIN_PKG_NAME, "data/custom_csvs/message78.csv").decode('utf-8')
    random.seed(seed)
    if hint_distribution_choice == 1:
        for portrait_name in PORTRAIT_HINTS:
            jokes = get_data(MAIN_PKG_NAME, "data/jokes.txt").decode('utf-8')
            joke_hint = random.choice(str.splitlines(jokes)).replace("\\\\n", "\n")
            csv_lines = csv_lines.replace(f"{portrait_name}", joke_hint)
    else:
        for portrait_name, portrait_hint in all_hints.items():
            if portrait_name not in PORTRAIT_HINTS:
                continue
            match hint_distribution_choice:
                case 4:
                    match portrait_hint["Class"]:
                        case "Prog":
                            item_color = "5"
                        case "Trap":
                            item_color = "2"
                        case _:
                            item_color = "6"
                    hintfo = (portrait_hint["Rec Player"]+"'s \n<COLOR>("+item_color+") "+portrait_hint["Item"]+
                              "\n<COLOR>(0) is somewhere in \n<COLOR>(3)"+portrait_hint["Send Player"]+"'s \n"+portrait_hint["Game"])
                    csv_lines = csv_lines.replace(f"{portrait_name}", hintfo)
                case _:
                    match portrait_hint["Class"]:
                        case "Prog":
                            item_color = "5"
                        case "Trap":
                            item_color = "2"
                        case _:
                            item_color = "6"
                    hintfo = (portrait_hint["Rec Player"]+"'s \n<COLOR>("+item_color+")"+portrait_hint["Item"]+
                              "\n<COLOR>(0) can be found at \n<COLOR>(1)"+portrait_hint["Send Player"]+"'s \n"+portrait_hint["Location"])
                    csv_lines = csv_lines.replace(f"{portrait_name}", hintfo)

    return __update_custom_event(gcm, "78", True, None, csv_lines)

# Updates clairvoya's hints and mario item information based on the options selected.
def randomize_clairvoya(gcm: GCM, req_mario_count: str, hint_distribution_choice: int,
    madame_hint: dict[str, str], seed: str) -> GCM:
    lines = get_data(MAIN_PKG_NAME, "data/custom_events/event36.txt").decode('utf-8')
    csv_lines = get_data(MAIN_PKG_NAME, "data/custom_csvs/message36.csv").decode('utf-8')
    random.seed(seed)

    match hint_distribution_choice:
        case 4:
            match madame_hint["Class"]:
                case "Prog":
                    item_color = "5"
                case "Trap":
                    item_color = "2"
                case _:
                    item_color = "6"
            csv_lines = csv_lines.replace("{RecPlayer}", madame_hint["Rec Player"])
            csv_lines = csv_lines.replace("{ItemColor}", item_color)
            csv_lines = csv_lines.replace("{ItemName}", madame_hint["Item"])
            csv_lines = csv_lines.replace("{SendPlayer}", madame_hint["Send Player"])
            csv_lines = csv_lines.replace("{WorldOrLoc}", madame_hint["Game"])
            case_type = "VagueHint"
        case 5:
            case_type = "DisabledHint"
        case 1:
            jokes = get_data(MAIN_PKG_NAME, "data/jokes.txt").decode('utf-8')
            joke_hint = random.choice(str.splitlines(jokes)).replace("\\\\n", "\n")
            csv_lines = csv_lines.replace("{JokeText}", joke_hint)
            case_type = "JokeHint"
        case _:
            match madame_hint["Class"]:
                case "Prog":
                    item_color = "5"
                case "Trap":
                    item_color = "2"
                case _:
                    item_color = "6"
            csv_lines = csv_lines.replace("{RecPlayer}", madame_hint["Rec Player"])
            csv_lines = csv_lines.replace("{ItemColor}", item_color)
            csv_lines = csv_lines.replace("{ItemName}", madame_hint["Item"])
            csv_lines = csv_lines.replace("{SendPlayer}", madame_hint["Send Player"])
            csv_lines = csv_lines.replace("{WorldOrLoc}", madame_hint["Location"])
            case_type = "SpecificHint"

    csv_lines = csv_lines.replace("{MarioCount}", req_mario_count)
    csv_lines = csv_lines.replace("{BreakHere}", "\n")
    lines = lines.replace("{HintType}", case_type)

    cases_to_replace = ["{CaseZero}", "{CaseOne}", "{CaseTwo}", "{CaseThree}", "{CaseFour}", "{CaseFive}"]
    str_good_end = "GoodEnd"
    str_bad_end = "MissingItems"

    for i in range(0, 6):
        if i >= int(req_mario_count):
            lines = lines.replace(cases_to_replace[i], str_good_end)
        else:
            lines = lines.replace(cases_to_replace[i], str_bad_end)

    return __update_custom_event(gcm, "36", True, lines, csv_lines)

# Writes all the in game hints for everything except clairvoya
def write_in_game_hints(gcm: GCM, hint_distribution_choice: int, all_hints: dict[str, dict[str, str]], maxhp: str,
    seed: str) -> GCM:
    random.seed(seed)

    for hint_name in ALWAYS_HINT:
        if hint_name == "Madame Clairvoya":
            continue
        event_no: int = 0
        match hint_name:
            case "Courtyard Toad":
                event_no = 4
            case "Foyer Toad":
                event_no = 17
            case "Wardrobe Balcony Toad":
                event_no = 32
            case "1F Washroom Toad":
                event_no = 63
            case "Center Telephone":
                event_no = 92
            case "Left Telephone":
                event_no = 93
            case "Right Telephone":
                event_no = 94
        if hint_distribution_choice != 1 and hint_distribution_choice != 5:
            hint_data = all_hints[hint_name]

        if event_no == 4:
            lines = get_data(MAIN_PKG_NAME, "data/custom_events/event04.txt").decode('utf-8')
        else:
            lines = get_data(MAIN_PKG_NAME, "data/custom_events/event"+str(event_no)+".txt").decode('utf-8')
        csv_lines = get_data(MAIN_PKG_NAME, "data/custom_csvs/message"+str(event_no)+".csv").decode('utf-8')

        match hint_distribution_choice:
            case 4:
                match hint_data["Class"]:
                    case "Prog":
                        item_color = "5"
                    case "Trap":
                        item_color = "2"
                    case _:
                        item_color = "6"
                csv_lines = csv_lines.replace("{RecPlayer}", hint_data["Rec Player"])
                csv_lines = csv_lines.replace("{ItemColor}", item_color)
                csv_lines = csv_lines.replace("{ItemName}", hint_data["Item"])
                csv_lines = csv_lines.replace("{SendPlayer}", hint_data["Send Player"])
                csv_lines = csv_lines.replace("{WorldOrLoc}", hint_data["Game"])
                case_type = "VagueHint"
            case 5:
                case_type = "DisabledHint"
            case 1:
                jokes = get_data(MAIN_PKG_NAME, "data/jokes.txt").decode('utf-8')
                joke_hint = random.choice(str.splitlines(jokes)).replace("\\\\n", "\n")
                csv_lines = csv_lines.replace("{JokeText}", joke_hint)
                case_type = "JokeHint"
            case _:
                match hint_data["Class"]:
                    case "Prog":
                        item_color = "5"
                    case "Trap":
                        item_color = "2"
                    case _:
                        item_color = "6"
                csv_lines = csv_lines.replace("{RecPlayer}", hint_data["Rec Player"])
                csv_lines = csv_lines.replace("{ItemColor}", item_color)
                csv_lines = csv_lines.replace("{ItemName}", hint_data["Item"])
                csv_lines = csv_lines.replace("{SendPlayer}", hint_data["Send Player"])
                csv_lines = csv_lines.replace("{WorldOrLoc}", hint_data["Location"])
                case_type = "SpecificHint"

        csv_lines = csv_lines.replace("{BreakHere}", "\n")
        lines = lines.replace("{HintType}", case_type)
        if event_no in [4, 17, 32, 63]:
            lines = lines.replace("{LUIGIMAXHP}", maxhp)

        if event_no == 4:
            gcm = __update_custom_event(gcm, "04", True, lines, csv_lines)
        else:
            gcm = __update_custom_event(gcm, str(event_no), True, lines, csv_lines)
    return gcm

# Update the spawn event info
def update_spawn_events(gcm: GCM) -> GCM:
    lines = get_data(MAIN_PKG_NAME, "data/custom_events/event11.txt").decode('utf-8')
    return __update_custom_event(gcm, "11", True, lines, None)

# Using the provided txt or csv lines for a given event file, updates the actual szp file in memory with this data.
def __update_custom_event(gcm: GCM, event_number: str, delete_all_other_files: bool,
    event_txt=None, event_csv=None) -> GCM:
    if not event_txt and not event_csv:
        raise Exception("Cannot have both the event text and csv text be null/empty.")

    custom_event = get_arc(gcm, "files/Event/event" + event_number + ".szp")
    event_txt_file = "event" + event_number + ".txt"
    event_csv_file = "message" + (event_number if not event_number.startswith("0") else event_number[1:]) + ".csv"

    if event_txt:
        if not any(info_files for info_files in custom_event.file_entries if info_files.name == event_txt_file):
            raise Exception(f"Unable to find an info file with name '{event_txt_file}' in provided RARC file.")
        lines = BytesIO(event_txt.encode('utf-8'))
        next((info_files for info_files in custom_event.file_entries if
              info_files.name == event_txt_file)).data = lines

    if event_csv:
        if not any(info_files for info_files in custom_event.file_entries if info_files.name == event_csv_file):
            raise Exception(f"Unable to find an info file with name '{event_csv_file}' in provided RARC file.")
        csv_lines = BytesIO(event_csv.encode('utf-8'))
        next((info_files for info_files in custom_event.file_entries if
              info_files.name == event_csv_file)).data = csv_lines

    custom_event.save_changes()

    if delete_all_other_files:
        files_to_keep: list[str] = [event_txt_file, ".", ".."]
        if event_csv:
            files_to_keep += [event_csv_file]

        files_to_delete: {RARCFileEntry} = set(list(sub_path for sub_path in custom_event.file_entries if
            not sub_path.is_dir and sub_path.name not in files_to_keep))

        for delete_file in files_to_delete:
            custom_event.delete_file(delete_file)

        #TODO check for all directories being empty and delete them.

    gcm.changed_files["files/Event/event" + event_number + ".szp"] = Yay0.compress(custom_event.data)
    return gcm

# Small function to identify all files that need to be deleted within a given event.
def __get_all_files_to_delete(custom_rarc: RARC, curr_dir_node: RARCNode, keep_file_list: list[str]) -> {RARCFileEntry}:
    files_to_delete: {RARCFileEntry} = set()
    directories_to_ignore = [".", ".."]
    for sub_path in curr_dir_node.files:
        if sub_path.name in directories_to_ignore:
            continue

        if sub_path.is_dir:
            __get_all_files_to_delete(custom_rarc, sub_path.node, keep_file_list)

        if sub_path.name not in keep_file_list:
            files_to_delete.difference_update([sub_path])
    return files_to_delete