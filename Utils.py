from __future__ import annotations

import shutil
import typing
import builtins
import os
import subprocess
import sys
import pickle
import functools
import io
import collections
import importlib
import logging

if typing.TYPE_CHECKING:
    from tkinter import Tk
else:
    Tk = typing.Any


def tuplize_version(version: str) -> Version:
    return Version(*(int(piece, 10) for piece in version.split(".")))


class Version(typing.NamedTuple):
    major: int
    minor: int
    build: int


__version__ = "0.3.3"
version_tuple = tuplize_version(__version__)

is_linux = sys.platform.startswith('linux')
is_macos = sys.platform == 'darwin'
is_windows = sys.platform in ("win32", "cygwin", "msys")

import jellyfish
from yaml import load, load_all, dump, SafeLoader

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def int16_as_bytes(value: int) -> typing.List[int]:
    value = value & 0xFFFF
    return [value & 0xFF, (value >> 8) & 0xFF]


def int32_as_bytes(value: int) -> typing.List[int]:
    value = value & 0xFFFFFFFF
    return [value & 0xFF, (value >> 8) & 0xFF, (value >> 16) & 0xFF, (value >> 24) & 0xFF]


def pc_to_snes(value: int) -> int:
    return ((value << 1) & 0x7F0000) | (value & 0x7FFF) | 0x8000


def snes_to_pc(value: int) -> int:
    return ((value & 0x7F0000) >> 1) | (value & 0x7FFF)


RetType = typing.TypeVar("RetType")


def cache_argsless(function: typing.Callable[[], RetType]) -> typing.Callable[[], RetType]:
    assert not function.__code__.co_argcount, "Can only cache 0 argument functions with this cache."

    sentinel = object()
    result: typing.Union[object, RetType] = sentinel

    def _wrap() -> RetType:
        nonlocal result
        if result is sentinel:
            result = function()
        return typing.cast(RetType, result)

    return _wrap


def is_frozen() -> bool:
    return typing.cast(bool, getattr(sys, 'frozen', False))


def local_path(*path: str) -> str:
    """Returns path to a file in the local Archipelago installation or source."""
    if hasattr(local_path, 'cached_path'):
        pass
    elif is_frozen():
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


def home_path(*path: str) -> str:
    """Returns path to a file in the user home's Archipelago directory."""
    if hasattr(home_path, 'cached_path'):
        pass
    elif sys.platform.startswith('linux'):
        home_path.cached_path = os.path.expanduser('~/Archipelago')
        os.makedirs(home_path.cached_path, 0o700, exist_ok=True)
    else:
        # not implemented
        home_path.cached_path = local_path()  # this will generate the same exceptions we got previously

    return os.path.join(home_path.cached_path, *path)


def user_path(*path: str) -> str:
    """Returns either local_path or home_path based on write permissions."""
    if hasattr(user_path, 'cached_path'):
        pass
    elif os.access(local_path(), os.W_OK):
        user_path.cached_path = local_path()
    else:
        user_path.cached_path = home_path()
        # populate home from local - TODO: upgrade feature
        if user_path.cached_path != local_path() and not os.path.exists(user_path('host.yaml')):
            for dn in ('Players', 'data/sprites'):
                shutil.copytree(local_path(dn), user_path(dn), dirs_exist_ok=True)
            for fn in ('manifest.json', 'host.yaml'):
                shutil.copy2(local_path(fn), user_path(fn))

    return os.path.join(user_path.cached_path, *path)


def output_path(*path: str):
    if hasattr(output_path, 'cached_path'):
        return os.path.join(output_path.cached_path, *path)
    output_path.cached_path = user_path(get_options()["general_options"]["output_path"])
    path = os.path.join(output_path.cached_path, *path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def open_file(filename):
    if sys.platform == 'win32':
        os.startfile(filename)
    else:
        open_command = 'open' if sys.platform == 'darwin' else 'xdg-open'
        subprocess.call([open_command, filename])


# from https://gist.github.com/pypt/94d747fe5180851196eb#gistcomment-4015118 with some changes
class UniqueKeyLoader(SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = set()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in mapping:
                logging.error(f"YAML duplicates sanity check failed{key_node.start_mark}")
                raise KeyError(f"Duplicate key {key} found in YAML. Already found keys: {mapping}.")
            mapping.add(key)
        return super().construct_mapping(node, deep)


parse_yaml = functools.partial(load, Loader=UniqueKeyLoader)
parse_yamls = functools.partial(load_all, Loader=UniqueKeyLoader)
unsafe_parse_yaml = functools.partial(load, Loader=Loader)


def get_cert_none_ssl_context():
    import ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


@cache_argsless
def get_public_ipv4() -> str:
    import socket
    import urllib.request
    ip = socket.gethostbyname(socket.gethostname())
    ctx = get_cert_none_ssl_context()
    try:
        ip = urllib.request.urlopen('https://checkip.amazonaws.com/', context=ctx).read().decode('utf8').strip()
    except Exception as e:
        try:
            ip = urllib.request.urlopen('https://v4.ident.me', context=ctx).read().decode('utf8').strip()
        except:
            logging.exception(e)
            pass  # we could be offline, in a local game, so no point in erroring out
    return ip


@cache_argsless
def get_public_ipv6() -> str:
    import socket
    import urllib.request
    ip = socket.gethostbyname(socket.gethostname())
    ctx = get_cert_none_ssl_context()
    try:
        ip = urllib.request.urlopen('https://v6.ident.me', context=ctx).read().decode('utf8').strip()
    except Exception as e:
        logging.exception(e)
        pass  # we could be offline, in a local game, or ipv6 may not be available
    return ip


@cache_argsless
def get_default_options() -> dict:
    # Refer to host.yaml for comments as to what all these options mean.
    options = {
        "general_options": {
            "output_path": "output",
        },
        "factorio_options": {
            "executable": os.path.join("factorio", "bin", "x64", "factorio"),
        },
        "sm_options": {
            "rom_file": "Super Metroid (JU).sfc",
            "sni": "SNI",
            "rom_start": True,
        },
        "soe_options": {
            "rom_file": "Secret of Evermore (USA).sfc",
        },
        "lttp_options": {
            "rom_file": "Zelda no Densetsu - Kamigami no Triforce (Japan).sfc",
            "sni": "SNI",
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
            "hint_cost": 10,
            "forfeit_mode": "goal",
            "collect_mode": "disabled",
            "remaining_mode": "goal",
            "auto_shutdown": 0,
            "compatibility": 2,
            "log_network": 0
        },
        "generator": {
            "teams": 1,
            "enemizer_path": os.path.join("EnemizerCLI", "EnemizerCLI.Core"),
            "player_files_path": "Players",
            "players": 0,
            "weights_file_path": "weights.yaml",
            "meta_file_path": "meta.yaml",
            "spoiler": 2,
            "glitch_triforce_room": 1,
            "race": 0,
            "plando_options": "bosses",
        },
        "minecraft_options": {
            "forge_directory": "Minecraft Forge server",
            "max_heap_size": "2G",
            "release_channel": "release"
        },
        "oot_options": {
            "rom_file": "The Legend of Zelda - Ocarina of Time.z64",
        }
    }

    return options


def update_options(src: dict, dest: dict, filename: str, keys: list) -> dict:
    for key, value in src.items():
        new_keys = keys.copy()
        new_keys.append(key)
        option_name = '.'.join(new_keys)
        if key not in dest:
            dest[key] = value
            if filename.endswith("options.yaml"):
                logging.info(f"Warning: {filename} is missing {option_name}")
        elif isinstance(value, dict):
            if not isinstance(dest.get(key, None), dict):
                if filename.endswith("options.yaml"):
                    logging.info(f"Warning: {filename} has {option_name}, but it is not a dictionary. overwriting.")
                dest[key] = value
            else:
                dest[key] = update_options(value, dest[key], filename, new_keys)
    return dest


@cache_argsless
def get_options() -> dict:
    if not hasattr(get_options, "options"):
        filenames = ("options.yaml", "host.yaml")
        locations = []
        if os.path.join(os.getcwd()) != local_path():
            locations += filenames  # use files from cwd only if it's not the local_path
        locations += [user_path(filename) for filename in filenames]

        for location in locations:
            if os.path.exists(location):
                with open(location) as f:
                    options = parse_yaml(f.read())

                get_options.options = update_options(get_default_options(), options, location, list())
                break
        else:
            raise FileNotFoundError(f"Could not find {filenames[1]} to load options.")
    return get_options.options


def get_item_name_from_id(code: int) -> str:
    from worlds import lookup_any_item_id_to_name
    return lookup_any_item_id_to_name.get(code, f'Unknown item (ID:{code})')


def get_location_name_from_id(code: int) -> str:
    from worlds import lookup_any_location_id_to_name
    return lookup_any_location_id_to_name.get(code, f'Unknown location (ID:{code})')


def persistent_store(category: str, key: typing.Any, value: typing.Any):
    path = user_path("_persistent_storage.yaml")
    storage: dict = persistent_load()
    category = storage.setdefault(category, {})
    category[key] = value
    with open(path, "wt") as f:
        f.write(dump(storage))


def persistent_load() -> typing.Dict[dict]:
    storage = getattr(persistent_load, "storage", None)
    if storage:
        return storage
    path = user_path("_persistent_storage.yaml")
    storage: dict = {}
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                storage = unsafe_parse_yaml(f.read())
        except Exception as e:
            logging.debug(f"Could not read store: {e}")
    if storage is None:
        storage = {}
    persistent_load.storage = storage
    return storage


def get_adjuster_settings(gameName: str):
    adjuster_settings = persistent_load().get("adjuster", {}).get(gameName, {})
    return adjuster_settings


@cache_argsless
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
    def __init__(self, *args, **kwargs):
        super(RestrictedUnpickler, self).__init__(*args, **kwargs)
        self.options_module = importlib.import_module("Options")
        self.net_utils_module = importlib.import_module("NetUtils")
        self.generic_properties_module = importlib.import_module("worlds.generic")

    def find_class(self, module, name):
        if module == "builtins" and name in safe_builtins:
            return getattr(builtins, name)
        # used by MultiServer -> savegame/multidata
        if module == "NetUtils" and name in {"NetworkItem", "ClientStatus", "Hint", "SlotType", "NetworkSlot"}:
            return getattr(self.net_utils_module, name)
        # Options and Plando are unpickled by WebHost -> Generate
        if module == "worlds.generic" and name in {"PlandoItem", "PlandoConnection"}:
            return getattr(self.generic_properties_module, name)
        if module.endswith("Options"):
            if module == "Options":
                mod = self.options_module
            else:
                mod = importlib.import_module(module)
            obj = getattr(mod, name)
            if issubclass(obj, self.options_module.Option):
                return obj
        # Forbid everything else.
        raise pickle.UnpicklingError("global '%s.%s' is forbidden" %
                                     (module, name))


def restricted_loads(s):
    """Helper function analogous to pickle.loads()."""
    return RestrictedUnpickler(io.BytesIO(s)).load()


class KeyedDefaultDict(collections.defaultdict):
    def __missing__(self, key):
        self[key] = value = self.default_factory(key)
        return value


def get_text_between(text: str, start: str, end: str) -> str:
    return text[text.index(start) + len(start): text.rindex(end)]


loglevel_mapping = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}


def init_logging(name: str, loglevel: typing.Union[str, int] = logging.INFO, write_mode: str = "w",
                 log_format: str = "[%(name)s at %(asctime)s]: %(message)s",
                 exception_logger: typing.Optional[str] = None):
    loglevel: int = loglevel_mapping.get(loglevel, loglevel)
    log_folder = user_path("logs")
    os.makedirs(log_folder, exist_ok=True)
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()
    root_logger.setLevel(loglevel)
    file_handler = logging.FileHandler(
        os.path.join(log_folder, f"{name}.txt"),
        write_mode,
        encoding="utf-8-sig")
    file_handler.setFormatter(logging.Formatter(log_format))
    root_logger.addHandler(file_handler)
    if sys.stdout:
        root_logger.addHandler(
            logging.StreamHandler(sys.stdout)
        )

    # Relay unhandled exceptions to logger.
    if not getattr(sys.excepthook, "_wrapped", False):  # skip if already modified
        orig_hook = sys.excepthook

        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            logging.getLogger(exception_logger).exception("Uncaught exception",
                                                          exc_info=(exc_type, exc_value, exc_traceback))
            return orig_hook(exc_type, exc_value, exc_traceback)

        handle_exception._wrapped = True

        sys.excepthook = handle_exception

    logging.info(f"Archipelago ({__version__}) logging initialized.")


def stream_input(stream, queue):
    def queuer():
        while 1:
            text = stream.readline().strip()
            if text:
                queue.put_nowait(text)

    from threading import Thread
    thread = Thread(target=queuer, name=f"Stream handler for {stream.name}", daemon=True)
    thread.start()
    return thread


def tkinter_center_window(window: Tk):
    window.update()
    xPos = int(window.winfo_screenwidth() / 2 - window.winfo_reqwidth() / 2)
    yPos = int(window.winfo_screenheight() / 2 - window.winfo_reqheight() / 2)
    window.geometry("+{}+{}".format(xPos, yPos))


class VersionException(Exception):
    pass


# noinspection PyPep8Naming
def format_SI_prefix(value, power=1000, power_labels=('', 'k', 'M', 'G', 'T', "P", "E", "Z", "Y")) -> str:
    n = 0

    while value > power:
        value /= power
        n += 1
    if type(value) == int:
        return f"{value} {power_labels[n]}"
    else:
        return f"{value:0.3f} {power_labels[n]}"


def get_fuzzy_ratio(word1: str, word2: str) -> float:
    return (1 - jellyfish.damerau_levenshtein_distance(word1.lower(), word2.lower())
            / max(len(word1), len(word2)))


def get_fuzzy_results(input_word: str, wordlist: typing.Sequence[str], limit: typing.Optional[int] = None) \
        -> typing.List[typing.Tuple[str, int]]:
    limit: int = limit if limit else len(wordlist)
    return list(
        map(
            lambda container: (container[0], int(container[1]*100)),  # convert up to limit to int %
            sorted(
                map(lambda candidate:
                    (candidate,  get_fuzzy_ratio(input_word, candidate)),
                    wordlist),
                key=lambda element: element[1],
                reverse=True)[0:limit]
        )
    )


def open_filename(title: str, filetypes: typing.Sequence[typing.Tuple[str, typing.Sequence[str]]]) \
        -> typing.Optional[str]:
    def run(*args: str):
        return subprocess.run(args, capture_output=True, text=True).stdout.split('\n', 1)[0] or None

    if is_linux:
        # prefer native dialog
        kdialog = shutil.which('kdialog')
        if kdialog:
            k_filters = '|'.join((f'{text} (*{" *".join(ext)})' for (text, ext) in filetypes))
            return run(kdialog, f'--title={title}', '--getopenfilename', '.', k_filters)
        zenity = shutil.which('zenity')
        if zenity:
            z_filters = (f'--file-filter={text} ({", ".join(ext)}) | *{" *".join(ext)}' for (text, ext) in filetypes)
            return run(zenity, f'--title={title}', '--file-selection', *z_filters)

    # fall back to tk
    try:
        import tkinter
        import tkinter.filedialog
    except Exception as e:
        logging.error('Could not load tkinter, which is likely not installed. '
                      f'This attempt was made because open_filename was used for "{title}".')
        raise e
    else:
        root = tkinter.Tk()
        root.withdraw()
        return tkinter.filedialog.askopenfilename(title=title, filetypes=((t[0], ' '.join(t[1])) for t in filetypes))


def messagebox(title: str, text: str, error: bool = False) -> None:
    def is_kivy_running():
        if 'kivy' in sys.modules:
            from kivy.app import App
            return App.get_running_app() is not None
        return False

    if is_kivy_running():
        from kvui import MessageBox
        MessageBox(title, text, error).open()
        return

    # fall back to tk
    try:
        import tkinter
        from tkinter.messagebox import showerror, showinfo
    except Exception as e:
        logging.error('Could not load tkinter, which is likely not installed. '
                      f'This attempt was made because messagebox was used for "{title}".')
        raise e
    else:
        root = tkinter.Tk()
        root.withdraw()
        showerror(title, text) if error else showinfo(title, text)
        root.update()
