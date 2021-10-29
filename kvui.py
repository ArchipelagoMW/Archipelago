import os
import logging
import typing
import asyncio

os.environ["KIVY_NO_CONSOLELOG"] = "1"
os.environ["KIVY_NO_FILELOG"] = "1"
os.environ["KIVY_NO_ARGS"] = "1"

from kivy.app import App
from kivy.core.window import Window
from kivy.base import ExceptionHandler, ExceptionManager, Config, Clock
from kivy.factory import Factory
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.utils import escape_markup
from kivy.lang import Builder

import Utils
from NetUtils import JSONtoTextParser, JSONMessagePart

if typing.TYPE_CHECKING:
    import CommonClient

    context_type = CommonClient.CommonContext
else:
    context_type = object


# I was surprised to find this didn't already exist in kivy :(
class HoverBehavior(object):
    """from https://stackoverflow.com/a/605348110"""
    hovered = BooleanProperty(False)
    border_point = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__(**kwargs)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return  # do proceed if I'm not displayed <=> If have no parent
        pos = args[1]
        # Next line to_widget allow to compensate for relative layout
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            return  # We have already done what was needed
        self.border_point = pos
        self.hovered = inside

        if inside:
            self.dispatch("on_enter")
        else:
            self.dispatch("on_leave")


Factory.register('HoverBehavior', HoverBehavior)


class ServerToolTip(Label):
    pass


class ServerLabel(HoverBehavior, Label):
    hover_text = """"""

    def __init__(self, *args, **kwargs):
        super(ServerLabel, self).__init__(*args, **kwargs)
        self.layout = FloatLayout()
        self.popuplabel = ServerToolTip(text="Test")
        self.layout.add_widget(self.popuplabel)

    def on_enter(self):
        self.popuplabel.text = self.get_text()
        App.get_running_app().root.add_widget(self.layout)

    def on_leave(self):
        App.get_running_app().root.remove_widget(self.layout)

    def get_text(self):
        if self.ctx.server:
            ctx = self.ctx
            text = f"Connected to: {ctx.server_address}."
            if ctx.slot is not None:
                text += f"\nYou are Slot Number {ctx.slot} in Team Number {ctx.team}, named {ctx.player_names[ctx.slot]}."
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
                if ctx.hint_cost is not None:
                    text += f"\nA new !hint <itemname> costs {ctx.hint_cost}% of checks made. " \
                            f"For you this means every {max(0, int(ctx.hint_cost * 0.01 * ctx.total_locations))} location checks."
                elif ctx.hint_cost == 0:
                    text += "\n!hint is free to use."

            else:
                text += f"\nYou are not authenticated yet."

            return text

        else:
            return "No current server connection. \nPlease connect to an Archipelago server."

    @property
    def ctx(self) -> context_type:
        return App.get_running_app().ctx


class MainLayout(GridLayout):
    pass


class ContainerLayout(FloatLayout):
    pass


class GameManager(App):
    logging_pairs = [
        ("Client", "Archipelago"),
    ]
    base_title = "Archipelago Client"

    def __init__(self, ctx: context_type):
        self.title = self.base_title
        self.ctx = ctx
        self.commandprocessor = ctx.command_processor(ctx)
        self.icon = r"data/icon.png"
        self.json_to_kivy_parser = KivyJSONtoTextParser(ctx)
        self.log_panels = {}
        super(GameManager, self).__init__()

    def build(self):
        self.container = ContainerLayout()

        self.grid = MainLayout()
        self.grid.cols = 1
        connect_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=30)
        # top part
        server_label = ServerLabel()
        connect_layout.add_widget(server_label)
        self.server_connect_bar = TextInput(text="archipelago.gg", size_hint_y=None, height=30, multiline=False)
        connect_layout.add_widget(self.server_connect_bar)
        self.server_connect_button = Button(text="Connect", size=(100, 30), size_hint_y=None, size_hint_x=None)
        self.server_connect_button.bind(on_press=self.connect_button_action)
        connect_layout.add_widget(self.server_connect_button)
        self.grid.add_widget(connect_layout)
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
            self.tabs.add_widget(panel)

        self.grid.add_widget(self.tabs)

        if len(self.logging_pairs) == 1:
            # Hide Tab selection if only one tab
            self.tabs.clear_tabs()
            self.tabs.do_default_tab = False
            self.tabs.current_tab.height = 0
            self.tabs.tab_height = 0

        # bottom part
        bottom_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=30)
        info_button = Button(height=30, text="Command:", size_hint_x=None)
        info_button.bind(on_release=self.command_button_action)
        bottom_layout.add_widget(info_button)
        textinput = TextInput(size_hint_y=None, height=30, multiline=False)
        textinput.bind(on_text_validate=self.on_message)
        bottom_layout.add_widget(textinput)
        self.grid.add_widget(bottom_layout)
        self.commandprocessor("/help")
        Clock.schedule_interval(self.update_texts, 1 / 30)
        self.container.add_widget(self.grid)
        return self.container

    def update_texts(self, dt):
        if self.ctx.server:
            self.title = self.base_title + f" | Connected to: {self.ctx.server_address}"
            self.server_connect_button.text = "Disconnect"
            self.progressbar.max = len(self.ctx.checked_locations) + len(self.ctx.missing_locations)
            self.progressbar.value = len(self.ctx.checked_locations)
        else:
            self.server_connect_button.text = "Connect"
            self.title = self.base_title
            self.progressbar.value = 0

    def command_button_action(self, button):
        logging.getLogger("Client").info("/help for client commands and !help for server commands.")

    def connect_button_action(self, button):
        if self.ctx.server:
            self.ctx.server_address = None
            asyncio.create_task(self.ctx.disconnect())
        else:
            asyncio.create_task(self.ctx.connect(self.server_connect_bar.text.replace("/connect ", "")))

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

    def print_json(self, data):
        text = self.json_to_kivy_parser(data)
        self.log_panels["Archipelago"].on_message_markup(text)
        self.log_panels["All"].on_message_markup(text)


class FactorioManager(GameManager):
    logging_pairs = [
        ("Client", "Archipelago"),
        ("FactorioServer", "Factorio Server Log"),
        ("FactorioWatcher", "Bridge Data Log"),
    ]
    base_title = "Archipelago Factorio Client"


class LttPManager(GameManager):
    logging_pairs = [
        ("Client", "Archipelago"),
        ("SNES", "SNES"),
    ]
    base_title = "Archipelago LttP Client"


class TextManager(GameManager):
    logging_pairs = [
        ("Client", "Archipelago")
    ]
    base_title = "Archipelago Text Client"


class LogtoUI(logging.Handler):
    def __init__(self, on_log):
        super(LogtoUI, self).__init__(logging.DEBUG)
        self.on_log = on_log

    def handle(self, record: logging.LogRecord) -> None:
        self.on_log(record)


class UILog(RecycleView):
    cols = 1

    def __init__(self, *loggers_to_handle, **kwargs):
        super(UILog, self).__init__(**kwargs)
        self.data = []
        for logger in loggers_to_handle:
            logger.addHandler(LogtoUI(self.on_log))

    def on_log(self, record: logging.LogRecord) -> None:
        self.data.append({"text": escape_markup(record.getMessage())})

    def on_message_markup(self, text):
        self.data.append({"text": text})


class E(ExceptionHandler):
    logger = logging.getLogger("Client")

    def handle_exception(self, inst):
        self.logger.exception(inst)
        return ExceptionManager.RAISE


class KivyJSONtoTextParser(JSONtoTextParser):
    color_codes = {
        # not exact color names, close enough but decent looking
        "black": "000000",
        "red": "EE0000",
        "green": "00FF7F",
        "yellow": "FAFAD2",
        "blue": "6495ED",
        "magenta": "EE00EE",
        "cyan": "00EEEE",
        "white": "FFFFFF"
    }

    def _handle_color(self, node: JSONMessagePart):
        colors = node["color"].split(";")
        node["text"] = escape_markup(node["text"])
        for color in colors:
            color_code = self.color_codes.get(color, None)
            if color_code:
                node["text"] = f"[color={color_code}]{node['text']}[/color]"
                return self._handle_text(node)
        return self._handle_text(node)


ExceptionManager.add_handler(E())

Config.set("input", "mouse", "mouse,disable_multitouch")
Config.set('kivy', 'exit_on_escape', '0')
Builder.load_file(Utils.local_path("data", "client.kv"))
