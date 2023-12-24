"""
Archipelago launcher for bundled app.

* if run with APBP as argument, launch corresponding client.
* if run with executable as argument, run it passing argv[2:] as arguments
* if run without arguments, open launcher GUI

Scroll down to components= to add components to the launcher as well as setup.py
"""


import argparse
import itertools
import logging
import multiprocessing
import shlex
import subprocess
import sys
import webbrowser
from os.path import isfile
from shutil import which
from typing import Sequence, Union, Optional

import Utils
import settings
from worlds.LauncherComponents import Component, components, Type, SuffixIdentifier, icon_paths

if __name__ == "__main__":
    import ModuleUpdate
    ModuleUpdate.update()

from Utils import is_frozen, user_path, local_path, init_logging, open_filename, messagebox, \
    is_windows, is_macos, is_linux


def open_host_yaml():
    file = settings.get_settings().filename
    assert file, "host.yaml missing"
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


def update_settings():
    from settings import get_settings
    get_settings().save()


components.extend([
    # Functions
    Component("Open host.yaml", func=open_host_yaml),
    Component("Open Patch", func=open_patch),
    Component("Generate Template Settings", func=generate_yamls),
    Component("Discord Server", icon="discord", func=lambda: webbrowser.open("https://discord.gg/8Z65BR2")),
    Component("18+ Discord Server", icon="discord", func=lambda: webbrowser.open("https://discord.gg/fqvNCCRsu4")),
    Component("Browse Files", func=browse_files),
])


def identify(path: Union[None, str]):
    if path is None:
        return None, None
    for component in components:
        if component.handles_file(path):
            return path, component
        elif path == component.display_name or path == component.script_name:
            return None, component
    return None, None


def get_exe(component: Union[str, Component]) -> Optional[Sequence[str]]:
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
    from kivy.uix.image import AsyncImage
    from kivy.uix.relativelayout import RelativeLayout

    class Launcher(App):
        base_title: str = "Archipelago Launcher"
        container: ContainerLayout
        grid: GridLayout

        _tools = {c.display_name: c for c in components if c.type == Type.TOOL}
        _clients = {c.display_name: c for c in components if c.type == Type.CLIENT}
        _adjusters = {c.display_name: c for c in components if c.type == Type.ADJUSTER}
        _miscs = {c.display_name: c for c in components if c.type == Type.MISC}

        def __init__(self, ctx=None):
            self.title = self.base_title
            self.ctx = ctx
            self.icon = r"data/icon.png"
            super().__init__()

        def build(self):
            self.container = ContainerLayout()
            self.grid = GridLayout(cols=2)
            self.container.add_widget(self.grid)
            self.grid.add_widget(Label(text="General"))
            self.grid.add_widget(Label(text="Clients"))
            button_layout = self.grid  # make buttons fill the window

            def build_button(component: Component):
                """
                Builds a button widget for a given component.

                Args:
                    component (Component): The component associated with the button.

                Returns:
                    None. The button is added to the parent grid layout.

                """
                button = Button(text=component.display_name)
                button.component = component
                button.bind(on_release=self.component_action)
                if component.icon != "icon":
                    image = AsyncImage(source=icon_paths[component.icon],
                                       size=(38, 38), size_hint=(None, 1), pos=(5, 0))
                    box_layout = RelativeLayout()
                    box_layout.add_widget(button)
                    box_layout.add_widget(image)
                    button_layout.add_widget(box_layout)
                else:
                    button_layout.add_widget(button)

            for (tool, client) in itertools.zip_longest(itertools.chain(
                    self._tools.items(), self._miscs.items(), self._adjusters.items()), self._clients.items()):
                # column 1
                if tool:
                    build_button(tool[1])
                else:
                    button_layout.add_widget(Label())
                # column 2
                if client:
                    build_button(client[1])
                else:
                    button_layout.add_widget(Label())

            return self.container

        @staticmethod
        def component_action(button):
            if button.component.func:
                button.component.func()
            else:
                launch(get_exe(button.component), button.component.cli)

        def _stop(self, *largs):
            # ran into what appears to be https://groups.google.com/g/kivy-users/c/saWDLoYCSZ4 with PyCharm.
            # Closing the window explicitly cleans it up.
            self.root_window.close()
            super()._stop(*largs)

    Launcher().run()


def run_component(component: Component, *args):
    if component.func:
        component.func(*args)
    elif component.script_name:
        subprocess.run([*get_exe(component.script_name), *args])
    else:
        logging.warning(f"Component {component} does not appear to be executable.")


def main(args: Optional[Union[argparse.Namespace, dict]] = None):
    if isinstance(args, argparse.Namespace):
        args = {k: v for k, v in args._get_kwargs()}
    elif not args:
        args = {}

    if "Patch|Game|Component" in args:
        file, component = identify(args["Patch|Game|Component"])
        if file:
            args['file'] = file
        if component:
            args['component'] = component
        if not component:
            logging.warning(f"Could not identify Component responsible for {args['Patch|Game|Component']}")

    if args["update_settings"]:
        update_settings()
    if 'file' in args:
        run_component(args["component"], args["file"], *args["args"])
    elif 'component' in args:
        run_component(args["component"], *args["args"])
    elif not args["update_settings"]:
        run_gui()


if __name__ == '__main__':
    init_logging('Launcher')
    Utils.freeze_support()
    multiprocessing.set_start_method("spawn")  # if launched process uses kivy, fork won't work
    parser = argparse.ArgumentParser(description='Archipelago Launcher')
    run_group = parser.add_argument_group("Run")
    run_group.add_argument("--update_settings", action="store_true",
                           help="Update host.yaml and exit.")
    run_group.add_argument("Patch|Game|Component", type=str, nargs="?",
                           help="Pass either a patch file, a generated game or the name of a component to run.")
    run_group.add_argument("args", nargs="*",
                           help="Arguments to pass to component.")
    main(parser.parse_args())

    from worlds.LauncherComponents import processes
    for process in processes:
        # we await all child processes to close before we tear down the process host
        # this makes it feel like each one is its own program, as the Launcher is closed now
        process.join()
