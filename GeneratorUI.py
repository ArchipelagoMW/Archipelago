import asyncio
import os
import re
import tempfile
import typing
import shlex
from shutil import which
from typing import Optional

import yaml

from kvui import ThemedApp, UILog

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarButtonContainer, MDSnackbarCloseButton, MDSnackbarText
from kivymd.uix.textfield import MDTextField
from Utils import is_linux, is_macos, is_windows, parse_yamls

kv = """
<OutlinedGrid@MDGridLayout>:
    canvas:
        Color:
            rgb: 1, 1, 1
        Line:
            width: 2
            rectangle: self.x, self.y, self.width, self.height

<MarkupLabel@SelectableLabel>
    markup: True
    size_hint: 1, None
    padding: [2, 2, 2, 2]
    on_ref_press: app.on_ref_press(*args)
    adaptive_height: True

MDBoxLayout:
    orientation: "vertical"
    padding: [10, 10, 10, 10]
    spacing: 10

    MDButton:
        text: "Archipelago Generator"
        size_hint: None, 0.1
        pos_hint: {"right": 1}
        on_press: app.open_file()

        MDButtonIcon:
            icon: "file-plus"

        MDButtonText:
            text: "Add File"

    StackLayout:
        canvas:
            Color:
                rgb: 1, 1, 1
            Line:
                width: 2
                rectangle: self.x, self.y, self.width, self.height

        padding: [10, 10, 10, 10]
        MDGridLayout:
            id: player_table
            adaptive_height: True
            row_default_height: 30
            cols: 4
            pos_hint: {"center_x": 0.5}

    MDBoxLayout:
        orientation: "horizontal"
        adaptive_height: True
        spacing: "5dp"

        MDLabel:
            text: "Additional options :"
            height: "30dp"
            adaptive_width: True

        TextInput:
            id: options_field
            multiline: False
            height: "30dp"
            size_hint_y: None
            background_color: app.theme_cls.backgroundColor
            cursor_color: app.theme_cls.primaryColor
            foreground_color: app.theme_cls.primaryColor

    MDButton:
        style: "filled"
        size_hint: None, 0.1
        pos_hint: {"center_x": 0.5}
        on_press: app.generate()

        MDButtonText:
            text: "Generate"

    MDLabel:
        style: "filled"
        size_hint: None, 0.1
        text: "Output"

    UILog:
        id: ui_log
        viewclass: "MarkupLabel"
        padding: [5, 5, 5, 5]

        canvas.before:
            Color:
                rgba: (1, 1, 1, 0.2)
            Rectangle:
                size: self.size
                pos: self.pos
"""


async def show_in_file_explorer(path: str) -> str:
    async def run(*args: str):
        proc = await asyncio.create_subprocess_exec(
            args[0],
            *args[1:],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, _ = await proc.communicate()
        return stdout.decode("utf-8").split("\n", 1)[0] or None

    if is_linux:
        # Attempt to open using DBus
        gdbus = which("gdbus")
        if gdbus:
            return await run(
                gdbus,
                "call",
                "--session",
                "--dest",
                "org.freedesktop.FileManager1",
                "--object-path",
                "/org/freedesktop/FileManager1",
                "--method",
                "org.freedesktop.FileManager1.ShowItems",
                f'["file://{path}"]',
                '""',
            )
    elif is_macos:
        # I have not tested this part yet
        return await run("open", "-R", path)
    elif is_windows:
        return await run("explorer", "/select", path)

    raise Exception("Could not show file in explorer")


async def open_filename(
    title: str, filetypes: typing.Iterable[typing.Tuple[str, typing.Iterable[str]]], suggest: str = ""
) -> Optional[str]:
    """Opens a file browser.
    Opens the native file browser if possible, falls back to tkinter otherwise.

    I copy-pasted this functions from utils to use the create_subprocess_exec function from asyncio and make the whole
    function async, even if it copies over the entire logic. I'm not sure that the TKinter part works correctly.

    I would have preferred to update  the existing function to support async, but it does not exactly work that way. The
    blocking nature of the function freezes the entire UI and leads to a program crash.
    """

    async def run(*args: str):
        proc = await asyncio.create_subprocess_exec(
            args[0],
            *args[1:],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, _ = await proc.communicate()
        return stdout.decode("utf-8").split("\n", 1)[0] or None

    if is_linux:
        # prefer native dialog
        kdialog = which("kdialog")
        if kdialog:
            k_filters = "|".join((f'{text} (*{" *".join(ext)})' for (text, ext) in filetypes))
            return await run(
                kdialog,
                f"--title={title}",
                "--getopenfilename",
                suggest or ".",
                k_filters,
            )
        zenity = which("zenity")
        if zenity:
            z_filters = (f'--file-filter={text} ({", ".join(ext)}) | *{" *".join(ext)}' for (text, ext) in filetypes)
            selection = (f"--filename={suggest}",) if suggest else ()
            return await run(zenity, f"--title={title}", "--file-selection", *z_filters, *selection)

    # fall back to tk
    try:
        import tkinter
        import tkinter.filedialog
    except Exception as e:
        raise e
    else:
        try:
            root = tkinter.Tk()
        except tkinter.TclError:
            return None  # GUI not available. None is the same as a user clicking "cancel"
        root.withdraw()
        return tkinter.filedialog.askopenfilename(
            title=title,
            filetypes=((t[0], " ".join(t[1])) for t in filetypes),
            initialfile=suggest or None,
        )


class GeneratorApp(ThemedApp):
    player_table: MDGridLayout
    ui_log: UILog
    options_field: TextInput

    players: list = []
    dropped_text: list[str] = []
    dropped_files: list[str] = []

    # Added this here for compatibility with SelectableLabel
    last_autofillable_command: str = ""
    textinput: MDTextField

    def __init__(self):
        super(GeneratorApp, self).__init__()
        self.yamls = []

    def build(self):
        self.set_colors()
        self.title = "Archipelago Generator"

        Window.bind(on_drop_file=self._on_file_drop)
        Window.bind(on_drop_text=self._on_text_drop)
        Window.bind(on_drop_begin=self._on_drop_begin)
        Window.bind(on_drop_end=self._on_drop_end)

        ui = Builder.load_string(kv)
        self.player_table = ui.ids.player_table
        self.ui_log = ui.ids.ui_log
        self.options_field = ui.ids.options_field

        # Added this here for compatibility with SelectableLabel
        self.textinput = MDTextField()

        # for header in ["No.", "Name", "Game", "Remove"]:
        self.player_table.add_widget(Label(text="No.", text_size=(None, 30), size_hint_x=2))
        self.player_table.add_widget(Label(text="Name", text_size=(None, 30), size_hint_x=8))
        self.player_table.add_widget(Label(text="Game", text_size=(None, 30), size_hint_x=8))
        self.player_table.add_widget(Label(text="", text_size=(None, 30), size_hint_x=2))

        return ui

    def _on_drop_begin(self, *_) -> None:
        self.dropped_text = []
        self.dropped_files = []

    def _on_file_drop(self, window, file_path: bytes, *_) -> None:
        self.dropped_files.append(file_path.decode("utf-8"))

    def _on_text_drop(self, window, text: bytes, *_) -> None:
        self.dropped_text.append(text.decode("utf-8"))

    def _on_drop_end(self, *_):
        for file_path in self.dropped_files:
            self._add_yaml_file(file_path)

        for document in parse_yamls("\n".join(self.dropped_text)):
            self._add_yaml(document)

    def on_ref_press(self, _, ref: str) -> None:
        match = re.match("file\\|(.*)", ref)
        if match:
            file_path = match.group(1)
            asyncio.create_task(show_in_file_explorer(file_path))

    def _add_yaml_file(self, file_path: str) -> None:
        with open(file_path, "r", encoding="utf-8") as f:
            for document in parse_yamls(f.read()):
                self._add_yaml(document, os.path.basename(file_path))

    def _add_yaml(self, document, file_name: Optional[str] = None) -> None:
        if (
            "name" not in document
            or "game" not in document
            or not isinstance(document["name"], str)
            or not isinstance(document["game"], str)
        ):
            message = "Invalid Player YAML file"
            if file_name:
                message = f"{message}: {file_name}"

            self._show_error_in_snackbar(message)
            return

        no = len(self.players) + 1

        name = document["name"]
        game = document["game"]

        widgets = [
            Label(text=str(no), size_hint_y=30),
            Label(text=name, size_hint_y=30),
            Label(text=game, size_hint_y=30),
            MDIconButton(
                icon="minus-circle-outline",
                style="standard",
                on_release=self._remove_yaml,
            ),
        ]

        for widget in widgets:
            self.player_table.add_widget(widget)

        self.players.append({"name": name, "game": game, "document": document, "widgets": widgets})

    async def _generate_async(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            for idx, player in enumerate(self.players):
                filename = f"P{idx}_{player["name"]}.yaml"
                file_path = os.path.join(temp_dir, filename)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(yaml.dump(player["document"]))

            process = await asyncio.create_subprocess_exec(
                "python",
                "Generate.py",
                "--player_files_path",
                temp_dir,
                *shlex.split(self.options_field.text),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            # Clear messages from previous run
            for i in range(0, len(self.ui_log.data)):
                self.ui_log.data.pop(0)

            asyncio.create_task(self._log_stream_to_ui(process.stdout, "ffffff"))
            asyncio.create_task(self._log_stream_to_ui(process.stderr, "ff0000"))

            # If there is an error with the Generate.py script, the script will wait for an input before closing.
            # Send a bunch of newlines just in case.
            process.stdin.write(10 * "\n".encode("utf-8"))
            await process.wait()

            if process.returncode == 0:
                self.ui_log.on_message_markup("[color=008000]Generation completed successfully[/color]")
            else:
                self.ui_log.on_message_markup(
                    f"[color=7F7FFF]Generation failed with status code {process.returncode}[/color]"
                )

    async def _log_stream_to_ui(self, stream: asyncio.StreamReader, color: str) -> None:
        while True:
            line = await stream.readline()
            if line:
                text = line.decode("utf-8").replace("\n", "")
                if text == "Press enter to close.":
                    continue

                match = re.match("Creating final archive at (.*)", text)
                if match:
                    start = match.start(1)
                    end = match.end(1)

                    text = f"{text[:start]}[ref=file|{match.group(1)}][u]{match.group(1)}[/u][/ref]{text[end:]}"

                self.ui_log.on_message_markup(f"[color={color}]{text}[/color]")
            else:
                break

    def generate(self) -> None:
        asyncio.create_task(self._generate_async())

    async def open_player_file(self) -> None:
        file_path = await open_filename("Select player file", (("YAML", ["yaml", "yml"]),))
        if file_path:
            self._add_yaml_file(file_path)

    def open_file(self) -> None:
        asyncio.create_task(self.open_player_file())

    def _remove_yaml(self, target) -> None:
        for player in self.players:
            if target in player["widgets"]:
                self.players.remove(player)

                for widget in player["widgets"]:
                    self.player_table.remove_widget(widget)

                self._renumber_players()
                break

    def _renumber_players(self) -> None:
        for idx, player in enumerate(self.players):
            player["no"] = idx + 1
            player["widgets"][0].text = str(idx + 1)

    def _show_error_in_snackbar(self, message: str) -> None:
        MDSnackbar(
            MDSnackbarText(text=message),
            MDSnackbarButtonContainer(MDSnackbarCloseButton(icon="close"), pos_hint={"center_y": 0.5}),
            y=dp(24),
            orientation="horizontal",
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
            background_color=self.theme_cls.onErrorContainerColor,
        ).open()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(GeneratorApp().async_run())
    loop.close()
