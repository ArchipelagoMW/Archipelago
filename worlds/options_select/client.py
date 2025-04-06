from kvui import (ThemedApp, ScrollBox, MainLayout, ContainerLayout, dp, Widget, MDBoxLayout, TooltipLabel, ToolTip,
                  MDLabel, ToggleButton)
from kivy.animation import Animation
from kivy.uix.behaviors.button import ButtonBehavior
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelContent, MDExpansionPanelHeader
from kivymd.uix.label import MDIcon
from kivymd.uix.list import MDListItem, MDListItemTrailingIcon, MDListItemSupportingText
from kivymd.uix.slider import MDSlider, MDSliderHandle, MDSliderValueLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer, MDDialogSupportingText
from kivymd.uix.divider import MDDivider
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.metrics import sp
from textwrap import dedent
from copy import deepcopy
import Utils
import typing
import webbrowser
from urllib.parse import urlparse
from worlds.AutoWorld import AutoWorldRegister, World
from Options import (Option, Toggle, TextChoice, Choice, FreeText, NamedRange, Range, OptionSet, OptionList, OptionDict,
                     Removed, Visibility, VerifyKeys, PlandoTexts, PlandoConnections, ItemLinks)

from .core import save_filename, FixedTooltipLabel


def validate_url(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False


def filter_tooltip(tooltip):
    if tooltip is None:
        tooltip = "No tooltip available."
    return dedent(tooltip).replace("\n", "<br>").replace("&", "&amp;").replace("[", "&bl;").replace("]", "&br;")


def option_can_be_randomized(option: typing.Type[Option]):
    # most options can be randomized, so we should just check for those that cannot
    if any(issubclass(option, option_type) for option_type in (VerifyKeys, Removed, PlandoTexts,
                                                               PlandoConnections, ItemLinks)):
        return False
    elif issubclass(option, FreeText) and not issubclass(option, TextChoice):
        return False
    return True


def check_random(value: typing.Any):
    if not isinstance(value, str):
        return value  # cannot be random if evaluated
    if value.startswith("random-"):
        return "random"
    return value


class TrailingPressedIconButton(
    ButtonBehavior, RotateBehavior, MDListItemTrailingIcon
):
    pass


class VisualRange(MDBoxLayout):
    option: typing.Type[Range]
    name: str
    slider: MDSlider = ObjectProperty(None)

    def __init__(self, *args, option: typing.Type[Range], name: str, **kwargs):
        self.option = option
        self.name = name
        super().__init__(args, kwargs)


class VisualChoice(MDButton):
    option: typing.Type[Choice]
    name: str
    text: MDButtonText = ObjectProperty(None)

    def __init__(self, *args, option: typing.Type[Choice], name: str, **kwargs):
        self.option = option
        self.name = name
        super().__init__(args, kwargs)


class VisualNamedRange(MDBoxLayout):
    option: typing.Type[NamedRange]
    name: str
    range: VisualRange = ObjectProperty(None)
    choice: MDButton = ObjectProperty(None)

    def __init__(self, *args, option: typing.Type[NamedRange], name: str, range: VisualRange, **kwargs):
        self.option = option
        self.name = name
        super().__init__(args, kwargs)
        self.range = range
        self.add_widget(self.range)


class VisualFreeText(MDTextField):
    option: typing.Type[FreeText] | typing.Type[TextChoice]
    name: str

    def __init__(self, *args, option: typing.Type[FreeText] | typing.Type[TextChoice], name: str, **kwargs):
        self.option = option
        self.name = name
        super().__init__(args, kwargs)


class VisualTextChoice(MDBoxLayout):
    option: typing.Type[TextChoice]
    name: str
    choice: VisualChoice = ObjectProperty(None)
    text: VisualFreeText = ObjectProperty(None)

    def __init__(self, *args, option: typing.Type[TextChoice], name: str, choice: VisualChoice,
                 text: VisualFreeText, **kwargs):
        self.option = option
        self.name = name
        super(MDBoxLayout, self).__init__(args, kwargs)
        self.choice = choice
        self.text = text
        self.add_widget(self.choice)
        self.add_widget(self.text)


class VisualToggle(MDBoxLayout):
    button: MDIconButton = ObjectProperty(None)
    option: typing.Type[Toggle]
    name: str

    def __init__(self, *args, option: typing.Type[Toggle], name: str, **kwargs):
        self.option = option
        self.name = name
        super().__init__(args, kwargs)


class VisualListSet(MDDialog):
    button: MDIconButton = ObjectProperty(None)
    option: typing.Type[OptionSet] | typing.Type[OptionList]
    scrollbox: ScrollBox = ObjectProperty(None)
    add: MDIconButton = ObjectProperty(None)
    save: MDButton = ObjectProperty(None)

    def __init__(self, *args, option: typing.Type[OptionSet] | typing.Type[OptionList], name: str, **kwargs):
        self.option = option
        self.name = name
        super().__init__(args, kwargs)

    def remove_item(self, button: MDIconButton):
        list_item = button.parent
        self.scrollbox.layout.remove_widget(list_item)

    def add_generic_item(self, key: str = "New Item"):
        item = MDListItem(theme_bg_color="Custom", md_bg_color=self.theme_cls.surfaceContainerLowColor)
        text = MDTextField(text=key, id="value", pos_hint={"center_x": 0.5, "center_y": 0.5}, size_hint_x=None,
                           width=dp(400))
        item.text = text
        item.ids.text_container.add_widget(text)
        item.add_widget(MDIconButton(icon="minus", on_release=self.remove_item, pos_hint={"center_x": 0.95,
                                                                                     "center_y": 0.5}))
        self.scrollbox.layout.add_widget(item)

    def add_set_item(self, key: str):
        text = MDListItemSupportingText(text=key, id="value")
        item = MDListItem(text, MDIconButton(icon="minus", on_release=self.remove_item))
        item.text = text
        self.scrollbox.layout.add_widget(item)


class YamlCreator(ThemedApp):
    container: ContainerLayout
    main_layout: MainLayout
    scrollbox: ScrollBox
    main_panel: MainLayout
    player_options: MainLayout
    option_layout: MainLayout
    name_input: MDTextField
    game_label: MDLabel
    current_game: str
    options: typing.Dict[str, typing.Any]

    def export_options(self, _: Widget):
        if self.name_input.text and self.current_game:
            file_name = save_filename("Export Options File As...", [("YAML", ["*.yaml"])],
                                      Utils.get_file_safe_name(f"{self.name_input.text}.yaml"))
            options = {
                "name": self.name_input.text,
                "description": f"YAML generated by Archipelago {Utils.__version__}.",
                "game": self.current_game,
                self.current_game: {k: check_random(v) for k, v in self.options.items()}
            }
            with open(file_name, 'w') as f:
                f.write(Utils.dump(options, sort_keys=False))
                f.close()

    def create_range(self, option: typing.Type[Range], name: str):
        def update_text(slider, touch):
            self.options[name] = int(slider.value)
            return

        box = VisualRange(option=option, name=name)
        box.slider.bind(on_touch_move=update_text)
        self.options[name] = option.default
        return box

    def create_named_range(self, option: typing.Type[NamedRange], name: str):
        def set_to_custom(slider, touch):
            if (not self.options[name] == slider.value) and (not self.options[name] in option.special_range_names or
                                                             slider.value != option.special_range_names[
                                                                 self.options[name]]):
                # we should validate the touch here,
                # but this is much cheaper
                self.options[name] = slider.value
                set_button_text(box.choice, "Custom")

        def set_button_text(button: MDButton, text: str):
            button.text.text = text

        def set_value(text):
            box.range.slider.value = min(max(option.special_range_names[text.lower()], option.range_start),
                                         option.range_end)
            set_button_text(box.choice, text)
            self.options[name] = text.lower()
            box.range.slider.dropdown.dismiss()

        def open(button):
            # for some reason this fixes an issue causing some to not open
            box.range.slider.dropdown.open()

        box = VisualNamedRange(option=option, name=name, range=self.create_range(option, name))
        box.range.slider.bind(on_touch_move=set_to_custom)
        items = [
            {
                "text": choice.title(),
                "on_release": lambda text=choice.title(): set_value(text)
            }
            for choice in option.special_range_names
        ]
        box.range.slider.dropdown = MDDropdownMenu(caller=box.range.slider, items=items)
        box.choice.bind(on_release=open)
        self.options[name] = option.default
        return box

    def create_free_text(self, option: typing.Type[FreeText] | typing.Type[TextChoice], name: str):
        text = VisualFreeText(option=option, name=name)

        def set_value(instance):
            self.options[name] = instance.text

        text.bind(on_text_validate=set_value)
        return text

    def create_choice(self, option: typing.Type[Choice], name: str):
        def set_button_text(button: VisualChoice, text: str):
            button.text.text = text

        def set_value(text, value):
            set_button_text(main_button, text)
            self.options[name] = value
            dropdown.dismiss()

        def open(button):
            # for some reason this fixes an issue causing some to not open
            dropdown.open()

        default_random = option.default == "random"
        main_button = VisualChoice(option=option, name=name)
        main_button.bind(on_release=open)

        items = [
            {
                "text": option.get_option_name(choice),
                "on_release": lambda val=choice: set_value(option.get_option_name(val), option.name_lookup[val])
            }
            for choice in option.name_lookup
        ]
        dropdown = MDDropdownMenu(caller=main_button, items=items)
        self.options[name] = option.name_lookup[option.default] if not default_random else option.default
        return main_button

    def create_text_choice(self, option: typing.Type[TextChoice], name: str):
        def set_button_text(button: MDButton, text: str):
            for child in button.children:
                if isinstance(child, MDButtonText):
                    child.text = text

        box = VisualTextChoice(option=option, name=name, choice=self.create_choice(option, name),
                               text=self.create_free_text(option, name))

        def set_value(instance):
            set_button_text(box.choice, "Custom")
            self.options[name] = instance.text

        box.text.bind(on_text_validate=set_value)
        return box

    def create_toggle(self, option: typing.Type[Toggle], name: str) -> Widget:
        def set_value(instance: MDIconButton):
            if instance.icon == "checkbox-outline":
                instance.icon = "checkbox-blank-outline"
            else:
                instance.icon = "checkbox-outline"
            self.options[name] = bool(not self.options[name])

        self.options[name] = bool(option.default)
        checkbox = VisualToggle(option=option, name=name)
        checkbox.button.bind(on_release=set_value)

        return checkbox

    def create_popup(self, option: typing.Type[OptionList] | typing.Type[OptionSet], name: str,
                     world: typing.Type[World]):
        # Despite taking verify keys, we're only supporting Set/List
        # Dict may be feasible in the future, but it needs additional typing work

        valid_keys = deepcopy(option.valid_keys)
        if option.verify_item_name:
            valid_keys += list(world.item_name_to_id.keys())
        if option.verify_location_name:
            valid_keys += list(world.location_name_to_id.keys())

        def apply_changes(button):
            if isinstance(option, OptionList):
                if name not in self.options:
                    self.options[name] = []
                self.options[name].clear()
                for list_item in dialog.scrollbox.layout.children:
                    self.options[name].append(getattr(list_item.text, "text"))
            else:
                if name not in self.options:
                    self.options[name] = set()
                self.options[name].clear()
                for list_item in dialog.scrollbox.layout.children:
                    self.options[name].add(getattr(list_item.text, "text"))
            dialog.dismiss()

        dialog = VisualListSet(option=option, name=name)
        dialog.scrollbox.layout.md_bg_color = self.theme_cls.surfaceContainerLowColor
        dialog.scrollbox.layout.theme_bg_color = "Custom"
        dialog.scrollbox.layout.spacing = dp(5)
        dialog.scrollbox.layout.padding = [0, dp(5), 0, 0]

        if valid_keys:
            def add_item(text):
                dialog.add_set_item(text)
                dropdown.dismiss()

            menu_items = [
                {
                    "text": choice.title(),
                    "on_release": lambda text=choice.title(): add_item(text)
                }
                for choice in valid_keys
            ]
            dropdown = MDDropdownMenu(caller=dialog.add, items=menu_items)
            dialog.add.bind(on_release=lambda x: dropdown.open())
            for item in sorted(option.default):
                dialog.add_set_item(item)
        else:
            dialog.add.bind(on_release=lambda x: dialog.add_generic_item())
            for item in sorted(option.default):
                dialog.add_generic_item(item)

        dialog.save.bind(on_release=apply_changes)
        dialog.open()

    def create_option_set_list(self, option: typing.Type[OptionList] | typing.Type[OptionSet], name: str,
                               world: typing.Type[World]):
        main_button = MDButton(MDButtonText(text="Edit"), on_release=lambda x: self.create_popup(option, name, world))
        return main_button

    def create_option(self, option: typing.Type[Option], name: str, world: typing.Type[World]) -> Widget:
        option_base = MDBoxLayout(orientation="vertical", size_hint_y=None)

        tooltip = filter_tooltip(option.__doc__)
        option_label = TooltipLabel(text=f"[ref=0|{tooltip}]{getattr(option, 'display_name', name)}")
        label_box = MDBoxLayout(orientation="horizontal")
        label_anchor = MDAnchorLayout(anchor_x="right", anchor_y="center")
        label_anchor.add_widget(option_label)
        label_box.add_widget(label_anchor)

        option_base.add_widget(label_box)
        if issubclass(option, NamedRange):
            option_base.add_widget(self.create_named_range(option, name))
        elif issubclass(option, Range):
            option_base.add_widget(self.create_range(option, name))
        elif issubclass(option, Toggle):
            option_base.add_widget(self.create_toggle(option, name))
        elif issubclass(option, TextChoice):
            option_base.add_widget(self.create_text_choice(option, name))
        elif issubclass(option, Choice):
            option_base.add_widget(self.create_choice(option, name))
        elif issubclass(option, FreeText):
            option_base.add_widget(self.create_free_text(option, name))
        elif issubclass(option, OptionList):
            option_base.add_widget(self.create_option_set_list(option, name, world))
        elif issubclass(option, OptionSet):
            option_base.add_widget(self.create_option_set_list(option, name, world))
        else:
            option_base.add_widget(MDLabel(text="This option isn't supported by the option creator.\n"
                                                "Please edit your yaml manually to set this option."))

        if option_can_be_randomized(option):
            def randomize_option(instance: Widget, value: str):
                value = value == "down"
                if value:
                    self.options[name] = "random-" + str(self.options[name])
                else:
                    self.options[name] = self.options[name].replace("random-", "")
                    if self.options[name].isnumeric() or self.options[name] in ("True", "False"):
                        self.options[name] = eval(self.options[name])

                base_object = instance.parent.parent
                label_object = instance.parent
                for child in base_object.children:
                    if child is not label_object:
                        child.disabled = value

            default_random = option.default == "random"
            random_toggle = ToggleButton(MDButtonText(text="Random?"), size_hint_x=None, width=dp(100),
                                         state="down" if default_random else "normal")
            random_toggle.bind(state=randomize_option)
            label_box.add_widget(random_toggle)
            if default_random:
                randomize_option(random_toggle, "down")

        return option_base

    def create_options_panel(self, world_button):
        self.option_layout.clear_widgets()
        self.options.clear()
        cls: typing.Type[World] = world_button.world_cls

        self.current_game = cls.game
        if not cls.web.options_page:
            self.current_game = "None"
            return
        elif isinstance(cls.web.options_page, str):
            self.current_game = "None"
            if validate_url(cls.web.options_page):
                webbrowser.open(cls.web.options_page)
            else:
                # attach onto archipelago.gg and see if we pass
                new_url = "https://archipelago.gg/" + cls.web.options_page
                if validate_url(new_url):
                    webbrowser.open(new_url)
                # else just fall through
        else:
            expansion_box = ScrollBox()
            expansion_box.layout.orientation = "vertical"
            expansion_box.layout.spacing = dp(3)
            expansion_box.scroll_type = ["bars"]
            expansion_box.do_scroll_x = False
            group_names = ["Game Options", *(group.name for group in cls.web.option_groups)]
            groups = {name: [] for name in group_names}
            for name, option in cls.options_dataclass.type_hints.items():
                group = next((group.name for group in cls.web.option_groups if option in group.options), "Game Options")
                groups[group].append((name, option))
            for group, options in groups.items():
                group_item = MDExpansionPanel(size_hint_y=None)
                group_header = MDExpansionPanelHeader(MDListItem(MDListItemSupportingText(text=group),
                                                                 TrailingPressedIconButton(icon="chevron-right",
                                                                                           on_release=lambda x,
                                                                                                             item=group_item:
                                                                                           self.tap_expansion_chevron(
                                                                                               item, x)),
                                                                 md_bg_color=self.theme_cls.surfaceContainerLowestColor,
                                                                 theme_bg_color="Custom",
                                                                 on_release=lambda x, item=group_item:
                                                                 self.tap_expansion_chevron(item, x)))
                group_content = MDExpansionPanelContent(orientation="vertical", theme_bg_color="Custom",
                                                        md_bg_color=self.theme_cls.surfaceContainerLowestColor,
                                                        padding=[dp(12), dp(100), dp(12), 0],
                                                        spacing=dp(3))
                group_item.add_widget(group_header)
                group_item.add_widget(group_content)
                group_box = ScrollBox()
                group_box.layout.orientation = "vertical"
                group_box.layout.spacing = dp(3)
                for name, option in options:
                    if name and option is not Removed and option.visibility & Visibility.simple_ui:
                        group_content.add_widget(self.create_option(option, name, cls))
                expansion_box.layout.add_widget(group_item)
            self.option_layout.add_widget(expansion_box)
        self.game_label.text = f"Game: {self.current_game}"

    def tap_expansion_chevron(
            self, panel: MDExpansionPanel, chevron: TrailingPressedIconButton
    ):
        Animation(
            padding=[0, dp(12), 0, dp(12)]
            if not panel.is_open
            else [0, 0, 0, 0],
            d=0.2,
        ).start(panel)
        panel.open() if not panel.is_open else panel.close()
        panel.set_chevron_down(
            chevron
        ) if not panel.is_open else panel.set_chevron_up(chevron)

    def build(self):
        self.set_colors()
        self.options = {}
        self.container = Builder.load_file(Utils.local_path("data/optionscreator.kv"))
        self.main_layout = MainLayout(cols=2)
        self.container.add_widget(self.main_layout)
        self.scrollbox = ScrollBox(size_hint_x=None, width=dp(150))
        self.scrollbox.do_scroll_x = False
        self.scrollbox.layout.orientation = "vertical"
        for world, cls in sorted(AutoWorldRegister.world_types.items(), key=lambda x: x[0]):
            if world == "Archipelago":
                continue
            world_text = MDButtonText(text=world, size_hint_y=None, width=dp(150),
                                      pos_hint={"x": 0.03, "center_y": 0.5})
            world_text.text_size = (world_text.width, None)
            world_text.bind(width=lambda *x, text=world_text: text.setter('text_size')(text, (text.width, None)),
                            texture_size=lambda *x, text=world_text: text.setter("height")(text,
                                                                                           world_text.texture_size[1]))
            world_button = MDButton(world_text, size_hint_x=None, width=dp(150), theme_width="Custom")
            world_button.radius = (dp(5), dp(5), dp(5), dp(5))
            world_button.bind(on_release=self.create_options_panel)
            world_button.world_cls = cls
            self.scrollbox.layout.add_widget(world_button)
        self.main_panel = MainLayout(rows=2)
        self.player_options = MDBoxLayout(orientation="horizontal", height=dp(60), size_hint_y=None, spacing=dp(5),
                                          padding=[0, dp(10), 0, 0])
        button_box = MDBoxLayout(orientation="vertical", spacing=dp(2))
        self.game_label = MDLabel(text="Game: None", pos_hint={"center_x": 0.5, "center_y": 0.5})
        button_box.add_widget(self.game_label)
        self.name_input = MDTextField(MDTextFieldHintText(text="Player Name"), multiline=False)
        self.player_options.add_widget(self.name_input)
        export_button = MDButton(MDButtonText(text="Export Options"), pos_hint={"center_x": 0.5, "center_y": 0.5})
        export_button.bind(on_press=self.export_options)
        button_box.add_widget(export_button)
        self.player_options.add_widget(button_box)
        self.option_layout = MainLayout(cols=1)
        self.main_panel.add_widget(self.player_options)
        self.main_panel.add_widget(self.option_layout)
        self.main_layout.add_widget(self.scrollbox)
        self.main_layout.add_widget(self.main_panel)

        return self.container


def launch():
    YamlCreator().run()
