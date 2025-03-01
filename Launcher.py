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
import urllib.parse
import webbrowser
from os.path import isfile
from shutil import which
from typing import Callable, Optional, Sequence, Tuple, Union

if __name__ == "__main__":
    import ModuleUpdate
    ModuleUpdate.update()

import settings
import Utils
from Utils import (init_logging, is_frozen, is_linux, is_macos, is_windows, local_path, messagebox, open_filename,
                   user_path)
from worlds.LauncherComponents import Component, components, icon_paths, SuffixIdentifier, Type


def open_host_yaml():
    s = settings.get_settings()
    file = s.filename
    s.save()
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
    Component("Generate Template Options", func=generate_yamls),
    Component("Archipelago Website", func=lambda: webbrowser.open("https://archipelago.gg/")),
    Component("Discord Server", icon="discord", func=lambda: webbrowser.open("https://discord.gg/8Z65BR2")),
    Component("Unrated/18+ Discord Server", icon="discord", func=lambda: webbrowser.open("https://discord.gg/fqvNCCRsu4")),
    Component("Browse Files", func=browse_files),
])


def handle_uri(path: str, launch_args: Tuple[str, ...]) -> None:
    url = urllib.parse.urlparse(path)
    queries = urllib.parse.parse_qs(url.query)
    launch_args = (path, *launch_args)
    client_component = None
    text_client_component = None
    if "game" in queries:
        game = queries["game"][0]
    else:  # TODO around 0.6.0 - this is for pre this change webhost uri's
        game = "Archipelago"
    for component in components:
        if component.supports_uri and component.game_name == game:
            client_component = component
        elif component.display_name == "Text Client":
            text_client_component = component

    if client_component is None:
        run_component(text_client_component, *launch_args)
        return

    from kvui import App, Button, BoxLayout, Label, Window

    class Popup(App):
        def __init__(self):
            self.title = "Connect to Multiworld"
            self.icon = r"data/icon.png"
            super().__init__()

        def build(self):
            layout = BoxLayout(orientation="vertical")
            layout.add_widget(Label(text="Select client to open and connect with."))
            button_row = BoxLayout(orientation="horizontal", size_hint=(1, 0.4))

            text_client_button = Button(
                text=text_client_component.display_name,
                on_release=lambda *args: run_component(text_client_component, *launch_args)
            )
            button_row.add_widget(text_client_button)

            game_client_button = Button(
                text=client_component.display_name,
                on_release=lambda *args: run_component(client_component, *launch_args)
            )
            button_row.add_widget(game_client_button)

            layout.add_widget(button_row)

            return layout

        def _stop(self, *largs):
            # see run_gui Launcher _stop comment for details
            self.root_window.close()
            super()._stop(*largs)

    Popup().run()


def identify(path: Union[None, str]) -> Tuple[Union[None, str], Union[None, Component]]:
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


refresh_components: Optional[Callable[[], None]] = None


def run_gui():
    from kvui import App, ContainerLayout, GridLayout, Button, Label, ScrollBox, Widget, ApAsyncImage
    from kivy.core.window import Window
    from kivy.uix.relativelayout import RelativeLayout

    class Launcher(App):
        base_title: str = "Archipelago Launcher"
        container: ContainerLayout
        grid: GridLayout
        _tool_layout: Optional[ScrollBox] = None
        _client_layout: Optional[ScrollBox] = None

        def __init__(self, ctx=None):
            self.title = self.base_title + " " + Utils.__version__
            self.ctx = ctx
            self.icon = r"data/icon.png"
            super().__init__()

        def _refresh_components(self) -> None:

            def build_button(component: Component) -> Widget:
                """
                Builds a button widget for a given component.

                Args:
                    component (Component): The component associated with the button.

                Returns:
                    None. The button is added to the parent grid layout.

                """
                button = Button(text=component.display_name, size_hint_y=None, height=40)
                button.component = component
                button.bind(on_release=self.component_action)
                if component.icon != "icon":
                    image = ApAsyncImage(source=icon_paths[component.icon],
                                         size=(38, 38), size_hint=(None, 1), pos=(5, 0))
                    box_layout = RelativeLayout(size_hint_y=None, height=40)
                    box_layout.add_widget(button)
                    box_layout.add_widget(image)
                    return box_layout
                return button

            # clear before repopulating
            assert self._tool_layout and self._client_layout, "must call `build` first"
            tool_children = reversed(self._tool_layout.layout.children)
            for child in tool_children:
                self._tool_layout.layout.remove_widget(child)
            client_children = reversed(self._client_layout.layout.children)
            for child in client_children:
                self._client_layout.layout.remove_widget(child)

            _tools = {c.display_name: c for c in components if c.type == Type.TOOL}
            _clients = {c.display_name: c for c in components if c.type == Type.CLIENT}
            _adjusters = {c.display_name: c for c in components if c.type == Type.ADJUSTER}
            _miscs = {c.display_name: c for c in components if c.type == Type.MISC}

            for (tool, client) in itertools.zip_longest(itertools.chain(
                _tools.items(), _miscs.items(), _adjusters.items()
            ), _clients.items()):
                # column 1
                if tool:
                    self._tool_layout.layout.add_widget(build_button(tool[1]))
                # column 2
                if client:
                    self._client_layout.layout.add_widget(build_button(client[1]))

        def build(self):
            self.container = ContainerLayout()
            self.grid = GridLayout(cols=2)
            self.container.add_widget(self.grid)
            self.grid.add_widget(Label(text="General", size_hint_y=None, height=40))
            self.grid.add_widget(Label(text="Clients", size_hint_y=None, height=40))
            self._tool_layout = ScrollBox()
            self._tool_layout.layout.orientation = "vertical"
            self.grid.add_widget(self._tool_layout)
            self._client_layout = ScrollBox()
            self._client_layout.layout.orientation = "vertical"
            self.grid.add_widget(self._client_layout)

            self._refresh_components()

            global refresh_components
            refresh_components = self._refresh_components

            Window.bind(on_drop_file=self._on_drop_file)

            return self.container

        @staticmethod
        def component_action(button):
            if button.component.func:
                button.component.func()
            else:
                launch(get_exe(button.component), button.component.cli)

        def _on_drop_file(self, window: Window, filename: bytes, x: int, y: int) -> None:
            """ When a patch file is dropped into the window, run the associated component. """
            file, component = identify(filename.decode())
            if file and component:
                run_component(component, file)
            else:
                logging.warning(f"unable to identify component for {file}")

        def _stop(self, *largs):
            # ran into what appears to be https://groups.google.com/g/kivy-users/c/saWDLoYCSZ4 with PyCharm.
            # Closing the window explicitly cleans it up.
            self.root_window.close()
            super()._stop(*largs)

    Launcher().run()

    # avoiding Launcher reference leak
    # and don't try to do something with widgets after window closed
    global refresh_components
    refresh_components = None


def run_component(component: Component, *args):
    if component.func:
        component.func(*args)
        if refresh_components:
            refresh_components()
    elif component.script_name:
        subprocess.run([*get_exe(component.script_name), *args])
    else:
        logging.warning(f"Component {component} does not appear to be executable.")


def main(args: Optional[Union[argparse.Namespace, dict]] = None):
    if isinstance(args, argparse.Namespace):
        args = {k: v for k, v in args._get_kwargs()}
    elif not args:
        args = {}

    path = args.get("Patch|Game|Component|url", None)
    if path is not None:
        if path.startswith("archipelago://"):
            handle_uri(path, args.get("args", ()))
            return
        file, component = identify(path)
        if file:
            args['file'] = file
        if component:
            args['component'] = component
        if not component:
            logging.warning(f"Could not identify Component responsible for {path}")

    if args["update_settings"]:
        update_settings()
    if "file" in args:
        run_component(args["component"], args["file"], *args["args"])
    elif "component" in args:
        run_component(args["component"], *args["args"])
    elif not args["update_settings"]:
        run_gui()


if __name__ == '__main__':
    init_logging('Launcher')
    Utils.freeze_support()
    multiprocessing.set_start_method("spawn")  # if launched process uses kivy, fork won't work
    parser = argparse.ArgumentParser(
        description='Archipelago Launcher',
        usage="[-h] [--update_settings] [Patch|Game|Component] [-- component args here]"
    )
    run_group = parser.add_argument_group("Run")
    run_group.add_argument("--update_settings", action="store_true",
                           help="Update host.yaml and exit.")
    run_group.add_argument("Patch|Game|Component|url", type=str, nargs="?",
                           help="Pass either a patch file, a generated game, the component name to run, or a url to "
                                "connect with.")
    run_group.add_argument("args", nargs="*",
                           help="Arguments to pass to component.")
    main(parser.parse_args())

    from worlds.LauncherComponents import processes
    for process in processes:
        # we await all child processes to close before we tear down the process host
        # this makes it feel like each one is its own program, as the Launcher is closed now
        process.join()
