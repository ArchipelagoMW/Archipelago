import os
import logging
import sys
os.makedirs("logs", exist_ok=True)
if getattr(sys, "frozen", False):
    logging.basicConfig(format='[%(name)s]: %(message)s', level=logging.INFO,
                        filename=os.path.join("logs", "FactorioClient.txt"), filemode="w")
else:
    logging.basicConfig(format='[%(name)s]: %(message)s', level=logging.INFO)
    logging.getLogger().addHandler(logging.FileHandler(os.path.join("logs", "FactorioClient.txt"), "w"))
os.environ["KIVY_NO_CONSOLELOG"] = "1"
os.environ["KIVY_NO_FILELOG"] = "1"
os.environ["KIVY_NO_ARGS"] = "1"

import asyncio
from CommonClient import server_loop, logger
from FactorioClient import FactorioContext, factorio_server_watcher


async def main():
    ctx = FactorioContext(None, None, True)

    ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
    factorio_server_task = asyncio.create_task(factorio_server_watcher(ctx), name="FactorioServer")
    ui_app = FactorioManager(ctx)
    ui_task = asyncio.create_task(ui_app.async_run(), name="UI")

    await ctx.exit_event.wait()  # wait for signal to exit application
    ui_app.stop()
    ctx.server_address = None
    ctx.snes_reconnect_address = None
    # allow tasks to quit
    await ui_task
    await factorio_server_task
    await ctx.server_task

    if ctx.server is not None and not ctx.server.socket.closed:
        await ctx.server.socket.close()
    if ctx.server_task is not None:
        await ctx.server_task

    while ctx.input_requests > 0:  # clear queue for shutdown
        ctx.input_queue.put_nowait(None)
        ctx.input_requests -= 1


from kivy.app import App
from kivy.uix.label import Label
from kivy.base import ExceptionHandler, ExceptionManager, Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.lang import Builder


class FactorioManager(App):
    def __init__(self, ctx):
        super(FactorioManager, self).__init__()
        self.ctx = ctx
        self.commandprocessor = ctx.command_processor(ctx)
        self.icon = "data/icon.png"

    def build(self):
        self.grid = GridLayout()
        self.grid.cols = 1
        self.tabs = TabbedPanel()
        self.tabs.default_tab_text = "All"
        self.title = "Archipelago Factorio Client"
        pairs = [
            ("Client", "Archipelago"),
            ("FactorioServer", "Factorio Server Log"),
            ("FactorioWatcher", "Bridge File Log"),
        ]
        self.tabs.default_tab_content = UILog(*(logging.getLogger(logger_name) for logger_name, name in pairs))
        for logger_name, display_name in pairs:
            bridge_logger = logging.getLogger(logger_name)
            panel = TabbedPanelItem(text=display_name)
            panel.content = UILog(bridge_logger)
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
            logger.exception(e)


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
        self.data.append({"text": record.getMessage()})


class E(ExceptionHandler):
    def handle_exception(self, inst):
        logger.exception(inst)
        return ExceptionManager.RAISE

ExceptionManager.add_handler(E())


Config.set("input", "mouse", "mouse,disable_multitouch")
Builder.load_string('''
<TabbedPanel>
    tab_width: 200
<Row@Label>:
    canvas.before:
        Color:
            rgba: 0.2, 0.2, 0.2, 1
        Rectangle:
            size: self.size
            pos: self.pos
    text_size: self.width, None
    size_hint_y: None
    height: self.texture_size[1]
    font_size: dp(20)
<UILog>:
    viewclass: 'Row'
    scroll_y: 0
    effect_cls: "ScrollEffect"
    RecycleBoxLayout:
        default_size: None, dp(20)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        spacing: dp(3)
''')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
