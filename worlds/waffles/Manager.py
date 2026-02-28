import os
import io
import zipfile
import logging
import pkgutil
import shutil
import json
import textwrap
import argparse
import tkinter as tk
from argparse import Namespace
from tkinter import Tk, StringVar, Entry, filedialog, messagebox, LEFT, X, BOTH, TOP, \
    E, W, BOTTOM, RIGHT, font as font, BooleanVar, LabelFrame
from tkinter.ttk import Separator, OptionMenu, Button, Frame, Label, Checkbutton
from tkinter.constants import DISABLED, NORMAL
from Utils import persistent_store, get_adjuster_settings_no_defaults, tkinter_center_window, open_filename

from .SNESGraphics import copy_gfx_tiles, convert_rgb_to_snes

import ModuleUpdate
ModuleUpdate.update()

GAME_NAME = "SMW: Spicy Mycena Waffles"
WINDOW_MIN_HEIGHT = 520
WINDOW_MIN_WIDTH = 380


class ArgumentDefaultsHelpFormatter(argparse.RawTextHelpFormatter):

    def _get_help_string(self, action):
        return textwrap.dedent(action.help)
    

def get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    #parser.add_argument("--rom", default="AP_Waffle.sfc", help="Path to a Waffles ROM to adjust.")
    parser.add_argument("--selected_pack", help="Path to a Graphics Pack for Waffles.")

    return parser


def main(launcher_args):
    parser = get_argparser()
    args = parser.parse_args(launcher_args, namespace=get_adjuster_settings_no_defaults(GAME_NAME))

    manager_gui()


def manager_gui():
    
    manager_window = Tk()
    manager_window.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
    manager_window.resizable(True, False)
    manager_window.wm_title(f"Spicy Mycena Waffles Adjuster")

    gfx_pack_frame, gfx_pack_vars = create_gfx_pack_frame(manager_window)
    enemy_shuffle_frame, enemy_shuffle_vars = create_enemy_shuffle_frame(manager_window)
    global_settings_frame = create_global_settings_frame(manager_window)
    file_frame, vars_ns = create_file_frame(manager_window, (gfx_pack_vars, enemy_shuffle_vars))

    file_frame.pack(side=TOP, padx=8, pady=4, fill=BOTH)
    global_settings_frame.pack(side=TOP, padx=8, pady=4, fill=BOTH)
    enemy_shuffle_frame.pack(side=TOP, padx=8, pady=4, fill=BOTH)
    gfx_pack_frame.pack(side=TOP, padx=8, pady=4, fill=BOTH)

    tkinter_center_window(manager_window)
    manager_window.mainloop()


def create_file_frame(parent=None, external_vars=None):
    vars_ns = Namespace()
    if external_vars:
        for var_group in external_vars:
            for key, value in vars(var_group).items():
                setattr(vars_ns, key, value)

    frame = LabelFrame(parent, text="Graphics Pack Options", padx=8, pady=8)

    vars_ns.patch_path = StringVar()
    load_frame = Frame(frame)
    file_label = Label(load_frame, text="Patch file: ")
    file_label.pack(side=LEFT, fill=X)
    file_value = Entry(load_frame, textvariable=vars_ns.patch_path, state="readonly")
    file_value.pack(side=RIGHT, fill=X, expand=True)

    def load_window():
        nonlocal vars_ns

        file_path = filedialog.askopenfilename(
            filetypes=[("Waffles Patch Files", ".apwaffle")])
        try:
            vars_ns.patch_path.set(file_path)
            load_data_from_patch(file_path, vars_ns)
        except Exception as e:
            messagebox.showerror(title="Error while reading Waffles Patch file", message=str(e))

    def save_window():
        nonlocal vars_ns
        if "" == vars_ns.patch_path.get():
            return
        save_adjusted_data(vars_ns)
        messagebox.showinfo(title="Success", message="Saved changes to Waffles Patch file!")

    load_button = Button(frame, text="Load Waffles Patch", command=load_window)
    save_button = Button(frame, text="Save changes to Waffles Patch", command=save_window)

    load_frame.pack(side=TOP, fill=X)
    load_button.pack(side=TOP, fill=X)
    save_button.pack(side=TOP, fill=X)

    return frame, vars_ns


def load_data_from_patch(patch_path, vars_ns):
    file = zipfile.ZipFile(patch_path)
    options_file = json.loads(file.read("options.json").decode("UTF-8"))

    vars_ns.enemy_shuffle_active.set(options_file["enemy_shuffle"])
    vars_ns.enemy_shuffle_seed.set(options_file["enemy_shuffle_seed"])

    if "graphics_pack" in options_file.keys():
        vars_ns.selected_pack.set(options_file["graphics_pack"])


def save_adjusted_data(vars_ns):
    patch_path = vars_ns.patch_path.get()
    file = zipfile.ZipFile(patch_path)

    zip_files = dict()
    for file_name in file.namelist():
        zip_files[file_name] = file.read(file_name)

    options_file = json.loads(file.read("options.json").decode("UTF-8"))
    options_file["enemy_shuffle"] = vars_ns.enemy_shuffle_active.get()
    options_file["enemy_shuffle_seed"] = vars_ns.enemy_shuffle_seed.get()
    options_file["graphics_pack"] = vars_ns.selected_pack.get()

    zip_files["options.json"] = json.dumps(options_file)

    zip_bytes = create_zipfile(zip_files)    
    if patch_path:
        with open(patch_path, "wb") as f:
            f.write(zip_bytes)


def create_gfx_pack_frame(parent=None):
    vars_ns = Namespace()
    frame = LabelFrame(parent, text="Graphics Pack Options", padx=8, pady=8)

    def extract_graphics_window():
        file_path = filedialog.askopenfilename(
            filetypes=[("SNES ROM Files", ".sfc"),
                    ("All Files", "*")]
        )
        try:
            extract_graphics_from_rom(file_path)
        except Exception as e:
            messagebox.showerror(title="Error while extracting graphics from Waffles ROM", message=str(e))

    extract_graphics_button = Button(frame, text="Extract Graphics Pack from Waffles ROM", command=extract_graphics_window)

    def export_pack_window():
        folder_path = filedialog.askdirectory()
        try:
            if len(folder_path) == 0:
                raise Exception("No path provided.")
            export_pack_from_folder(folder_path)
        except Exception as e:
            messagebox.showerror(title="Error while saving Graphics Pack to a zip file", message=str(e))

    pack_graphics_button = Button(frame, text="Create Graphics Pack from Folder", command=export_pack_window)

    def select_pack_window():
        nonlocal vars_ns
        pack_reference = open_filename("Select Graphics Pack zip file", filetypes=[("Zip File", [".zip"])])
        vars_ns.selected_pack.set(pack_reference)

    vars_ns.selected_pack = StringVar()
    pack_selected_frame = Frame(frame)
    pack_selected_label = Label(pack_selected_frame, text="Patch file: ")
    pack_selected_label.pack(side=LEFT, fill=X)
    pack_selected_value = Entry(pack_selected_frame, textvariable=vars_ns.selected_pack, state="readonly")
    pack_selected_value.pack(side=RIGHT, fill=X, expand=True)
    
    from Utils import persistent_load
    persistent_settings = persistent_load().get("graphics_pack", {}).get(GAME_NAME, Namespace())
    if hasattr(persistent_settings, "selected_pack"):
        vars_ns.selected_pack.set(persistent_settings.selected_pack)
    pack_selected_button = Button(frame, text="Load Graphics Pack file", command=select_pack_window)

    def save_window():
        nonlocal vars_ns
        save_vars = Namespace()
        save_vars.selected_pack = vars_ns.selected_pack.get()
        persistent_store("graphics_pack", GAME_NAME, save_vars)
        messagebox.showinfo(title="Success", message="Saved global Graphics Pack!")

    save_button = Button(frame, text="Save as Global Graphics Pack", command=save_window)

    separator = Separator(frame, orient=tk.HORIZONTAL)

    pack_selected_frame.pack(side=TOP, fill=X)
    pack_selected_button.pack(side=TOP, fill=X)
    save_button.pack(side=TOP, fill=X)
    separator.pack(fill=X, expand=True, pady=10)
    pack_graphics_button.pack(side=TOP, fill=X)
    extract_graphics_button.pack(side=TOP, fill=X)

    return frame, vars_ns


def create_global_settings_frame(parent=None):
    vars_ns = Namespace()
    frame = LabelFrame(parent, text="Global Settings", padx=8, pady=8)

    vars_ns.lr_wallrun = BooleanVar()
    lr_wallrun_frame = Frame(frame)
    lr_wallrun_check = Checkbutton(lr_wallrun_frame, variable=vars_ns.lr_wallrun)
    lr_wallrun_check.pack(side=LEFT, fill=X)
    lr_wallrun_label = Label(lr_wallrun_frame, text="Wall Run Anywhere requires holding L/R")
    lr_wallrun_label.pack(side=LEFT, fill=X)

    vars_ns.lr_swim = BooleanVar()
    lr_swim_frame = Frame(frame)
    lr_swim_check = Checkbutton(lr_swim_frame, variable=vars_ns.lr_swim)
    lr_swim_check.pack(side=LEFT, fill=X)
    lr_swim_label = Label(lr_swim_frame, text="Fast Swimming requires holding L/R")
    lr_swim_label.pack(side=LEFT, fill=X)

    vars_ns.mute_music = BooleanVar()
    mute_music_frame = Frame(frame)
    mute_music_check = Checkbutton(mute_music_frame, variable=vars_ns.mute_music)
    mute_music_check.pack(side=LEFT, fill=X)
    mute_music_label = Label(mute_music_frame, text="No music")
    mute_music_label.pack(side=LEFT, fill=X)

    def save_window():
        nonlocal vars_ns
        save_vars = Namespace()
        save_vars.lr_wallrun = vars_ns.lr_wallrun.get()
        save_vars.lr_swim = vars_ns.lr_swim.get()
        save_vars.mute_music = vars_ns.mute_music.get()
        persistent_store("global_settings", GAME_NAME, save_vars)
        messagebox.showinfo(title="Success", message="Saved Global Settings!")

    save_button = Button(frame, text="Save Global Settings", command=save_window)

    mute_music_frame.pack(side=TOP, fill=X)
    lr_wallrun_frame.pack(side=TOP, fill=X)
    lr_swim_frame.pack(side=TOP, fill=X)
    save_button.pack(side=TOP, fill=X)

    from Utils import persistent_load
    persistent_settings = persistent_load().get("global_settings", {}).get(GAME_NAME, Namespace())
    if hasattr(persistent_settings, "lr_wallrun"):
        vars_ns.lr_wallrun.set(persistent_settings.lr_wallrun)
    if hasattr(persistent_settings, "lr_swim"):
        vars_ns.lr_swim.set(persistent_settings.lr_swim)
    if hasattr(persistent_settings, "mute_music"):
        vars_ns.mute_music.set(persistent_settings.mute_music)

    return frame


def create_enemy_shuffle_frame(parent=None):
    vars = Namespace()
    frame = LabelFrame(parent, text="Enemy Shuffle Options", padx=8, pady=8)

    vars.enemy_shuffle_active = BooleanVar()
    active_frame = Frame(frame)
    active_check = Checkbutton(active_frame, variable=vars.enemy_shuffle_active)
    active_check.pack(side=LEFT, fill=X)
    active_label = Label(active_frame, text="Enable Enemy Shuffle")
    active_label.pack(side=LEFT, fill=X)

    def entry_callback(P):
        return str.isdigit(P) or P == ""

    vars.enemy_shuffle_seed = StringVar()
    vars.enemy_shuffle_seed.set(12345)
    seed_frame = Frame(frame)
    seed_cmd = seed_frame.register(entry_callback)
    seed_label = Label(seed_frame, text="Seed: ")
    seed_label.pack(side=LEFT, fill=X)
    seed_value = Entry(seed_frame, textvariable=vars.enemy_shuffle_seed, validate="all", validatecommand=(seed_cmd, "%P"))
    seed_value.pack(side=RIGHT, fill=X, expand=True)

    active_frame.pack(side=TOP, fill=X)
    seed_frame.pack(side=TOP, fill=X)

    return frame, vars


def extract_graphics_from_rom(rom_path):
    if not isinstance(rom_path, str) or not os.path.isfile(rom_path):
        return
    
    with open(rom_path, "rb") as f:
        rom = bytearray(f.read())

    player_gfx = rom[0xE0000:0xE0000 + 23808]
    player_extra_gfx = rom[0xE6000:0xE6000 + 1024]
    player_map_gfx = rom[0xE6400:0xE6400 + 1664]
    player_name_gfx = rom[0x179C00:0x179C00 + 160]
    palette_map = rom[0xE6C50:0xE6C50 + 48]
    palette_shared = rom[0x030A0:0x030A0 + 0x7E0]
    yoshi_anim_gfx = rom[0xE8000:0xE8000 + 12288]
    sprites_gfx = rom[0x100000:0x100000 + 144384]

    original_cwd = os.getcwd()
    
    try:
        os.chdir("./data")
        os.mkdir("sprites")
    except FileExistsError:
        pass

    try: 
        os.chdir("./sprites")
        os.mkdir("smw")
    except FileExistsError:
        pass

    try: 
        os.chdir("./smw")
        os.mkdir("output_from_rom")
    except FileExistsError:
        pass

    os.chdir("./output_from_rom")

    output_path = os.getcwd()
    for filename in os.listdir(output_path):
        file_path = os.path.join(output_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    
    with open(f"player.bin", "wb") as f:
        f.write(player_gfx)
    with open(f"player_extra.bin", "wb") as f:
        f.write(player_extra_gfx)
    with open(f"player_map.bin", "wb") as f:
        f.write(player_map_gfx)
    with open(f"player_name.bin", "wb") as f:
        f.write(player_name_gfx)
    base_ow_palette = bytearray(pkgutil.get_data(__name__, "data/palette_ow.mw3"))
    base_ow_palette[0x98*2:0xA0*2] = palette_map[0x00:0x10]
    base_ow_palette[0xA8*2:0xB0*2] = palette_map[0x10:0x20]
    base_ow_palette[0xB8*2:0xC0*2] = palette_map[0x20:0x30]
    with open(f"map.mw3", "wb") as f:
        f.write(base_ow_palette)
    with open(f"shared.mw3", "wb") as f:
        f.write(palette_shared)
    with open(f"yoshi+anim.bin", "wb") as f:
        f.write(yoshi_anim_gfx)
    with open(f"sprites.bin", "wb") as f:
        f.write(sprites_gfx)

    os.startfile(output_path)
    os.chdir(original_cwd)


def export_pack_from_folder(folder_path):
    gfx_32 = open_pack_file([f"{folder_path}/GFX32.bin", f"{folder_path}/player.bin"])
    gfx_33 = open_pack_file([f"{folder_path}/GFX33.bin", f"{folder_path}/yoshi+anim.bin"])
    gfx_00 = open_pack_file([f"{folder_path}/GFX00.bin"])
    gfx_10 = open_pack_file([f"{folder_path}/GFX10.bin"])
    gfx_28 = open_pack_file([f"{folder_path}/GFX28.bin"])
    map_pal = open_pack_file([f"{folder_path}/map.pal", f"{folder_path}/Overworld_palette.pal"])
    shared_pal = open_pack_file([f"{folder_path}/shared.pal", f"{folder_path}/Shared_palette.smwpal"])
    sprites = open_pack_file([f"{folder_path}/sprites.bin"])

    zip_files = dict()

    if gfx_32:
        zip_files["player.bin"] = bytes(gfx_32)

        if gfx_00:
            order = [0x80, 0x91, 0x81, 0x90, 0x82, 0x83]
            gfx_00 += copy_gfx_tiles(gfx_32, order, [5, 32])
            order = [0x69, 0x69, 0x0C, 0x69, 0x1A, 0x1B, 0x0D, 0x69, 0x22, 0x23, 0x32, 0x33, 0x0A, 0x0B, 0x20, 0x21,
                    0x30, 0x31, 0x7E, 0x69, 0x80, 0x4A, 0x81, 0x5B, 0x82, 0x4B, 0x83, 0x5A, 0x84, 0x69, 0x85, 0x85]
            player_small_tiles = copy_gfx_tiles(gfx_00, order, [5, 32])
            zip_files["player_extra.bin"] = bytes(player_small_tiles)

    if gfx_10:
        order = [0x06, 0x07, 0x16, 0x17,
                0x08, 0x09, 0x18, 0x19,
                0x0A, 0x0B, 0x1A, 0x1B,
                0x0C, 0x0D, 0x1C, 0x1D,
                0x0E, 0x0F, 0x1E, 0x1F,
                0x20, 0x21, 0x30, 0x31,
                0x24, 0x25, 0x34, 0x35,
                0x46, 0x47, 0x56, 0x57,
                0x64, 0x65, 0x74, 0x75,
                0x66, 0x67, 0x76, 0x77,
                0x2E, 0x2F, 0x3E, 0x3F,
                0x40, 0x41, 0x50, 0x51,
                0x42, 0x43, 0x52, 0x53]
        player_map_tiles = copy_gfx_tiles(gfx_10, order, [5, 32])
        zip_files["player_map.bin"] = bytes(player_map_tiles)

    if gfx_33:
        zip_files["yoshi+anim.bin"] = bytes(gfx_33)

    if gfx_28:
        order = [0x30, 0x31, 0x32, 0x33, 0x34]
        player_name_tiles = copy_gfx_tiles(gfx_28, order, [4, 16])
        zip_files["player_name.bin"] = bytes(player_name_tiles)

    if shared_pal:
        zip_files["shared.mw3"] = bytes(shared_pal)

    if map_pal:
        map_pal = convert_rgb_to_snes(map_pal) 
        map_colors = bytearray()
        map_colors += bytearray([map_pal[(0x98*2)+(i)] for i in range(16)])
        map_colors += bytearray([map_pal[(0xA8*2)+(i)] for i in range(16)])
        map_colors += bytearray([map_pal[(0xB8*2)+(i)] for i in range(16)])
        zip_files["map.mw3"] = bytes(map_colors)

    if sprites:
        zip_files["sprites.bin"] = bytes(sprites)

    zip_bytes = create_zipfile(zip_files)

    zip_path = filedialog.asksaveasfilename(initialdir = folder_path,
                                            title = "Select file",
                                            filetypes = (("Zip files","*.zip"),("All files","*.*"))
                                            )

    if zip_path:
        with open(zip_path, "wb") as f:
            f.write(zip_bytes)
    


def open_pack_file(paths: list[str]):
    for path in paths:
        if not os.path.isfile(path):
            continue
        with open(path, "rb") as f:
            file_bytes = f.read()
            file_bytes = bytearray(file_bytes)
        return file_bytes
    return None


def create_zipfile(files: dict[str, bytes]) -> io.BytesIO:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for filename, content in files.items():
            zf.writestr(filename, content)
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def launch(*launcher_args):
    main(launcher_args)
