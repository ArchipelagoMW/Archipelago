if __name__ == "__main__":
    import ModuleUpdate

    ModuleUpdate.update()


from kvui import (ThemedApp, ScrollBox, MainLayout, ContainerLayout, dp, Widget, MDBoxLayout, TooltipLabel, MDLabel,
                  ToggleButton, MarkupDropdown, ResizableTextField, HoverBehavior,
                  HoverableMDButton, HoverableToggleButton, HoverableMDIconButton,
                  FixedPositionMDDropdownMenu, FixedScaleMDSlider)
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.text.markup import MarkupLabel
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.utils import escape_markup
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelContent, MDExpansionPanelHeader
from kivymd.uix.list import MDListItem, MDListItemTrailingIcon, MDListItemSupportingText
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.menu.menu import MDDropdownTextItem
from kivymd.uix.slider import MDSlider, MDSliderHandle, MDSliderValueLabel
from copy import deepcopy
import re
import typing
from textwrap import dedent
from urllib.parse import urlparse
import webbrowser
import Utils
from Options import (Option, OptionError, Toggle, TextChoice, Choice, FreeText, NamedRange, Range, OptionSet, OptionList,
                     Removed, OptionCounter, Visibility)
from worlds.AutoWorld import AutoWorldRegister, World

# --- Constants ---
# Matches Generate.handle_name() and game client slot name limits
MAX_SLOT_NAME_LENGTH = 16

# Theme color keys for getattr(app.theme_cls, ...) to avoid string duplication
THEME_SURFACE_CONTAINER_LOWEST = "surfaceContainerLowestColor"
THEME_SURFACE_CONTAINER_LOW = "surfaceContainerLowColor"

# --- Option UI widgets ---


class HoverableDropdownItem(HoverBehavior, MDDropdownTextItem):
    """Dropdown menu item that highlights on hover."""

    def on_enter(self, *args):
        app = ThemedApp.get_running_app()
        if app and hasattr(app, "theme_cls") and hasattr(self, "md_bg_color"):
            self.md_bg_color = getattr(app.theme_cls, THEME_SURFACE_CONTAINER_LOW)
            self.theme_bg_color = "Custom"

    def on_leave(self, *args):
        if hasattr(self, "md_bg_color"):
            self.md_bg_color = (0, 0, 0, 0)
            self.theme_bg_color = "Custom"


Factory.register("HoverableDropdownItem", HoverableDropdownItem)


def validate_url(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False


def filter_tooltip(tooltip):
    if tooltip is None:
        tooltip = "No tooltip available."
    tooltip = dedent(tooltip).strip().replace("\n", "<br>").replace("&", "&amp;") \
        .replace("[", "&bl;").replace("]", "&br;")
    tooltip = re.sub(r"\*\*(.+?)\*\*", r"[b]\g<1>[/b]", tooltip)
    tooltip = re.sub(r"\*(.+?)\*", r"[i]\g<1>[/i]", tooltip)
    return escape_markup(tooltip)


def option_can_be_randomized(option: typing.Type[Option]):
    # most options can be randomized, so we should just check for those that cannot
    if not option.supports_weighting:
        return False
    elif issubclass(option, FreeText) and not issubclass(option, TextChoice):
        return False
    return True


def check_random(value: typing.Any):
    if not isinstance(value, str):
        return value  # cannot be random if evaluated
    if value.startswith("random-"):
        return "random"
    return value


class TrailingPressedIconButton(ButtonBehavior, RotateBehavior, MDListItemTrailingIcon):
    pass


class WorldButton(HoverableToggleButton):
    world_cls: typing.Type[World]
    world_name: str


class OptionRow(MDBoxLayout):
    """Option row layout: label row (with optional random toggle) and option widget container. Filled in create_option."""


class VisualRange(MDBoxLayout):
    option: typing.Type[Range]
    name: str
    tag: MDLabel = ObjectProperty(None)
    slider: MDSlider = ObjectProperty(None)

    def __init__(self, *args, option: typing.Type[Range], name: str, **kwargs):
        self.option = option
        self.name = name
        super().__init__(*args, **kwargs)

        def update_points(*update_args):
            pass

        self.slider._update_points = update_points


class VisualChoice(HoverableMDButton):
    option: typing.Type[Choice]
    name: str
    text: MDButtonText = ObjectProperty(None)

    def __init__(self, *args, option: typing.Type[Choice], name: str, **kwargs):
        self.option = option
        self.name = name
        super().__init__(*args, **kwargs)


class VisualNamedRange(MDBoxLayout):
    option: typing.Type[NamedRange]
    name: str
    range: VisualRange = ObjectProperty(None)
    choice: MDButton = ObjectProperty(None)

    def __init__(self, *args, option: typing.Type[NamedRange], name: str, range_widget: VisualRange, **kwargs):
        self.option = option
        self.name = name
        super().__init__(*args, **kwargs)
        self.range = range_widget
        self.add_widget(self.range)


class VisualFreeText(ResizableTextField):
    option: typing.Type[FreeText] | typing.Type[TextChoice]
    name: str

    def __init__(self, *args, option: typing.Type[FreeText] | typing.Type[TextChoice], name: str, **kwargs):
        self.option = option
        self.name = name
        super().__init__(*args, **kwargs)


class VisualTextChoice(MDBoxLayout):
    option: typing.Type[TextChoice]
    name: str
    choice: VisualChoice = ObjectProperty(None)
    text: VisualFreeText = ObjectProperty(None)

    def __init__(self, *args, option: typing.Type[TextChoice], name: str, choice: VisualChoice,
                 text: VisualFreeText, **kwargs):
        self.option = option
        self.name = name
        super().__init__(*args, **kwargs)
        self.choice = choice
        self.text = text
        self.add_widget(self.choice)
        self.add_widget(self.text)


class VisualToggle(MDBoxLayout):
    button: MDIconButton = ObjectProperty(None)
    option: typing.Type[Toggle]
    name: str

    def __init__(self, *args, option: typing.Type[Toggle], name: str, **kwargs):
        self.option = option
        self.name = name
        super().__init__(*args, **kwargs)


class CounterItemValue(ResizableTextField):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        return super().insert_text(re.sub(self.pat, "", substring), from_undo=from_undo)


class VisualListSetCounter(MDDialog):
    button: MDIconButton = ObjectProperty(None)
    option: typing.Type[OptionSet] | typing.Type[OptionList] | typing.Type[OptionCounter]
    scrollbox: ScrollBox = ObjectProperty(None)
    add: MDIconButton = ObjectProperty(None)
    save: MDButton = ObjectProperty(None)
    input: ResizableTextField = ObjectProperty(None)
    dropdown: MDDropdownMenu
    valid_keys: typing.Iterable[str]

    def __init__(self, *args, option: typing.Type[OptionSet] | typing.Type[OptionList],
                 name: str, valid_keys: typing.Iterable[str], **kwargs):
        self.option = option
        self.name = name
        self.valid_keys = valid_keys
        super().__init__(*args, **kwargs)
        self.dropdown = MarkupDropdown(caller=self.input, border_margin=dp(2),
                                       width=self.input.width, position="bottom")
        self.input.bind(text=self.on_text)
        self.input.bind(on_text_validate=self.validate_add)

    def validate_add(self, instance):
        if self.valid_keys:
            if self.input.text not in self.valid_keys:
                show_result_snack("Item must be a valid key for this option.", "warning")
                return

        if not issubclass(self.option, OptionList):
            if any(self.input.text == child.text.text for child in self.scrollbox.layout.children):
                show_result_snack("This value is already in the set.", "warning")
                return

        self.add_set_item(self.input.text)
        self.input.set_text(self.input, "")

    def remove_item(self, button: MDIconButton):
        list_item = button.parent
        self.scrollbox.layout.remove_widget(list_item)

    def add_set_item(self, key: str, value: int | None = None):
        text = MDListItemSupportingText(text=key, id="value")
        if issubclass(self.option, OptionCounter):
            value_txt = CounterItemValue(text=str(value) if value else "1")
            item = MDListItem(text,
                              value_txt,
                              MDIconButton(icon="minus", on_release=self.remove_item), focus_behavior=False)
            item.value = value_txt
        else:
            item = MDListItem(text, MDIconButton(icon="minus", on_release=self.remove_item), focus_behavior=False)
        item.text = text
        self.scrollbox.layout.add_widget(item)

    def on_text(self, instance, value):
        if not self.valid_keys:
            return
        if len(value) >= 3:
            self.dropdown.items.clear()

            def on_press(txt):
                split_text = MarkupLabel(text=txt, markup=True).markup
                self.input.set_text(self.input, "".join(text_frag for text_frag in split_text
                                                        if not text_frag.startswith("[")))
                self.input.focus = True
                self.dropdown.dismiss()

            lowered = value.lower()
            for item_name in self.valid_keys:
                try:
                    index = item_name.lower().index(lowered)
                except ValueError:
                    pass  # substring not found
                else:
                    text = escape_markup(item_name)
                    text = text[:index] + "[b]" + text[index:index + len(value)] + "[/b]" + text[index + len(value):]
                    self.dropdown.items.append({
                        "text": text,
                        "on_release": lambda txt=text: on_press(txt),
                        "markup": True
                    })
            if not self.dropdown.parent:
                self.dropdown.open()
        else:
            self.dropdown.dismiss()


class OptionsCreator(ThemedApp):
    base_title: str = "Archipelago Options Creator"
    container: ContainerLayout
    main_layout: MainLayout
    scrollbox: ScrollBox
    main_panel: MainLayout
    player_options: MainLayout
    option_layout: MainLayout
    name_input: ResizableTextField
    world_search_input: ResizableTextField
    game_label: MDLabel
    current_game: str
    options: typing.Dict[str, typing.Any]
    world_buttons: list[WorldButton]
    selected_world_button: WorldButton | None

    def __init__(self):
        """Initialize the app title, icon, and option state."""
        self.title = self.base_title + " " + Utils.__version__
        self.icon = r"data/icon.png"
        self.current_game = ""
        self.options = {}
        self.world_buttons = []
        self.selected_world_button = None
        self.options_dropdown_menu: MDDropdownMenu | None = None
        super().__init__()

    def filter_world_buttons(self, value: str) -> None:
        lowered = value.lower().strip()
        self.scrollbox.layout.clear_widgets()
        for world_button in self.world_buttons:
            if lowered in world_button.world_name.lower():
                self.scrollbox.layout.add_widget(world_button)

    def on_export_result(self, text: str | None, level: str = "info") -> None:
        """Re-enable the UI after export and optionally show a result message."""
        self.container.disabled = False
        if text is not None:
            Clock.schedule_once(lambda _: show_result_snack(text, level), 0)

    def export_options_background(self, options: dict[str, typing.Any]) -> None:
        """Run in a background thread: prompt for path and write options YAML to disk."""
        try:
            file_name = Utils.save_filename("Export Options File As...", [("YAML", [".yaml"])],
                                            Utils.get_file_safe_name(f"{self.name_input.text}.yaml"))
        except Exception:
            self.on_export_result("Could not open dialog. Already open?", "error")
            raise

        if not file_name:
            self.on_export_result(None)  # No file selected. No need to show a message for this.
            return

        try:
            with open(file_name, 'w') as f:
                f.write(Utils.dump(options, sort_keys=False))
            self.on_export_result("File saved successfully.", "info")
        except Exception:
            self.on_export_result("Could not save file.", "error")
            raise

    def export_options(self, button: Widget) -> None:
        """Validate name/game, build options dict, and start background export to YAML."""
        if 0 < len(self.name_input.text) <= MAX_SLOT_NAME_LENGTH and self.current_game:
            import threading
            world_cls = AutoWorldRegister.world_types[self.current_game]
            options = {
                "name": self.name_input.text,
                "description": f"YAML generated by Archipelago {Utils.__version__}.",
                "game": self.current_game,
                "world_version": world_cls.world_version.as_simple_string(),
                self.current_game: {k: check_random(v) for k, v in self.options.items()}
            }
            threading.Thread(target=self.export_options_background, args=(options,), daemon=True).start()
            self.container.disabled = True
        elif not self.name_input.text:
            show_result_snack("Name must not be empty.", "error")
        elif not self.current_game:
            show_result_snack("You must select a game to play.", "error")
        else:
            show_result_snack(f"Name cannot be longer than {MAX_SLOT_NAME_LENGTH} characters.", "warning")

    def _import_fail(self, message: str | None = None) -> None:
        Clock.schedule_once(lambda _: self._on_import_result(message), 0)
        Clock.schedule_once(lambda _: setattr(self.container, 'disabled', False), 0)

    def open_options_dropdown(self, trigger: Widget) -> None:
        """Open the options dropdown (Import / Reset to defaults) anchored to the trigger widget."""
        if self.options_dropdown_menu is None:
            return
        self.options_dropdown_menu.caller = trigger
        self.options_dropdown_menu.open()

    def _menu_import_options(self) -> None:
        """Close the dropdown and run the import-from-YAML flow."""
        if self.options_dropdown_menu:
            self.options_dropdown_menu.dismiss()
        self.import_options(None)

    def _menu_reset_to_defaults(self) -> None:
        """Close the dropdown and reset the current game's options to defaults."""
        if self.options_dropdown_menu:
            self.options_dropdown_menu.dismiss()
        self.reset_options_to_defaults()

    def reset_options_to_defaults(self) -> None:
        """Reload the current game's options panel with default values and persist to cache."""
        if not self.current_game:
            show_result_snack("You must select a game first.", "warning")
            return
        self._reset_to_defaults = True
        self.create_options_panel()
        self._save_options_cache()

    def _resolve_options_from_dict(
        self, world_cls: typing.Type[World], raw: dict
    ) -> tuple[dict[str, typing.Any], list[str], list[str]]:
        """Resolve raw option dict to UI values. Returns (resolved, defaulted_from_error, missing)."""
        resolved: dict[str, typing.Any] = {}
        defaulted_from_error: list[str] = []
        missing: list[str] = []
        for name, option in world_cls.options_dataclass.type_hints.items():
            if not name or not (option.visibility & Visibility.simple_ui):
                continue
            if name not in raw:
                resolved[name] = None
                missing.append(name)
                continue
            try:
                opt_instance = option.from_any(raw[name])
                resolved[name] = self._option_value_for_ui(option, opt_instance)
            except (OptionError, Exception):
                resolved[name] = None
                defaulted_from_error.append(name)
        return resolved, defaulted_from_error, missing

    def _option_value_for_ui(self, option: typing.Type[Option], opt_instance: Option) -> typing.Any:
        """Convert Option instance from from_any() to the value stored in self.options."""
        if issubclass(option, (OptionSet, OptionList)):
            return sorted(opt_instance.value)
        if issubclass(option, OptionCounter):
            return dict(opt_instance.value)
        if issubclass(option, Toggle):
            return bool(opt_instance.value)
        return opt_instance.value

    def import_options(self, button: Widget) -> None:
        """Start background YAML import in a thread. Switches to the game from the file if different; name validated after file selection."""
        import threading
        self.container.disabled = True
        threading.Thread(target=self._import_options_background, daemon=True).start()

    def _import_options_background(self) -> None:
        """Run in a background thread: open file dialog, parse YAML, resolve options, then schedule UI apply."""
        try:
            file_name = Utils.open_filename("Import Options from YAML", [("YAML", [".yaml"])])
        except Exception:
            self._import_fail("Could not open dialog. Already open?")
            return
        if not file_name:
            self._import_fail()
            return
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
            data = Utils.parse_yaml(content)
        except Exception:
            self._import_fail("Could not parse YAML.")
            return
        import_game = data.get("game")
        if not import_game or import_game not in AutoWorldRegister.world_types:
            self._import_fail("YAML must specify a valid game.")
            return
        self.pending_import_game = import_game if import_game != self.current_game else None
        world_cls = AutoWorldRegister.world_types[import_game]
        raw_options = data.get(import_game, {})
        imported_name = data.get("name")
        if not isinstance(imported_name, str) or not imported_name.strip():
            self._import_fail("YAML must include a valid name (not empty).")
            return
        imported_name = imported_name.strip()
        if len(imported_name) > MAX_SLOT_NAME_LENGTH:
            self._import_fail(f"Name in file must be 1–{MAX_SLOT_NAME_LENGTH} characters.")
            return
        resolved, defaulted_from_error, missing = self._resolve_options_from_dict(world_cls, raw_options)
        yaml_version = data.get("world_version")
        self.pending_import_name = imported_name
        self.pending_import_options = resolved
        self.pending_import_warnings = defaulted_from_error + missing
        self.pending_import_version_mismatch = bool(
            yaml_version and world_cls.world_version and yaml_version != world_cls.world_version.as_simple_string()
        )
        Clock.schedule_once(lambda _: self._apply_import_and_show_snacks(), 0)

    def _on_import_result(self, text: str | None, level: str = "error") -> None:
        """Re-enable the UI after import and optionally show an error or status message."""
        self.container.disabled = False
        if text is not None:
            show_result_snack(text, level)

    def _apply_import_and_show_snacks(self) -> None:
        """Apply pending imported options to the panel, show warnings/version snackbars, and save cache."""
        self.container.disabled = False
        self._applying_import_or_cache = True
        if getattr(self, 'pending_import_game', None) is not None:
            self.current_game = self.pending_import_game
            self.pending_import_game = None
            # Clear search so the switched-to world is visible and its button can be highlighted
            if getattr(self, "world_search_input", None) is not None:
                self.world_search_input.text = ""
            self._sync_game_button()
        imported_name = getattr(self, 'pending_import_name', None)
        if imported_name is not None:
            self.name_input.text = imported_name
        self.create_options_panel()
        warnings = getattr(self, 'pending_import_warnings', []) or []
        version_mismatch = getattr(self, 'pending_import_version_mismatch', False)
        if warnings:
            show_result_snack(f"Options not found or invalid; defaults used: {_snack_names(warnings)}.", "warning")
        if version_mismatch:
            show_result_snack("YAML world version differs from this apworld; some options may not apply.", "warning")
        self.pending_import_name = None
        self.pending_import_options = None
        self.pending_import_warnings = None
        self.pending_import_version_mismatch = False
        self.pending_import_game = None
        self._applying_import_or_cache = False
        self._save_options_cache()

    def _sync_game_button(self) -> None:
        """Set the world button for current_game to selected (down), all others to normal."""
        if not getattr(self, "scrollbox", None) or not getattr(self.scrollbox, "layout", None):
            return
        self.selected_world_button = None
        for button in self.scrollbox.layout.children:
            if getattr(button, "world_cls", None):
                is_current = button.world_cls.game == self.current_game
                button.state = "down" if is_current else "normal"
                if is_current:
                    self.selected_world_button = button

    def _save_options_cache(self) -> None:
        """Persist current game, name, and options to a per-game YAML cache file when not mid-import."""
        if getattr(self, '_applying_import_or_cache', False) or not self.current_game or self.current_game == "None":
            return
        try:
            world_cls = AutoWorldRegister.world_types[self.current_game]
        except KeyError:
            return
        path = Utils.cache_path("OptionsCreator", Utils.get_file_safe_name(self.current_game) + ".yaml")
        try:
            import os
            os.makedirs(os.path.dirname(path), exist_ok=True)
        except Exception:
            return
        cache_data = {
            "game": self.current_game,
            "world_version": world_cls.world_version.as_simple_string(),
            "name": self.name_input.text,
            "options": {k: check_random(v) for k, v in self.options.items()}
        }
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(Utils.dump(cache_data, sort_keys=False))
        except Exception:
            pass

    def create_range(self, option: typing.Type[Range], name: str, initial_value: typing.Any = None):
        """Build a slider widget for a Range option and bind it to self.options[name]."""
        def update_text(range_box: VisualRange):
            self.options[name] = int(range_box.slider.value)
            range_box.tag.text = str(int(range_box.slider.value))
            self._save_options_cache()

        box = VisualRange(option=option, name=name)
        box.slider.bind(on_touch_move=lambda _, _1: update_text(box))
        if initial_value is not None:
            val = int(initial_value)
            val = min(max(val, option.range_start), option.range_end)
            self.options[name] = val
            box.slider.value = val
            box.tag.text = str(val)
        else:
            self.options[name] = option.default
        return box

    def create_named_range(self, option: typing.Type[NamedRange], name: str, initial_value: typing.Any = None):
        """Build a NamedRange widget (slider + preset choices) and bind it to self.options[name]."""
        def set_to_custom(range_box: VisualNamedRange):
            if (not self.options[name] == range_box.range.slider.value) \
                    and (not self.options[name] in option.special_range_names or
                         range_box.range.slider.value != option.special_range_names[self.options[name]]):
                # we should validate the touch here,
                # but this is much cheaper
                self.options[name] = int(range_box.range.slider.value)
                range_box.range.tag.text = str(int(range_box.range.slider.value))
                set_button_text(range_box.choice, "Custom")
                self._save_options_cache()

        def set_button_text(button: MDButton, text: str):
            button.text.text = text

        def set_value(text: str, range_box: VisualNamedRange):
            range_box.range.slider.value = min(max(option.special_range_names[text.lower()], option.range_start),
                                               option.range_end)
            range_box.range.tag.text = str(int(range_box.range.slider.value))
            set_button_text(range_box.choice, text)
            self.options[name] = text.lower()
            range_box.range.slider.dropdown.dismiss()
            self._save_options_cache()

        def open_dropdown(button):
            # for some reason this fixes an issue causing some to not open
            box.range.slider.dropdown.open()

        range_initial: typing.Any = None
        if initial_value is not None:
            if isinstance(initial_value, str) and initial_value.lower() in option.special_range_names:
                range_initial = option.special_range_names[initial_value.lower()]
            elif isinstance(initial_value, int):
                range_initial = initial_value
        range_widget = self.create_range(option, name, range_initial)
        box = VisualNamedRange(option=option, name=name, range_widget=range_widget)
        if initial_value is not None:
            if isinstance(initial_value, str) and initial_value.lower() in option.special_range_names:
                box.range.slider.value = min(max(option.special_range_names[initial_value.lower()],
                                                option.range_start), option.range_end)
                box.range.tag.text = str(int(box.range.slider.value))
                set_button_text(box.choice, initial_value.title() if isinstance(initial_value, str) else initial_value)
                self.options[name] = initial_value.lower()
            elif isinstance(initial_value, int):
                box.range.slider.value = min(max(initial_value, option.range_start), option.range_end)
                box.range.tag.text = str(int(box.range.slider.value))
                set_button_text(box.choice, "Custom")
                self.options[name] = initial_value
        elif option.default in option.special_range_names:
            # value can get mismatched in this case
            box.range.slider.value = min(max(option.special_range_names[option.default], option.range_start),
                                               option.range_end)
            box.range.tag.text = str(int(box.range.slider.value))
            self.options[name] = option.default
        else:
            self.options[name] = option.default
        box.range.slider.bind(on_touch_move=lambda _, _2: set_to_custom(box))
        items = [
            {
                "text": choice.title(),
                "on_release": lambda text=choice.title(): set_value(text, box),
                "viewclass": "HoverableDropdownItem",
            }
            for choice in option.special_range_names
        ]
        box.range.slider.dropdown = FixedPositionMDDropdownMenu(caller=box.choice, items=items)
        box.choice.bind(on_release=open_dropdown)
        return box

    def create_free_text(self, option: typing.Type[FreeText] | typing.Type[TextChoice], name: str,
                         initial_value: typing.Any = None):
        """Build a free-text field for a FreeText/TextChoice option and bind it to self.options[name]."""
        text = VisualFreeText(option=option, name=name)
        if initial_value is not None:
            self.options[name] = str(initial_value)
            text.text = str(initial_value)
        else:
            self.options[name] = option.default if isinstance(option.default, str) else ""

        def set_value(instance):
            self.options[name] = instance.text
            self._save_options_cache()

        text.bind(on_text_validate=set_value)
        return text

    def create_choice(self, option: typing.Type[Choice], name: str, initial_value: typing.Any = None):
        """Build a choice button with dropdown for a Choice option and bind selection to self.options[name]."""
        def set_button_text(button: VisualChoice, text: str):
            button.text.text = text

        def set_value(text, value):
            set_button_text(main_button, text)
            self.options[name] = value
            dropdown.dismiss()
            self._save_options_cache()

        def open_dropdown(button):
            # for some reason this fixes an issue causing some to not open
            dropdown.open()

        default_string = isinstance(option.default, str)
        main_button = VisualChoice(option=option, name=name)
        main_button.bind(on_release=open_dropdown)

        items = [
            {
                "text": option.get_option_name(choice),
                "on_release": lambda val=choice: set_value(option.get_option_name(val), option.name_lookup[val]),
                "viewclass": "HoverableDropdownItem",
            }
            for choice in option.name_lookup
        ]
        dropdown = FixedPositionMDDropdownMenu(caller=main_button, items=items)
        if initial_value is not None:
            self.options[name] = initial_value
            display = option.get_option_name(initial_value) if initial_value in option.name_lookup else str(initial_value)
            set_button_text(main_button, display)
        else:
            self.options[name] = option.name_lookup[option.default] if not default_string else option.default
        return main_button

    def create_text_choice(self, option: typing.Type[TextChoice], name: str, initial_value: typing.Any = None):
        """Build a TextChoice widget (dropdown + custom text field) and bind to self.options[name]."""
        choice_initial: typing.Any = None
        text_initial: typing.Any = None
        if initial_value is not None:
            if isinstance(initial_value, int) and initial_value in option.name_lookup:
                choice_initial = initial_value
            else:
                text_initial = str(initial_value)
        box = VisualTextChoice(option=option, name=name, choice=self.create_choice(option, name, choice_initial),
                               text=self.create_free_text(option, name, text_initial))

        def set_value(instance):
            set_button_text(box.choice, "Custom")
            self.options[name] = instance.text
            self._save_options_cache()

        box.text.bind(on_text_validate=set_value)
        if initial_value is not None and not (isinstance(initial_value, int) and initial_value in option.name_lookup):
            if hasattr(box.text, 'text'):
                box.text.text = str(initial_value)
        return box

    def create_toggle(self, option: typing.Type[Toggle], name: str, initial_value: typing.Any = None) -> Widget:
        """Build a checkbox-style toggle for a Toggle option and bind to self.options[name]."""
        def set_value(instance: MDIconButton):
            if instance.icon == "checkbox-outline":
                instance.icon = "checkbox-blank-outline"
            else:
                instance.icon = "checkbox-outline"
            self.options[name] = bool(not self.options[name])
            self._save_options_cache()

        if initial_value is not None:
            self.options[name] = bool(initial_value)
        else:
            self.options[name] = bool(option.default)
        checkbox = VisualToggle(option=option, name=name)
        checkbox.button.bind(on_release=set_value)
        if initial_value is not None:
            checkbox.button.icon = "checkbox-outline" if self.options[name] else "checkbox-blank-outline"
        return checkbox

    def create_popup(self, option: typing.Type[OptionList] | typing.Type[OptionSet] | typing.Type[OptionCounter],
                     name: str, world: typing.Type[World]):
        """Open a dialog to edit an OptionSet, OptionList, or OptionCounter; on save, update self.options[name]."""
        valid_keys = sorted(option.valid_keys)
        if option.verify_item_name:
            valid_keys += list(world.item_name_to_id.keys())
        if option.verify_location_name:
            valid_keys += list(world.location_name_to_id.keys())

        def apply_changes(button):
            self.options[name].clear()
            if issubclass(option, OptionCounter):
                for list_item in dialog.scrollbox.layout.children:
                    self.options[name][getattr(list_item.text, "text")] = int(getattr(list_item.value, "text"))
            else:
                for list_item in dialog.scrollbox.layout.children:
                    self.options[name].append(getattr(list_item.text, "text"))
            dialog.dismiss()
            self._save_options_cache()

        dialog = VisualListSetCounter(option=option, name=name, valid_keys=valid_keys)
        dialog.ids.container.spacing = dp(30)
        dialog.scrollbox.layout.theme_bg_color = "Custom"
        dialog.scrollbox.layout.md_bg_color = getattr(self.theme_cls, THEME_SURFACE_CONTAINER_LOW)
        dialog.scrollbox.layout.spacing = dp(5)
        dialog.scrollbox.layout.padding = [0, dp(5), 0, 0]

        if name not in self.options:
            # convert from non-mutable to mutable
            # We use list syntax even for sets, set behavior is enforced through GUI
            if issubclass(option, OptionCounter):
                self.options[name] = deepcopy(option.default)
            else:
                self.options[name] = sorted(option.default)

        if issubclass(option, OptionCounter):
            for value in sorted(self.options[name]):
                dialog.add_set_item(value, self.options[name].get(value, None))
        else:
            for value in sorted(self.options[name]):
                dialog.add_set_item(value)

        dialog.save.bind(on_release=apply_changes)
        dialog.open()

    def create_option_set_list_counter(self, option: typing.Type[OptionList] | typing.Type[OptionSet] |
                                       typing.Type[OptionCounter], name: str, world: typing.Type[World],
                                       initial_value: typing.Any = None):
        """Build an 'Edit' button that opens the set/list/counter popup for this option."""
        if initial_value is not None:
            if issubclass(option, OptionCounter):
                self.options[name] = deepcopy(initial_value)
            else:
                self.options[name] = sorted(initial_value) if isinstance(initial_value, (list, set)) else list(initial_value)
        else:
            if issubclass(option, OptionCounter):
                self.options[name] = deepcopy(option.default)
            else:
                default = option.default
                self.options[name] = sorted(default) if isinstance(default, (list, set)) else list(default)
        main_button = HoverableMDButton(MDButtonText(text="Edit"), on_release=lambda x: self.create_popup(option, name, world))
        return main_button

    def create_option(self, option: typing.Type[Option], name: str, world: typing.Type[World]) -> Widget:
        """Create the appropriate UI control for the option type and attach a random toggle if supported."""
        option_base = OptionRow()
        initial_value = (getattr(self, 'pending_import_options', None) or {}).get(name)

        tooltip = filter_tooltip(option.__doc__)
        option_label = TooltipLabel(text=f"[ref=0|{tooltip}]{getattr(option, 'display_name', name)}")
        option_base.ids.label_anchor.add_widget(option_label)

        if issubclass(option, NamedRange):
            option_base.ids.option_widget_container.add_widget(self.create_named_range(option, name, initial_value))
        elif issubclass(option, Range):
            option_base.ids.option_widget_container.add_widget(self.create_range(option, name, initial_value))
        elif issubclass(option, Toggle):
            option_base.ids.option_widget_container.add_widget(self.create_toggle(option, name, initial_value))
        elif issubclass(option, TextChoice):
            option_base.ids.option_widget_container.add_widget(self.create_text_choice(option, name, initial_value))
        elif issubclass(option, Choice):
            option_base.ids.option_widget_container.add_widget(self.create_choice(option, name, initial_value))
        elif issubclass(option, FreeText):
            option_base.ids.option_widget_container.add_widget(self.create_free_text(option, name, initial_value))
        elif any(issubclass(option, cls) for cls in (OptionSet, OptionList, OptionCounter)):
            option_base.ids.option_widget_container.add_widget(
                self.create_option_set_list_counter(option, name, world, initial_value))
        else:
            option_base.ids.option_widget_container.add_widget(
                MDLabel(text="This option isn't supported by the option creator.\n"
                       "Please edit your yaml manually to set this option."))

        if option_can_be_randomized(option):
            def randomize_option(instance: Widget, value: str):
                value = value == "down"
                if value:
                    self.options[name] = "random-" + str(self.options[name])
                else:
                    self.options[name] = self.options[name].replace("random-", "")
                    if self.options[name].isnumeric():
                        self.options[name] = int(self.options[name])
                    elif self.options[name] in ("True", "False"):
                        self.options[name] = self.options[name] == "True"

                base_object = instance.parent.parent
                label_object = instance.parent
                for child in base_object.children:
                    if child is not label_object:
                        child.disabled = value
                self._save_options_cache()

            default_random = option.default == "random"
            random_toggle = HoverableToggleButton(MDButtonText(text="Random?"), size_hint_x=None, width=dp(100),
                                         state="down" if default_random else "normal")
            random_toggle.bind(state=randomize_option)
            option_base.ids.label_box.add_widget(random_toggle)
            if default_random:
                randomize_option(random_toggle, "down")

        return option_base

    def _handle_external_options_page(self, cls: typing.Type[World]) -> None:
        """Unpress world button, set current_game to None, open URL in browser, show snack."""
        self.current_game = "None"
        self._sync_game_button()
        url = cls.web.options_page
        if validate_url(url):
            webbrowser.open(url)
            show_result_snack("Launching in default browser...", "info")
            return
        new_url = "https://archipelago.gg/" + url
        if validate_url(new_url):
            webbrowser.open(new_url)
            show_result_snack("Launching in default browser...", "info")
        else:
            show_result_snack("Invalid options page, please report to world developer.", "error")

    def create_options_panel(self):
        """Load or build the options UI for the selected world: cache load, groups, and option widgets."""
        self.option_layout.clear_widgets()
        self.options.clear()
        cls: typing.Type[World] = AutoWorldRegister.world_types[self.current_game]

        if not cls.web.options_page:
            self.current_game = "None"
            self._sync_game_button()
            self.game_label.text = f"Game: {self.current_game}"
            return
        elif isinstance(cls.web.options_page, str):
            self._handle_external_options_page(cls)
            self.game_label.text = f"Game: {self.current_game}"
            return
        else:
            # Reset-to-defaults: skip cache and clear any pending import
            self.pending_cache_removed = []
            self.pending_cache_set_to_default = []
            self.pending_cache_version_mismatch = False
            if getattr(self, '_reset_to_defaults', False):
                self._reset_to_defaults = False
                self.pending_import_options = None
            # Load from cache only when not applying an import (import sets pending_import_options before calling us)
            elif getattr(self, 'pending_import_options', None) is None:
                import os
                cache_file = Utils.cache_path("OptionsCreator", Utils.get_file_safe_name(cls.game) + ".yaml")
                removed: list[str] = []
                set_to_default: list[str] = []
                version_mismatch = False
                if os.path.isfile(cache_file):
                    try:
                        with open(cache_file, 'r', encoding='utf-8') as f:
                            cache = Utils.parse_yaml(f.read())
                    except Exception:
                        cache = None
                    if isinstance(cache, dict) and cache.get("game") == cls.game:
                        cache_opts = cache.get("options", {})
                        cache_version = cache.get("world_version")
                        current_version = cls.world_version.as_simple_string() if cls.world_version else None
                        version_mismatch = bool(cache_version and current_version and cache_version != current_version)
                        current_option_names = {name for name, opt in cls.options_dataclass.type_hints.items()
                                               if name and (opt.visibility & Visibility.simple_ui)}
                        for name in list(cache_opts):
                            if name not in current_option_names:
                                removed.append(name)
                        resolved_cache, defaulted_from_error, missing = self._resolve_options_from_dict(cls, cache_opts)
                        set_to_default = defaulted_from_error + (missing if version_mismatch else [])
                        if resolved_cache:
                            self._applying_import_or_cache = True
                            self.pending_import_options = resolved_cache
                            self.pending_cache_removed = removed
                            self.pending_cache_set_to_default = set_to_default
                            self.pending_cache_version_mismatch = version_mismatch
                            if cache.get("name"):
                                self.name_input.text = str(cache["name"])[:MAX_SLOT_NAME_LENGTH]

            expansion_box = ScrollBox()
            expansion_box.layout.orientation = "vertical"
            expansion_box.layout.spacing = dp(3)
            expansion_box.scroll_type = ["bars"]  # vertical scroll bars only
            expansion_box.do_scroll_x = False  # ScrollView defaults do_scroll_x True
            group_names = ["Game Options", *(group.name for group in cls.web.option_groups)]
            groups = {name: [] for name in group_names}
            for name, option in cls.options_dataclass.type_hints.items():
                group = next((group.name for group in cls.web.option_groups if option in group.options), "Game Options")
                groups[group].append((name, option))

            for group, options in groups.items():
                options = [(name, option) for name, option in options
                           if name and option.visibility & Visibility.simple_ui]
                if not options:
                    continue  # Game Options can be empty if every other option is in another group
                    # Can also have an option group of options that should not render on simple ui
                group_item = MDExpansionPanel(size_hint_y=None)
                group_header = MDExpansionPanelHeader(MDListItem(MDListItemSupportingText(text=group),
                                                                 TrailingPressedIconButton(icon="chevron-right",
                                                                                           on_release=lambda x,
                                                                                           item=group_item:
                                                                                           self.tap_expansion_chevron(
                                                                                               item, x)),
                                                                 md_bg_color=getattr(self.theme_cls, THEME_SURFACE_CONTAINER_LOWEST),
                                                                 theme_bg_color="Custom",
                                                                 on_release=lambda x, item=group_item:
                                                                 self.tap_expansion_chevron(item, x)))
                group_content = MDExpansionPanelContent(orientation="vertical", theme_bg_color="Custom",
                                                        md_bg_color=getattr(self.theme_cls, THEME_SURFACE_CONTAINER_LOWEST),
                                                        padding=[dp(12), dp(100), dp(12), 0],
                                                        spacing=dp(3))
                group_item.add_widget(group_header)
                group_item.add_widget(group_content)
                for name, option in options:
                    group_content.add_widget(self.create_option(option, name, cls))
                expansion_box.layout.add_widget(group_item)
            self.option_layout.add_widget(expansion_box)

            # Show cache load snacks and clear pending cache state
            removed = getattr(self, 'pending_cache_removed', [])
            set_to_default = getattr(self, 'pending_cache_set_to_default', [])
            version_mismatch = getattr(self, 'pending_cache_version_mismatch', False)
            if removed or set_to_default or version_mismatch:
                def _show_cache_snacks(_dt):
                    self._applying_import_or_cache = False
                    if removed:
                        show_result_snack(f"Some options no longer exist: {_snack_names(removed)}.", "warning")
                    if version_mismatch and set_to_default:
                        show_result_snack(f"World version changed; options set to default: {_snack_names(set_to_default)}.", "warning")
                    elif version_mismatch:
                        show_result_snack("World version changed; some options may have been reset.", "warning")
                    self.pending_cache_removed = []
                    self.pending_cache_set_to_default = []
                    self.pending_cache_version_mismatch = False
                Clock.schedule_once(_show_cache_snacks, 0)
            else:
                self._applying_import_or_cache = False
        self.game_label.text = f"Game: {self.current_game}"

    @staticmethod
    def tap_expansion_chevron(panel: MDExpansionPanel, chevron: TrailingPressedIconButton | MDListItem):
        """Toggle the expansion panel open/closed and update the chevron icon."""
        if isinstance(chevron, MDListItem):
            chevron = next((child for child in chevron.ids.trailing_container.children
                            if isinstance(child, TrailingPressedIconButton)), None)
        panel.open() if not panel.is_open else panel.close()
        if chevron:
            panel.set_chevron_down(
                chevron
            ) if not panel.is_open else panel.set_chevron_up(chevron)

    def build(self):
        """Build the root layout, world buttons, option dropdown, and wire bindings."""
        self.set_colors()
        self.container = Builder.load_file(Utils.local_path("data/optionscreator.kv"))
        self.root = self.container
        self.main_layout = self.container.ids.main
        self.scrollbox = self.container.ids.scrollbox

        def world_button_action(world_btn: WorldButton):
            if self.selected_world_button and self.selected_world_button is not world_btn:
                self.selected_world_button.state = "normal"
            world_btn.state = "down"
            self.selected_world_button = world_btn
            self.current_game = world_btn.world_cls.game
            self.create_options_panel()

        for world, cls in sorted(AutoWorldRegister.world_types.items(), key=lambda x: x[0]):
            if cls.hidden:
                continue
            world_text = MDButtonText(text=world, size_hint_y=None, width=dp(150),
                                      pos_hint={"x": 0.03, "center_y": 0.5})
            world_text.text_size = (world_text.width, None)
            world_text.bind(width=lambda *x, text=world_text: text.setter('text_size')(text, (text.width, None)),
                            texture_size=lambda *x, text=world_text: text.setter("height")(text,
                                                                                           world_text.texture_size[1]))
            world_button = WorldButton(world_text)
            world_button.bind(on_release=world_button_action)
            world_button.world_cls = cls
            world_button.world_name = world
            self.world_buttons.append(world_button)
            self.scrollbox.layout.add_widget(world_button)
        self.main_panel = self.container.ids.player_layout
        self.player_options = self.container.ids.player_options
        self.game_label = self.container.ids.game
        self.name_input = self.container.ids.player_name
        self.world_search_input = self.container.ids.world_search
        self.option_layout = self.container.ids.options
        self.world_search_input.bind(text=lambda instance, value: self.filter_world_buttons(value))

        trigger = self.container.ids.options_dropdown_trigger
        self.options_dropdown_menu = MDDropdownMenu(
            caller=trigger,
            items=[
                {"text": "Import from YAML", "on_release": self._menu_import_options, "height": dp(56), "viewclass": "HoverableDropdownItem"},
                {"text": "Reset to defaults", "on_release": self._menu_reset_to_defaults, "height": dp(56), "viewclass": "HoverableDropdownItem"},
            ],
            md_bg_color=getattr(self.theme_cls, THEME_SURFACE_CONTAINER_LOWEST),
            theme_bg_color="Custom",
            radius=[dp(5)],
        )

        def set_height(instance, value):
            instance.height = value[1]

        self.game_label.bind(texture_size=set_height)

        # Uncomment to re-enable the Kivy console/live editor
        # Ctrl-E to enable it, make sure numlock/capslock is disabled
        # from kivy.modules.console import create_console
        # from kivy.core.window import Window
        # create_console(Window, self.container)

        return self.container


# --- Result toasts (stacking snackbar) ---

def _snack_names(lst: list[str], max_show: int = 8) -> str:
    """Format a list of names for snackbar; truncate with 'and N others' if needed."""
    return ", ".join(lst) if len(lst) <= max_show else ", ".join(lst[:max_show - 1]) + f" and {len(lst) - max_show + 1} others."


_snackbar_stack: MDBoxLayout | None = None


def _get_snackbar_stack() -> MDBoxLayout:
    """Return the shared snackbar stack container, creating and adding it to the Window if needed."""
    global _snackbar_stack
    if _snackbar_stack is None:
        _snackbar_stack = MDBoxLayout(
            orientation="vertical",
            size_hint_x=1,
            size_hint_y=None,
            height=0,
            padding=[0, 0, 0, dp(24)],
            spacing=dp(8),
            pos_hint={"center_x": 0.5, "bottom": 1},
        )
        _snackbar_stack.bind(minimum_height=_snackbar_stack.setter("height"))
        Window.add_widget(_snackbar_stack)
    return _snackbar_stack


class ResultSnackbar(MDCard):
    """Single snackbar: wrapping label (left), close button (right), level-based color, auto-dismiss."""

    def __init__(self, text: str, level: str = "info", duration: float = 8, **kwargs):
        if level == "error":
            bg = (0.55, 0.15, 0.15, 1)
        elif level == "warning":
            bg = (0.6, 0.42, 0.05, 1)
        else:
            bg = (0.18, 0.4, 0.58, 1)
        kwargs.setdefault("theme_bg_color", "Custom")
        kwargs.setdefault("md_bg_color", bg)
        super().__init__(**kwargs)
        self.opacity = 0
        self.size_hint_x = None
        self.size_hint_y = None
        self.pos_hint = {"center_x": 0.5}
        wrap_width = max(int(Window.size[0] * 0.48), dp(250))
        self.width = wrap_width + dp(56)
        self._duration = duration
        self._stack: MDBoxLayout | None = None

        label = Label(
            text=text,
            padding=(dp(4), dp(4)),
            size_hint_x=1,
            size_hint_y=None,
            text_size=(wrap_width, None),
            halign="left",
            valign="middle",
        )
        label.bind(texture_size=lambda w, ts: setattr(w, "height", ts[1]))
        label_anchor = MDAnchorLayout(anchor_x="left", anchor_y="center", size_hint_x=1, size_hint_y=1)
        label_anchor.add_widget(label)
        content_box = MDBoxLayout(orientation="horizontal", size_hint_x=1, size_hint_y=1, padding=[dp(16), dp(8), dp(4), dp(12)])
        content_box.add_widget(label_anchor)

        close_btn = MDIconButton(
            icon="close",
            size_hint_x=None,
            size_hint_y=None,
            width=dp(48),
            height=dp(48),
        )
        close_btn.bind(on_release=lambda *a: self.dismiss())
        btn_anchor = MDAnchorLayout(anchor_x="center", anchor_y="center", size_hint_x=None, width=close_btn.width, size_hint_y=1)
        btn_anchor.add_widget(close_btn)
        content_box.add_widget(btn_anchor)

        self.add_widget(content_box)
        self._label = label
        self._content_box = content_box
        self.height = 0

    def _sync_content_height(self, *args: object) -> None:
        if hasattr(self, "_content_box") and self._content_box:
            self._content_box.height = self.height

    def dismiss(self) -> None:
        """Fade out and remove from stack."""
        if self._stack is None:
            return

        def remove(anim, widget):
            if self._stack and self.parent == self._stack:
                self._stack.remove_widget(self)
            self._stack = None

        anim = Animation(opacity=0, duration=0.15)
        anim.bind(on_complete=remove)
        anim.start(self)

    def _layout_height(self, _dt: float) -> None:
        extra = dp(30)
        h = self._label.height + extra
        self._content_box.size_hint_y = None
        self.bind(height=self._sync_content_height)
        self._label.bind(height=lambda w, val: self._update_height(val + extra))
        Animation(height=h, duration=0.2).start(self)
        Animation(opacity=1, duration=0.2).start(self)
        if self._duration > 0:
            Clock.schedule_once(
                lambda dt: self.dismiss() if self._stack and self.parent else None,
                self._duration,
            )

    def _update_height(self, h: float) -> None:
        self.height = h
        if hasattr(self, "_content_box") and self._content_box:
            self._content_box.height = h


def show_result_snack(text: str, level: str = "info") -> None:
    """Show a stacking snackbar with wrapping text and level-based color. One-line API: text + type."""
    stack = _get_snackbar_stack()
    snack = ResultSnackbar(text=text, level=level, duration=8)
    snack._stack = stack
    stack.add_widget(snack)
    Clock.schedule_once(snack._layout_height, 0)


def launch():
    OptionsCreator().run()


if __name__ == "__main__":
    Utils.init_logging("OptionsCreator")
    launch()
