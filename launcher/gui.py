from __future__ import annotations

import importlib
import logging
from collections.abc import Sequence
from typing import Any

import Utils
from core import ComponentKind, Err, Ok, StartLocalHost, StopJob

from .components import activate_component, run_component, set_refresh_components
from .components.host import is_host_component
from .bridge import dispatch, subscribe_events, unsubscribe_events
from .models import LauncherEntry
from .resolution import get_components, identify
from .runtime import create_shortcut


def _icon_paths() -> dict[str, str]:
    """Load launcher icon paths lazily."""

    from worlds.LauncherComponents import icon_paths

    return icon_paths


def _stdout_log(message: str) -> None:
    """Write launcher UI activity to stdout for foreground terminal sessions."""

    print(f"[launcher] {message}", flush=True)


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
    Animation = importlib.import_module("kivy.animation").Animation
    Clock = importlib.import_module("kivy.clock").Clock
    dp = importlib.import_module("kivy.metrics").dp
    properties_module = importlib.import_module("kivy.properties")
    BooleanProperty = properties_module.BooleanProperty
    NumericProperty = properties_module.NumericProperty
    ObjectProperty = properties_module.ObjectProperty
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
    MDScreen = kvui.MDScreen
    MDScreenManager = kvui.MDScreenManagerBase
    ScrollBox = kvui.ScrollBox
    ThemedApp = kvui.ThemedApp
    globals()["Type"] = ComponentKind

    class LauncherCard(MDCard):
        expanded = BooleanProperty(False)
        collapsed_height = NumericProperty(dp(58))
        expanded_height = NumericProperty(dp(84))
        _press_pos: tuple[float, float] | None = None
        component: LauncherEntry
        image: str
        context_button: Any = ObjectProperty(None)

        def __init__(self, *card_args, component: LauncherEntry, image_path: str = "", **kwargs):
            self.component = component
            self.image = image_path
            super().__init__(*card_args, **kwargs)
            self.register_event_type("on_card_release")

        def on_card_release(self) -> None:
            pass

        def on_touch_down(self, touch):
            if touch.is_mouse_scrolling:
                return super().on_touch_down(touch)
            if self.collide_point(*touch.pos):
                self._press_pos = touch.pos
            return super().on_touch_down(touch)

        def get_expanded_height(self) -> float:
            description_label = self.ids.get("description_label")
            text_stack = self.ids.get("text_stack")
            if description_label is None or text_stack is None:
                return self.expanded_height

            description_label.texture_update()
            text_stack.do_layout()
            base_height = max(self.collapsed_height, dp(58))
            extra_height = max(0, description_label.texture_size[1] - dp(14))
            return max(base_height, base_height + extra_height)

        def on_touch_up(self, touch):
            if super().on_touch_up(touch):
                return True
            if touch.is_mouse_scrolling:
                self._press_pos = None
                return False
            action_row = self.ids.get("action_row")
            if action_row is not None and action_row.collide_point(*action_row.to_widget(*touch.pos)):
                self._press_pos = None
                return False
            if self.collide_point(*touch.pos) and self._press_pos is not None:
                dx = touch.pos[0] - self._press_pos[0]
                dy = touch.pos[1] - self._press_pos[1]
                self._press_pos = None
                if abs(dx) > dp(8) or abs(dy) > dp(8):
                    return False
                self.dispatch("on_card_release")
                return True
            self._press_pos = None
            return False

    class HostScreen(MDScreen):
        selected_path_label: Any = ObjectProperty(None)
        status_label: Any = ObjectProperty(None)
        log_output: Any = ObjectProperty(None)
        start_button: Any = ObjectProperty(None)
        stop_button: Any = ObjectProperty(None)
        load_button: Any = ObjectProperty(None)

    class Launcher(ThemedApp):
        base_title: str = "Archipelago Launcher"
        screen_manager: Any = ObjectProperty(None)
        top_screen: Any = ObjectProperty(None)
        host_screen: Any = ObjectProperty(None)
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
            self.host_component: LauncherEntry | None = None
            self.host_multidata_path: str = ""
            self.host_job_id: str | None = None
            self.host_event_subscription: int | None = None
            self.host_status_text = "Select a multi-world file to start hosting."
            self.host_log_text = ""
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
            button_card.bind(on_card_release=lambda card: self.toggle_card(card))
            return button_card

        def show_launcher_screen(self) -> None:
            if self.screen_manager is not None:
                self.screen_manager.current = "launcher"

        def show_host_screen(self, component: LauncherEntry | None = None) -> None:
            if component is not None:
                self.host_component = component
            self._sync_host_screen()
            if self.screen_manager is not None:
                self.screen_manager.current = "host"

        def load_host_multidata(self) -> None:
            filetypes = (("Multiworld data", (".archipelago", ".zip")),)
            selected_path = Utils.open_filename("Select multiworld data", filetypes) or ""
            if not selected_path:
                return
            self.host_multidata_path = selected_path
            self.host_status_text = f"Loaded {selected_path}"
            self._sync_host_screen()

        def start_host(self) -> None:
            if self.host_job_id:
                self.host_status_text = "Host is already running."
                self._sync_host_screen()
                return
            if not self.host_multidata_path:
                self.host_status_text = "Load a multi-world file before starting the host."
                self._sync_host_screen()
                return

            result = dispatch(StartLocalHost(multidata_path=self.host_multidata_path))
            match result:
                case Err(error=error):
                    self.host_status_text = error.message
                case Ok(value=value):
                    self.host_log_text = ""
                    self.host_job_id = value.job_id
                    self.host_status_text = f"Starting host for {self.host_multidata_path}"
            self._sync_host_screen()

        def stop_host(self) -> None:
            if not self.host_job_id:
                self.host_status_text = "Host is not running."
                self._sync_host_screen()
                return

            result = dispatch(StopJob(job_id=self.host_job_id))
            match result:
                case Err(error=error):
                    self.host_status_text = error.message
                case Ok():
                    self.host_status_text = "Stopping host..."
            self._sync_host_screen()

        def _handle_core_event(self, event: Any) -> None:
            Clock.schedule_once(lambda *_args: self._apply_core_event(event))

        def _apply_core_event(self, event: Any) -> None:
            data = getattr(event, "data", None)
            if not isinstance(data, dict):
                return
            if data.get("job_id") != self.host_job_id:
                return

            if event.name == "job_log":
                message = data.get("message")
                if isinstance(message, str):
                    self.host_log_text = f"{self.host_log_text}\n{message}".strip()
                    self._sync_host_screen()
                return

            if event.name != "job_status":
                return

            status = data.get("status")
            error = data.get("error")
            if status == "running":
                self.host_status_text = "Host running."
            elif status == "pending":
                self.host_status_text = "Starting host..."
            elif status == "cancelled":
                self.host_status_text = "Host stopped."
                self.host_job_id = None
            elif status == "failed":
                self.host_status_text = error if isinstance(error, str) and error else "Host failed."
                self.host_job_id = None
            elif status == "succeeded":
                self.host_status_text = "Host completed."
                self.host_job_id = None

            self._sync_host_screen()

        def _sync_host_screen(self) -> None:
            if not self.host_screen:
                return

            selected_path = self.host_multidata_path or "No multi-world loaded."
            self.host_screen.selected_path_label.text = selected_path
            self.host_screen.status_label.text = self.host_status_text
            self.host_screen.log_output.text = self.host_log_text
            self.host_screen.start_button.disabled = not self.host_multidata_path or self.host_job_id is not None
            self.host_screen.stop_button.disabled = self.host_job_id is None

        @staticmethod
        def _describe_filter(type_filter: Sequence[str | ComponentKind]) -> list[str]:
            return [value if isinstance(value, str) else value.name for value in type_filter]

        @staticmethod
        def _describe_cards(cards: Sequence[LauncherCard]) -> list[str]:
            return [card.component.display_name for card in cards]

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
            _stdout_log(
                "filter changed: "
                f"filters={self._describe_filter(type_filter)} "
                f"count={len(cards)} "
                f"components={self._describe_cards(cards)}"
            )

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
                _stdout_log("search cleared")
                self._refresh_components(self.current_filter)
                return

            sub_matches = [
                card
                for card in self.cards
                if name.lower() in card.component.display_name.lower() and card.component.kind is not ComponentKind.HIDDEN
            ]
            _stdout_log(
                "search changed: "
                f"query={name!r} "
                f"count={len(sub_matches)} "
                f"components={self._describe_cards(sub_matches)}"
            )
            self.button_layout.layout.clear_widgets()
            for card in sub_matches:
                self.button_layout.layout.add_widget(card)

        def toggle_card(self, card: LauncherCard) -> None:
            expand = not card.expanded
            for other_card in self.cards:
                other_card.expanded = expand and other_card is card
                target_height = other_card.get_expanded_height() if other_card.expanded else other_card.collapsed_height
                Animation.cancel_all(other_card, "height")
                Animation(height=target_height, duration=0.12, t="out_quad").start(other_card)

        def build(self):
            self.top_screen = Builder.load_file(Utils.local_path("data/launcher.kv"))
            self.host_screen = Builder.load_file(Utils.local_path("data/host.kv"))
            self.grid = self.top_screen.ids.grid
            self.navigation = self.top_screen.ids.navigation
            self.button_layout = self.top_screen.ids.button_layout
            self.search_box = self.top_screen.ids.search_box
            self.button_layout.layout.padding = (dp(12), dp(6), dp(24), dp(10))
            self.button_layout.layout.spacing = dp(12)
            self.set_colors()
            self.top_screen.md_bg_color = self.theme_cls.backgroundColor
            self.host_screen.md_bg_color = self.theme_cls.backgroundColor
            self.host_event_subscription = subscribe_events(self._handle_core_event)

            launcher_screen = MDScreen(name="launcher")
            launcher_screen.add_widget(self.top_screen)
            self.screen_manager = MDScreenManager()
            self.screen_manager.add_widget(launcher_screen)
            self.screen_manager.add_widget(self.host_screen)

            set_refresh_components(self._refresh_components)

            Window.bind(on_drop_file=self._on_drop_file)
            Window.bind(on_keyboard=self._on_keyboard)

            for component in get_components():
                self.cards.append(self.build_card(component))

            self._refresh_components(self.current_filter)
            self._sync_host_screen()
            return self.screen_manager

        def on_start(self):
            if self.launch_components:
                build_uri_popup(self.launch_components, tuple(self.launch_args or ()))
                self.launch_components = None
                self.launch_args = None

        def component_action(self, button):
            if is_host_component(button.component):
                self.show_host_screen(button.component)
                return

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
            if self.host_event_subscription is not None:
                unsubscribe_events(self.host_event_subscription)
                self.host_event_subscription = None
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
