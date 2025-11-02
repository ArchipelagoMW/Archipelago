import os
import logging
import sys
import typing
import re
import io
import pkgutil
from collections import deque
assert "kivy" not in sys.modules, "kvui should be imported before kivy for frozen compatibility"

if sys.platform == "win32":
    import ctypes

    # kivy 2.2.0 introduced DPI awareness on Windows, but it makes the UI enter an infinitely recursive re-layout
    # by setting the application to not DPI Aware, Windows handles scaling the entire window on its own, ignoring kivy's
    ctypes.windll.shcore.SetProcessDpiAwareness(0)

os.environ["KIVY_NO_CONSOLELOG"] = "1"
os.environ["KIVY_NO_FILELOG"] = "1"
os.environ["KIVY_NO_ARGS"] = "1"
os.environ["KIVY_LOG_ENABLE"] = "0"

import Utils

if Utils.is_frozen():
    os.environ["KIVY_DATA_DIR"] = Utils.local_path("data")

import platformdirs
os.environ["KIVY_HOME"] = os.path.join(platformdirs.user_config_dir("Archipelago", False), "kivy")
os.makedirs(os.environ["KIVY_HOME"], exist_ok=True)

from kivy.config import Config

Config.set("input", "mouse", "mouse,disable_multitouch")
Config.set("kivy", "exit_on_escape", "0")
Config.set("graphics", "multisamples", "0")  # multisamples crash old intel drivers

# Workaround for an issue where importing kivy.core.window before loading sounds
# will hang the whole application on Linux once the first sound is loaded.
# kivymd imports kivy.core.window, so we have to do this before the first kivymd import.
# No longer necessary when we switch to kivy 3.0.0, which fixes this issue.
from kivy.core.audio import SoundLoader
for classobj in SoundLoader._classes:
    # The least invasive way to force a SoundLoader class to load its audio engine seems to be calling
    # .extensions(), which e.g. in audio_sdl2.pyx then calls a function called "mix_init()"
    classobj.extensions()

from kivymd.uix.divider import MDDivider
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.core.text.markup import MarkupLabel
from kivy.core.image import ImageLoader, ImageLoaderBase, ImageData
from kivy.base import ExceptionHandler, ExceptionManager
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty, StringProperty
from kivy.metrics import dp, sp
from kivy.uix.widget import Widget
from kivy.uix.layout import Layout
from kivy.utils import escape_markup
from kivy.lang import Builder
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.behaviors import FocusBehavior, ToggleButtonBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager

from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.menu.menu import MDDropdownTextItem
from kivymd.uix.dropdownitem import MDDropDownItem, MDDropDownItemText
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon, MDIconButton
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.textfield.textfield import MDTextField
from kivymd.uix.progressindicator import MDLinearProgressIndicator
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.tooltip import MDTooltip, MDTooltipPlain

fade_in_animation = Animation(opacity=0, duration=0) + Animation(opacity=1, duration=0.25)

from NetUtils import JSONtoTextParser, JSONMessagePart, SlotType, HintStatus
from Utils import async_start, get_input_text_from_response

if typing.TYPE_CHECKING:
    import CommonClient

    context_type = CommonClient.CommonContext
else:
    context_type = object

remove_between_brackets = re.compile(r"\[.*?]")


class ThemedApp(MDApp):
    def set_colors(self):
        text_colors = KivyJSONtoTextParser.TextColors()
        self.theme_cls.theme_style = text_colors.theme_style
        self.theme_cls.primary_palette = text_colors.primary_palette
        self.theme_cls.dynamic_scheme_name = text_colors.dynamic_scheme_name
        self.theme_cls.dynamic_scheme_contrast = text_colors.dynamic_scheme_contrast


class ImageIcon(MDButtonIcon, AsyncImage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = ApAsyncImage(**kwargs)
        self.add_widget(self.image)

    def add_widget(self, widget, index=0, canvas=None):
        return super(MDIcon, self).add_widget(widget)


class ImageButton(MDIconButton):
    def __init__(self, **kwargs):
        image_args = dict()
        for kwarg in ("fit_mode", "image_size", "color", "source", "texture"):
            val = kwargs.pop(kwarg, "None")
            if val != "None":
                image_args[kwarg.replace("image_", "")] = val
        super().__init__()
        self.image = ApAsyncImage(**image_args)

        def set_center(button, center):
            self.image.center_x = self.center_x
            self.image.center_y = self.center_y

        self.bind(center=set_center)
        self.add_widget(self.image)

    def add_widget(self, widget, index=0, canvas=None):
        return super(MDIcon, self).add_widget(widget)


class ScrollBox(MDScrollView):
    layout: MDBoxLayout = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# thanks kivymd
class ToggleButton(MDButton, ToggleButtonBehavior):
    def __init__(self, *args, **kwargs):
        super(ToggleButton, self).__init__(*args, **kwargs)
        self.bind(state=self._update_bg)

    def _update_bg(self, _, state: str):
        if self.disabled:
            return
        if self.theme_bg_color == "Primary":
            self.theme_bg_color = "Custom"

        if state == "down":
            self.md_bg_color = self.theme_cls.primaryColor
            for child in self.children:
                if child.theme_text_color == "Primary":
                    child.theme_text_color = "Custom"
                if child.theme_icon_color == "Primary":
                    child.theme_icon_color = "Custom"
                child.text_color = self.theme_cls.onPrimaryColor
                child.icon_color = self.theme_cls.onPrimaryColor
        else:
            self.md_bg_color = self.theme_cls.surfaceContainerLowestColor
            for child in self.children:
                if child.theme_text_color == "Primary":
                    child.theme_text_color = "Custom"
                if child.theme_icon_color == "Primary":
                    child.theme_icon_color = "Custom"
                child.text_color = self.theme_cls.primaryColor
                child.icon_color = self.theme_cls.primaryColor


# thanks kivymd
class ResizableTextField(MDTextField):
    """
    Resizable MDTextField that manually overrides the builtin sizing.

    Note that in order to use this, the sizing must be specified from within a .kv rule.
    """
    def __init__(self, *args, **kwargs):
        # cursed rules override
        rules = Builder.match(self)
        textfield = next((rule for rule in rules if rule.name == f"<MDTextField>"), None)
        if textfield:
            subclasses = rules[rules.index(textfield) + 1:]
            for subclass in subclasses:
                height_rule = subclass.properties.get("height", None)
                if height_rule:
                    height_rule.ignore_prev = True
        super().__init__(*args, **kwargs)


def on_release(self: MDButton, *args):
    super(MDButton, self).on_release(args)
    self.on_leave()


MDButton.on_release = on_release


# I was surprised to find this didn't already exist in kivy :(
class HoverBehavior(object):
    """originally from https://stackoverflow.com/a/605348110"""
    hovered = BooleanProperty(False)
    border_point = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.register_event_type("on_enter")
        self.register_event_type("on_leave")
        Window.bind(mouse_pos=self.on_mouse_pos)
        Window.bind(on_cursor_leave=self.on_cursor_leave)
        super(HoverBehavior, self).__init__(**kwargs)

    def on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return  # Abort if not displayed

        # to_widget translates window pos to within widget pos
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            return  # We have already done what was needed
        self.border_point = pos
        self.hovered = inside

        if inside:
            self.dispatch("on_enter")
        else:
            self.dispatch("on_leave")

    def on_cursor_leave(self, *args):
        # if the mouse left the window, it is obviously no longer inside the hover label.
        self.hovered = BooleanProperty(False)
        self.border_point = ObjectProperty(None)
        self.dispatch("on_leave")


Factory.register("HoverBehavior", HoverBehavior)


class ToolTip(MDTooltipPlain):
    pass


class ServerToolTip(ToolTip):
    pass


class HovererableLabel(HoverBehavior, MDLabel):
    pass


class TooltipLabel(HovererableLabel, MDTooltip):
    tooltip_display_delay = 0.1

    def create_tooltip(self, text, x, y):
        text = text.replace("<br>", "\n").replace("&amp;", "&").replace("&bl;", "[").replace("&br;", "]")
        # position float layout
        center_x, center_y = self.to_window(self.center_x, self.center_y)
        self.shift_y = y - center_y
        shift_x = center_x - x
        if shift_x > 0:
            self.shift_left = shift_x
        else:
            self.shift_right = shift_x

        if self._tooltip:
            # update
            self._tooltip.text = text
        else:
            self._tooltip = ToolTip(text=text, pos_hint={})
            self.display_tooltip()

    def on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return  # Abort if not displayed
        super().on_mouse_pos(window, pos)
        if self.refs and self.hovered:

            tx, ty = self.to_widget(*pos, relative=True)
            # Why TF is Y flipped *within* the texture?
            ty = self.texture_size[1] - ty
            hit = False
            for uid, zones in self.refs.items():
                for zone in zones:
                    x, y, w, h = zone
                    if x <= tx <= w and y <= ty <= h:
                        self.create_tooltip(uid.split("|", 1)[1], *pos)
                        hit = True
                        break
            if not hit:
                self.remove_tooltip()

    def on_enter(self):
        pass

    def on_leave(self):
        self.remove_tooltip()
        self._tooltip = None


class ServerLabel(HoverBehavior, MDTooltip, MDBoxLayout):
    tooltip_display_delay = 0.1
    text: str = StringProperty("Server:")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_widget(MDIcon(icon="information", font_size=sp(15)))
        self.add_widget(TooltipLabel(text=self.text, pos_hint={"center_x": 0.5, "center_y": 0.5},
                                     font_size=sp(15)))
        self._tooltip = ServerToolTip(text="Test")

    def on_enter(self):
        self._tooltip.text = self.get_text()
        self.display_tooltip()

    def on_leave(self):
        self.animation_tooltip_dismiss()

    @property
    def ctx(self) -> context_type:
        return MDApp.get_running_app().ctx

    def get_text(self):
        if self.ctx.server:
            ctx = self.ctx
            text = f"Connected to: {ctx.server_address}."
            if ctx.slot is not None:
                text += f"\nYou are Slot Number {ctx.slot} in Team Number {ctx.team}, " \
                        f"named {ctx.player_names[ctx.slot]}."
                if ctx.items_received:
                    text += f"\nYou have received {len(ctx.items_received)} items. " \
                            f"You can list them in order with /received."
                if ctx.total_locations:
                    text += f"\nYou have checked {len(ctx.checked_locations)} " \
                            f"out of {ctx.total_locations} locations. " \
                            f"You can get more info on missing checks with /missing."
                if ctx.permissions:
                    text += "\nPermissions:"
                    for permission_name, permission_data in ctx.permissions.items():
                        text += f"\n    {permission_name}: {permission_data}"
                if ctx.hint_cost is not None and ctx.total_locations:
                    min_cost = int(ctx.server_version >= (0, 3, 9))
                    text += f"\nA new !hint <itemname> costs {ctx.hint_cost}% of checks made. " \
                            f"For you this means every " \
                            f"{max(min_cost, int(ctx.hint_cost * 0.01 * ctx.total_locations))} " \
                            "location checks." \
                            f"\nYou currently have {ctx.hint_points} points."
                elif ctx.hint_cost == 0:
                    text += "\n!hint is free to use."
                if ctx.stored_data and "_read_race_mode" in ctx.stored_data:
                    text += "\nRace mode is enabled." \
                        if ctx.stored_data["_read_race_mode"] else "\nRace mode is disabled."
            else:
                text += f"\nYou are not authenticated yet."

            return text

        else:
            return "No current server connection. \nPlease connect to an Archipelago server."


class MainLayout(MDGridLayout):
    pass


class ContainerLayout(MDFloatLayout):
    pass


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """


class SelectableLabel(RecycleDataViewBehavior, TooltipLabel):
    """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_size(self, instance_label, size: list) -> None:
        super().on_size(instance_label, size)
        if self.parent:
            self.width = self.parent.width

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos):
            if self.selected:
                self.parent.clear_selection()
            else:
                # Not a fan of the following few lines, but they work.
                temp = MarkupLabel(text=self.text).markup
                text = "".join(part for part in temp if not part.startswith("["))
                cmdinput = MDApp.get_running_app().textinput
                if not cmdinput.text:
                    input_text = get_input_text_from_response(text, MDApp.get_running_app().last_autofillable_command)
                    if input_text is not None:
                        cmdinput.text = input_text

                Clipboard.copy(text.replace("&amp;", "&").replace("&bl;", "[").replace("&br;", "]"))
                return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected


class MarkupDropdownTextItem(MDDropdownTextItem):
    def __init__(self):
        super().__init__()
        for child in self.children:
            if child.__class__ == MDLabel:
                child.markup = True
    # Currently, this only lets us do markup on text that does not have any icons
    # Create new TextItems as needed


class MarkupDropdown(MDDropdownMenu):
    def on_items(self, instance, value: list) -> None:
        """
        The method sets the class that will be used to create the menu item.
        """

        items = []
        viewclass = "MarkupDropdownTextItem"

        for data in value:
            if "viewclass" not in data:
                if (
                    "leading_icon" not in data
                    and "trailing_icon" not in data
                    and "trailing_text" not in data
                ):
                    viewclass = "MarkupDropdownTextItem"
                elif (
                    "leading_icon" in data
                    and "trailing_icon" not in data
                    and "trailing_text" not in data
                ):
                    viewclass = "MDDropdownLeadingIconItem"
                elif (
                    "leading_icon" not in data
                    and "trailing_icon" in data
                    and "trailing_text" not in data
                ):
                    viewclass = "MDDropdownTrailingIconItem"
                elif (
                    "leading_icon" not in data
                    and "trailing_icon" in data
                    and "trailing_text" in data
                ):
                    viewclass = "MDDropdownTrailingIconTextItem"
                elif (
                    "leading_icon" in data
                    and "trailing_icon" in data
                    and "trailing_text" in data
                ):
                    viewclass = "MDDropdownLeadingTrailingIconTextItem"
                elif (
                    "leading_icon" in data
                    and "trailing_icon" in data
                    and "trailing_text" not in data
                ):
                    viewclass = "MDDropdownLeadingTrailingIconItem"
                elif (
                    "leading_icon" not in data
                    and "trailing_icon" not in data
                    and "trailing_text" in data
                ):
                    viewclass = "MDDropdownTrailingTextItem"
                elif (
                    "leading_icon" in data
                    and "trailing_icon" not in data
                    and "trailing_text" in data
                ):
                    viewclass = "MDDropdownLeadingIconTrailingTextItem"

                data["viewclass"] = viewclass

            if "height" not in data:
                data["height"] = dp(48)

            items.append(data)

        self._items = items
        # Update items in view
        if hasattr(self, "menu"):
            self.menu.data = self._items


class AutocompleteHintInput(ResizableTextField):
    min_chars = NumericProperty(3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dropdown = MarkupDropdown(caller=self, position="bottom", border_margin=dp(2), width=self.width)
        self.bind(on_text_validate=self.on_message)
        self.bind(width=lambda instance, x: setattr(self.dropdown, "width", x))

    def on_message(self, instance):
        MDApp.get_running_app().commandprocessor("!hint "+instance.text)

    def on_text(self, instance, value):
        if len(value) >= self.min_chars:
            self.dropdown.items.clear()
            ctx: context_type = MDApp.get_running_app().ctx
            if not ctx.game:
                return
            item_names = ctx.item_names._game_store[ctx.game].values()

            def on_press(text):
                split_text = MarkupLabel(text=text).markup
                self.set_text(self, "".join(text_frag for text_frag in split_text
                                            if not text_frag.startswith("[")))
                self.dropdown.dismiss()
                self.focus = True

            lowered = value.lower()
            for item_name in item_names:
                try:
                    index = item_name.lower().index(lowered)
                except ValueError:
                    pass  # substring not found
                else:
                    text = escape_markup(item_name)
                    text = text[:index] + "[b]" + text[index:index+len(value)]+"[/b]"+text[index+len(value):]
                    self.dropdown.items.append({
                        "text": text,
                        "on_release": lambda txt=text: on_press(txt),
                        "markup": True
                    })
            if not self.dropdown.parent:
                self.dropdown.open()
        else:
            self.dropdown.dismiss()


status_icons = {
    HintStatus.HINT_NO_PRIORITY: "information",
    HintStatus.HINT_PRIORITY: "exclamation-thick",
    HintStatus.HINT_AVOID: "alert"
}


class HintLabel(RecycleDataViewBehavior, MDBoxLayout):
    selected = BooleanProperty(False)
    striped = BooleanProperty(False)
    index = None
    dropdown: MDDropdownMenu

    def __init__(self):
        super(HintLabel, self).__init__()
        self.receiving_text = ""
        self.item_text = ""
        self.finding_text = ""
        self.location_text = ""
        self.entrance_text = ""
        self.status_text = ""
        self.hint = {}

        ctx = MDApp.get_running_app().ctx
        menu_items = []

        for status in (HintStatus.HINT_NO_PRIORITY, HintStatus.HINT_PRIORITY, HintStatus.HINT_AVOID):
            name = status_names[status]
            status_button = MDDropDownItem(MDDropDownItemText(text=name), size_hint_y=None, height=dp(50))
            status_button.status = status
            menu_items.append({
                "text": name,
                "leading_icon": status_icons[status],
                "on_release": lambda x=status: select(self, x)
            })

        self.dropdown = MDDropdownMenu(caller=self.ids["status"], items=menu_items)

        def select(instance, data):
            ctx.update_hint(self.hint["location"],
                            self.hint["finding_player"],
                            data)

        self.dropdown.bind(on_release=self.dropdown.dismiss)

    def set_height(self, instance, value):
        self.height = max([child.texture_size[1] for child in self.children])

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.striped = data.get("striped", False)
        self.receiving_text = data["receiving"]["text"]
        self.item_text = data["item"]["text"]
        self.finding_text = data["finding"]["text"]
        self.location_text = data["location"]["text"]
        self.entrance_text = data["entrance"]["text"]
        self.status_text = data["status"]["text"]
        self.hint = data["status"]["hint"]
        return super(HintLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(HintLabel, self).on_touch_down(touch):
            return True
        if self.index:  # skip header
            if self.collide_point(*touch.pos):
                status_label = self.ids["status"]
                if status_label.collide_point(*touch.pos):
                    if self.hint["status"] == HintStatus.HINT_FOUND:
                        return
                    ctx = MDApp.get_running_app().ctx
                    if ctx.slot_concerns_self(self.hint["receiving_player"]):  # If this player owns this hint
                        # open a dropdown
                        self.dropdown.open()
                elif self.selected:
                    self.parent.clear_selection()
                else:
                    text = "".join((self.receiving_text, "\'s ", self.item_text, " is at ", self.location_text, " in ",
                                    self.finding_text, "\'s World", (" at " + self.entrance_text)
                                    if self.entrance_text != "Vanilla"
                                    else "", ". (", self.status_text.lower(), ")"))
                    temp = MarkupLabel(text).markup
                    text = "".join(part for part in temp if not part.startswith("["))
                    Clipboard.copy(escape_markup(text).replace("&amp;", "&").replace("&bl;", "[").replace("&br;", "]"))
                    return self.parent.select_with_touch(self.index, touch)
        else:
            parent = self.parent
            parent.clear_selection()
            parent: HintLog = parent.parent
            # find correct column
            for child in self.children:
                if child.collide_point(*touch.pos):
                    key = child.sort_key
                    if key == "status":
                        parent.hint_sorter = lambda element: status_sort_weights[element["status"]["hint"]["status"]]
                    else:
                        parent.hint_sorter = lambda element: (
                            remove_between_brackets.sub("", element[key]["text"]).lower()
                        )
                    if key == parent.sort_key:
                        # second click reverses order
                        parent.reversed = not parent.reversed
                    else:
                        parent.sort_key = key
                        parent.reversed = False
                    MDApp.get_running_app().update_hints()

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        if self.index:
            self.selected = is_selected


class ConnectBarTextInput(ResizableTextField):
    def insert_text(self, substring, from_undo=False):
        s = substring.replace("\n", "").replace("\r", "")
        return super(ConnectBarTextInput, self).insert_text(s, from_undo=from_undo)


def is_command_input(string: str) -> bool:
    return len(string) > 0 and string[0] in "/!"


class CommandPromptTextInput(ResizableTextField):
    MAXIMUM_HISTORY_MESSAGES = 50

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._command_history_index = -1
        self._command_history: typing.Deque[str] = deque(maxlen=CommandPromptTextInput.MAXIMUM_HISTORY_MESSAGES)

    def update_history(self, new_entry: str) -> None:
        self._command_history_index = -1
        if is_command_input(new_entry):
            self._command_history.appendleft(new_entry)

    def keyboard_on_key_down(
        self,
        window,
        keycode: typing.Tuple[int, str],
        text: typing.Optional[str],
        modifiers: typing.List[str]
    ) -> bool:
        """
        :param window: The kivy window object
        :param keycode: A tuple of (keycode, keyname). Keynames are always lowercase
        :param text: The text printed by this key, not accounting for modifiers, or `None` if no text.
                     Seems to pretty naively interpret the keycode as unicode, so numlock can return odd characters.
        :param modifiers: A list of string modifiers, like `ctrl` or `numlock`
        """
        if keycode[1] == 'up':
            self._change_to_history_text_if_available(self._command_history_index + 1)
            return True
        if keycode[1] == 'down':
            self._change_to_history_text_if_available(self._command_history_index - 1)
            return True
        return super().keyboard_on_key_down(window, keycode, text, modifiers)

    def _change_to_history_text_if_available(self, new_index: int) -> None:
        if new_index < -1:
            return
        if new_index >= len(self._command_history):
            return
        self._command_history_index = new_index
        if new_index == -1:
            self.text = ""
            return
        self.text = self._command_history[self._command_history_index]


class MessageBoxLabel(MDLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._label.refresh()


class MessageBox(Popup):
    def __init__(self, title, text, error=False, **kwargs):
        label = MessageBoxLabel(text=text, padding=("6dp", "0dp"))
        separator_color = [217 / 255, 129 / 255, 122 / 255, 1.] if error else [47 / 255., 167 / 255., 212 / 255, 1.]
        super().__init__(title=title, content=label, size_hint=(0.5, None), width=max(100, int(label.width) + 40),
                         separator_color=separator_color, **kwargs)


class MDNavigationItemBase(MDNavigationItem):
    text = StringProperty(None)


class ButtonsPrompt(MDDialog):
    def __init__(self, title: str, text: str, response: typing.Callable[[str], None],
                 *prompts: str, **kwargs) -> None:
        """
        Customizable popup box that lets you create any number of buttons. The text of the pressed button is returned to
        the callback.

        :param title: The title of the popup.
        :param text: The message prompt in the popup.
        :param response: A callable that will get called when the user presses a button. The prompt will not close
         itself so should be done here if you want to close it when certain buttons are pressed.
        :param prompts: Any number of strings to be used for the buttons.
        """
        layout = MDBoxLayout(orientation="vertical")
        label = MessageBoxLabel(text=text)
        layout.add_widget(label)

        def on_release(button: MDButton, *args) -> None:
            response(button.text)

        buttons = [MDDivider()]
        for prompt in prompts:
            button = MDButton(
                MDButtonText(text=prompt, pos_hint={"center_x": 0.5, "center_y": 0.5}),
                on_release=on_release,
                style="text",
                theme_width="Custom",
                size_hint_x=1,
            )
            button.text = prompt
            buttons.extend([button, MDDivider()])

        super().__init__(
            MDDialogHeadlineText(text=title),
            MDDialogSupportingText(text=text),
            MDDialogButtonContainer(*buttons, orientation="vertical"),
            **kwargs,
        )


class MDScreenManagerBase(MDScreenManager):
    current_tab: MDNavigationItemBase
    local_screen_names: list[str]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.local_screen_names = []

    def add_widget(self, widget: Widget, *args, **kwargs) -> None:
        super().add_widget(widget, *args, **kwargs)
        if "index" in kwargs:
            self.local_screen_names.insert(kwargs["index"], widget.name)
        else:
            self.local_screen_names.append(widget.name)

    def switch_screens(self, new_tab: MDNavigationItemBase) -> None:
        """
        Called whenever the user clicks a tab to switch to a different screen.

        :param new_tab: The new screen to switch to's tab.
        """
        name = new_tab.text
        if self.local_screen_names.index(name) > self.local_screen_names.index(self.current_screen.name):
            self.transition.direction = "left"
        else:
            self.transition.direction = "right"
        self.current = name
        self.current_tab = new_tab


class CommandButton(MDButton, MDTooltip):
    def __init__(self, *args, manager: "GameManager", **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self._tooltip = ToolTip(text="Test")

    def on_enter(self):
        self._tooltip.text = self.manager.commandprocessor.get_help_text()
        self._tooltip.font_size = dp(20 - (len(self._tooltip.text) // 400))  # mostly guessing on the numbers here
        self.display_tooltip()

    def on_leave(self):
        self.animation_tooltip_dismiss()


class GameManager(ThemedApp):
    logging_pairs = [
        ("Client", "Archipelago"),
    ]
    base_title: str = "Archipelago Client"
    last_autofillable_command: str

    main_area_container: MDGridLayout
    """ subclasses can add more columns beside the tabs """

    tabs: MDNavigationBar
    screens: MDScreenManagerBase

    def __init__(self, ctx: context_type):
        self.title = self.base_title
        self.ctx = ctx
        self.commandprocessor = ctx.command_processor(ctx)
        self.icon = r"data/icon.png"
        self.json_to_kivy_parser = KivyJSONtoTextParser(ctx)
        self.log_panels: typing.Dict[str, Widget] = {}

        # keep track of last used command to autofill on click
        self.last_autofillable_command = "!hint"
        autofillable_commands = ("!hint_location", "!hint", "!getitem")
        original_say = ctx.on_user_say

        def intercept_say(text):
            text = original_say(text)
            if text:
                for command in autofillable_commands:
                    if text.startswith(command):
                        self.last_autofillable_command = command
                        break
            return text

        ctx.on_user_say = intercept_say

        super(GameManager, self).__init__()

    @property
    def tab_count(self):
        if hasattr(self, "tabs"):
            return max(1, len(self.tabs.children))
        return 1

    def on_start(self):
        def on_start(*args):
            self.root.md_bg_color = self.theme_cls.backgroundColor
        super().on_start()
        Clock.schedule_once(on_start)

    def build(self) -> Layout:
        self.set_colors()
        self.container = ContainerLayout()

        self.grid = MainLayout()
        self.grid.cols = 1
        self.connect_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(40),
                                          spacing=5, padding=(5, 10))
        # top part
        server_label = ServerLabel(width=dp(75))
        self.connect_layout.add_widget(server_label)
        self.server_connect_bar = ConnectBarTextInput(text=self.ctx.suggested_address or "archipelago.gg:",
                                                      pos_hint={"center_x": 0.5, "center_y": 0.5})

        def connect_bar_validate(sender):
            if not self.ctx.server:
                self.connect_button_action(sender)

        self.server_connect_bar.height = dp(30)
        self.server_connect_bar.bind(on_text_validate=connect_bar_validate)
        self.connect_layout.add_widget(self.server_connect_bar)
        self.server_connect_button = MDButton(MDButtonText(text="Connect"), style="filled", size=(dp(100), dp(70)),
                                              size_hint_x=None, size_hint_y=None, radius=5, pos_hint={"center_y": 0.55})
        self.server_connect_button.bind(on_press=self.connect_button_action)
        self.server_connect_button.height = self.server_connect_bar.height
        self.connect_layout.add_widget(self.server_connect_button)
        self.grid.add_widget(self.connect_layout)
        self.progressbar = MDLinearProgressIndicator(size_hint_y=None, height=3)
        self.grid.add_widget(self.progressbar)

        # middle part
        self.screens = MDScreenManagerBase(pos_hint={"center_x": 0.5})
        self.tabs = MDNavigationBar(orientation="horizontal", size_hint_y=None, height=dp(40), set_bars_color=True)
        # bind the method to the bar for back compatibility
        self.tabs.remove_tab = self.remove_client_tab
        self.screens.current_tab = self.add_client_tab(
            "All" if len(self.logging_pairs) > 1 else "Archipelago",
            UILog(*(logging.getLogger(logger_name) for logger_name, name in self.logging_pairs)),
        )
        self.log_panels["All"] = self.screens.current_tab.content
        self.screens.current_tab.active = True

        for logger_name, display_name in self.logging_pairs:
            bridge_logger = logging.getLogger(logger_name)
            self.log_panels[display_name] = UILog(bridge_logger)
            if len(self.logging_pairs) > 1:
                self.add_client_tab(display_name, self.log_panels[display_name])

        self.hint_log = HintLog(self.json_to_kivy_parser)
        hint_panel = self.add_client_tab("Hints", HintLayout(self.hint_log))
        self.log_panels["Hints"] = hint_panel.content

        self.main_area_container = MDGridLayout(size_hint_y=1, rows=1)
        tab_container = MDGridLayout(size_hint_y=1, cols=1)
        tab_container.add_widget(self.tabs)
        tab_container.add_widget(self.screens)
        self.main_area_container.add_widget(tab_container)

        self.grid.add_widget(self.main_area_container)

        # bottom part
        bottom_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(40), spacing=5, padding=(5, 10))
        info_button = CommandButton(MDButtonText(text="Command:", halign="left"), manager=self, radius=5,
                                    style="filled", size=(dp(100), dp(70)), size_hint_x=None, size_hint_y=None,
                                    pos_hint={"center_y": 0.575})
        info_button.bind(on_release=self.command_button_action)
        bottom_layout.add_widget(info_button)
        self.textinput = CommandPromptTextInput(size_hint_y=None, multiline=False, write_tab=False)
        self.textinput.bind(on_text_validate=self.on_message)
        info_button.height = self.textinput.height
        self.textinput.text_validate_unfocus = False
        bottom_layout.add_widget(self.textinput)
        self.grid.add_widget(bottom_layout)
        self.commandprocessor("/help")
        Clock.schedule_interval(self.update_texts, 1 / 30)
        self.container.add_widget(self.grid)

        # If the address contains a port, select it; otherwise, select the host.
        s = self.server_connect_bar.text
        host_start = s.find("@") + 1
        ipv6_end = s.find("]", host_start) + 1
        port_start = s.find(":", ipv6_end if ipv6_end > 0 else host_start) + 1
        self.server_connect_bar.focus = True
        self.server_connect_bar.select_text(port_start if port_start > 0 else host_start, len(s))

        # Uncomment to enable the kivy live editor console
        # Press Ctrl-E (with numlock/capslock) disabled to open
        # from kivy.core.window import Window
        # from kivy.modules import console
        # console.create_console(Window, self.container)

        return self.container

    def add_client_tab(self, title: str, content: Widget, index: int = -1) -> MDNavigationItemBase:
        """
        Adds a new tab to the client window with a given title, and provides a given Widget as its content.
        Returns the new tab widget, with the provided content being placed on the tab as content.

        :param title: The title of the tab.
        :param content: The Widget to be added as content for this tab's new MDScreen. Will also be added to the
         returned tab as tab.content.
        :param index: The index to insert the tab at. Defaults to -1, meaning the tab will be appended to the end.

        :return: The new tab.
        """
        if self.tabs.children:
            self.tabs.add_widget(MDDivider(orientation="vertical"))
        new_tab = MDNavigationItemBase(text=title)
        new_tab.content = content
        new_screen = MDScreen(name=title)
        new_screen.add_widget(content)
        if -1 < index <= len(self.tabs.children):
            remapped_index = len(self.tabs.children) - index
            self.tabs.add_widget(new_tab, index=remapped_index)
            self.screens.add_widget(new_screen, index=index)
        else:
            self.tabs.add_widget(new_tab)
            self.screens.add_widget(new_screen)
        return new_tab

    def remove_client_tab(self, tab: MDNavigationItemBase) -> None:
        """
        Called to remove a tab and its screen.

        :param tab: The tab to remove.
        """
        tab_index = self.tabs.children.index(tab)
        # if the tab is currently active we need to swap before removing it
        if tab == self.screens.current_tab:
            if not tab_index:
                # account for the divider
                swap_index = tab_index + 2
            else:
                swap_index = tab_index - 2
            self.tabs.children[swap_index].on_release()
            # self.screens.switch_screens(self.tabs.children[swap_index])
        # get the divider to the left if we can
        if not tab_index:
            divider_index = tab_index + 1
        else:
            divider_index = tab_index - 1
        self.tabs.remove_widget(self.tabs.children[divider_index])
        self.tabs.remove_widget(tab)
        self.screens.remove_widget(self.screens.get_screen(tab.text))

    def update_texts(self, dt):
        if hasattr(self.screens.current_tab.content, "fix_heights"):
            getattr(self.screens.current_tab.content, "fix_heights")()
        if self.ctx.server:
            self.title = self.base_title + " " + Utils.__version__ + \
                         f" | Connected to: {self.ctx.server_address} " \
                         f"{'.'.join(str(e) for e in self.ctx.server_version)}"
            self.server_connect_button._button_text.text = "Disconnect"
            self.server_connect_bar.readonly = True
            self.progressbar.max = len(self.ctx.checked_locations) + len(self.ctx.missing_locations)
            self.progressbar.value = len(self.ctx.checked_locations)
        else:
            self.server_connect_button._button_text.text = "Connect"
            self.server_connect_bar.readonly = False
            self.title = self.base_title + " " + Utils.__version__
            self.progressbar.value = 0

    def command_button_action(self, button):
        if self.ctx.server:
            logging.getLogger("Client").info("/help for client commands and !help for server commands.")
        else:
            logging.getLogger("Client").info("/help for client commands and once you are connected, "
                                             "!help for server commands.")

    def connect_button_action(self, button):
        self.ctx.username = None
        self.ctx.password = None
        if self.ctx.server:
            async_start(self.ctx.disconnect())
        else:
            async_start(self.ctx.connect(self.server_connect_bar.text.replace("/connect ", "")))

    def on_stop(self):
        # "kill" input tasks
        for x in range(self.ctx.input_requests):
            self.ctx.input_queue.put_nowait("")
        self.ctx.input_requests = 0

        self.ctx.exit_event.set()

    def on_message(self, textinput: CommandPromptTextInput):
        try:
            input_text = textinput.text.strip()
            textinput.text = ""
            textinput.update_history(input_text)

            if self.ctx.input_requests > 0:
                self.ctx.input_requests -= 1
                self.ctx.input_queue.put_nowait(input_text)
            elif is_command_input(input_text):
                self.ctx.on_ui_command(input_text)
                self.commandprocessor(input_text)
            elif input_text:
                self.commandprocessor(input_text)

        except Exception as e:
            logging.getLogger("Client").exception(e)

    def print_json(self, data: typing.List[JSONMessagePart]):
        text = self.json_to_kivy_parser(data)
        self.log_panels["Archipelago"].on_message_markup(text)
        self.log_panels["All"].on_message_markup(text)

    def focus_textinput(self):
        if hasattr(self, "textinput"):
            self.textinput.focus = True

    def update_address_bar(self, text: str):
        if hasattr(self, "server_connect_bar"):
            self.server_connect_bar.text = text
        else:
            logging.getLogger("Client").info("Could not update address bar as the GUI is not yet initialized.")

    def enable_energy_link(self):
        if not hasattr(self, "energy_link_label"):
            self.energy_link_label = MDLabel(text="Energy Link: Standby",
                                           size_hint_x=None, width=150, halign="center")
            self.connect_layout.add_widget(self.energy_link_label)

    def set_new_energy_link_value(self):
        if hasattr(self, "energy_link_label"):
            self.energy_link_label.text = f"EL: {Utils.format_SI_prefix(self.ctx.current_energy_link_value)}J"

    def update_hints(self):
        hints = self.ctx.stored_data.get(f"_read_hints_{self.ctx.team}_{self.ctx.slot}", [])
        self.hint_log.refresh_hints(hints)


class LogtoUI(logging.Handler):
    def __init__(self, on_log):
        super(LogtoUI, self).__init__(logging.INFO)
        self.on_log = on_log

    @staticmethod
    def format_compact(record: logging.LogRecord) -> str:
        if isinstance(record.msg, Exception):
            return str(record.msg)
        return (f"{record.exc_info[1]}\n" if record.exc_info else "") + str(record.msg).split("\n")[0]

    def handle(self, record: logging.LogRecord) -> None:
        if getattr(record, "skip_gui", False):
            pass  # skip output
        elif getattr(record, "compact_gui", False):
            self.on_log(self.format_compact(record))
        else:
            self.on_log(self.format(record))


class UILog(MDRecycleView):
    messages: typing.ClassVar[int]  # comes from kv file
    adaptive_height = True

    def __init__(self, *loggers_to_handle, **kwargs):
        super(UILog, self).__init__(**kwargs)
        self.data = []
        for logger in loggers_to_handle:
            logger.addHandler(LogtoUI(self.on_log))

    def on_log(self, record: str) -> None:
        self.data.append({"text": escape_markup(record)})
        self.clean_old()

    def on_message_markup(self, text):
        self.data.append({"text": text})
        self.clean_old()

    def clean_old(self):
        if len(self.data) > self.messages:
            self.data.pop(0)

    def fix_heights(self):
        """Workaround fix for divergent texture and layout heights"""
        for element in self.children[0].children:
            if element.height != element.texture_size[1]:
                element.height = element.texture_size[1]


class HintLayout(MDBoxLayout):
    orientation = "vertical"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        boxlayout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(40))
        boxlayout.add_widget(MDLabel(text="New Hint:", size_hint_x=None, size_hint_y=None,
                                     height=dp(40), width=dp(75), halign="center", valign="center"))
        boxlayout.add_widget(AutocompleteHintInput())
        self.add_widget(boxlayout)

    def fix_heights(self):
        for child in self.children:
            fix_func = getattr(child, "fix_heights", None)
            if fix_func:
                fix_func()


status_names: typing.Dict[HintStatus, str] = {
    HintStatus.HINT_FOUND: "Found",
    HintStatus.HINT_UNSPECIFIED: "Unspecified",
    HintStatus.HINT_NO_PRIORITY: "No Priority",
    HintStatus.HINT_AVOID: "Avoid",
    HintStatus.HINT_PRIORITY: "Priority",
}
status_colors: typing.Dict[HintStatus, str] = {
    HintStatus.HINT_FOUND: "green",
    HintStatus.HINT_UNSPECIFIED: "white",
    HintStatus.HINT_NO_PRIORITY: "cyan",
    HintStatus.HINT_AVOID: "salmon",
    HintStatus.HINT_PRIORITY: "plum",
}
status_sort_weights: dict[HintStatus, int] = {
    HintStatus.HINT_FOUND: 0,
    HintStatus.HINT_UNSPECIFIED: 1,
    HintStatus.HINT_NO_PRIORITY: 2,
    HintStatus.HINT_AVOID: 3,
    HintStatus.HINT_PRIORITY: 4,
}

class HintLog(MDRecycleView):
    header = {
        "receiving": {"text": "[u]Receiving Player[/u]"},
        "item": {"text": "[u]Item[/u]"},
        "finding": {"text": "[u]Finding Player[/u]"},
        "location": {"text": "[u]Location[/u]"},
        "entrance": {"text": "[u]Entrance[/u]"},
        "status": {"text": "[u]Status[/u]",
                   "hint": {"receiving_player": -1, "location": -1, "finding_player": -1, "status": ""}},
        "striped": True,
    }
    data: list[typing.Any]
    sort_key: str = ""
    reversed: bool = True

    def __init__(self, parser):
        super(HintLog, self).__init__()
        self.data = [self.header]
        self.parser = parser

    def refresh_hints(self, hints):
        if not hints:  # Fix the scrolling looking visually wrong in some edge cases
            self.scroll_y = 1.0
        data = []
        ctx = MDApp.get_running_app().ctx
        for hint in hints:
            if not hint.get("status"): # Allows connecting to old servers
                hint["status"] = HintStatus.HINT_FOUND if hint["found"] else HintStatus.HINT_UNSPECIFIED
            hint_status_node = self.parser.handle_node({"type": "color",
                                                        "color": status_colors.get(hint["status"], "red"),
                                                        "text": status_names.get(hint["status"], "Unknown")})
            if hint["status"] != HintStatus.HINT_FOUND and ctx.slot_concerns_self(hint["receiving_player"]):
                hint_status_node = f"[u]{hint_status_node}[/u]"
            data.append({
                "receiving": {"text": self.parser.handle_node({"type": "player_id", "text": hint["receiving_player"]})},
                "item": {"text": self.parser.handle_node({
                    "type": "item_id",
                    "text": hint["item"],
                    "flags": hint["item_flags"],
                    "player": hint["receiving_player"],
                })},
                "finding": {"text": self.parser.handle_node({"type": "player_id", "text": hint["finding_player"]})},
                "location": {"text": self.parser.handle_node({
                    "type": "location_id",
                    "text": hint["location"],
                    "player": hint["finding_player"],
                })},
                "entrance": {"text": self.parser.handle_node({"type": "color" if hint["entrance"] else "text",
                                                              "color": "blue", "text": hint["entrance"]
                                                              if hint["entrance"] else "Vanilla"})},
                "status": {
                    "text": hint_status_node,
                    "hint": hint,
                },
            })

        data.sort(key=self.hint_sorter, reverse=self.reversed)
        for i in range(0, len(data), 2):
            data[i]["striped"] = True
        data.insert(0, self.header)
        self.data = data

    @staticmethod
    def hint_sorter(element: dict) -> str:
        return element["status"]["hint"]["status"]  # By status by default

    def fix_heights(self):
        """Workaround fix for divergent texture and layout heights"""
        for element in self.children[0].children:
            max_height = max(child.texture_size[1] for child in element.children)
            element.height = max_height


class ApAsyncImage(AsyncImage):

    def is_uri(self, filename: str) -> bool:
        if filename.startswith("ap:"):
            return True
        else:
            return super().is_uri(filename)


class ImageLoaderPkgutil(ImageLoaderBase):
    def load(self, filename: str) -> typing.List[ImageData]:
        # take off the "ap:" prefix
        module, path = filename[3:].split("/", 1)
        data = pkgutil.get_data(module, path)
        return self._bytes_to_data(data)

    @staticmethod
    def _bytes_to_data(data: typing.Union[bytes, bytearray]) -> typing.List[ImageData]:
        loader = next(loader for loader in ImageLoader.loaders if loader.can_load_memory())
        return loader.load(loader, io.BytesIO(data))


# grab the default loader method so we can override it but use it as a fallback
_original_image_loader_load = ImageLoader.load


def load_override(filename: str, default_load=_original_image_loader_load, **kwargs):
    if filename.startswith("ap:"):
        return ImageLoaderPkgutil(filename)
    else:
        return default_load(filename, **kwargs)


ImageLoader.load = load_override


class E(ExceptionHandler):
    logger = logging.getLogger("Client")

    def handle_exception(self, inst):
        self.logger.exception("Uncaught Exception:", exc_info=inst)
        return ExceptionManager.PASS


class KivyJSONtoTextParser(JSONtoTextParser):
    # dummy class to absorb kvlang definitions
    class TextColors(Widget):
        white: str = StringProperty("FFFFFF")
        black: str = StringProperty("000000")
        red: str = StringProperty("EE0000")
        green: str = StringProperty("00FF7F")
        yellow: str = StringProperty("FAFAD2")
        blue: str = StringProperty("6495ED")
        magenta: str = StringProperty("EE00EE")
        cyan: str = StringProperty("00EEEE")
        slateblue: str = StringProperty("6D8BE8")
        plum: str = StringProperty("AF99EF")
        salmon: str = StringProperty("FA8072")
        orange: str = StringProperty("FF7700")
        # KivyMD parameters
        theme_style: str = StringProperty("Dark")
        primary_palette: str = StringProperty("Lightsteelblue")
        dynamic_scheme_name: str = StringProperty("VIBRANT")
        dynamic_scheme_contrast: int = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        # we grab the color definitions from the .kv file, then overwrite the JSONtoTextParser default entries
        colors = self.TextColors()
        color_codes = self.color_codes.copy()
        for name, code in color_codes.items():
            color_codes[name] = getattr(colors, name, code)
        self.color_codes = color_codes
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        self.ref_count = 0
        return super(KivyJSONtoTextParser, self).__call__(*args, **kwargs)

    def _handle_item_name(self, node: JSONMessagePart):
        flags = node.get("flags", 0)
        item_types = []
        if flags & 0b001:  # advancement
            item_types.append("progression")
        if flags & 0b010:  # useful
            item_types.append("useful")
        if flags & 0b100:  # trap
            item_types.append("trap")
        if not item_types:
            item_types.append("normal")

        node.setdefault("refs", []).append("Item Class: " + ", ".join(item_types))
        return super(KivyJSONtoTextParser, self)._handle_item_name(node)

    def _handle_player_id(self, node: JSONMessagePart):
        player = int(node["text"])
        slot_info = self.ctx.slot_info.get(player, None)
        if slot_info:
            text = f"Game: {slot_info.game}<br>" \
                   f"Type: {SlotType(slot_info.type).name}"
            if slot_info.group_members:
                text += f"<br>Members:<br> " + "<br> ".join(
                    escape_markup(self.ctx.player_names[player])
                    for player in slot_info.group_members
                )
            node.setdefault("refs", []).append(text)
        return super(KivyJSONtoTextParser, self)._handle_player_id(node)

    def _handle_color(self, node: JSONMessagePart):
        colors = node["color"].split(";")
        node["text"] = escape_markup(node["text"])
        for color in colors:
            color_code = self.color_codes.get(color, None)
            if color_code:
                node["text"] = f"[color={color_code}]{node['text']}[/color]"
                return self._handle_text(node)
        return self._handle_text(node)

    def _handle_text(self, node: JSONMessagePart):
        # All other text goes through _handle_color, and we don't want to escape markup twice,
        # or mess up text that already has intentional markup applied to it
        if node.get("type", "text") == "text":
            node["text"] = escape_markup(node["text"])
        for ref in node.get("refs", []):
            node["text"] = f"[ref={self.ref_count}|{ref}]{node['text']}[/ref]"
            self.ref_count += 1
        return super(KivyJSONtoTextParser, self)._handle_text(node)


ExceptionManager.add_handler(E())

Builder.load_file(Utils.local_path("data", "client.kv"))
user_file = Utils.user_path("data", "user.kv")
if os.path.exists(user_file):
    logging.info("Loading user.kv into builder.")
    Builder.load_file(user_file)
