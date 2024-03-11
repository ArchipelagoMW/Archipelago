from kivy.app import App
from kivy.metrics import dp

import Utils
import typing
from kvui import ContainerLayout, MainLayout, KivyJSONtoTextParser
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivy.uix.boxlayout import BoxLayout

from kivy.graphics import Color, Rectangle

if __name__ == "__main__":
    import ModuleUpdate
    ModuleUpdate.update()


def hex_color_to_tuple(color: str):
    if len(color) != 6:
        color = color[:5]
    red = color[:2]
    green = color[2:4]
    blue = color[4:]
    r_ratio = int(red, 16) / 255
    g_ratio = int(green, 16) / 255
    b_ratio = int(blue, 16) / 255
    return r_ratio, g_ratio, b_ratio, 1.0


default_colors = {
        "white": "FFFFFF",
        "black": "000000",
        "red": "EE0000",
        "green": "00FF7F",  # typically a location
        "yellow": "FAFAD2",  # typically other slots/players
        "blue": "6495ED",  # typically extra info (such as entrance)
        "magenta": "EE00EE",  # typically your slot/player
        "cyan": "00EEEE",  # typically regular item
        "slateblue": "6D8BE8",  # typically useful item
        "plum": "AF99EF",  # typically progression item
        "salmon": "FA8072",  # typically trap item
    }


class ColorPickerApp(App):
    base_title: str = "Archipelago Color Picker"
    container: ContainerLayout
    grid: MainLayout
    color_picker: ColorPicker
    button_layout: GridLayout
    text_colors = default_colors.copy()
    buttons = {}
    current_color = "red"

    def __init__(self, ctx=None):
        self.title = self.base_title
        self.ctx = ctx
        self.icon = r"data/icon.png"
        super().__init__()
        text_colors = KivyJSONtoTextParser.TextColors()
        for color in self.text_colors:
            self.text_colors[color] = getattr(text_colors, color, "FFFFFF")

    def build(self):
        self.container = ContainerLayout()
        self.grid = MainLayout(cols=1)
        self.grid.spacing = 20
        self.grid.padding = 20
        self.container.add_widget(self.grid)
        self.color_picker = ColorPicker(color=hex_color_to_tuple(self.text_colors[self.current_color]))
        self.color_picker.bind(color=self.on_color)
        self.grid.add_widget(self.color_picker)
        self.options_layout = BoxLayout(size_hint_y=None, height=dp(40), orientation="horizontal")
        defaults_button = Button(text="Restore Defaults")
        defaults_button.bind(on_release=self.restore_defaults)
        self.options_layout.add_widget(defaults_button)
        self.grid.add_widget(self.options_layout)
        self.button_layout = GridLayout(cols=3, size_hint_y=0.5)
        self.button_layout.spacing = 5
        self.button_layout.padding = (10, 5)

        for color in self.text_colors:
            new_button = Button(text=color.title(), background_color=hex_color_to_tuple(self.text_colors[color]))
            new_button.bind(on_release=self.set_color)
            self.buttons[color] = new_button
            self.button_layout.add_widget(new_button)

        self.grid.add_widget(self.button_layout)
        return self.container

    @staticmethod
    def set_color(button):
        picker_app: ColorPickerApp = App.get_running_app()
        picker_app.current_color = button.text.lower()
        picker_app.color_picker.set_color(hex_color_to_tuple(picker_app.text_colors[picker_app.current_color]))

    @staticmethod
    def get_color(button):
        picker_app: ColorPickerApp = App.get_running_app() # little surprised this doesn't give type warnings
        return hex_color_to_tuple(picker_app.text_colors[button.text.lower()])

    @staticmethod
    def on_color(instance, value):
        picker_app: ColorPickerApp = App.get_running_app()
        picker_app.text_colors[picker_app.current_color] = instance.hex_color[1:-2] # formatted usually #RRGGBBAA
        picker_app.buttons[picker_app.current_color].background_color = value

    @staticmethod
    def restore_defaults(button):
        picker_app: ColorPickerApp = App.get_running_app()
        picker_app.text_colors = default_colors.copy()
        for button in picker_app.buttons:
            picker_app.buttons[button].background_color = hex_color_to_tuple(picker_app.text_colors[button])
        picker_app.color_picker.set_color(hex_color_to_tuple(picker_app.text_colors[picker_app.current_color]))

    def set_colors(self, text_colors: KivyJSONtoTextParser.TextColors):
        pass

    def on_stop(self):
        user_colors = open(Utils.local_path("data", "user.kv"), 'w')
        user_colors.write("<TextColors>:\n")
        for color in self.text_colors:
            user_colors.write(f"\t{color}: \"{self.text_colors[color].upper()}\"\n")
        user_colors.write(f"<Label>:\n\tcolor: \"{self.text_colors['white']}\"")
        super().on_stop()


if __name__ == '__main__':
    ColorPickerApp().run()
