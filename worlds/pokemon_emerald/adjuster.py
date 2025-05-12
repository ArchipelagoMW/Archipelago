import tkinter as tk
import argparse
import logging
import os
import math

from bps.apply import apply_to_bytearrays as apply_bps_patch

from Utils import local_path, persistent_store, get_adjuster_settings, get_adjuster_settings_no_defaults, \
    tkinter_center_window, data_to_bps_patch
from worlds.pokemon_emerald.adjuster_patcher import get_patch_from_sprite_pack, extract_palette_from_file, \
    extract_sprites, validate_sprite_pack, get_pokemon_data, stringify_pokemon_data, destringify_pokemon_data, \
    validate_pokemon_data_string, stringify_move_pool, destringify_move_pool, keep_different_pokemon_data
from worlds.pokemon_emerald.adjuster_constants import POKEMON_TYPES, POKEMON_FOLDERS, TRAINER_FOLDERS, \
    POKEMON_ABILITIES, POKEMON_GENDER_RATIOS, REVERSE_POKEMON_GENDER_RATIOS
from argparse import Namespace
from tkinter import messagebox

logger = logging.getLogger('EmeraldAdjuster')
isSpritePackValid = False
isPatchValid = False
objectFolders = []
ap_rom = None

GAME_EMERALD = 'Pokemon Emerald'

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
    adjusterSettings = get_adjuster_settings(GAME_EMERALD)

    from tkinter import LEFT, TOP, X, E, W, END, DISABLED, NORMAL, StringVar, \
        IntVar, LabelFrame, Frame, Label, Entry, Button, Checkbutton, \
        OptionMenu, PhotoImage, filedialog, font
    # TODO: Try Comboboxes or CustomTinker OptionMenus
    from tkinter.ttk import Notebook
    from tkinter.tix import Tk, Balloon
    from tkinter.scrolledtext import ScrolledText
    from Utils import __version__ as MWVersion

    window = Tk()
    window.wm_title(f'Archipelago {MWVersion} Emerald Adjuster')
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
            patch = filedialog.askopenfilename(initialdir=oldPatchFolder, initialfile=oldPatchFile, title='Choose an Emerald ROM or an .apemerald patch file.', filetypes=[('Rom & Patch Files', ['.gba', '.apemerald'])])
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
            spritePack = filedialog.askdirectory(initialdir=oldSpritePackFolder, title='Choose a sprite pack.', mustexist=True)
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

    pokemonROMData = None
    pokemonSavedData = None

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
            nonlocal pokemonROMData, pokemonSavedData
            pokemonROMData = get_pokemon_data(folder)
            pokemonData = pokemonROMData.copy()
            pokemonSavedData = None
            # Load local data if it exists and replace existing fields
            pokemonSavedDataPath = os.path.join(opts.sprite_pack.get(), currentSpriteFolder.get(), 'data.txt')
            if os.path.exists(pokemonSavedDataPath):
                with open(pokemonSavedDataPath) as pokemonSavedDataFile:
                    pokemonSavedDataString = pokemonSavedDataFile.read()
                pokemonSavedDataErrors, haspokemonSavedDataError = validate_pokemon_data_string(folder, pokemonSavedDataString)
                if haspokemonSavedDataError:
                    messagebox.showerror(title='Error while loading Pokemon data', message=pokemonSavedDataErrors)
                    pokemonSavedData = None
                else:
                    pokemonSavedData = destringify_pokemon_data(currentSpriteFolder.get(), pokemonSavedDataString)
                    for field in pokemonSavedData:
                        if field == 'dex':
                            pokemonData[field] = pokemonSavedData[field] = (pokemonSavedData[field] << 7) + (pokemonData[field] % 0x7F)
                        else:
                            pokemonData[field] = pokemonSavedData[field]
            
            # Fill in the fields in the data editor and check them
            pokemonHP.set(pokemonData['hp'])
            pokemonSPD.set(pokemonData['spd'])
            pokemonATK.set(pokemonData['atk'])
            pokemonDEF.set(pokemonData['def'])
            pokemonSPATK.set(pokemonData['spatk'])
            pokemonSPDEF.set(pokemonData['spdef'])
            pokemonType1.set(POKEMON_TYPES[pokemonData['type1']])
            pokemonType2.set(POKEMON_TYPES[pokemonData['type2']])
            pokemonAbility1.set(POKEMON_ABILITIES[pokemonData['ability1']].title())
            pokemonAbility2.set(POKEMON_ABILITIES[pokemonData['ability2']].title())
            pokemonGenderRatio.set(POKEMON_GENDER_RATIOS[pokemonData['gender_ratio']])
            pokemonForbidFlip.set(pokemonData['dex'] >> 7)

            movePoolInput.delete('1.0', END)
            movePoolInput.insert(END, stringify_move_pool(pokemonData['move_pool']))

            checkAllFields()

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

    currentSpriteFolder = StringVar(value='--------')
    currentSprite = StringVar(value='--------')
    folders = []
    sprites = []

    spritePreviewFrame = LabelFrame(mainWindowFrame, text='Sprite Preview', padx=8, pady=8)
    spritePreviewFrame.grid_rowconfigure(0, weight=1)
    spritePreviewFrame.grid_rowconfigure(1, weight=1)
    spritePreviewFrame.grid_columnconfigure(0, weight=1)
    spritePreviewFrame.grid_columnconfigure(1, weight=1)

    folderSelectorFrame = Frame(spritePreviewFrame)
    folderSelectorFrame.grid(row=0, column=0, padx=8)
    folderSelectorLabel = Label(folderSelectorFrame, text='Current Folder')
    folderSelector = OptionMenu(folderSelectorFrame, currentSpriteFolder, '--------', *folders)

    spriteSelectorFrame = Frame(spritePreviewFrame)
    spriteSelectorFrame.grid(row=0, column=1, padx=8)
    spriteSelectorLabel = Label(spriteSelectorFrame, text='Current Sprite')
    spriteSelector = OptionMenu(spriteSelectorFrame, currentSprite, '--------', *sprites)

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

    dataEditionLabelFrame = LabelFrame(spritePreviewFrame, text='Pokemon Data Editor', padx=8)
    dataEditionError = Label(spritePreviewFrame, text='A ROM needs to\nbe loaded to edit\na Pokemon\'s data!', padx=8)

    def savePokemonData():
        pokemonName = currentSpriteFolder.get()
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
            'ability2': POKEMON_ABILITIES.index(pokemonAbility2.get().upper()),
            'gender_ratio': REVERSE_POKEMON_GENDER_RATIOS[pokemonGenderRatio.get()],
            'dex': (int(pokemonForbidFlip.get()) << 7) + int(pokemonROMData['dex']) % 0x7F,
            'move_pool': destringify_move_pool(movePoolInput.get('1.0', END))
        }
        # Trim the data that has not been changed
        nonlocal pokemonSavedData
        pokemonSavedData = keep_different_pokemon_data(pokemonROMData, newPokemonData)
        checkAllFields()

        # Save changes to a specific data file
        pokemonSavedDataString = stringify_pokemon_data(pokemonSavedData)
        dataPath = os.path.join(opts.sprite_pack.get(), currentSpriteFolder.get(), 'data.txt')
        if os.path.exists(dataPath):
            os.remove(dataPath)
        if pokemonSavedDataString:
            with open(dataPath, 'w') as dataFile:
                dataFile.write(pokemonSavedDataString)
        
        tryValidateSpritePack(opts.sprite_pack.get())
        messagebox.showinfo(title='Success', message=f'Data for the Pokemon {pokemonName} has been successfully saved!')

    dataEditionNotebook = Notebook(dataEditionLabelFrame, padding=2)
    dataEditionNotebook.pack(side=TOP)
    dataEditionButton = Button(dataEditionLabelFrame, text='Save Data', command=savePokemonData)
    dataEditionButton.pack(side=TOP, pady=4)
    dataEditionTooltip = Balloon(dataEditionLabelFrame)

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
    pokemonGenderRatio = StringVar()
    pokemonForbidFlip = IntVar()

    def updateFieldValidity(fieldName, value):
        validFieldValues[fieldName] = value
        anyValueInvalid = list(k for k, v in validFieldValues.items() if not v)
        dataEditionButton['state'] = DISABLED if anyValueInvalid else NORMAL

    normalFont = font.nametofont("TkDefaultFont")
    boldFont = normalFont.copy()
    boldFont['weight'] = 'bold'
    def checkValue(entry, label, field, balloonMessage):
        fieldValue = str('[ {} ]'.format(entry.get('1.0', END)).replace('\n', ', ') if type(entry) is ScrolledText else entry.get()).strip()
        blueBalloonMessage = '\nThis label is blue because this value is different from the one within the ROM.'
        boldBalloonMessage = '\nThis label is in bold because this value has been changed and hasn\'t been saved.'
        errors, hasError = validate_pokemon_data_string(currentSpriteFolder.get(), { field: fieldValue })
        tempPokemonDataString = '{}: {}'.format(field, fieldValue)
        isDifferentFromROM = True
        isDifferentFromData = False
        internalField = 'dex' if field == 'forbid_flip' else field
        if not hasError:
            tempPokemonData = destringify_pokemon_data(currentSpriteFolder.get(), tempPokemonDataString)
            if 'dex' in list(tempPokemonData.keys()):
                tempPokemonData['dex'] = (tempPokemonData['dex'] << 7) + (pokemonROMData['dex'] % 0x7F)
            differentPokemonData = keep_different_pokemon_data(pokemonROMData, tempPokemonData)
            isDifferentFromROM = internalField in list(differentPokemonData.keys())
            if pokemonSavedData and internalField in list(pokemonSavedData.keys()):
                differentPokemonData = keep_different_pokemon_data(pokemonSavedData, tempPokemonData)
                isDifferentFromData = internalField in list(differentPokemonData.keys())
            else:
                isDifferentFromData = isDifferentFromROM

        label.config(fg='red' if hasError else 'blue' if isDifferentFromROM else 'black', font=boldFont if isDifferentFromData else normalFont)
        dataEditionTooltip.unbind_widget(label)
        dataEditionTooltip.bind_widget(label, balloonmsg=balloonMessage + ('\n' + errors if hasError else blueBalloonMessage if isDifferentFromROM else '') + (boldBalloonMessage if isDifferentFromData else ''))
        updateFieldValidity(field, not hasError)
    
    def checkAllFields():
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

    # TODO: Make the confirm button blue if there is any data to change
    def buildStatFrame():
        # Tab for changing the Pokemon's base stats
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
        dataEditionTooltip.bind_widget(statHPLabel, balloonmsg=statHPBalloonMessage)
        statHPInput = Entry(statHPFrame, textvariable=pokemonHP, width=7)
        statSPDFrame = Frame(statFrame, padx=2, pady=2)
        statSPDFrame.grid(row=0, column=1)
        statSPDLabel = Label(statSPDFrame, text='Speed')
        dataEditionTooltip.bind_widget(statSPDLabel, balloonmsg=statSPDBalloonMessage)
        statSPDInput = Entry(statSPDFrame, textvariable=pokemonSPD, width=7)
        statATKFrame = Frame(statFrame, padx=2, pady=2)
        statATKFrame.grid(row=1, column=0)
        statATKLabel = Label(statATKFrame, text='Attack')
        dataEditionTooltip.bind_widget(statATKLabel, balloonmsg=statATKBalloonMessage)
        statATKInput = Entry(statATKFrame, textvariable=pokemonATK, width=7)
        statDEFFrame = Frame(statFrame, padx=2, pady=2)
        statDEFFrame.grid(row=2, column=0)
        statDEFLabel = Label(statDEFFrame, text='Defense')
        dataEditionTooltip.bind_widget(statDEFLabel, balloonmsg=statDEFBalloonMessage)
        statDEFInput = Entry(statDEFFrame, textvariable=pokemonDEF, width=7)
        statSPATKFrame = Frame(statFrame, padx=2, pady=2)
        statSPATKFrame.grid(row=1, column=1)
        statSPATKLabel = Label(statSPATKFrame, text='Sp. Atk.')
        dataEditionTooltip.bind_widget(statSPATKLabel, balloonmsg=statSPATKBalloonMessage)
        statSPATKInput = Entry(statSPATKFrame, textvariable=pokemonSPATK, width=7)
        statSPDEFFrame = Frame(statFrame, padx=2, pady=2)
        statSPDEFFrame.grid(row=2, column=1)
        statSPDEFLabel = Label(statSPDEFFrame, text='Sp. Def.')
        dataEditionTooltip.bind_widget(statSPDEFLabel, balloonmsg=statSPDEFBalloonMessage)
        statSPDEFInput = Entry(statSPDEFFrame, textvariable=pokemonSPDEF, width=7)

        statHPLabel.pack(side=TOP)
        statHPInput.pack(side=TOP)
        statHPInput.bind('<KeyRelease>', lambda _: checkValue(pokemonHP, statHPLabel, 'hp', statHPBalloonMessage))
        statSPDLabel.pack(side=TOP)
        statSPDInput.pack(side=TOP)
        statSPDInput.bind('<KeyRelease>', lambda _: checkValue(pokemonSPD, statSPDLabel, 'spd', statSPDBalloonMessage))
        statATKLabel.pack(side=TOP)
        statATKInput.pack(side=TOP)
        statATKInput.bind('<KeyRelease>', lambda _: checkValue(pokemonATK, statATKLabel, 'atk', statATKBalloonMessage))
        statDEFLabel.pack(side=TOP)
        statDEFInput.pack(side=TOP)
        statDEFInput.bind('<KeyRelease>', lambda _: checkValue(pokemonDEF, statDEFLabel, 'def', statDEFBalloonMessage))
        statSPATKLabel.pack(side=TOP)
        statSPATKInput.pack(side=TOP)
        statSPATKInput.bind('<KeyRelease>', lambda _: checkValue(pokemonSPATK, statSPATKLabel, 'spatk', statSPATKBalloonMessage))
        statSPDEFLabel.pack(side=TOP)
        statSPDEFInput.pack(side=TOP)
        statSPDEFInput.bind('<KeyRelease>', lambda _: checkValue(pokemonSPDEF, statSPDEFLabel, 'spdef', statSPDEFBalloonMessage))

    type1Label = type2Label = ability1Label = ability2Label = genderRatioLabel = forbidFlipLabel = None
    type1BalloonMessage = 'This value changes the Pokemon\'s first type.'
    type2BalloonMessage = 'This value changes the Pokemon\'s second type.\nMake it match the first type if you want the Pokemon to only have one type.'
    ability1BalloonMessage = 'This value changes the Pokemon\'s first ability.'
    ability2BalloonMessage = 'This value changes the Pokemon\'s second ability.\nMake it -------- if you want the Pokemon to only have one ability.'
    genderRatioBalloonMessage = 'This value changes the Pokemon\'s gender ratio.'
    forbidFlipBalloonMessage = 'This value dictates whether the Pokemon\'s sprite can be flipped or not.\nThe sprite is flipped when looking at a Pokemon\'s status screen in your team.'

    def buildExtraDataFrame():
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
        dataEditionTooltip.bind_widget(type1Label, balloonmsg=type1BalloonMessage)
        type1Input = OptionMenu(type1Frame, pokemonType1, 'Normal', *POKEMON_TYPES[1:], command=lambda _: checkValue(pokemonType1, type1Label, 'type1', type1BalloonMessage))
        type2Frame = Frame(extraDataFrame, padx=2, pady=2)
        type2Frame.grid(row=1, column=0)
        type2Label = Label(type2Frame, text='Type 2')
        dataEditionTooltip.bind_widget(type2Label, balloonmsg=type2BalloonMessage)
        type2Input = OptionMenu(type2Frame, pokemonType2, 'Normal', *POKEMON_TYPES[1:], command=lambda _: checkValue(pokemonType2, type2Label, 'type2', type2BalloonMessage))
        ability1Frame = Frame(extraDataFrame, padx=2, pady=2)
        ability1Frame.grid(row=0, column=1)
        ability1Label = Label(ability1Frame, text='Ability 1')
        dataEditionTooltip.bind_widget(ability1Label, balloonmsg=ability1BalloonMessage)
        ability1Input = Entry(ability1Frame, textvariable=pokemonAbility1, width=12)
        ability2Frame = Frame(extraDataFrame, padx=2, pady=2)
        ability2Frame.grid(row=1, column=1)
        ability2Label = Label(ability2Frame, text='Ability 2')
        dataEditionTooltip.bind_widget(ability2Label, balloonmsg=ability2BalloonMessage)
        ability2Input = Entry(ability2Frame, textvariable=pokemonAbility2, width=12)
        genderRatioFrame = Frame(extraDataFrame, padx=2, pady=2)
        genderRatioFrame.grid(row=2, column=0)
        genderRatioLabel = Label(genderRatioFrame, text='Gender')
        dataEditionTooltip.bind_widget(genderRatioLabel, balloonmsg=genderRatioBalloonMessage)
        genderRatioInput = OptionMenu(genderRatioFrame, pokemonGenderRatio, '100% M', *list(POKEMON_GENDER_RATIOS.values())[1:], command=lambda _: checkValue(pokemonGenderRatio, genderRatioLabel, 'gender_ratio', genderRatioBalloonMessage))
        forbidFlipFrame = Frame(extraDataFrame, padx=2, pady=2)
        forbidFlipFrame.grid(row=2, column=1)
        forbidFlipLabel = Label(forbidFlipFrame, text='Forbid Flip')
        dataEditionTooltip.bind_widget(forbidFlipLabel, balloonmsg=forbidFlipBalloonMessage)
        forbidFlipInput = Checkbutton(forbidFlipFrame, variable=pokemonForbidFlip, command=lambda: checkValue(pokemonForbidFlip, forbidFlipLabel, 'forbid_flip', forbidFlipBalloonMessage))

        type1Label.pack(side=TOP)
        type1Input.pack(side=TOP)
        type2Label.pack(side=TOP)
        type2Input.pack(side=TOP)
        ability1Label.pack(side=TOP)
        ability1Input.pack(side=TOP)
        ability1Input.bind('<KeyRelease>', lambda e: checkValue(e.widget, ability1Label, 'ability1', ability1BalloonMessage))
        ability2Label.pack(side=TOP)
        ability2Input.pack(side=TOP)
        ability2Input.bind('<KeyRelease>', lambda e: checkValue(e.widget, ability2Label, 'ability2', ability2BalloonMessage))
        genderRatioLabel.pack(side=TOP)
        genderRatioInput.pack(side=TOP)
        forbidFlipLabel.pack(side=TOP)
        forbidFlipInput.pack(side=TOP)

    movePoolInput = movePoolLabel = None
    movePoolBalloonMessage = 'This value contains the Pokemon\'s levelup learnset.\nEach line must contain a move.\nEach move must be written in the format \'<move>: <level>\'.\nWith <move> being a known Pokemon move from this generation.\nAnd with <level> being a number between 1 and 100.'

    def buildMovePoolFrame():
        movePoolFrame = Frame(spritePreviewFrame)
        dataEditionNotebook.add(movePoolFrame, text='Move Pool')

        nonlocal movePoolInput, movePoolLabel
        
        movePoolLabel = Label(movePoolFrame, text='Move Pool')
        movePoolInput = ScrolledText(movePoolFrame, undo=True, width=24, height=10)

        movePoolLabel.pack(side=TOP)
        movePoolInput.pack(side=TOP)
        movePoolInput.bind('<KeyRelease>', lambda e: checkValue(e.widget, movePoolLabel, 'move_pool', movePoolBalloonMessage))

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
            messagebox.showerror(title='Error while adjusting Rom', message=str(e))
        else:
            messagebox.showinfo(title='Success', message=f'Rom patched successfully to {path}')

    def saveGUISettings():
        guiargs = Namespace()
        guiargs.patch = opts.patch.get()
        guiargs.sprite_pack = opts.sprite_pack.get()
        persistent_store('adjuster', GAME_EMERALD, guiargs)
        messagebox.showinfo(title='Success', message='Settings saved to persistent storage')

    # Adjust button
    bottomFrame = Frame(mainWindowFrame)

    adjustButton = Button(bottomFrame, text='Adjust Rom', command=adjustRom)
    adjustButton.pack(side=LEFT, padx=(5,5))
    saveButton = Button(bottomFrame, text='Save Settings', command=saveGUISettings)
    saveButton.pack(side=LEFT, padx=(5,5))

    bottomFrame.pack(side=TOP, pady=(5,5))
    
    def tryValidateSpritePack(_spritePack, _patchChanged = False):
        has_error = False
        global ap_rom
        if isPatchValid:
            ap_rom = ap_rom if not _patchChanged else build_ap_rom(opts.patch.get())
        if isPatchValid and isSpritePackValid:
            errors, has_error = validate_sprite_pack(_spritePack, ap_rom)
            adjustButton['state'] = DISABLED if has_error else NORMAL
            spritePreviewErrorLabel['text'] = errors or 'No anomaly detected! The sprite pack is valid.'
        else: 
            adjustButton['state'] = DISABLED
            spritePreviewErrorLabel['text'] = 'Both a sprite pack and a patch/ROM must be selected to validate the sprite pack.'
        return has_error

    patchSelect(adjusterSettings.patch or '')
    spritePackSelect(adjusterSettings.sprite_pack or '')

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
