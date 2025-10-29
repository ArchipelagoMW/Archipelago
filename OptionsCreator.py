from kvui import (ThemedApp, ScrollBox, MainLayout, ContainerLayout, dp, Widget, MDBoxLayout, TooltipLabel, MDLabel,
                  ToggleButton, MarkupDropdown, ResizableTextField)
from kivy.uix.behaviors.button import ButtonBehavior
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelContent, MDExpansionPanelHeader
from kivymd.uix.list import MDListItem, MDListItemTrailingIcon, MDListItemSupportingText
from kivymd.uix.slider import MDSlider
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivy.core.text.markup import MarkupLabel
from kivy.utils import escape_markup
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from textwrap import dedent
from copy import deepcopy
import Utils
import typing
import webbrowser
import re
from urllib.parse import urlparse
from worlds.AutoWorld import AutoWorldRegister, World
from Options import (Option, Toggle, TextChoice, Choice, FreeText, NamedRange, Range, OptionSet, OptionList, Removed,
                     OptionCounter, Visibility)


def validate_url(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False


def filter_tooltip(tooltip):
    if tooltip is None:
        tooltip = "No tooltip available."
    tooltip = dedent(tooltip).strip().replace("\n", "<br>").replace("&", "&amp;") \
        .replace("[", "&bl;").replace("]", "&br;")
    tooltip = re.sub(r"\*\*(.+?)\*\*", r"[b]\g<1>[/b]", tooltip)
    tooltip = re.sub(r"\*(.+?)\*", r"[i]\g<1>[/i]", tooltip)
    return escape_markup(tooltip)


def option_can_be_randomized(option: typing.Type[Option]):
    # most options can be randomized, so we should just check for those that cannot
    if not option.supports_weighting:
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


class TrailingPressedIconButton(ButtonBehavior, RotateBehavior, MDListItemTrailingIcon):
    pass


class WorldButton(ToggleButton):
    world_cls: typing.Type[World]


class VisualRange(MDBoxLayout):
    option: typing.Type[Range]
    name: str
    tag: MDLabel = ObjectProperty(None)
    slider: MDSlider = ObjectProperty(None)

    def __init__(self, *args, option: typing.Type[Range], name: str, **kwargs):
        self.option = option
        self.name = name
        super().__init__(*args, **kwargs)

        def update_points(*update_args):
            pass

        self.slider._update_points = update_points


class VisualChoice(MDButton):
    option: typing.Type[Choice]
    name: str
    text: MDButtonText = ObjectProperty(None)

    def __init__(self, *args, option: typing.Type[Choice], name: str, **kwargs):
        self.option = option
        self.name = name
        super().__init__(*args, **kwargs)


class VisualNamedRange(MDBoxLayout):
    option: typing.Type[NamedRange]
    name: str
    range: VisualRange = ObjectProperty(None)
    choice: MDButton = ObjectProperty(None)

    def __init__(self, *args, option: typing.Type[NamedRange], name: str, range_widget: VisualRange, **kwargs):
        self.option = option
        self.name = name
        super().__init__(*args, **kwargs)
        self.range = range_widget
        self.add_widget(self.range)


class VisualFreeText(ResizableTextField):
    option: typing.Type[FreeText] | typing.Type[TextChoice]
    name: str

    def __init__(self, *args, option: typing.Type[FreeText] | typing.Type[TextChoice], name: str, **kwargs):
        self.option = option
        self.name = name
        super().__init__(*args, **kwargs)


class VisualTextChoice(MDBoxLayout):
    option: typing.Type[TextChoice]
    name: str
    choice: VisualChoice = ObjectProperty(None)
    text: VisualFreeText = ObjectProperty(None)

    def __init__(self, *args, option: typing.Type[TextChoice], name: str, choice: VisualChoice,
                 text: VisualFreeText, **kwargs):
        self.option = option
        self.name = name
        super(MDBoxLayout, self).__init__(*args, **kwargs)
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
        super().__init__(*args, **kwargs)


class CounterItemValue(ResizableTextField):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        return super().insert_text(re.sub(self.pat, "", substring), from_undo=from_undo)


class VisualListSetCounter(MDDialog):
    button: MDIconButton = ObjectProperty(None)
    option: typing.Type[OptionSet] | typing.Type[OptionList] | typing.Type[OptionCounter]
    scrollbox: ScrollBox = ObjectProperty(None)
    add: MDIconButton = ObjectProperty(None)
    save: MDButton = ObjectProperty(None)
    input: ResizableTextField = ObjectProperty(None)
    dropdown: MDDropdownMenu
    valid_keys: typing.Iterable[str]

    def __init__(self, *args, option: typing.Type[OptionSet] | typing.Type[OptionList],
                 name: str, valid_keys: typing.Iterable[str], **kwargs):
        self.option = option
        self.name = name
        self.valid_keys = valid_keys
        super().__init__(*args, **kwargs)
        self.dropdown = MarkupDropdown(caller=self.input, border_margin=dp(2),
                                       width=self.input.width, position="bottom")
        self.input.bind(text=self.on_text)
        self.input.bind(on_text_validate=self.validate_add)

    def validate_add(self, instance):
        if self.valid_keys:
            if self.input.text not in self.valid_keys:
                MDSnackbar(MDSnackbarText(text="Item must be a valid key for this option."), y=dp(24),
                           pos_hint={"center_x": 0.5}, size_hint_x=0.5).open()
                return

        if not issubclass(self.option, OptionList):
            if any(self.input.text == child.text.text for child in self.scrollbox.layout.children):
                MDSnackbar(MDSnackbarText(text="This value is already in the set."), y=dp(24),
                           pos_hint={"center_x": 0.5}, size_hint_x=0.5).open()
                return

        self.add_set_item(self.input.text)
        self.input.set_text(self.input, "")

    def remove_item(self, button: MDIconButton):
        list_item = button.parent
        self.scrollbox.layout.remove_widget(list_item)

    def add_set_item(self, key: str, value: int | None = None):
        text = MDListItemSupportingText(text=key, id="value")
        if issubclass(self.option, OptionCounter):
            value_txt = CounterItemValue(text=str(value) if value else "1")
            item = MDListItem(text,
                              value_txt,
                              MDIconButton(icon="minus", on_release=self.remove_item), focus_behavior=False)
            item.value = value_txt
        else:
            item = MDListItem(text, MDIconButton(icon="minus", on_release=self.remove_item), focus_behavior=False)
        item.text = text
        self.scrollbox.layout.add_widget(item)

    def on_text(self, instance, value):
        if not self.valid_keys:
            return
        if len(value) >= 3:
            self.dropdown.items.clear()

            def on_press(txt):
                split_text = MarkupLabel(text=txt, markup=True).markup
                self.input.set_text(self.input, "".join(text_frag for text_frag in split_text
                                                        if not text_frag.startswith("[")))
                self.input.focus = True
                self.dropdown.dismiss()

            lowered = value.lower()
            for item_name in self.valid_keys:
                try:
                    index = item_name.lower().index(lowered)
                except ValueError:
                    pass  # substring not found
                else:
                    text = escape_markup(item_name)
                    text = text[:index] + "[b]" + text[index:index + len(value)] + "[/b]" + text[index + len(value):]
                    self.dropdown.items.append({
                        "text": text,
                        "on_release": lambda txt=text: on_press(txt),
                        "markup": True
                    })
            if not self.dropdown.parent:
                self.dropdown.open()
        else:
            self.dropdown.dismiss()


class OptionsCreator(ThemedApp):
    base_title: str = "Archipelago Options Creator"
    container: ContainerLayout
    main_layout: MainLayout
    scrollbox: ScrollBox
    main_panel: MainLayout
    player_options: MainLayout
    option_layout: MainLayout
    name_input: ResizableTextField
    game_label: MDLabel
    current_game: str
    options: typing.Dict[str, typing.Any]

    def __init__(self):
        self.title = self.base_title + " " + Utils.__version__
        self.icon = r"data/icon.png"
        self.current_game = ""
        self.options = {}
        super().__init__()

    def export_options(self, button: Widget):
        if 0 < len(self.name_input.text) < 17 and self.current_game:
            file_name = Utils.save_filename("Export Options File As...", [("YAML", ["*.yaml"])],
                                            Utils.get_file_safe_name(f"{self.name_input.text}.yaml"))
            options = {
                "name": self.name_input.text,
                "description": f"YAML generated by Archipelago {Utils.__version__}.",
                "game": self.current_game,
                self.current_game: {k: check_random(v) for k, v in self.options.items()}
            }
            try:
                with open(file_name, 'w') as f:
                    f.write(Utils.dump(options, sort_keys=False))
                    f.close()
                    MDSnackbar(MDSnackbarText(text="File saved successfully."), y=dp(24), pos_hint={"center_x": 0.5},
                               size_hint_x=0.5).open()
            except FileNotFoundError:
                MDSnackbar(MDSnackbarText(text="Saving cancelled."), y=dp(24), pos_hint={"center_x": 0.5},
                           size_hint_x=0.5).open()
        elif not self.name_input.text:
            MDSnackbar(MDSnackbarText(text="Name must not be empty."), y=dp(24), pos_hint={"center_x": 0.5},
                       size_hint_x=0.5).open()
        elif not self.current_game:
            MDSnackbar(MDSnackbarText(text="You must select a game to play."), y=dp(24), pos_hint={"center_x": 0.5},
                       size_hint_x=0.5).open()
        else:
            MDSnackbar(MDSnackbarText(text="Name cannot be longer than 16 characters."), y=dp(24),
                       pos_hint={"center_x": 0.5}, size_hint_x=0.5).open()

    def create_range(self, option: typing.Type[Range], name: str):
        def update_text(range_box: VisualRange):
            self.options[name] = int(range_box.slider.value)
            range_box.tag.text = str(int(range_box.slider.value))
            return

        box = VisualRange(option=option, name=name)
        box.slider.bind(on_touch_move=lambda _, _1: update_text(box))
        self.options[name] = option.default
        return box

    def create_named_range(self, option: typing.Type[NamedRange], name: str):
        def set_to_custom(range_box: VisualNamedRange):
            if (not self.options[name] == range_box.range.slider.value) \
                    and (not self.options[name] in option.special_range_names or
                         range_box.range.slider.value != option.special_range_names[self.options[name]]):
                # we should validate the touch here,
                # but this is much cheaper
                self.options[name] = int(range_box.range.slider.value)
                range_box.range.tag.text = str(int(range_box.range.slider.value))
                set_button_text(range_box.choice, "Custom")

        def set_button_text(button: MDButton, text: str):
            button.text.text = text

        def set_value(text: str, range_box: VisualNamedRange):
            range_box.range.slider.value = min(max(option.special_range_names[text.lower()], option.range_start),
                                               option.range_end)
            range_box.range.tag.text = str(int(range_box.range.slider.value))
            set_button_text(range_box.choice, text)
            self.options[name] = text.lower()
            range_box.range.slider.dropdown.dismiss()

        def open_dropdown(button):
            # for some reason this fixes an issue causing some to not open
            box.range.slider.dropdown.open()

        box = VisualNamedRange(option=option, name=name, range_widget=self.create_range(option, name))
        box.range.slider.bind(on_touch_move=lambda _, _2: set_to_custom(box))
        items = [
            {
                "text": choice.title(),
                "on_release": lambda text=choice.title(): set_value(text, box)
            }
            for choice in option.special_range_names
        ]
        box.range.slider.dropdown = MDDropdownMenu(caller=box.choice, items=items)
        box.choice.bind(on_release=open_dropdown)
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

        def open_dropdown(button):
            # for some reason this fixes an issue causing some to not open
            dropdown.open()

        default_random = option.default == "random"
        main_button = VisualChoice(option=option, name=name)
        main_button.bind(on_release=open_dropdown)

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

    def create_popup(self, option: typing.Type[OptionList] | typing.Type[OptionSet] | typing.Type[OptionCounter],
                     name: str, world: typing.Type[World]):

        valid_keys = sorted(option.valid_keys)
        if option.verify_item_name:
            valid_keys += list(world.item_name_to_id.keys())
        if option.verify_location_name:
            valid_keys += list(world.location_name_to_id.keys())

        if not issubclass(option, OptionCounter):
            def apply_changes(button):
                self.options[name].clear()
                for list_item in dialog.scrollbox.layout.children:
                    self.options[name].append(getattr(list_item.text, "text"))
                dialog.dismiss()
        else:
            def apply_changes(button):
                self.options[name].clear()
                for list_item in dialog.scrollbox.layout.children:
                    self.options[name][getattr(list_item.text, "text")] = int(getattr(list_item.value, "text"))
                dialog.dismiss()

        dialog = VisualListSetCounter(option=option, name=name, valid_keys=valid_keys)
        dialog.ids.container.spacing = dp(30)
        dialog.scrollbox.layout.theme_bg_color = "Custom"
        dialog.scrollbox.layout.md_bg_color = self.theme_cls.surfaceContainerLowColor
        dialog.scrollbox.layout.spacing = dp(5)
        dialog.scrollbox.layout.padding = [0, dp(5), 0, 0]

        if name not in self.options:
            # convert from non-mutable to mutable
            # We use list syntax even for sets, set behavior is enforced through GUI
            if issubclass(option, OptionCounter):
                self.options[name] = deepcopy(option.default)
            else:
                self.options[name] = sorted(option.default)

        if issubclass(option, OptionCounter):
            for value in sorted(self.options[name]):
                dialog.add_set_item(value, self.options[name].get(value, None))
        else:
            for value in sorted(self.options[name]):
                dialog.add_set_item(value)

        dialog.save.bind(on_release=apply_changes)
        dialog.open()

    def create_option_set_list_counter(self, option: typing.Type[OptionList] | typing.Type[OptionSet] |
                                       typing.Type[OptionCounter], name: str, world: typing.Type[World]):
        main_button = MDButton(MDButtonText(text="Edit"), on_release=lambda x: self.create_popup(option, name, world))
        return main_button

    def create_option(self, option: typing.Type[Option], name: str, world: typing.Type[World]) -> Widget:
        option_base = MDBoxLayout(orientation="vertical", size_hint_y=None, padding=[0, 0, dp(5), dp(5)])

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
        elif any(issubclass(option, cls) for cls in (OptionSet, OptionList, OptionCounter)):
            option_base.add_widget(self.create_option_set_list_counter(option, name, world))
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

    def create_options_panel(self, world_button: WorldButton):
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
                MDSnackbar(MDSnackbarText(text="Launching in default browser..."), y=dp(24), pos_hint={"center_x": 0.5},
                           size_hint_x=0.5).open()
                world_button.state = "normal"
            else:
                # attach onto archipelago.gg and see if we pass
                new_url = "https://archipelago.gg/" + cls.web.options_page
                if validate_url(new_url):
                    webbrowser.open(new_url)
                    MDSnackbar(MDSnackbarText(text="Launching in default browser..."), y=dp(24),
                               pos_hint={"center_x": 0.5},
                               size_hint_x=0.5).open()
                else:
                    MDSnackbar(MDSnackbarText(text="Invalid options page, please report to world developer."), y=dp(24),
                               pos_hint={"center_x": 0.5},
                               size_hint_x=0.5).open()
                world_button.state = "normal"
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
                if not options:
                    continue  # Game Options can be empty if every other option is in another group
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

    @staticmethod
    def tap_expansion_chevron(panel: MDExpansionPanel, chevron: TrailingPressedIconButton | MDListItem):
        if isinstance(chevron, MDListItem):
            chevron = next((child for child in chevron.ids.trailing_container.children
                            if isinstance(child, TrailingPressedIconButton)), None)
        panel.open() if not panel.is_open else panel.close()
        if chevron:
            panel.set_chevron_down(
                chevron
            ) if not panel.is_open else panel.set_chevron_up(chevron)

    def build(self):
        self.set_colors()
        self.options = {}
        self.container = Builder.load_file(Utils.local_path("data/optionscreator.kv"))
        self.root = self.container
        self.main_layout = self.container.ids.main
        self.scrollbox = self.container.ids.scrollbox

        def world_button_action(world_btn: WorldButton):
            if self.current_game != world_btn.world_cls.game:
                old_button = next((button for button in self.scrollbox.layout.children
                                   if button.world_cls.game == self.current_game), None)
                if old_button:
                    old_button.state = "normal"
            else:
                world_btn.state = "down"
            self.create_options_panel(world_btn)

        for world, cls in sorted(AutoWorldRegister.world_types.items(), key=lambda x: x[0]):
            if world == "Archipelago":
                continue
            world_text = MDButtonText(text=world, size_hint_y=None, width=dp(150),
                                      pos_hint={"x": 0.03, "center_y": 0.5})
            world_text.text_size = (world_text.width, None)
            world_text.bind(width=lambda *x, text=world_text: text.setter('text_size')(text, (text.width, None)),
                            texture_size=lambda *x, text=world_text: text.setter("height")(text,
                                                                                           world_text.texture_size[1]))
            world_button = WorldButton(world_text, size_hint_x=None, width=dp(150), theme_width="Custom",
                                       radius=(dp(5), dp(5), dp(5), dp(5)))
            world_button.bind(on_release=world_button_action)
            world_button.world_cls = cls
            self.scrollbox.layout.add_widget(world_button)
        self.main_panel = self.container.ids.player_layout
        self.player_options = self.container.ids.player_options
        self.game_label = self.container.ids.game
        self.name_input = self.container.ids.player_name
        self.option_layout = self.container.ids.options

        def set_height(instance, value):
            instance.height = value[1]

        self.game_label.bind(texture_size=set_height)

        # Uncomment to re-enable the Kivy console/live editor
        # Ctrl-E to enable it, make sure numlock/capslock is disabled
        # from kivy.modules.console import create_console
        # from kivy.core.window import Window
        # create_console(Window, self.container)

        return self.container


def launch():
    OptionsCreator().run()


if __name__ == "__main__":
    Utils.init_logging("OptionsCreator")
    launch()
