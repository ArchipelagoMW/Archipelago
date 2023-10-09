from __future__ import annotations

import asyncio
import json
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
import warnings

from argparse import Namespace
from settings import Settings, get_settings
from typing import BinaryIO, Coroutine, Optional, Set, Dict, Any, Union
from yaml import load, load_all, dump, SafeLoader

try:
    from yaml import CLoader as UnsafeLoader
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Loader as UnsafeLoader
    from yaml import Dumper

if typing.TYPE_CHECKING:
    import tkinter
    import pathlib
    from BaseClasses import Region


def tuplize_version(version: str) -> Version:
    return Version(*(int(piece, 10) for piece in version.split(".")))


class Version(typing.NamedTuple):
    major: int
    minor: int
    build: int

    def as_simple_string(self) -> str:
        return ".".join(str(item) for item in self)


__version__ = "0.4.3"
version_tuple = tuplize_version(__version__)

is_linux = sys.platform.startswith("linux")
is_macos = sys.platform == "darwin"
is_windows = sys.platform in ("win32", "cygwin", "msys")


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
    """
    Returns path to a file in the local Archipelago installation or source.
    This might be read-only and user_path should be used instead for ROMs, configuration, etc.
    """
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
        if hasattr(__main__, "__file__") and os.path.isfile(__main__.__file__):
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
    if hasattr(user_path, "cached_path"):
        pass
    elif os.access(local_path(), os.W_OK):
        user_path.cached_path = local_path()
    else:
        user_path.cached_path = home_path()
        # populate home from local
        if user_path.cached_path != local_path():
            import filecmp
            if not os.path.exists(user_path("manifest.json")) or \
                    not filecmp.cmp(local_path("manifest.json"), user_path("manifest.json"), shallow=True):
                import shutil
                for dn in ("Players", "data/sprites"):
                    shutil.copytree(local_path(dn), user_path(dn), dirs_exist_ok=True)
                for fn in ("manifest.json",):
                    shutil.copy2(local_path(fn), user_path(fn))

    return os.path.join(user_path.cached_path, *path)


def cache_path(*path: str) -> str:
    """Returns path to a file in the user's Archipelago cache directory."""
    if hasattr(cache_path, "cached_path"):
        pass
    else:
        import platformdirs
        cache_path.cached_path = platformdirs.user_cache_dir("Archipelago", False)

    return os.path.join(cache_path.cached_path, *path)


def output_path(*path: str) -> str:
    if hasattr(output_path, 'cached_path'):
        return os.path.join(output_path.cached_path, *path)
    output_path.cached_path = user_path(get_options()["general_options"]["output_path"])
    path = os.path.join(output_path.cached_path, *path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def open_file(filename: typing.Union[str, "pathlib.Path"]) -> None:
    if is_windows:
        os.startfile(filename)
    else:
        from shutil import which
        open_command = which("open") if is_macos else (which("xdg-open") or which("gnome-open") or which("kde-open"))
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
unsafe_parse_yaml = functools.partial(load, Loader=UnsafeLoader)

del load, load_all  # should not be used. don't leak their names


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
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        # if hostname or resolvconf is not set up properly, this may fail
        warnings.warn("Could not resolve own hostname, falling back to 127.0.0.1")
        ip = "127.0.0.1"

    ctx = get_cert_none_ssl_context()
    try:
        ip = urllib.request.urlopen("https://checkip.amazonaws.com/", context=ctx, timeout=10).read().decode("utf8").strip()
    except Exception as e:
        # noinspection PyBroadException
        try:
            ip = urllib.request.urlopen("https://v4.ident.me", context=ctx, timeout=10).read().decode("utf8").strip()
        except Exception:
            logging.exception(e)
            pass  # we could be offline, in a local game, so no point in erroring out
    return ip


@cache_argsless
def get_public_ipv6() -> str:
    import socket
    import urllib.request
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        # if hostname or resolvconf is not set up properly, this may fail
        warnings.warn("Could not resolve own hostname, falling back to ::1")
        ip = "::1"

    ctx = get_cert_none_ssl_context()
    try:
        ip = urllib.request.urlopen("https://v6.ident.me", context=ctx, timeout=10).read().decode("utf8").strip()
    except Exception as e:
        logging.exception(e)
        pass  # we could be offline, in a local game, or ipv6 may not be available
    return ip


OptionsType = Settings  # TODO: remove ~2 versions after 0.4.1


@cache_argsless
def get_default_options() -> Settings:  # TODO: remove ~2 versions after 0.4.1
    return Settings(None)


get_options = get_settings  # TODO: add a warning ~2 versions after 0.4.1 and remove once all games are ported


def persistent_store(category: str, key: typing.Any, value: typing.Any):
    path = user_path("_persistent_storage.yaml")
    storage: dict = persistent_load()
    category = storage.setdefault(category, {})
    category[key] = value
    with open(path, "wt") as f:
        f.write(dump(storage, Dumper=Dumper))


def persistent_load() -> typing.Dict[str, dict]:
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


def get_file_safe_name(name: str) -> str:
    return "".join(c for c in name if c not in '<>:"/\\|?*')


def load_data_package_for_checksum(game: str, checksum: typing.Optional[str]) -> Dict[str, Any]:
    if checksum and game:
        if checksum != get_file_safe_name(checksum):
            raise ValueError(f"Bad symbols in checksum: {checksum}")
        path = cache_path("datapackage", get_file_safe_name(game), f"{checksum}.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8-sig") as f:
                    return json.load(f)
            except Exception as e:
                logging.debug(f"Could not load data package: {e}")

    # fall back to old cache
    cache = persistent_load().get("datapackage", {}).get("games", {}).get(game, {})
    if cache.get("checksum") == checksum:
        return cache

    # cache does not match
    return {}


def store_data_package_for_checksum(game: str, data: typing.Dict[str, Any]) -> None:
    checksum = data.get("checksum")
    if checksum and game:
        if checksum != get_file_safe_name(checksum):
            raise ValueError(f"Bad symbols in checksum: {checksum}")
        game_folder = cache_path("datapackage", get_file_safe_name(game))
        os.makedirs(game_folder, exist_ok=True)
        try:
            with open(os.path.join(game_folder, f"{checksum}.json"), "w", encoding="utf-8-sig") as f:
                json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        except Exception as e:
            logging.debug(f"Could not store data package: {e}")

def get_default_adjuster_settings(game_name: str) -> Namespace:
    import LttPAdjuster
    adjuster_settings = Namespace()
    if game_name == LttPAdjuster.GAME_ALTTP:
        return LttPAdjuster.get_argparser().parse_known_args(args=[])[0]

    return adjuster_settings


def get_adjuster_settings_no_defaults(game_name: str) -> Namespace:
    return persistent_load().get("adjuster", {}).get(game_name, Namespace())


def get_adjuster_settings(game_name: str) -> Namespace:
    adjuster_settings = get_adjuster_settings_no_defaults(game_name)
    default_settings = get_default_adjuster_settings(game_name)

    # Fill in any arguments from the argparser that we haven't seen before
    return Namespace(**vars(adjuster_settings), **{k:v for k,v in vars(default_settings).items() if k not in vars(adjuster_settings)})


@cache_argsless
def get_unique_identifier():
    uuid = persistent_load().get("client", {}).get("uuid", None)
    if uuid:
        return uuid

    import uuid
    uuid = uuid.getnode()
    persistent_store("client", "uuid", uuid)
    return uuid


safe_builtins = frozenset((
    'set',
    'frozenset',
))


class RestrictedUnpickler(pickle.Unpickler):
    generic_properties_module: Optional[object]

    def __init__(self, *args, **kwargs):
        super(RestrictedUnpickler, self).__init__(*args, **kwargs)
        self.options_module = importlib.import_module("Options")
        self.net_utils_module = importlib.import_module("NetUtils")
        self.generic_properties_module = None

    def find_class(self, module, name):
        if module == "builtins" and name in safe_builtins:
            return getattr(builtins, name)
        # used by MultiServer -> savegame/multidata
        if module == "NetUtils" and name in {"NetworkItem", "ClientStatus", "Hint", "SlotType", "NetworkSlot"}:
            return getattr(self.net_utils_module, name)
        # Options and Plando are unpickled by WebHost -> Generate
        if module == "worlds.generic" and name in {"PlandoItem", "PlandoConnection"}:
            if not self.generic_properties_module:
                self.generic_properties_module = importlib.import_module("worlds.generic")
            return getattr(self.generic_properties_module, name)
        # pep 8 specifies that modules should have "all-lowercase names" (options, not Options)
        if module.lower().endswith("options"):
            if module == "Options":
                mod = self.options_module
            else:
                mod = importlib.import_module(module)
            obj = getattr(mod, name)
            if issubclass(obj, self.options_module.Option):
                return obj
        # Forbid everything else.
        raise pickle.UnpicklingError(f"global '{module}.{name}' is forbidden")


def restricted_loads(s):
    """Helper function analogous to pickle.loads()."""
    return RestrictedUnpickler(io.BytesIO(s)).load()


class ByValue:
    """
    Mixin for enums to pickle value instead of name (restores pre-3.11 behavior). Use as left-most parent.
    See https://github.com/python/cpython/pull/26658 for why this exists.
    """
    def __reduce_ex__(self, prot):
        return self.__class__, (self._value_, )


class KeyedDefaultDict(collections.defaultdict):
    """defaultdict variant that uses the missing key as argument to default_factory"""
    default_factory: typing.Callable[[typing.Any], typing.Any]

    def __missing__(self, key):
        self[key] = value = self.default_factory(key)
        return value


def get_text_between(text: str, start: str, end: str) -> str:
    return text[text.index(start) + len(start): text.rindex(end)]


def get_text_after(text: str, start: str) -> str:
    return text[text.index(start) + len(start):]


loglevel_mapping = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}


def init_logging(name: str, loglevel: typing.Union[str, int] = logging.INFO, write_mode: str = "w",
                 log_format: str = "[%(name)s at %(asctime)s]: %(message)s",
                 exception_logger: typing.Optional[str] = None):
    import datetime
    loglevel: int = loglevel_mapping.get(loglevel, loglevel)
    log_folder = user_path("logs")
    os.makedirs(log_folder, exist_ok=True)
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()
    root_logger.setLevel(loglevel)
    logging.getLogger("websockets").setLevel(loglevel)  # make sure level is applied for websockets
    if "a" not in write_mode:
        name += f"_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
    file_handler = logging.FileHandler(
        os.path.join(log_folder, f"{name}.txt"),
        write_mode,
        encoding="utf-8-sig")
    file_handler.setFormatter(logging.Formatter(log_format))

    class Filter(logging.Filter):
        def __init__(self, filter_name, condition):
            super().__init__(filter_name)
            self.condition = condition

        def filter(self, record: logging.LogRecord) -> bool:
            return self.condition(record)

    file_handler.addFilter(Filter("NoStream", lambda record: not getattr(record,  "NoFile", False)))
    root_logger.addHandler(file_handler)
    if sys.stdout:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.addFilter(Filter("NoFile", lambda record: not getattr(record, "NoStream", False)))
        root_logger.addHandler(stream_handler)

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

    def _cleanup():
        for file in os.scandir(log_folder):
            if file.name.endswith(".txt"):
                last_change = datetime.datetime.fromtimestamp(file.stat().st_mtime)
                if datetime.datetime.now() - last_change > datetime.timedelta(days=7):
                    try:
                        os.unlink(file.path)
                    except Exception as e:
                        logging.exception(e)
                    else:
                        logging.debug(f"Deleted old logfile {file.path}")
    import threading
    threading.Thread(target=_cleanup, name="LogCleaner").start()
    import platform
    logging.info(
        f"Archipelago ({__version__}) logging initialized"
        f" on {platform.platform()}"
        f" running Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )


def stream_input(stream, queue):
    def queuer():
        while 1:
            try:
                text = stream.readline().strip()
            except UnicodeDecodeError as e:
                logging.exception(e)
            else:
                if text:
                    queue.put_nowait(text)

    from threading import Thread
    thread = Thread(target=queuer, name=f"Stream handler for {stream.name}", daemon=True)
    thread.start()
    return thread


def tkinter_center_window(window: "tkinter.Tk") -> None:
    window.update()
    x = int(window.winfo_screenwidth() / 2 - window.winfo_reqwidth() / 2)
    y = int(window.winfo_screenheight() / 2 - window.winfo_reqheight() / 2)
    window.geometry(f"+{x}+{y}")


class VersionException(Exception):
    pass


def chaining_prefix(index: int, labels: typing.Tuple[str]) -> str:
    text = ""
    max_label = len(labels) - 1
    while index > max_label:
        text += labels[-1]
        index -= max_label
    return labels[index] + text


# noinspection PyPep8Naming
def format_SI_prefix(value, power=1000, power_labels=("", "k", "M", "G", "T", "P", "E", "Z", "Y")) -> str:
    """Formats a value into a value + metric/si prefix. More info at https://en.wikipedia.org/wiki/Metric_prefix"""
    import decimal
    n = 0
    value = decimal.Decimal(value)
    limit = power - decimal.Decimal("0.005")
    while value >= limit:
        value /= power
        n += 1

    return f"{value.quantize(decimal.Decimal('1.00'))} {chaining_prefix(n, power_labels)}"


def get_fuzzy_results(input_word: str, wordlist: typing.Sequence[str], limit: typing.Optional[int] = None) \
        -> typing.List[typing.Tuple[str, int]]:
    import jellyfish

    def get_fuzzy_ratio(word1: str, word2: str) -> float:
        return (1 - jellyfish.damerau_levenshtein_distance(word1.lower(), word2.lower())
                / max(len(word1), len(word2)))

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


def open_filename(title: str, filetypes: typing.Sequence[typing.Tuple[str, typing.Sequence[str]]], suggest: str = "") \
        -> typing.Optional[str]:
    def run(*args: str):
        return subprocess.run(args, capture_output=True, text=True).stdout.split("\n", 1)[0] or None

    if is_linux:
        # prefer native dialog
        from shutil import which
        kdialog = which("kdialog")
        if kdialog:
            k_filters = '|'.join((f'{text} (*{" *".join(ext)})' for (text, ext) in filetypes))
            return run(kdialog, f"--title={title}", "--getopenfilename", suggest or ".", k_filters)
        zenity = which("zenity")
        if zenity:
            z_filters = (f'--file-filter={text} ({", ".join(ext)}) | *{" *".join(ext)}' for (text, ext) in filetypes)
            selection = (f"--filename={suggest}",) if suggest else ()
            return run(zenity, f"--title={title}", "--file-selection", *z_filters, *selection)

    # fall back to tk
    try:
        import tkinter
        import tkinter.filedialog
    except Exception as e:
        logging.error('Could not load tkinter, which is likely not installed. '
                      f'This attempt was made because open_filename was used for "{title}".')
        raise e
    else:
        try:
            root = tkinter.Tk()
        except tkinter.TclError:
            return None  # GUI not available. None is the same as a user clicking "cancel"
        root.withdraw()
        return tkinter.filedialog.askopenfilename(title=title, filetypes=((t[0], ' '.join(t[1])) for t in filetypes),
                                                  initialfile=suggest or None)


def open_directory(title: str, suggest: str = "") -> typing.Optional[str]:
    def run(*args: str):
        return subprocess.run(args, capture_output=True, text=True).stdout.split("\n", 1)[0] or None

    if is_linux:
        # prefer native dialog
        from shutil import which
        kdialog = which("kdialog")
        if kdialog:
            return run(kdialog, f"--title={title}", "--getexistingdirectory",
                       os.path.abspath(suggest) if suggest else ".")
        zenity = which("zenity")
        if zenity:
            z_filters = ("--directory",)
            selection = (f"--filename={os.path.abspath(suggest)}/",) if suggest else ()
            return run(zenity, f"--title={title}", "--file-selection", *z_filters, *selection)

    # fall back to tk
    try:
        import tkinter
        import tkinter.filedialog
    except Exception as e:
        logging.error('Could not load tkinter, which is likely not installed. '
                      f'This attempt was made because open_filename was used for "{title}".')
        raise e
    else:
        try:
            root = tkinter.Tk()
        except tkinter.TclError:
            return None  # GUI not available. None is the same as a user clicking "cancel"
        root.withdraw()
        return tkinter.filedialog.askdirectory(title=title, mustexist=True, initialdir=suggest or None)


def messagebox(title: str, text: str, error: bool = False) -> None:
    def run(*args: str):
        return subprocess.run(args, capture_output=True, text=True).stdout.split("\n", 1)[0] or None

    def is_kivy_running():
        if "kivy" in sys.modules:
            from kivy.app import App
            return App.get_running_app() is not None
        return False

    if is_kivy_running():
        from kvui import MessageBox
        MessageBox(title, text, error).open()
        return

    if is_linux and "tkinter" not in sys.modules:
        # prefer native dialog
        from shutil import which
        kdialog = which("kdialog")
        if kdialog:
            return run(kdialog, f"--title={title}", "--error" if error else "--msgbox", text)
        zenity = which("zenity")
        if zenity:
            return run(zenity, f"--title={title}", f"--text={text}", "--error" if error else "--info")

    elif is_windows:
        import ctypes
        style = 0x10 if error else 0x0
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)
    
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


def title_sorted(data: typing.Sequence, key=None, ignore: typing.Set = frozenset(("a", "the"))):
    """Sorts a sequence of text ignoring typical articles like "a" or "the" in the beginning."""
    def sorter(element: Union[str, Dict[str, Any]]) -> str:
        if (not isinstance(element, str)):
            element = element["title"]

        parts = element.split(maxsplit=1)
        if parts[0].lower() in ignore:
            return parts[1].lower()
        else:
            return element.lower()
    return sorted(data, key=lambda i: sorter(key(i)) if key else sorter(i))


def read_snes_rom(stream: BinaryIO, strip_header: bool = True) -> bytearray:
    """Reads rom into bytearray and optionally strips off any smc header"""
    buffer = bytearray(stream.read())
    if strip_header and len(buffer) % 0x400 == 0x200:
        return buffer[0x200:]
    return buffer


_faf_tasks: "Set[asyncio.Task[typing.Any]]" = set()


def async_start(co: Coroutine[None, None, typing.Any], name: Optional[str] = None) -> None:
    """
    Use this to start a task when you don't keep a reference to it or immediately await it,
    to prevent early garbage collection. "fire-and-forget"
    """
    # https://docs.python.org/3.10/library/asyncio-task.html#asyncio.create_task
    # Python docs:
    # ```
    # Important: Save a reference to the result of [asyncio.create_task],
    # to avoid a task disappearing mid-execution.
    # ```
    # This implementation follows the pattern given in that documentation.

    task: asyncio.Task[typing.Any] = asyncio.create_task(co, name=name)
    _faf_tasks.add(task)
    task.add_done_callback(_faf_tasks.discard)


def deprecate(message: str):
    if __debug__:
        raise Exception(message)
    import warnings
    warnings.warn(message)

def _extend_freeze_support() -> None:
    """Extend multiprocessing.freeze_support() to also work on Non-Windows for spawn."""
    # upstream issue: https://github.com/python/cpython/issues/76327
    # code based on https://github.com/pyinstaller/pyinstaller/blob/develop/PyInstaller/hooks/rthooks/pyi_rth_multiprocessing.py#L26
    import multiprocessing
    import multiprocessing.spawn

    def _freeze_support() -> None:
        """Minimal freeze_support. Only apply this if frozen."""
        from subprocess import _args_from_interpreter_flags

        # Prevent `spawn` from trying to read `__main__` in from the main script
        multiprocessing.process.ORIGINAL_DIR = None

        # Handle the first process that MP will create
        if (
            len(sys.argv) >= 2 and sys.argv[-2] == '-c' and sys.argv[-1].startswith((
                'from multiprocessing.semaphore_tracker import main',  # Py<3.8
                'from multiprocessing.resource_tracker import main',  # Py>=3.8
                'from multiprocessing.forkserver import main'
            )) and set(sys.argv[1:-2]) == set(_args_from_interpreter_flags())
        ):
            exec(sys.argv[-1])
            sys.exit()

        # Handle the second process that MP will create
        if multiprocessing.spawn.is_forking(sys.argv):
            kwargs = {}
            for arg in sys.argv[2:]:
                name, value = arg.split('=')
                if value == 'None':
                    kwargs[name] = None
                else:
                    kwargs[name] = int(value)
            multiprocessing.spawn.spawn_main(**kwargs)
            sys.exit()

    if not is_windows and is_frozen():
        multiprocessing.freeze_support = multiprocessing.spawn.freeze_support = _freeze_support


def freeze_support() -> None:
    """This behaves like multiprocessing.freeze_support but also works on Non-Windows."""
    import multiprocessing
    _extend_freeze_support()
    multiprocessing.freeze_support()


def visualize_regions(root_region: Region, file_name: str, *,
                      show_entrance_names: bool = False, show_locations: bool = True, show_other_regions: bool = True,
                      linetype_ortho: bool = True) -> None:
    """Visualize the layout of a world as a PlantUML diagram.

    :param root_region: The region from which to start the diagram from. (Usually the "Menu" region of your world.)
    :param file_name: The name of the destination .puml file.
    :param show_entrance_names: (default False) If enabled, the name of the entrance will be shown near each connection.
    :param show_locations: (default True) If enabled, the locations will be listed inside each region.
            Priority locations will be shown in bold.
            Excluded locations will be stricken out.
            Locations without ID will be shown in italics.
            Locked locations will be shown with a padlock icon.
            For filled locations, the item name will be shown after the location name.
            Progression items will be shown in bold.
            Items without ID will be shown in italics.
    :param show_other_regions: (default True) If enabled, regions that can't be reached by traversing exits are shown.
    :param linetype_ortho: (default True) If enabled, orthogonal straight line parts will be used; otherwise polylines.

    Example usage in World code:
    from Utils import visualize_regions
    visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")

    Example usage in Main code:
    from Utils import visualize_regions
    for player in world.player_ids:
        visualize_regions(world.get_region("Menu", player), f"{world.get_out_file_name_base(player)}.puml")
    """
    assert root_region.multiworld, "The multiworld attribute of root_region has to be filled"
    from BaseClasses import Entrance, Item, Location, LocationProgressType, MultiWorld, Region
    from collections import deque
    import re

    uml: typing.List[str] = list()
    seen: typing.Set[Region] = set()
    regions: typing.Deque[Region] = deque((root_region,))
    multiworld: MultiWorld = root_region.multiworld

    def fmt(obj: Union[Entrance, Item, Location, Region]) -> str:
        name = obj.name
        if isinstance(obj, Item):
            name = multiworld.get_name_string_for_object(obj)
            if obj.advancement:
                name = f"**{name}**"
            if obj.code is None:
                name = f"//{name}//"
        if isinstance(obj, Location):
            if obj.progress_type == LocationProgressType.PRIORITY:
                name = f"**{name}**"
            elif obj.progress_type == LocationProgressType.EXCLUDED:
                name = f"--{name}--"
            if obj.address is None:
                name = f"//{name}//"
        return re.sub("[\".:]", "", name)

    def visualize_exits(region: Region) -> None:
        for exit_ in region.exits:
            if exit_.connected_region:
                if show_entrance_names:
                    uml.append(f"\"{fmt(region)}\" --> \"{fmt(exit_.connected_region)}\" : \"{fmt(exit_)}\"")
                else:
                    try:
                        uml.remove(f"\"{fmt(exit_.connected_region)}\" --> \"{fmt(region)}\"")
                        uml.append(f"\"{fmt(exit_.connected_region)}\" <--> \"{fmt(region)}\"")
                    except ValueError:
                        uml.append(f"\"{fmt(region)}\" --> \"{fmt(exit_.connected_region)}\"")
            else:
                uml.append(f"circle \"unconnected exit:\\n{fmt(exit_)}\"")
                uml.append(f"\"{fmt(region)}\" --> \"unconnected exit:\\n{fmt(exit_)}\"")

    def visualize_locations(region: Region) -> None:
        any_lock = any(location.locked for location in region.locations)
        for location in region.locations:
            lock = "<&lock-locked> " if location.locked else "<&lock-unlocked,color=transparent> " if any_lock else ""
            if location.item:
                uml.append(f"\"{fmt(region)}\" : {{method}} {lock}{fmt(location)}: {fmt(location.item)}")
            else:
                uml.append(f"\"{fmt(region)}\" : {{field}} {lock}{fmt(location)}")

    def visualize_region(region: Region) -> None:
        uml.append(f"class \"{fmt(region)}\"")
        if show_locations:
            visualize_locations(region)
        visualize_exits(region)

    def visualize_other_regions() -> None:
        if other_regions := [region for region in multiworld.get_regions(root_region.player) if region not in seen]:
            uml.append("package \"other regions\" <<Cloud>> {")
            for region in other_regions:
                uml.append(f"class \"{fmt(region)}\"")
            uml.append("}")

    uml.append("@startuml")
    uml.append("hide circle")
    uml.append("hide empty members")
    if linetype_ortho:
        uml.append("skinparam linetype ortho")
    while regions:
        if (current_region := regions.popleft()) not in seen:
            seen.add(current_region)
            visualize_region(current_region)
            regions.extend(exit_.connected_region for exit_ in current_region.exits if exit_.connected_region)
    if show_other_regions:
        visualize_other_regions()
    uml.append("@enduml")

    with open(file_name, "wt", encoding="utf-8") as f:
        f.write("\n".join(uml))
