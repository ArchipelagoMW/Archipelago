"""
Application settings / host.yaml interface using type hints.
This is different from player options.
"""

import os
import os.path
import shutil
import sys
import types
import typing
import warnings
from enum import IntEnum
from threading import Lock
from typing import cast, Any, BinaryIO, ClassVar, Dict, Iterator, List, Optional, TextIO, Tuple, Union, TypeVar

__all__ = [
    "get_settings", "fmt_doc", "no_gui",
    "Group", "Bool", "Path", "UserFilePath", "UserFolderPath", "LocalFilePath", "LocalFolderPath",
    "OptionalUserFilePath", "OptionalUserFolderPath", "OptionalLocalFilePath", "OptionalLocalFolderPath",
    "GeneralOptions", "ServerOptions", "GeneratorOptions", "SNIOptions", "Settings"
]

no_gui = False
skip_autosave = False
_world_settings_name_cache: Dict[str, str] = {}  # TODO: cache on disk and update when worlds change
_world_settings_name_cache_updated = False
_lock = Lock()


def _update_cache() -> None:
    """Load all worlds and update world_settings_name_cache"""
    global _world_settings_name_cache_updated
    if _world_settings_name_cache_updated:
        return

    try:
        from worlds.AutoWorld import AutoWorldRegister
        for world in AutoWorldRegister.world_types.values():
            annotation = world.__annotations__.get("settings", None)
            if annotation is None or annotation == "ClassVar[Optional['Group']]":
                continue
            _world_settings_name_cache[world.settings_key] = f"{world.__module__}.{world.__name__}"
    finally:
        _world_settings_name_cache_updated = True


def fmt_doc(cls: type, level: int) -> str:
    comment = cls.__doc__
    assert comment, f"{cls} has no __doc__"
    indent = level * 2 * " "
    return "\n".join(map(lambda s: f"{indent}# {s}", filter(None, map(lambda s: s.strip(), comment.split("\n")))))


class Group:
    _type_cache: ClassVar[Optional[Dict[str, Any]]] = None
    _dumping: bool = False
    _has_attr: bool = False
    _changed: bool = False
    _dumper: ClassVar[type]

    def __getitem__(self, key: str) -> Any:
        try:
            return getattr(self, key)
        except NameError:
            raise KeyError(key)

    def __iter__(self) -> Iterator[str]:
        cls_members = dir(self.__class__)
        members = filter(lambda k: not k.startswith("_") and (k not in cls_members or k in self.__annotations__),
                         list(self.__annotations__) +
                         [name for name in dir(self) if name not in self.__annotations__])
        return members.__iter__()

    def __contains__(self, key: str) -> bool:
        try:
            self._has_attr = True
            return hasattr(self, key)
        finally:
            self._has_attr = False

    def __setitem__(self, key: str, value: Any) -> None:
        setattr(self, key, value)

    def __getattribute__(self, item: str) -> Any:
        attr = super().__getattribute__(item)
        if isinstance(attr, Path) and not super().__getattribute__("_dumping"):
            if attr.required and not attr.exists() and not super().__getattribute__("_has_attr"):
                # if a file is required, and the one from settings does not exist, ask the user to provide it
                # unless we are dumping the settings, because that would ask for each entry
                with _lock:  # lock to avoid opening multiple
                    new = None if no_gui else attr.browse()
                    if new is None:
                        raise FileNotFoundError(f"{attr} does not exist, but "
                                                f"{self.__class__.__name__}.{item} is required")
                    setattr(self, item, new)
                    self._changed = True
                    attr = new
            # resolve the path immediately when accessing it
            return attr.__class__(attr.resolve())
        return attr

    @property
    def changed(self) -> bool:
        return self._changed or any(map(lambda v: isinstance(v, Group) and v.changed,
                                        self.__dict__.values()))

    @classmethod
    def get_type_hints(cls) -> Dict[str, Any]:
        """Returns resolved type hints for the class"""
        if cls._type_cache is None:
            if not cls.__annotations__ or not isinstance(next(iter(cls.__annotations__.values())), str):
                # non-str: assume already resolved
                cls._type_cache = cls.__annotations__
            else:
                # str: build dicts and resolve with eval
                mod = sys.modules[cls.__module__]  # assume the module wasn't deleted
                mod_dict = {k: getattr(mod, k) for k in dir(mod)}
                cls._type_cache = typing.get_type_hints(cls, globalns=mod_dict, localns=cls.__dict__)
        return cls._type_cache

    def get(self, key: str, default: Any = None) -> Any:
        if key in self:
            return self[key]
        return default

    def items(self) -> List[Tuple[str, Any]]:
        return [(key, getattr(self, key)) for key in self]

    def update(self, dct: Dict[str, Any]) -> None:
        assert isinstance(dct, dict), f"{self.__class__.__name__}.update called with " \
                                      f"{dct.__class__.__name__} instead of dict."

        for k in self.__annotations__:
            if not k.startswith("_") and k not in dct:
                self._changed = True  # key missing from host.yaml

        for k, v in dct.items():
            # don't do getattr to stay lazy with world group init/loading
            # instead we assign unknown groups as dicts and a later getattr will upcast them
            attr = self.__dict__[k] if k in self.__dict__ else \
                self.__class__.__dict__[k] if k in self.__class__.__dict__ else None
            if isinstance(attr, Group):
                # update group
                if k not in self.__dict__:
                    attr = attr.__class__()  # make a copy of default
                    setattr(self, k, attr)
                if isinstance(v, dict):
                    attr.update(v)
                else:
                    warnings.warn(f"{self.__class__.__name__}.{k} "
                                  f"tried to update Group from {type(v)}")
            elif isinstance(attr, dict):
                # update dict
                if k not in self.__dict__:
                    attr = attr.copy()  # make a copy of default
                    setattr(self, k, attr)
                if isinstance(v, dict):
                    attr.update(v)
                else:
                    warnings.warn(f"{self.__class__.__name__}.{k} "
                                  f"tried to update dict from {type(v)}")
            else:
                # assign value, try to upcast to type hint
                annotation = self.get_type_hints().get(k, None)
                candidates = (
                    [] if annotation is None else (
                        typing.get_args(annotation)
                        if typing.get_origin(annotation) in (Union, types.UnionType)
                        else [annotation]
                    )
                )
                none_type = type(None)
                for cls in candidates:
                    assert isinstance(cls, type), f"{self.__class__.__name__}.{k}: type {cls} not supported in settings"
                    if v is None and cls is none_type:
                        # assign None, i.e. from Optional
                        setattr(self, k, v)
                        break
                    if cls is bool and isinstance(v, bool):
                        # assign bool - special handling because issubclass(int, bool) is True
                        setattr(self, k, v)
                        break
                    if cls is not bool and issubclass(cls, type(v)):
                        # upcast, i.e. int -> IntEnum, str -> Path
                        setattr(self, k, cls.__call__(v))
                        break
                    if issubclass(cls, (tuple, set)) and isinstance(v, list):
                        # convert or upcast from list
                        setattr(self, k, cls.__call__(v))
                        break
                else:
                    # assign scalar and hope for the best
                    setattr(self, k, v)
                    if annotation:
                        warnings.warn(f"{self.__class__.__name__}.{k} "
                                      f"assigned from incompatible type {type(v).__name__}")

    def as_dict(self, *args: str, downcast: bool = True) -> Dict[str, Any]:
        return {
            name: _to_builtin(cast(object, getattr(self, name))) if downcast else getattr(self, name)
            for name in self if not args or name in args
        }

    @classmethod
    def _dump_value(cls, value: Any, f: TextIO, indent: str) -> None:
        """Write a single yaml line to f"""
        from Utils import dump, Dumper as BaseDumper
        yaml_line: str = dump(value, Dumper=cast(BaseDumper, cls._dumper), width=2**31-1)
        assert yaml_line.count("\n") == 1, f"Unexpected input for yaml dumper: {value}"
        f.write(f"{indent}{yaml_line}")

    @classmethod
    def _dump_item(cls, name: Optional[str], attr: object, f: TextIO, level: int) -> None:
        """Write a group, dict or sequence item to f, where attr can be a scalar or a collection"""

        # lazy construction of yaml Dumper to avoid loading Utils early
        from Utils import Dumper as BaseDumper
        from yaml import ScalarNode, MappingNode
        if not hasattr(cls, "_dumper"):
            if cls is Group or not hasattr(Group, "_dumper"):
                class Dumper(BaseDumper):
                    def represent_mapping(self, tag: str, mapping: Any, flow_style: Any = None) -> MappingNode:
                        from yaml import ScalarNode
                        res: MappingNode = super().represent_mapping(tag, mapping, flow_style)
                        pairs = cast(List[Tuple[ScalarNode, Any]], res.value)
                        for k, v in pairs:
                            k.style = None  # remove quotes from keys
                        return res

                    def represent_str(self, data: str) -> ScalarNode:
                        # default double quote all strings
                        return self.represent_scalar("tag:yaml.org,2002:str", data, style='"')

                Dumper.add_representer(str, Dumper.represent_str)
                Group._dumper = Dumper
            if cls is not Group:
                cls._dumper = Group._dumper

        indent = "  " * level
        start = f"{indent}-\n" if name is None else f"{indent}{name}:\n"
        if isinstance(attr, Group):
            # handle group
            f.write(start)
            attr.dump(f, level=level+1)
        elif isinstance(attr, (list, tuple, set)) and attr:
            # handle non-empty sequence; empty use one-line [] syntax
            f.write(start)
            for value in attr:
                cls._dump_item(None, value, f, level=level + 1)
        elif isinstance(attr, dict) and attr:
            # handle non-empty dict; empty use one-line {} syntax
            f.write(start)
            for dict_key, value in attr.items():
                # not dumping doc string here, since there is no way to upcast it after dumping
                assert dict_key is not None, "Key None is reserved for sequences"
                cls._dump_item(dict_key, value, f, level=level + 1)
        else:
            # dump scalar or empty sequence or mapping item
            line = [_to_builtin(attr)] if name is None else {name: _to_builtin(attr)}
            cls._dump_value(line, f, indent=indent)

    def dump(self, f: TextIO, level: int = 0) -> None:
        """Dump Group to stream f at given indentation level"""
        # There is no easy way to generate extra lines into default yaml output,
        # so we format part of it by hand using an odd recursion here and in _dump_*.

        self._dumping = True
        try:
            # fetch class to avoid going through getattr
            cls = self.__class__
            type_hints = cls.get_type_hints()
            entries = [e for e in self]
            if not entries:
                # write empty dict for empty Group with no instance values
                cls._dump_value({}, f, indent="  " * level)
            # validate group
            for name in cls.__annotations__.keys():
                assert hasattr(cls, name), f"{cls}.{name} is missing a default value"
            # dump ordered members
            for name in entries:
                attr = cast(object, getattr(self, name))
                attr_cls = type_hints[name] if name in type_hints else attr.__class__
                attr_cls_origin = typing.get_origin(attr_cls)
                # resolve to first type for doc string
                while attr_cls_origin is Union or attr_cls_origin is types.UnionType:
                    attr_cls = typing.get_args(attr_cls)[0]
                    attr_cls_origin = typing.get_origin(attr_cls)
                if attr_cls.__doc__ and attr_cls.__module__ != "builtins":
                    f.write(fmt_doc(attr_cls, level=level) + "\n")
                self._dump_item(name, attr, f, level=level)
            self._changed = False
        finally:
            self._dumping = False


class Bool:
    # can't subclass bool, so we use this and Union or type: ignore
    def __bool__(self) -> bool:
        raise NotImplementedError()


# Types for generic settings
T = TypeVar("T", bound="Path")


def _resolve_exe(s: str) -> str:
    """Append exe file extension if the file is an executable"""
    if isinstance(s, Path):
        from Utils import is_windows
        if s.is_exe and is_windows and not s.lower().endswith(".exe"):
            return str(s + ".exe")
    return str(s)


def _to_builtin(o: object) -> Any:
    """Downcast object to a builtin type for output"""
    if o is None:
        return None
    c = o.__class__
    while c.__module__ != "builtins":
        c = c.__base__
    return c.__call__(o)


class Path(str):
    # paths in host.yaml are str
    required: bool = True
    """Marks the file as required and opens a file browser when missing"""
    is_exe: bool = False
    """Special cross-platform handling for executables"""
    description: Optional[str] = None
    """Title to display when browsing for the file"""
    copy_to: Optional[str] = None
    """If not None, copy to AP folder instead of linking it"""

    @classmethod
    def validate(cls, path: str) -> None:
        """Overload and raise to validate input files from browse"""
        pass

    def browse(self: T, **kwargs: Any) -> Optional[T]:
        """Opens a file browser to search for the file"""
        raise NotImplementedError(f"Please use a subclass of Path for {self.__class__.__name__}")

    def resolve(self) -> str:
        return _resolve_exe(self)

    def exists(self) -> bool:
        return os.path.exists(self.resolve())


class _UserPath(str):
    def resolve(self) -> str:
        if os.path.isabs(self):
            return str(self)
        from Utils import user_path
        return user_path(_resolve_exe(self))


class _LocalPath(str):
    def resolve(self) -> str:
        if os.path.isabs(self):
            return str(self)
        from Utils import local_path
        return local_path(_resolve_exe(self))


class FilePath(Path):
    # path to a file

    md5s: ClassVar[List[Union[str, bytes]]] = []
    """MD5 hashes for default validator."""

    def browse(self: T,
               filetypes: Optional[typing.Sequence[typing.Tuple[str, typing.Sequence[str]]]] = None, **kwargs: Any)\
            -> Optional[T]:
        from Utils import open_filename, is_windows
        if not filetypes:
            if self.is_exe:
                name, ext = "Program", ".exe" if is_windows else ""
            else:
                ext = os.path.splitext(self)[1]
                name = ext[1:] if ext else "File"
            filetypes = [(name, [ext])]
        res = open_filename(f"Select {self.description or self.__class__.__name__}", filetypes, self)
        if res:
            self.validate(res)
            if self.copy_to:
                # instead of linking the file, copy it
                dst = self.__class__(self.copy_to).resolve()
                shutil.copy(res, dst, follow_symlinks=True)
                res = dst
            try:
                rel = os.path.relpath(res, self.__class__("").resolve())
                if not rel.startswith(".."):
                    res = rel
            except ValueError:
                pass
            return self.__class__(res)
        return None

    @classmethod
    def _validate_stream_hashes(cls, f: BinaryIO) -> None:
        """Helper to efficiently validate stream against hashes"""
        if not cls.md5s:
            return  # no hashes to validate against

        pos = f.tell()
        try:
            from hashlib import md5
            file_md5 = md5()
            block = bytearray(64*1024)
            view = memoryview(block)
            while n := f.readinto(view):  # type: ignore
                file_md5.update(view[:n])
            file_md5_hex = file_md5.hexdigest()
            for valid_md5 in cls.md5s:
                if isinstance(valid_md5, str):
                    if valid_md5.lower() == file_md5_hex:
                        break
                elif valid_md5 == file_md5.digest():
                    break
            else:
                raise ValueError(f"Hashes do not match for {cls.__name__}")
        finally:
            f.seek(pos)

    @classmethod
    def validate(cls, path: str) -> None:
        """Try to open and validate file against hashes"""
        with open(path, "rb", buffering=0) as f:
            try:
                cls._validate_stream_hashes(f)
            except ValueError:
                raise ValueError(f"File hash does not match for {path}")


class FolderPath(Path):
    # path to a folder

    def browse(self: T, **kwargs: Any) -> Optional[T]:
        from Utils import open_directory
        res = open_directory(f"Select {self.description or self.__class__.__name__}", self)
        if res:
            try:
                rel = os.path.relpath(res, self.__class__("").resolve())
                if not rel.startswith(".."):
                    res = rel
            except ValueError:
                pass
            return self.__class__(res)
        return None


class UserFilePath(_UserPath, FilePath):
    pass


class UserFolderPath(_UserPath, FolderPath):
    pass


class OptionalUserFilePath(UserFilePath):
    required = False


class OptionalUserFolderPath(UserFolderPath):
    required = False


class LocalFilePath(_LocalPath, FilePath):
    pass


class LocalFolderPath(_LocalPath, FolderPath):
    pass


class OptionalLocalFilePath(LocalFilePath):
    required = False


class OptionalLocalFolderPath(LocalFolderPath):
    required = False


class SNESRomPath(UserFilePath):
    # Special UserFilePath that ignores an optional header when validating

    @classmethod
    def validate(cls, path: str) -> None:
        """Try to open and validate file against hashes"""
        with open(path, "rb", buffering=0) as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            if size % 1024 == 512:
                f.seek(512)  # skip header
            elif size % 1024 == 0:
                f.seek(0)  # header-less
            else:
                raise ValueError(f"Unexpected file size for {path}")

            try:
                cls._validate_stream_hashes(f)
            except ValueError:
                raise ValueError(f"File hash does not match for {path}")


# World-independent setting groups

class GeneralOptions(Group):
    class OutputPath(OptionalUserFolderPath):
        """
        Where to place output files
        """
        # created on demand, so marked as optional

    output_path: OutputPath = OutputPath("output")


class ServerOptions(Group):
    """
    Options for MultiServer
    Null means nothing, for the server this means to default the value
    These overwrite command line arguments!
    """

    class ServerPassword(str):
        """
        Allows for clients to log on and manage the server.  If this is null, no remote administration is possible.
        """

    class DisableItemCheat(Bool):
        """Disallow !getitem"""

    class LocationCheckPoints(int):
        """
        Client hint system
        Points given to a player for each acquired item in their world
        """

    class HintCost(int):
        """
        Relative point cost to receive a hint via !hint for players
        so for example hint_cost: 20 would mean that for every 20% of available checks, you get the ability to hint,
        for a total of 5
        """

    class ReleaseMode(str):
        """
        Release modes
        A Release sends out the remaining items *from* a world that releases
        "disabled" -> clients can't release,
        "enabled" -> clients can always release
        "auto" -> automatic release on goal completion
        "auto-enabled" -> automatic release on goal completion and manual release is also enabled
        "goal" -> release is allowed after goal completion
        """

    class CollectMode(str):
        """
        Collect modes
        A Collect sends the remaining items *to* a world that collects
        "disabled" -> clients can't collect,
        "enabled" -> clients can always collect
        "auto" -> automatic collect on goal completion
        "auto-enabled" -> automatic collect on goal completion and manual collect is also enabled
        "goal" -> collect is allowed after goal completion
        """

    class RemainingMode(str):
        """
        Remaining modes
        !remaining handling, that tells a client which items remain in their pool
        "enabled" -> Client can always ask for remaining items
        "disabled" -> Client can never ask for remaining items
        "goal" -> Client can ask for remaining items after goal completion
        """

    class AutoShutdown(int):
        """Automatically shut down the server after this many seconds without new location checks, 0 to keep running"""

    class Compatibility(IntEnum):
        """
        Compatibility handling
        2 -> Recommended for casual/cooperative play, attempt to be compatible with everything across all versions
        1 -> No longer in use, kept reserved in case of future use
        0 -> Recommended for tournaments to force a level playing field, only allow an exact version match
        """
        OFF = 0
        ON = 1
        FULL = 2

    class LogNetwork(IntEnum):
        """log all server traffic, mostly for dev use"""
        OFF = 0
        ON = 1

    host: Optional[str] = None
    port: int = 38281
    password: Optional[str] = None
    multidata: Optional[str] = None
    savefile: Optional[str] = None
    disable_save: bool = False
    loglevel: str = "info"
    logtime: bool = False
    server_password: Optional[ServerPassword] = None
    disable_item_cheat: Union[DisableItemCheat, bool] = False
    location_check_points: LocationCheckPoints = LocationCheckPoints(1)
    hint_cost: HintCost = HintCost(10)
    release_mode: ReleaseMode = ReleaseMode("auto")
    collect_mode: CollectMode = CollectMode("auto")
    remaining_mode: RemainingMode = RemainingMode("goal")
    auto_shutdown: AutoShutdown = AutoShutdown(0)
    compatibility: Compatibility = Compatibility(2)
    log_network: LogNetwork = LogNetwork(0)


class GeneratorOptions(Group):
    """Options for Generation"""

    class EnemizerPath(LocalFilePath):
        """Location of your Enemizer CLI, available here: https://github.com/Ijwu/Enemizer/releases"""
        is_exe = True

    class PlayerFilesPath(OptionalUserFolderPath):
        """Folder from which the player yaml files are pulled from"""
        # created on demand, so marked as optional

    class Players(int):
        """amount of players, 0 to infer from player files"""

    class WeightsFilePath(str):
        """
        general weights file, within the stated player_files_path location
        gets used if players is higher than the amount of per-player files found to fill remaining slots
        """
        # this is special because the path is relative to player_files_path

    class MetaFilePath(str):
        """Meta file name, within the stated player_files_path location"""
        # this is special because the path is relative to player_files_path

    class Spoiler(IntEnum):
        """
        Create a spoiler file
        0 -> None
        1 -> Spoiler without playthrough or paths to playthrough required items
        2 -> Spoiler with playthrough (viable solution to goals)
        3 -> Spoiler with playthrough and traversal paths towards items
        """
        NONE = 0
        BASIC = 1
        PLAYTHROUGH = 2
        FULL = 3

    class PlandoOptions(str):
        """
        List of options that can be plando'd. Can be combined, for example "bosses, items"
        Available options: bosses, items, texts, connections
        """

    class Race(IntEnum):
        """Create encrypted race roms and flag games as race mode"""
        OFF = 0
        ON = 1

    class PanicMethod(str):
        """
        What to do if the current item placements appear unsolvable.
        raise -> Raise an exception and abort.
        swap -> Attempt to fix it by swapping prior placements around. (Default)
        start_inventory -> Move remaining items to start_inventory, generate additional filler items to fill locations.
        """

    enemizer_path: EnemizerPath = EnemizerPath("EnemizerCLI/EnemizerCLI.Core")  # + ".exe" is implied on Windows
    player_files_path: PlayerFilesPath = PlayerFilesPath("Players")
    players: Players = Players(0)
    weights_file_path: WeightsFilePath = WeightsFilePath("weights.yaml")
    meta_file_path: MetaFilePath = MetaFilePath("meta.yaml")
    spoiler: Spoiler = Spoiler(3)
    race: Race = Race(0)
    plando_options: PlandoOptions = PlandoOptions("bosses, connections, texts")
    panic_method: PanicMethod = PanicMethod("swap")
    loglevel: str = "info"
    logtime: bool = False


class SNIOptions(Group):
    class SNIPath(LocalFolderPath):
        """
        Set this to your SNI folder location if you want the MultiClient to attempt an auto start, \
does nothing if not found
        """

    class SnesRomStart(str):
        """
        Set this to false to never autostart a rom (such as after patching)
        True for operating system default program
        Alternatively, a path to a program to open the .sfc file with
        """

    sni_path: SNIPath = SNIPath("SNI")
    snes_rom_start: Union[SnesRomStart, bool] = True


class BizHawkClientOptions(Group):
    class EmuHawkPath(UserFilePath):
        """
        The location of the EmuHawk you want to auto launch patched ROMs with
        """
        is_exe = True
        description = "EmuHawk Executable"

    class RomStart(str):
        """
        Set this to true to autostart a patched ROM in BizHawk with the connector script,
        to false to never open the patched rom automatically,
        or to a path to an external program to open the ROM file with that instead.
        """

    emuhawk_path: EmuHawkPath = EmuHawkPath(None)
    rom_start: Union[RomStart, bool] = True


# Top-level group with lazy loading of worlds

class Settings(Group):
    general_options: GeneralOptions = GeneralOptions()
    server_options: ServerOptions = ServerOptions()
    generator: GeneratorOptions = GeneratorOptions()
    sni_options: SNIOptions = SNIOptions()
    bizhawkclient_options: BizHawkClientOptions = BizHawkClientOptions()

    _filename: Optional[str] = None

    def __getattribute__(self, key: str) -> Any:
        if key.startswith("_") or key in self.__class__.__dict__:
            # not a group or a hard-coded group
            pass
        elif key not in dir(self) or isinstance(super().__getattribute__(key), dict):
            # settings class not loaded yet
            if key not in _world_settings_name_cache:
                # find world that provides the settings class
                _update_cache()
                # check for missing keys to update _changed
                for world_settings_name in _world_settings_name_cache:
                    if world_settings_name not in dir(self):
                        self._changed = True
            if key not in _world_settings_name_cache:
                # not a world group
                return super().__getattribute__(key)
            # directly import world and grab settings class
            world_mod, world_cls_name = _world_settings_name_cache[key].rsplit(".", 1)
            world = cast(type, getattr(__import__(world_mod, fromlist=[world_cls_name]), world_cls_name))
            assert getattr(world, "settings_key") == key
            try:
                cls_or_name = world.__annotations__["settings"]
            except KeyError:
                import warnings
                warnings.warn(f"World {world_cls_name} does not define settings. Please consider upgrading the world.")
                return super().__getattribute__(key)
            if isinstance(cls_or_name, str):
                # Try to resolve type. Sadly we can't use get_type_hints, see https://bugs.python.org/issue43463
                cls_name = cls_or_name
                if "[" in cls_name:  # resolve ClassVar[]
                    cls_name = cls_name.split("[", 1)[1].rsplit("]", 1)[0]
                cls = cast(type, getattr(__import__(world_mod, fromlist=[cls_name]), cls_name))
            else:
                type_args = typing.get_args(cls_or_name)  # resolve ClassVar[]
                cls = type_args[0] if type_args else cast(type, cls_or_name)
            impl: Group = cast(Group, cls())
            assert isinstance(impl, Group), f"{world_cls_name}.settings has to inherit from settings.Group. " \
                                            "If that's already the case, please avoid recursive partial imports."
            # above assert fails for recursive partial imports
            # upcast loaded data to settings class
            try:
                dct = super().__getattribute__(key)
                if isinstance(dct, dict):
                    impl.update(dct)
                else:
                    self._changed = True  # key is a class var -> new section
            except AttributeError:
                self._changed = True  # key is unknown -> new section
            setattr(self, key, impl)

        return super().__getattribute__(key)

    def __init__(self, location: Optional[str]):  # change to PathLike[str] once we drop 3.8?
        super().__init__()
        if location:
            from Utils import parse_yaml
            with open(location, encoding="utf-8-sig") as f:
                from yaml.error import MarkedYAMLError
                try:
                    options = parse_yaml(f.read())
                except MarkedYAMLError as ex:
                    if ex.problem_mark:
                        f.seek(0)
                        lines = f.readlines()
                        problem_line = lines[ex.problem_mark.line]
                        error_line = " " * ex.problem_mark.column + "^"
                        raise Exception(f"{ex.context} {ex.problem}\n{problem_line}{error_line}")
                    raise ex
                # TODO: detect if upgrade is required
                # TODO: once we have a cache for _world_settings_name_cache, detect if any game section is missing
                self.update(options or {})
            self._filename = location

        def autosave() -> None:
            if __debug__:
                import __main__
                main_file = getattr(__main__, "__file__", "")
                assert "pytest" not in main_file and "unittest" not in main_file, \
                       f"Auto-saving {self._filename} during unittests"
            if self._filename and self.changed and not skip_autosave:
                self.save()

        if not skip_autosave:
            import atexit
            atexit.register(autosave)

    def save(self, location: Optional[str] = None) -> None:  # as above
        from Utils import parse_yaml
        location = location or self._filename
        assert location, "No file specified"
        temp_location = location + ".tmp"  # not using tempfile to test expected file access
        # remove old temps
        if os.path.exists(temp_location):
            os.unlink(temp_location)
        # can't use utf-8-sig because it breaks backward compat: pyyaml on Windows with bytes does not strip the BOM
        with open(temp_location, "w", encoding="utf-8") as f:
            self.dump(f)
            f.flush()
            if hasattr(os, "fsync"):
                os.fsync(f.fileno())
        # validate new file is valid yaml
        with open(temp_location, encoding="utf-8") as f:
            parse_yaml(f.read())
        # replace old with new, try atomic operation first
        try:
            os.rename(temp_location, location)
        except (OSError, FileExistsError):
            os.unlink(location)
            os.rename(temp_location, location)
        self._filename = location

    def dump(self, f: TextIO, level: int = 0) -> None:
        # load all world setting classes
        _update_cache()
        for key in _world_settings_name_cache:
            self.__getattribute__(key)  # load all worlds
        super().dump(f, level)

    @property
    def filename(self) -> Optional[str]:
        return self._filename


# host.yaml loader

def get_settings() -> Settings:
    """Returns settings from the default host.yaml"""
    with _lock:  # make sure we only have one instance
        res = getattr(get_settings, "_cache", None)
        if not res:
            from Utils import user_path, local_path
            filenames = ("options.yaml", "host.yaml")
            locations: List[str] = []
            if os.path.join(os.getcwd()) != local_path():
                locations += filenames  # use files from cwd only if it's not the local_path
            locations += [user_path(filename) for filename in filenames]
            for location in locations:
                try:
                    res = Settings(location)
                    break
                except FileNotFoundError:
                    continue
            else:
                warnings.warn(f"Could not find {filenames[1]} to load options. Creating a new one.")
                res = Settings(None)
                res.save(user_path(filenames[1]))
            setattr(get_settings, "_cache", res)
        return res
