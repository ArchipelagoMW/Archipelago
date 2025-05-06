import tkinter as tk
import argparse
import logging
import os
import math

from bps.apply import apply_to_bytearrays as apply_bps_patch

from Utils import local_path, persistent_store, get_adjuster_settings, get_adjuster_settings_no_defaults, \
    tkinter_center_window, data_to_bps_patch
from worlds.pokemon_emerald.sprite_patcher import get_patch_from_sprite_pack, extract_palette_from_file, \
    extract_sprites, get_pokemon_data, stringify_pokemon_data, destringify_pokemon_data, validate_ability, \
    validate_pokemon_data_string, validate_move_pool_string, stringify_move_pool, destringify_move_pool, \
    keep_different_pokemon_data, validate_sprite_pack
from worlds.pokemon_emerald.adjuster_constants import POKEMON_TYPES, POKEMON_FOLDERS, TRAINER_FOLDERS, \
    POKEMON_ABILITIES, POKEMON_GENDER_RATIOS, REVERSE_POKEMON_GENDER_RATIOS
from argparse import Namespace
from tkinter import messagebox

logger = logging.getLogger('EmeraldAdjuster')
isSpritePackValid = False
isPatchValid = False
objectFolders = []
ap_rom = None

GAME_EMERALD = "Pokemon Emerald"

async def main():
    parser = getArgparser()
    args = parser.parse_args(namespace=get_adjuster_settings_no_defaults(GAME_EMERALD))
    
    logging.basicConfig(format='%(message)s', level=logging.INFO)

    global objectFolders
    objectFolders = TRAINER_FOLDERS + POKEMON_FOLDERS

    args = parser.parse_args()
    if not os.path.isfile(args.patch):
        adjustGUI()
    else:
        adjust(args)

def getArgparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--patch', default='', help='Path to a Pokemon Emerald AP-randomized ROM to adjust or path to a .apemerald patch file.')
    parser.add_argument('--sprite-pack', default='', help='Path to the Emerald sprite pack folder to use.')
    return parser

def adjustGUI():
    adjuster_settings = get_adjuster_settings(GAME_EMERALD)

    from tkinter import LEFT, TOP, X, E, W, END, DISABLED, NORMAL, StringVar, \
        IntVar,  Tk, LabelFrame, Frame, Label, Entry, Button, Checkbutton, \
        OptionMenu, PhotoImage, filedialog
    from tkinter.ttk import Notebook
    from tkinter.scrolledtext import ScrolledText
    from Utils import __version__ as MWVersion

    window = Tk()
    window.wm_title(f"Archipelago {MWVersion} Emerald Adjuster")
    setIcon(window)

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

    def patchSelect(_forcedPatch = None):
        global isPatchValid

        if not _forcedPatch is None:
            patch = _forcedPatch
        else:
            oldPatchFolder = os.path.dirname(opts.patch.get()) if isPatchValid else None
            oldPatchFile = opts.patch.get() if isPatchValid else None
            patch = filedialog.askopenfilename(initialdir=oldPatchFolder, initialfile=oldPatchFile, filetypes=[("Rom & Patch Files", [".gba", ".apemerald"]), ("All Files", "*")])
        opts.patch.set(patch)

        isPatchValid = len(patch) > 0 and os.path.exists(patch)
        tryValidateSpritePack(opts.sprite_pack.get(), True)

        if not isPatchValid:
            spriteExtractorFrame.pack_forget()
            if dataEditionLabelFrame.winfo_ismapped():
                dataEditionLabelFrame.grid_forget()
                dataEditionError.grid(row=0, column=2, rowspan=2)
        else:
            if dataEditionError.winfo_ismapped():
                switchSpriteFolder(currentSpriteFolder.get(), currentSprite.get())
            spritePreviewFrame.pack_forget()
            bottomFrame.pack_forget()
            spriteExtractorFrame.pack(side=TOP, expand=True, fill=X, pady=5)
            if isSpritePackValid:
                spritePreviewFrame.pack(side=TOP, expand=True, fill=X, pady=5)
            bottomFrame.pack(side=TOP, pady=5)
    
    def setCurrentSpriteFolder(folder: str):
        currentSpriteFolder.set(folder)
        switchSpriteFolder(folder)

    def spritePackSelect(_forcedSpritePack = None):
        global isSpritePackValid

        if not _forcedSpritePack is None:
            spritePack = _forcedSpritePack
        else:
            oldSpritePackFolder = opts.sprite_pack.get() if isSpritePackValid else None
            spritePack = filedialog.askdirectory(initialdir=oldSpritePackFolder, mustexist=True)
        opts.sprite_pack.set(spritePack)
        isSpritePackValid = len(spritePack) > 0 and os.path.isdir(spritePack)
        tryValidateSpritePack(opts.sprite_pack.get())

        switchSpriteFolder('--------')

        # Reset var and delete all old options
        currentSpriteFolder.set('--------')
        folderSelector['menu'].delete(0, 'end')
        folderSelector['menu'].add_command(label='--------', command=lambda value='--------':setCurrentSpriteFolder(value))

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
            folderSelector['menu'].add_command(label=folder, command=lambda value=folder:setCurrentSpriteFolder(value))

    patchSelectButton = Button(patchDialogFrame, text='Select Patch/Rom', command=patchSelect)
    patchDialogFrame.pack(side=TOP, expand=True, fill=X)
    patchLabel.pack(side=LEFT)
    patchEntry.pack(side=LEFT, expand=True, fill=X)
    patchSelectButton.pack(side=LEFT)
    spritePackSelectButton = Button(spritePackFrame, text='Select Pack', command=spritePackSelect)
    spritePackFrame.pack(side=TOP, expand=True, fill=X)
    spritePackLabel.pack(side=LEFT)
    spritePackEntry.pack(side=LEFT, expand=True, fill=X)
    spritePackSelectButton.pack(side=LEFT)
    
    ####################
    # Sprite Extractor #
    ####################

    def extractSprites():
        if not spriteExtractorFolder.get():
            spriteExtractorWarning['text'] = 'Write the name of the object you want to extract!'
            return
        if not spriteExtractorFolder.get() in objectFolders:
            spriteExtractorWarning['text'] = 'The name given is not a known Trainer or Pokemon!'
            return

        baseFolderPath:str = None
        if isSpritePackValid:
            baseFolderPath = opts.sprite_pack.get()
        outputFolder = filedialog.askdirectory(initialdir=baseFolderPath, mustexist=False, title='Select a folder to extract the sprites to.')
        if len(outputFolder) == 0:
            return
        if not os.path.isdir(outputFolder):
            os.makedirs(outputFolder)
        
        extract_sprites(spriteExtractorFolder.get(), outputFolder, build_ap_rom(opts.patch.get()))
        messagebox.showinfo(title='Success', message=f'All sprites for {spriteExtractorFolder.get()} have successfully been extracted!')
        
    def extractAllSprites():
        baseFolderPath:str = None
        if isSpritePackValid:
            baseFolderPath = opts.sprite_pack.get()
        outputFolder = filedialog.askdirectory(initialdir=baseFolderPath, mustexist=False, title='Select a folder to extract all sprites to.')
        if len(outputFolder) == 0:
            return
        if not os.path.isdir(outputFolder):
            os.makedirs(outputFolder)

        rom = build_ap_rom(opts.patch.get())
        for object in objectFolders:
            currentOutput = os.path.join(outputFolder, object)
            if not os.path.isdir(currentOutput):
                os.makedirs(currentOutput)
            extract_sprites(object, currentOutput, rom)
        messagebox.showinfo(title='Success', message=f'All sprites have successfully been extracted!')

    spriteExtractorFolder = StringVar()

    spriteExtractorFrame = LabelFrame(mainWindowFrame, text='Sprite Extractor', padx=8, pady=8)
    spriteExtractorFrame.grid_columnconfigure(0, weight=1)
    spriteExtractorFrame.grid_columnconfigure(1, weight=1)
    spriteExtractorInfo = Label(spriteExtractorFrame, text='Type the name of the Trainer/Pokemon you want to\nextract then press the button below.')
    spriteExtractorInfo.grid(row=0, column=0, columnspan=2, pady=2)
    spriteExtractorEntry = Entry(spriteExtractorFrame, textvariable=spriteExtractorFolder)
    spriteExtractorEntry.grid(row=1, column=0, columnspan=2, pady=2)
    spriteExtractorWarning = Label(spriteExtractorFrame, text='If any error happens, it will be shown here!')
    spriteExtractorWarning.grid(row=2, column=0, columnspan=2, pady=2)
    spriteExtractorButton = Button(spriteExtractorFrame, text='Extract', command=extractSprites)
    spriteExtractorButton.grid(row=3, column=0, sticky=E, padx=5, pady=2)
    spriteExtractorButtonAll = Button(spriteExtractorFrame, text='Extract All (takes a long time)', command=extractAllSprites)
    spriteExtractorButtonAll.grid(row=3, column=1, sticky=W, padx=5, pady=2)
    
    #############################
    # Sprite and Palette Viewer #
    #############################

    def setCurrentSprite(sprite: str):
        currentSprite.set(sprite)
        switchSprite(sprite)

    def switchSpriteFolder(folder: str, sprite: str='--------'):
        switchSprite(sprite)

        # Reset var and delete all old options
        currentSprite.set(sprite)
        spriteSelector['menu'].delete(0, 'end')
        spriteSelector['menu'].add_command(label='--------', command=lambda sprite='--------':setCurrentSprite(sprite))

        dir: str = os.path.join(opts.sprite_pack.get(), folder)
        # List valid sprites
        if isSpritePackValid and folder != '--------' and os.path.isdir(dir):
            for sprite in os.listdir(dir):
                fullDir = os.path.join(dir, sprite)
                if os.path.isdir(fullDir) or not sprite.endswith('.png'):
                    continue
                spriteSelector['menu'].add_command(label=sprite[:-4], command=lambda value=sprite[:-4]:setCurrentSprite(value))
        
        # Show Pokemon data edition widgets or not
        if not folder in POKEMON_FOLDERS:
            spritePreviewFrame.grid_columnconfigure(2, weight=0)
            dataEditionLabelFrame.grid_forget()
            dataEditionError.grid_forget()
        else:
            spritePreviewFrame.grid_columnconfigure(2, weight=1)
            if not isPatchValid:
                dataEditionLabelFrame.grid_forget()
                dataEditionError.grid(row=0, column=2, rowspan=2)
                return
            else:
                dataEditionError.grid_forget()
                dataEditionLabelFrame.grid(row=0, column=2, rowspan=2)

            # Fill in data editor fields
            data = get_pokemon_data(folder)
            # Load local data if it exists and replace existing fields
            edited_data_path = os.path.join(opts.sprite_pack.get(), currentSpriteFolder.get(), 'data.txt')
            if os.path.exists(edited_data_path):
                with open(edited_data_path) as edited_data_file:
                    edited_data_string = edited_data_file.read()
                edited_data_errors, has_edited_data_error = validate_pokemon_data_string(folder, edited_data_string)
                if has_edited_data_error:
                    messagebox.showerror(title="Error while loading Pokemon data", message=edited_data_errors)
                else:
                    edited_data = destringify_pokemon_data(currentSpriteFolder.get(), edited_data_string)
                    for field in edited_data:
                        if field == 'dex':
                            data[field] = (edited_data[field] << 7) + data[field] % 0x7F
                        else:
                            data[field] = edited_data[field]
            
            # Fill in the fields in the data editor
            pokemonHP.set(data['hp'])
            pokemonSPD.set(data['spd'])
            pokemonATK.set(data['atk'])
            pokemonDEF.set(data['def'])
            pokemonSPATK.set(data['spatk'])
            pokemonSPDEF.set(data['spdef'])
            pokemonType1.set(POKEMON_TYPES[data['type1']])
            pokemonType2.set(POKEMON_TYPES[data['type2']])
            pokemonAbility1.set(POKEMON_ABILITIES[data['ability1']].title())
            pokemonAbility2.set(POKEMON_ABILITIES[data['ability2']].title())
            pokemonGender.set(POKEMON_GENDER_RATIOS[data['gender_ratio']])
            pokemonForbidFlip.set(data['dex'] >> 7)

            movePoolInput.delete('1.0', END)
            movePoolInput.insert(END, stringify_move_pool(data['move_pool']))
            # TODO: Trigger validation function for all those fields

    def switchSprite(sprite: str):
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
    spritePreviewFrame.grid_rowconfigure(0, weight=1)
    spritePreviewFrame.grid_rowconfigure(1, weight=1)
    spritePreviewFrame.grid_columnconfigure(0, weight=1)
    spritePreviewFrame.grid_columnconfigure(1, weight=1)

    folderSelectorFrame = Frame(spritePreviewFrame)
    folderSelectorFrame.grid(row=0, column=0, padx=8)
    folderSelectorLabel = Label(folderSelectorFrame, text="Current Folder")
    folderSelector = OptionMenu(folderSelectorFrame, currentSpriteFolder, "--------", *folders)

    spriteSelectorFrame = Frame(spritePreviewFrame)
    spriteSelectorFrame.grid(row=0, column=1, padx=8)
    spriteSelectorLabel = Label(spriteSelectorFrame, text="Current Sprite")
    spriteSelector = OptionMenu(spriteSelectorFrame, currentSprite, "--------", *sprites)

    spriteFrame = Frame(spritePreviewFrame, padx=2, pady=2)
    spriteFrame.grid(row=1, column=0, padx=8)
    spriteLabel = Label(spriteFrame, text="Sprite")
    spriteLabelImage = Label(spriteFrame, width=128, height=126)

    palettePreviewFrame = Frame(spritePreviewFrame, width=128)
    palettePreviewFrame.grid(row=1, column=1, padx=8)
    paletteLabel = Label(palettePreviewFrame, text="Palette")
    paletteLabel.grid(row=0, column=0, columnspan=4)
    palettePreviews = []
    for i in range(16):
        palettePreview = Frame(palettePreviewFrame, width=32, height=32, bg='#000000')
        palettePreview.grid(row=1+math.floor(i/4), column=i%4)
        palettePreviews.append(palettePreview)
    
    #########################
    ## Pokemon Data Editor ##
    #########################

    dataEditionLabelFrame = LabelFrame(spritePreviewFrame, text='Pokemon Data Editor', padx=8)
    dataEditionError = Label(spritePreviewFrame, text='A ROM needs to\nbe loaded to edit\na Pokemon\'s data!', padx=8)

    def savePokemonData():
        pokemon_name = currentSpriteFolder.get()
        old_pokemon_data = get_pokemon_data(pokemon_name)
        # Build an object with all the registered data
        new_pokemon_data = {
            'hp': int(pokemonHP.get()),
            'atk': int(pokemonATK.get()),
            'def': int(pokemonDEF.get()),
            'spatk': int(pokemonSPATK.get()),
            'spdef': int(pokemonSPDEF.get()),
            'spd': int(pokemonSPD.get()),
            'type1': POKEMON_TYPES.index(pokemonType1.get()),
            'type2': POKEMON_TYPES.index(pokemonType2.get()),
            'ability1': POKEMON_ABILITIES.index(pokemonAbility1.get().upper()),
            'ability2': POKEMON_ABILITIES.index(pokemonAbility2.get().upper()),
            'gender_ratio': REVERSE_POKEMON_GENDER_RATIOS[pokemonGender.get()],
            'dex': (int(pokemonForbidFlip.get()) << 7) + int(old_pokemon_data['dex']) % 0x7F,
            'move_pool': destringify_move_pool(movePoolInput.get('1.0', END))
        }
        # Trim the data that has not been changed
        new_minimal_data = keep_different_pokemon_data(old_pokemon_data, new_pokemon_data)
        
        # Save changes to a specific file
        new_data_string = stringify_pokemon_data(new_minimal_data)
        data_path = os.path.join(opts.sprite_pack.get(), currentSpriteFolder.get(), 'data.txt')
        if os.path.exists(data_path):
            os.remove(data_path)
        if new_data_string:
            with open(data_path, 'w') as data_file:
                data_file.write(new_data_string)
        messagebox.showinfo(title="Success", message=f"Data for the Pokemon {pokemon_name} has been successfully saved!")

    dataEditionNotebook = Notebook(dataEditionLabelFrame, padding=2)
    dataEditionNotebook.pack(side=TOP)
    dataEditionButton = Button(dataEditionLabelFrame, text='Save Data', command=savePokemonData)
    dataEditionButton.pack(side=TOP, pady=4)

    validFieldValues = {
        'hp': True,
        'spd': True,
        'atk': True,
        'def': True,
        'spatk': True,
        'spdef': True,
        'ability1': True,
        'ability2': True,
        'movePool': True
    }

    pokemonHP = StringVar()
    pokemonSPD = StringVar()
    pokemonATK = StringVar()
    pokemonDEF = StringVar()
    pokemonSPATK = StringVar()
    pokemonSPDEF = StringVar()

    pokemonType1 = StringVar()
    pokemonType2 = StringVar()
    pokemonAbility1 = StringVar()
    pokemonAbility2 = StringVar()
    pokemonGender = StringVar()
    pokemonForbidFlip = IntVar()

    movePoolInput = None

    def updateFieldValidity(fieldName, value):
        validFieldValues[fieldName] = value
        anyValueInvalid = any(filter(lambda v: v == False or None, [validFieldValues[field] for field in validFieldValues]))
        dataEditionButton['state'] = DISABLED if anyValueInvalid else NORMAL
    
    # TODO: Add description tooltips on each label
    # TODO: Update tooltips to say a value is different from the one in the ROM if the text is BLUE
    # TODO: Update tooltips to add error if the text is RED
    # TODO: Add validation functions to each value
    def buildStatFrame():
        # Tab for changing the Pokemon's base stats
        statFrame = Frame(dataEditionNotebook)
        dataEditionNotebook.add(statFrame, text='Stats')
        statFrame.grid_rowconfigure(0, weight=1)
        statFrame.grid_rowconfigure(1, weight=1)
        statFrame.grid_rowconfigure(2, weight=1)
        statFrame.grid_columnconfigure(0, weight=1)
        statFrame.grid_columnconfigure(1, weight=1)

        def checkStatValue(entry, label, validField):
            try:
                value = int(entry.get().strip())
                valid = 1 <= value <= 255
            except ValueError:
                valid = False
            # TODO: Turn the label BLUE if the value is different from the one in the ROM
            entry.config(fg='black' if valid else 'red')
            label.config(fg='black' if valid else 'red')
            updateFieldValidity(validField, valid)

        statHPFrame = Frame(statFrame, padx=2, pady=2)
        statHPFrame.grid(row=0, column=0)
        statHPLabel = Label(statHPFrame, text="HP")
        statHPInput = Entry(statHPFrame, textvariable=pokemonHP, width=7)
        statSPDFrame = Frame(statFrame, padx=2, pady=2)
        statSPDFrame.grid(row=0, column=1)
        statSPDLabel = Label(statSPDFrame, text="Speed")
        statSPDInput = Entry(statSPDFrame, textvariable=pokemonSPD, width=7)
        statATKFrame = Frame(statFrame, padx=2, pady=2)
        statATKFrame.grid(row=1, column=0)
        statATKLabel = Label(statATKFrame, text="Attack")
        statATKInput = Entry(statATKFrame, textvariable=pokemonATK, width=7)
        statDEFFrame = Frame(statFrame, padx=2, pady=2)
        statDEFFrame.grid(row=2, column=0)
        statDEFLabel = Label(statDEFFrame, text="Defense")
        statDEFInput = Entry(statDEFFrame, textvariable=pokemonDEF, width=7)
        statSPATKFrame = Frame(statFrame, padx=2, pady=2)
        statSPATKFrame.grid(row=1, column=1)
        statSPATKLabel = Label(statSPATKFrame, text="Sp. Atk.")
        statSPATKInput = Entry(statSPATKFrame, textvariable=pokemonSPATK, width=7)
        statSPDEFFrame = Frame(statFrame, padx=2, pady=2)
        statSPDEFFrame.grid(row=2, column=1)
        statSPDEFLabel = Label(statSPDEFFrame, text="Sp. Def.")
        statSPDEFInput = Entry(statSPDEFFrame, textvariable=pokemonSPDEF, width=7)

        statHPLabel.pack(side=TOP)
        statHPInput.pack(side=TOP)
        statHPInput.bind('<KeyRelease>', lambda e: checkStatValue(e.widget, statHPLabel, 'hp'))
        statSPDLabel.pack(side=TOP)
        statSPDInput.pack(side=TOP)
        statSPDInput.bind('<KeyRelease>', lambda e: checkStatValue(e.widget, statSPDLabel, 'spd'))
        statATKLabel.pack(side=TOP)
        statATKInput.pack(side=TOP)
        statATKInput.bind('<KeyRelease>', lambda e: checkStatValue(e.widget, statATKLabel, 'atk'))
        statDEFLabel.pack(side=TOP)
        statDEFInput.pack(side=TOP)
        statDEFInput.bind('<KeyRelease>', lambda e: checkStatValue(e.widget, statDEFLabel, 'def'))
        statSPATKLabel.pack(side=TOP)
        statSPATKInput.pack(side=TOP)
        statSPATKInput.bind('<KeyRelease>', lambda e: checkStatValue(e.widget, statSPATKLabel, 'spatk'))
        statSPDEFLabel.pack(side=TOP)
        statSPDEFInput.pack(side=TOP)
        statSPDEFInput.bind('<KeyRelease>', lambda e: checkStatValue(e.widget, statSPDEFLabel, 'spdef'))

    def buildExtraDataFrame():
        extraDataFrame = Frame(spritePreviewFrame)
        dataEditionNotebook.add(extraDataFrame, text='Other')
        extraDataFrame.grid_rowconfigure(0, weight=1)
        extraDataFrame.grid_rowconfigure(1, weight=1)
        extraDataFrame.grid_rowconfigure(2, weight=1)
        extraDataFrame.grid_columnconfigure(0, weight=1)
        extraDataFrame.grid_columnconfigure(1, weight=1)

        def checkAbility(entry, label, validField):
            valid = validate_ability(entry.get().strip())
            entry.config(fg='black' if valid else 'red')
            label.config(fg='black' if valid else 'red')
            updateFieldValidity(validField, valid)

        type1Frame = Frame(extraDataFrame, padx=2, pady=2)
        type1Frame.grid(row=0, column=0)
        type1Label = Label(type1Frame, text="Type 1")
        type1Input = OptionMenu(type1Frame, pokemonType1, 'Normal', *POKEMON_TYPES[1:])
        type2Frame = Frame(extraDataFrame, padx=2, pady=2)
        type2Frame.grid(row=1, column=0)
        type2Label = Label(type2Frame, text="Type 2")
        type2Input = OptionMenu(type2Frame, pokemonType2, 'Normal', *POKEMON_TYPES[1:])
        ability1Frame = Frame(extraDataFrame, padx=2, pady=2)
        ability1Frame.grid(row=0, column=1)
        ability1Label = Label(ability1Frame, text="Ability 1")
        ability1Input = Entry(ability1Frame, textvariable=pokemonAbility1, width=12)
        ability2Frame = Frame(extraDataFrame, padx=2, pady=2)
        ability2Frame.grid(row=1, column=1)
        ability2Label = Label(ability2Frame, text="Ability 2")
        ability2Input = Entry(ability2Frame, textvariable=pokemonAbility2, width=12)
        genderFrame = Frame(extraDataFrame, padx=2, pady=2)
        genderFrame.grid(row=2, column=0)
        genderLabel = Label(genderFrame, text="Gender")
        genderInput = OptionMenu(genderFrame, pokemonGender, '100% M', *list(POKEMON_GENDER_RATIOS.values())[1:])
        forbidFlipFrame = Frame(extraDataFrame, padx=2, pady=2)
        forbidFlipFrame.grid(row=2, column=1)
        forbidFlipLabel = Label(forbidFlipFrame, text="Forbid Flip")
        forbidFlipInput = Checkbutton(forbidFlipFrame, variable=pokemonForbidFlip)

        type1Label.pack(side=TOP)
        type1Input.pack(side=TOP)
        type2Label.pack(side=TOP)
        type2Input.pack(side=TOP)
        ability1Label.pack(side=TOP)
        ability1Input.pack(side=TOP)
        ability1Input.bind('<KeyRelease>', lambda e: checkAbility(e.widget, ability1Label, 'ability1'))
        ability2Label.pack(side=TOP)
        ability2Input.pack(side=TOP)
        ability2Input.bind('<KeyRelease>', lambda e: checkAbility(e.widget, ability2Label, 'ability2'))
        genderLabel.pack(side=TOP)
        genderInput.pack(side=TOP)
        forbidFlipLabel.pack(side=TOP)
        forbidFlipInput.pack(side=TOP)

    def buildMovePoolFrame():
        nonlocal movePoolInput
        movePoolFrame = Frame(spritePreviewFrame)
        dataEditionNotebook.add(movePoolFrame, text='Move Pool')

        movePoolLabel = Label(movePoolFrame, text="Move Pool")
        movePoolInput = ScrolledText(movePoolFrame, undo=True, width=24, height=10)

        def checkMovePool(entry, label, validField):
            errors, hasError = validate_move_pool_string(currentSpriteFolder.get(), entry.get('1.0', END).strip())
            entry.config(fg='red' if hasError else 'black')
            label.config(fg='red' if hasError else 'black')
            updateFieldValidity(validField, not hasError)

        movePoolLabel.pack(side=TOP)
        movePoolInput.pack(side=TOP)
        movePoolInput.bind('<KeyRelease>', lambda e: checkMovePool(e.widget, movePoolLabel, 'move_pool'))

    buildStatFrame()
    buildMovePoolFrame()
    buildExtraDataFrame()

    spritePreviewErrorLabel = Label(spritePreviewFrame, text='No error detected! The sprite pack is valid.', pady=4)
    spritePreviewErrorLabel.grid(row=2, column=0, columnspan=4)

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
        has_error = False
        global ap_rom
        if isPatchValid:
            ap_rom = ap_rom if not _patch_changed else build_ap_rom(opts.patch.get())
        if isPatchValid and isSpritePackValid:
            errors, has_error = validate_sprite_pack(_sprite_pack, ap_rom)
            adjustButton['state'] = DISABLED if has_error else NORMAL
            spritePreviewErrorLabel['text'] = errors or 'No anomaly detected! The sprite pack is valid.'
        else: 
            adjustButton['state'] = DISABLED
            spritePreviewErrorLabel['text'] = 'Both a sprite pack and a patch/ROM must be selected to validate the sprite pack.'
        return has_error

    patchSelect(adjuster_settings.patch or '')
    spritePackSelect(adjuster_settings.sprite_pack or '')

    tkinter_center_window(window)
    window.mainloop()

def setIcon(window):
    from tkinter import PhotoImage
    logo = PhotoImage(file=local_path('data', 'icon.png'))
    window.tk.call('wm', 'iconphoto', window._w, logo)

def adjust(args):
    global ap_rom
    ap_rom = ap_rom or build_ap_rom(args.patch)

    if not args.sprite_pack:
        raise Exception('Cannot adjust the ROM, a sprite pack is required!')
    
    # Build sprite pack patch & apply patch
    try:
        sprite_pack_bps_patch = build_sprite_pack_patch(args.sprite_pack, ap_rom)
    except Exception as e:
        if hasattr(e, 'message'):
            raise Exception('Error during patch creation: {}'.format(e.message))
        else:
            raise Exception('Error during patch creation: {}'.format(str(e)))

    adjusted_ap_rom = bytearray(len(ap_rom))
    apply_bps_patch(sprite_pack_bps_patch, ap_rom, adjusted_ap_rom)

    path_pieces = os.path.splitext(args.patch)
    adjusted_path = path_pieces[0] + '-adjusted.gba'
    with open(adjusted_path, 'wb') as outfile:
        outfile.write(adjusted_ap_rom)
    return adjusted_path

def build_ap_rom(_patch):
    if not _patch:
        messagebox.showerror(title='Failure', message=f'Cannot build the AP ROM: a patch file or a patched ROM is required!')
        return
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
        messagebox.showerror(title='Failure', message=f'Cannot build the AP ROM: invalid file extension: requires .gba or .apemerald')
        return

def build_sprite_pack_patch(sprite_pack, ap_rom):
    _, has_error = validate_sprite_pack(sprite_pack, ap_rom)
    if has_error:
        raise Exception('Cannot adjust the ROM as the sprite pack is erroneous!')
    
    sprite_pack_path = sprite_pack
    sprite_pack_data = get_patch_from_sprite_pack(sprite_pack_path, ap_rom)
    sprite_pack_bps_patch = data_to_bps_patch(sprite_pack_data, ap_rom)
    return sprite_pack_bps_patch

def launch():
    import colorama, asyncio
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()

if __name__ == '__main__':
    main()
