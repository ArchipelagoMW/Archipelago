"""
Archipelago Launcher

* If run with a patch file as argument, launch corresponding client with the patch file as an argument.
* If run with component name as argument, run it passing argv[2:] as arguments.
* If run without arguments or unknown arguments, open launcher GUI.

Additional components can be added to worlds.LauncherComponents.components.
"""

import argparse
import logging
import multiprocessing
import os
import shlex
import subprocess
import sys
import urllib.parse
from collections.abc import Callable, Sequence
from shutil import which
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from worlds.LauncherComponents import Component, Type

if __name__ == "__main__":
    import ModuleUpdate

    ModuleUpdate.update()

import Utils
from Utils import env_cleared_lib_path, init_logging, is_linux, is_macos, is_windows, local_path

if __name__ == "__main__":
    init_logging('Launcher')



def update_settings():
    from settings import get_settings
    get_settings().save()


def handle_uri(path: str) -> tuple[list["Component"], "Component"]:
    from worlds.LauncherComponents import components
    url = urllib.parse.urlparse(path)
    queries = urllib.parse.parse_qs(url.query)
    client_components = []
    text_client_component = None
    game = queries["game"][0]
    for component in components:
        if component.supports_uri and component.game_name == game:
            client_components.append(component)
        elif component.display_name == "Text Client":
            text_client_component = component
    return client_components, text_client_component


def build_uri_popup(component_list: list["Component"], launch_args: tuple[str, ...]) -> None:
    from kvui import ButtonsPrompt
    component_options = {
        component.display_name: component for component in component_list
    }
    popup = ButtonsPrompt("Connect to Multiworld",
                          "Select client to open and connect with.",
                          lambda component_name: run_component(component_options[component_name], *launch_args),
                          *component_options.keys())
    popup.open()



def launch(exe: Sequence[str], in_terminal: bool = False) -> bool:
    """Runs the given command/args in `exe` in a new process.

    If `in_terminal` is True, it will attempt to run in a terminal window,
    and the return value will indicate whether one was found."""
    if in_terminal:
        if is_windows:
            # intentionally using a window title with a space so it gets quoted and treated as a title
            subprocess.Popen(["start", "Running Archipelago", *exe], shell=True)
            return True
        elif is_linux:
            terminal = which("x-terminal-emulator") or which("konsole") or which("gnome-terminal") or which("xterm")
            if terminal:
                # Clear LD_LIB_PATH during terminal startup, but set it again when running command in case it's needed
                ld_lib_path = os.environ.get("LD_LIBRARY_PATH")
                lib_path_setter = f"env LD_LIBRARY_PATH={shlex.quote(ld_lib_path)} " if ld_lib_path else ""
                env = env_cleared_lib_path()

                subprocess.Popen([terminal, "-e", lib_path_setter + shlex.join(exe)], env=env)
                return True
        elif is_macos:
            terminal = [which("open"), "-W", "-a", "Terminal.app"]
            subprocess.Popen([*terminal, *exe])
            return True
    subprocess.Popen(exe)
    return False


def create_shortcut(button: Any, component: "Component") -> None:
    from pyshortcuts import make_shortcut
    env = os.environ
    if "APPIMAGE" in env:
        script = env["ARGV0"]
        wkdir = None # defaults to ~ on Linux
    else:
        script = sys.argv[0]
        wkdir = Utils.local_path()

    script = f"{script} \"{component.display_name}\""
    make_shortcut(script, name=f"Archipelago {component.display_name}", icon=local_path("data", "icon.ico"),
                  startmenu=False, terminal=False, working_dir=wkdir, noexe=Utils.is_frozen())
    button.menu.dismiss()


refresh_components: Callable[[], None] | None = None


def run_gui(launch_components: list["Component"], args: Any) -> None:
    import threading
    from kvui import (ThemedApp, MDFloatLayout, MDGridLayout, ScrollBox,
                      MDScreenManager, MDScreen, LoadingScreen, LogtoLoadingScreen)
    from kivy.properties import ObjectProperty
    from kivy.core.window import Window
    from kivy.metrics import dp
    from kivy.clock import Clock
    from kivymd.uix.button import MDIconButton, MDButton
    from kivymd.uix.card import MDCard
    from kivymd.uix.menu import MDDropdownMenu
    from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
    from kivymd.uix.textfield import MDTextField

    from kivy.lang.builder import Builder

    class LauncherCard(MDCard):
        component: "Component | None"
        image: str
        context_button: MDIconButton = ObjectProperty(None)

        def __init__(self, *args, component: "Component | None" = None, image_path: str = "", **kwargs):
            self.component = component
            self.image = image_path
            super().__init__(args, kwargs)

    class Launcher(ThemedApp):
        base_title: str = "Archipelago Launcher"
        top_screen: MDFloatLayout = ObjectProperty(None)
        navigation: MDGridLayout = ObjectProperty(None)
        grid: MDGridLayout = ObjectProperty(None)
        button_layout: ScrollBox = ObjectProperty(None)
        search_box: MDTextField = ObjectProperty(None)
        cards: list[LauncherCard]
        current_filter: Sequence["Type"] | None

        def __init__(self, ctx=None, components=None, args=None):
            self.title = self.base_title + " " + Utils.__version__
            self.ctx = ctx
            self.icon = r"data/icon.png"
            self.favorites = []
            self.launch_components = components
            self.launch_args = args
            self.cards = []
            self.current_filter = ()
            super().__init__()

        def load_filter(self):
            from worlds.LauncherComponents import Type
            self.current_filter = (Type.CLIENT, Type.TOOL, Type.ADJUSTER, Type.MISC)
            persistent = Utils.persistent_load()
            if "launcher" in persistent:
                if "favorites" in persistent["launcher"]:
                    self.favorites.extend(persistent["launcher"]["favorites"])
                if "filter" in persistent["launcher"]:
                    if persistent["launcher"]["filter"]:
                        filters = []
                        for filter in persistent["launcher"]["filter"].split(", "):
                            if filter == "favorites":
                                filters.append(filter)
                            else:
                                filters.append(Type[filter])
                        self.current_filter = filters

        def set_favorite(self, caller):
            if caller.component.display_name in self.favorites:
                self.favorites.remove(caller.component.display_name)
                caller.icon = "star-outline"
            else:
                self.favorites.append(caller.component.display_name)
                caller.icon = "star"

        def build_card(self, component: "Component") -> LauncherCard:
            """
                Builds a card widget for a given component.

                :param component: The component associated with the button.

                :return: The created Card Widget.
                """
            from worlds.LauncherComponents import icon_paths
            button_card = LauncherCard(component=component,
                                       image_path=icon_paths[component.icon])

            def open_menu(caller):
                caller.menu.open()

            menu_items = [
                {
                    "text": "Add shortcut on desktop",
                    "leading_icon": "laptop",
                    "on_release": lambda: create_shortcut(button_card.context_button, component)
                }
            ]
            button_card.context_button.menu = MDDropdownMenu(caller=button_card.context_button, items=menu_items)
            button_card.context_button.bind(on_release=open_menu)

            return button_card

        def _refresh_components(self, type_filter: Sequence["Type"] | None = None) -> None:
            if not type_filter:
                from worlds.LauncherComponents import Type
                type_filter = [Type.CLIENT, Type.ADJUSTER, Type.TOOL, Type.MISC]
            favorites = "favorites" in type_filter

            # clear before repopulating
            assert self.button_layout, "must call `build` first"
            tool_children = reversed(self.button_layout.layout.children)
            for child in tool_children:
                self.button_layout.layout.remove_widget(child)

            cards = [card for card in self.cards if card.component.type in type_filter
                     or favorites and card.component.display_name in self.favorites]

            self.current_filter = type_filter

            for card in cards:
                self.button_layout.layout.add_widget(card)

            top = self.button_layout.children[0].y + self.button_layout.children[0].height \
                           - self.button_layout.height
            scroll_percent = self.button_layout.convert_distance_to_scroll(0, top)
            self.button_layout.scroll_y = max(0, min(1, scroll_percent[1]))

        def filter_clients_by_type(self, caller: MDButton):
            self._refresh_components(caller.type)
            self.search_box.text = ""

        def filter_clients_by_name(self, caller: MDTextField, name: str) -> None:
            if len(name) == 0:
                self._refresh_components(self.current_filter)
                return
            from worlds.LauncherComponents import Type

            sub_matches = [
                card for card in self.cards
                if name.lower() in card.component.display_name.lower() and card.component.type != Type.HIDDEN
            ]
            self.button_layout.layout.clear_widgets()
            for card in sub_matches:
                self.button_layout.layout.add_widget(card)

        def build(self):
            self.set_colors()
            self.screen_manager = MDScreenManager()
            self.top_screen = Builder.load_file(Utils.local_path("data/launcher.kv"))
            self.loading_screen = LoadingScreen(name="loading")
            self.screen_manager.add_widget(self.loading_screen)
            self.grid = self.top_screen.ids.grid
            self.navigation = self.top_screen.ids.navigation
            self.button_layout = self.top_screen.ids.button_layout
            self.search_box = self.top_screen.ids.search_box
            self.top_screen.md_bg_color = self.theme_cls.backgroundColor

            Window.bind(on_drop_file=self._on_drop_file)
            Window.bind(on_keyboard=self._on_keyboard)

            # Uncomment to re-enable the Kivy console/live editor
            # Ctrl-E to enable it, make sure numlock/capslock is disabled
            # from kivy.modules.console import create_console
            # create_console(Window, self.top_screen)

            main_screen = MDScreen(name="main")
            main_screen.add_widget(self.top_screen)
            self.screen_manager.add_widget(main_screen)

            return self.screen_manager

        def on_start(self):
            super().on_start()
            logger = logging.getLogger("Worlds")
            logger.propagate = False
            self.loading_handler = LogtoLoadingScreen(self.loading_screen.update_text)
            logger.addHandler(self.loading_handler)
            threading.Thread(target=self.do_loading, name="WorldLoading").start()

            if self.launch_components:
                build_uri_popup(self.launch_components, self.launch_args)
                self.launch_components = None
                self.launch_args = None

        def do_loading(self):
            import importlib
            import time
            start = time.perf_counter()
            assert "worlds" not in sys.modules, "worlds module already loaded."
            importlib.import_module("worlds")
            logging.error(f"Worlds module loaded in {time.perf_counter() - start:.2f} seconds")

            global refresh_components
            logger = logging.getLogger("Worlds")
            logger.info("User Data")
            self.load_filter()

            refresh_components = self._refresh_components
            logger.info("Finalizing startup")
            Clock.schedule_once(self.finish_loading)

        def finish_loading(self, dt):
            from worlds.LauncherComponents import components
            logger = logging.getLogger("Worlds")
            for component in components:
                self.cards.append(self.build_card(component))
            self._refresh_components(self.current_filter)
            logger.removeHandler(self.loading_handler)
            self.screen_manager.current = "main"

        @staticmethod
        def component_action(button):
            open_text = "Opening in a new window..."
            if button.component.func:
                # Note: if we want to draw the Snackbar before running func, func needs to be wrapped in schedule_once
                button.component.func()
            else:
                # if launch returns False, it started the process in background (not in a new terminal)
                from worlds.LauncherComponents import get_exe
                if not launch(get_exe(button.component), button.component.cli) and button.component.cli:
                    open_text = "Running in the background..."

            MDSnackbar(MDSnackbarText(text=open_text), y=dp(24), pos_hint={"center_x": 0.5},
                       size_hint_x=0.5).open()

        def _on_drop_file(self, window: Window, filename: bytes, x: int, y: int) -> None:
            """ When a patch file is dropped into the window, run the associated component. """
            from worlds.LauncherComponents import identify
            file, component = identify(filename.decode())
            if file and component:
                run_component(component, file)
            else:
                logging.warning(f"unable to identify component for {filename}")

        def _on_keyboard(self, window: Window, key: int, scancode: int, codepoint: str, modifier: list[str]):
            # Activate search as soon as we start typing, no matter if we are focused on the search box or not.
            # Focus first, then capture the first character we type, otherwise it gets swallowed and lost.
            # Limit text input to ASCII non-control characters (space bar to tilde).
            if not self.search_box.focus:
                self.search_box.focus = True
                if key in range(32, 126):
                    self.search_box.text += codepoint

        def _stop(self, *largs):
            # ran into what appears to be https://groups.google.com/g/kivy-users/c/saWDLoYCSZ4 with PyCharm.
            # Closing the window explicitly cleans it up.
            self.root_window.close()
            super()._stop(*largs)

        def on_stop(self):
            from worlds.LauncherComponents import Type
            Utils.persistent_store("launcher", "favorites", self.favorites)
            Utils.persistent_store("launcher", "filter", ", ".join(filter.name if isinstance(filter, Type) else filter
                                                                   for filter in self.current_filter))
            super().on_stop()

    Launcher(components=launch_components, args=args).run()

    # avoiding Launcher reference leak
    # and don't try to do something with widgets after window closed
    global refresh_components
    refresh_components = None


def run_component(component: "Component", *args):
    global refresh_components
    component.run(*args)
    if refresh_components:
        refresh_components()


def main(args: argparse.Namespace | dict | None = None):
    if isinstance(args, argparse.Namespace):
        args = {k: v for k, v in args._get_kwargs()}
    elif not args:
        args = {}

    path = args.get("Patch|Game|Component|url", None)
    if path is not None:
        if path.startswith("archipelago://"):
            args["args"] = (path, *args.get("args", ()))
            # add the url arg to the passthrough args
            components, text_client_component = handle_uri(path)
            if not components:
                args["component"] = text_client_component
            else:
                args['launch_components'] = [text_client_component, *components]
        else:
            from worlds.LauncherComponents import identify
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
        run_gui(args.get("launch_components", None), args.get("args", ()))


if __name__ == '__main__':
    multiprocessing.freeze_support()
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
