import os
import logging
import sys
import typing

if sys.platform == "win32":
    import ctypes

    # kivy 2.2.0 introduced DPI awareness on Windows, but it makes the UI enter an infinitely recursive re-layout
    # by setting the application to not DPI Aware, Windows handles scaling the entire window on its own, ignoring kivy's
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(0)
    except FileNotFoundError:  # shcore may not be found on <= Windows 7
        pass  # TODO: remove silent except when Python 3.8 is phased out.

os.environ["KIVY_NO_CONSOLELOG"] = "1"
os.environ["KIVY_NO_FILELOG"] = "1"
os.environ["KIVY_NO_ARGS"] = "1"
os.environ["KIVY_LOG_ENABLE"] = "0"

import Utils

if Utils.is_frozen():
    os.environ["KIVY_DATA_DIR"] = Utils.local_path("data")

from kivy.config import Config

Config.set("input", "mouse", "mouse,disable_multitouch")
Config.set("kivy", "exit_on_escape", "0")
Config.set("graphics", "multisamples", "0")  # multisamples crash old intel drivers

from kivy.app import App
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.core.text.markup import MarkupLabel
from kivy.base import ExceptionHandler, ExceptionManager
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.layout import Layout
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.utils import escape_markup
from kivy.lang import Builder
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.animation import Animation
from kivy.uix.popup import Popup

fade_in_animation = Animation(opacity=0, duration=0) + Animation(opacity=1, duration=0.25)

from NetUtils import JSONtoTextParser, JSONMessagePart, SlotType
from Utils import async_start

if typing.TYPE_CHECKING:
    import CommonClient

    context_type = CommonClient.CommonContext
else:
    context_type = object


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
                if not cmdinput.text and " did you mean " in text:
                    for question in ("Didn't find something that closely matches, did you mean ",
                                     "Too many close matches, did you mean "):
                        if text.startswith(question):
                            name = Utils.get_text_between(text, question,
                                                          "? (")
                            cmdinput.text = f"!{App.get_running_app().last_autofillable_command} {name}"
                            break
                elif not cmdinput.text and text.startswith("Missing: "):
                    cmdinput.text = text.replace("Missing: ", "!hint_location ")

                Clipboard.copy(text.replace("&amp;", "&").replace("&bl;", "[").replace("&br;", "]"))
                return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected


class HintLabel(RecycleDataViewBehavior, BoxLayout):
    selected = BooleanProperty(False)
    striped = BooleanProperty(False)
    index = None
    no_select = []

    def __init__(self):
        super(HintLabel, self).__init__()
        self.receiving_text = ""
        self.item_text = ""
        self.finding_text = ""
        self.location_text = ""
        self.entrance_text = ""
        self.found_text = ""
        for child in self.children:
            child.bind(texture_size=self.set_height)

    def set_height(self, instance, value):
        self.height = max([child.texture_size[1] for child in self.children])

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        if "select" in data and not data["select"] and index not in self.no_select:
            self.no_select.append(index)
        self.striped = data["striped"]
        self.receiving_text = data["receiving"]["text"]
        self.item_text = data["item"]["text"]
        self.finding_text = data["finding"]["text"]
        self.location_text = data["location"]["text"]
        self.entrance_text = data["entrance"]["text"]
        self.found_text = data["found"]["text"]
        self.height = self.minimum_height
        return super(HintLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(HintLabel, self).on_touch_down(touch):
            return True
        if self.index not in self.no_select:
            if self.collide_point(*touch.pos):
                if self.selected:
                    self.parent.clear_selection()
                else:
                    text = "".join([self.receiving_text, "\'s ", self.item_text, " is at ", self.location_text, " in ",
                                    self.finding_text, "\'s World", (" at " + self.entrance_text)
                                    if self.entrance_text != "Vanilla"
                                    else "", ". (", self.found_text.lower(), ")"])
                    temp = MarkupLabel(text).markup
                    text = "".join(
                        part for part in temp if not part.startswith(("[color", "[/color]", "[ref=", "[/ref]")))
                    Clipboard.copy(escape_markup(text).replace("&amp;", "&").replace("&bl;", "[").replace("&br;", "]"))
                    return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        if self.index not in self.no_select:
            self.selected = is_selected


class ConnectBarTextInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        s = substring.replace("\n", "").replace("\r", "")
        return super(ConnectBarTextInput, self).insert_text(s, from_undo=from_undo)


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
        self.log_panels = {}

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

        hint_panel = TabbedPanelItem(text="Hints")
        self.log_panels["Hints"] = hint_panel.content = HintLog(self.json_to_kivy_parser)
        self.tabs.add_widget(hint_panel)

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
        self.textinput = TextInput(size_hint_y=None, height=dp(30), multiline=False, write_tab=False)
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
        if self.ctx.server:
            self.ctx.username = None
            async_start(self.ctx.disconnect())
        else:
            async_start(self.ctx.connect(self.server_connect_bar.text.replace("/connect ", "")))

    def on_stop(self):
        # "kill" input tasks
        for x in range(self.ctx.input_requests):
            self.ctx.input_queue.put_nowait("")
        self.ctx.input_requests = 0

        self.ctx.exit_event.set()

    def on_message(self, textinput: TextInput):
        try:
            input_text = textinput.text.strip()
            textinput.text = ""

            if self.ctx.input_requests > 0:
                self.ctx.input_requests -= 1
                self.ctx.input_queue.put_nowait(input_text)
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
        hints = self.ctx.stored_data[f"_read_hints_{self.ctx.team}_{self.ctx.slot}"]
        self.log_panels["Hints"].refresh_hints(hints)

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


class HintLog(RecycleView):
    header = {
        "receiving": {"text": "[u]Receiving Player[/u]"},
        "item": {"text": "[u]Item[/u]"},
        "finding": {"text": "[u]Finding Player[/u]"},
        "location": {"text": "[u]Location[/u]"},
        "entrance": {"text": "[u]Entrance[/u]"},
        "found": {"text": "[u]Status[/u]"},
        "striped": True,
        "select": False,
    }

    def __init__(self, parser):
        super(HintLog, self).__init__()
        self.data = [self.header]
        self.parser = parser

    def refresh_hints(self, hints):
        self.data = [self.header]
        striped = False
        for hint in hints:
            self.data.append({
                "striped": striped,
                "receiving": {"text": self.parser.handle_node({"type": "player_id", "text": hint["receiving_player"]})},
                "item": {"text": self.parser.handle_node(
                    {"type": "item_id", "text": hint["item"], "flags": hint["item_flags"]})},
                "finding": {"text": self.parser.handle_node({"type": "player_id", "text": hint["finding_player"]})},
                "location": {"text": self.parser.handle_node({"type": "location_id", "text": hint["location"]})},
                "entrance": {"text": self.parser.handle_node({"type": "color" if hint["entrance"] else "text",
                                                              "color": "blue", "text": hint["entrance"]
                                                              if hint["entrance"] else "Vanilla"})},
                "found": {
                    "text": self.parser.handle_node({"type": "color", "color": "green" if hint["found"] else "red",
                                                     "text": "Found" if hint["found"] else "Not Found"})},
            })
            striped = not striped


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
        if flags & 0b001:  # advancement
            itemtype = "progression"
        elif flags & 0b010:  # useful
            itemtype = "useful"
        elif flags & 0b100:  # trap
            itemtype = "trap"
        else:
            itemtype = "normal"
        node.setdefault("refs", []).append("Item Class: " + itemtype)
        return super(KivyJSONtoTextParser, self)._handle_item_name(node)

    def _handle_player_id(self, node: JSONMessagePart):
        player = int(node["text"])
        slot_info = self.ctx.slot_info.get(player, None)
        if slot_info:
            text = f"Game: {slot_info.game}<br>" \
                   f"Type: {SlotType(slot_info.type).name}"
            if slot_info.group_members:
                text += f"<br>Members:<br> " + \
                        "<br> ".join(self.ctx.player_names[player] for player in slot_info.group_members)
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
