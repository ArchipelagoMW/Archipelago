import argparse
import logging
import os
import math

from bps.apply import apply_to_bytearrays as apply_bps_patch

from Utils import local_path, persistent_store, get_adjuster_settings, get_adjuster_settings_no_defaults, \
    tkinter_center_window, data_to_bps_patch, open_image_secure
from worlds.pokemon_emerald.adjuster_patcher import get_patch_from_sprite_pack, extract_palette_from_file, \
    extract_sprites, validate_sprite_pack, get_pokemon_data, stringify_pokemon_data, destringify_pokemon_data, \
    validate_pokemon_data_string, stringify_move_pool, destringify_move_pool, keep_different_pokemon_data, \
    handle_address_collection, find_folder_object_info, load_constants
from worlds.pokemon_emerald.adjuster_constants import POKEMON_TYPES, POKEMON_FOLDERS, POKEMON_ABILITIES, \
    POKEMON_GENDER_RATIOS, REVERSE_POKEMON_GENDER_RATIOS
from argparse import Namespace
from tkinter import messagebox, IntVar

try:
    from worlds.pokemon_frlg.adjuster import *
    frlgSupport = True
except:
    frlgSupport = False

logger = logging.getLogger('EmeraldAdjuster')
isSpritePackValid = False
isPatchValid = False
romVersion = 'Emerald'
objectFolders = None
apRom = None
isRomAp = None

GAME_EMERALD = 'Pokemon Emerald'

async def main():
    # Main function of the adjuster
    parser = getArgparser()
    args = parser.parse_args(namespace=get_adjuster_settings_no_defaults(GAME_EMERALD))

    logging.basicConfig(format='%(message)s', level=logging.INFO)

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

def fetchPatch(_opts):
    # Asks for a ROM or patch file then validates it
    from tkinter import filedialog
    oldPatchFolder = os.path.dirname(_opts.patch.get()) if isPatchValid else None
    oldPatchFile = _opts.patch.get() if isPatchValid else None
    patch = filedialog.askopenfilename(initialdir=oldPatchFolder, initialfile=oldPatchFile, title='Choose a Pokemon Emerald ROM or an .apemerald patch file.', filetypes=[('Rom & Patch Files', ['.gba', '.apemerald'])])
    if patch and os.path.exists(patch):
        if os.path.splitext(patch)[-1] == '.gba':
            # If .gba, verify ROM integrity by checking for its internal name at addresses #0000A0-#0000AB (must be POKEMON EMER)
            with open(patch, 'rb') as stream:
                patchData = bytearray(stream.read())
                internalName = patchData[0xA0:0xAC].decode('utf-8')
                if internalName == 'POKEMON EMER':
                    return patch, 'Emerald'
        elif os.path.splitext(patch)[-1] == '.apemerald':
            return patch, 'Emerald'
    messagebox.showerror(title='Error while loading a ROM', message=f'The ROM at path {patch} isn\'t a valid Pokemon Emerald ROM!')
    return patch, 'Unknown'

def adjustGUI():
    adjusterSettings = get_adjuster_settings(GAME_EMERALD)

    from tkinter import LEFT, TOP, X, E, W, END, DISABLED, NORMAL, StringVar, \
        LabelFrame, Frame, Label, Entry, Button, Checkbutton, OptionMenu, \
        PhotoImage, filedialog, font
    from .tkentrycomplete import AutocompleteCombobox
    from tkinter.ttk import Notebook, Spinbox
    from tkinter.tix import Tk, Balloon
    from tkinter.scrolledtext import ScrolledText
    from Utils import __version__ as MWVersion

    window = Tk()
    window.wm_title(f'Archipelago {MWVersion} {'Pokemon Gen 3' if frlgSupport else 'Emerald'} Adjuster')
    setIcon(window)

    mainWindowFrame = Frame(window, padx=8, pady=8)
    mainWindowFrame.pack(side=TOP, expand=True, fill=X)

    opts = Namespace()

    ##############################################
    # ROM/Patch Selection, Sprite Pack Selection #
    ##############################################

    def patchSelect(_forcedPatch = None):
        # Run when we ask for the user to select a ROM or patch file,
        # or when the ROM or patch file needs to be reloaded
        global isPatchValid
        global romVersion

        if not _forcedPatch is None:
            patch = _forcedPatch
        elif frlgSupport:
            patch, romVersion = frlgFetchPatch(opts, isPatchValid)
        else:
            patch, romVersion = fetchPatch(opts)
        opts.patch.set(patch)

        load_constants(romVersion)

        isPatchValid = len(patch) > 0 and os.path.exists(patch)
        tryValidateSpritePack(opts.sprite_pack.get(), True)

        global objectFolders
        strainrFolderObjectInfo = find_folder_object_info('strainr')
        trainerFolderObjectInfo = find_folder_object_info('trainer')
        pokemonFolderObjectInfo = find_folder_object_info('pokemon')
        objectFolders = strainrFolderObjectInfo['folders'] + trainerFolderObjectInfo['folders'] + pokemonFolderObjectInfo['folders']

        if not isPatchValid:
            # If the patch is invalid, hide the isAP checkbox, the Sprite Extractor
            # and the data edition window if it's displayed
            patchIsAPCheckbox.pack_forget()
            spriteExtractorFrame.pack_forget()
            if dataEditionLabelFrame.winfo_ismapped():
                dataEditionLabelFrame.grid_forget()
                dataEditionError.grid(row=0, column=2, rowspan=2)
        else:
            # If the patch is valid, show the isAP checkbox, the Sprite Extractor
            # and the data edition window if it's displayed
            patchIsAPCheckbox.pack(side=LEFT, padx=(4,0))
            if dataEditionError.winfo_ismapped():
                switchSpriteFolder(currentValidSpriteFolder.get().title(), currentValidSprite.get())
            spritePreviewFrame.pack_forget()
            bottomFrame.pack_forget()
            spriteExtractorFrame.pack(side=TOP, expand=True, fill=X, pady=5)
            spriteExtractorComboBox.set_completion_list(objectFolders)
            if isSpritePackValid:
                spritePreviewFrame.pack(side=TOP, expand=True, fill=X, pady=5)
            bottomFrame.pack(side=TOP, pady=5)

    def spritePackSelect(_forcedSpritePack = None, _forcedFolder = '', _forcedSprite = ''):
        # Run when we ask for the user to select a sprite pack,
        # or when the sprite pack needs to be reloaded
        global isSpritePackValid

        if not _forcedSpritePack is None:
            spritePack = _forcedSpritePack
        else:
            oldSpritePackFolder = opts.sprite_pack.get() if isSpritePackValid else None
            spritePack = filedialog.askdirectory(initialdir=oldSpritePackFolder, title='Choose a sprite pack.', mustexist=True)
        opts.sprite_pack.set(spritePack)
        isSpritePackValid = len(spritePack) > 0 and os.path.isdir(spritePack)
        tryValidateSpritePack(opts.sprite_pack.get())

        if not isSpritePackValid:
            # If the sprite pack is invalid, do not show the Sprite Preview
            spritePreviewFrame.pack_forget()
            folderSelector.set_completion_list([''])
        else:
            # If the sprite pack is valid, show the Sprite Viewer
            bottomFrame.pack_forget()
            spritePreviewFrame.pack(side=TOP, expand=True, fill=X, pady=5)
            bottomFrame.pack(side=TOP, pady=5)

            # Detect existing object folders and list them
            existingFolders = []
            for dir in os.listdir(spritePack):
                if dir in objectFolders:
                    existingFolders.append(dir)
            nonlocal folders
            folders = ['', *existingFolders]
            folderSelector.set_completion_list(folders)

        switchSpriteFolder(_forcedFolder, _forcedSprite)

    global isRomAp
    isRomAp = IntVar()
    opts.patch = StringVar()
    opts.sprite_pack = StringVar()

    # Two lines with a label, an entry field and a button to ask for the
    # ROM/patch file to use for the adjuster, and the sprite pack
    # An extra checkbox is provided if the user wants to override whether the
    # given ROM is an Archipelago ROM or not, in case the auto-detection is wrong
    patchDialogFrame = Frame(mainWindowFrame, padx=8, pady=2)
    patchLabel = Label(patchDialogFrame, text='Patch / Modified Rom')
    patchEntry = Entry(patchDialogFrame, textvariable=opts.patch)
    patchSelectButton = Button(patchDialogFrame, text='Select Patch/Rom', command=patchSelect)
    patchIsAPCheckbox = Checkbutton(patchDialogFrame, variable=isRomAp, text='Is AP?')

    spritePackFrame = Frame(mainWindowFrame, padx=8, pady=2)
    spritePackLabel = Label(spritePackFrame, text='Sprite pack to load')
    spritePackEntry = Entry(spritePackFrame, textvariable=opts.sprite_pack)
    spritePackSelectButton = Button(spritePackFrame, text='Select Pack', command=spritePackSelect)

    # Balloon object used for displaying tooltips in the app, if some elements are hovered over
    mainWindowTooltip = Balloon(mainWindowFrame)
    mainWindowTooltip.bind_widget(patchIsAPCheckbox, balloonmsg='Override this value if your ROM is badly detected as an AP one.\nIf enabled, the adjuster will use data addresses from\nthe Archipelago patch for the game to inject the various data it needs to.')

    patchDialogFrame.pack(side=TOP, expand=True, fill=X)
    patchLabel.pack(side=LEFT)
    patchEntry.pack(side=LEFT, expand=True, fill=X)
    patchSelectButton.pack(side=LEFT)
    spritePackFrame.pack(side=TOP, expand=True, fill=X)
    spritePackLabel.pack(side=LEFT)
    spritePackEntry.pack(side=LEFT, expand=True, fill=X)
    spritePackSelectButton.pack(side=LEFT)

    ####################
    # Sprite Extractor #
    ####################

    def checkSpriteExtraction(_):
        # Enables or disables the sprite extraction button if the sprite's name is valid or not
        extractionFolderValid = spriteExtractorFolder.get() and spriteExtractorFolder.get() in objectFolders
        spriteExtractorButton['state'] = NORMAL if extractionFolderValid else DISABLED

    def extractSprites():
        # Run when the Extract button is pressed
        # Extract all the sprites from the given Pokemon or Trainer into the given folder
        if not spriteExtractorFolder.get() or not spriteExtractorFolder.get() in objectFolders:
            return

        baseFolderPath = None
        if isSpritePackValid:
            baseFolderPath = opts.sprite_pack.get()
        outputFolder = filedialog.askdirectory(initialdir=baseFolderPath, mustexist=False, title='Select a folder to extract the sprites to.')
        if len(outputFolder) == 0:
            return
        if not os.path.isdir(outputFolder):
            os.makedirs(outputFolder)

        handle_address_collection(apRom, romVersion, isRomAp.get())
        extract_sprites(spriteExtractorFolder.get(), outputFolder)
        messagebox.showinfo(title='Success', message=f'All sprites for {spriteExtractorFolder.get()} have successfully been extracted!')

    def extractAllSprites():
        # Run when the Extract All button is pressed
        # Extract all the sprites from all Pokemons and Trainers into the given folder
        baseFolderPath = None
        if isSpritePackValid:
            baseFolderPath = opts.sprite_pack.get()
        outputFolder = filedialog.askdirectory(initialdir=baseFolderPath, mustexist=False, title='Select a folder to extract all sprites to.')
        if len(outputFolder) == 0:
            return
        if not os.path.isdir(outputFolder):
            os.makedirs(outputFolder)

        handle_address_collection(apRom, romVersion, isRomAp.get())
        for object in objectFolders:
            # Extract each Pokemon and Trainer into subfolders
            currentOutput = os.path.join(outputFolder, object)
            if not os.path.isdir(currentOutput):
                os.makedirs(currentOutput)
            extract_sprites(object, currentOutput)
        messagebox.showinfo(title='Success', message=f'All sprites have successfully been extracted!')

    spriteExtractorFolder = StringVar()

    # A label to give some info, an input to choose the Pokemon or Trainer's name, and two buttons:
    # One for extracting only the given Pokemon or Trainer, and one for extracting all Pokemons and Trainers
    spriteExtractorFrame = LabelFrame(mainWindowFrame, text='Sprite Extractor', padx=8, pady=8)
    spriteExtractorFrame.grid_columnconfigure(0, weight=1)
    spriteExtractorFrame.grid_columnconfigure(1, weight=1)
    spriteExtractorInfo = Label(spriteExtractorFrame, text='Type the name of the Trainer/Pokemon you want to\nextract then press the button below.')
    spriteExtractorInfo.grid(row=0, column=0, columnspan=2, pady=2)
    spriteExtractorComboBox = AutocompleteCombobox(spriteExtractorFrame, textvariable=spriteExtractorFolder, width=14)
    spriteExtractorComboBox.bind('<KeyRelease>', checkSpriteExtraction, add='+')
    spriteExtractorComboBox.set_completion_list([''])
    spriteExtractorComboBox.grid(row=1, column=0, columnspan=2, pady=2)
    spriteExtractorButton = Button(spriteExtractorFrame, text='Extract', command=extractSprites)
    spriteExtractorButton.grid(row=3, column=0, sticky=E, padx=5, pady=2)
    spriteExtractorButtonAll = Button(spriteExtractorFrame, text='Extract All (takes a long time)', command=extractAllSprites)
    spriteExtractorButtonAll.grid(row=3, column=1, sticky=W, padx=5, pady=2)

    #############################
    # Sprite and Palette Viewer #
    #############################

    pokemonROMData = None
    pokemonSavedData = None

    def switchSpriteFolder(_folder: str, _sprite: str=''):
        # Run whenever the current sprite folder is changed
        # Loads the various data related to a Pokemon or Trainer, depending on the folder
        folderPath = os.path.join(opts.sprite_pack.get(), currentSpriteFolder.get().title())
        if _folder and not os.path.isdir(folderPath):
            # Non-existent folder, reload the pack
            folderSelector.set('')
            spriteSelector.set('')
            spritePackSelect(opts.sprite_pack.get())
            return
        if not _folder in folderSelector._completion_list:
            # Folder just created, reload the pack
            spriteSelector.set('')
            spritePackSelect(opts.sprite_pack.get(), _folder)
            return

        currentSpriteFolder.set(_folder)
        currentValidSpriteFolder.set(_folder)
        folderSelector.set(_folder)

        dir: str = os.path.join(opts.sprite_pack.get(), _folder)
        # Retrieve and list valid sprites
        spritesInFolder = []
        if isSpritePackValid and _folder and os.path.isdir(dir):
            for sprite in os.listdir(dir):
                fullPath = os.path.join(dir, sprite)
                if os.path.isdir(fullPath) or not sprite.endswith('.png'):
                    continue
                try:
                    open_image_secure(fullPath)
                except:
                    # If the image is invalid, don't add it to the sprite list
                    continue
                spritesInFolder.append(sprite[:-4])
        nonlocal sprites
        sprites = ['', *spritesInFolder]
        spriteSelector.set_completion_list(sprites)

        switchSprite(_sprite)

        if not _folder in POKEMON_FOLDERS or _folder == 'Egg':
            # Trainer folder, do not show the Pokemon data edition frame
            spritePreviewFrame.grid_columnconfigure(2, weight=0)
            dataEditionLabelFrame.grid_forget()
            dataEditionError.grid_forget()
        else:
            # Pokemon folder, show the Pokemon data edition frame
            spritePreviewFrame.grid_columnconfigure(2, weight=1)
            if not isPatchValid:
                dataEditionLabelFrame.grid_forget()
                dataEditionError.grid(row=0, column=2, rowspan=2)
                return
            else:
                dataEditionError.grid_forget()
                dataEditionLabelFrame.grid(row=0, column=2, rowspan=2)

            dataFolder = 'Unown A' if _folder.startswith('Unown ') else _folder
            # Fill in data editor fields
            nonlocal pokemonROMData, pokemonSavedData
            pokemonROMData = get_pokemon_data(dataFolder)
            pokemonData = pokemonROMData.copy()
            pokemonSavedData = None
            pokemonSavedDataPath = os.path.join(opts.sprite_pack.get(), dataFolder, 'data.txt')
            if os.path.exists(pokemonSavedDataPath):
                # Load local data if it exists and replace the fields' values
                with open(pokemonSavedDataPath) as pokemonSavedDataFile:
                    pokemonSavedDataString = pokemonSavedDataFile.read()
                pokemonSavedDataErrors, hasPokemonSavedDataError = validate_pokemon_data_string(_folder, pokemonSavedDataString)
                if hasPokemonSavedDataError:
                    messagebox.showerror(title='Error while loading Pokemon data', message=pokemonSavedDataErrors)
                    pokemonSavedData = None
                else:
                    pokemonSavedData = destringify_pokemon_data(dataFolder, pokemonSavedDataString)
                    for field in pokemonSavedData:
                        if field == 'dex':
                            pokemonData[field] = pokemonSavedData[field] = (pokemonSavedData[field] << 7) + (pokemonData[field] % 0x80)
                        else:
                            pokemonData[field] = pokemonSavedData[field]

            # Fill in the fields in the data editor and check their validity
            pokemonHP.set(pokemonData['hp'])
            pokemonSPD.set(pokemonData['spd'])
            pokemonATK.set(pokemonData['atk'])
            pokemonDEF.set(pokemonData['def'])
            pokemonSPATK.set(pokemonData['spatk'])
            pokemonSPDEF.set(pokemonData['spdef'])
            pokemonType1.set(POKEMON_TYPES[pokemonData['type1']])
            pokemonType2.set(POKEMON_TYPES[pokemonData['type2']])
            pokemonAbility1.set(POKEMON_ABILITIES[pokemonData['ability1']].title())
            pokemonAbility2.set(POKEMON_ABILITIES[pokemonData['ability2']].title() if pokemonData['ability2'] else POKEMON_ABILITIES[pokemonData['ability1']].title())
            pokemonGenderRatio.set(POKEMON_GENDER_RATIOS[pokemonData['gender_ratio']])
            pokemonForbidFlip.set(pokemonData['dex'] >> 7)

            movePoolInput.delete('1.0', END)
            movePoolInput.insert(END, stringify_move_pool(pokemonData['move_pool']))

            checkAllFields()

    def switchSprite(_sprite: str):
        # Run whenever the current sprite is changed
        # Displays the new sprite and its palette in the adjuster
        spritePath = os.path.join(opts.sprite_pack.get(), currentValidSpriteFolder.get().title(), _sprite + '.png')
        if _sprite and not os.path.exists(spritePath):
            # Non-existent folder, reload the pack
            folderSelector.set('')
            spriteSelector.set('')
            spritePackSelect(opts.sprite_pack.get())
            return
        if not _sprite in sprites:
            # Non-existant sprite, reload the pack
            spriteSelector.set('')
            spritePackSelect(opts.sprite_pack.get())
            return

        currentSprite.set(_sprite)
        currentValidSprite.set(_sprite)
        spriteSelector.set(_sprite)

        # Display the Archipelago icon as default
        if not _sprite:
            _sprite = local_path('data', 'default.png')
        else:
            _sprite = spritePath[:-4]
        if not _sprite.endswith('.png'):
            _sprite = _sprite + '.png'

        # Switch the displayed sprite
        newImage = PhotoImage(file=_sprite).zoom(2, 2)
        spriteLabelImage.configure(image=newImage)
        spriteLabelImage.image = newImage

        # Extract the colors from the sprite
        palette = extract_palette_from_file(_sprite)
        for i in range(16):
            palettePreviews[i]['bg'] = '#' + (palette[i] if i < len(palette) else '000000')

    def checkCurrentSpriteFolder(_):
        # Run when the current sprite folder's value is changed
        # This only switches the current sprite folder is it's recognized
        if currentSpriteFolder.get().title() in objectFolders and folderSelector.position == len(currentSpriteFolder.get()):
            folderPath = os.path.join(opts.sprite_pack.get(), currentSpriteFolder.get().title())
            if not os.path.isdir(folderPath):
                os.makedirs(folderPath)
            updateCurrentSpriteFolder('')

    def updateCurrentSpriteFolder(_):
        # Updates the current sprite folder, it must be considered valid
        switchSpriteFolder(currentSpriteFolder.get().title())

    def checkCurrentSprite(_):
        # Run when the current sprite's value is changed
        # This only switches the current sprite is it's recognized
        if currentSprite.get() in sprites and spriteSelector.position == len(currentSprite.get()):
            updateCurrentSprite('')

    def updateCurrentSprite(_):
        # Updates the current sprite, it must be considered valid
        switchSprite(currentSprite.get())

    currentSpriteFolder = StringVar(value='')
    currentValidSpriteFolder = StringVar(value='')
    currentSprite = StringVar(value='')
    currentValidSprite = StringVar(value='')
    folders = ['']
    sprites = ['']

    # Two sets of labels and autocompleting comboboxes for selecting a sprite folder and a sprite
    # Then one image to display the sprites, and 16 images arranged in a grid to display the palette
    spritePreviewFrame = LabelFrame(mainWindowFrame, text='Sprite Preview', padx=8, pady=8)
    spritePreviewFrame.grid_rowconfigure(0, weight=1)
    spritePreviewFrame.grid_rowconfigure(1, weight=1)
    spritePreviewFrame.grid_columnconfigure(0, weight=1)
    spritePreviewFrame.grid_columnconfigure(1, weight=1)

    folderSelectorFrame = Frame(spritePreviewFrame)
    folderSelectorFrame.grid(row=0, column=0, padx=8)
    folderSelectorLabel = Label(folderSelectorFrame, text='Current Folder')
    folderSelector = AutocompleteCombobox(folderSelectorFrame, textvariable=currentSpriteFolder, width=14)
    folderSelector.set_completion_list(folders)
    folderSelector.bind('<<ComboboxSelected>>', updateCurrentSpriteFolder)
    folderSelector.bind('<KeyRelease>', checkCurrentSpriteFolder, add='+')

    spriteSelectorFrame = Frame(spritePreviewFrame)
    spriteSelectorFrame.grid(row=0, column=1, padx=8)
    spriteSelectorLabel = Label(spriteSelectorFrame, text='Current Sprite')
    spriteSelector = AutocompleteCombobox(spriteSelectorFrame, textvariable=currentSprite, width=14)
    spriteSelector.set_completion_list(sprites)
    spriteSelector.bind('<<ComboboxSelected>>', updateCurrentSprite)
    spriteSelector.bind('<KeyRelease>', checkCurrentSprite, add='+')

    spriteFrame = Frame(spritePreviewFrame, padx=2, pady=2)
    spriteFrame.grid(row=1, column=0, padx=8)
    spriteLabel = Label(spriteFrame, text='Sprite')
    spriteLabelImage = Label(spriteFrame, width=128, height=126)

    palettePreviewFrame = Frame(spritePreviewFrame, width=128)
    palettePreviewFrame.grid(row=1, column=1, padx=8)
    paletteLabel = Label(palettePreviewFrame, text='Palette')
    paletteLabel.grid(row=0, column=0, columnspan=4)
    palettePreviews = []
    for i in range(16):
        palettePreview = Frame(palettePreviewFrame, width=32, height=32, bg='#000000')
        palettePreview.grid(row=1+math.floor(i/4), column=i%4)
        palettePreviews.append(palettePreview)

    #########################
    ## Pokemon Data Editor ##
    #########################

    # Frame that contains the Pokemon data editor
    # And if it's not editable, an error message to display instead
    dataEditionLabelFrame = LabelFrame(spritePreviewFrame, text='Pokemon Data Editor', padx=8)
    dataEditionError = Label(spritePreviewFrame, text='A ROM needs to\nbe loaded to edit\na Pokemon\'s data!', padx=8)

    def savePokemonData():
        # Saves the Pokemon's data into the given folder's 'data.txt' file
        pokemonName = currentValidSpriteFolder.get()
        if pokemonName.startswith('Unown '):
            pokemonName = 'Unown A'
        # Build an object with all the registered data
        newPokemonData = {
            'hp': int(pokemonHP.get()),
            'atk': int(pokemonATK.get()),
            'def': int(pokemonDEF.get()),
            'spatk': int(pokemonSPATK.get()),
            'spdef': int(pokemonSPDEF.get()),
            'spd': int(pokemonSPD.get()),
            'type1': POKEMON_TYPES.index(pokemonType1.get()),
            'type2': POKEMON_TYPES.index(pokemonType2.get()),
            'ability1': POKEMON_ABILITIES.index(pokemonAbility1.get().upper()),
            'ability2': POKEMON_ABILITIES.index(pokemonAbility2.get().upper()) or POKEMON_ABILITIES.index(pokemonAbility1.get().upper()),
            'gender_ratio': REVERSE_POKEMON_GENDER_RATIOS[pokemonGenderRatio.get()],
            'dex': (int(pokemonForbidFlip.get()) << 7) + int(pokemonROMData['dex']) % 0x80,
            'move_pool': destringify_move_pool(movePoolInput.get('1.0', END))
        }
        # Trim the data that has not been changed
        nonlocal pokemonSavedData
        pokemonSavedData = keep_different_pokemon_data(pokemonROMData, newPokemonData)
        checkAllFields()

        # Save changes to a specific data file
        pokemonSavedDataString = stringify_pokemon_data(pokemonSavedData)
        dataFolderPath = os.path.join(opts.sprite_pack.get(), pokemonName)
        if not os.path.isdir(dataFolderPath):
            os.makedirs(dataFolderPath)
        dataPath = os.path.join(dataFolderPath, 'data.txt')
        if pokemonSavedDataString:
            with open(dataPath, 'w') as dataFile:
                dataFile.write(pokemonSavedDataString)

        tryValidateSpritePack(opts.sprite_pack.get())
        messagebox.showinfo(title='Success', message=f'Data for the Pokemon {pokemonName} has been successfully saved!')

    # Notebook containing several tabs for various data to change and a button to save the data
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
    changedFieldValues = { k: False for k, _ in validFieldValues.items() }

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
    pokemonGenderRatio = StringVar()
    pokemonForbidFlip = IntVar()

    def updateFieldValidity(fieldName, value):
        # Disables the Pokemon data saving button if any data is erroneous
        validFieldValues[fieldName] = value
        anyValueInvalid = list(k for k, v in validFieldValues.items() if not v)
        dataEditionButton['state'] = DISABLED if anyValueInvalid else NORMAL

    def updateFieldChange(fieldName, value):
        # Displays the Pokemon data saving button's text in bold if any data has been changed
        changedFieldValues[fieldName] = value
        anyValueChanged = list(k for k, v in changedFieldValues.items() if v)
        dataEditionButton.config(font=boldFont if anyValueChanged else normalFont)

    normalFont = font.nametofont("TkDefaultFont")
    boldFont = normalFont.copy()
    boldFont['weight'] = 'bold'
    def checkValue(entry, label, field, balloonMessage):
        # Checks if a given Pokemon data value is valid or if it has been changed
        # And updates its label's color and font in consequence
        # Red if invalid, blue if different from the ROM, bold if different from the saved data
        fieldValue = str('[ {} ]'.format(entry.get('1.0', END)).replace('\n', ', ') if type(entry) is ScrolledText else entry.get()).strip()
        blueBalloonMessage = '\nThis label is blue because this value is different from the one within the ROM.'
        boldBalloonMessage = '\nThis label is in bold because this value has been changed and hasn\'t been saved.'
        errors, hasError = validate_pokemon_data_string(currentValidSpriteFolder.get(), { field: fieldValue })
        tempPokemonDataString = '{}: {}'.format(field, fieldValue)
        isDifferentFromROM = True
        isDifferentFromData = False
        internalField = 'dex' if field == 'forbid_flip' else field
        if not hasError:
            tempPokemonData = destringify_pokemon_data(currentValidSpriteFolder.get(), tempPokemonDataString)
            if 'dex' in list(tempPokemonData.keys()):
                tempPokemonData['dex'] = (tempPokemonData['dex'] << 7) + (pokemonROMData['dex'] % 0x80)
            differentPokemonData = keep_different_pokemon_data(pokemonROMData, tempPokemonData)
            isDifferentFromROM = internalField in list(differentPokemonData.keys())
            if pokemonSavedData and internalField in list(pokemonSavedData.keys()):
                differentPokemonData = keep_different_pokemon_data(pokemonSavedData, tempPokemonData)
                isDifferentFromData = internalField in list(differentPokemonData.keys())
            else:
                isDifferentFromData = isDifferentFromROM

        label.config(fg='red' if hasError else 'blue' if isDifferentFromROM else 'black', font=boldFont if isDifferentFromData else normalFont)
        mainWindowTooltip.unbind_widget(label)
        mainWindowTooltip.bind_widget(label, balloonmsg=balloonMessage + ('\n' + errors if hasError else blueBalloonMessage if isDifferentFromROM else '') + (boldBalloonMessage if isDifferentFromData else ''))
        updateFieldValidity(field, not hasError)
        updateFieldChange(field, isDifferentFromData)

    def checkAllFields():
        # Checks all Pokemon data values, and updates their labels
        checkValue(pokemonHP, statHPLabel, 'hp', statHPBalloonMessage)
        checkValue(pokemonSPD, statSPDLabel, 'spd', statSPDBalloonMessage)
        checkValue(pokemonATK, statATKLabel, 'atk', statATKBalloonMessage)
        checkValue(pokemonDEF, statDEFLabel, 'def', statDEFBalloonMessage)
        checkValue(pokemonSPATK, statSPATKLabel, 'spatk', statSPATKBalloonMessage)
        checkValue(pokemonSPDEF, statSPDEFLabel, 'spdef', statSPDEFBalloonMessage)
        checkValue(pokemonType1, type1Label, 'type1', type1BalloonMessage)
        checkValue(pokemonType2, type2Label, 'type2', type2BalloonMessage)
        checkValue(pokemonAbility1, ability1Label, 'ability1', ability1BalloonMessage)
        checkValue(pokemonAbility2, ability2Label, 'ability2', ability2BalloonMessage)
        checkValue(pokemonGenderRatio, genderRatioLabel, 'gender_ratio', genderRatioBalloonMessage)
        checkValue(pokemonForbidFlip, forbidFlipLabel, 'forbid_flip', forbidFlipBalloonMessage)
        checkValue(movePoolInput, movePoolLabel, 'move_pool', movePoolBalloonMessage)

    statHPLabel = statSPDLabel = statATKLabel = statDEFLabel = statSPATKLabel = statSPDEFLabel = None
    statHPBalloonMessage = 'This value changes the Pokemon\'s base HP.\nAwaits a value between 1 and 255.'
    statSPDBalloonMessage = 'This value changes the Pokemon\'s base Speed.\nAwaits a value between 1 and 255.'
    statATKBalloonMessage = 'This value changes the Pokemon\'s base Attack.\nAwaits a value between 1 and 255.'
    statDEFBalloonMessage = 'This value changes the Pokemon\'s base Defense.\nAwaits a value between 1 and 255.'
    statSPATKBalloonMessage = 'This value changes the Pokemon\'s base Special Attack.\nAwaits a value between 1 and 255.'
    statSPDEFBalloonMessage = 'This value changes the Pokemon\'s base Special Defense.\nAwaits a value between 1 and 255.'

    def buildStatFrame():
        # Tab for changing the Pokemon's base stats
        # Six groups of labels and spinboxes, one for each stat
        statFrame = Frame(dataEditionNotebook)
        dataEditionNotebook.add(statFrame, text='Stats')
        statFrame.grid_rowconfigure(0, weight=1)
        statFrame.grid_rowconfigure(1, weight=1)
        statFrame.grid_rowconfigure(2, weight=1)
        statFrame.grid_columnconfigure(0, weight=1)
        statFrame.grid_columnconfigure(1, weight=1)

        nonlocal statHPLabel, statSPDLabel, statATKLabel, statDEFLabel, statSPATKLabel, statSPDEFLabel
        statHPFrame = Frame(statFrame, padx=2, pady=2)
        statHPFrame.grid(row=0, column=0)
        statHPLabel = Label(statHPFrame, text='HP')
        mainWindowTooltip.bind_widget(statHPLabel, balloonmsg=statHPBalloonMessage)
        statHPInput = Spinbox(statHPFrame, textvariable=pokemonHP, width=7, from_=1, to=255)
        statSPDFrame = Frame(statFrame, padx=2, pady=2)
        statSPDFrame.grid(row=0, column=1)
        statSPDLabel = Label(statSPDFrame, text='Speed')
        mainWindowTooltip.bind_widget(statSPDLabel, balloonmsg=statSPDBalloonMessage)
        statSPDInput = Spinbox(statSPDFrame, textvariable=pokemonSPD, width=7, from_=1, to=255)
        statATKFrame = Frame(statFrame, padx=2, pady=2)
        statATKFrame.grid(row=1, column=0)
        statATKLabel = Label(statATKFrame, text='Attack')
        mainWindowTooltip.bind_widget(statATKLabel, balloonmsg=statATKBalloonMessage)
        statATKInput = Spinbox(statATKFrame, textvariable=pokemonATK, width=7, from_=1, to=255)
        statDEFFrame = Frame(statFrame, padx=2, pady=2)
        statDEFFrame.grid(row=2, column=0)
        statDEFLabel = Label(statDEFFrame, text='Defense')
        mainWindowTooltip.bind_widget(statDEFLabel, balloonmsg=statDEFBalloonMessage)
        statDEFInput = Spinbox(statDEFFrame, textvariable=pokemonDEF, width=7, from_=1, to=255)
        statSPATKFrame = Frame(statFrame, padx=2, pady=2)
        statSPATKFrame.grid(row=1, column=1)
        statSPATKLabel = Label(statSPATKFrame, text='Sp. Atk.')
        mainWindowTooltip.bind_widget(statSPATKLabel, balloonmsg=statSPATKBalloonMessage)
        statSPATKInput = Spinbox(statSPATKFrame, textvariable=pokemonSPATK, width=7, from_=1, to=255)
        statSPDEFFrame = Frame(statFrame, padx=2, pady=2)
        statSPDEFFrame.grid(row=2, column=1)
        statSPDEFLabel = Label(statSPDEFFrame, text='Sp. Def.')
        mainWindowTooltip.bind_widget(statSPDEFLabel, balloonmsg=statSPDEFBalloonMessage)
        statSPDEFInput = Spinbox(statSPDEFFrame, textvariable=pokemonSPDEF, width=7, from_=1, to=255)

        statHPLabel.pack(side=TOP)
        statHPInput.pack(side=TOP)
        statHPInput.bind('<KeyRelease>', lambda _: checkValue(pokemonHP, statHPLabel, 'hp', statHPBalloonMessage), add='+')
        statSPDLabel.pack(side=TOP)
        statSPDInput.pack(side=TOP)
        statSPDInput.bind('<KeyRelease>', lambda _: checkValue(pokemonSPD, statSPDLabel, 'spd', statSPDBalloonMessage), add='+')
        statATKLabel.pack(side=TOP)
        statATKInput.pack(side=TOP)
        statATKInput.bind('<KeyRelease>', lambda _: checkValue(pokemonATK, statATKLabel, 'atk', statATKBalloonMessage), add='+')
        statDEFLabel.pack(side=TOP)
        statDEFInput.pack(side=TOP)
        statDEFInput.bind('<KeyRelease>', lambda _: checkValue(pokemonDEF, statDEFLabel, 'def', statDEFBalloonMessage), add='+')
        statSPATKLabel.pack(side=TOP)
        statSPATKInput.pack(side=TOP)
        statSPATKInput.bind('<KeyRelease>', lambda _: checkValue(pokemonSPATK, statSPATKLabel, 'spatk', statSPATKBalloonMessage), add='+')
        statSPDEFLabel.pack(side=TOP)
        statSPDEFInput.pack(side=TOP)
        statSPDEFInput.bind('<KeyRelease>', lambda _: checkValue(pokemonSPDEF, statSPDEFLabel, 'spdef', statSPDEFBalloonMessage), add='+')

    type1Label = type2Label = ability1Label = ability2Label = genderRatioLabel = forbidFlipLabel = None
    type1BalloonMessage = 'This value changes the Pokemon\'s first type.'
    type2BalloonMessage = 'This value changes the Pokemon\'s second type.\nMake it match the first type if you want the Pokemon to only have one type.'
    ability1BalloonMessage = 'This value changes the Pokemon\'s first ability.'
    ability2BalloonMessage = 'This value changes the Pokemon\'s second ability.\nMake it the same ability as the first if you want the Pokemon to only have one ability.'
    genderRatioBalloonMessage = 'This value changes the Pokemon\'s gender ratio.'
    forbidFlipBalloonMessage = 'This value dictates whether the Pokemon\'s sprite can be flipped or not.\nThe sprite is flipped when looking at a Pokemon\'s status screen in your team.'

    def buildExtraDataFrame():
        # Tab for changing the Pokemon's types, abilities, gender ratio and whether its sprite can be flipped in-game or not
        # Each type can be chosen with a simple option menu, while each ability requires an autocompleting combobox
        # Gender ratios are limied, so an option menu is enough to display all values
        # The option to forbid sprites for being flipped is a checkbox
        extraDataFrame = Frame(spritePreviewFrame)
        dataEditionNotebook.add(extraDataFrame, text='Other')
        extraDataFrame.grid_rowconfigure(0, weight=1)
        extraDataFrame.grid_rowconfigure(1, weight=1)
        extraDataFrame.grid_rowconfigure(2, weight=1)
        extraDataFrame.grid_columnconfigure(0, weight=1)
        extraDataFrame.grid_columnconfigure(1, weight=1)

        nonlocal type1Label, type2Label, ability1Label, ability2Label, genderRatioLabel, forbidFlipLabel

        type1Frame = Frame(extraDataFrame, padx=2, pady=2)
        type1Frame.grid(row=0, column=0)
        type1Label = Label(type1Frame, text='Type 1')
        mainWindowTooltip.bind_widget(type1Label, balloonmsg=type1BalloonMessage)
        type1Input = OptionMenu(type1Frame, pokemonType1, 'Normal', *POKEMON_TYPES[1:], command=lambda _: checkValue(pokemonType1, type1Label, 'type1', type1BalloonMessage))
        type2Frame = Frame(extraDataFrame, padx=2, pady=2)
        type2Frame.grid(row=1, column=0)
        type2Label = Label(type2Frame, text='Type 2')
        mainWindowTooltip.bind_widget(type2Label, balloonmsg=type2BalloonMessage)
        type2Input = OptionMenu(type2Frame, pokemonType2, 'Normal', *POKEMON_TYPES[1:], command=lambda _: checkValue(pokemonType2, type2Label, 'type2', type2BalloonMessage))
        ability1Frame = Frame(extraDataFrame, padx=2, pady=2)
        ability1Frame.grid(row=0, column=1)
        ability1Label = Label(ability1Frame, text='Ability 1')
        mainWindowTooltip.bind_widget(ability1Label, balloonmsg=ability1BalloonMessage)
        ability1Input = AutocompleteCombobox(ability1Frame, textvariable=pokemonAbility1, width=12)
        ability1Input.set_completion_list([ability.title() for ability in POKEMON_ABILITIES][1:])
        ability2Frame = Frame(extraDataFrame, padx=2, pady=2)
        ability2Frame.grid(row=1, column=1)
        ability2Label = Label(ability2Frame, text='Ability 2')
        mainWindowTooltip.bind_widget(ability2Label, balloonmsg=ability2BalloonMessage)
        ability2Input = AutocompleteCombobox(ability2Frame, textvariable=pokemonAbility2, width=12)
        ability2Input.set_completion_list([ability.title() for ability in POKEMON_ABILITIES][1:])
        genderRatioFrame = Frame(extraDataFrame, padx=2, pady=2)
        genderRatioFrame.grid(row=2, column=0)
        genderRatioLabel = Label(genderRatioFrame, text='Gender')
        mainWindowTooltip.bind_widget(genderRatioLabel, balloonmsg=genderRatioBalloonMessage)
        genderRatioInput = OptionMenu(genderRatioFrame, pokemonGenderRatio, '100% M', *list(POKEMON_GENDER_RATIOS.values())[1:], command=lambda _: checkValue(pokemonGenderRatio, genderRatioLabel, 'gender_ratio', genderRatioBalloonMessage))
        forbidFlipFrame = Frame(extraDataFrame, padx=2, pady=2)
        forbidFlipFrame.grid(row=2, column=1)
        forbidFlipLabel = Label(forbidFlipFrame, text='Forbid Flip')
        mainWindowTooltip.bind_widget(forbidFlipLabel, balloonmsg=forbidFlipBalloonMessage)
        forbidFlipInput = Checkbutton(forbidFlipFrame, variable=pokemonForbidFlip, command=lambda: checkValue(pokemonForbidFlip, forbidFlipLabel, 'forbid_flip', forbidFlipBalloonMessage))

        type1Label.pack(side=TOP)
        type1Input.pack(side=TOP)
        type2Label.pack(side=TOP)
        type2Input.pack(side=TOP)
        ability1Label.pack(side=TOP)
        ability1Input.pack(side=TOP)
        ability1Input.bind('<<ComboboxSelected>>', lambda e: checkValue(e.widget, ability1Label, 'ability1', ability1BalloonMessage))
        ability1Input.bind('<KeyRelease>', lambda e: checkValue(e.widget, ability1Label, 'ability1', ability1BalloonMessage), add='+')
        ability2Label.pack(side=TOP)
        ability2Input.pack(side=TOP)
        ability2Input.bind('<<ComboboxSelected>>', lambda e: checkValue(e.widget, ability2Label, 'ability2', ability2BalloonMessage))
        ability2Input.bind('<KeyRelease>', lambda e: checkValue(e.widget, ability2Label, 'ability2', ability2BalloonMessage), add='+')
        genderRatioLabel.pack(side=TOP)
        genderRatioInput.pack(side=TOP)
        forbidFlipLabel.pack(side=TOP)
        forbidFlipInput.pack(side=TOP)

    movePoolInput = movePoolLabel = None
    movePoolBalloonMessage = 'This value contains the Pokemon\'s levelup learnset.\nEach line must contain a move.\nEach move must be written in the format \'<move>: <level>\'.\nWith <move> being a known Pokemon move from this generation.\nAnd with <level> being a number between 1 and 100.'

    def buildMovePoolFrame():
        # Tab for changing the Pokemon's levelup moveset
        # Only one big scrolling text which may be changed in the future to make it more ergonomic
        movePoolFrame = Frame(spritePreviewFrame)
        dataEditionNotebook.add(movePoolFrame, text='Move Pool')

        nonlocal movePoolInput, movePoolLabel

        movePoolLabel = Label(movePoolFrame, text='Move Pool')
        movePoolInput = ScrolledText(movePoolFrame, undo=True, width=24, height=10)

        movePoolLabel.pack(side=TOP)
        movePoolInput.pack(side=TOP)
        movePoolInput.bind('<KeyRelease>', lambda e: checkValue(e.widget, movePoolLabel, 'move_pool', movePoolBalloonMessage), add='+')

    buildStatFrame()
    buildMovePoolFrame()
    buildExtraDataFrame()

    # Label that displays all errors and warnings from within the pack at the end
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
            messagebox.showerror(title='Error while adjusting Rom', message=str(e))
        else:
            messagebox.showinfo(title='Success', message=f'Rom patched successfully to {path}')

    def saveGUISettings():
        guiargs = Namespace()
        guiargs.patch = opts.patch.get()
        guiargs.sprite_pack = opts.sprite_pack.get()
        persistent_store('adjuster', GAME_EMERALD, guiargs)
        messagebox.showinfo(title='Success', message='Settings saved to persistent storage')

    bottomFrame = Frame(mainWindowFrame)

    # Buttons for adjusting the ROM and saving the current adjuster's configuration
    adjustButton = Button(bottomFrame, text='Adjust Rom', command=adjustRom)
    adjustButton.pack(side=LEFT, padx=(5,5))
    saveButton = Button(bottomFrame, text='Save Settings', command=saveGUISettings)
    saveButton.pack(side=LEFT, padx=(5,5))

    bottomFrame.pack(side=TOP, pady=(5,5))

    def tryValidateSpritePack(_spritePack, _patchChanged = False):
        # Validates the sprite pack if both the ROM/patch file and the sprite packs are valid
        hasError = False
        if isPatchValid:
            global apRom
            apRom = apRom if not _patchChanged else buildApRom(opts.patch.get())
            isRomApState = handle_address_collection(apRom, romVersion, None if _patchChanged else isRomAp.get())
            if _patchChanged:
                # Change the state of the isAP button automatically when a new patch is loaded
                if isRomApState:
                    patchIsAPCheckbox.select()
                else:
                    patchIsAPCheckbox.deselect()
                patchIsAPCheckbox['state'] = DISABLED if not opts.patch.get().endswith('.gba') else NORMAL
        if isPatchValid and isSpritePackValid:
            errors, hasError = validate_sprite_pack(_spritePack)
            adjustButton['state'] = DISABLED if hasError else NORMAL
            spritePreviewErrorLabel['text'] = errors or 'No anomaly detected! The sprite pack is valid.'
        else:
            adjustButton['state'] = DISABLED
            spritePreviewErrorLabel['text'] = 'Both a sprite pack and a patch/ROM must be selected to validate the sprite pack.'
        return hasError

    patchSelect(adjusterSettings.patch or '')
    spritePackSelect(adjusterSettings.sprite_pack or '')

    tkinter_center_window(window)
    window.mainloop()

def setIcon(window):
    # Sets the adjuster's icon
    from tkinter import PhotoImage
    logo = PhotoImage(file=local_path('data', 'icon.png'))
    window.tk.call('wm', 'iconphoto', window._w, logo)

def adjust(args):
    # Adjusts the ROM by applying the patch file of one was given,
    # Building a BPS patch from the given sprite pack, and applying it
    global apRom
    apRom = apRom or buildApRom(args.patch)

    if not args.sprite_pack:
        raise Exception('Cannot adjust the ROM, a sprite pack is required!')

    # Build sprite pack patch & apply patch
    try:
        spritePackBpsPatch = buildSpritePackPatch(args.sprite_pack)
    except Exception as e:
        if hasattr(e, 'message'):
            raise Exception('Error during patch creation: {}'.format(e.message))
        else:
            raise Exception('Error during patch creation: {}'.format(str(e)))

    adjustedApRom = bytearray(len(apRom))
    apply_bps_patch(spritePackBpsPatch, apRom, adjustedApRom)

    romPathWithNoExtension = os.path.splitext(args.patch)
    adjustedRomPath = romPathWithNoExtension[0] + '-adjusted.gba'
    with open(adjustedRomPath, 'wb') as outfile:
        outfile.write(adjustedApRom)
    return adjustedRomPath

def buildApRom(_patch):
    # Builds the AP ROM if a patch file was given
    if not _patch:
        messagebox.showerror(title='Failure', message=f'Cannot build the AP ROM: a patch file or a patched ROM is required!')
        return
    if os.path.splitext(_patch)[-1] == '.gba':
        # Load up the ROM directly
        with open(_patch, 'rb') as stream:
            romData = bytearray(stream.read())
    elif os.path.splitext(_patch)[-1] == '.apemerald':
        # Patch the registered ROM as an AP ROM
        import Patch
        _, apRomPath = Patch.create_rom_file(_patch)
        with open(apRomPath, 'rb') as stream:
            romData = bytearray(stream.read())
    elif frlgSupport:
        # Extend check to .apfirered and .apleafgreen if FR/LG is supported
        romData = frlgBuildApRom(_patch)
        if not romData:
            return
    else:
        messagebox.showerror(title='Failure', message=f'Cannot build the AP ROM: invalid file extension: requires .gba or .apemerald')
        return

    return romData

def buildSpritePackPatch(_spritePack):
    # Builds the BPS patch including all of the sprite pack's data
    errors, hasError = validate_sprite_pack(_spritePack)
    if hasError:
        raise Exception(f'Cannot adjust the ROM as the sprite pack contains errors:\n{errors}')

    spritePackData = get_patch_from_sprite_pack(_spritePack, romVersion)
    spritePackBpsPatch = data_to_bps_patch(spritePackData)
    return spritePackBpsPatch

def launch():
    import colorama, asyncio
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()

if __name__ == '__main__':
    main()
