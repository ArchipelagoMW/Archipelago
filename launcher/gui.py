from __future__ import annotations

import importlib
import logging
from collections.abc import Sequence
from typing import Any

import Utils
from core import ComponentKind

from .components import activate_component, run_component, set_refresh_components
from .models import LauncherEntry
from .resolution import get_components, identify
from .runtime import create_shortcut


def _icon_paths() -> dict[str, str]:
    """Load launcher icon paths lazily."""

    from worlds.LauncherComponents import icon_paths

    return icon_paths


def build_uri_popup(component_list: list[LauncherEntry], launch_args: tuple[str, ...]) -> None:
    """Build the URI component selection popup.

    Example::

        build_uri_popup(components, ("archipelago://example",))
    """

    from kvui import ButtonsPrompt

    component_options = {component.display_name: component for component in component_list}
    popup = ButtonsPrompt(
        "Connect to Multiworld",
        "Select client to open and connect with.",
        lambda component_name: run_component(component_options[component_name], *launch_args),
        *component_options.keys(),
    )
    popup.open()


def run_gui(launch_components: list[LauncherEntry] | None, args: Sequence[str]) -> None:
    """Run the launcher Kivy GUI.

    Example::

        run_gui(None, ())
    """

    import kvui

    Window = importlib.import_module("kivy.core.window").Window
    Builder = importlib.import_module("kivy.lang.builder").Builder
    dp = importlib.import_module("kivy.metrics").dp
    ObjectProperty = importlib.import_module("kivy.properties").ObjectProperty
    button_module = importlib.import_module("kivymd.uix.button")
    MDButton = button_module.MDButton
    MDCard = importlib.import_module("kivymd.uix.card").MDCard
    MDDropdownMenu = importlib.import_module("kivymd.uix.menu").MDDropdownMenu
    snackbar_module = importlib.import_module("kivymd.uix.snackbar")
    MDSnackbar = snackbar_module.MDSnackbar
    MDSnackbarText = snackbar_module.MDSnackbarText
    MDTextField = importlib.import_module("kivymd.uix.textfield").MDTextField

    MDFloatLayout = kvui.MDFloatLayout
    MDGridLayout = kvui.MDGridLayout
    ScrollBox = kvui.ScrollBox
    ThemedApp = kvui.ThemedApp
    globals()["Type"] = ComponentKind

    class LauncherCard(MDCard):
        component: LauncherEntry
        image: str
        context_button: Any = ObjectProperty(None)

        def __init__(self, *card_args, component: LauncherEntry, image_path: str = "", **kwargs):
            self.component = component
            self.image = image_path
            super().__init__(*card_args, **kwargs)

    class Launcher(ThemedApp):
        base_title: str = "Archipelago Launcher"
        top_screen: Any = ObjectProperty(None)
        navigation: Any = ObjectProperty(None)
        grid: Any = ObjectProperty(None)
        button_layout: Any = ObjectProperty(None)
        search_box: Any = ObjectProperty(None)
        cards: list[LauncherCard]
        current_filter: Sequence[str | ComponentKind] | None

        def __init__(self, ctx=None, components=None, args=None):
            self.title = self.base_title + " " + Utils.__version__
            self.ctx = ctx
            self.icon = r"data/icon.png"
            self.favorites: list[str] = []
            self.launch_components = components
            self.launch_args = args
            self.cards = []
            self.current_filter = (ComponentKind.CLIENT, ComponentKind.TOOL, ComponentKind.ADJUSTER, ComponentKind.MISC)
            persistent = Utils.persistent_load()
            if "launcher" in persistent:
                if "favorites" in persistent["launcher"]:
                    self.favorites.extend(persistent["launcher"]["favorites"])
                if "filter" in persistent["launcher"] and persistent["launcher"]["filter"]:
                    filters: list[str | ComponentKind] = []
                    for component_filter in persistent["launcher"]["filter"].split(", "):
                        if component_filter == "favorites":
                            filters.append(component_filter)
                        else:
                            filters.append(ComponentKind[component_filter])
                    self.current_filter = filters
            super().__init__()

        @staticmethod
        def _normalize_filter_values(type_filter: Sequence[str | ComponentKind] | None) -> list[str | ComponentKind]:
            """Map persisted/KV filter values onto `ComponentKind` members."""

            if not type_filter:
                return [ComponentKind.CLIENT, ComponentKind.ADJUSTER, ComponentKind.TOOL, ComponentKind.MISC]

            normalized: list[str | ComponentKind] = []
            for value in type_filter:
                if value == "favorites":
                    normalized.append(value)
                    continue
                if isinstance(value, ComponentKind):
                    normalized.append(value)
                    continue

                member_name = getattr(value, "name", None)
                if isinstance(member_name, str) and member_name in ComponentKind.__members__:
                    normalized.append(ComponentKind[member_name])
                    continue

                if isinstance(value, str):
                    upper_value = value.upper()
                    if upper_value in ComponentKind.__members__:
                        normalized.append(ComponentKind[upper_value])
            return normalized

        def set_favorite(self, caller):
            if caller.component.display_name in self.favorites:
                self.favorites.remove(caller.component.display_name)
                caller.icon = "star-outline"
            else:
                self.favorites.append(caller.component.display_name)
                caller.icon = "star"

        def build_card(self, component: LauncherEntry) -> LauncherCard:
            """Build a launcher card widget for `component`.

            Example::

                card = self.build_card(component)
            """

            button_card = LauncherCard(component=component, image_path=_icon_paths().get(component.icon, _icon_paths()["icon"]))

            def open_menu(caller):
                caller.menu.open()

            menu_items = [
                {
                    "text": "Add shortcut on desktop",
                    "leading_icon": "laptop",
                    "on_release": lambda: create_shortcut(button_card.context_button, component),
                }
            ]
            button_card.context_button.menu = MDDropdownMenu(caller=button_card.context_button, items=menu_items)
            button_card.context_button.bind(on_release=open_menu)
            return button_card

        def _refresh_components(self, type_filter: Sequence[str | ComponentKind] | None = None) -> None:
            type_filter = self._normalize_filter_values(type_filter)
            favorites = "favorites" in type_filter

            assert self.button_layout, "must call `build` first"
            for child in reversed(self.button_layout.layout.children):
                self.button_layout.layout.remove_widget(child)

            cards = [
                card
                for card in self.cards
                if card.component.kind in type_filter or favorites and card.component.display_name in self.favorites
            ]
            self.current_filter = type_filter

            for card in cards:
                self.button_layout.layout.add_widget(card)

            if not self.button_layout.layout.children:
                return
            top_child = self.button_layout.layout.children[0]
            top = top_child.y + top_child.height - self.button_layout.height
            scroll_percent = self.button_layout.convert_distance_to_scroll(0, top)
            self.button_layout.scroll_y = max(0, min(1, scroll_percent[1]))

        def filter_clients_by_type(self, caller: Any):
            self._refresh_components(caller.type)
            self.search_box.text = ""

        def filter_clients_by_name(self, caller: Any, name: str) -> None:
            if len(name) == 0:
                self._refresh_components(self.current_filter)
                return

            sub_matches = [
                card
                for card in self.cards
                if name.lower() in card.component.display_name.lower() and card.component.kind is not ComponentKind.HIDDEN
            ]
            self.button_layout.layout.clear_widgets()
            for card in sub_matches:
                self.button_layout.layout.add_widget(card)

        def build(self):
            self.top_screen = Builder.load_file(Utils.local_path("data/launcher.kv"))
            self.grid = self.top_screen.ids.grid
            self.navigation = self.top_screen.ids.navigation
            self.button_layout = self.top_screen.ids.button_layout
            self.search_box = self.top_screen.ids.search_box
            self.set_colors()
            self.top_screen.md_bg_color = self.theme_cls.backgroundColor

            set_refresh_components(self._refresh_components)

            Window.bind(on_drop_file=self._on_drop_file)
            Window.bind(on_keyboard=self._on_keyboard)

            for component in get_components():
                self.cards.append(self.build_card(component))

            self._refresh_components(self.current_filter)
            return self.top_screen

        def on_start(self):
            if self.launch_components:
                build_uri_popup(self.launch_components, tuple(self.launch_args or ()))
                self.launch_components = None
                self.launch_args = None

        @staticmethod
        def component_action(button):
            open_text = activate_component(button.component)
            MDSnackbar(
                MDSnackbarText(text=open_text),
                y=dp(24),
                pos_hint={"center_x": 0.5},
                size_hint_x=0.5,
            ).open()

        def _on_drop_file(self, window: Any, filename: bytes, x: int, y: int) -> None:
            """Run the component associated with a dropped file."""

            file_path, component = identify(filename.decode())
            if file_path and component is not None:
                run_component(component, file_path)
            else:
                logging.warning(f"unable to identify component for {filename}")

        def _on_keyboard(self, window: Any, key: int, scancode: int, codepoint: str, modifier: list[str]):
            if not self.search_box.focus:
                self.search_box.focus = True
                if key in range(32, 126):
                    self.search_box.text += codepoint

        def _stop(self, *largs):
            self.root_window.close()
            super()._stop(*largs)

        def on_stop(self):
            Utils.persistent_store("launcher", "favorites", self.favorites)
            Utils.persistent_store(
                "launcher",
                "filter",
                ", ".join(
                    component_filter.name if isinstance(component_filter, ComponentKind) else component_filter
                    for component_filter in self.current_filter or ()
                ),
            )
            super().on_stop()

    Launcher(components=launch_components, args=args).run()
    set_refresh_components(None)
