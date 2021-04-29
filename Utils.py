from __future__ import annotations

import typing


def tuplize_version(version: str) -> typing.Tuple[int, ...]:
    return Version(*(int(piece, 10) for piece in version.split(".")))


class Version(typing.NamedTuple):
    major: int
    minor: int
    build: int

__version__ = "0.0.4"
_version_tuple = tuplize_version(__version__)

import builtins
import os
import subprocess
import sys
import pickle
import functools
import io

from yaml import load, dump, safe_load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def int16_as_bytes(value):
    value = value & 0xFFFF
    return [value & 0xFF, (value >> 8) & 0xFF]


def int32_as_bytes(value):
    value = value & 0xFFFFFFFF
    return [value & 0xFF, (value >> 8) & 0xFF, (value >> 16) & 0xFF, (value >> 24) & 0xFF]


def pc_to_snes(value):
    return ((value << 1) & 0x7F0000) | (value & 0x7FFF) | 0x8000


def snes_to_pc(value):
    return ((value & 0x7F0000) >> 1) | (value & 0x7FFF)


def parse_player_names(names, players, teams):
    names = tuple(n for n in (n.strip() for n in names.split(",")) if n)
    if len(names) != len(set(names)):
        import collections
        name_counter = collections.Counter(names)
        raise ValueError(f"Duplicate Player names is not supported, "
                         f'found multiple "{name_counter.most_common(1)[0][0]}".')
    ret = []
    while names or len(ret) < teams:
        team = [n[:16] for n in names[:players]]
        # 16 bytes in rom per player, which will map to more in unicode, but those characters later get filtered
        while len(team) != players:
            team.append(f"Player{len(team) + 1}")
        ret.append(team)

        names = names[players:]
    return ret


def is_bundled() -> bool:
    return getattr(sys, 'frozen', False)


def local_path(*path):
    if local_path.cached_path:
        return os.path.join(local_path.cached_path, *path)

    elif is_bundled():
        if hasattr(sys, "_MEIPASS"):
            # we are running in a PyInstaller bundle
            local_path.cached_path = sys._MEIPASS  # pylint: disable=protected-access,no-member
        else:
            # cx_Freeze
            local_path.cached_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        import __main__
        if hasattr(__main__, "__file__"):
            # we are running in a normal Python environment
            local_path.cached_path = os.path.dirname(os.path.abspath(__main__.__file__))
        else:
            # pray
            local_path.cached_path = os.path.abspath(".")

    return os.path.join(local_path.cached_path, *path)


local_path.cached_path = None


def output_path(*path):
    if output_path.cached_path:
        return os.path.join(output_path.cached_path, *path)
    output_path.cached_path = local_path(get_options()["general_options"]["output_path"])
    path = os.path.join(output_path.cached_path, *path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


output_path.cached_path = None


def open_file(filename):
    if sys.platform == 'win32':
        os.startfile(filename)
    else:
        open_command = 'open' if sys.platform == 'darwin' else 'xdg-open'
        subprocess.call([open_command, filename])


def close_console():
    if sys.platform == 'win32':
        # windows
        import ctypes.wintypes
        try:
            ctypes.windll.kernel32.FreeConsole()
        except Exception:
            pass


parse_yaml = safe_load
unsafe_parse_yaml = functools.partial(load, Loader=Loader)


def get_public_ipv4() -> str:
    import socket
    import urllib.request
    import logging
    ip = socket.gethostbyname(socket.gethostname())
    try:
        ip = urllib.request.urlopen('https://checkip.amazonaws.com/').read().decode('utf8').strip()
    except Exception as e:
        try:
            ip = urllib.request.urlopen('https://v4.ident.me').read().decode('utf8').strip()
        except:
            logging.exception(e)
            pass  # we could be offline, in a local game, so no point in erroring out
    return ip


def get_public_ipv6() -> str:
    import socket
    import urllib.request
    import logging
    ip = socket.gethostbyname(socket.gethostname())
    try:
        ip = urllib.request.urlopen('https://v6.ident.me').read().decode('utf8').strip()
    except Exception as e:
        logging.exception(e)
        pass  # we could be offline, in a local game, or ipv6 may not be available
    return ip


def get_default_options() -> dict:
    if not hasattr(get_default_options, "options"):
        # Refer to host.yaml for comments as to what all these options mean.
        options = {
            "general_options": {
                "output_path": "output",
            },
            "factorio_options": {
                "executable": "factorio\\bin\\x64\\factorio",
                "script-output": "factorio\\script-output",
            },
            "lttp_options": {
                "rom_file": "Zelda no Densetsu - Kamigami no Triforce (Japan).sfc",
                "qusb2snes": "QUsb2Snes\\QUsb2Snes.exe",
                "rom_start": True,

            },
            "server_options": {
                "host": None,
                "port": 38281,
                "password": None,
                "multidata": None,
                "savefile": None,
                "disable_save": False,
                "loglevel": "info",
                "server_password": None,
                "disable_item_cheat": False,
                "location_check_points": 1,
                "hint_cost": 1000,
                "forfeit_mode": "goal",
                "remaining_mode": "goal",
                "auto_shutdown": 0,
                "compatibility": 2,
                "log_network": 0
            },
            "multi_mystery_options": {
                "teams": 1,
                "enemizer_path": "EnemizerCLI/EnemizerCLI.Core.exe",
                "player_files_path": "Players",
                "players": 0,
                "weights_file_path": "weights.yaml",
                "meta_file_path": "meta.yaml",
                "pre_roll": False,
                "player_name": "",
                "create_spoiler": 1,
                "zip_roms": 0,
                "zip_diffs": 2,
                "zip_spoiler": 0,
                "zip_multidata": 1,
                "zip_format": 1,
                "glitch_triforce_room": 1,
                "race": 0,
                "cpu_threads": 0,
                "max_attempts": 0,
                "take_first_working": False,
                "keep_all_seeds": False,
                "log_output_path": "Output Logs",
                "log_level": None,
                "plando_options": "bosses",
            }
        }

        get_default_options.options = options
    return get_default_options.options


blacklisted_options = {"multi_mystery_options.cpu_threads",
                       "multi_mystery_options.max_attempts",
                       "multi_mystery_options.take_first_working",
                       "multi_mystery_options.keep_all_seeds",
                       "multi_mystery_options.log_output_path",
                       "multi_mystery_options.log_level"}


def update_options(src: dict, dest: dict, filename: str, keys: list) -> dict:
    import logging
    for key, value in src.items():
        new_keys = keys.copy()
        new_keys.append(key)
        option_name = '.'.join(new_keys)
        if key not in dest:
            dest[key] = value
            if filename.endswith("options.yaml") and option_name not in blacklisted_options:
                logging.info(f"Warning: {filename} is missing {option_name}")
        elif isinstance(value, dict):
            if not isinstance(dest.get(key, None), dict):
                if filename.endswith("options.yaml") and option_name not in blacklisted_options:
                    logging.info(f"Warning: {filename} has {option_name}, but it is not a dictionary. overwriting.")
                dest[key] = value
            else:
                dest[key] = update_options(value, dest[key], filename, new_keys)
    return dest


def get_options() -> dict:
    if not hasattr(get_options, "options"):
        locations = ("options.yaml", "host.yaml",
                     local_path("options.yaml"), local_path("host.yaml"))

        for location in locations:
            if os.path.exists(location):
                with open(location) as f:
                    options = parse_yaml(f.read())

                get_options.options = update_options(get_default_options(), options, location, list())
                break
        else:
            raise FileNotFoundError(f"Could not find {locations[1]} to load options.")
    return get_options.options


def get_item_name_from_id(code: int) -> str:
    from worlds import lookup_any_item_id_to_name
    return lookup_any_item_id_to_name.get(code, f'Unknown item (ID:{code})')


def get_location_name_from_id(code: int) -> str:
    from worlds import lookup_any_location_id_to_name
    return lookup_any_location_id_to_name.get(code, f'Unknown location (ID:{code})')


def persistent_store(category: str, key: typing.Any, value: typing.Any):
    path = local_path("_persistent_storage.yaml")
    storage: dict = persistent_load()
    category = storage.setdefault(category, {})
    category[key] = value
    with open(path, "wt") as f:
        f.write(dump(storage))


def persistent_load() -> typing.Dict[dict]:
    storage = getattr(persistent_load, "storage", None)
    if storage:
        return storage
    path = local_path("_persistent_storage.yaml")
    storage: dict = {}
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                storage = unsafe_parse_yaml(f.read())
        except Exception as e:
            import logging
            logging.debug(f"Could not read store: {e}")
    if storage is None:
        storage = {}
    persistent_load.storage = storage
    return storage


def get_adjuster_settings(romfile: str) -> typing.Tuple[str, bool]:
    if hasattr(get_adjuster_settings, "adjuster_settings"):
        adjuster_settings = getattr(get_adjuster_settings, "adjuster_settings")
    else:
        adjuster_settings = persistent_load().get("adjuster", {}).get("last_settings_3", {})

    if adjuster_settings:
        import pprint
        import Patch
        adjuster_settings.rom = romfile
        adjuster_settings.baserom = Patch.get_base_rom_path()
        adjuster_settings.world = None
        whitelist = {"disablemusic", "fastmenu", "heartbeep", "heartcolor", "ow_palettes", "quickswap",
                     "uw_palettes", "sprite"}
        printed_options = {name: value for name, value in vars(adjuster_settings).items() if name in whitelist}
        if hasattr(adjuster_settings, "sprite_pool"):
            sprite_pool = {}
            for sprite in getattr(adjuster_settings, "sprite_pool"):
                if sprite in sprite_pool:
                    sprite_pool[sprite] += 1
                else:
                    sprite_pool[sprite] = 1
            if sprite_pool:
                printed_options["sprite_pool"] = sprite_pool


        if hasattr(get_adjuster_settings, "adjust_wanted"):
            adjust_wanted = getattr(get_adjuster_settings, "adjust_wanted")
        elif persistent_load().get("adjuster", {}).get("never_adjust", False):  # never adjust, per user request
            return romfile, False
        else:
            adjust_wanted = input(f"Last used adjuster settings were found. Would you like to apply these? \n"
                                  f"{pprint.pformat(printed_options)}\n"
                                  f"Enter yes, no or never: ")
        if adjust_wanted and adjust_wanted.startswith("y"):
            if hasattr(adjuster_settings, "sprite_pool"):
                from Adjuster import AdjusterWorld
                adjuster_settings.world = AdjusterWorld(getattr(adjuster_settings, "sprite_pool"))

            adjusted = True
            import Adjuster
            _, romfile = Adjuster.adjust(adjuster_settings)

            if hasattr(adjuster_settings, "world"):
                delattr(adjuster_settings, "world")
        elif adjust_wanted and "never" in adjust_wanted:
            persistent_store("adjuster", "never_adjust", True)
            return romfile, False
        else:
            adjusted = False
            import logging
            if not hasattr(get_adjuster_settings, "adjust_wanted"):
                logging.info(f"Skipping post-patch adjustment")
        get_adjuster_settings.adjuster_settings = adjuster_settings
        get_adjuster_settings.adjust_wanted = adjust_wanted
        return romfile, adjusted
    return romfile, False


def get_unique_identifier():
    uuid = persistent_load().get("client", {}).get("uuid", None)
    if uuid:
        return uuid

    import uuid
    uuid = uuid.getnode()
    persistent_store("client", "uuid", uuid)
    return uuid


safe_builtins = {
    'set',
    'frozenset',
}


class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "builtins" and name in safe_builtins:
            return getattr(builtins, name)
        if module == "NetUtils" and name in {"NetworkItem", "ClientStatus", "Hint"}:
            import NetUtils
            return getattr(NetUtils, name)
        # Forbid everything else.
        raise pickle.UnpicklingError("global '%s.%s' is forbidden" %
                                     (module, name))


def restricted_loads(s):
    """Helper function analogous to pickle.loads()."""
    return RestrictedUnpickler(io.BytesIO(s)).load()