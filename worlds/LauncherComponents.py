import bisect
import logging
import pathlib
import weakref
from enum import Enum, auto
from typing import Optional, Callable, List, Iterable, Tuple

from Utils import local_path, open_filename


class Type(Enum):
    TOOL = auto()
    MISC = auto()
    CLIENT = auto()
    ADJUSTER = auto()
    FUNC = auto()  # do not use anymore
    HIDDEN = auto()


class Component:
    """
    A Component represents a process launchable by Archipelago Launcher, either by a User action in the GUI,
    by resolving an archipelago://user:pass@host:port link from the WebHost, by resolving a patch file's metadata,
    or by using a component name arg while running the Launcher in CLI i.e. `ArchipelagoLauncher.exe "Text Client"`

    Expected to be appended to LauncherComponents.component list to be used.
    """
    display_name: str
    """Used as the GUI button label and the component name in the CLI args"""
    description: str
    """Optional description displayed on the GUI underneath the display name"""
    type: Type
    """
    Enum "Type" classification of component intent, for filtering in the Launcher GUI
    If not set in the constructor, it will be inferred by display_name
    """
    script_name: Optional[str]
    """Recommended to use func instead; Name of file to run when the component is called"""
    frozen_name: Optional[str]
    """Recommended to use func instead; Name of the frozen executable file for this component"""
    icon: str  # just the name, no suffix
    """Lookup ID for the icon path in LauncherComponents.icon_paths"""
    cli: bool
    """Bool to control if the component gets launched in an appropriate Terminal for the OS"""
    func: Optional[Callable]
    """
    Function that gets called when the component gets launched
    Any arg besides the component name arg is passed into the func as well, so handling *args is suggested
    """
    file_identifier: Optional[Callable[[str], bool]]
    """
    Function that is run against patch file arg to identify which component is appropriate to launch
    If the function is an Instance of SuffixIdentifier the suffixes will also be valid for the Open Patch component
    """
    game_name: Optional[str]
    """Game name to identify component when handling launch links from WebHost"""
    supports_uri: Optional[bool]
    """Bool to identify if a component supports being launched by launch links from WebHost"""

    def __init__(self, display_name: str, script_name: Optional[str] = None, frozen_name: Optional[str] = None,
                 cli: bool = False, icon: str = 'icon', component_type: Optional[Type] = None,
                 func: Optional[Callable] = None, file_identifier: Optional[Callable[[str], bool]] = None,
                 game_name: Optional[str] = None, supports_uri: Optional[bool] = False, description: str = "") -> None:
        self.display_name = display_name
        self.description = description
        self.script_name = script_name
        self.frozen_name = frozen_name or f'Archipelago{script_name}' if script_name else None
        self.icon = icon
        self.cli = cli
        if component_type == Type.FUNC:
            from Utils import deprecate
            deprecate(f"Launcher Component {self.display_name} is using Type.FUNC Type, which is pending removal.")
            component_type = Type.MISC

        self.type = component_type or (
            Type.CLIENT if "Client" in display_name else
            Type.ADJUSTER if "Adjuster" in display_name else Type.MISC)
        self.func = func
        self.file_identifier = file_identifier
        self.game_name = game_name
        self.supports_uri = supports_uri

    def handles_file(self, path: str):
        return self.file_identifier(path) if self.file_identifier else False

    def __repr__(self):
        return f"{self.__class__.__name__}({self.display_name})"


processes = weakref.WeakSet()


def launch_subprocess(func: Callable, name: str | None = None, args: Tuple[str, ...] = ()) -> None:
    import multiprocessing
    process = multiprocessing.Process(target=func, name=name, args=args)
    process.start()
    processes.add(process)


def launch(func: Callable, name: str | None = None, args: Tuple[str, ...] = ()) -> None:
    from Utils import is_kivy_running
    if is_kivy_running():
        launch_subprocess(func, name, args)
    else:
        func(*args)


class SuffixIdentifier:
    suffixes: Iterable[str]

    def __init__(self, *args: str):
        self.suffixes = args

    def __call__(self, path: str) -> bool:
        if isinstance(path, str):
            for suffix in self.suffixes:
                if path.endswith(suffix):
                    return True
        return False


def launch_textclient(*args):
    import CommonClient
    launch(CommonClient.run_as_textclient, name="TextClient", args=args)


def _install_apworld(apworld_src: str = "") -> Optional[Tuple[pathlib.Path, pathlib.Path]]:
    if not apworld_src:
        apworld_src = open_filename('Select APWorld file to install', (('APWorld', ('.apworld',)),))
        if not apworld_src:
            # user closed menu
            return

    if not apworld_src.endswith(".apworld"):
        raise Exception(f"Wrong file format, looking for .apworld. File identified: {apworld_src}")

    apworld_path = pathlib.Path(apworld_src)

    try:
        import zipfile
        zip = zipfile.ZipFile(apworld_path)
        directories = [f.name for f in zipfile.Path(zip).iterdir() if f.is_dir()]
        if len(directories) == 1 and directories[0] in apworld_path.stem:
            module_name = directories[0]
            apworld_name = module_name + ".apworld"
        else:
            raise Exception("APWorld appears to be invalid or damaged. (expected a single directory)")
        zip.open(module_name + "/__init__.py")
    except ValueError as e:
        raise Exception("Archive appears invalid or damaged.") from e
    except KeyError as e:
        raise Exception("Archive appears to not be an apworld. (missing __init__.py)") from e

    import worlds
    if worlds.user_folder is None:
        raise Exception("Custom Worlds directory appears to not be writable.")
    for world_source in worlds.world_sources:
        if apworld_path.samefile(world_source.resolved_path):
            # Note that this doesn't check if the same world is already installed.
            # It only checks if the user is trying to install the apworld file
            # that comes from the installation location (worlds or custom_worlds)
            raise Exception(f"APWorld is already installed at {world_source.resolved_path}.")

    # TODO: run generic test suite over the apworld.
    # TODO: have some kind of version system to tell from metadata if the apworld should be compatible.

    target = pathlib.Path(worlds.user_folder) / apworld_name
    import shutil
    shutil.copyfile(apworld_path, target)

    # If a module with this name is already loaded, then we can't load it now.
    # TODO: We need to be able to unload a world module,
    # so the user can update a world without restarting the application.
    found_already_loaded = False
    for loaded_world in worlds.world_sources:
        loaded_name = pathlib.Path(loaded_world.path).stem
        if module_name == loaded_name:
            found_already_loaded = True
            break
    if found_already_loaded:
        raise Exception(f"Installed APWorld successfully, but '{module_name}' is already loaded,\n"
                        "so a Launcher restart is required to use the new installation.\n"
                        "If the Launcher is not open, no action needs to be taken.")
    world_source = worlds.WorldSource(str(target), is_zip=True)
    bisect.insort(worlds.world_sources, world_source)
    world_source.load()

    return apworld_path, target


def install_apworld(apworld_path: str = "") -> None:
    try:
        res = _install_apworld(apworld_path)
        if res is None:
            logging.info("Aborting APWorld installation.")
            return
        source, target = res
    except Exception as e:
        import Utils
        Utils.messagebox(e.__class__.__name__, str(e), error=True)
        logging.exception(e)
    else:
        import Utils
        logging.info(f"Installed APWorld successfully, copied {source} to {target}.")
        Utils.messagebox("Install complete.", f"Installed APWorld from {source}.")


components: List[Component] = [
    # Launcher
    Component('Launcher', 'Launcher', component_type=Type.HIDDEN),
    # Core
    Component('Host', 'MultiServer', 'ArchipelagoServer', cli=True,
              file_identifier=SuffixIdentifier('.archipelago', '.zip'),
              description="Host a generated multiworld on your computer."),
    Component('Generate', 'Generate', cli=True,
              description="Generate a multiworld with the YAMLs in the players folder."),
    Component("Install APWorld", func=install_apworld, file_identifier=SuffixIdentifier(".apworld"),
              description="Install an APWorld to play games not included with Archipelago by default."),
    Component('Text Client', 'CommonClient', 'ArchipelagoTextClient', func=launch_textclient,
              description="Connect to a multiworld using the text client."),
    Component('Links Awakening DX Client', 'LinksAwakeningClient',
              file_identifier=SuffixIdentifier('.apladx')),
    Component('LttP Adjuster', 'LttPAdjuster'),
    # Ocarina of Time
    Component('OoT Client', 'OoTClient',
              file_identifier=SuffixIdentifier('.apz5')),
    Component('OoT Adjuster', 'OoTAdjuster'),
    # TLoZ
    Component('Zelda 1 Client', 'Zelda1Client', file_identifier=SuffixIdentifier('.aptloz')),
    # ChecksFinder
    Component('ChecksFinder Client', 'ChecksFinderClient'),
    # Starcraft 2
    Component('Starcraft 2 Client', 'Starcraft2Client'),
    # Zillion
    Component('Zillion Client', 'ZillionClient',
              file_identifier=SuffixIdentifier('.apzl')),

    #MegaMan Battle Network 3
    Component('MMBN3 Client', 'MMBN3Client', file_identifier=SuffixIdentifier('.apbn3'))
]


# if registering an icon from within an apworld, the format "ap:module.name/path/to/file.png" can be used
icon_paths = {
    'icon': local_path('data', 'icon.png'),
    'discord': local_path('data', 'discord-mark-blue.png'),
}
