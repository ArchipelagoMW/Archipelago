import argparse
import logging
import os
import math

from bps.apply import apply_to_bytearrays as apply_bps_patch

from Utils import local_path, persistent_store, get_adjuster_settings, get_adjuster_settings_no_defaults, \
    tkinter_center_window, data_to_bps_patch, open_image_secure
from .adjuster_patcher import get_patch_from_sprite_pack, extract_palette_from_file, \
    validate_sprite_pack, get_pokemon_data, stringify_pokemon_data, destringify_pokemon_data, \
    validate_pokemon_data_string, stringify_move_pool, destringify_move_pool, keep_different_pokemon_data, \
    handle_address_collection, find_folder_object_info, load_constants
from .adjuster_patcher import extract_sprites as extract_sprites_internal
from .adjuster_constants import POKEMON_TYPES, POKEMON_FOLDERS, POKEMON_ABILITIES, POKEMON_GENDER_RATIOS, \
    REVERSE_POKEMON_GENDER_RATIOS
from argparse import Namespace
from tkinter import Widget, messagebox, IntVar
from tkinter.tix import Tk

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
is_sprite_pack_valid = False
is_patch_valid = False
rom_version = "Emerald"
object_folders = POKEMON_FOLDERS
ap_rom: bytearray = None
is_rom_ap: IntVar = None

adjuster_name = "Gen 3" if frlg_support and emerald_support \
    else "Emerald" if emerald_support \
    else "Firered/Leafgreen" if frlg_support \
    else "No-Goal"
adjuster_extensions = [".gba", *EMERALD_PATCH_EXTENSIONS.split("/"), *FR_LG_PATCH_EXTENSIONS.split("/")]
GAME_GEN3_ADJUSTER = "Pokemon Gen 3 Adjuster"


def build_ap_rom(_patch: str):
    # Builds the AP ROM if a patch file was given or opens the AP ROM file that was given
    if not _patch:
        messagebox.showerror(title="Failure",
                             message="Cannot build the AP ROM: a patch file or a patched ROM is required!")
        return

    rom_data: bytearray = None
    if os.path.splitext(_patch)[-1] == ".gba":
        # Load up the ROM directly
        with open(_patch, "rb") as stream:
            rom_data = bytearray(stream.read())
    else:
        # Patch the registered ROM as an AP ROM
        if emerald_support:
            rom_data = emerald_build_ap_rom(_patch)
        if frlg_support and not rom_data:
            rom_data = frlg_build_ap_rom(_patch)
    if not rom_data:
        messagebox.showerror(title="Failure",
                             message="Cannot build the AP ROM: invalid file extension: "
                                     + f"requires {'/'.join(adjuster_extensions[1:])}")
        return bytearray()

    return rom_data


def emerald_build_ap_rom(_patch: str):
    # Builds the AP ROM if a patch file was given
    # Handles Pokemon Emerald patching
    if os.path.splitext(_patch)[-1] == ".apemerald":
        import Patch
        _, ap_rom_path = Patch.create_rom_file(_patch)
        with open(ap_rom_path, "rb") as stream:
            return bytearray(stream.read())
    return bytearray()


def frlg_build_ap_rom(_patch: str):
    # Builds the AP ROM if a patch file was given
    # Handles Pokemon Firered/Leafgreen patching
    if os.path.splitext(_patch)[-1] in [".apfirered", ".apleafgreen"]:
        import Patch
        _, ap_rom_path = Patch.create_rom_file(_patch)
        with open(ap_rom_path, "rb") as stream:
            return bytearray(stream.read())
    return bytearray()


def emerald_fetch_patch(_patch: str) -> tuple[str, str]:
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


def frlg_fetch_patch(_patch: str) -> tuple[str, str]:
    # Asks for a ROM or patch file then validates it
    # Handles the check for Pokemon Firered/Leafgreen
    if _patch and os.path.exists(_patch):
        if os.path.splitext(_patch)[-1] == ".gba":
            # If .gba, verify ROM integrity by checking for its internal name at addresses #0000A0-#0000AB
            with open(_patch, "rb") as stream:
                rom_data = bytearray(stream.read())
                return _patch, frlg_get_rom_version(rom_data)
        elif os.path.splitext(_patch)[-1] in [".apfirered", ".apleafgreen"]:
            # If .apfirered or .apleafgreen, patch the ROM to fetch its revision number
            patch_data = frlg_build_ap_rom(_patch)
            return _patch, frlg_get_rom_version(patch_data)
    return _patch, "Unknown"


def frlg_get_rom_version(_rom_data: bytearray):
    # Retrieves and returns the version of the ROM given
    allowed_internal_names = {"POKEMON FIRE": "Firered", "POKEMON LEAF": "Leafgreen"}
    internal_name = _rom_data[0xA0:0xAC].decode("utf-8")
    internal_revision = int(_rom_data[0xBC])
    version_name = allowed_internal_names.get(internal_name, "")
    if not version_name:
        return "Unknown"
    return f"{version_name}{'_rev1' if internal_revision == 1 else ''}"


def build_sprite_pack_patch(_sprite_pack: str):
    # Builds the BPS patch including all of the sprite pack's data
    errors, has_error = validate_sprite_pack(_sprite_pack)
    if has_error:
        raise Exception("Cannot adjust the ROM as the sprite pack contains errors:\n{}".format(errors))

    sprite_pack_data = get_patch_from_sprite_pack(_sprite_pack, rom_version)
    sprite_pack_bps_patch = data_to_bps_patch(sprite_pack_data)
    return sprite_pack_bps_patch


async def main():
    # Main function of the adjuster
    logging.basicConfig(format="%(message)s", level=logging.INFO)

    parser = get_argparser()
    args = parser.parse_args(namespace=get_adjuster_settings_no_defaults(GAME_GEN3_ADJUSTER))
    is_command_line: str = args.patch

    if not emerald_support and not frlg_support:
        if is_command_line:
            raise Exception("This Archipelago installation doesn't contain tools for neither Pokemon Emerald or "
                            + "Pokemon Firered/Leafgreen.")
        else:
            messagebox.showerror("This Archipelago installation doesn't contain tools for neither Pokemon Emerald or "
                                 + "Pokemon Firered/Leafgreen.")
            return

    if not is_command_line:
        adjust_gui()
    else:
        adjust(args)


def get_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch", default="",
                        help="Path to a Pokemon Gen 3 AP-randomized ROM to adjust or path to a fitting patch file.")
    parser.add_argument("--sprite-pack", default="", help="Path to the Pokemon Gen 3 sprite pack folder to use.")
    return parser


def adjust_gui():
    adjuster_settings = get_adjuster_settings(GAME_GEN3_ADJUSTER)

    from tkinter import LEFT, TOP, X, E, W, END, DISABLED, NORMAL, StringVar, \
        LabelFrame, Frame, Label, Entry, Button, Checkbutton, OptionMenu, \
        PhotoImage, filedialog, font
    from .tkentrycomplete import AutocompleteCombobox
    from tkinter.ttk import Notebook, Spinbox
    from tkinter.tix import Tk, Balloon
    from tkinter.scrolledtext import ScrolledText
    from Utils import __version__ as mw_version

    window = Tk()
    window.wm_title(f"Archipelago {mw_version} Pokemon {adjuster_name} Adjuster")
    set_icon(window)

    main_window_frame = Frame(window, padx=8, pady=8)
    main_window_frame.pack(side=TOP, expand=True, fill=X)

    opts = Namespace()

    ##############################################
    # ROM/Patch Selection, Sprite Pack Selection #
    ##############################################

    def patch_select(_forced_patch: str = None):
        # Run when we ask for the user to select a ROM or patch file,
        # or when the ROM or patch file needs to be reloaded
        global is_patch_valid
        global rom_version

        if _forced_patch is not None:
            patch = _forced_patch
        else:
            title = f"Choose a Pokemon {adjuster_name} ROM ({adjuster_extensions[0]}) or a "\
                    + f"{'/'.join(adjuster_extensions[1:])} patch file."

            from tkinter import filedialog
            old_patch_folder: str = os.path.dirname(opts.patch.get()) if is_patch_valid else None
            old_patch_file: str = opts.patch.get() if is_patch_valid else None
            patch = filedialog.askopenfilename(initialdir=old_patch_folder, initialfile=old_patch_file, title=title,
                                               filetypes=[("Rom & Patch Files", adjuster_extensions)])

            if patch:
                rom_version = "Unknown"
                if emerald_support:
                    patch, rom_version = emerald_fetch_patch(patch)
                if frlg_support and rom_version == "Unknown":
                    patch, rom_version = frlg_fetch_patch(patch)
                if rom_version == "Unknown":
                    messagebox.showerror(title="Error while loading a ROM",
                                         message=f"The ROM at path {patch} isn't a valid Pokemon {adjuster_name} ROM!")
                    return
        opts.patch.set(patch)

        is_patch_valid = len(patch) > 0 and os.path.exists(patch)
        if not is_patch_valid:
            # If the patch is invalid, hide the isAP checkbox, the Sprite Extractor
            # and the data edition window if it's displayed
            patch_is_ap_checkbox.pack_forget()
            sprite_extractor_frame.pack_forget()
            if data_edition_label_frame.winfo_ismapped():
                data_edition_label_frame.grid_forget()
                data_edition_error.grid(row=0, column=2, rowspan=2)
        else:
            load_constants(rom_version)
            try_validate_sprite_pack(opts.sprite_pack.get(), True)

            global object_folders
            trainer_folder_object_info = find_folder_object_info("trainer")
            players_folder_object_info = find_folder_object_info("players")
            pokemon_folder_object_info = find_folder_object_info("pokemon")
            object_folders = trainer_folder_object_info["folders"] + players_folder_object_info["folders"] \
                + pokemon_folder_object_info["folders"]
            if is_sprite_pack_valid:
                detect_existing_folders(opts.sprite_pack.get())
            check_sprite_extraction("")

            # If the patch is valid, show the isAP checkbox, the Sprite Extractor
            # and the data edition window if it's displayed
            patch_is_ap_checkbox.pack(side=LEFT, padx=(4, 0))
            if data_edition_error.winfo_ismapped():
                switch_sprite_folder(current_valid_sprite_folder.get().title(), current_valid_sprite.get())
            sprite_preview_frame.pack_forget()
            bottom_frame.pack_forget()
            sprite_extractor_frame.pack(side=TOP, expand=True, fill=X, pady=5)
            sprite_extractor_combobox.set_completion_list(object_folders)
            if is_sprite_pack_valid:
                sprite_preview_frame.pack(side=TOP, expand=True, fill=X, pady=5)
            bottom_frame.pack(side=TOP, pady=5)

    def detect_existing_folders(sprite_pack: str):
        # Detect existing object folders and list them
        existing_folders: list[str] = []
        for dir in os.listdir(sprite_pack):
            if dir in object_folders:
                existing_folders.append(dir)
        nonlocal folders
        folders = ["", *existing_folders]
        folder_selector.set_completion_list(folders)

    def sprite_pack_select(_forced_sprite_pack: str = None, _forced_folder="", _forced_sprite=""):
        # Run when we ask for the user to select a sprite pack,
        # or when the sprite pack needs to be reloaded
        global is_sprite_pack_valid

        if _forced_sprite_pack is not None:
            sprite_pack = _forced_sprite_pack
        else:
            old_sprite_pack_folder: str = opts.sprite_pack.get() if is_sprite_pack_valid else None
            sprite_pack = filedialog.askdirectory(initialdir=old_sprite_pack_folder, title="Choose a sprite pack.",
                                                  mustexist=True)
        opts.sprite_pack.set(sprite_pack)
        is_sprite_pack_valid = len(sprite_pack) > 0 and os.path.isdir(sprite_pack)
        try_validate_sprite_pack(opts.sprite_pack.get())

        if not is_sprite_pack_valid:
            # If the sprite pack is invalid, do not show the Sprite Preview
            sprite_preview_frame.pack_forget()
            folder_selector.set_completion_list([""])
        else:
            # If the sprite pack is valid, show the Sprite Viewer
            bottom_frame.pack_forget()
            sprite_preview_frame.pack(side=TOP, expand=True, fill=X, pady=5)
            bottom_frame.pack(side=TOP, pady=5)

            detect_existing_folders(sprite_pack)
        switch_sprite_folder(_forced_folder, _forced_sprite)

    global is_rom_ap
    is_rom_ap = IntVar()
    opts.patch = StringVar()
    opts.sprite_pack = StringVar()

    # Two lines with a label, an entry field and a button to ask for the
    # ROM/patch file to use for the adjuster, and the sprite pack
    # An extra checkbox is provided if the user wants to override whether the
    # given ROM is an Archipelago ROM or not, in case the auto-detection is wrong
    patch_dialog_frame = Frame(main_window_frame, padx=8, pady=2)
    patch_label = Label(patch_dialog_frame, text="Patch / Modified Rom")
    patch_entry = Entry(patch_dialog_frame, textvariable=opts.patch)
    patch_select_button = Button(patch_dialog_frame, text="Select Patch/Rom", command=patch_select)
    patch_is_ap_checkbox = Checkbutton(patch_dialog_frame, variable=is_rom_ap, text="Is AP?")

    sprit_pack_frame = Frame(main_window_frame, padx=8, pady=2)
    sprite_pack_label = Label(sprit_pack_frame, text="Sprite pack to load")
    sprite_pack_entry = Entry(sprit_pack_frame, textvariable=opts.sprite_pack)
    sprite_pack_select_button = Button(sprit_pack_frame, text="Select Pack", command=sprite_pack_select)

    # Balloon object used for displaying tooltips in the app, if some elements are hovered over
    main_window_tooltip = Balloon(main_window_frame)
    main_window_tooltip.bind_widget(patch_is_ap_checkbox,
                                    balloonmsg="Override this value if your ROM is badly detected as an AP one.\n"
                                               + "If enabled, the adjuster will use data addresses from "
                                               + "the Archipelago patch for the game to inject the various data "
                                               + "it needs to.")

    patch_dialog_frame.pack(side=TOP, expand=True, fill=X)
    patch_label.pack(side=LEFT)
    patch_entry.pack(side=LEFT, expand=True, fill=X)
    patch_select_button.pack(side=LEFT)
    sprit_pack_frame.pack(side=TOP, expand=True, fill=X)
    sprite_pack_label.pack(side=LEFT)
    sprite_pack_entry.pack(side=LEFT, expand=True, fill=X)
    sprite_pack_select_button.pack(side=LEFT)

    ####################
    # Sprite Extractor #
    ####################

    def check_sprite_extraction(_):
        # Enables or disables the sprite extraction button if the sprite's name is valid or not
        extraction_folder_valid = sprite_extractor_folder.get() in object_folders
        sprite_extractor_button["state"] = NORMAL if extraction_folder_valid else DISABLED

    def extract_sprites():
        # Run when the Extract button is pressed
        # Extract all the sprites from the given Pokemon or Trainer into the given folder
        if not sprite_extractor_folder.get() in object_folders:
            return

        base_folder_path: str = None
        if is_sprite_pack_valid:
            base_folder_path = opts.sprite_pack.get()
        output_folder = filedialog.askdirectory(initialdir=base_folder_path, mustexist=False,
                                                title="Select a folder to extract the sprites to.")
        if len(output_folder) == 0:
            return
        if not os.path.isdir(output_folder):
            os.makedirs(output_folder)

        handle_address_collection(ap_rom, rom_version, is_rom_ap.get())
        extract_sprites_internal(sprite_extractor_folder.get(), output_folder)
        messagebox.showinfo(title="Success",
                            message=f"All sprites for {sprite_extractor_folder.get()} "
                            + "have successfully been extracted!")

    def extract_all_sprites():
        # Run when the Extract All button is pressed
        # Extract all the sprites from all Pokemons and Trainers into the given folder
        base_folder_path: str = None
        if is_sprite_pack_valid:
            base_folder_path = opts.sprite_pack.get()
        output_folder = filedialog.askdirectory(initialdir=base_folder_path, mustexist=False,
                                                title="Select a folder to extract all sprites to.")
        if len(output_folder) == 0:
            return
        if not os.path.isdir(output_folder):
            os.makedirs(output_folder)

        handle_address_collection(ap_rom, rom_version, is_rom_ap.get())
        for object in object_folders:
            # Extract each Pokemon and Trainer into subfolders
            current_output = os.path.join(output_folder, object)
            if not os.path.isdir(current_output):
                os.makedirs(current_output)
            extract_sprites_internal(object, current_output)
        messagebox.showinfo(title="Success", message="All sprites have successfully been extracted!")

    sprite_extractor_folder = StringVar()

    # A label to give some info, an input to choose the Pokemon or Trainer's name, and two buttons:
    # One for extracting only the given Pokemon or Trainer, and one for extracting all Pokemons and Trainers
    sprite_extractor_frame = LabelFrame(main_window_frame, text="Sprite Extractor", padx=8, pady=8)
    sprite_extractor_frame.grid_columnconfigure(0, weight=1)
    sprite_extractor_frame.grid_columnconfigure(1, weight=1)
    sprite_extractor_info = Label(sprite_extractor_frame,
                                  text="Type the name of the Trainer/Pokemon you want to\n"
                                  + "extract then press the button below.")
    sprite_extractor_info.grid(row=0, column=0, columnspan=2, pady=2)
    sprite_extractor_combobox = AutocompleteCombobox(sprite_extractor_frame, textvariable=sprite_extractor_folder,
                                                     width=14)
    sprite_extractor_combobox.bind("<KeyRelease>", check_sprite_extraction, add="+")
    sprite_extractor_combobox.set_completion_list([""])
    sprite_extractor_combobox.grid(row=1, column=0, columnspan=2, pady=2)
    sprite_extractor_button = Button(sprite_extractor_frame, text="Extract", command=extract_sprites)
    sprite_extractor_button.grid(row=3, column=0, sticky=E, padx=5, pady=2)
    sprite_extractor_button_all = Button(sprite_extractor_frame, text="Extract All (takes a long time)",
                                         command=extract_all_sprites)
    sprite_extractor_button_all.grid(row=3, column=1, sticky=W, padx=5, pady=2)

    #############################
    # Sprite and Palette Viewer #
    #############################

    pokemon_rom_data: dict[str, int | list[dict[str, str | int]]] = None
    pokemon_saved_data: dict[str, int | list[dict[str, str | int]]] = None

    def switch_sprite_folder(_folder: str, _sprite: str = ""):
        # Run whenever the current sprite folder is changed
        # Loads the various data related to a Pokemon or Trainer, depending on the folder
        folder_path = os.path.join(opts.sprite_pack.get(), current_sprite_folder.get().title())
        if _folder and not os.path.isdir(folder_path):
            # Non-existent folder, reload the pack
            folder_selector.set("")
            sprite_selector.set("")
            sprite_pack_select(opts.sprite_pack.get())
            return
        if _folder not in folder_selector._completion_list:
            # Folder just created, reload the pack
            sprite_selector.set("")
            sprite_pack_select(opts.sprite_pack.get(), _folder)
            return

        current_sprite_folder.set(_folder)
        current_valid_sprite_folder.set(_folder)
        folder_selector.set(_folder)

        dir: str = os.path.join(opts.sprite_pack.get(), _folder)
        # Retrieve and list valid sprites
        sprites_in_folder: list[str] = []
        if is_sprite_pack_valid and _folder and os.path.isdir(dir):
            for sprite in os.listdir(dir):
                full_path = os.path.join(dir, sprite)
                if os.path.isdir(full_path) or not sprite.endswith(".png"):
                    continue
                try:
                    open_image_secure(full_path)
                except Exception:
                    # If the image is invalid, don't add it to the sprite list
                    continue
                sprites_in_folder.append(sprite[:-4])
        nonlocal sprites
        sprites = ["", *sprites_in_folder]
        sprite_selector.set_completion_list(sprites)

        switch_sprite(_sprite)

        if _folder not in POKEMON_FOLDERS or _folder == "Egg":
            # Trainer folder, do not show the Pokemon data edition frame
            sprite_preview_frame.grid_columnconfigure(2, weight=0)
            data_edition_label_frame.grid_forget()
            data_edition_error.grid_forget()
        else:
            # Pokemon folder, show the Pokemon data edition frame
            sprite_preview_frame.grid_columnconfigure(2, weight=1)
            if not is_patch_valid:
                data_edition_label_frame.grid_forget()
                data_edition_error.grid(row=0, column=2, rowspan=2)
                return
            else:
                data_edition_error.grid_forget()
                data_edition_label_frame.grid(row=0, column=2, rowspan=2)

            data_folder = "Unown A" if _folder.startswith("Unown ") else _folder
            # Fill in data editor fields
            nonlocal pokemon_rom_data, pokemon_saved_data
            pokemon_rom_data = get_pokemon_data(data_folder)
            pokemon_data = pokemon_rom_data.copy()
            pokemon_saved_data = None
            pokemon_saved_data_path = os.path.join(opts.sprite_pack.get(), data_folder, "data.txt")
            if os.path.exists(pokemon_saved_data_path):
                # Load local data if it exists and replace the fields' values
                with open(pokemon_saved_data_path) as pokemonSavedDataFile:
                    pokemon_saved_data_string = pokemonSavedDataFile.read()
                pokemon_saved_data_errors, pokemon_saved_data_has_error =\
                    validate_pokemon_data_string(_folder, pokemon_saved_data_string)
                if pokemon_saved_data_has_error:
                    messagebox.showerror(title="Error while loading Pokemon data", message=pokemon_saved_data_errors)
                else:
                    pokemon_saved_data = destringify_pokemon_data(data_folder, pokemon_saved_data_string)
                    for field in pokemon_saved_data:
                        if field == "dex":
                            pokemon_data[field] = pokemon_saved_data[field] = (pokemon_saved_data[field] << 7) + \
                                (pokemon_data[field] % 0x80)
                        else:
                            pokemon_data[field] = pokemon_saved_data[field]

            # Fill in the fields in the data editor and check their validity
            pokemon_hp.set(pokemon_data["hp"])
            pokemon_spd.set(pokemon_data["spd"])
            pokemon_atk.set(pokemon_data["atk"])
            pokemon_def.set(pokemon_data["def"])
            pokemon_spatk.set(pokemon_data["spatk"])
            pokemon_spdef.set(pokemon_data["spdef"])
            pokemon_type_1.set(POKEMON_TYPES[pokemon_data["type1"]])
            pokemon_type_2.set(POKEMON_TYPES[pokemon_data["type2"]])
            pokemon_ability_1.set(POKEMON_ABILITIES[pokemon_data["ability1"]].title())
            pokemon_ability_2.set(POKEMON_ABILITIES[pokemon_data["ability2"]].title() if pokemon_data["ability2"]
                                  else POKEMON_ABILITIES[pokemon_data["ability1"]].title())
            pokemon_gender_ratio.set(POKEMON_GENDER_RATIOS[pokemon_data["gender_ratio"]])
            pokemon_forbid_flip.set(pokemon_data["dex"] >> 7)

            move_pool_input.delete("1.0", END)
            move_pool_input.insert(END, stringify_move_pool(pokemon_data["move_pool"]))

            check_all_fields()

    def switch_sprite(_sprite: str):
        # Run whenever the current sprite is changed
        # Displays the new sprite and its palette in the adjuster
        sprite_path = os.path.join(opts.sprite_pack.get(), current_valid_sprite_folder.get().title(), _sprite + ".png")
        if _sprite and not os.path.exists(sprite_path):
            # Non-existent folder, reload the pack
            folder_selector.set("")
            sprite_selector.set("")
            sprite_pack_select(opts.sprite_pack.get())
            return
        if _sprite not in sprites:
            # Non-existant sprite, reload the pack
            sprite_selector.set("")
            sprite_pack_select(opts.sprite_pack.get())
            return

        current_sprite.set(_sprite)
        current_valid_sprite.set(_sprite)
        sprite_selector.set(_sprite)

        # Display the Archipelago icon as default
        if not _sprite:
            _sprite = local_path("data", "gen3_adjuster_default.png")
        else:
            _sprite = sprite_path[:-4]
        if not _sprite.endswith(".png"):
            _sprite = _sprite + ".png"

        # Switch the displayed sprite
        new_image = PhotoImage(file=_sprite).zoom(2, 2)
        sprite_label_image.configure(image=new_image)
        sprite_label_image.image = new_image

        # Extract the colors from the sprite
        palette = extract_palette_from_file(_sprite)
        for i in range(16):
            palette_previews[i]["bg"] = "#" + (palette[i] if i < len(palette) else "000000")

    def check_current_sprite_folder(_):
        # Run when the current sprite folder's value is changed
        # This only switches the current sprite folder is it's recognized
        if current_sprite_folder.get().title() in object_folders \
                and folder_selector.position == len(current_sprite_folder.get()):
            folderPath = os.path.join(opts.sprite_pack.get(), current_sprite_folder.get().title())
            if not os.path.isdir(folderPath):
                os.makedirs(folderPath)
            update_current_sprite_folder("")

    def update_current_sprite_folder(_):
        # Updates the current sprite folder, it must be considered valid
        switch_sprite_folder(current_sprite_folder.get().title())

    def check_current_sprite(_):
        # Run when the current sprite's value is changed
        # This only switches the current sprite is it's recognized
        if current_sprite.get() in sprites and sprite_selector.position == len(current_sprite.get()):
            update_current_sprite("")

    def update_current_sprite(_):
        # Updates the current sprite, it must be considered valid
        switch_sprite(current_sprite.get())

    current_sprite_folder = StringVar(value="")
    current_valid_sprite_folder = StringVar(value="")
    current_sprite = StringVar(value="")
    current_valid_sprite = StringVar(value="")
    folders = [""]
    sprites = [""]

    # Two sets of labels and autocompleting comboboxes for selecting a sprite folder and a sprite
    # Then one image to display the sprites, and 16 images arranged in a grid to display the palette
    sprite_preview_frame = LabelFrame(main_window_frame, text="Sprite Preview", padx=8, pady=8)
    sprite_preview_frame.grid_rowconfigure(0, weight=1)
    sprite_preview_frame.grid_rowconfigure(1, weight=1)
    sprite_preview_frame.grid_columnconfigure(0, weight=1)
    sprite_preview_frame.grid_columnconfigure(1, weight=1)

    folder_selector_frame = Frame(sprite_preview_frame)
    folder_selector_frame.grid(row=0, column=0, padx=8)
    folder_selector_label = Label(folder_selector_frame, text="Current Folder")
    folder_selector = AutocompleteCombobox(folder_selector_frame, textvariable=current_sprite_folder, width=14)
    folder_selector.set_completion_list(folders)
    folder_selector.bind("<<ComboboxSelected>>", update_current_sprite_folder)
    folder_selector.bind("<KeyRelease>", check_current_sprite_folder, add="+")

    sprite_selector_frame = Frame(sprite_preview_frame)
    sprite_selector_frame.grid(row=0, column=1, padx=8)
    sprite_selector_label = Label(sprite_selector_frame, text="Current Sprite")
    sprite_selector = AutocompleteCombobox(sprite_selector_frame, textvariable=current_sprite, width=14)
    sprite_selector.set_completion_list(sprites)
    sprite_selector.bind("<<ComboboxSelected>>", update_current_sprite)
    sprite_selector.bind("<KeyRelease>", check_current_sprite, add="+")

    sprite_frame = Frame(sprite_preview_frame, padx=2, pady=2)
    sprite_frame.grid(row=1, column=0, padx=8)
    sprite_label = Label(sprite_frame, text="Sprite")
    sprite_label_image = Label(sprite_frame, width=128, height=126)

    palette_preview_frame = Frame(sprite_preview_frame, width=128)
    palette_preview_frame.grid(row=1, column=1, padx=8)
    palette_label = Label(palette_preview_frame, text="Palette")
    palette_label.grid(row=0, column=0, columnspan=4)
    palette_previews: list[Frame] = []
    for i in range(16):
        palette_preview = Frame(palette_preview_frame, width=32, height=32, bg="#000000")
        palette_preview.grid(row=1 + math.floor(i / 4), column=i % 4)
        palette_previews.append(palette_preview)

    #######################
    # Pokemon Data Editor #
    #######################

    # Frame that contains the Pokemon data editor
    # And if it's not editable, an error message to display instead
    data_edition_label_frame = LabelFrame(sprite_preview_frame, text="Pokemon Data Editor", padx=8)
    data_edition_error = Label(sprite_preview_frame, text="A ROM needs to\nbe loaded to edit\na Pokemon's data!",
                               padx=8)

    def save_pokemon_data():
        # Saves the Pokemon's data into the given folder's "data.txt" file
        pokemon_name = current_valid_sprite_folder.get()
        if pokemon_name.startswith("Unown "):
            pokemon_name = "Unown A"
        # Build an object with all the registered data
        new_pokemon_data: dict[str, int | list[dict[str, str | int]]] = {
            "hp": int(pokemon_hp.get()),
            "atk": int(pokemon_atk.get()),
            "def": int(pokemon_def.get()),
            "spatk": int(pokemon_spatk.get()),
            "spdef": int(pokemon_spdef.get()),
            "spd": int(pokemon_spd.get()),
            "type1": POKEMON_TYPES.index(pokemon_type_1.get()),
            "type2": POKEMON_TYPES.index(pokemon_type_2.get()),
            "ability1": POKEMON_ABILITIES.index(pokemon_ability_1.get().upper()),
            "ability2": POKEMON_ABILITIES.index(pokemon_ability_2.get().upper())
            or POKEMON_ABILITIES.index(pokemon_ability_1.get().upper()),
            "gender_ratio": REVERSE_POKEMON_GENDER_RATIOS[pokemon_gender_ratio.get()],
            "dex": (int(pokemon_forbid_flip.get()) << 7) + int(pokemon_rom_data["dex"]) % 0x80,
            "move_pool": destringify_move_pool(move_pool_input.get("1.0", END))
        }
        # Trim the data that has not been changed
        nonlocal pokemon_saved_data
        pokemon_saved_data = keep_different_pokemon_data(pokemon_rom_data, new_pokemon_data)
        check_all_fields()

        # Save changes to a specific data file
        pokemon_saved_data_string = stringify_pokemon_data(pokemon_saved_data)
        data_folder_path = os.path.join(opts.sprite_pack.get(), pokemon_name)
        if not os.path.isdir(data_folder_path):
            os.makedirs(data_folder_path)
        data_path = os.path.join(data_folder_path, "data.txt")
        if pokemon_saved_data_string:
            with open(data_path, "w") as data_file:
                data_file.write(pokemon_saved_data_string)

        try_validate_sprite_pack(opts.sprite_pack.get())
        messagebox.showinfo(title="Success",
                            message=f"Data for the Pokemon {pokemon_name} has been successfully saved!")

    # Notebook containing several tabs for various data to change and a button to save the data
    data_edition_notebook = Notebook(data_edition_label_frame, padding=2)
    data_edition_notebook.pack(side=TOP)
    data_edition_button = Button(data_edition_label_frame, text="Save Data", command=save_pokemon_data)
    data_edition_button.pack(side=TOP, pady=4)

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

    pokemon_hp = StringVar()
    pokemon_spd = StringVar()
    pokemon_atk = StringVar()
    pokemon_def = StringVar()
    pokemon_spatk = StringVar()
    pokemon_spdef = StringVar()

    pokemon_type_1 = StringVar()
    pokemon_type_2 = StringVar()
    pokemon_ability_1 = StringVar()
    pokemon_ability_2 = StringVar()
    pokemon_gender_ratio = StringVar()
    pokemon_forbid_flip = IntVar()

    def update_field_validity(fieldName: str, value: bool):
        # Disables the Pokemon data saving button if any data is erroneous
        valid_field_values[fieldName] = value
        any_value_invalid = list(k for k, v in valid_field_values.items() if not v)
        data_edition_button["state"] = DISABLED if any_value_invalid else NORMAL

    def update_field_change(fieldName: str, value: bool):
        # Displays the Pokemon data saving button's text in bold if any data has been changed
        changed_field_values[fieldName] = value
        any_value_changed = list(k for k, v in changed_field_values.items() if v)
        data_edition_button.config(font=bold_font if any_value_changed else normal_font)

    normal_font = font.nametofont("TkDefaultFont")
    bold_font = normal_font.copy()
    bold_font["weight"] = "bold"

    def check_value(entry: Widget | StringVar | IntVar, label: Label, field: str, balloonMessage: str):
        # Checks if a given Pokemon data value is valid or if it has been changed
        # And updates its label's color and font in consequence
        # Red if invalid, blue if different from the ROM, bold if different from the saved data
        field_value = str("[ {} ]".format(entry.get('1.0', END)).replace("\n", ", ") if type(entry) is ScrolledText
                          else entry.get()).strip()
        blue_balloon_message = "\nThis label is blue because this value is different from the one within the ROM."
        bold_balloon_message = "\nThis label is in bold because this value has been changed and hasn't been saved."
        errors, has_error = validate_pokemon_data_string(current_valid_sprite_folder.get(), {field: field_value})
        temp_pokemon_data_string = f"{field}: {field_value}"
        is_different_from_rom = True
        is_different_from_data = False
        internal_field = "dex" if field == "forbid_flip" else field
        if not has_error:
            temp_pokemon_data = destringify_pokemon_data(current_valid_sprite_folder.get(), temp_pokemon_data_string)
            if "dex" in list(temp_pokemon_data.keys()):
                temp_pokemon_data["dex"] = (temp_pokemon_data["dex"] << 7) + (pokemon_rom_data["dex"] % 0x80)
            different_pokemon_data = keep_different_pokemon_data(pokemon_rom_data, temp_pokemon_data)
            is_different_from_rom = internal_field in list(different_pokemon_data.keys())
            if pokemon_saved_data and internal_field in list(pokemon_saved_data.keys()):
                different_pokemon_data = keep_different_pokemon_data(pokemon_saved_data, temp_pokemon_data)
                is_different_from_data = internal_field in list(different_pokemon_data.keys())
            else:
                is_different_from_data = is_different_from_rom

        label.config(fg="red" if has_error else "blue" if is_different_from_rom else "black",
                     font=bold_font if is_different_from_data else normal_font)
        main_window_tooltip.unbind_widget(label)
        main_window_tooltip.bind_widget(
            label,
            balloonmsg=f"{balloonMessage}"
                       + '\n{}'.format(errors) if has_error else blue_balloon_message if is_different_from_rom else ''
                       + f"{bold_balloon_message if is_different_from_data else ''}"
        )
        update_field_validity(field, not has_error)
        update_field_change(field, is_different_from_data)

    def check_all_fields():
        # Checks all Pokemon data values, and updates their labels
        check_value(pokemon_hp, stat_hp_label, "hp", stat_hp_balloon_message)
        check_value(pokemon_spd, stat_spd_label, "spd", stat_spd_balloon_message)
        check_value(pokemon_atk, stat_atk_label, "atk", stat_atk_balloon_message)
        check_value(pokemon_def, stat_def_label, "def", stat_def_balloon_message)
        check_value(pokemon_spatk, stat_spatk_label, "spatk", stat_spatk_balloon_message)
        check_value(pokemon_spdef, stat_spdef_label, "spdef", stat_spdef_balloon_message)
        check_value(pokemon_type_1, type_1_label, "type1", type_1_balloon_message)
        check_value(pokemon_type_2, type_2_label, "type2", type_2_balloon_message)
        check_value(pokemon_ability_1, ability_1_label, "ability1", ability_1_balloon_message)
        check_value(pokemon_ability_2, ability_2_label, "ability2", ability_2_balloon_message)
        check_value(pokemon_gender_ratio, gender_ratio_label, "gender_ratio", gender_ratio_balloon_message)
        check_value(pokemon_forbid_flip, forbid_flip_label, "forbid_flip", forbid_flip_balloon_message)
        check_value(move_pool_input, move_pool_label, "move_pool", move_pool_balloon_message)

    stat_hp_label: Label = None
    stat_spd_label: Label = None
    stat_atk_label: Label = None
    stat_def_label: Label = None
    stat_spatk_label: Label = None
    stat_spdef_label: Label = None
    stat_hp_balloon_message = "This value changes the Pokemon's base HP.\nAwaits a value between 1 and 255."
    stat_spd_balloon_message = "This value changes the Pokemon's base Speed.\nAwaits a value between 1 and 255."
    stat_atk_balloon_message = "This value changes the Pokemon's base Attack.\nAwaits a value between 1 and 255."
    stat_def_balloon_message = "This value changes the Pokemon's base Defense.\nAwaits a value between 1 and 255."
    stat_spatk_balloon_message = "This value changes the Pokemon's base Special Attack.\n"\
                                 + "Awaits a value between 1 and 255."
    stat_spdef_balloon_message = "This value changes the Pokemon's base Special Defense.\n"\
                                 + "Awaits a value between 1 and 255."

    def build_stat_frame():
        # Tab for changing the Pokemon's base stats
        # Six groups of labels and spinboxes, one for each stat
        stat_frame = Frame(data_edition_notebook)
        data_edition_notebook.add(stat_frame, text="Stats")
        stat_frame.grid_rowconfigure(0, weight=1)
        stat_frame.grid_rowconfigure(1, weight=1)
        stat_frame.grid_rowconfigure(2, weight=1)
        stat_frame.grid_columnconfigure(0, weight=1)
        stat_frame.grid_columnconfigure(1, weight=1)

        nonlocal stat_hp_label, stat_spd_label, stat_atk_label, stat_def_label, stat_spatk_label, stat_spdef_label
        stat_hp_frame = Frame(stat_frame, padx=2, pady=2)
        stat_hp_frame.grid(row=0, column=0)
        stat_hp_label = Label(stat_hp_frame, text="HP")
        main_window_tooltip.bind_widget(stat_hp_label, balloonmsg=stat_hp_balloon_message)
        stat_hp_input = Spinbox(stat_hp_frame, textvariable=pokemon_hp, width=7, from_=1, to=255)

        stat_spd_frame = Frame(stat_frame, padx=2, pady=2)
        stat_spd_frame.grid(row=0, column=1)
        stat_spd_label = Label(stat_spd_frame, text="Speed")
        main_window_tooltip.bind_widget(stat_spd_label, balloonmsg=stat_spd_balloon_message)
        stat_spd_input = Spinbox(stat_spd_frame, textvariable=pokemon_spd, width=7, from_=1, to=255)

        stat_atk_frame = Frame(stat_frame, padx=2, pady=2)
        stat_atk_frame.grid(row=1, column=0)
        stat_atk_label = Label(stat_atk_frame, text="Attack")
        main_window_tooltip.bind_widget(stat_atk_label, balloonmsg=stat_atk_balloon_message)
        stat_atk_input = Spinbox(stat_atk_frame, textvariable=pokemon_atk, width=7, from_=1, to=255)

        stat_def_frame = Frame(stat_frame, padx=2, pady=2)
        stat_def_frame.grid(row=2, column=0)
        stat_def_label = Label(stat_def_frame, text="Defense")
        main_window_tooltip.bind_widget(stat_def_label, balloonmsg=stat_def_balloon_message)
        stat_def_input = Spinbox(stat_def_frame, textvariable=pokemon_def, width=7, from_=1, to=255)

        stat_spatk_frame = Frame(stat_frame, padx=2, pady=2)
        stat_spatk_frame.grid(row=1, column=1)
        stat_spatk_label = Label(stat_spatk_frame, text="Sp. Atk.")
        main_window_tooltip.bind_widget(stat_spatk_label, balloonmsg=stat_spatk_balloon_message)
        stat_spatk_input = Spinbox(stat_spatk_frame, textvariable=pokemon_spatk, width=7, from_=1, to=255)

        stat_spdef_frame = Frame(stat_frame, padx=2, pady=2)
        stat_spdef_frame.grid(row=2, column=1)
        stat_spdef_label = Label(stat_spdef_frame, text="Sp. Def.")
        main_window_tooltip.bind_widget(stat_spdef_label, balloonmsg=stat_spdef_balloon_message)
        stat_spdef_input = Spinbox(stat_spdef_frame, textvariable=pokemon_spdef, width=7, from_=1, to=255)

        stat_hp_label.pack(side=TOP)
        stat_hp_input.pack(side=TOP)
        stat_hp_input.bind("<KeyRelease>",
                           lambda _: check_value(pokemon_hp, stat_hp_label, "hp", stat_hp_balloon_message),
                           add="+")
        stat_spd_label.pack(side=TOP)
        stat_spd_input.pack(side=TOP)
        stat_spd_input.bind("<KeyRelease>",
                            lambda _: check_value(pokemon_spd, stat_spd_label, "spd", stat_spd_balloon_message),
                            add="+")
        stat_atk_label.pack(side=TOP)
        stat_atk_input.pack(side=TOP)
        stat_atk_input.bind("<KeyRelease>",
                            lambda _: check_value(pokemon_atk, stat_atk_label, "atk", stat_atk_balloon_message),
                            add="+")
        stat_def_label.pack(side=TOP)
        stat_def_input.pack(side=TOP)
        stat_def_input.bind("<KeyRelease>",
                            lambda _: check_value(pokemon_def, stat_def_label, "def", stat_def_balloon_message),
                            add="+")
        stat_spatk_label.pack(side=TOP)
        stat_spatk_input.pack(side=TOP)
        stat_spatk_input.bind("<KeyRelease>",
                              lambda _: check_value(pokemon_spatk, stat_spatk_label, "spatk",
                                                    stat_spatk_balloon_message),
                              add="+")
        stat_spdef_label.pack(side=TOP)
        stat_spdef_input.pack(side=TOP)
        stat_spdef_input.bind("<KeyRelease>",
                              lambda _: check_value(pokemon_spdef, stat_spdef_label, "spdef",
                                                    stat_spdef_balloon_message),
                              add="+")

    type_1_label: Label = None
    type_2_label: Label = None
    ability_1_label: Label = None
    ability_2_label: Label = None
    gender_ratio_label: Label = None
    forbid_flip_label: Label = None
    type_1_balloon_message = "This value changes the Pokemon's first type."
    type_2_balloon_message = "This value changes the Pokemon's second type.\n"\
                             + "Make it match the first type if you want the Pokemon to only have one type."
    ability_1_balloon_message = "This value changes the Pokemon's first ability."
    ability_2_balloon_message = "This value changes the Pokemon's second ability.\n"\
                                + "Make it match the first ability if you want the Pokemon to only have one ability."
    gender_ratio_balloon_message = "This value changes the Pokemon's gender ratio."
    forbid_flip_balloon_message = "This value dictates whether the Pokemon's sprite can be flipped or not.\n"\
                                  + "The sprite is flipped when looking at a Pokemon's status screen in your team."

    def build_extra_data_frame():
        # Tab for changing the Pokemon's types, abilities, gender ratio and whether its sprite can be flipped or not
        # Each type can be chosen with a simple option menu, while each ability requires an autocompleting combobox
        # Gender ratios are limied, so an option menu is enough to display all values
        # The option to forbid sprites for being flipped is a checkbox
        extra_data_frame = Frame(sprite_preview_frame)
        data_edition_notebook.add(extra_data_frame, text="Other")
        extra_data_frame.grid_rowconfigure(0, weight=1)
        extra_data_frame.grid_rowconfigure(1, weight=1)
        extra_data_frame.grid_rowconfigure(2, weight=1)
        extra_data_frame.grid_columnconfigure(0, weight=1)
        extra_data_frame.grid_columnconfigure(1, weight=1)

        nonlocal type_1_label, type_2_label, ability_1_label, ability_2_label, gender_ratio_label, forbid_flip_label

        type_1_frame = Frame(extra_data_frame, padx=2, pady=2)
        type_1_frame.grid(row=0, column=0)
        type_1_label = Label(type_1_frame, text="Type 1")
        main_window_tooltip.bind_widget(type_1_label, balloonmsg=type_1_balloon_message)
        type_1_input = OptionMenu(type_1_frame, pokemon_type_1, "Normal", *POKEMON_TYPES[1:],
                                  command=lambda _: check_value(pokemon_type_1, type_1_label,
                                                                "type1", type_1_balloon_message))

        type_2_frame = Frame(extra_data_frame, padx=2, pady=2)
        type_2_frame.grid(row=1, column=0)
        type_2_label = Label(type_2_frame, text="Type 2")
        main_window_tooltip.bind_widget(type_2_label, balloonmsg=type_2_balloon_message)
        type_2_input = OptionMenu(type_2_frame, pokemon_type_2, "Normal", *POKEMON_TYPES[1:],
                                  command=lambda _: check_value(pokemon_type_2, type_2_label,
                                                                "type2", type_2_balloon_message))

        ability_1_frame = Frame(extra_data_frame, padx=2, pady=2)
        ability_1_frame.grid(row=0, column=1)
        ability_1_label = Label(ability_1_frame, text="Ability 1")
        main_window_tooltip.bind_widget(ability_1_label, balloonmsg=ability_1_balloon_message)
        ability_1_input = AutocompleteCombobox(ability_1_frame, textvariable=pokemon_ability_1, width=12)
        ability_1_input.set_completion_list([ability.title() for ability in POKEMON_ABILITIES][1:])

        ability_2_frame = Frame(extra_data_frame, padx=2, pady=2)
        ability_2_frame.grid(row=1, column=1)
        ability_2_label = Label(ability_2_frame, text="Ability 2")
        main_window_tooltip.bind_widget(ability_2_label, balloonmsg=ability_2_balloon_message)
        ability_2_input = AutocompleteCombobox(ability_2_frame, textvariable=pokemon_ability_2, width=12)
        ability_2_input.set_completion_list([ability.title() for ability in POKEMON_ABILITIES][1:])

        gender_ratio_frame = Frame(extra_data_frame, padx=2, pady=2)
        gender_ratio_frame.grid(row=2, column=0)
        gender_ratio_label = Label(gender_ratio_frame, text="Gender")
        main_window_tooltip.bind_widget(gender_ratio_label, balloonmsg=gender_ratio_balloon_message)
        gender_ratio_input = OptionMenu(gender_ratio_frame, pokemon_gender_ratio, "100% M",
                                        *list(POKEMON_GENDER_RATIOS.values())[1:],
                                        command=lambda _: check_value(pokemon_gender_ratio, gender_ratio_label,
                                                                      "gender_ratio", gender_ratio_balloon_message))

        forbid_flip_frame = Frame(extra_data_frame, padx=2, pady=2)
        forbid_flip_frame.grid(row=2, column=1)
        forbid_flip_label = Label(forbid_flip_frame, text="Forbid Flip")
        main_window_tooltip.bind_widget(forbid_flip_label, balloonmsg=forbid_flip_balloon_message)
        forbid_flip_input = Checkbutton(forbid_flip_frame, variable=pokemon_forbid_flip,
                                        command=lambda: check_value(pokemon_forbid_flip, forbid_flip_label,
                                                                    "forbid_flip", forbid_flip_balloon_message))

        type_1_label.pack(side=TOP)
        type_1_input.pack(side=TOP)
        type_2_label.pack(side=TOP)
        type_2_input.pack(side=TOP)
        ability_1_label.pack(side=TOP)
        ability_1_input.pack(side=TOP)
        ability_1_input.bind("<<ComboboxSelected>>",
                             lambda e: check_value(e.widget, ability_1_label, "ability1", ability_1_balloon_message))
        ability_1_input.bind("<KeyRelease>",
                             lambda e: check_value(e.widget, ability_1_label, "ability1", ability_1_balloon_message),
                             add="+")
        ability_2_label.pack(side=TOP)
        ability_2_input.pack(side=TOP)
        ability_2_input.bind("<<ComboboxSelected>>",
                             lambda e: check_value(e.widget, ability_2_label, "ability2", ability_2_balloon_message))
        ability_2_input.bind("<KeyRelease>",
                             lambda e: check_value(e.widget, ability_2_label, "ability2", ability_2_balloon_message),
                             add="+")
        gender_ratio_label.pack(side=TOP)
        gender_ratio_input.pack(side=TOP)
        forbid_flip_label.pack(side=TOP)
        forbid_flip_input.pack(side=TOP)

    move_pool_input: ScrolledText = None
    move_pool_label: Label = None
    move_pool_balloon_message = "This value contains the Pokemon's levelup learnset.\nEach line must contain a move.\n"\
                                + "Each move must be written in the format \"<move>: <level>\".\n"\
                                + "With <move> being a known Pokemon move from this generation.\n"\
                                + "And with <level> being a number between 1 and 100."

    def build_move_pool_frame():
        # Tab for changing the Pokemon's levelup moveset
        # Only one big scrolling text which may be changed in the future to make it more ergonomic
        move_pool_frame = Frame(sprite_preview_frame)
        data_edition_notebook.add(move_pool_frame, text="Move Pool")

        nonlocal move_pool_input, move_pool_label

        move_pool_label = Label(move_pool_frame, text="Move Pool")
        move_pool_input = ScrolledText(move_pool_frame, undo=True, width=24, height=10)

        move_pool_label.pack(side=TOP)
        move_pool_input.pack(side=TOP)
        move_pool_input.bind("<KeyRelease>",
                             lambda e: check_value(e.widget, move_pool_label, "move_pool", move_pool_balloon_message),
                             add="+")

    build_stat_frame()
    build_move_pool_frame()
    build_extra_data_frame()

    # Label that displays all errors and warnings from within the pack at the end
    sprite_preview_error_label = Label(sprite_preview_frame, text="No error detected! The sprite pack is valid.",
                                       pady=4)
    sprite_preview_error_label.grid(row=2, column=0, columnspan=4)

    folder_selector_label.pack(side=TOP, expand=True, fill=X)
    folder_selector.pack(side=TOP, expand=True, fill=X)
    sprite_selector_label.pack(side=TOP, expand=True, fill=X)
    sprite_selector.pack(side=TOP, expand=True, fill=X)
    sprite_label.pack(side=TOP, expand=True, fill=X)
    sprite_label_image.pack(side=TOP)

    ##########################
    # Apply and Save Buttons #
    ##########################

    def adjust_rom():
        try:
            gui_args = Namespace()
            gui_args.patch = opts.patch.get()
            gui_args.sprite_pack = opts.sprite_pack.get()
            path = adjust(gui_args)
        except Exception as e:
            logging.exception(e)
            messagebox.showerror(title="Error while adjusting Rom", message=str(e))
        else:
            messagebox.showinfo(title="Success", message=f"Rom patched successfully to {path}")

    def save_gui_settings():
        gui_args = Namespace()
        gui_args.patch = opts.patch.get()
        gui_args.sprite_pack = opts.sprite_pack.get()
        persistent_store("adjuster", GAME_GEN3_ADJUSTER, gui_args)
        messagebox.showinfo(title="Success", message="Settings saved to persistent storage")

    bottom_frame = Frame(main_window_frame)

    # Buttons for adjusting the ROM and saving the current adjuster's configuration
    adjust_button = Button(bottom_frame, text="Adjust Rom", command=adjust_rom)
    adjust_button.pack(side=LEFT, padx=(5, 5))
    save_button = Button(bottom_frame, text="Save Settings", command=save_gui_settings)
    save_button.pack(side=LEFT, padx=(5, 5))

    bottom_frame.pack(side=TOP, pady=(5, 5))

    def try_validate_sprite_pack(_sprite_pack: str, _patch_changed=False):
        # Validates the sprite pack if both the ROM/patch file and the sprite packs are valid
        has_error = False
        if is_patch_valid:
            global ap_rom
            ap_rom = ap_rom if not _patch_changed else build_ap_rom(opts.patch.get())
            if not ap_rom:
                sprite_preview_error_label["text"] = "Could not build the AP ROM."
                return
            is_rom_ap_state = handle_address_collection(ap_rom, rom_version,
                                                        None if _patch_changed else is_rom_ap.get())
            if _patch_changed:
                # Change the state of the isAP button automatically when a new patch is loaded
                if is_rom_ap_state:
                    patch_is_ap_checkbox.select()
                else:
                    patch_is_ap_checkbox.deselect()
                patch_is_ap_checkbox["state"] = DISABLED if not opts.patch.get().endswith(".gba") else NORMAL
        if is_patch_valid and is_sprite_pack_valid:
            errors, has_error = validate_sprite_pack(_sprite_pack)
            adjust_button["state"] = DISABLED if has_error else NORMAL
            sprite_preview_error_label["text"] = errors or "No anomaly detected! The sprite pack is valid."
        else:
            adjust_button["state"] = DISABLED
            sprite_preview_error_label["text"] = "Both a sprite pack and a patch/ROM must be selected to validate the "\
                                                 + "sprite pack."
        return

    patch_select(adjuster_settings.patch or "")
    sprite_pack_select(adjuster_settings.sprite_pack or "")

    tkinter_center_window(window)
    window.mainloop()


def set_icon(window: Tk):
    # Sets the adjuster's icon
    from tkinter import PhotoImage
    logo = PhotoImage(file=local_path("data", "icon.png"))
    window.tk.call("wm", "iconphoto", window._w, logo)


def adjust(args: Namespace):
    # Adjusts the ROM by applying the patch file of one was given,
    # Building a BPS patch from the given sprite pack, and applying it
    global ap_rom
    ap_rom = ap_rom or build_ap_rom(args.patch)
    if not ap_rom:
        raise Exception("Could not build the AP ROM.")
    handle_address_collection(ap_rom, rom_version, is_rom_ap.get())

    if not args.sprite_pack:
        raise Exception("Cannot adjust the ROM, a sprite pack is required!")

    # Build sprite pack patch & apply patch
    try:
        sprite_pack_bps_patch = build_sprite_pack_patch(args.sprite_pack)
    except Exception as e:
        if hasattr(e, "message"):
            raise Exception(f"Error during patch creation: {e.message}")
        else:
            raise Exception(f"Error during patch creation: {str(e)}")

    adjusted_ap_rom = bytearray(len(ap_rom))
    apply_bps_patch(sprite_pack_bps_patch, ap_rom, adjusted_ap_rom)

    rom_path_with_no_extension: tuple[str, str] = os.path.splitext(args.patch)
    adjusted_rom_path = rom_path_with_no_extension[0] + "-adjusted.gba"
    with open(adjusted_rom_path, "wb") as output_file:
        output_file.write(adjusted_ap_rom)
    return adjusted_rom_path


def launch():
    import colorama
    import asyncio
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()


if __name__ == "__main__":
    main()
