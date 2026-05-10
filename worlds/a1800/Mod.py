from collections.abc import Callable
from itertools import groupby
from os import walk
from os.path import dirname, join, relpath
from typing import Any, TYPE_CHECKING, Optional
from zipfile import ZipFile, ZIP_DEFLATED

import jinja2

from Utils import __version__, get_text_after
from worlds.Files import APPlayerContainer

from .Items import A1800Item, item_dict
from .Locations import A1800Location

if TYPE_CHECKING:
    from . import A1800World

_g_next_guid: int = 1701000000  # Start of Anno 1800 Archipelago Randomizer GUID range


def get_next_guid() -> int:
    global _g_next_guid
    _g_next_guid += 1
    return _g_next_guid


class A1800ModFile(APPlayerContainer):
    game = "A1800"
    compression_method = ZIP_DEFLATED
    writing_tasks: list[Callable[[], tuple[str, str | bytes]]]
    patch_file_ending = ".zip"

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.writing_tasks = []

    def write_contents(self, opened_zipfile: ZipFile):
        if not self.path:
            raise FileNotFoundError(f"Cannot write A1800ModFile due to no path provided.")

        mod_dir = self.path[:-4]  # cut off .zip

        for root, _, files in walk(mod_dir):
            for file in files:
                filename = join(root, file)
                opened_zipfile.write(filename, relpath(filename, join(mod_dir, '..')))

        for task in self.writing_tasks:
            target, content = task()
            opened_zipfile.writestr(target, content)

        super(A1800ModFile, self).write_contents(opened_zipfile)


def generate_mod(world: "A1800World", output_directory: str):
    player = world.player
    multiworld = world.multiworld

    def load_template(name: str):
        import pkgutil
        data = pkgutil.get_data(__name__, "data/mod_template/" + name)
        if data:
            return data.decode(), name, lambda: False
        else:
            return None

    template_env: Optional[jinja2.Environment] = \
        jinja2.Environment(loader=jinja2.FunctionLoader(load_template))

    modinfo_template = template_env.get_template("modinfo.json")
    readme_en_template = template_env.get_template("readme_en.md")
    readme_de_template = template_env.get_template("readme_de.md")
    data_py_template = template_env.get_template("data/archipelago/scripts/data.py")
    data_lua_template = template_env.get_template("data/archipelago/scripts/data.lua")
    on_game_loaded_template = template_env.get_template("data/archipelago/scripts/on_game_loaded.py")
    triggers_template = template_env.get_template("data/config/export/main/asset/triggers.include.xml")
    set_is_unlocked_template = template_env.get_template("data/archipelago/scripts/set_is_unlocked/set_is_unlocked.py")
    ap_receive_item_template = template_env.get_template(
        "data/archipelago/scripts/ap_receive_item/ap_receive_item.lua")

    # get data for templates
    mod_name = f"AP-{multiworld.seed_name}-P{player}-{multiworld.get_file_safe_player_name(player)}"
    versioned_mod_name = mod_name + "-" + __version__

    start_trigger_guid = get_next_guid()

    def trigger_key(location: A1800Location) -> tuple[int, int]:
        return location.data.population_guid or 0, location.data.amount or 0

    checkable_locations = [location for location in multiworld.get_filled_locations(
        player) if isinstance(location, A1800Location) and not location.is_event]
    trigger_to_locations = {get_next_guid(): (key, list(locations)) for key, locations in groupby(
        sorted(checkable_locations, key=trigger_key), key=trigger_key)}
    victory_trigger_guid = get_next_guid()

    def location_to_data(location: A1800Location) -> tuple[int, A1800Location, list[int]]:
        return (
            get_next_guid(),
            location,
            location.item.data.anno_guids[1] if isinstance(location.item, A1800Item) else []
        )

    trigger_to_location_data = {guid: (trigger, list(map(location_to_data, locations)))
                                for guid, (trigger, locations) in trigger_to_locations.items()}

    location_guid_data = {location_guid: (location.address, False) for _,
                          (_, locations) in trigger_to_location_data.items() for location_guid, location, _ in locations}

    item_id_to_guids = {data.ap_code: (data.anno_guids[1], 0) for _, data in item_dict.items() if not data.is_event and data.ap_code} | {location.item.code: (
        unlock_guids, location_guid) for _, (_, locations) in trigger_to_location_data.items() for location_guid, location, unlock_guids in locations if location.item and location.item.code}

    victory_location = next((location for location in multiworld.get_filled_locations(player)
                             if location.name == "Victory Condition"), None)
    victory_location = victory_location if isinstance(victory_location, A1800Location) else None
    victory_guid = get_next_guid()
    victory_condition = (victory_trigger_guid, victory_location.data.population_guid, victory_location.data.amount,
                         victory_guid) if victory_location else (victory_trigger_guid, 0, 0, victory_guid)

    template_data: dict[str, Any] = {
        "lock_guid_list": set([guid for _, data in item_dict.items() if not data.is_event for guid in data.anno_guids[0]]),
        "trigger_to_location_data": trigger_to_location_data,
        "location_guid_data": location_guid_data,
        "item_id_to_guids": item_id_to_guids,
        "start_trigger_guid": start_trigger_guid,
        "starting_guids": set([guid for item in multiworld.precollected_items[player] if isinstance(item, A1800Item)
                               for guid in item.data.anno_guids[1]]),
        "victory_condition": victory_condition,
        "mod_name": versioned_mod_name,
        "ap_version": __version__,
        "slot_name": world.player_name,
        "seed_name": multiworld.seed_name,
    }

    zipfile_path = join(output_directory, versioned_mod_name + ".zip")
    mod = A1800ModFile(zipfile_path, player=player, player_name=world.player_name)

    if world.zip_path:
        with ZipFile(world.zip_path) as zipfile:
            for file in zipfile.infolist():
                if not file.is_dir() and "/data/mod/" in file.filename:
                    file_path = get_text_after(file.filename, "/data/mod/")
                    mod.writing_tasks.append(lambda arcpath=file_path, content=zipfile.read(file): (arcpath, content))
    else:
        basepath = join(dirname(__file__), "data", "mod")
        for dirpath, _, filenames in walk(basepath):
            base_arc_path = (relpath(dirpath, basepath)).rstrip("/.\\")
            for filename in filenames:
                mod.writing_tasks.append(lambda arcpath=(base_arc_path + "/" + filename),
                                         file_path=join(dirpath, filename): (arcpath, open(file_path, "rb").read()))

    mod.writing_tasks.append(lambda: ("modinfo.json", modinfo_template.render(**template_data)))
    mod.writing_tasks.append(lambda: ("readme_en.md", readme_en_template.render(**template_data)))
    mod.writing_tasks.append(lambda: ("readme_de.md", readme_de_template.render(**template_data)))
    mod.writing_tasks.append(lambda: ("data/archipelago/scripts/data.py", data_py_template.render(**template_data)))
    mod.writing_tasks.append(lambda: ("data/archipelago/scripts/data.lua", data_lua_template.render(**template_data)))
    mod.writing_tasks.append(lambda: ("data/archipelago/scripts/on_game_loaded.py",
                             on_game_loaded_template.render(**template_data)))
    mod.writing_tasks.append(lambda: ("data/config/export/main/asset/triggers.include.xml",
                             triggers_template.render(**template_data)))

    for location_guid in location_guid_data.keys():
        set_is_unlocked_data: dict[str, Any] = {
            "unlocked_guid": location_guid,
            "victory": False,
        }
        mod.writing_tasks.append(lambda location_guid=location_guid, set_is_unlocked_data=set_is_unlocked_data: (
            f"data/archipelago/scripts/set_is_unlocked/set_is_unlocked_{location_guid}.py", set_is_unlocked_template.render(**set_is_unlocked_data)))

    set_is_unlocked_data: dict[str, Any] = {
        "unlocked_guid": victory_guid,
        "victory": True,
    }
    mod.writing_tasks.append(lambda victory_guid=victory_guid, set_is_unlocked_data=set_is_unlocked_data: (
        f"data/archipelago/scripts/set_is_unlocked/set_is_unlocked_{victory_guid}.py", set_is_unlocked_template.render(**set_is_unlocked_data)))

    for item_id, (unlock_guids, location_guid) in item_id_to_guids.items():
        ap_receive_item_data: dict[str, Any] = {
            "unlock_guids": unlock_guids,
            "location_guid": location_guid,
        }
        mod.writing_tasks.append(lambda item_id=item_id, ap_receive_item_data=ap_receive_item_data: (
            f"data/archipelago/scripts/ap_receive_item/ap_receive_item_{item_id}.lua", ap_receive_item_template.render(**ap_receive_item_data)))

    # write the mod file
    mod.write()
