import bisect
import logging
import pathlib
import weakref
import sys
import webbrowser
from typing import Optional, Callable, Iterable, Sequence

from Utils import local_path, open_filename, is_frozen, is_kivy_running, open_file, user_path, read_apignore, \
    is_windows, Type


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

    def run(self, *args) -> bool:
        if self.func:
            self.func(*args)
        elif self.script_name:
            import subprocess
            subprocess.run([*get_exe(self.script_name), *args])
        else:
            logging.warning(f"Component {self} does not appear to be executable.")


processes = weakref.WeakSet()


def launch_subprocess(func: Callable, name: str | None = None, args: tuple[str, ...] = ()) -> None:
    import multiprocessing
    process = multiprocessing.Process(target=func, name=name, args=args)
    process.start()
    processes.add(process)


def launch(func: Callable, name: str | None = None, args: tuple[str, ...] = ()) -> None:
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


def _install_apworld(apworld_src: str = "") -> Optional[tuple[pathlib.Path, pathlib.Path]]:
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
    if found_already_loaded and is_kivy_running():
        raise Exception(f"Installed APWorld successfully, but '{module_name}' is already loaded, "
                        "so a Launcher restart is required to use the new installation.")
    world_source = worlds.WorldSource(str(target), is_zip=True, relative=False)
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
        Utils.messagebox("Notice", str(e), error=True)
        logging.exception(e)
    else:
        import Utils
        logging.info(f"Installed APWorld successfully, copied {source} to {target}.")
        Utils.messagebox("Install complete.", f"Installed APWorld from {source}.")


def export_datapackage() -> None:
    import json

    from worlds import network_data_package

    path = user_path("datapackage_export.json")
    with open(path, "w") as f:
        json.dump(network_data_package, f, indent=4)

    open_file(path)

def open_patch():
    from Utils import messagebox
    from os.path import isfile
    suffixes = []
    for c in components:
        if c.type == Type.CLIENT and \
                isinstance(c.file_identifier, SuffixIdentifier) and \
                (c.script_name is None or isfile(get_exe(c)[-1])):
            suffixes += c.file_identifier.suffixes
    try:
        filename = open_filename("Select patch", (("Patches", suffixes),))
    except Exception as e:
        messagebox("Error", str(e), error=True)
    else:
        file, component = identify(filename)
        if file and component:
            exe = get_exe(component)
            if exe is None or not isfile(exe[-1]):
                exe = get_exe("Launcher")

            launch([*exe, file], component.cli)


def get_exe(component: str | Component) -> Sequence[str] | None:
    if isinstance(component, str):
        name = component
        component = None
        if name.startswith("Archipelago"):
            name = name[11:]
        if name.endswith(".exe"):
            name = name[:-4]
        if name.endswith(".py"):
            name = name[:-3]
        if not name:
            return None
        for c in components:
            if c.script_name == name or c.frozen_name == f"Archipelago{name}":
                component = c
                break
        if not component:
            return None
    if is_frozen():
        suffix = ".exe" if is_windows else ""
        return [local_path(f"{component.frozen_name}{suffix}")] if component.frozen_name else None
    else:
        return [sys.executable, local_path(f"{component.script_name}.py")] if component.script_name else None

def identify(path: None | str) -> tuple[None | str, None | Component]:
    if path is None:
        return None, None
    for component in components:
        if component.handles_file(path):
            return path, component
        elif path == component.display_name or path == component.script_name:
            return None, component
    return None, None

def open_host_yaml():
    import settings
    import subprocess
    from shutil import which
    from Utils import is_linux, is_macos, env_cleared_lib_path
    s = settings.get_settings()
    file = s.filename
    s.save()
    assert file, "host.yaml missing"
    if is_linux:
        exe = which('sensible-editor') or which('gedit') or \
              which('xdg-open') or which('gnome-open') or which('kde-open')
    elif is_macos:
        exe = which("open")
    else:
        webbrowser.open(file)
        return

    env = env_cleared_lib_path()
    subprocess.Popen([exe, file], env=env)

def generate_yamls(*args):
    import argparse

    from Options import generate_yaml_templates

    parser = argparse.ArgumentParser(description="Generate Template Options", usage="[-h] [--skip_open_folder]")
    parser.add_argument("--skip_open_folder", action="store_true")
    args = parser.parse_args(args)

    target = user_path("Players", "Templates")
    generate_yaml_templates(target, False)
    if not args.skip_open_folder:
        open_folder(target)


def browse_files():
    open_folder(user_path())


def open_folder(folder_path):
    import subprocess
    from shutil import which
    from Utils import is_linux, is_macos, env_cleared_lib_path

    if is_linux:
        exe = which('xdg-open') or which('gnome-open') or which('kde-open')
    elif is_macos:
        exe = which("open")
    else:
        webbrowser.open(folder_path)
        return

    if exe:
        env = env_cleared_lib_path()
        subprocess.Popen([exe, folder_path], env=env)
    else:
        logging.warning(f"No file browser available to open {folder_path}")


components: list[Component] = [
    # Launcher
    Component('Launcher', 'Launcher', component_type=Type.HIDDEN),
    # Core
    Component('Host', 'MultiServer', 'ArchipelagoServer', cli=True,
              file_identifier=SuffixIdentifier('.archipelago', '.zip'),
              description="Host a generated multiworld on your computer."),
    Component('Generate', 'Generate', cli=True,
              description="Generate a multiworld with the YAMLs in the players folder."),
    Component("Options Creator", "OptionsCreator", "ArchipelagoOptionsCreator", component_type=Type.TOOL,
              description="Visual creator for Archipelago option files."),
    Component("Install APWorld", func=install_apworld, file_identifier=SuffixIdentifier(".apworld"),
              description="Install an APWorld to play games not included with Archipelago by default."),
    Component('Text Client', 'CommonClient', 'ArchipelagoTextClient', func=launch_textclient,
              description="Connect to a multiworld using the text client."),
    # Functions
    Component("Open host.yaml", func=open_host_yaml,
              description="Open the host.yaml file to change settings for generation, games, and more."),
    Component("Open Patch", func=open_patch,
              description="Open a patch file, downloaded from the room page or provided by the host."),
    Component("Generate Template Options", func=generate_yamls,
              description="Generate template YAMLs for currently installed games."),
    Component("Archipelago Website", func=lambda: webbrowser.open("https://archipelago.gg/"),
              description="Open archipelago.gg in your browser."),
    Component("Discord Server", icon="discord", func=lambda: webbrowser.open("https://discord.gg/8Z65BR2"),
              description="Join the Discord server to play public multiworlds, report issues, or just chat!"),
    Component("Unrated/18+ Discord Server", icon="discord",
              func=lambda: webbrowser.open("https://discord.gg/fqvNCCRsu4"),
              description="Find unrated and 18+ games in the After Dark Discord server."),
    Component("Browse Files", func=browse_files,
              description="Open the Archipelago installation folder in your file browser."),
    Component('LttP Adjuster', 'LttPAdjuster'),
    # Ocarina of Time
    Component('OoT Client', 'OoTClient',
              file_identifier=SuffixIdentifier('.apz5')),
    Component('OoT Adjuster', 'OoTAdjuster'),
    # TLoZ
    Component('Zelda 1 Client', 'Zelda1Client', file_identifier=SuffixIdentifier('.aptloz')),
    # ChecksFinder
    Component('ChecksFinder Client', 'ChecksFinderClient'),
    # Zillion
    Component('Zillion Client', 'ZillionClient',
              file_identifier=SuffixIdentifier('.apzl')),

    # MegaMan Battle Network 3
    Component('MMBN3 Client', 'MMBN3Client', file_identifier=SuffixIdentifier('.apbn3')),

    Component("Export Datapackage", func=export_datapackage, component_type=Type.TOOL,
              description="Write item/location data for installed worlds to a file and open it."),
]


# if registering an icon from within an apworld, the format "ap:module.name/path/to/file.png" can be used
icon_paths = {
    'icon': local_path('data', 'icon.png'),
    'discord': local_path('data', 'discord-mark-blue.png'),
}

if not is_frozen():
    def _build_apworlds(*launch_args: str):
        import json
        import os
        import zipfile

        from worlds import AutoWorldRegister
        from worlds.Files import APWorldContainer
        from Launcher import open_folder

        import argparse
        parser = argparse.ArgumentParser(prog="Build APWorlds", description="Build script for APWorlds")
        parser.add_argument("worlds", type=str, default=(), nargs="*", help="names of APWorlds to build")
        parser.add_argument("--skip_open_folder", action="store_true", help="don't open the output build folder")
        args = parser.parse_args(launch_args)

        if args.worlds:
            games = [(game, AutoWorldRegister.world_types.get(game, None)) for game in args.worlds]
        else:
            games = [(worldname, worldtype) for worldname, worldtype in AutoWorldRegister.world_types.items()
                     if not worldtype.zip_path]

        global_apignores = read_apignore(local_path("data", "GLOBAL.apignore"))
        if not global_apignores:
            raise RuntimeError("Could not read global apignore file for build component")

        apworlds_folder = os.path.join("build", "apworlds")
        os.makedirs(apworlds_folder, exist_ok=True)
        for worldname, worldtype in games:
            if not worldtype:
                logging.error(f"Requested APWorld \"{worldname}\" does not exist.")
                continue
            file_name = os.path.split(os.path.dirname(worldtype.__file__))[1]
            world_directory = os.path.join("worlds", file_name)
            if os.path.isfile(os.path.join(world_directory, "archipelago.json")):
                with open(os.path.join(world_directory, "archipelago.json"), mode="r", encoding="utf-8") as manifest_file:
                    manifest = json.load(manifest_file)

                assert "game" in manifest, (
                    f"World directory {world_directory} has an archipelago.json manifest file, but it "
                    "does not define a \"game\"."
                )
                assert manifest["game"] == worldtype.game, (
                    f"World directory {world_directory} has an archipelago.json manifest file, but value of the "
                    f"\"game\" field ({manifest['game']} does not equal the World class's game ({worldtype.game})."
                )
            else:
                manifest = {}

            zip_path = os.path.join(apworlds_folder, file_name + ".apworld")
            apworld = APWorldContainer(str(zip_path))
            apworld.game = worldtype.game
            manifest.update(apworld.get_manifest())
            apworld.manifest_path = os.path.join(file_name, "archipelago.json")

            local_ignores = read_apignore(pathlib.Path(world_directory, ".apignore"))
            apignores = global_apignores + local_ignores if local_ignores else global_apignores

            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
                for file in apignores.match_tree_files(world_directory, negate=True):
                    zf.write(pathlib.Path(world_directory, file), pathlib.Path(file_name, file))

                zf.writestr(apworld.manifest_path, json.dumps(manifest))

        if not args.skip_open_folder:
            open_folder(apworlds_folder)

    components.append(Component("Build APWorlds", func=_build_apworlds, cli=True,
                                description="Build APWorlds from loose-file world folders."))
