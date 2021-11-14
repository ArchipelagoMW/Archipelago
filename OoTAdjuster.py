import tkinter as tk
import shutil
import argparse
import logging
import random
import os
from itertools import chain

from BaseClasses import MultiWorld
from Options import Choice, Range, Toggle
from worlds.oot import OOTWorld
from worlds.oot.Cosmetics import patch_cosmetics, format_cosmetic_option_result
from worlds.oot.Options import cosmetic_options, sfx_options
from worlds.oot.Rom import Rom, compress_rom_file
from Utils import output_path, local_path, open_file

logger = logging.getLogger('OoTAdjuster')

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--rom', default='', 
        help='Path to an OoT randomized ROM to adjust.')
    for name, option in chain(cosmetic_options.items(), sfx_options.items()):
        parser.add_argument('--'+name, default=None,
            help=option.__doc__)
    parser.add_argument('--is_glitched', default=False, action='store_true',
        help='Setting this to true will enable protection on kokiri tunic colors for weirdshot.')
    parser.add_argument('--deathlink',
        help='Enable DeathLink system', action='store_true')

    args = parser.parse_args()
    if not os.path.isfile(args.rom):
        adjustGUI()
    else:
        adjust(args)

def adjustGUI():
    from tkinter import Tk, LEFT, BOTTOM, TOP, E, W, \
        StringVar, IntVar, Checkbutton, Frame, Label, X, Entry, Button, \
        OptionMenu, filedialog, messagebox, ttk
    from argparse import Namespace
    from Main import __version__ as MWVersion

    window = tk.Tk()
    window.wm_title(f"Archipelago {MWVersion} OoT Adjuster")
    set_icon(window)

    # Select ROM
    romDialogFrame = Frame(window)
    romLabel = Label(romDialogFrame, text='Rom to adjust')
    romVar = StringVar()
    romEntry = Entry(romDialogFrame, textvariable=romVar)

    def RomSelect():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".z64", ".n64")), ("All Files", "*")])
        romVar.set(rom)

    romSelectButton = Button(romDialogFrame, text='Select Rom', command=RomSelect)
    romDialogFrame.pack(side=TOP, expand=True, fill=X)
    romLabel.pack(side=LEFT)
    romEntry.pack(side=LEFT, expand=True, fill=X)
    romSelectButton.pack(side=LEFT)

    # Cosmetic options
    romSettingsFrame = Frame(window)
    opts = Namespace()

    def dropdown_option(type, option_name, row, column):
        if type == 'cosmetic':
            option = cosmetic_options[option_name]
        elif type == 'sfx':
            option = sfx_options[option_name]
        optionFrame = Frame(romSettingsFrame)
        optionFrame.grid(row=row, column=column, sticky=E)
        optionLabel = Label(optionFrame, text=option.displayname)
        optionLabel.pack(side=LEFT)
        setattr(opts, option_name, StringVar())
        getattr(opts, option_name).set(option.name_lookup[option.default])
        optionMenu = OptionMenu(optionFrame, getattr(opts, option_name), *option.name_lookup.values())
        optionMenu.pack(side=LEFT)

    dropdown_option('cosmetic', 'default_targeting', 0, 0)
    dropdown_option('cosmetic', 'display_dpad', 0, 1)
    dropdown_option('cosmetic', 'correct_model_colors', 0, 2)
    dropdown_option('cosmetic', 'background_music', 1, 0)
    dropdown_option('cosmetic', 'fanfares', 1, 1)
    dropdown_option('cosmetic', 'ocarina_fanfares', 1, 2)
    dropdown_option('cosmetic', 'kokiri_color', 2, 0)
    dropdown_option('cosmetic', 'goron_color', 2, 1)
    dropdown_option('cosmetic', 'zora_color', 2, 2)
    dropdown_option('cosmetic', 'silver_gauntlets_color', 3, 0)
    dropdown_option('cosmetic', 'golden_gauntlets_color', 3, 1)
    dropdown_option('cosmetic', 'mirror_shield_frame_color', 3, 2)
    dropdown_option('cosmetic', 'navi_color_default_inner', 4, 0)
    dropdown_option('cosmetic', 'navi_color_default_outer', 4, 1)
    dropdown_option('cosmetic', 'navi_color_enemy_inner', 5, 0)
    dropdown_option('cosmetic', 'navi_color_enemy_outer', 5, 1)
    dropdown_option('cosmetic', 'navi_color_npc_inner', 6, 0)
    dropdown_option('cosmetic', 'navi_color_npc_outer', 6, 1)
    dropdown_option('cosmetic', 'navi_color_prop_inner', 7, 0)
    dropdown_option('cosmetic', 'navi_color_prop_outer', 7, 1)
    # sword_trail_duration, 8, 2
    dropdown_option('cosmetic', 'sword_trail_color_inner', 8, 0)
    dropdown_option('cosmetic', 'sword_trail_color_outer', 8, 1)
    dropdown_option('cosmetic', 'bombchu_trail_color_inner', 9, 0)
    dropdown_option('cosmetic', 'bombchu_trail_color_outer', 9, 1)
    dropdown_option('cosmetic', 'boomerang_trail_color_inner', 10, 0)
    dropdown_option('cosmetic', 'boomerang_trail_color_outer', 10, 1)
    dropdown_option('cosmetic', 'heart_color', 11, 0)
    dropdown_option('cosmetic', 'magic_color', 12, 0)
    dropdown_option('cosmetic', 'a_button_color', 11, 1)
    dropdown_option('cosmetic', 'b_button_color', 11, 2)
    dropdown_option('cosmetic', 'c_button_color', 12, 1)
    dropdown_option('cosmetic', 'start_button_color', 12, 2)

    dropdown_option('sfx', 'sfx_navi_overworld', 14, 0)
    dropdown_option('sfx', 'sfx_navi_enemy', 14, 1)
    dropdown_option('sfx', 'sfx_low_hp', 14, 2)
    dropdown_option('sfx', 'sfx_menu_cursor', 15, 0)
    dropdown_option('sfx', 'sfx_menu_select', 15, 1)
    dropdown_option('sfx', 'sfx_nightfall', 15, 2)
    dropdown_option('sfx', 'sfx_horse_neigh', 16, 0)
    dropdown_option('sfx', 'sfx_hover_boots', 16, 1)
    dropdown_option('sfx', 'sfx_ocarina', 16, 2)

    # Special cases
    # Sword trail duration is a range
    option = cosmetic_options['sword_trail_duration']
    optionFrame = Frame(romSettingsFrame)
    optionFrame.grid(row=8, column=2, sticky=E)
    optionLabel = Label(optionFrame, text=option.displayname)
    optionLabel.pack(side=LEFT)
    setattr(opts, 'sword_trail_duration', StringVar())
    getattr(opts, 'sword_trail_duration').set(option.default)
    optionMenu = OptionMenu(optionFrame, getattr(opts, 'sword_trail_duration'), *range(4, 21))
    optionMenu.pack(side=LEFT)

    # Glitched is a checkbox
    opts.is_glitched = IntVar(value=0)
    glitched_checkbox = Checkbutton(romSettingsFrame, text="Glitched Logic?", variable=opts.is_glitched)
    glitched_checkbox.grid(row=17, column=0, sticky=W)

    # Deathlink is a checkbox
    opts.deathlink = IntVar(value=0)
    deathlink_checkbox = Checkbutton(romSettingsFrame, text="DeathLink (Team Deaths)", variable=opts.deathlink)
    deathlink_checkbox.grid(row=17, column=1, sticky=W)

    romSettingsFrame.pack(side=TOP)

    def adjustRom():
        try:
            guiargs = Namespace()
            guiargs.rom = romVar.get()
            options = vars(opts)
            for o in options:
                result = options[o].get()
                if result == 'true':
                    result = True
                if result == 'false':
                    result = False
                setattr(guiargs, o, result)
            guiargs.sword_trail_duration = int(guiargs.sword_trail_duration)
            path = adjust(guiargs)
        except Exception as e:
            logging.exception(e)
            messagebox.showerror(title="Error while adjusting Rom", message=str(e))
        else:
            messagebox.showinfo(title="Success", message=f"Rom patched successfully to {path}")

    # Adjust button
    bottomFrame = Frame(window)
    adjustButton = Button(bottomFrame, text='Adjust Rom', command=adjustRom)
    adjustButton.pack(side=BOTTOM, padx=(5, 5))
    bottomFrame.pack(side=BOTTOM, pady=(5, 5))

    window.mainloop()

def set_icon(window):
    logo = tk.PhotoImage(file=local_path('data', 'icon.png'))
    window.tk.call('wm', 'iconphoto', window._w, logo)

def adjust(args):
    # Create a fake world and OOTWorld to use as a base
    world = MultiWorld(1)
    world.slot_seeds = {1: random}
    ootworld = OOTWorld(world, 1)
    # Set options in the fake OOTWorld
    for name, option in chain(cosmetic_options.items(), sfx_options.items()):
        result = getattr(args, name, None)
        if result is None:
            if issubclass(option, Choice):
                result = option.name_lookup[option.default]
            elif issubclass(option, Range) or issubclass(option, Toggle):
                result = option.default
            else:
                raise Exception("Unsupported option type")
        setattr(ootworld, name, result)
    ootworld.logic_rules = 'glitched' if args.is_glitched else 'glitchless'
    ootworld.death_link = args.deathlink
    # Load up the ROM
    rom = Rom(file=args.rom, force_use=True)
    # Call patch_cosmetics
    patch_cosmetics(ootworld, rom)
    # Output new file
    path_pieces = os.path.splitext(args.rom)
    decomp_path = path_pieces[0] + '-adjusted' + path_pieces[1]
    comp_path = path_pieces[0] + '-adjusted-comp' + path_pieces[1]
    rom.write_to_file(decomp_path)
    compress_rom_file(decomp_path, comp_path)
    os.remove(decomp_path)
    return comp_path

if __name__ == '__main__':
    main()
