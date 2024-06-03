from kvui import (App, ScrollBox, Button, MainLayout, ContainerLayout, dp, Widget, BoxLayout, TooltipLabel, ToolTip,
                  Label)
from kivy.uix.slider import Slider
from kivy.uix.dropdown import DropDown
import Utils
import typing
import webbrowser
from urllib.parse import urlparse
from worlds.AutoWorld import AutoWorldRegister, World
from Options import (Option, Toggle, TextChoice, Choice, FreeText, NamedRange, Range, OptionSet, OptionList, OptionDict,
                     Removed, Visibility)


def validate_url(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False


class YamlCreator(App):
    container: ContainerLayout
    main_layout: MainLayout
    scrollbox: ScrollBox
    option_layout: MainLayout
    options: typing.Dict[str, typing.Any]

    def create_range(self, option: typing.Type[Range], name: str):
        def update_text(slider, touch):
            slider.text.text = f"{slider.value:.0f}"
            self.options[name] = slider.value
            return

        box = BoxLayout(spacing=15, orientation="horizontal")
        slider = Slider(min=option.range_start, max=option.range_end, value=option.default, step=1)
        number_label = Label(text=str(option.default))
        slider.text = number_label
        slider.bind(on_touch_move=update_text)
        box.add_widget(slider)
        box.slider = slider
        box.add_widget(number_label)
        self.options[name] = option.default
        return box

    def create_named_range(self, option: typing.Type[NamedRange], name: str):
        def set_to_custom(slider, touch):
            slider.dropdown.select("Custom")
            self.options[name] = slider.value

        def set_value(button):
            slider_box.slider.dropdown.select(button.text)
            self.options[name] = button.text.lower()
            slider_box.slider.value = option.special_range_names[button.text.lower()]
            slider_box.slider.text.text = f"{slider_box.slider.value:.0f}"

        def open(button):
            # for some reason this fixes an issue causing some to not open
            slider_box.slider.dropdown.open(button)

        box = BoxLayout(orientation="vertical", spacing=5)
        slider_box = self.create_range(option, name)
        slider_box.slider.bind(on_touch_move=set_to_custom)
        slider_box.slider.dropdown = DropDown()
        for choice in option.special_range_names:
            btn = Button(text=choice.title(), size_hint_y=None)
            btn.bind(on_release=set_value)
            slider_box.slider.dropdown.add_widget(btn)
        if option.default in option.special_range_names.values():
            default = list(option.special_range_names.keys())[list(option.special_range_names.values())
                                                              .index(option.default)]
        else:
            default = "Custom"
        main_button = Button(text=default.title())
        main_button.bind(on_release=open)
        slider_box.slider.dropdown.bind(on_select=lambda instance, x: setattr(main_button, 'text', x))
        box.add_widget(main_button)
        box.add_widget(slider_box)
        self.options[name] = option.default
        return box

    def create_choice(self, option: typing.Type[Choice], name: str):
        def set_value(button):
            dropdown.select(button.text)
            self.options[name] = button.value

        def open(button):
            # for some reason this fixes an issue causing some to not open
            dropdown.open(button)

        dropdown = DropDown()
        for choice in option.name_lookup:
            btn = Button(text=option.get_option_name(choice), size_hint_y=None)
            btn.value = option.name_lookup[choice]
            btn.bind(on_release=set_value)
            dropdown.add_widget(btn)
        main_button = Button(text=option.get_option_name(option.default))
        main_button.bind(on_release=open)
        self.options[name] = option.name_lookup[option.default]
        dropdown.bind(on_select=lambda instance, x: setattr(main_button, 'text', x))
        return main_button

    def create_text_choice(self, option: typing.Type[TextChoice], name: str):
        pass

    def create_option(self, option: typing.Type[Option], name: str) -> Widget:
        option_base = BoxLayout(orientation="vertical", size_hint_y=None)
        tooltip = option.__doc__.replace("\n    ", " ").replace("\n", "")
        option_label = TooltipLabel(text=f"[ref=0|{tooltip}]{getattr(option, 'display_name', name)}",
                                    size_hint_y=None)
        option_base.add_widget(option_label)
        if issubclass(option, NamedRange):
            option_base.add_widget(self.create_named_range(option, name))
        elif issubclass(option, Range):
            option_base.add_widget(self.create_range(option, name))
        elif issubclass(option, TextChoice):
            pass
        elif issubclass(option, Choice):
            option_base.add_widget(self.create_choice(option, name))
        return option_base

    def create_options_panel(self, world_button):
        self.option_layout.clear_widgets()
        self.options.clear()
        cls: typing.Type[World] = world_button.world_cls
        if not cls.web.options_page:
            return
        elif isinstance(cls.web.options_page, str):
            if validate_url(cls.web.options_page):
                webbrowser.open(cls.web.options_page)
            else:
                # attach onto archipelago.gg and see if we pass
                new_url = "https://archipelago.gg/" + cls.web.options_page
                if validate_url(new_url):
                    webbrowser.open(new_url)
                # else just fall through
        else:
            new_scroll = ScrollBox()
            new_scroll.scroll_type = ["bars"]
            new_scroll.layout.orientation = "vertical"
            for name, option in cls.options_dataclass.type_hints.items():
                if option is not Removed and option.visibility & Visibility.simple_ui:
                    new_scroll.layout.add_widget(self.create_option(option, name))
            self.option_layout.add_widget(new_scroll)

    def build(self):
        self.options = {}
        self.container = ContainerLayout()
        self.main_layout = MainLayout(cols=2)
        self.container.add_widget(self.main_layout)
        self.scrollbox = ScrollBox(size_hint_x=None, width=dp(150))
        self.scrollbox.layout.orientation = "vertical"
        for world, cls in AutoWorldRegister.world_types.items():
            if world == "Archipelago":
                continue
            world_button = Button(text=world, size_hint_y=None)
            world_button.text_size = (dp(100), None)
            world_button.bind(on_release=self.create_options_panel)
            world_button.world_cls = cls
            self.scrollbox.layout.add_widget(world_button)
        self.option_layout = MainLayout(cols=1)
        self.main_layout.add_widget(self.scrollbox)
        self.main_layout.add_widget(self.option_layout)

        return self.container


def launch():
    YamlCreator().run()
