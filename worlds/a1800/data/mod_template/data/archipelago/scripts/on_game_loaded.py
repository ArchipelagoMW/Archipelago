import sys
from pathlib import Path

mod_path = Path.cwd() / "mods" / "{{ mod_name }}"
src_path = mod_path / "data" / "archipelago" / "scripts"

if not src_path in sys.path:
    sys.path.append(str(src_path))

try:
    from anno_server import AnnoServer
    from data import g_location_guid_data, ITEM_ID_TO_GUIDS

    g_victory = False

    try:
        anno_server.close()
    except NameError:
        pass

    anno_server = AnnoServer(globals(), mod_path / "A1800APCommunication.dat",
                             src_path, "{{ slot_name }}", "{{ seed_name }}")

    console.startScript(str(src_path / "data.lua"))
    console.startScript(str(src_path / "polling.lua"))
except Exception as e:
    import traceback
    traceback.print_exc()
