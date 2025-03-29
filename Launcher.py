"""
Archipelago Launcher

* if run with APBP as argument, launch corresponding client.
* if run with executable as argument, run it passing argv[2:] as arguments
* if run without arguments, open launcher GUI

Scroll down to components= to add components to the launcher as well as setup.py
"""

import os
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
from typing import Callable, Optional, Sequence, Tuple, Union, Any


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
    client_component = []
    text_client_component = None
    if "game" in queries:
        game = queries["game"][0]
    else:  # TODO around 0.6.0 - this is for pre this change webhost uri's
        game = "Archipelago"
    for component in components:
        if component.supports_uri and component.game_name == game:
            client_component.append(component)
        elif component.display_name == "Text Client":
            text_client_component = component

    from kvui import MDButton, MDButtonText
    from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer, MDDialogSupportingText
    from kivymd.uix.divider import MDDivider

    if client_component is None:
        run_component(text_client_component, *launch_args)
        return
    else:
        popup_text = MDDialogSupportingText(text="Select client to open and connect with.")
        component_buttons = [MDDivider()]
        for component in [text_client_component, *client_component]:
            component_buttons.append(MDButton(
                MDButtonText(text=component.display_name),
                on_release=lambda *args, comp=component: run_component(comp, *launch_args),
                style="text"
            ))
        component_buttons.append(MDDivider())

    MDDialog(
        # Headline
        MDDialogHeadlineText(text="Connect to Multiworld"),
        # Text
        popup_text,
        # Content
        MDDialogContentContainer(
            *component_buttons,
            orientation="vertical"
        ),

    ).open()


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

def create_shortcut(button: Any, component: Component) -> None:
    from pyshortcuts import make_shortcut
    script = sys.argv[0]
    wkdir = Utils.local_path()

    script = f"{script} \"{component.display_name}\""
    make_shortcut(script, name=f"Archipelago {component.display_name}", icon=local_path("data", "icon.ico"),
                  startmenu=False, terminal=False, working_dir=wkdir)
    button.menu.dismiss()


refresh_components: Optional[Callable[[], None]] = None


def run_gui(path: str, args: Any) -> None:
    from kvui import (MDApp, MDFloatLayout, MDGridLayout, MDButton, MDLabel, MDButtonText, MDButtonIcon, ScrollBox,
                      ContainerLayout, Widget, MDBoxLayout, ApAsyncImage)
    from kivy.core.window import Window
    from kivy.metrics import dp
    from kivy.uix.image import AsyncImage
    from kivymd.uix.button import MDIconButton
    from kivymd.uix.card import MDCard
    from kivymd.uix.menu import MDDropdownMenu
    from kivymd.uix.navigationdrawer import MDNavigationDrawerDivider
    from kivymd.uix.relativelayout import MDRelativeLayout
    from kivymd.uix.screen import MDScreen
    from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

    class Launcher(MDApp):
        base_title: str = "Archipelago Launcher"
        container: ContainerLayout
        navigation: MDBoxLayout
        grid: MDGridLayout
        button_layout: ScrollBox | None = None

        def __init__(self, ctx=None, path=None, args=None):
            self.title = self.base_title + " " + Utils.__version__
            self.ctx = ctx
            self.icon = r"data/icon.png"
            self.favorites = []
            self.launch_uri = path
            self.launch_args = args
            persistent = Utils.persistent_load()
            if "launcher" in persistent:
                if "favorites" in persistent["launcher"]:
                    self.favorites.extend(persistent["launcher"]["favorites"])
            super().__init__()

        def _refresh_components(self, type_filter: Sequence[str | Type] | None = None) -> None:
            if not type_filter:
                type_filter = [Type.CLIENT, Type.ADJUSTER, Type.TOOL, Type.MISC]
            favorites = "favorites" in type_filter

            def build_card(component: Component) -> Widget:
                """
                Builds a card widget for a given component.

                :param component: The component associated with the button.

                :return: The created Card Widget.
                """
                button_card = MDCard(style="filled", padding="4dp", size_hint=(1, None), height=dp(75))
                button_layout = MDRelativeLayout()
                button_card.add_widget(button_layout)

                source = icon_paths[component.icon]
                image = ApAsyncImage(source=source, size=(40, 40), size_hint_y=None,
                                     pos_hint={"center_x": 0.1, "center_y": 0.5})

                button_layout.add_widget(image)
                button_layout.add_widget(MDLabel(text=component.display_name,
                                                 pos_hint={"center_x": 0.5,
                                                           "center_y": 0.85 if component.description else 0.65},
                                                 halign="center", font_style="Title", role="medium",
                                                 theme_text_color="Custom", text_color=self.theme_cls.primaryColor))
                if component.description:
                    button_layout.add_widget(MDLabel(text=component.description,
                                                     pos_hint={"center_x": 0.5, "center_y": 0.35}, halign="center",
                                                     role="small", theme_text_color="Custom",
                                                     text_color=self.theme_cls.primaryColor))

                favorite_button = MDIconButton(icon="star" if component.display_name in self.favorites
                                               else "star-outline",
                                               style="standard", pos_hint={"center_x": 0.85, "center_y": 0.8},
                                               theme_text_color="Custom", text_color=self.theme_cls.primaryColor)
                favorite_button.component = component

                def set_favorite(caller):
                    if caller.component.display_name in self.favorites:
                        self.favorites.remove(caller.component.display_name)
                        caller.icon = "star-outline"
                    else:
                        self.favorites.append(caller.component.display_name)
                        caller.icon = "star"

                favorite_button.bind(on_release=set_favorite)
                button_layout.add_widget(favorite_button)
                context_button = MDIconButton(icon="menu", style="standard",
                                              pos_hint={"center_x": 0.95, "center_y": 0.8}, theme_text_color="Custom",
                                              text_color=self.theme_cls.primaryColor)

                def open_menu(caller):
                    caller.menu.open()

                menu_items = [
                    {
                        "text": "Add shortcut on desktop",
                        "leading_icon": "laptop",
                        "on_release": lambda: create_shortcut(context_button, component)
                    }
                ]
                context_button.menu = MDDropdownMenu(caller=context_button, items=menu_items)
                context_button.bind(on_release=open_menu)
                button_layout.add_widget(context_button)

                button = MDButton(MDButtonText(text="Open"), pos_hint={"center_x": 0.9, "center_y": 0.25},
                                  size_hint_y=None,  height=dp(25))
                button.component = component
                button.bind(on_release=self.component_action)
                button_layout.add_widget(button)

                return button_card

            # clear before repopulating
            assert self.button_layout, "must call `build` first"
            tool_children = reversed(self.button_layout.layout.children)
            for child in tool_children:
                self.button_layout.layout.remove_widget(child)

            _tools = {c.display_name: c for c in components if c.type == Type.TOOL}
            _clients = {c.display_name: c for c in components if c.type == Type.CLIENT}
            _adjusters = {c.display_name: c for c in components if c.type == Type.ADJUSTER}
            _miscs = {c.display_name: c for c in components if c.type == Type.MISC}

            for (name, component) in itertools.chain(
                    _tools.items(), _miscs.items(), _adjusters.items(), _clients.items()):
                if component.type in type_filter or favorites and component.display_name in self.favorites:
                    self.button_layout.layout.add_widget(build_card(component))

        def build(self):
            from kvui import KivyJSONtoTextParser
            text_colors = KivyJSONtoTextParser.TextColors()
            self.theme_cls.theme_style = getattr(text_colors, "theme_style", "Dark")
            self.theme_cls.primary_palette = getattr(text_colors, "primary_palette", "Green")
            self.top_screen = MDFloatLayout()
            self.top_screen.md_bg_color = self.theme_cls.backgroundColor
            self.grid = MDGridLayout(cols=2)
            self.navigation = MDGridLayout(cols=1, size_hint_x=0.25, width=dp(50))
            self.top_screen.add_widget(self.grid)
            self.grid.add_widget(self.navigation)
            self.button_layout = ScrollBox()
            self.button_layout.layout.orientation = "vertical"
            self.button_layout.layout.spacing = 10
            self.button_layout.scroll_wheel_distance = 40
            self.button_layout.do_scroll_x = False
            self.button_layout.scroll_type = ["content", "bars"]
            self.grid.add_widget(self.button_layout)
            self.grid.padding = 10
            self.grid.spacing = 5
            self._refresh_components()

            # handle menu
            menu_icons = {
                "Client": "controller",
                "Tool": "desktop-classic",
                "Adjuster": "wrench",
                "Misc": "dots-horizontal-circle-outline"
            }

            def filter_clients(caller):
                self._refresh_components(caller.type)

            all_item = MDButton(
                MDButtonIcon(icon="asterisk"),
                MDButtonText(text="All"),
                style="text"
            )
            all_item.type = (Type.CLIENT, Type.TOOL, Type.ADJUSTER, Type.MISC)
            all_item.bind(on_release=filter_clients)
            self.navigation.add_widget(all_item)
            for type in (Type.CLIENT, Type.TOOL, Type.ADJUSTER, Type.MISC):
                name = str(type).rsplit(".")[1].title()
                item = MDButton(
                    MDButtonIcon(icon=menu_icons[name]),
                    MDButtonText(text=name),
                    style="text"
                )
                item.type = (type,)
                item.bind(on_release=filter_clients)
                self.navigation.add_widget(item)
            favorite_item = MDButton(
                MDButtonIcon(icon="star"),
                MDButtonText(text="Favorites"),
                style="text"
            )
            favorite_item.type = ("favorites",)
            favorite_item.bind(on_release=filter_clients)
            self.navigation.add_widget(favorite_item)
            self.navigation.add_widget(MDNavigationDrawerDivider())

            global refresh_components
            refresh_components = self._refresh_components

            Window.bind(on_drop_file=self._on_drop_file)

            return self.top_screen

        def on_start(self):
            if self.launch_uri:
                handle_uri(self.launch_uri, self.launch_args)
                self.launch_uri = None
                self.launch_args = None

        @staticmethod
        def component_action(button):
            MDSnackbar(MDSnackbarText(text="Opening in a new window..."), y=dp(24), pos_hint={"center_x": 0.5},
                       size_hint_x=0.5).open()
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

        def on_stop(self):
            Utils.persistent_store("launcher", "favorites", self.favorites)
            super().on_stop()

    Launcher(path=path, args=args).run()

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
        if not path.startswith("archipelago://"):
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
        run_gui(path, args.get("args", ()))


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
