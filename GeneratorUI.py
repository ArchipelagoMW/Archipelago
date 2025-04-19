import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
import re
import tempfile
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
from Utils import is_linux, is_macos, is_windows, local_path, parse_yamls, open_filename

async def show_in_file_explorer(path: str) -> None:
    """Open the specified path in the native file explorer for the user's operating system
    
    :param path: The path of the file or folder to show
    """
    async def run(*args: str) -> None:
        proc = await asyncio.create_subprocess_exec(
            args[0],
            *args[1:],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        await proc.communicate()

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

class GeneratorApp(ThemedApp):
    player_table: MDGridLayout
    ui_log: UILog
    options_field: TextInput

    players: list
    dropped_text: list[str]
    dropped_files: list[str]

    # Added this here for compatibility with SelectableLabel
    last_autofillable_command: str = ""
    textinput: MDTextField

    def __init__(self):
        super(GeneratorApp, self).__init__()
        self.players = []
        self.dropped_text = []
        self.dropped_files = []

    def build(self):
        self.set_colors()
        self.title = "Archipelago Generator"

        Window.bind(on_drop_file=self._on_file_drop)
        Window.bind(on_drop_text=self._on_text_drop)
        Window.bind(on_drop_begin=self._on_drop_begin)
        Window.bind(on_drop_end=self._on_drop_end)

        ui = Builder.load_file(local_path("data", "generator.kv"))
        self.player_table = ui.ids.player_table
        self.ui_log = ui.ids.ui_log
        self.options_field = ui.ids.options_field

        # Added this here for compatibility with SelectableLabel
        self.textinput = MDTextField()

        # for header in ["No.", "Name", "Game", "Remove"]:
        self.player_table.add_widget(Label(text="No.", text_size=(None, 30), size_hint_x=2))
        self.player_table.add_widget(Label(text="Name", text_size=(None, 30), size_hint_x=8))
        self.player_table.add_widget(Label(text="Game", text_size=(None, 30), size_hint_x=8))
        self.player_table.add_widget(Label(text="File", text_size=(None, 30), size_hint_x=8))
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
        def show_error() -> None:
            message = "Invalid Player YAML file"
            if file_name:
                message = f"{message}: {file_name}"

            self._show_error_in_snackbar(message)
            return
        
        no = len(self.players) + 1

        if "name" not in document:
            name = "N/A" 
        elif isinstance(document["name"], str):
            name = document["name"]
        elif isinstance(document["name"], dict):
            name = '/'.join(document["name"].keys())
        else:
            show_error()

        if len(name) > 30:
            name = f"{name[0:29]}..."

        if "game" not in document:
            game = "N/A"
        elif isinstance(document["game"], str):
            game = document["game"]
        elif isinstance(document["game"], dict):
            keys = document["game"].keys()
            count = len(keys)
            game = list(keys)[0]
            if count > 1:
                game = f"{game} (+{count - 1} more)"
        else:
            return show_error()

        widgets = [
            Label(text=str(no), size_hint_x=2, size_hint_y=30),
            Label(text=name, size_hint_x=8, size_hint_y=30),
            Label(text=game, size_hint_x=8, size_hint_y=30),
            Label(text=file_name or "Text Drop"),
            MDIconButton(
                icon="minus-circle-outline",
                style="standard",
                on_release=self._remove_yaml,
                size_hint_x=2
            ),
        ]

        for widget in widgets:
            self.player_table.add_widget(widget)

        self.players.append({"name": name, "game": game, "document": document, "widgets": widgets})

    async def _generate_async(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            for idx, player in enumerate(self.players):
                filename = f"P{idx}.yaml"
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
        with ThreadPoolExecutor(1) as executor:
            file_path = await asyncio.get_running_loop().run_in_executor(executor, lambda: open_filename("Select player file", (("YAML", ["yaml", "yml"]),)))
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
