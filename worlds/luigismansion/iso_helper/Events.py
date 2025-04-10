import re
from io import BytesIO
import random
from pkgutil import get_data

from gclib.gcm import GCM
from gclib.rarc import RARC, RARCNode, RARCFileEntry
from gclib.yaz0_yay0 import Yay0


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

def randomize_music(gcm: GCM, seed: str) -> GCM:
    list_ignore_events = ["event00.szp"]
    event_dir = gcm.get_or_create_dir_file_entry("files/Event")
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
                    random.seed(seed)
                    int_music_selection = random.randint(0, 52)
                event_str = event_str.replace(music_match, "<BGM>(" + str(int_music_selection) + ")")

        updated_event = BytesIO(event_str.encode('utf-8'))

        next(event_file for event_file in event_arc.file_entries if
             event_file.name == name_to_find).data = updated_event

        event_arc.save_changes()
        gcm.changed_files[lm_event.file_path] = Yay0.compress(event_arc.data)
    return gcm

def randomize_clairvoya(gcm: GCM, req_mario_count: str, hint_distribution_choice: int,
    madame_hint: dict[str, str], seed: str) -> GCM:
    # Update Madame Clairvoya's event to check mario items.
    lines = get_data(MAIN_PKG_NAME, "data/custom_events/event36.txt").decode('utf-8')
    csv_lines = get_data(MAIN_PKG_NAME, "data/custom_csvs/message36.csv").decode('utf-8')

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
            random.seed(seed)
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

    __update_custom_event_pre_loaded(gcm, "36", True, lines, csv_lines)
    return gcm

def __update_custom_event_pre_loaded(gcm: GCM, event_number: str, delete_all_other_files: bool,
    event_txt: str, event_csv=None):
    custom_event = get_arc(gcm, "files/Event/event" + event_number + ".szp")
    event_txt_file = "event" + event_number + ".txt"
    event_csv_file = "message" + (event_number if not event_number.startswith("0") else event_number[1:]) + ".csv"

    if not any(info_files for info_files in custom_event.file_entries if info_files.name == event_txt_file):
        raise Exception(f"Unable to find an info file with name '{event_txt_file}' in provided RARC file.")

    lines = BytesIO(event_txt.encode('utf-8'))
    next((info_files for info_files in custom_event.file_entries if info_files.name == event_txt_file)).data = lines

    if event_csv:
        if not any(info_files for info_files in custom_event.file_entries if info_files.name == event_csv_file):
            raise Exception(f"Unable to find an info file with name '{event_csv_file}' in provided RARC file.")
        lines = BytesIO(event_csv.encode('utf-8'))
        next((info_files for info_files in custom_event.file_entries if info_files.name == event_csv_file)).data = lines

    if delete_all_other_files:
        files_to_keep: list[str] = [event_txt_file, ".", ".."]
        if event_csv:
            files_to_keep += [event_csv_file]

        files_to_delete: {RARCFileEntry} = set(list(sub_path for sub_path in custom_event.file_entries if
            not sub_path.is_dir and sub_path.name not in files_to_keep))

        for delete_file in files_to_delete:
            custom_event.delete_file(delete_file)

        #TODO check for all directories being empty and delete them.

    custom_event.save_changes()
    gcm.changed_files["files/Event/event" + event_number + ".szp"] = Yay0.compress(custom_event.data)
    return gcm

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