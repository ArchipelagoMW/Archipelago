import tkinter as tk
import argparse
import logging
import os
import zipfile
from itertools import chain

from BaseClasses import MultiWorld
from Options import Choice, Range, Toggle
from Utils import local_path, persistent_store, tkinter_center_window
from worlds.pokemon_emerald.texture_patcher import handle_sprite_pack

logger = logging.getLogger('EmeraldAdjuster')

GAME_EMERALD = "Pokemon Emerald"

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--rom', default='', 
        help='Path to a Pokemon Emerald randomized ROM to adjust.')
    parser.add_argument('--texture-pack', default='',
        help='Path to the Emerald texture pack folder to use.')

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
    from Utils import __version__ as MWVersion

    window = tk.Tk()
    window.wm_title(f"Archipelago {MWVersion} Emerald Adjuster")
    set_icon(window)

    opts = Namespace()

    # Select ROM
    romDialogFrame = Frame(window, padx=8, pady=2)
    romLabel = Label(romDialogFrame, text='Rom to adjust')
    opts.rom = StringVar()
    romEntry = Entry(romDialogFrame, textvariable=opts.rom)
    texturePackFrame = Frame(window, padx=8, pady=2)
    texturePackLabel = Label(texturePackFrame, text='Texture pack to load')
    opts.texture_pack = StringVar()
    texturePackEntry = Entry(texturePackFrame, textvariable=opts.texture_pack)

    def RomSelect():
        rom = filedialog.askopenfilename(filetypes=[("Rom & Patch Files", [".gba", ".apemerald"]), ("All Files", "*")])
        opts.rom.set(rom)
    def TexturePackSelect():
        rom = filedialog.askdirectory()
        opts.texture_pack.set(rom)

    romSelectButton = Button(romDialogFrame, text='Select Rom', command=RomSelect)
    romDialogFrame.pack(side=TOP, expand=True, fill=X)
    romLabel.pack(side=LEFT)
    romEntry.pack(side=LEFT, expand=True, fill=X)
    romSelectButton.pack(side=LEFT)
    texturePackSelectButton = Button(texturePackFrame, text='Select Pack', command=TexturePackSelect)
    texturePackFrame.pack(side=TOP, expand=True, fill=X)
    texturePackLabel.pack(side=LEFT)
    texturePackEntry.pack(side=LEFT, expand=True, fill=X)
    texturePackSelectButton.pack(side=LEFT)

    # romOptionsFrame = LabelFrame(parent, text="Rom options", padx=8, pady=8)
    # TODO: Add pack preview frame (allow sprite extraction, preview existing sprites)

    def adjustRom():
        try:
            guiargs = Namespace()
            guiargs.rom = opts.rom.get()
            guiargs.texture_pack = opts.texture_pack.get()
            path = adjust(guiargs)
        except Exception as e:
            logging.exception(e)
            messagebox.showerror(title="Error while adjusting Rom", message=str(e))
        else:
            messagebox.showinfo(title="Success", message=f"Rom patched successfully to {path}")

    def saveGUISettings():
        guiargs = Namespace()
        guiargs.texture_pack = opts.texture_pack.get()
        persistent_store("adjuster", GAME_EMERALD, guiargs)
        messagebox.showinfo(title="Success", message="Settings saved to persistent storage")

    # Adjust button
    bottomFrame = Frame(window)

    adjustButton = Button(bottomFrame, text='Adjust Rom', command=adjustRom)
    adjustButton.pack(side=LEFT, padx=(5,5))
    saveButton = Button(bottomFrame, text='Save Settings', command=saveGUISettings)
    saveButton.pack(side=LEFT, padx=(5,5))

    bottomFrame.pack(side=TOP, pady=(5,5))

    tkinter_center_window(window)
    window.mainloop()

def set_icon(window):
    logo = tk.PhotoImage(file=local_path('data', 'icon.png'))
    window.tk.call('wm', 'iconphoto', window._w, logo)

def adjust(args):
    buffer = []
    if os.path.splitext(args.rom)[-1] == '.gba':
        # Load up the ROM
        with open(args.rom, 'rb') as stream:
            buffer = bytearray(stream.read())
    elif os.path.splitext(args.rom)[-1] == '.apemerald':
        # TODO: Handle .apemerald file
        pass
    else:
        raise Exception("Invalid file extension; requires .gba or .apemerald")

    # Apply texture pack
    patch = build_texture_pack_patch(args)
    # TODO: Apply patch to .gba
    # Output new file
    path_pieces = os.path.splitext(args.rom)
    adjusted_path = path_pieces[0] + '-adjusted.gba'

    with open(adjusted_path, 'wb') as outfile:
        outfile.write(buffer)
    return adjusted_path

def build_texture_pack_patch(args):
    texture_pack_path = args.texture_pack
    patch = handle_sprite_pack(texture_pack_path)
    return patch

if __name__ == '__main__':
    main()
