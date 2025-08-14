import os

import Utils
import typing
from kvui import ContainerLayout, MainLayout, KivyJSONtoTextParser, ThemedApp
from kivy.metrics import dp
from kivy.uix.textinput import TextInput
from kivy.lang.parser import Parser
from kivy.core.window import Window
from kivymd.uix.button import MDButton, MDButtonText
from kivy.uix.colorpicker import ColorPicker
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.utils import hex_colormap, get_color_from_hex

if __name__ == "__main__":
    import ModuleUpdate
    ModuleUpdate.update()


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

default_dynamic_theme: dict[str, str | float] = {
    "theme_style": "Dark",
    "primary_palette": "Lightsteelblue",
    "dynamic_scheme_name": "VIBRANT",
    "dynamic_scheme_contrast": 0.0
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


class ColorButton(MDButton):
    real_name: str = "white"
    color_usage: str = "Text"
    text: MDButtonText = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        if "real_name" in kwargs:
            self.real_name = kwargs.pop("real_name")
        self.color_usage = color_usages[self.real_name]
        super().__init__(*args, **kwargs)


class ColorPickerApp(ThemedApp):
    base_title: str = "Archipelago Color Picker"
    container: ContainerLayout
    grid: MainLayout
    color_picker: ColorPicker
    button_layout: MainLayout
    options_layout: MDBoxLayout
    presets_button: MDButton
    preset_dropdown: MDDropdownMenu
    color_layout: MainLayout
    theme_layout: MainLayout
    text_colors: dict[str, str] = default_colors.copy()
    dynamic_theme: dict[str, str | float] = default_dynamic_theme.copy()
    buttons: dict[str, MDButton] = {}
    current_color: str = "red"

    def __init__(self, ctx=None) -> None:
        self.title = self.base_title
        self.ctx = ctx
        self.icon = r"data/icon.png"
        super().__init__()
        text_colors = KivyJSONtoTextParser.TextColors()
        for color in self.text_colors:
            self.text_colors[color] = getattr(text_colors, color, "FFFFFF")
        for val in self.dynamic_theme:
            self.dynamic_theme[val] = getattr(text_colors, val)

    def build(self) -> Widget:
        self.set_colors()
        self.container = Builder.load_file(Utils.local_path("data/colorpicker.kv"))
        self.grid = self.container.grid
        self.color_picker = self.container.color_picker
        self.color_picker.color = get_color_from_hex(self.text_colors[self.current_color])
        self.color_picker.bind(color=lambda picker, x: self.on_color(picker, x))
        self.options_layout = self.container.options
        self.presets_button = self.container.presets
        self.preset_dropdown = MDDropdownMenu(caller=self.presets_button)

        def open_dropdown(button: MDButton) -> None:
            self.populate_dropdown(self.preset_dropdown)
            self.preset_dropdown.open()

        self.presets_button.bind(on_release=open_dropdown)
        self.preset_dropdown.bind(on_select=lambda instance, x: self.set_preset(instance, x))
        self.button_layout = self.container.buttons
        self.color_layout = self.container.colors

        for color in self.text_colors:
            new_button = ColorButton(real_name=color)
            new_button.bind(on_release=lambda button: self.set_color(button))
            self.buttons[color] = new_button
            self.color_layout.add_widget(new_button)
        self.theme_layout = self.container.theme

        def update_dynamic_val(dropdown: MDDropdownMenu, name: str, val: str | float):
            setattr(self.theme_cls, name, val)
            self.dynamic_theme[name] = val
            dropdown.dismiss()

        def update_contrast(instance: MDTextField):
            val = min(1.0, max(0.0, float(instance.text)))
            self.theme_cls.dynamic_scheme_contrast = val
            self.dynamic_theme["dynamic_scheme_contrast"] = val
            instance.text = str(val)

        theme_button = self.container.style
        palette_button = self.container.palette
        scheme_button = self.container.scheme
        contrast_input = self.container.contrast
        theme_dropdown = MDDropdownMenu(caller=theme_button, items=[
            {
                "text": "Light",
                "on_release": lambda: update_dynamic_val(theme_dropdown, "theme_style", "Light")
            },
            {
                "text": "Dark",
                "on_release": lambda: update_dynamic_val(theme_dropdown, "theme_style", "Dark")
            }
        ])
        theme_button.bind(on_release=lambda x: theme_dropdown.open())
        palette_dropdown = MDDropdownMenu(caller=palette_button, items=[
            {
                "text": color.title(),
                "on_release": lambda col=color.title(): update_dynamic_val(palette_dropdown, "primary_palette", col)
            } for color in hex_colormap
        ])
        palette_button.bind(on_press=lambda x: palette_dropdown.open())
        scheme_dropdown = MDDropdownMenu(caller=scheme_button, items=[
            {
                "text": scheme.title(),
                "on_release": lambda sch=scheme.upper(): update_dynamic_val(scheme_dropdown, "dynamic_scheme_name", sch)
            } for scheme in ("TONAL_SPOT", "SPRITZ", "VIBRANT", "EXPRESSIVE", "FRUIT_SALAD", "RAINBOW", "MONOCHROME",
                             "FIDELITY", "CONTENT")
        ])
        scheme_button.bind(on_release=lambda x: scheme_dropdown.open())
        contrast_input.bind(on_text_validate=update_contrast)


        # Uncomment to re-enable the Kivy console/live editor
        # Ctrl-E to enable it, make sure numlock/capslock is disabled
        from kivy.modules.console import create_console
        create_console(Window, self.container)

        return self.container

    def populate_dropdown(self, dropdown: MDDropdownMenu) -> None:
        dropdown.items.clear()
        path = Utils.user_path("data", "presets")
        for dirpath, _, files in os.walk(path):
            for file in files:
                if file.endswith(".kv"):
                    file_path = os.path.join(dirpath, file)
                    dropdown.items.append({
                        "text": file.replace(".kv", ""),
                        "on_release": lambda path=file_path: self.set_preset(dropdown, path)
                    })
        dropdown.items.append({
            "text": "Save as new Preset?",
            "on_release": lambda: self.save_preset_menu()
        })

    def set_preset(self, _: MDDropdownMenu, path: str) -> None:
        preset_name, _ = os.path.splitext(os.path.basename(path))
        setattr(self.presets_button, "text", f"Preset Loaded: {preset_name}")
        self.parse_preset_kv(path)

    def set_color(self, button: MDButton):
        self.current_color = button.real_name.lower()
        self.color_picker.set_color(get_color_from_hex(self.text_colors[self.current_color]))

    def get_color(self, button):
        return get_color_from_hex(self.text_colors[button.real_name.lower()])

    def on_color(self, instance, value):
        self.text_colors[self.current_color] = instance.hex_color[1:-2]  # formatted usually #RRGGBBAA
        self.buttons[self.current_color].md_bg_color = value

    def restore_defaults(self):
        self.set_text_colors(default_colors, default_dynamic_theme)
        setattr(self.presets_button, "text", "Preset Loaded: None")

    def restore_current(self):
        user_colors = Utils.local_path("data", "user.kv")
        self.parse_preset_kv(user_colors)
        setattr(self.presets_button, "text", "Preset Loaded: None")

    def set_text_colors(self, colors, dynamic):
        self.text_colors = colors.copy()
        self.dynamic_theme = dynamic.copy()
        for button in self.buttons:
            self.buttons[button].md_bg_color = get_color_from_hex(self.text_colors[button])
        self.color_picker.set_color(get_color_from_hex(self.text_colors[self.current_color]))

    def parse_preset_kv(self, path):
        colors = default_colors.copy()
        dynamic = default_dynamic_theme.copy()
        # This is thick in the Kivy weeds
        parser = Parser(content=open(path, 'r').read())
        for selector, rule in parser.rules:
            if selector.key == "mdlabel":
                colors["white"] = rule.properties["color"].co_value
            elif selector.key == "textcolors":
                for prop in rule.properties:
                    if prop in colors:
                        colors[prop] = rule.properties[prop].co_value
                    elif prop in dynamic:
                        dynamic[prop] = rule.properties[prop].co_value
        self.set_text_colors(colors, dynamic)

    def save_preset_menu(self):
        save: bool = False
        outer_box = MDBoxLayout(orientation="vertical", spacing=10)
        preset_name = TextInput(size_hint_y=None, height=50)
        inner_box = MDBoxLayout(orientation="horizontal", spacing=10)
        outer_box.add_widget(preset_name)
        outer_box.add_widget(inner_box)
        cancel = MDButton(MDButtonText(text="Cancel"), size_hint_y=None, height=50)
        confirm = MDButton(MDButtonText(text="Confirm"), size_hint_y=None, height=50)
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
                    self.write_color_file(open(file_path, 'w'), self.text_colors, self.dynamic_theme)
            else:
                popup.dismiss()

        cancel.bind(on_release=lambda button: on_close(False))
        confirm.bind(on_release=lambda button: on_close(True))
        popup.open()

    @staticmethod
    def write_color_file(file, colors, dynamic):
        file.write("<TextColors>:\n")
        for color in colors:
            file.write(f"\t{color}: \"{colors[color].upper()}\"\n")
        for val in dynamic:
            if val == "dynamic_scheme_contrast":
                file.write(f"\t{val}: {dynamic[val]}\n")
            else:
                file.write(f"\t{val}: \"{dynamic[val]}\"\n")
        file.write(f"<SelectableLabel>:\n\ttext_color: \"{colors['white']}\"")

    def on_stop(self):
        user_colors = open(Utils.user_path("data", "user.kv"), 'w')
        self.write_color_file(user_colors, self.text_colors, self.dynamic_theme)
        super().on_stop()


if __name__ == '__main__':
    ColorPickerApp().run()
