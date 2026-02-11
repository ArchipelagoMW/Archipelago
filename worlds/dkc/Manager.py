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
from tkinter import Tk, Frame, Label, StringVar, IntVar, Entry, filedialog, messagebox, Button, LEFT, X, Y, BOTH, TOP, LabelFrame, \
    Checkbutton, E, W, BOTTOM, RIGHT, font as font, BooleanVar, Canvas, INSERT, Spinbox
from tkinter.ttk import Separator
from tkinter.constants import DISABLED, NORMAL
from Utils import persistent_store, get_adjuster_settings_no_defaults, tkinter_center_window, open_filename

from .SNESGraphics import copy_gfx_tiles, convert_rgb_to_snes

import ModuleUpdate
ModuleUpdate.update()

GAME_NAME = "Donkey Kong Country"
WINDOW_MIN_HEIGHT = 380
WINDOW_MIN_WIDTH = 660

class ArgumentDefaultsHelpFormatter(argparse.RawTextHelpFormatter):

    def _get_help_string(self, action):
        return textwrap.dedent(action.help)
    

def get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    #parser.add_argument("--rom", default="AP_Waffle.sfc", help="Path to a Waffles ROM to adjust.")

    return parser


def main(launcher_args):
    parser = get_argparser()
    args = parser.parse_args(launcher_args, namespace=get_adjuster_settings_no_defaults(GAME_NAME))

    manager_gui()


def manager_gui():    
    manager_window = Tk()
    manager_window.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
    manager_window.resizable(True, False)
    manager_window.wm_title(f"Donkey Kong Country Adjuster")

    left_frame = Frame(manager_window)
    right_frame = Frame(manager_window)

    linked_frame, linked_vars = create_linked_frame(left_frame)
    misc_frame, misc_vars = create_misc_frame(left_frame)
    boss_frame, boss_vars = create_boss_frame(right_frame)
    file_frame, vars_ns = create_file_frame(left_frame, (linked_vars, misc_vars, boss_vars))

    file_frame.pack(side=TOP, padx=8, pady=8, fill=BOTH)
    linked_frame.pack(side=TOP, padx=8, pady=8, fill=BOTH)
    misc_frame.pack(side=TOP, padx=8, pady=8, fill=BOTH)

    boss_frame.pack(side=TOP, padx=8, pady=8, fill=BOTH)

    left_frame.pack(side=LEFT, fill=BOTH, expand=True)
    right_frame.pack(side=LEFT, fill=BOTH, expand=True)

    tkinter_center_window(manager_window)
    manager_window.mainloop()


def create_file_frame(parent=None, external_vars=None):
    vars_ns = Namespace()
    if external_vars:
        for var_group in external_vars:
            for key, value in vars(var_group).items():
                setattr(vars_ns, key, value)

    frame = LabelFrame(parent, text="File Manager", padx=8, pady=8)

    vars_ns.patch_path = StringVar()
    load_frame = Frame(frame)
    file_label = Label(load_frame, text="Patch file: ")
    file_label.pack(side=LEFT, fill=X)
    file_value = Entry(load_frame, textvariable=vars_ns.patch_path, state="readonly")
    file_value.pack(side=RIGHT, fill=X, expand=True)

    def load_patch_window():
        nonlocal vars_ns

        file_path = filedialog.askopenfilename(
            filetypes=[("DKC Patch Files", ".apdkc")])
        try:
            vars_ns.patch_path.set(file_path)
            load_data_from_patch(file_path, vars_ns)
        except Exception as e:
            messagebox.showerror(title="Error while reading DKC Patch file", message=str(e))

    def save_patch_window():
        nonlocal vars_ns
        if "" == vars_ns.patch_path.get():
            return
        save_adjusted_data(vars_ns)
        messagebox.showinfo(title="Success", message="Saved changes to DKC Patch file!")

    load_button = Button(frame, text="Load DKC Patch", command=load_patch_window)
    save_button = Button(frame, text="Save changes to DKC Patch", command=save_patch_window)

    load_frame.pack(side=TOP, fill=X)
    load_button.pack(side=TOP, fill=X)
    save_button.pack(side=TOP, fill=X)

    return frame, vars_ns


def load_data_from_patch(patch_path, vars_ns):
    file = zipfile.ZipFile(patch_path)
    options_file = json.loads(file.read("data.json").decode("UTF-8"))

    if "death_link" in options_file.keys():
        vars_ns.death_link_active.set(options_file["death_link"])
    if "energy_link" in options_file.keys():
        vars_ns.energy_link_active.set(options_file["energy_link"])
    if "trap_link" in options_file.keys():
        vars_ns.trap_link_active.set(options_file["trap_link"])
    if "kong_letters" in options_file.keys():
        vars_ns.kong_letters.set(options_file["kong"])
    if "master_necky_hp" in options_file.keys():
        vars_ns.master_necky_hp.set(options_file["master_necky_hp"])
    if "master_necky_double" in options_file.keys():
        vars_ns.master_necky_double.set(options_file["master_necky_double"])
    if "master_necky_snr_hp" in options_file.keys():
        vars_ns.master_necky_snr_hp.set(options_file["master_necky_snr_hp"])
    if "queen_b_hp" in options_file.keys():
        vars_ns.queen_b_hp.set(options_file["queen_b_hp"])
    if "very_gnawty_hp" in options_file.keys():
        vars_ns.very_gnawty_hp.set(options_file["very_gnawty_hp"])
    if "very_gnawty_army" in options_file.keys():
        vars_ns.very_gnawty_army.set(options_file["very_gnawty_army"])
    if "really_gnawty_hp" in options_file.keys():
        vars_ns.really_gnawty_hp.set(options_file["really_gnawty_hp"])
    if "really_gnawty_army" in options_file.keys():
        vars_ns.really_gnawty_army.set(options_file["really_gnawty_army"])
    if "dumb_drum_stun" in options_file.keys():
        vars_ns.dumb_drum_stun.set(options_file["dumb_drum_stun"])
    if "dumb_drum_enemy_drop" in options_file.keys():
        vars_ns.dumb_drum_enemy_drop.set(options_file["dumb_drum_enemy_drop"])


def save_adjusted_data(vars_ns):
    patch_path = vars_ns.patch_path.get()
    file = zipfile.ZipFile(patch_path)

    zip_files = dict()
    for file_name in file.namelist():
        zip_files[file_name] = file.read(file_name)

    options_file = json.loads(file.read("data.json").decode("UTF-8"))
    options_file["death_link"] = vars_ns.death_link_active.get()
    options_file["energy_link"] = vars_ns.energy_link_active.get()
    options_file["trap_link"] = vars_ns.trap_link_active.get()
    options_file["kong"] = vars_ns.kong_letters.get()
    options_file["master_necky_hp"] = vars_ns.master_necky_hp.get()
    options_file["master_necky_double"] = vars_ns.master_necky_double.get()
    options_file["master_necky_snr_hp"] = vars_ns.master_necky_snr_hp.get()
    options_file["queen_b_hp"] = vars_ns.queen_b_hp.get()
    options_file["very_gnawty_hp"] = vars_ns.very_gnawty_hp.get()
    options_file["very_gnawty_army"] = vars_ns.very_gnawty_army.get()
    options_file["really_gnawty_hp"] = vars_ns.really_gnawty_hp.get()
    options_file["really_gnawty_army"] = vars_ns.really_gnawty_army.get()
    options_file["dumb_drum_enemy_drop"] = vars_ns.dumb_drum_enemy_drop.get()
    options_file["dumb_drum_stun"] = vars_ns.dumb_drum_stun.get()

    zip_files["data.json"] = json.dumps(options_file)

    zip_bytes = create_zipfile(zip_files)    
    if patch_path:
        with open(patch_path, "wb") as f:
            f.write(zip_bytes)


def create_linked_frame(parent=None):
    vars = Namespace()
    frame = LabelFrame(parent, text="Linked Options", padx=8, pady=8)

    vars.death_link_active = BooleanVar()
    death_frame = Frame(frame)
    death_check = Checkbutton(death_frame, variable=vars.death_link_active)
    death_check.pack(side=LEFT, fill=X)
    death_label = Label(death_frame, text="Enable Death Link")
    death_label.pack(side=LEFT, fill=X)

    vars.energy_link_active = BooleanVar()
    energy_frame = Frame(frame)
    energy_check = Checkbutton(energy_frame, variable=vars.energy_link_active)
    energy_check.pack(side=LEFT, fill=X)
    energy_label = Label(energy_frame, text="Enable Energy Link")
    energy_label.pack(side=LEFT, fill=X)

    vars.trap_link_active = BooleanVar()
    trap_frame = Frame(frame)
    trap_check = Checkbutton(trap_frame, variable=vars.trap_link_active)
    trap_check.pack(side=LEFT, fill=X)
    trap_label = Label(trap_frame, text="Enable Trap Link")
    trap_label.pack(side=LEFT, fill=X)

    death_frame.pack(side=TOP, fill=X)
    energy_frame.pack(side=TOP, fill=X)
    trap_frame.pack(side=TOP, fill=X)

    return frame, vars


def create_misc_frame(parent=None):
    vars = Namespace()
    frame = LabelFrame(parent, text="Misc Options", padx=8, pady=8)
    vars.kong_letters = StringVar()
    
    def force_uppercase(*args):
        value = vars.kong_letters.get()
        value = ''.join(c for c in value if 'A' <= c.upper() <= 'Z')
        vars.kong_letters.set(value.upper()[:4])
    
    letters_frame = Frame(frame)
    letters_label = Label(letters_frame, text="KONG Letters: ")
    vars.kong_letters.trace_add("write", force_uppercase)
    vars.kong_letters.set("KONG")
    letters_label.pack(side=LEFT, fill=X)
    letters_value = Entry(letters_frame, textvariable=vars.kong_letters)
    letters_value.pack(side=RIGHT, fill=X, expand=True)

    letters_frame.pack(side=TOP, fill=X)
    
    return frame, vars


def create_boss_frame(parent=None):
    vars = Namespace()
    frame = LabelFrame(parent, text="Boss Config Options", padx=8, pady=8)

    vars.master_necky_hp = IntVar()
    master_necky_hp_frame = Frame(frame)
    master_necky_hp_spin = Spinbox(master_necky_hp_frame, textvariable=vars.master_necky_hp, from_=1, to=9, width=3, relief="sunken",
                                   repeatdelay=500, repeatinterval=100)
    master_necky_hp_label = Label(master_necky_hp_frame, text="Master Necky HP: ")
    master_necky_hp_label.pack(side=LEFT, fill=X)
    master_necky_hp_spin.pack(side=LEFT, fill=X)
    
    vars.master_necky_double = BooleanVar()
    master_necky_double_frame = Frame(frame)
    master_necky_double_check = Checkbutton(master_necky_double_frame, variable=vars.master_necky_double)
    master_necky_double_check.pack(side=LEFT, fill=X)
    master_necky_double_label = Label(master_necky_double_frame, text="Master Necky double fight (may cause lag)")
    master_necky_double_label.pack(side=LEFT, fill=X)

    vars.master_necky_snr_hp = IntVar()
    master_necky_snr_hp_frame = Frame(frame)
    master_necky_snr_hp_spin = Spinbox(master_necky_snr_hp_frame, textvariable=vars.master_necky_snr_hp, from_=1, to=9, width=3, relief="sunken",
                                   repeatdelay=500, repeatinterval=100)
    master_necky_snr_hp_label = Label(master_necky_snr_hp_frame, text="Master Necky Snr HP: ")
    master_necky_snr_hp_label.pack(side=LEFT, fill=X)
    master_necky_snr_hp_spin.pack(side=LEFT, fill=X)

    vars.queen_b_hp = IntVar()
    queen_b_hp_frame = Frame(frame)
    queen_b_hp_spin = Spinbox(queen_b_hp_frame, textvariable=vars.queen_b_hp, from_=1, to=9, width=3, relief="sunken",
                                   repeatdelay=500, repeatinterval=100)
    queen_b_hp_label = Label(queen_b_hp_frame, text="Queen B HP: ")
    queen_b_hp_label.pack(side=LEFT, fill=X)
    queen_b_hp_spin.pack(side=LEFT, fill=X)
    
    vars.very_gnawty_hp = IntVar()
    very_gnawty_hp_frame = Frame(frame)
    very_gnawty_hp_spin = Spinbox(very_gnawty_hp_frame, textvariable=vars.very_gnawty_hp, from_=1, to=9, width=3, relief="sunken",
                                   repeatdelay=500, repeatinterval=100)
    very_gnawty_hp_label = Label(very_gnawty_hp_frame, text="Very Gnawty HP: ")
    very_gnawty_hp_label.pack(side=LEFT, fill=X)
    very_gnawty_hp_spin.pack(side=LEFT, fill=X)
    
    vars.very_gnawty_army = BooleanVar()
    very_gnawty_army_frame = Frame(frame)
    very_gnawty_army_check = Checkbutton(very_gnawty_army_frame, variable=vars.very_gnawty_army)
    very_gnawty_army_check.pack(side=LEFT, fill=X)
    very_gnawty_army_label = Label(very_gnawty_army_frame, text="Very Gnawty spawns an Army when hurt")
    very_gnawty_army_label.pack(side=LEFT, fill=X)
    
    vars.really_gnawty_hp = IntVar()
    really_gnawty_hp_frame = Frame(frame)
    really_gnawty_hp_spin = Spinbox(really_gnawty_hp_frame, textvariable=vars.really_gnawty_hp, from_=1, to=9, width=3, relief="sunken",
                                   repeatdelay=500, repeatinterval=100)
    really_gnawty_hp_label = Label(really_gnawty_hp_frame, text="Really Gnawty HP: ")
    really_gnawty_hp_label.pack(side=LEFT, fill=X)
    really_gnawty_hp_spin.pack(side=LEFT, fill=X)
    
    vars.really_gnawty_army = BooleanVar()
    really_gnawty_army_frame = Frame(frame)
    really_gnawty_army_check = Checkbutton(really_gnawty_army_frame, variable=vars.really_gnawty_army)
    really_gnawty_army_check.pack(side=LEFT, fill=X)
    really_gnawty_army_label = Label(really_gnawty_army_frame, text="Really Gnawty spawns two Army when hurt")
    really_gnawty_army_label.pack(side=LEFT, fill=X)
    
    vars.dumb_drum_enemy_drop = BooleanVar()
    dumb_drum_enemy_drop_frame = Frame(frame)
    dumb_drum_enemy_drop_check = Checkbutton(dumb_drum_enemy_drop_frame, variable=vars.dumb_drum_enemy_drop)
    dumb_drum_enemy_drop_check.pack(side=LEFT, fill=X)
    dumb_drum_enemy_drop_label = Label(dumb_drum_enemy_drop_frame, text="Dumb Drum drops additional enemies")
    dumb_drum_enemy_drop_label.pack(side=LEFT, fill=X)
    
    vars.dumb_drum_stun = BooleanVar()
    dumb_drum_stun_frame = Frame(frame)
    dumb_drum_stun_check = Checkbutton(dumb_drum_stun_frame, variable=vars.dumb_drum_stun)
    dumb_drum_stun_check.pack(side=LEFT, fill=X)
    dumb_drum_stun_label = Label(dumb_drum_stun_frame, text="Dumb Drum can stun players (jank)")
    dumb_drum_stun_label.pack(side=LEFT, fill=X)
    
    separator_very_gnawty = Separator(frame, orient=tk.HORIZONTAL)
    separator_master_necky = Separator(frame, orient=tk.HORIZONTAL)
    separator_queen_b = Separator(frame, orient=tk.HORIZONTAL)
    separator_really_gnawty = Separator(frame, orient=tk.HORIZONTAL)
    separator_drum = Separator(frame, orient=tk.HORIZONTAL)

    very_gnawty_hp_frame.pack(side=TOP, fill=X)
    very_gnawty_army_frame.pack(side=TOP, fill=X)
    separator_very_gnawty.pack(fill=X, expand=True, pady=10)
    master_necky_hp_frame.pack(side=TOP, fill=X)
    master_necky_double_frame.pack(side=TOP, fill=X)
    separator_master_necky.pack(fill=X, expand=True, pady=10)
    queen_b_hp_frame.pack(side=TOP, fill=X)
    separator_queen_b.pack(fill=X, expand=True, pady=10)
    really_gnawty_hp_frame.pack(side=TOP, fill=X)
    really_gnawty_army_frame.pack(side=TOP, fill=X)
    separator_really_gnawty.pack(fill=X, expand=True, pady=10)
    dumb_drum_enemy_drop_frame.pack(side=TOP, fill=X)
    dumb_drum_stun_frame.pack(side=TOP, fill=X)
    separator_drum.pack(fill=X, expand=True, pady=10)
    master_necky_snr_hp_frame.pack(side=TOP, fill=X)

    return frame, vars


def create_zipfile(files: dict[str, bytes]) -> io.BytesIO:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for filename, content in files.items():
            zf.writestr(filename, content)
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def launch(*launcher_args):
    main(launcher_args)

