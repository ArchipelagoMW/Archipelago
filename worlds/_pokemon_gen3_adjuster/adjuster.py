import argparse
import logging
import os
import typing

from Utils import local_path, persistent_store, get_adjuster_settings, get_adjuster_settings_no_defaults, \
    data_to_bps_patch, open_image_secure, open_filename, open_directory
from .adjuster_patcher import get_patch_from_sprite_pack, extract_palette_from_file, \
    validate_sprite_pack, get_pokemon_data, stringify_pokemon_data, destringify_pokemon_data, \
    validate_pokemon_data_string, stringify_move_pool, destringify_move_pool, keep_different_pokemon_data, \
    handle_address_collection, find_folder_object_info, load_constants
from .adjuster_patcher import extract_sprites as extract_sprites_internal
from .adjuster_constants import POKEMON_TYPES, POKEMON_FOLDERS, POKEMON_ABILITIES, POKEMON_GENDER_RATIOS, \
    REVERSE_POKEMON_GENDER_RATIOS
from argparse import Namespace

# Try to import the Pokemon Emerald and Pokemon Firered/Leafgreen data
try:
    from worlds.pokemon_emerald.adjuster_constants import EMERALD_PATCH_EXTENSIONS
    emerald_support = True
except ModuleNotFoundError:
    from .adjuster_constants_emerald_fallback import EMERALD_PATCH_EXTENSIONS
    emerald_support = False
try:
    from worlds.pokemon_frlg.adjuster_constants import FR_LG_PATCH_EXTENSIONS
    frlg_support = True
except ModuleNotFoundError:
    from .adjuster_constants_frlg_fallback import FR_LG_PATCH_EXTENSIONS
    frlg_support = False

logger = logging.getLogger("PokemonGen3Adjuster")
opts = Namespace()
adjuster_name = "Gen 3" if frlg_support and emerald_support \
    else "Emerald" if emerald_support \
    else "Firered/Leafgreen" if frlg_support \
    else "No-Goal"

GAME_GEN3_ADJUSTER = "Pokemon Gen 3 Adjuster"

def run_kivy_gui() -> None:
    from bps.apply import apply_to_bytearrays as apply_bps_patch

    from kvui import KivyJSONtoTextParser, ResizableTextField, ThemedApp

    from kivy.clock import Clock
    from kivy.factory import Factory
    from kivy.graphics.context_instructions import Color
    from kivy.graphics.vertex_instructions import Rectangle
    from kivy.properties import ObjectProperty, BoundedNumericProperty, StringProperty, ListProperty
    from kivy.uix.image import AsyncImage
    from kivy.uix.layout import Layout
    from kivy.uix.popup import Popup
    from kivy.uix.textinput import TextInput
    from kivy.uix.widget import Widget
    from kivymd.uix.behaviors import StencilBehavior
    from kivymd.uix.button import MDButton, MDButtonText
    from kivymd.uix.card import MDCard
    from kivymd.uix.fitimage import FitImage
    from kivymd.uix.selectioncontrol.selectioncontrol import MDCheckbox
    from kivymd.uix.label import MDLabel
    from kivymd.uix.menu import MDDropdownMenu
    from kivymd.uix.tooltip import MDTooltip
    from kivymd.uix.widget import MDWidget
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivymd.uix.floatlayout import MDFloatLayout
    from kivymd.uix.gridlayout import MDGridLayout


    # Miscellaneaous objects
    class Spinbox(ResizableTextField):
        min: int = 1
        max: int = 255
        val: int

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.val = BoundedNumericProperty(self.min, min=self.min, max=self.max,
                                              errorhandler=lambda x: self.max if x > self.max else self.min)
            self.text = str(self.val)

        def increment(self):
            self.text = min(int(self.text) + 1, self.max)

        def decrement(self):
            self.text = max(int(self.text) - 1, self.min)

        def on_text(self, _, value: str):
            self.val = int(value) if value.isdigit() else self.val


    class AutocompleteInput(ResizableTextField):
        items: list[str] = ListProperty([])

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            self.dropdown = MDDropdownMenu(caller=self, position="bottom", border_margin=8, width=self.width)
            self.bind(width=lambda _, x: setattr(self.dropdown, "width", x))
            self.bind(items=lambda s, _: self.on_text(s, self.text))

        def on_focus(self, _, value):
            if value:
                self.on_text(None, self.text)
            else:
                self.dropdown.dismiss()

        def on_text(self, _, value):
            self.dropdown.items.clear()
            value = value.title()

            def on_press(text):
                self.text = text
                self.dropdown.dismiss()
                self.focus = True

            for item_name in self.items:
                if item_name.startswith(value):
                    self.dropdown.items.append({
                        "text": item_name,
                        "on_release": lambda txt=item_name: on_press(txt),
                    })
            if not self.dropdown.parent and self.focus:
                self.dropdown.open()


    class CheckItem(MDBoxLayout):
        checkbox: MDCheckbox = ObjectProperty()
        text: str = StringProperty("")


    class TooltipMDLabel(MDTooltip, MDLabel):
        tooltip_text: str = StringProperty("")


    class FitImageTop(MDBoxLayout, StencilBehavior):
        source = ObjectProperty()
        _container = ObjectProperty()

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            Clock.schedule_once(self._late_init)

        def _late_init(self, *_):
            self._container = FitImageTopContainer(self.source, False)
            self.bind(source=self._container.setter("source"))
            self.add_widget(self._container)

        def reload(self):
            self._container.image.reload()


    class FitImageTopContainer(Widget):
        source = ObjectProperty()
        image = ObjectProperty()
        halved: bool = False

        def __init__(self, source, mipmap, **kwargs):
            super().__init__(**kwargs)
            self.image = AsyncImage(mipmap=mipmap)
            self.loader_clock = Clock.schedule_interval(self.adjust_size, self.image.anim_delay)
            self.image.bind(
                on_load=lambda _: (
                    self.adjust_size(),
                    self.loader_clock.cancel(),
                )
            )
            self.source = source
            self.bind(size=self.adjust_size, pos=self.adjust_size)

        def on_source(self, _, value):
            if isinstance(value, str):
                self.image.source = value
            else:
                self.image.texture = value
            self.adjust_size()

        def adjust_size(self, *args):
            if not self.parent or not self.image.texture:
                return
            self.image.texture.mag_filter = "nearest"

            (par_x, par_y) = self.parent.size

            if par_x == 0 or par_y == 0:
                with self.canvas:
                    self.canvas.clear()
                return

            par_scale = par_x / par_y
            (img_x, img_y) = self.image.texture.size
            img_scale = img_x / img_y

            # Don't squish tall images too much in case of overworld sprites
            if img_x == 16 and not self.halved:
                self.halved = True
                self.parent.width /= 2
                return
            if img_x != 16 and self.halved:
                self.halved = False
                self.parent.width *= 2
                return

            if par_scale > img_scale:
                (img_x_new, img_y_new) = (img_x, img_x / par_scale)
            else:
                (img_x_new, img_y_new) = (img_y * par_scale, img_y)

            subtexture = self.image.texture.get_region(0, img_y - img_y_new, img_x_new, img_y_new)
            with self.canvas:
                self.canvas.clear()
                Color(1, 1, 1)
                Rectangle(texture=subtexture, pos=self.pos, size=(par_x, par_y))


    class InfoPopup(Popup):
        popup_contents: MDBoxLayout = ObjectProperty()
        popup_text: str = StringProperty("Popup text")
        button_text: str = StringProperty("OK")

        def open(self, _title="Title", _text="Popup text", _button_text="OK"):
            self.title = _title
            self.popup_text = _text
            self.button_text = _button_text
            super().open(self)


    # Actual useful objects
    class PatchFrame(MDBoxLayout):
        label: MDLabel = ObjectProperty()
        entry: ResizableTextField = ObjectProperty()
        select_button: MDButton = ObjectProperty()
        is_ap_checkbox: CheckItem = ObjectProperty()

        rom_version: str = "Unknown"
        object_folders: list[str] = POKEMON_FOLDERS
        is_patch_valid: bool = False

        def late_init(self):
            self.entry.bind(text=self.update_patch)
            hide_widget(self.is_ap_checkbox)

        def select_patch(self, _forced_patch: str = None):
            # Run when we ask for the user to select a ROM or patch file,
            # or when the ROM or patch file needs to be reloaded
            if _forced_patch is not None:
                patch = _forced_patch
            else:
                title = f"Select a Pokemon {adjuster_name} ROM or patch file."
                old_patch_folder: str = os.path.dirname(opts.patch) if self.is_patch_valid else None
                patch = open_filename(title, [("Rom & Patch Files", app.adjuster_extensions)], old_patch_folder) or ""
            self.entry.text = patch or ""

        def update_patch(self, _, _patch: str):
            self.rom_version = "Unknown"
            if _patch:
                if emerald_support:
                    _patch, self.rom_version = self.emerald_fetch_patch(_patch)
                if frlg_support and self.rom_version == "Unknown":
                    _patch, self.rom_version = self.frlg_fetch_patch(_patch)
                if self.rom_version == "Unknown" and not self.entry.focus:
                    Factory.InfoPopup().open("Error while loading a ROM",
                                             f"The ROM at path\n{_patch}\nisn't a valid Pokemon {adjuster_name} ROM!")

            opts.patch = _patch

            self.is_patch_valid = self.rom_version != "Unknown" and os.path.exists(_patch)
            if self.is_patch_valid:
                load_constants(self.rom_version)
            app.top_frame.try_validate_sprite_pack(opts.sprite_pack, True)
            colors = KivyJSONtoTextParser.TextColors()
            if not self.is_patch_valid:
                # If the patch is invalid, hide the isAP checkbox, the Sprite Extractor
                # and the data edition window if it's displayed
                hide_widget(self.is_ap_checkbox)
                hide_widget(app.sprite_extractor)
                self.entry.text_color_normal = colors.red
                self.entry.text_color_focus = colors.red
            else:
                trainer_folder_object_info = find_folder_object_info("trainer")
                players_folder_object_info = find_folder_object_info("players")
                pokemon_folder_object_info = find_folder_object_info("pokemon")
                self.object_folders = trainer_folder_object_info["folders"] + players_folder_object_info["folders"] \
                    + pokemon_folder_object_info["folders"]
                if app.top_frame.sprite_pack_frame.is_sprite_pack_valid:
                    app.sprite_preview.detect_existing_folders(opts.sprite_pack)
                app.sprite_extractor.update_sprite_extraction(self, "")

                # If the patch is valid, show the isAP checkbox, the Sprite Extractor
                # and the data edition window if it's displayed
                show_widget(self.is_ap_checkbox)
                show_widget(app.sprite_extractor, 2 if app.sprite_preview.parent is not None else 1)
                app.sprite_extractor.input.items = self.object_folders
                self.entry.text_color_normal = colors.white
                self.entry.text_color_focus = colors.white
            app.sprite_preview.update_graphics()

        def emerald_fetch_patch(self, _patch: str) -> tuple[str, str]:
            # Asks for a ROM or patch file then validates it
            # Handles the check for Pokemon Emerald
            if _patch and os.path.exists(_patch):
                if os.path.splitext(_patch)[-1] == ".gba":
                    # If .gba, verify ROM integrity by checking for its internal name at addresses #0000A0-#0000AB
                    with open(_patch, "rb") as stream:
                        rom_data = bytearray(stream.read())
                        internal_name = rom_data[0xA0:0xAC].decode("utf-8")
                        if internal_name == "POKEMON EMER":
                            return _patch, "Emerald"
                elif os.path.splitext(_patch)[-1] == ".apemerald":
                    return _patch, "Emerald"
            return _patch, "Unknown"

        def frlg_fetch_patch(self, _patch: str) -> tuple[str, str]:
            # Asks for a ROM or patch file then validates it
            # Handles the check for Pokemon Firered/Leafgreen
            if _patch and os.path.exists(_patch):
                if os.path.splitext(_patch)[-1] == ".gba":
                    # If .gba, verify ROM integrity by checking for its internal name at addresses #0000A0-#0000AB
                    with open(_patch, "rb") as stream:
                        rom_data = bytearray(stream.read())
                        return _patch, app.frlg_get_rom_version(rom_data)
                elif os.path.splitext(_patch)[-1] in [".apfirered", ".apleafgreen"]:
                    # If .apfirered or .apleafgreen, patch the ROM to fetch its revision number
                    patch_data = app.frlg_build_ap_rom(_patch)
                    return _patch, app.frlg_get_rom_version(patch_data)
            return _patch, "Unknown"


    class SpritePackFrame(MDBoxLayout):
        label: MDLabel = ObjectProperty()
        entry: ResizableTextField = ObjectProperty()
        select_button: MDButton = ObjectProperty()

        is_sprite_pack_valid: bool = False

        def late_init(self):
            self.entry.bind(text=self.update_sprite_pack)

        def reload_pack(self):
            self.update_sprite_pack(self, self.entry.text)

        def select_sprite_pack(self, _forced_sprite_pack: str = None):
            # Run when we ask for the user to select a sprite pack,
            # or when the sprite pack needs to be reloaded
            if _forced_sprite_pack is not None:
                sprite_pack = _forced_sprite_pack
            else:
                old_sprite_pack_folder: str = opts.sprite_pack if self.is_sprite_pack_valid else None
                sprite_pack = open_directory("Choose a sprite pack.", old_sprite_pack_folder)
            self.entry.text = sprite_pack or ""

        def update_sprite_pack(self, _, _sprite_pack: str):
            opts.sprite_pack = _sprite_pack

            self.is_sprite_pack_valid = _sprite_pack is not None and os.path.isdir(_sprite_pack)
            app.top_frame.try_validate_sprite_pack(opts.sprite_pack)
            colors = KivyJSONtoTextParser.TextColors()
            if not self.is_sprite_pack_valid:
                # If the sprite pack is invalid, do not show the Sprite Preview
                hide_widget(app.sprite_preview)
                app.sprite_preview.existing_folders = []
                self.entry.text_color_normal = colors.red
                self.entry.text_color_focus = colors.red
            else:
                # If the sprite pack is valid, show the Sprite Preview
                show_widget(app.sprite_preview, 1)
                app.sprite_preview.detect_existing_folders(_sprite_pack)
                self.entry.text_color_normal = colors.white
                self.entry.text_color_focus = colors.white
            app.sprite_preview.update_graphics()


    class TopFrame(MDCard):
        patch_frame: PatchFrame = ObjectProperty()
        sprite_pack_frame: SpritePackFrame = ObjectProperty()

        def late_init(self):
            self.patch_frame.late_init()
            self.sprite_pack_frame.late_init()

        def try_validate_sprite_pack(self, _sprite_pack: str, _patch_changed=False):
            # Validates the sprite pack if both the ROM/patch file and the sprite packs are valid
            has_error = False
            if self.patch_frame.is_patch_valid:
                app.ap_rom = app.ap_rom if not _patch_changed else app.build_ap_rom(opts.patch)
                if not app.ap_rom:
                    app.sprite_preview.error_label.text = "Could not build the AP ROM."
                    return
                is_rom_ap_state = handle_address_collection(app.ap_rom, app.top_frame.patch_frame.rom_version,
                                                            None if _patch_changed else
                                                            self.patch_frame.is_ap_checkbox.checkbox.active)
                if _patch_changed:
                    # Change the state of the isAP button automatically when a new patch is loaded
                    self.patch_frame.is_ap_checkbox.checkbox.active = is_rom_ap_state
                    self.patch_frame.is_ap_checkbox.checkbox.disabled = not opts.patch.endswith(".gba")
            if self.patch_frame.is_patch_valid and self.sprite_pack_frame.is_sprite_pack_valid:
                errors, has_error = validate_sprite_pack(_sprite_pack)
                app.bottom_frame.adjust_rom.disabled = has_error
                app.sprite_preview.error_label.text = errors or "No anomaly detected! The sprite pack is valid."
            else:
                app.bottom_frame.adjust_rom.disabled = True
                app.sprite_preview.error_label.text = \
                    "Both a sprite pack and a patch/ROM must\nbe selected to validate the sprite pack."


    class SpriteExtractorFrame(MDCard):
        input: AutocompleteInput = ObjectProperty()
        extract_button: MDButton = ObjectProperty()
        extract_all_button: MDButton = ObjectProperty()

        def late_init(self):
            self.extract_button.disabled = True
            self.input.bind(text=self.update_sprite_extraction)

        def update_sprite_extraction(self, _, _value: str = "Shouldnotbewritten"):
            # Enables or disables the sprite extraction button if the sprite's name is valid or not
            text = _value if _value != "Shouldnotbewritten" else self.input.text
            self.extract_button.disabled = text not in app.top_frame.patch_frame.object_folders
            colors = KivyJSONtoTextParser.TextColors()
            self.input.fill_color_normal = colors.red if self.extract_button.disabled else colors.white
            self.input.fill_color_focus = colors.red if self.extract_button.disabled else colors.white

        def extract_sprites(self):
            # Run when the Extract button is pressed
            # Extract all the sprites from the given Pokemon or Trainer into the given folder
            if self.input.text not in app.top_frame.patch_frame.object_folders:
                return

            base_folder_path: str = ""
            if app.top_frame.sprite_pack_frame.is_sprite_pack_valid:
                base_folder_path = opts.sprite_pack
            output_folder = open_directory("Select a folder to extract the sprites to.", base_folder_path)
            if not output_folder:
                return
            if not os.path.isdir(output_folder):
                os.makedirs(output_folder)

            handle_address_collection(app.ap_rom, app.top_frame.patch_frame.rom_version,
                                      app.top_frame.patch_frame.is_ap_checkbox.checkbox.active)
            extract_sprites_internal(self.input.text, output_folder)
            Factory.InfoPopup().open("Successful Sprite Extraction",
                                     f"All sprites for {self.input.text}\nhave successfully been extracted!")

        def extract_all_sprites(self):
            # Run when the Extract All button is pressed
            # Extract all the sprites from all Pokemons and Trainers into the given folder
            base_folder_path: str = None
            if app.top_frame.sprite_pack_frame.is_sprite_pack_valid:
                base_folder_path = opts.sprite_pack
            output_folder = open_directory("Select a folder to extract all sprites to.", base_folder_path)
            if not output_folder:
                return
            if not os.path.isdir(output_folder):
                os.makedirs(output_folder)

            handle_address_collection(app.ap_rom, app.top_frame.patch_frame.rom_version,
                                      app.top_frame.patch_frame.is_ap_checkbox.checkbox.active)
            for object in app.top_frame.patch_frame.object_folders:
                # Extract each Pokemon and Trainer into subfolders
                current_output = os.path.join(output_folder, object)
                if not os.path.isdir(current_output):
                    os.makedirs(current_output)
                extract_sprites_internal(object, current_output)
            Factory.InfoPopup().open("Successful Sprite Extraction", "All sprites have successfully been extracted!")


    class PokemonDataEditorFrame(MDBoxLayout):
        hp_input: Spinbox = ObjectProperty()
        hp_label: MDLabel = ObjectProperty()
        spd_input: Spinbox = ObjectProperty()
        spd_label: MDLabel = ObjectProperty()
        atk_input: Spinbox = ObjectProperty()
        atk_label: MDLabel = ObjectProperty()
        def_input: Spinbox = ObjectProperty()
        def_label: MDLabel = ObjectProperty()
        spatk_input: Spinbox = ObjectProperty()
        spatk_label: MDLabel = ObjectProperty()
        spdef_input: Spinbox = ObjectProperty()
        spdef_label: MDLabel = ObjectProperty()
        move_pool_input: TextInput = ObjectProperty()
        move_pool_label: MDLabel = ObjectProperty()
        type_1_button: MDButton = ObjectProperty()
        type_1_input: MDButtonText = ObjectProperty()
        type_1_label: MDLabel = ObjectProperty()
        type_1_dropdown: MDDropdownMenu
        type_2_button: MDButton = ObjectProperty()
        type_2_input: MDButtonText = ObjectProperty()
        type_2_label: MDLabel = ObjectProperty()
        type_2_dropdown: MDDropdownMenu
        ability_1_input: AutocompleteInput = ObjectProperty()
        ability_1_label: MDLabel = ObjectProperty()
        ability_2_input: AutocompleteInput = ObjectProperty()
        ability_2_label: MDLabel = ObjectProperty()
        gender_ratio_button: MDButton = ObjectProperty()
        gender_ratio_input: MDButtonText = ObjectProperty()
        gender_ratio_label: MDLabel = ObjectProperty()
        gender_ratio_dropdown: MDDropdownMenu
        forbid_flip_input: MDCheckbox = ObjectProperty()
        forbid_flip_label: MDLabel = ObjectProperty()
        save_data: MDButton = ObjectProperty()
        save_data_text: MDButtonText = ObjectProperty()

        hp_tooltip = "This value changes the Pokemon's base HP.\nAwaits a value between 1 and 255."
        spd_tooltip = "This value changes the Pokemon's base Speed.\nAwaits a value between 1 and 255."
        atk_tooltip = "This value changes the Pokemon's base Attack.\nAwaits a value between 1 and 255."
        def_tooltip = "This value changes the Pokemon's base Defense.\nAwaits a value between 1 and 255."
        spatk_tooltip = "This value changes the Pokemon's base Special Attack.\nAwaits a value between 1 and 255."
        spdef_tooltip = "This value changes the Pokemon's base Special Defense.\nAwaits a value between 1 and 255."
        type_1_tooltip = "This value changes the Pokemon's first type."
        type_2_tooltip = "This value changes the Pokemon's second type.\n"\
                         + "Make it match the first type if you want the Pokemon to only have one type."
        ability_1_tooltip = "This value changes the Pokemon's first ability."
        ability_2_tooltip = "This value changes the Pokemon's second ability.\n"\
                            + "Make it match the first ability if you want the Pokemon to only have one ability."
        gender_ratio_tooltip = "This value changes the Pokemon's gender ratio."
        forbid_flip_tooltip = "This value dictates whether the Pokemon's sprite can be flipped or not.\n"\
                              + "The sprite is flipped when looking at a Pokemon's status screen in your team."
        move_pool_tooltip = "This value contains the Pokemon's levelup learnset.\nEach line must contain a move.\n"\
                            + "Each move must be written in the format \"<move>: <level>\".\n"\
                            + "With <move> being a known Pokemon move from this generation.\n"\
                            + "And with <level> being a number between 1 and 100."

        green_tooltip = "This label is green because this value is different from the one within the ROM."
        bold_tooltip = "This label is in bold because this value has been changed and hasn't been saved."

        valid_field_values = {
            "hp": True,
            "spd": True,
            "atk": True,
            "def": True,
            "spatk": True,
            "spdef": True,
            "ability1": True,
            "ability2": True,
            "movePool": True
        }
        changed_field_values = {k: False for k, _ in valid_field_values.items()}

        pokemon_rom_data: dict[str, int | list[dict[str, str | int]]] = None
        pokemon_saved_data: dict[str, int | list[dict[str, str | int]]] = None

        def late_init(self):
            self.md_bg_color = app.theme_cls.backgroundColor

            self.ability_1_input.items = list(map(lambda a: a.title(), POKEMON_ABILITIES))
            self.ability_2_input.items = list(map(lambda a: a.title(), POKEMON_ABILITIES))

            def on_press_type_1(text):
                self.type_1_input.text = text
                self.type_1_dropdown.dismiss()
                self.type_1_input.focus = True

            def on_press_type_2(text):
                self.type_2_input.text = text
                self.type_2_dropdown.dismiss()
                self.type_2_input.focus = True

            def on_press_gender_ratio(text):
                self.gender_ratio_input.text = text
                self.gender_ratio_dropdown.dismiss()
                self.gender_ratio_input.focus = True

            # Dropdowns for the Type 1 and Type 2 fields
            self.type_1_dropdown = MDDropdownMenu(caller=self.type_1_button, position="bottom", border_margin=8,
                                                  width=self.type_1_button.width)
            self.type_2_dropdown = MDDropdownMenu(caller=self.type_2_button, position="bottom", border_margin=8,
                                                  width=self.type_2_button.width)
            for pokemon_type in POKEMON_TYPES:
                self.type_1_dropdown.items.append({
                    "text": pokemon_type,
                    "on_release": lambda txt=pokemon_type: on_press_type_1(txt),
                })
                self.type_2_dropdown.items.append({
                    "text": pokemon_type,
                    "on_release": lambda txt=pokemon_type: on_press_type_2(txt),
                })
            self.type_1_button.bind(on_press=lambda _: self.type_1_dropdown.open())
            self.type_2_button.bind(on_press=lambda _: self.type_2_dropdown.open())

            # Dropdown for the Gender Ratio field
            self.gender_ratio_dropdown = MDDropdownMenu(caller=self.gender_ratio_button, position="bottom",
                                                        border_margin=8, width=self.gender_ratio_button.width)
            for _, gender_ratio in POKEMON_GENDER_RATIOS.items():
                self.gender_ratio_dropdown.items.append({
                    "text": gender_ratio,
                    "on_release": lambda txt=gender_ratio: on_press_gender_ratio(txt),
                })
            self.gender_ratio_button.bind(on_press=lambda _: self.gender_ratio_dropdown.open())

        def update_field_validity(self, _field_name: str, _value: bool):
            # Disables the Pokemon data saving button if any data is erroneous
            self.valid_field_values[_field_name] = _value
            any_value_invalid = list(k for k, v in self.valid_field_values.items() if not v)
            self.save_data.disabled = len(any_value_invalid) > 0

        def update_field_change(self, _field_name: str, _value: bool):
            # Displays the Pokemon data saving button's text in bold if any data has been changed
            self.changed_field_values[_field_name] = _value
            any_value_changed = list(k for k, v in self.changed_field_values.items() if v)
            self.save_data_text.bold = len(any_value_changed) > 0

        def check_value(self, _field_object: ObjectProperty, _label: TooltipMDLabel, _field: str, _tooltip: str):
            # Checks if a given Pokemon data value is valid or if it has been changed
            # And updates its label's color and font in consequence
            # Red if invalid, blue if different from the ROM, bold if different from the saved data
            field_value = ""
            if hasattr(_field_object, "active"):
                field_value = "1" if _field_object.active else "0"
            else:
                field_value = _field_object.text
            errors, has_error = validate_pokemon_data_string(app.sprite_preview.folder_input.text,
                                                             {_field: field_value})
            temp_pokemon_data_string = f"{_field}: {field_value.replace(chr(10), ', ')}"
            is_different_from_rom = True
            is_different_from_data = False
            internal_field = "dex" if _field == "forbid_flip" else _field
            if not has_error:
                temp_pokemon_data = destringify_pokemon_data(app.sprite_preview.sprite_input.text,
                                                             temp_pokemon_data_string)
                if "dex" in list(temp_pokemon_data.keys()):
                    temp_pokemon_data["dex"] = (temp_pokemon_data["dex"] << 7) + (self.pokemon_rom_data["dex"] % 0x80)
                different_pokemon_data = keep_different_pokemon_data(self.pokemon_rom_data, temp_pokemon_data)
                is_different_from_rom = internal_field in list(different_pokemon_data.keys())
                if self.pokemon_saved_data and internal_field in list(self.pokemon_saved_data.keys()):
                    different_pokemon_data = keep_different_pokemon_data(self.pokemon_saved_data, temp_pokemon_data)
                    is_different_from_data = internal_field in list(different_pokemon_data.keys())
                else:
                    is_different_from_data = is_different_from_rom

            colors = KivyJSONtoTextParser.TextColors()
            _label.text_color = colors.red if has_error else colors.green if is_different_from_rom else colors.blue
            _label.bold = is_different_from_data
            full_tooltip = _tooltip \
                + (f"\n{errors}" if has_error else f"\n{self.green_tooltip}" if is_different_from_rom else "") \
                + (f"\n{self.bold_tooltip}" if is_different_from_data else "")
            _label.tooltip_text = full_tooltip
            self.update_field_validity(_field, not has_error)
            self.update_field_change(_field, is_different_from_data)

        def fill_in_fields(self, _folder: str):
            # Fills in the fields in the data editor and check their validity
            data_folder = "Unown A" if _folder.startswith("Unown ") else _folder
            # Fill in data editor fields
            self.pokemon_rom_data = get_pokemon_data(data_folder)
            pokemon_data = self.pokemon_rom_data.copy()
            self.pokemon_saved_data = None
            pokemon_saved_data_path = os.path.join(opts.sprite_pack, data_folder, "data.txt")
            if os.path.exists(pokemon_saved_data_path):
                # Load local data if it exists and replace the fields' values
                with open(pokemon_saved_data_path) as pokemonSavedDataFile:
                    pokemon_saved_data_string = pokemonSavedDataFile.read()
                pokemon_saved_data_errors, pokemon_saved_data_has_error =\
                    validate_pokemon_data_string(_folder, pokemon_saved_data_string)
                if pokemon_saved_data_has_error:
                    Factory.InfoPopup().open("Error while loading Pokemon data",
                                            pokemon_saved_data_errors)
                else:
                    self.pokemon_saved_data = destringify_pokemon_data(data_folder, pokemon_saved_data_string)
                    for field in self.pokemon_saved_data:
                        if field == "dex":
                            pokemon_data[field] = self.pokemon_saved_data[field] = \
                                (self.pokemon_saved_data[field] << 7) + (pokemon_data[field] % 0x80)
                        else:
                            pokemon_data[field] = self.pokemon_saved_data[field]

            self.hp_input.text = str(pokemon_data["hp"])
            self.spd_input.text = str(pokemon_data["spd"])
            self.atk_input.text = str(pokemon_data["atk"])
            self.def_input.text = str(pokemon_data["def"])
            self.spatk_input.text = str(pokemon_data["spatk"])
            self.spdef_input.text = str(pokemon_data["spdef"])
            self.type_1_input.text = POKEMON_TYPES[pokemon_data["type1"]]
            self.type_2_input.text = POKEMON_TYPES[pokemon_data["type2"]]
            self.ability_1_input.text = POKEMON_ABILITIES[pokemon_data["ability1"]].title()
            self.ability_2_input.text = POKEMON_ABILITIES[pokemon_data["ability2"]].title() \
                if pokemon_data["ability2"] else POKEMON_ABILITIES[pokemon_data["ability1"]].title()
            self.gender_ratio_input.text = POKEMON_GENDER_RATIOS[pokemon_data["gender_ratio"]]
            self.forbid_flip_input.active = (pokemon_data["dex"] >> 7) > 0
            self.move_pool_input.text = stringify_move_pool(pokemon_data["move_pool"])

            self.check_all_fields()

        def check_all_fields(self):
            # Checks all Pokemon data values, and updates their labels
            self.check_value(self.hp_input, self.hp_label, "hp", self.hp_tooltip)
            self.check_value(self.spd_input, self.spd_label, "spd", self.spd_tooltip)
            self.check_value(self.atk_input, self.atk_label, "atk", self.atk_tooltip)
            self.check_value(self.def_input, self.def_label, "def", self.def_tooltip)
            self.check_value(self.spatk_input, self.spatk_label, "spatk", self.spatk_tooltip)
            self.check_value(self.spdef_input, self.spdef_label, "spdef", self.spdef_tooltip)
            self.check_value(self.type_1_input, self.type_1_label, "type1", self.type_1_tooltip)
            self.check_value(self.type_2_input, self.type_2_label, "type2", self.type_2_tooltip)
            self.check_value(self.ability_1_input, self.ability_1_label, "ability1", self.ability_1_tooltip)
            self.check_value(self.ability_2_input, self.ability_2_label, "ability2", self.ability_2_tooltip)
            self.check_value(self.gender_ratio_input, self.gender_ratio_label, "gender_ratio",
                             self.gender_ratio_tooltip)
            self.check_value(self.forbid_flip_input, self.forbid_flip_label, "dex", self.forbid_flip_tooltip)
            self.check_value(self.move_pool_input, self.move_pool_label, "move_pool", self.move_pool_tooltip)

        def save_pokemon_data(self):
            # Saves the Pokemon's data into the given folder's "data.txt" file
            pokemon_name = app.sprite_preview.current_sprite_folder
            if pokemon_name.startswith("Unown "):
                pokemon_name = "Unown A"
            # Build an object with all the registered data
            new_pokemon_data: dict[str, int | list[dict[str, str | int]]] = {
                "hp": int(self.hp_input.text),
                "atk": int(self.atk_input.text),
                "def": int(self.def_input.text),
                "spatk": int(self.spatk_input.text),
                "spdef": int(self.spdef_input.text),
                "spd": int(self.spd_input.text),
                "type1": POKEMON_TYPES.index(self.type_1_input.text),
                "type2": POKEMON_TYPES.index(self.type_2_input.text),
                "ability1": POKEMON_ABILITIES.index(self.ability_1_input.text.upper()),
                "ability2": POKEMON_ABILITIES.index(self.ability_2_input.text.upper())
                    or POKEMON_ABILITIES.index(self.ability_1_input.text.upper()),
                "gender_ratio": REVERSE_POKEMON_GENDER_RATIOS[self.gender_ratio_input.text],
                "dex": ((1 if self.forbid_flip_input.active else 0) << 7) + int(self.pokemon_rom_data["dex"]) % 0x80,
                "move_pool": destringify_move_pool(self.move_pool_input.text)
            }
            # Trim the data that has not been changed
            self.pokemon_saved_data = keep_different_pokemon_data(self.pokemon_rom_data, new_pokemon_data)
            self.check_all_fields()

            # Save changes to a specific data file
            pokemon_saved_data_string = stringify_pokemon_data(self.pokemon_saved_data)
            data_folder_path = os.path.join(opts.sprite_pack, pokemon_name)
            if not os.path.isdir(data_folder_path):
                os.makedirs(data_folder_path)
            data_path = os.path.join(data_folder_path, "data.txt")
            if pokemon_saved_data_string:
                with open(data_path, "w") as data_file:
                    data_file.write(pokemon_saved_data_string)
            elif os.path.exists(data_path):
                os.remove(data_path)
            app.top_frame.try_validate_sprite_pack(opts.sprite_pack)
            Factory.InfoPopup().open("Successful Pokemon Data Save",
                                     f"Data for the Pokemon {pokemon_name} has been successfully saved!")


    class SpritePreviewFrame(MDCard):
        default_image = local_path("data", "gen3_adjuster_default.png")
        current_sprite_folder: str = StringProperty("")
        existing_folders: list[str] = ListProperty([""])
        current_sprite: str = StringProperty("")
        existing_sprites: list[str] = ListProperty([""])
        palette_cells: list[MDWidget] = []

        grid: MDGridLayout = ObjectProperty()
        sprite_box: MDGridLayout = ObjectProperty()
        folder_input: AutocompleteInput = ObjectProperty()
        sprite_input: AutocompleteInput = ObjectProperty()
        data_editor_frame: PokemonDataEditorFrame = ObjectProperty()
        data_editor_error: MDLabel = ObjectProperty()
        sprite_image: FitImage = ObjectProperty()
        palette_grid: MDGridLayout = ObjectProperty()
        error_label: MDLabel = ObjectProperty()

        def late_init(self):
            for _ in range(16):
                widget = MDWidget(md_bg_color="000000")
                self.palette_grid.add_widget(widget)
                self.palette_cells.append(widget)

            self.data_editor_frame.late_init()
            self.sprite_input.disabled = True
            hide_widget(self.data_editor_frame)
            hide_widget(self.data_editor_error)
            self.bind(existing_folders=self.update_folder_list)
            self.bind(existing_sprites=self.update_sprite_list)
            self.folder_input.bind(text=self.on_text_folder_input)
            self.sprite_input.bind(text=self.on_text_sprite_input)

        def update_graphics(self):
            self.switch_sprite_folder(self.current_sprite_folder, self.current_sprite)

        def on_text_folder_input(self, _, _new_folder: str):
            # Run when the current sprite folder's value is changed
            # This only switches the current sprite folder if it's recognized
            if _new_folder.title() in app.top_frame.patch_frame.object_folders:
                folder_path = os.path.join(opts.sprite_pack, _new_folder.title())
                if not os.path.isdir(folder_path):
                    os.makedirs(folder_path)
                self.switch_sprite_folder(_new_folder, self.seek_main_sprite(_new_folder))
            else:
                self.hide_data_editor_style()
                self.hide_data_editor()
                if self.current_sprite_folder:
                    self.switch_sprite_folder("")

        def seek_main_sprite(self, _new_folder: str):
            folder_path = os.path.join(opts.sprite_pack, _new_folder.title())
            main_sprites = ["front_anim", "front", "battle_front", "battle_front_1"]
            for sprite in main_sprites:
                if os.path.exists(os.path.join(folder_path, sprite + ".png")):
                    return sprite
            return ""

        def switch_sprite_folder(self, _new_folder, _new_sprite: str = ""):
            # Run whenever the current sprite folder is changed
            # Loads the various data related to a Pokemon or Trainer, depending on the folder
            if not app.top_frame.sprite_pack_frame.is_sprite_pack_valid:
                self.hide_data_editor_style()
                self.hide_data_editor()
                self.current_sprite_folder = ""
                self.sprite_input.disabled = True
                self.sprite_input.text = ""
                self.switch_sprite("")
                return

            _new_folder = _new_folder.title()
            folder_path = os.path.join(opts.sprite_pack, _new_folder)
            if _new_folder:
                if not os.path.isdir(folder_path):
                    # Non-existent folder, reload the pack
                    self.folder_input.text = ""
                    app.top_frame.sprite_pack_frame.reload_pack()
                    return
                if _new_folder not in self.existing_folders:
                    # Folder just created, reload the pack
                    app.top_frame.sprite_pack_frame.reload_pack()
                    return

            self.current_sprite_folder = _new_folder

            # Retrieve and list valid sprites
            if app.top_frame.sprite_pack_frame.is_sprite_pack_valid and _new_folder and os.path.isdir(folder_path):
                self.detect_existing_sprites(folder_path)

            self.sprite_input.disabled = _new_folder == ""
            if self.sprite_input.text == _new_sprite:
                self.on_text_sprite_input(self, _new_sprite)
            else:
                self.sprite_input.text = _new_sprite

            colors = KivyJSONtoTextParser.TextColors()
            if _new_folder:
                self.folder_input.text_color_normal = colors.white
                self.folder_input.text_color_focus = colors.white
            else:
                self.folder_input.text_color_normal = colors.red
                self.folder_input.text_color_focus = colors.red

            self.hide_data_editor_style()
            if _new_folder not in POKEMON_FOLDERS or _new_folder == "Egg":
                # Trainer folder, do not show the Pokemon data edition frame
                self.hide_data_editor()
            else:
                # Pokemon folder, show the Pokemon data edition frame
                self.grid.cols = 2
                if not app.top_frame.patch_frame.is_patch_valid:
                    hide_widget(self.data_editor_frame)
                    show_widget(self.data_editor_error)
                    return
                show_widget(self.data_editor_frame)
                hide_widget(self.data_editor_error)
                self.grid.adaptive_size = False
                self.grid.adaptive_height = True
                self.grid.size_hint_x = 1
                self.sprite_box.size_hint_y = 1
                self.data_editor_frame.fill_in_fields(_new_folder)

        def hide_data_editor(self):
            hide_widget(self.data_editor_frame)
            hide_widget(self.data_editor_error)
            self.grid.cols = 1

        def hide_data_editor_style(self):
            # Style changes applied when hiding the data editor
            self.grid.adaptive_size = True
            self.grid.adaptive_height = False
            self.grid.size_hint_x = None
            self.sprite_box.size_hint_y = None
            self.sprite_box.height = 174

        def detect_existing_folders(self, _sprite_pack: str):
            # Detect existing object folders and list them
            existing_folders: list[str] = [""]
            for dir in os.listdir(_sprite_pack):
                if dir in app.top_frame.patch_frame.object_folders:
                    existing_folders.append(dir)
            self.existing_folders = existing_folders

        def update_folder_list(self, _, _folders: list[str]):
            self.folder_input.items = _folders
            if self.folder_input.text not in _folders:
                self.folder_input.text = ""

        def on_text_sprite_input(self, _, _new_sprite: str):
            # Run when the current sprite's value is changed
            # This only switches the current sprite if it's recognized
            self.switch_sprite(_new_sprite if _new_sprite in self.existing_sprites else "")

        def switch_sprite(self, _new_sprite: str):
            # Run whenever the current sprite is changed
            # Displays the new sprite and its palette in the adjuster
            folder_path = os.path.join(opts.sprite_pack, self.current_sprite_folder.title())
            sprite_path = os.path.join(folder_path, _new_sprite + ".png")
            if _new_sprite and (not os.path.exists(sprite_path) or _new_sprite not in self.existing_sprites):
                # Non-existent folder or sprite, reload the pack
                if not os.path.exists(folder_path):
                    app.sprite_preview.folder_input.text = ""
                else:
                    app.sprite_preview.sprite_input.text = ""
                app.top_frame.sprite_pack_frame.reload_pack()
                return

            self.current_sprite = _new_sprite

            # Display the Archipelago icon as default
            if not _new_sprite:
                sprite_path = local_path("data", "gen3_adjuster_default.png")

            if app:
                # Switch the displayed sprite
                self.sprite_image.source = sprite_path

                # Extract the colors from the sprite
                palette = extract_palette_from_file(sprite_path)
                for i in range(16):
                    self.palette_cells[i].md_bg_color = (palette[i] if i < len(palette) else "000000")

        def detect_existing_sprites(self, _dir: str):
            sprites: list[str] = [""]
            for sprite in os.listdir(_dir):
                full_path = os.path.join(_dir, sprite)
                if os.path.isdir(full_path) or not sprite.endswith(".png"):
                    continue
                try:
                    open_image_secure(full_path)
                except Exception:
                    # If the image is invalid, don't add it to the sprite list
                    continue
                sprites.append(sprite[:-4])
            self.existing_sprites = sprites

        def update_sprite_list(self, _, _sprites: list[str]):
            self.sprite_input.items = _sprites
            if self.sprite_input.text not in _sprites:
                self.sprite_input.text = ""


    class BottomFrame(MDBoxLayout):
        adjust_rom: MDButton = ObjectProperty()
        save_data: MDButton = ObjectProperty()

        def late_init(self):
            self.adjust_rom.disabled = True

        def save_gui_settings(self):
            gui_args = Namespace()
            gui_args.patch = opts.patch
            gui_args.sprite_pack = opts.sprite_pack
            persistent_store("adjuster", GAME_GEN3_ADJUSTER, gui_args)
            Factory.InfoPopup().open("Successful Adjuster Data Save",
                                     "Adjuster settings saved to persistent storage!")

        def press_adjust_rom(self):
            try:
                gui_args = Namespace()
                gui_args.patch = opts.patch
                gui_args.sprite_pack = opts.sprite_pack
                path = app.adjust(gui_args)
            except Exception as e:
                logging.exception(e)
                Factory.InfoPopup().open("Error while adjusting the ROM",
                                         str(e))
            else:
                Factory.InfoPopup().open("Successful ROM Adjustment",
                                         f"ROM patched successfully to\n{path}")


    class AdjusterRootLayout(MDFloatLayout):
        top_frame: TopFrame = ObjectProperty()
        sprite_extractor: SpriteExtractorFrame = ObjectProperty()
        sprite_preview: SpritePreviewFrame = ObjectProperty()
        bottom_frame: BottomFrame = ObjectProperty()

        ap_rom: bytearray = None
        adjuster_extensions = [".gba", *EMERALD_PATCH_EXTENSIONS.split("/"), *FR_LG_PATCH_EXTENSIONS.split("/")]

        def late_init(self):
            self.top_frame.late_init()
            self.sprite_extractor.late_init()
            hide_widget(self.sprite_extractor)
            self.sprite_preview.late_init()
            hide_widget(self.sprite_preview)
            self.bottom_frame.late_init()

        def adjust(self, args: Namespace):
            # Adjusts the ROM by applying the patch file of one was given,
            # Building a BPS patch from the given sprite pack, and applying it
            self.ap_rom = self.ap_rom or self.build_ap_rom(args.patch)
            if not self.ap_rom:
                raise Exception("Could not build the AP ROM.")
            handle_address_collection(self.ap_rom, app.top_frame.patch_frame.rom_version,
                                      app.top_frame.patch_frame.is_ap_checkbox.checkbox.active)

            if not args.sprite_pack:
                raise Exception("Cannot adjust the ROM, a sprite pack is required!")

            # Build sprite pack patch & apply patch
            try:
                sprite_pack_bps_patch = self.build_sprite_pack_patch(args.sprite_pack)
            except Exception as e:
                if hasattr(e, "message"):
                    raise Exception(f"Error during patch creation: {e.message}")
                else:
                    raise Exception(f"Error during patch creation: {str(e)}")

            adjusted_ap_rom = bytearray(len(self.ap_rom))
            apply_bps_patch(sprite_pack_bps_patch, app.ap_rom, adjusted_ap_rom)

            rom_path_with_no_extension: tuple[str, str] = os.path.splitext(args.patch)
            adjusted_rom_path = rom_path_with_no_extension[0] + "-adjusted.gba"
            with open(adjusted_rom_path, "wb") as output_file:
                output_file.write(adjusted_ap_rom)
            return adjusted_rom_path

        def build_ap_rom(self, _patch: str):
            # Builds the AP ROM if a patch file was given or opens the AP ROM file that was given
            if not _patch:
                Factory.InfoPopup().open("Failed ROM Build",
                                         "Cannot build the AP ROM: a patch file or a patched ROM is required!")
                return

            rom_data: bytearray = None
            if os.path.splitext(_patch)[-1] == ".gba":
                # Load up the ROM directly
                with open(_patch, "rb") as stream:
                    rom_data = bytearray(stream.read())
            else:
                # Patch the registered ROM as an AP ROM
                if emerald_support:
                    rom_data = self.emerald_build_ap_rom(_patch)
                if frlg_support and not rom_data:
                    rom_data = self.frlg_build_ap_rom(_patch)
            if not rom_data:
                Factory.InfoPopup().open("Failed ROM Build",
                                         "Cannot build the AP ROM: invalid file extension: "
                                         + f"requires {'/'.join(self.adjuster_extensions[1:])}")
                return bytearray()

            return rom_data

        def emerald_build_ap_rom(self, _patch: str):
            # Builds the AP ROM if a patch file was given
            # Handles Pokemon Emerald patching
            if os.path.splitext(_patch)[-1] == ".apemerald":
                import Patch
                _, ap_rom_path = Patch.create_rom_file(_patch)
                with open(ap_rom_path, "rb") as stream:
                    return bytearray(stream.read())
            return bytearray()

        def frlg_build_ap_rom(self, _patch: str):
            # Builds the AP ROM if a patch file was given
            # Handles Pokemon Firered/Leafgreen patching
            if os.path.splitext(_patch)[-1] in [".apfirered", ".apleafgreen"]:
                import Patch
                _, ap_rom_path = Patch.create_rom_file(_patch)
                with open(ap_rom_path, "rb") as stream:
                    return bytearray(stream.read())
            return bytearray()

        def frlg_get_rom_version(self, _rom_data: bytearray):
            # Retrieves and returns the version of the ROM given
            allowed_internal_names = {"POKEMON FIRE": "Firered", "POKEMON LEAF": "Leafgreen"}
            internal_name = _rom_data[0xA0:0xAC].decode("utf-8")
            internal_revision = int(_rom_data[0xBC])
            version_name = allowed_internal_names.get(internal_name, "")
            if not version_name:
                return "Unknown"
            return f"{version_name}{'_rev1' if internal_revision == 1 else ''}"

        def build_sprite_pack_patch(self, _sprite_pack: str):
            # Builds the BPS patch including all of the sprite pack's data
            errors, has_error = validate_sprite_pack(_sprite_pack)
            if has_error:
                raise Exception("Cannot adjust the ROM as the sprite pack contains errors:\n{}".format(errors))

            sprite_pack_data = get_patch_from_sprite_pack(_sprite_pack, app.top_frame.patch_frame.rom_version)
            sprite_pack_bps_patch = data_to_bps_patch(sprite_pack_data)
            return sprite_pack_bps_patch


    class Adjuster(ThemedApp):
        def __init__(self):
            from Utils import __version__ as mw_version
            self.title = f"Archipelago {mw_version} Pokemon {adjuster_name} Adjuster"
            self.icon = r"data/icon.png"
            self.json_to_kivy_parser = KivyJSONtoTextParser(None)
            self.log_panels: typing.Dict[str, Widget] = {}
            super().__init__()

        def build(self) -> Layout:
            self.set_colors()
            self.container = AdjusterRootLayout()
            self.container.theme_cls = self.theme_cls
            self.container.md_bg_color = self.theme_cls.backgroundColor

            global app
            app = self.container
            app.late_init()

            # Load saved data
            adjuster_settings = get_adjuster_settings(GAME_GEN3_ADJUSTER)
            if hasattr(adjuster_settings, "patch"):
                if type(adjuster_settings.patch) is not str:
                    # Valid tkinter data, transform it
                    adjuster_settings.patch = adjuster_settings.patch.get()
                    adjuster_settings.sprite_pack = adjuster_settings.sprite_pack.get()
                app.top_frame.patch_frame.entry.text = adjuster_settings.patch
                app.top_frame.sprite_pack_frame.entry.text = adjuster_settings.sprite_pack

            # Uncomment to enable the kivy live editor console
            # Press Ctrl-E (with numlock/capslock) disabled to open
            from kivy.core.window import Window
            from kivy.modules import console
            console.create_console(Window, self.container)

            return self.container


    def hide_widget(_wid: Widget):
        if _wid.parent:
            _wid.saved_parent = _wid.parent
            _wid.parent.remove_widget(_wid)

    def show_widget(_wid: Widget, id: int = 0):
        if hasattr(_wid, "saved_parent") and _wid.parent != _wid.saved_parent:
            _wid.saved_parent.add_widget(_wid, index=id)

    app: AdjusterRootLayout = None

    opts.patch = ""
    opts.sprite_pack = ""
    Adjuster().run()

async def main():
    # Main function of the adjuster
    logging.basicConfig(format="%(message)s", level=logging.INFO)

    if not emerald_support and not frlg_support:
        raise Exception("This Archipelago installation doesn't contain tools for neither Pokemon Emerald or "
                        + "Pokemon Firered/Leafgreen.")

    run_kivy_gui()

def launch():
    import colorama
    import asyncio
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()

if __name__ == "__main__":
    main()
