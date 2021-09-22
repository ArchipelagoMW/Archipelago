import os
import logging

os.environ["KIVY_NO_CONSOLELOG"] = "1"
os.environ["KIVY_NO_FILELOG"] = "1"
os.environ["KIVY_NO_ARGS"] = "1"
from kivy.app import App
from kivy.base import ExceptionHandler, ExceptionManager, Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.utils import escape_markup
from kivy.lang import Builder

import Utils
from NetUtils import JSONtoTextParser, JSONMessagePart

class GameManager(App):
    logging_pairs = [
        ("Client", "Archipelago"),
    ]

    def __init__(self, ctx):
        self.ctx = ctx
        self.commandprocessor = ctx.command_processor(ctx)
        self.icon = r"data/icon.png"
        self.json_to_kivy_parser = KivyJSONtoTextParser(ctx)
        self.log_panels = {}
        super(GameManager, self).__init__()

    def build(self):
        self.grid = GridLayout()
        self.grid.cols = 1

        self.tabs = TabbedPanel()
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
        textinput = TextInput(size_hint_y=None, height=30, multiline=False)
        textinput.bind(on_text_validate=self.on_message)
        self.grid.add_widget(textinput)
        self.commandprocessor("/help")
        return self.grid

    def on_stop(self):
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
    title = "Archipelago Factorio Client"

class LttPManager(GameManager):
    logging_pairs = [
        ("Client", "Archipelago"),
        ("SNES", "SNES"),
    ]
    title = "Archipelago LttP Client"

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
