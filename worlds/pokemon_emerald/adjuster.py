import tkinter as tk
import argparse
import logging
import os
import math

from bps.apply import apply_to_bytearrays as apply_bps_patch

from Utils import local_path, persistent_store, get_adjuster_settings, get_adjuster_settings_no_defaults, \
    tkinter_center_window, data_to_bps_patch
from worlds.pokemon_emerald.sprite_patcher import handle_sprite_pack, extract_palette_from_file, \
    extract_sprites, validate_sprite_pack, POKEMON_FOLDERS, TRAINER_FOLDERS
from argparse import Namespace

logger = logging.getLogger('EmeraldAdjuster')
isSpritePackValid = False
isPatchValid = False
objectFolders = []
ap_rom = None

GAME_EMERALD = "Pokemon Emerald"

async def main():
    parser = get_argparser()
    args = parser.parse_args(namespace=get_adjuster_settings_no_defaults(GAME_EMERALD))
    
    logging.basicConfig(format='%(message)s', level=logging.INFO)

    global objectFolders
    objectFolders = TRAINER_FOLDERS + POKEMON_FOLDERS

    args = parser.parse_args()
    if not os.path.isfile(args.patch):
        adjustGUI()
    else:
        adjust(args)

def get_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--patch', default='', help='Path to a Pokemon Emerald AP-randomized ROM to adjust or path to a .apemerald patch file.')
    parser.add_argument('--sprite-pack', default='', help='Path to the Emerald sprite pack folder to use.')
    return parser

def adjustGUI():
    adjuster_settings = get_adjuster_settings(GAME_EMERALD)

    from tkinter import LEFT, TOP, X, StringVar, LabelFrame, Frame, Label, \
        Entry, Button, OptionMenu, PhotoImage, filedialog, messagebox
    from Utils import __version__ as MWVersion

    window = tk.Tk()
    window.wm_title(f"Archipelago {MWVersion} Emerald Adjuster")
    set_icon(window)

    mainWindowFrame = Frame(window, padx=8, pady=8)
    mainWindowFrame.pack(side=TOP, expand=True, fill=X)

    opts = Namespace()

    ##############################################
    # ROM/Patch Selection, Sprite Pack Selection #
    ##############################################

    patchDialogFrame = Frame(mainWindowFrame, padx=8, pady=2)
    patchLabel = Label(patchDialogFrame, text='Patch / Modified Rom')
    opts.patch = StringVar()
    patchEntry = Entry(patchDialogFrame, textvariable=opts.patch)
    spritePackFrame = Frame(mainWindowFrame, padx=8, pady=2)
    spritePackLabel = Label(spritePackFrame, text='Sprite pack to load')
    opts.sprite_pack = StringVar()
    spritePackEntry = Entry(spritePackFrame, textvariable=opts.sprite_pack)

    def PatchSelect(_forcedPatch = None):
        global isPatchValid

        if not _forcedPatch is None:
            patch = _forcedPatch
        else:
            patch = filedialog.askopenfilename(initialfile=opts.patch.get() if isPatchValid else None, filetypes=[("Rom & Patch Files", [".gba", ".apemerald"]), ("All Files", "*")])
        opts.patch.set(patch)

        isPatchValid = len(patch) > 0 and os.path.exists(patch)
        tryValidateSpritePack(opts.sprite_pack.get(), True)

        if not isPatchValid:
            spriteExtractorFrame.pack_forget()
        else:
            spritePreviewFrame.pack_forget()
            bottomFrame.pack_forget()
            spriteExtractorFrame.pack(side=TOP, expand=True, fill=X, pady=5)
            if isSpritePackValid:
                spritePreviewFrame.pack(side=TOP, expand=True, fill=X, pady=5)
            bottomFrame.pack(side=TOP, pady=5)
    
    def SetCurrentSpriteFolder(folder: str):
        currentSpriteFolder.set(folder)
        SwitchSpriteFolder(folder)

    def SpritePackSelect(_forcedSpritePack = None):
        global isSpritePackValid

        if not _forcedSpritePack is None:
            spritePack = _forcedSpritePack
        else:
            spritePack = filedialog.askdirectory(initialdir=opts.sprite_pack.get() if isSpritePackValid else None, mustexist=True)
        opts.sprite_pack.set(spritePack)
        isSpritePackValid = len(spritePack) > 0 and os.path.isdir(spritePack)
        tryValidateSpritePack(opts.sprite_pack.get())

        SwitchSpriteFolder('--------')

        # Reset var and delete all old options
        currentSpriteFolder.set('--------')
        folderSelector['menu'].delete(0, 'end')
        folderSelector['menu'].add_command(label='--------', command=lambda value='--------':SetCurrentSpriteFolder(value))

        if not isSpritePackValid:
            spritePreviewFrame.pack_forget()
            return
        else:
            bottomFrame.pack_forget()
            spritePreviewFrame.pack(side=TOP, expand=True, fill=X, pady=5)
            bottomFrame.pack(side=TOP, pady=5)
        
        # Detect existing object folders and list them
        existingFolders = []
        for dir in os.listdir(spritePack):
            fullDir = os.path.join(spritePack, dir)
            if not os.path.isdir(fullDir):
                continue
            if dir in objectFolders:
                existingFolders.append(dir)
        for folder in existingFolders:
            folderSelector['menu'].add_command(label=folder, command=lambda value=folder:SetCurrentSpriteFolder(value))


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
    
    ####################
    # Sprite Extractor #
    ####################

    def ExtractSprites():
        if not opts.sprite_pack:
            spriteExtractorWarning['text'] = 'You need to select a sprite pack to extract sprites!'
            return
        if not spriteExtractorFolder.get():
            spriteExtractorWarning['text'] = 'Write the name of the object you want to extract!'
            return
        if not spriteExtractorFolder.get() in objectFolders:
            spriteExtractorWarning['text'] = 'The name given is not a known Trainer or Pokemon!'
            return
        

        baseFolderPath:str = None
        if isSpritePackValid:
            baseFolderPath = os.path.join(opts.sprite_pack.get(), spriteExtractorFolder.get())
            if os.path.isdir(baseFolderPath):
                baseFolderPath = baseFolderPath + '-original'
        outputFolder = filedialog.askdirectory(initialdir=baseFolderPath, mustexist=False, title='Select a folder to extract the sprites to.')
        if len(outputFolder) == 0:
            return
        if not os.path.isdir(outputFolder):
            os.makedirs(outputFolder)
        
        extract_sprites(spriteExtractorFolder.get(), outputFolder, build_ap_rom(opts.patch.get()))
        

    spriteExtractorFolder = StringVar()

    spriteExtractorFrame = LabelFrame(mainWindowFrame, text='Sprite Extractor', padx=8, pady=8)
    spriteExtractorInfo = Label(spriteExtractorFrame, text='Type the name of the Trainer/Pokemon you want to\nextract then press the button below.')
    spriteExtractorEntry = Entry(spriteExtractorFrame, textvariable=spriteExtractorFolder)
    spriteExtractorWarning = Label(spriteExtractorFrame, text='If any error happens, it will be shown here!')
    spriteExtractorButton = Button(spriteExtractorFrame, text='Extract', command=ExtractSprites)

    spriteExtractorInfo.pack(side=TOP, pady=2)
    spriteExtractorEntry.pack(side=TOP, pady=2)
    spriteExtractorWarning.pack(side=TOP, pady=2)
    spriteExtractorButton.pack(side=TOP, pady=2)
    
    #############################
    # Sprite and Palette Viewer #
    #############################

    def SetCurrentSprite(sprite: str):
        currentSprite.set(sprite)
        SwitchSprite(sprite)

    def SwitchSpriteFolder(folder: str):
        SwitchSprite('--------')

        # Reset var and delete all old options
        currentSprite.set('--------')
        spriteSelector['menu'].delete(0, 'end')
        spriteSelector['menu'].add_command(label='--------', command=lambda sprite='--------':SetCurrentSprite(sprite))

        dir: str = os.path.join(opts.sprite_pack.get(), folder)
        if not isSpritePackValid or folder == '--------' or not os.path.isdir(dir):
            return

        # List valid sprites
        for sprite in os.listdir(dir):
            fullDir = os.path.join(dir, sprite)
            if os.path.isdir(fullDir) or not sprite.endswith('.png'):
                continue
            spriteSelector['menu'].add_command(label=sprite[:-4], command=lambda value=sprite[:-4]:SetCurrentSprite(value))

    def SwitchSprite(sprite: str):
        # Display the Archipelago icon as default
        if sprite == '--------':
            sprite = local_path('data', 'default.png')
        else:
            sprite = os.path.join(opts.sprite_pack.get(), currentSpriteFolder.get(), sprite)
        if not sprite.endswith('.png'):
            sprite = sprite + '.png'

        # Switch the displayed sprite
        newImage = PhotoImage(file=sprite).zoom(2, 2)
        spriteLabelImage.configure(image=newImage)
        spriteLabelImage.image = newImage

        # Extract the colors from the sprite
        palette = extract_palette_from_file(sprite)
        for i in range(16):
            palettePreviews[i]['bg'] = '#' + (palette[i] if i < len(palette) else '000000')

    currentSpriteFolder = StringVar(value="--------")
    currentSprite = StringVar(value="--------")
    folders = []
    sprites = []

    spritePreviewFrame = LabelFrame(mainWindowFrame, text="Sprite Preview", padx=8, pady=8)
    selectorFrame = Frame(spritePreviewFrame, padx=2, pady=2)
    selectorFrame.grid_rowconfigure(0, weight=1)
    selectorFrame.grid_rowconfigure(1, weight=1)
    selectorFrame.grid_columnconfigure(0, weight=1)
    selectorFrame.grid_columnconfigure(1, weight=1)

    folderSelectorFrame = Frame(selectorFrame)
    folderSelectorFrame.grid(row=0, column=0)
    folderSelectorLabel = Label(folderSelectorFrame, text="Current Folder")
    folderSelector = OptionMenu(folderSelectorFrame, currentSpriteFolder, "--------", *folders)

    spriteSelectorFrame = Frame(selectorFrame)
    spriteSelectorFrame.grid(row=0, column=1)
    spriteSelectorLabel = Label(spriteSelectorFrame, text="Current Sprite")
    spriteSelector = OptionMenu(spriteSelectorFrame, currentSprite, "--------", *sprites)

    spriteFrame = Frame(selectorFrame, padx=2, pady=2)
    spriteFrame.grid(row=1, column=0)
    spriteLabel = Label(spriteFrame, text="Sprite")
    spriteLabelImage = Label(spriteFrame, width=128, height=126)

    palettePreviewFrame = Frame(selectorFrame, width=128)
    palettePreviewFrame.grid(row=1, column=1)
    paletteLabel = Label(palettePreviewFrame, text="Palette")
    paletteLabel.grid(row=0, column=0, columnspan=4)
    palettePreviews = []
    for i in range(16):
        palettePreview = Frame(palettePreviewFrame, width=32, height=32, bg='#000000')
        palettePreview.grid(row=1+math.floor(i/4), column=i%4)
        palettePreviews.append(palettePreview)
    
    spritePreviewErrorLabel = Label(selectorFrame, text='No error detected! The sprite pack is valid.', pady=2)
    spritePreviewErrorLabel.grid(row=2, column=0, columnspan=2)

    selectorFrame.pack(side=TOP, expand=True, fill=X)
    folderSelectorLabel.pack(side=TOP, expand=True, fill=X)
    folderSelector.pack(side=TOP, expand=True, fill=X)
    spriteSelectorLabel.pack(side=TOP, expand=True, fill=X)
    spriteSelector.pack(side=TOP, expand=True, fill=X)
    spriteLabel.pack(side=TOP, expand=True, fill=X)
    spriteLabelImage.pack(side=TOP)

    ##########################
    # Apply and Save Buttons #
    ##########################

    def adjustRom():
        try:
            guiargs = Namespace()
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
        guiargs.patch = opts.patch.get()
        guiargs.sprite_pack = opts.sprite_pack.get()
        persistent_store("adjuster", GAME_EMERALD, guiargs)
        messagebox.showinfo(title="Success", message="Settings saved to persistent storage")

    # Adjust button
    bottomFrame = Frame(mainWindowFrame)

    adjustButton = Button(bottomFrame, text='Adjust Rom', command=adjustRom)
    adjustButton.pack(side=LEFT, padx=(5,5))
    saveButton = Button(bottomFrame, text='Save Settings', command=saveGUISettings)
    saveButton.pack(side=LEFT, padx=(5,5))

    bottomFrame.pack(side=TOP, pady=(5,5))
    
    def tryValidateSpritePack(_sprite_pack, _patch_changed = False):
        global ap_rom
        if isPatchValid:
            ap_rom = ap_rom if not _patch_changed else build_ap_rom(opts.patch.get())
        if isPatchValid and isSpritePackValid:
            errors, has_error = validate_sprite_pack(_sprite_pack, ap_rom)
            adjustButton['state'] = tk.DISABLED if has_error else tk.NORMAL
            spritePreviewErrorLabel['text'] = errors or 'No anomaly detected! The sprite pack is valid.'
        else: 
            adjustButton['state'] = tk.DISABLED
            spritePreviewErrorLabel['text'] = 'Both a sprite pack and a patch/ROM must be selected to validate the sprite pack.'

    PatchSelect(adjuster_settings.patch or '')
    SpritePackSelect(adjuster_settings.sprite_pack or '')

    tkinter_center_window(window)
    window.mainloop()

def set_icon(window):
    logo = tk.PhotoImage(file=local_path('data', 'icon.png'))
    window.tk.call('wm', 'iconphoto', window._w, logo)

def adjust(args):
    global ap_rom
    ap_rom = ap_rom or build_ap_rom(args.patch)

    # Build sprite pack patch & apply patch
    if not args.sprite_pack:
        raise Exception("A sprite pack is required!")
    sprite_pack_bps_patch = build_sprite_pack_patch(args.sprite_pack, ap_rom)
    adjusted_ap_rom = bytearray(len(ap_rom))
    apply_bps_patch(sprite_pack_bps_patch, ap_rom, adjusted_ap_rom)

    path_pieces = os.path.splitext(args.patch)
    adjusted_path = path_pieces[0] + '-adjusted.gba'
    with open(adjusted_path, 'wb') as outfile:
        outfile.write(adjusted_ap_rom)
    return adjusted_path

def build_ap_rom(_patch):
    if not _patch:
        raise Exception("A patch file or a patched ROM is required!")
    if os.path.splitext(_patch)[-1] == '.gba':
        # Load up the ROM directly
        with open(_patch, 'rb') as stream:
            return bytearray(stream.read())
    elif os.path.splitext(_patch)[-1] == '.apemerald':
        # Patch the registered ROM as an AP ROM
        import Patch
        _, ap_rom_path = Patch.create_rom_file(_patch)
        with open(ap_rom_path, 'rb') as stream:
            return bytearray(stream.read())
    else:
        raise Exception("Invalid file extension; requires .gba or .apemerald")

def build_sprite_pack_patch(sprite_pack, ap_rom):
    sprite_pack_path = sprite_pack
    sprite_pack_data = handle_sprite_pack(sprite_pack_path, ap_rom)
    sprite_pack_bps_patch = data_to_bps_patch(sprite_pack_data, ap_rom)
    return sprite_pack_bps_patch

def launch():
    import colorama, asyncio
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()

if __name__ == '__main__':
    main()
