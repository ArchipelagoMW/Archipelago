import re
from io import BytesIO
from random import randint

from gclib.gcm import GCM
from gclib.rarc import RARC
from gclib.yaz0_yay0 import Yay0


def randomize_music(gcm: GCM) -> GCM:
    list_ignore_events = ["event00.szp"]
    event_dir = gcm.get_or_create_dir_file_entry("files/Event")
    for lm_event in [event_file for event_file in event_dir.children if not event_file.is_dir]:
        if lm_event.name in list_ignore_events or not re.match(r"event\d+\.szp", lm_event.name):
            continue

        if lm_event.file_path in gcm.changed_files:
            lm_event_bytes = gcm.get_changed_file_data(lm_event.file_path)
        else:
            lm_event_bytes = gcm.read_file_data(lm_event.file_path)

        event_arc = RARC(lm_event_bytes)  # Automatically decompresses Yay0
        event_arc.read()

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
                    int_music_selection = randint(0, 52)
                event_str = event_str.replace(music_match, "<BGM>(" + str(int_music_selection) + ")")

        updated_event = BytesIO(event_str.encode('utf-8'))

        next(event_file for event_file in event_arc.file_entries if
             event_file.name == name_to_find).data = updated_event

        event_arc.save_changes()
        gcm.changed_files[lm_event.file_path] = Yay0.compress(event_arc.data)
    return gcm