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
import webbrowser
from os.path import isfile
from shutil import which
from typing import Sequence, Union, Optional

import Utils
from worlds.LauncherComponents import Component, components, Type, SuffixIdentifier

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


def generate_yamls():
    from Options import generate_yaml_templates

    target = Utils.user_path("Players", "Templates")
    generate_yaml_templates(target, False)
    open_folder(target)


def browse_files():
    open_folder(user_path())


def open_folder(folder_path):
    if is_linux:
        exe = which('xdg-open') or which('gnome-open') or which('kde-open')
        subprocess.Popen([exe, folder_path])
    elif is_macos:
        exe = which("open")
        subprocess.Popen([exe, folder_path])
    else:
        webbrowser.open(folder_path)


components.extend([
    # Functions
    Component('Open host.yaml', func=open_host_yaml),
    Component('Open Patch', func=open_patch),
    Component('Generate Template Settings', func=generate_yamls),
    Component('Discord Server', func=lambda: webbrowser.open("https://discord.gg/8Z65BR2")),
    Component('18+ Discord Server', func=lambda: webbrowser.open("https://discord.gg/fqvNCCRsu4")),
    Component('Browse Files', func=browse_files),
])


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
