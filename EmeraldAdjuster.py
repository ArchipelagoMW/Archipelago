import tkinter as tk
import argparse
import logging
import os

from bps.apply import apply_to_bytearrays as apply_bps_patch

from Utils import local_path, persistent_store, tkinter_center_window, data_to_bps_patch
from worlds.pokemon_emerald.sprite_patcher import handle_sprite_pack

logger = logging.getLogger('EmeraldAdjuster')

GAME_EMERALD = "Pokemon Emerald"

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--rom', default='', 
        help='Path to a Pokemon Emerald randomized ROM to adjust.')
    parser.add_argument('--sprite-pack', default='',
        help='Path to the Emerald sprite pack folder to use.')

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
    romLabel = Label(romDialogFrame, text='Original Rom')
    opts.rom = StringVar()
    romEntry = Entry(romDialogFrame, textvariable=opts.rom)
    patchDialogFrame = Frame(window, padx=8, pady=2)
    patchLabel = Label(patchDialogFrame, text='Patch / Modified Rom')
    opts.patch = StringVar()
    patchEntry = Entry(patchDialogFrame, textvariable=opts.patch)
    spritePackFrame = Frame(window, padx=8, pady=2)
    spritePackLabel = Label(spritePackFrame, text='Sprite pack to load')
    opts.sprite_pack = StringVar()
    spritePackEntry = Entry(spritePackFrame, textvariable=opts.sprite_pack)

    def RomSelect():
        rom = filedialog.askopenfilename(filetypes=[("Rom", [".gba"]), ("All Files", "*")])
        opts.rom.set(rom)
    def PatchSelect():
        patch = filedialog.askopenfilename(filetypes=[("Rom & Patch Files", [".gba", ".apemerald"]), ("All Files", "*")])
        opts.patch.set(patch)
    def SpritePackSelect():
        rom = filedialog.askdirectory()
        opts.sprite_pack.set(rom)

    romSelectButton = Button(romDialogFrame, text='Select Rom', command=RomSelect)
    romDialogFrame.pack(side=TOP, expand=True, fill=X)
    romLabel.pack(side=LEFT)
    romEntry.pack(side=LEFT, expand=True, fill=X)
    romSelectButton.pack(side=LEFT)
    patchSelectButton = Button(patchDialogFrame, text='Select Patch/Rom', command=PatchSelect)
    patchDialogFrame.pack(side=TOP, expand=True, fill=X)
    patchLabel.pack(side=LEFT)
    patchEntry.pack(side=LEFT, expand=True, fill=X)
    patchSelectButton.pack(side=LEFT)
    spritePackSelectButton = Button(spritePackFrame, text='Select Pack', command=SpritePackSelect)
    spritePackFrame.pack(side=TOP, expand=True, fill=X)
    spritePackLabel.pack(side=LEFT)
    spritePackEntry.pack(side=LEFT, expand=True, fill=X)
    spritePackSelectButton.pack(side=LEFT)

    # romOptionsFrame = LabelFrame(parent, text="Rom options", padx=8, pady=8)
    # TODO: Add pack preview frame (allow sprite extraction, preview existing sprites)

    def adjustRom():
        try:
            guiargs = Namespace()
            guiargs.rom = opts.rom.get()
            guiargs.patch = opts.patch.get()
            guiargs.sprite_pack = opts.sprite_pack.get()
            path = adjust(guiargs)
        except Exception as e:
            logging.exception(e)
            messagebox.showerror(title="Error while adjusting Rom", message=str(e))
        else:
            messagebox.showinfo(title="Success", message=f"Rom patched successfully to {path}")

    def saveGUISettings():
        guiargs = Namespace()
        guiargs.sprite_pack = opts.sprite_pack.get()
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
    if not args.patch:
        raise Exception("A patch file or a patched ROM is required!")
    if os.path.splitext(args.patch)[-1] == '.gba':
        # Load up the patched ROM directly
        with open(args.patch, 'rb') as stream:
            ap_rom = bytearray(stream.read())
    elif os.path.splitext(args.patch)[-1] == '.apemerald':
        # Load the original rom and patch it as an AP rom
        if not args.rom:
            raise Exception("The original ROM is needed if a patch is given!")
        with open(args.rom, 'rb') as stream:
            rom = bytearray(stream.read())
        # TODO: Handle .apemerald file
        ap_rom = rom
        pass
    else:
        raise Exception("Invalid file extension; requires .gba or .apemerald")

    # Build sprite pack patch & apply patch
    if not args.sprite_pack:
        raise Exception("A sprite pack is required!")
    sprite_pack_bps_patch = build_sprite_pack_patch(args.sprite_pack, ap_rom)
    adjusted_ap_rom = bytearray(len(ap_rom))
    apply_bps_patch(sprite_pack_bps_patch, ap_rom, adjusted_ap_rom)

    path_pieces = os.path.splitext(args.rom or args.patch)
    adjusted_path = path_pieces[0] + '-adjusted.gba'
    with open(adjusted_path, 'wb') as outfile:
        outfile.write(adjusted_ap_rom)
    return adjusted_path

def build_sprite_pack_patch(sprite_pack, ap_rom):
    sprite_pack_path = sprite_pack
    sprite_pack_data = handle_sprite_pack(sprite_pack_path, ap_rom)
    sprite_pack_bps_patch = data_to_bps_patch(sprite_pack_data, ap_rom)
    return sprite_pack_bps_patch

if __name__ == '__main__':
    main()
