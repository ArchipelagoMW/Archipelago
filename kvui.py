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

from kivy.app import App
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.core.text.markup import MarkupLabel
from kivy.core.image import ImageLoader, ImageLoaderBase, ImageData
from kivy.base import ExceptionHandler, ExceptionManager
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty
from kivy.metrics import dp
from kivy.effects.scroll import ScrollEffect
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.layout import Layout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.recycleview import RecycleView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.dropdown import DropDown
from kivy.utils import escape_markup
from kivy.lang import Builder
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.image import AsyncImage

fade_in_animation = Animation(opacity=0, duration=0) + Animation(opacity=1, duration=0.25)

from NetUtils import JSONtoTextParser, JSONMessagePart, SlotType, HintStatus
from Utils import async_start, get_input_text_from_response

if typing.TYPE_CHECKING:
    import CommonClient

    context_type = CommonClient.CommonContext
else:
    context_type = object

remove_between_brackets = re.compile(r"\[.*?]")


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


class ToolTip(Label):
    pass


class ServerToolTip(ToolTip):
    pass


class ScrollBox(ScrollView):
    layout: BoxLayout

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = BoxLayout(size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter("height"))
        self.add_widget(self.layout)
        self.effect_cls = ScrollEffect
        self.bar_width = dp(12)
        self.scroll_type = ["content", "bars"]


class HovererableLabel(HoverBehavior, Label):
    pass


class TooltipLabel(HovererableLabel):
    tooltip = None

    def create_tooltip(self, text, x, y):
        text = text.replace("<br>", "\n").replace("&amp;", "&").replace("&bl;", "[").replace("&br;", "]")
        if self.tooltip:
            # update
            self.tooltip.children[0].text = text
        else:
            self.tooltip = FloatLayout()
            tooltip_label = ToolTip(text=text)
            self.tooltip.add_widget(tooltip_label)
            fade_in_animation.start(self.tooltip)
            App.get_running_app().root.add_widget(self.tooltip)

        # handle left-side boundary to not render off-screen
        x = max(x, 3 + self.tooltip.children[0].texture_size[0] / 2)

        # position float layout
        self.tooltip.x = x - self.tooltip.width / 2
        self.tooltip.y = y - self.tooltip.height / 2 + 48

    def remove_tooltip(self):
        if self.tooltip:
            App.get_running_app().root.remove_widget(self.tooltip)
            self.tooltip = None

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


class ServerLabel(HovererableLabel):
    def __init__(self, *args, **kwargs):
        super(HovererableLabel, self).__init__(*args, **kwargs)
        self.layout = FloatLayout()
        self.popuplabel = ServerToolTip(text="Test")
        self.layout.add_widget(self.popuplabel)

    def on_enter(self):
        self.popuplabel.text = self.get_text()
        App.get_running_app().root.add_widget(self.layout)
        fade_in_animation.start(self.layout)

    def on_leave(self):
        App.get_running_app().root.remove_widget(self.layout)

    @property
    def ctx(self) -> context_type:
        return App.get_running_app().ctx

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


class MainLayout(GridLayout):
    pass


class ContainerLayout(FloatLayout):
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
                text = "".join(part for part in temp if not part.startswith(("[color", "[/color]", "[ref=", "[/ref]")))
                cmdinput = App.get_running_app().textinput
                if not cmdinput.text:
                    input_text = get_input_text_from_response(text, App.get_running_app().last_autofillable_command)
                    if input_text is not None:
                        cmdinput.text = input_text

                Clipboard.copy(text.replace("&amp;", "&").replace("&bl;", "[").replace("&br;", "]"))
                return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected

        
class AutocompleteHintInput(TextInput):
    min_chars = NumericProperty(3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dropdown = DropDown()
        self.dropdown.bind(on_select=lambda instance, x: setattr(self, 'text', x))
        self.bind(on_text_validate=self.on_message)

    def on_message(self, instance):
        App.get_running_app().commandprocessor("!hint "+instance.text)

    def on_text(self, instance, value):
        if len(value) >= self.min_chars:
            self.dropdown.clear_widgets()
            ctx: context_type = App.get_running_app().ctx
            if not ctx.game:
                return
            item_names = ctx.item_names._game_store[ctx.game].values()

            def on_press(button: Button):
                split_text = MarkupLabel(text=button.text).markup
                return self.dropdown.select("".join(text_frag for text_frag in split_text
                                                    if not text_frag.startswith("[")))
            lowered = value.lower()
            for item_name in item_names:
                try:
                    index = item_name.lower().index(lowered)
                except ValueError:
                    pass  # substring not found
                else:
                    text = escape_markup(item_name)
                    text = text[:index] + "[b]" + text[index:index+len(value)]+"[/b]"+text[index+len(value):]
                    btn = Button(text=text, size_hint_y=None, height=dp(30), markup=True)
                    btn.bind(on_release=on_press)
                    self.dropdown.add_widget(btn)
            if not self.dropdown.attach_to:
                self.dropdown.open(self)
        else:
            self.dropdown.dismiss()


class HintLabel(RecycleDataViewBehavior, BoxLayout):
    selected = BooleanProperty(False)
    striped = BooleanProperty(False)
    index = None
    dropdown: DropDown

    def __init__(self):
        super(HintLabel, self).__init__()
        self.receiving_text = ""
        self.item_text = ""
        self.finding_text = ""
        self.location_text = ""
        self.entrance_text = ""
        self.status_text = ""
        self.hint = {}
        for child in self.children:
            child.bind(texture_size=self.set_height)


        ctx = App.get_running_app().ctx
        self.dropdown = DropDown()

        def set_value(button):
            self.dropdown.select(button.status)

        def select(instance, data):
            ctx.update_hint(self.hint["location"],
                            self.hint["finding_player"],
                            data)

        for status in (HintStatus.HINT_NO_PRIORITY, HintStatus.HINT_PRIORITY, HintStatus.HINT_AVOID):
            name = status_names[status]
            status_button = Button(text=name, size_hint_y=None, height=dp(50))
            status_button.status = status
            status_button.bind(on_release=set_value)
            self.dropdown.add_widget(status_button)

        self.dropdown.bind(on_select=select)

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
        self.height = self.minimum_height
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
                    ctx = App.get_running_app().ctx
                    if ctx.slot_concerns_self(self.hint["receiving_player"]):  # If this player owns this hint
                        # open a dropdown
                        self.dropdown.open(self.ids["status"])
                elif self.selected:
                    self.parent.clear_selection()
                else:
                    text = "".join((self.receiving_text, "\'s ", self.item_text, " is at ", self.location_text, " in ",
                                    self.finding_text, "\'s World", (" at " + self.entrance_text)
                                    if self.entrance_text != "Vanilla"
                                    else "", ". (", self.status_text.lower(), ")"))
                    temp = MarkupLabel(text).markup
                    text = "".join(
                        part for part in temp if not part.startswith(("[color", "[/color]", "[ref=", "[/ref]")))
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
                    App.get_running_app().update_hints()

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        if self.index:
            self.selected = is_selected


class ConnectBarTextInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        s = substring.replace("\n", "").replace("\r", "")
        return super(ConnectBarTextInput, self).insert_text(s, from_undo=from_undo)


def is_command_input(string: str) -> bool:
    return len(string) > 0 and string[0] in "/!"


class CommandPromptTextInput(TextInput):
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


class MessageBox(Popup):
    class MessageBoxLabel(Label):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self._label.refresh()
            self.size = self._label.texture.size
            if self.width + 50 > Window.width:
                self.text_size[0] = Window.width - 50
                self._label.refresh()
                self.size = self._label.texture.size

    def __init__(self, title, text, error=False, **kwargs):
        label = MessageBox.MessageBoxLabel(text=text)
        separator_color = [217 / 255, 129 / 255, 122 / 255, 1.] if error else [47 / 255., 167 / 255., 212 / 255, 1.]
        super().__init__(title=title, content=label, size_hint=(None, None), width=max(100, int(label.width) + 40),
                         separator_color=separator_color, **kwargs)
        self.height += max(0, label.height - 18)


class GameManager(App):
    logging_pairs = [
        ("Client", "Archipelago"),
    ]
    base_title: str = "Archipelago Client"
    last_autofillable_command: str

    main_area_container: GridLayout
    """ subclasses can add more columns beside the tabs """

    def __init__(self, ctx: context_type):
        self.title = self.base_title
        self.ctx = ctx
        self.commandprocessor = ctx.command_processor(ctx)
        self.icon = r"data/icon.png"
        self.json_to_kivy_parser = KivyJSONtoTextParser(ctx)
        self.log_panels: typing.Dict[str, Widget] = {}

        # keep track of last used command to autofill on click
        self.last_autofillable_command = "hint"
        autofillable_commands = ("hint_location", "hint", "getitem")
        original_say = ctx.on_user_say

        def intercept_say(text):
            text = original_say(text)
            if text:
                for command in autofillable_commands:
                    if text.startswith("!" + command):
                        self.last_autofillable_command = command
                        break
            return text

        ctx.on_user_say = intercept_say

        super(GameManager, self).__init__()

    @property
    def tab_count(self):
        if hasattr(self, "tabs"):
            return max(1, len(self.tabs.tab_list))
        return 1

    def build(self) -> Layout:
        self.container = ContainerLayout()

        self.grid = MainLayout()
        self.grid.cols = 1
        self.connect_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(30))
        # top part
        server_label = ServerLabel()
        self.connect_layout.add_widget(server_label)
        self.server_connect_bar = ConnectBarTextInput(text=self.ctx.suggested_address or "archipelago.gg:",
                                                      size_hint_y=None,
                                                      height=dp(30), multiline=False, write_tab=False)

        def connect_bar_validate(sender):
            if not self.ctx.server:
                self.connect_button_action(sender)

        self.server_connect_bar.bind(on_text_validate=connect_bar_validate)
        self.connect_layout.add_widget(self.server_connect_bar)
        self.server_connect_button = Button(text="Connect", size=(dp(100), dp(30)), size_hint_y=None, size_hint_x=None)
        self.server_connect_button.bind(on_press=self.connect_button_action)
        self.connect_layout.add_widget(self.server_connect_button)
        self.grid.add_widget(self.connect_layout)
        self.progressbar = ProgressBar(size_hint_y=None, height=3)
        self.grid.add_widget(self.progressbar)

        # middle part
        self.tabs = TabbedPanel(size_hint_y=1)
        self.tabs.default_tab_text = "All"
        self.log_panels["All"] = self.tabs.default_tab_content = UILog(*(logging.getLogger(logger_name)
                                                                         for logger_name, name in
                                                                         self.logging_pairs))

        for logger_name, display_name in self.logging_pairs:
            bridge_logger = logging.getLogger(logger_name)
            panel = TabbedPanelItem(text=display_name)
            self.log_panels[display_name] = panel.content = UILog(bridge_logger)
            if len(self.logging_pairs) > 1:
                # show Archipelago tab if other logging is present
                self.tabs.add_widget(panel)

        hint_panel = self.add_client_tab("Hints", HintLayout())
        self.hint_log = HintLog(self.json_to_kivy_parser)
        self.log_panels["Hints"] = hint_panel.content
        hint_panel.content.add_widget(self.hint_log)

        if len(self.logging_pairs) == 1:
            self.tabs.default_tab_text = "Archipelago"

        self.main_area_container = GridLayout(size_hint_y=1, rows=1)
        self.main_area_container.add_widget(self.tabs)

        self.grid.add_widget(self.main_area_container)

        # bottom part
        bottom_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(30))
        info_button = Button(size=(dp(100), dp(30)), text="Command:", size_hint_x=None)
        info_button.bind(on_release=self.command_button_action)
        bottom_layout.add_widget(info_button)
        self.textinput = CommandPromptTextInput(size_hint_y=None, height=dp(30), multiline=False, write_tab=False)
        self.textinput.bind(on_text_validate=self.on_message)
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

        return self.container

    def add_client_tab(self, title: str, content: Widget) -> Widget:
        """Adds a new tab to the client window with a given title, and provides a given Widget as its content.
         Returns the new tab widget, with the provided content being placed on the tab as content."""
        new_tab = TabbedPanelItem(text=title)
        new_tab.content = content
        self.tabs.add_widget(new_tab)
        return new_tab

    def update_texts(self, dt):
        if hasattr(self.tabs.content.children[0], "fix_heights"):
            self.tabs.content.children[0].fix_heights()  # TODO: remove this when Kivy fixes this upstream
        if self.ctx.server:
            self.title = self.base_title + " " + Utils.__version__ + \
                         f" | Connected to: {self.ctx.server_address} " \
                         f"{'.'.join(str(e) for e in self.ctx.server_version)}"
            self.server_connect_button.text = "Disconnect"
            self.server_connect_bar.readonly = True
            self.progressbar.max = len(self.ctx.checked_locations) + len(self.ctx.missing_locations)
            self.progressbar.value = len(self.ctx.checked_locations)
        else:
            self.server_connect_button.text = "Connect"
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
            self.energy_link_label = Label(text="Energy Link: Standby",
                                           size_hint_x=None, width=150)
            self.connect_layout.add_widget(self.energy_link_label)

    def set_new_energy_link_value(self):
        if hasattr(self, "energy_link_label"):
            self.energy_link_label.text = f"EL: {Utils.format_SI_prefix(self.ctx.current_energy_link_value)}J"

    def update_hints(self):
        hints = self.ctx.stored_data.get(f"_read_hints_{self.ctx.team}_{self.ctx.slot}", [])
        self.hint_log.refresh_hints(hints)

    # default F1 keybind, opens a settings menu, that seems to break the layout engine once closed
    def open_settings(self, *largs):
        pass


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


class UILog(RecycleView):
    messages: typing.ClassVar[int]  # comes from kv file

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


class HintLayout(BoxLayout):
    orientation = "vertical"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        boxlayout = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(30))
        boxlayout.add_widget(Label(text="New Hint:", size_hint_x=None, size_hint_y=None, height=dp(30)))
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


class HintLog(RecycleView):
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
        ctx = App.get_running_app().ctx
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

    def _bytes_to_data(self, data: typing.Union[bytes, bytearray]) -> typing.List[ImageData]:
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
        pass

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
