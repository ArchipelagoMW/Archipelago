"""
Archipelago launcher for bundled app.

* if run with APBP as argument, launch corresponding client.
* if run with executable as argument, run it passing argv[2:] as arguments
* if run without arguments, open launcher GUI

Scroll down to components= to add components to the launcher as well as setup.py
"""


import argparse
import itertools
import shlex
import subprocess
import sys
from enum import Enum, auto
from os.path import isfile
from shutil import which
from typing import Iterable, Sequence, Callable, Union, Optional

if __name__ == "__main__":
    import ModuleUpdate
    ModuleUpdate.update()

from Utils import is_frozen, user_path, local_path, init_logging, open_filename, messagebox, \
    is_windows, is_macos, is_linux


def open_host_yaml():
    file = user_path('host.yaml')
    if is_linux:
        exe = which('sensible-editor') or which('gedit') or \
              which('xdg-open') or which('gnome-open') or which('kde-open')
        subprocess.Popen([exe, file])
    elif is_macos:
        exe = which("open")
        subprocess.Popen([exe, file])
    else:
        import webbrowser
        webbrowser.open(file)


def open_patch():
    suffixes = []
    for c in components:
        if isfile(get_exe(c)[-1]):
            suffixes += c.file_identifier.suffixes if c.type == Type.CLIENT and \
                                                      isinstance(c.file_identifier, SuffixIdentifier) else []
    try:
        filename = open_filename('Select patch', (('Patches', suffixes),))
    except Exception as e:
        messagebox('Error', str(e), error=True)
    else:
        file, _, component = identify(filename)
        if file and component:
            launch([*get_exe(component), file], component.cli)


def browse_files():
    file = user_path()
    if is_linux:
        exe = which('xdg-open') or which('gnome-open') or which('kde-open')
        subprocess.Popen([exe, file])
    elif is_macos:
        exe = which("open")
        subprocess.Popen([exe, file])
    else:
        import webbrowser
        webbrowser.open(file)


# noinspection PyArgumentList
class Type(Enum):
    TOOL = auto()
    FUNC = auto()  # not a real component
    CLIENT = auto()
    ADJUSTER = auto()


class SuffixIdentifier:
    suffixes: Iterable[str]

    def __init__(self, *args: str):
        self.suffixes = args

    def __call__(self, path: str):
        if isinstance(path, str):
            for suffix in self.suffixes:
                if path.endswith(suffix):
                    return True
        return False


class Component:
    display_name: str
    type: Optional[Type]
    script_name: Optional[str]
    frozen_name: Optional[str]
    icon: str  # just the name, no suffix
    cli: bool
    func: Optional[Callable]
    file_identifier: Optional[Callable[[str], bool]]

    def __init__(self, display_name: str, script_name: Optional[str] = None, frozen_name: Optional[str] = None,
                 cli: bool = False, icon: str = 'icon', component_type: Type = None, func: Optional[Callable] = None,
                 file_identifier: Optional[Callable[[str], bool]] = None):
        self.display_name = display_name
        self.script_name = script_name
        self.frozen_name = frozen_name or f'Archipelago{script_name}' if script_name else None
        self.icon = icon
        self.cli = cli
        self.type = component_type or \
            None if not display_name else \
            Type.FUNC if func else \
            Type.CLIENT if 'Client' in display_name else \
            Type.ADJUSTER if 'Adjuster' in display_name else Type.TOOL
        self.func = func
        self.file_identifier = file_identifier

    def handles_file(self, path: str):
        return self.file_identifier(path) if self.file_identifier else False


components: Iterable[Component] = (
    # Launcher
    Component('', 'Launcher'),
    # Core
    Component('Host', 'MultiServer', 'ArchipelagoServer', cli=True,
              file_identifier=SuffixIdentifier('.archipelago', '.zip')),
    Component('Generate', 'Generate', cli=True),
    Component('Text Client', 'CommonClient', 'ArchipelagoTextClient'),
    # SNI
    Component('SNI Client', 'SNIClient',
              file_identifier=SuffixIdentifier('.apz3', '.apm3', '.apsoe', '.aplttp', '.apsm', '.apsmz3', '.apdkc3',
                                               '.apsmw', '.apl2ac')),
    Component('LttP Adjuster', 'LttPAdjuster'),
    # Factorio
    Component('Factorio Client', 'FactorioClient'),
    # Minecraft
    Component('Minecraft Client', 'MinecraftClient', icon='mcicon', cli=True,
              file_identifier=SuffixIdentifier('.apmc')),
    # Ocarina of Time
    Component('OoT Client', 'OoTClient',
              file_identifier=SuffixIdentifier('.apz5')),
    Component('OoT Adjuster', 'OoTAdjuster'),
    # FF1
    Component('FF1 Client', 'FF1Client'),
    # Pokémon
    Component('Pokemon Client', 'PokemonClient', file_identifier=SuffixIdentifier('.apred', '.apblue')),
    # ChecksFinder
    Component('ChecksFinder Client', 'ChecksFinderClient'),
    # Starcraft 2
    Component('Starcraft 2 Client', 'Starcraft2Client'),
    # Wargroove
    Component('Wargroove Client', 'WargrooveClient'),
    # Zillion
    Component('Zillion Client', 'ZillionClient',
              file_identifier=SuffixIdentifier('.apzl')),
    # Functions
    Component('Open host.yaml', func=open_host_yaml),
    Component('Open Patch', func=open_patch),
    Component('Browse Files', func=browse_files),
)
icon_paths = {
    'icon': local_path('data', 'icon.ico' if is_windows else 'icon.png'),
    'mcicon': local_path('data', 'mcicon.ico')
}


def identify(path: Union[None, str]):
    if path is None:
        return None, None, None
    for component in components:
        if component.handles_file(path):
            return path, component.script_name, component
    return (None, None, None) if '/' in path or '\\' in path else (None, path, None)


def get_exe(component: Union[str, Component]) -> Optional[Sequence[str]]:
    if isinstance(component, str):
        name = component
        component = None
        if name.startswith('Archipelago'):
            name = name[11:]
        if name.endswith('.exe'):
            name = name[:-4]
        if name.endswith('.py'):
            name = name[:-3]
        if not name:
            return None
        for c in components:
            if c.script_name == name or c.frozen_name == f'Archipelago{name}':
                component = c
                break
        if not component:
            return None
    if is_frozen():
        suffix = '.exe' if is_windows else ''
        return [local_path(f'{component.frozen_name}{suffix}')]
    else:
        return [sys.executable, local_path(f'{component.script_name}.py')]


def launch(exe, in_terminal=False):
    if in_terminal:
        if is_windows:
            subprocess.Popen(['start', *exe], shell=True)
            return
        elif is_linux:
            terminal = which('x-terminal-emulator') or which('gnome-terminal') or which('xterm')
            if terminal:
                subprocess.Popen([terminal, '-e', shlex.join(exe)])
                return
        elif is_macos:
            terminal = [which('open'), '-W', '-a', 'Terminal.app']
            subprocess.Popen([*terminal, *exe])
            return
    subprocess.Popen(exe)


def run_gui():
    from kvui import App, ContainerLayout, GridLayout, Button, Label

    class Launcher(App):
        base_title: str = "Archipelago Launcher"
        container: ContainerLayout
        grid: GridLayout

        _tools = {c.display_name: c for c in components if c.type == Type.TOOL and isfile(get_exe(c)[-1])}
        _clients = {c.display_name: c for c in components if c.type == Type.CLIENT and isfile(get_exe(c)[-1])}
        _adjusters = {c.display_name: c for c in components if c.type == Type.ADJUSTER and isfile(get_exe(c)[-1])}
        _funcs = {c.display_name: c for c in components if c.type == Type.FUNC}

        def __init__(self, ctx=None):
            self.title = self.base_title
            self.ctx = ctx
            self.icon = r"data/icon.png"
            super().__init__()

        def build(self):
            self.container = ContainerLayout()
            self.grid = GridLayout(cols=2)
            self.container.add_widget(self.grid)

            button_layout = self.grid  # make buttons fill the window
            for (tool, client) in itertools.zip_longest(itertools.chain(
                    self._tools.items(), self._funcs.items(), self._adjusters.items()), self._clients.items()):
                # column 1
                if tool:
                    button = Button(text=tool[0])
                    button.component = tool[1]
                    button.bind(on_release=self.component_action)
                    button_layout.add_widget(button)
                else:
                    button_layout.add_widget(Label())
                # column 2
                if client:
                    button = Button(text=client[0])
                    button.component = client[1]
                    button.bind(on_press=self.component_action)
                    button_layout.add_widget(button)
                else:
                    button_layout.add_widget(Label())

            return self.container

        @staticmethod
        def component_action(button):
            if button.component.type == Type.FUNC:
                button.component.func()
            else:
                launch(get_exe(button.component), button.component.cli)

    Launcher().run()


def main(args: Optional[Union[argparse.Namespace, dict]] = None):
    if isinstance(args, argparse.Namespace):
        args = {k: v for k, v in args._get_kwargs()}
    elif not args:
        args = {}

    if "Patch|Game|Component" in args:
        file, component, _ = identify(args["Patch|Game|Component"])
        if file:
            args['file'] = file
        if component:
            args['component'] = component

    if 'file' in args:
        subprocess.run([*get_exe(args['component']), args['file'], *args['args']])
    elif 'component' in args:
        subprocess.run([*get_exe(args['component']), *args['args']])
    else:
        run_gui()


if __name__ == '__main__':
    init_logging('Launcher')
    parser = argparse.ArgumentParser(description='Archipelago Launcher')
    parser.add_argument('Patch|Game|Component', type=str, nargs='?',
                        help="Pass either a patch file, a generated game or the name of a component to run.")
    parser.add_argument('args', nargs="*", help="Arguments to pass to component.")
    main(parser.parse_args())
