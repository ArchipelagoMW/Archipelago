import os

import Utils
import typing
from kvui import ContainerLayout, MainLayout, KivyJSONtoTextParser
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.textinput import TextInput
from kivy.lang.builder import Builder
from kivy.lang.parser import Parser
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

if __name__ == "__main__":
    import ModuleUpdate
    ModuleUpdate.update()


def hex_color_to_tuple(color: str) -> typing.Tuple[float, float, float, float]:
    if len(color) != 6:
        color = color[:5]
    red = color[:2]
    green = color[2:4]
    blue = color[4:]
    r_ratio = int(red, 16) / 255
    g_ratio = int(green, 16) / 255
    b_ratio = int(blue, 16) / 255
    return r_ratio, g_ratio, b_ratio, 1.0


default_colors: typing.Dict[str, str] = {
    "white": "FFFFFF",
    "black": "000000",
    "red": "EE0000",
    "green": "00FF7F",
    "yellow": "FAFAD2",
    "blue": "6495ED",
    "magenta": "EE00EE",
    "cyan": "00EEEE",
    "slateblue": "6D8BE8",
    "plum": "AF99EF",
    "salmon": "FA8072",
    "orange": "FF7700",
}

color_usages: typing.Dict[str, str] = {
    "white": "Text Color",
    "black": "Black",
    "red": "Red/Not Found",
    "green": "Location/Found",
    "yellow": "Other Players",
    "blue": "Entrance",
    "magenta": "Current Player",
    "cyan": "Filler Item",
    "slateblue": "Useful Item",
    "plum": "Progression Item",
    "salmon": "Trap Item",
    "orange": "Command Echo",
}

class ColorPickerApp(App):
    base_title: str = "Archipelago Color Picker"
    container: ContainerLayout
    grid: MainLayout
    color_picker: ColorPicker
    button_layout: GridLayout
    options_layout: BoxLayout
    presets_button: Button
    preset_dropdown: DropDown
    text_colors: typing.Dict[str, str] = default_colors.copy()
    buttons: typing.Dict[str, Button] = {}
    current_color: str = "red"

    def __init__(self, ctx=None) -> None:
        self.title = self.base_title
        self.ctx = ctx
        self.icon = r"data/icon.png"
        super().__init__()
        text_colors = KivyJSONtoTextParser.TextColors()
        for color in self.text_colors:
            self.text_colors[color] = getattr(text_colors, color, "FFFFFF")

    def build(self) -> Widget:
        self.container = ContainerLayout()
        self.grid = MainLayout(cols=1)
        self.grid.spacing = 20
        self.grid.padding = 20
        self.container.add_widget(self.grid)
        self.color_picker = ColorPicker(color=hex_color_to_tuple(self.text_colors[self.current_color]))
        self.color_picker.bind(color=lambda picker, x: self.on_color(picker, x))
        self.grid.add_widget(self.color_picker)
        self.options_layout = BoxLayout(size_hint_y=None, height=dp(40), orientation="horizontal")
        defaults_button = Button(text="Restore Defaults")
        defaults_button.bind(on_release=lambda _: self.restore_defaults())
        self.options_layout.add_widget(defaults_button)
        current_button = Button(text="Restore Current")
        current_button.bind(on_release=lambda _: self.restore_current())
        self.options_layout.add_widget(current_button)
        self.presets_button = Button(text="Preset Loaded: None")
        self.preset_dropdown = DropDown()
        self.populate_dropdown(self.preset_dropdown)

        def open_dropdown(button: Button) -> None:
            self.preset_dropdown.open(button)

        self.presets_button.bind(on_release=self.preset_dropdown.open)
        self.preset_dropdown.bind(on_select=lambda instance, x: self.set_preset(instance, x))
        self.options_layout.add_widget(self.presets_button)
        self.grid.add_widget(self.options_layout)
        self.button_layout = GridLayout(cols=3, size_hint_y=0.5)
        self.button_layout.spacing = 5
        self.button_layout.padding = (10, 5)

        for color in self.text_colors:
            new_button = Button(text=color_usages[color], background_color=hex_color_to_tuple(self.text_colors[color]))
            new_button.real_name = color
            new_button.bind(on_release=lambda button: self.set_color(button))
            self.buttons[color] = new_button
            self.button_layout.add_widget(new_button)

        self.grid.add_widget(self.button_layout)
        return self.container

    def populate_dropdown(self, dropdown: DropDown) -> None:
        dropdown.clear_widgets()
        path = Utils.local_path("data", "presets")
        for dirpath, _, files in os.walk(path):
            for file in files:
                if file.endswith(".kv"):
                    new_button = Button(text=file.replace(".kv", ""), size_hint_y=None)
                    new_button.path = os.path.join(dirpath, file)
                    new_button.bind(on_release=lambda button: self.preset_dropdown.select(button.path))
                    dropdown.add_widget(new_button)
        save_button = Button(text="Save as new Preset?", size_hint_y=None)
        save_button.bind(on_release=lambda button: self.save_preset_menu())
        dropdown.add_widget(save_button)

    def set_preset(self, _: DropDown, path: str) -> None:
        preset_name, _ = os.path.splitext(os.path.basename(path))
        setattr(self.presets_button, "text", f"Preset Loaded: {preset_name}")
        self.parse_preset_kv(path)

    def set_color(self, button: Button):
        self.current_color = button.real_name.lower()
        self.color_picker.set_color(hex_color_to_tuple(self.text_colors[self.current_color]))

    def get_color(self, button):
        return hex_color_to_tuple(self.text_colors[button.real_name.lower()])

    def on_color(self, instance, value):
        self.text_colors[self.current_color] = instance.hex_color[1:-2]  # formatted usually #RRGGBBAA
        self.buttons[self.current_color].background_color = value

    def restore_defaults(self):
        self.set_colors(default_colors)
        setattr(self.presets_button, "text", "Preset Loaded: None")

    def restore_current(self):
        user_colors = Utils.local_path("data", "user.kv")
        self.parse_preset_kv(user_colors)
        setattr(self.presets_button, "text", "Preset Loaded: None")

    def set_colors(self, colors):
        self.text_colors = colors.copy()
        for button in self.buttons:
            self.buttons[button].background_color = hex_color_to_tuple(self.text_colors[button])
        self.color_picker.set_color(hex_color_to_tuple(self.text_colors[self.current_color]))

    def parse_preset_kv(self, path):
        colors = default_colors.copy()
        # This is thick in the Kivy weeds
        parser = Parser(content=open(path, 'r').read())
        for selector, rule in parser.rules:
            if selector.key == "label":
                colors["white"] = rule.properties["color"].co_value
            elif selector.key == "textcolors":
                for prop in rule.properties:
                    colors[prop] = rule.properties[prop].co_value
        self.set_colors(colors)

    def save_preset_menu(self):
        save: bool = False
        outer_box = BoxLayout(orientation="vertical", spacing=10)
        preset_name = TextInput(size_hint_y=None, height=50)
        inner_box = BoxLayout(orientation="horizontal", spacing=10)
        outer_box.add_widget(preset_name)
        outer_box.add_widget(inner_box)
        cancel = Button(text="Cancel", size_hint_y=None, height=50)
        confirm = Button(text="Confirm", size_hint_y=None, height=50)
        inner_box.add_widget(cancel)
        inner_box.add_widget(confirm)
        popup = Popup(title="Save Preset As...",
                      content=outer_box, size_hint=(0.5, 0.3))

        def on_close(res):
            if res:
                name = preset_name.text
                if name:
                    popup.dismiss()
                    file_name = f"{name}.kv" if not name.endswith(".kv") else name
                    file_path = os.path.join(Utils.local_path("data", "presets", file_name))
                    if not os.path.exists(os.path.dirname(file_path)):
                        os.mkdir(os.path.dirname(file_path))
                    self.write_color_file(open(file_path, 'w'), self.text_colors)
                    self.populate_dropdown(self.preset_dropdown)
                    self.preset_dropdown.select(file_path)
                    self.preset_dropdown.dismiss()
            else:
                popup.dismiss()

        cancel.bind(on_release=lambda button: on_close(False))
        confirm.bind(on_release=lambda button: on_close(True))
        popup.open()

    @staticmethod
    def write_color_file(file, colors):
        file.write("<TextColors>:\n")
        for color in colors:
            file.write(f"\t{color}: \"{colors[color].upper()}\"\n")
        file.write(f"<Label>:\n\tcolor: \"{colors['white']}\"")

    def on_stop(self):
        user_colors = open(Utils.local_path("data", "user.kv"), 'w')
        self.write_color_file(user_colors, self.text_colors)
        super().on_stop()


if __name__ == '__main__':
    ColorPickerApp().run()
