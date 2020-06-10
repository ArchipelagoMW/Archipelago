#!/usr/bin/env python3
from argparse import Namespace
from glob import glob
import json
import logging
import random
import os
import shutil
from tkinter import Checkbutton, OptionMenu, Toplevel, LabelFrame, PhotoImage, Tk, LEFT, RIGHT, BOTTOM, TOP, StringVar, IntVar, Frame, Label, W, E, X, BOTH, Entry, Spinbox, Button, filedialog, messagebox, ttk
from urllib.parse import urlparse
from urllib.request import urlopen

import ModuleUpdate
ModuleUpdate.update()

from AdjusterMain import adjust
from EntranceRandomizer import parse_arguments
from GuiUtils import ToolTips, set_icon, BackgroundTaskProgress
from Main import main, __version__ as ESVersion
from Rom import Sprite
from Utils import is_bundled, local_path, output_path, open_file


def guiMain(args=None):
    mainWindow = Tk()
    mainWindow.wm_title("Entrance Shuffle %s" % ESVersion)

    set_icon(mainWindow)

    notebook = ttk.Notebook(mainWindow)
    randomizerWindow = ttk.Frame(notebook)
    adjustWindow = ttk.Frame(notebook)
    customWindow = ttk.Frame(notebook)
    notebook.add(randomizerWindow, text='Randomize')
    notebook.add(adjustWindow, text='Adjust')
    notebook.add(customWindow, text='Custom')
    notebook.pack()

    # Shared Controls

    farBottomFrame = Frame(mainWindow)

    def open_output():
        open_file(output_path(''))

    openOutputButton = Button(farBottomFrame, text='Open Output Directory', command=open_output)

    if os.path.exists(local_path('README.html')):
        def open_readme():
            open_file(local_path('README.html'))
        openReadmeButton = Button(farBottomFrame, text='Open Documentation', command=open_readme)
        openReadmeButton.pack(side=LEFT)

    farBottomFrame.pack(side=BOTTOM, fill=X, padx=5, pady=5)

    # randomizer controls

    topFrame = Frame(randomizerWindow)
    rightHalfFrame = Frame(topFrame)
    checkBoxFrame = Frame(rightHalfFrame)

    createSpoilerVar = IntVar()
    createSpoilerCheckbutton = Checkbutton(checkBoxFrame, text="Create Spoiler Log", variable=createSpoilerVar)
    suppressRomVar = IntVar()
    suppressRomCheckbutton = Checkbutton(checkBoxFrame, text="Do not create patched Rom", variable=suppressRomVar)
    openpyramidVar = IntVar()
    openpyramidCheckbutton = Checkbutton(checkBoxFrame, text="Pre-open Pyramid Hole", variable=openpyramidVar)
    mcsbshuffleFrame = Frame(checkBoxFrame)
    mcsbLabel = Label(mcsbshuffleFrame, text="Shuffle: ")
    mapshuffleVar = IntVar()
    mapshuffleCheckbutton = Checkbutton(mcsbshuffleFrame, text="Maps", variable=mapshuffleVar)
    compassshuffleVar = IntVar()
    compassshuffleCheckbutton = Checkbutton(mcsbshuffleFrame, text="Compasses", variable=compassshuffleVar)
    keyshuffleVar = IntVar()
    keyshuffleCheckbutton = Checkbutton(mcsbshuffleFrame, text="Keys", variable=keyshuffleVar)
    bigkeyshuffleVar = IntVar()
    bigkeyshuffleCheckbutton = Checkbutton(mcsbshuffleFrame, text="BigKeys", variable=bigkeyshuffleVar)
    retroVar = IntVar()
    retroCheckbutton = Checkbutton(checkBoxFrame, text="Retro mode (universal keys)", variable=retroVar)
    shuffleGanonVar = IntVar()
    shuffleGanonVar.set(1) #set default
    shuffleGanonCheckbutton = Checkbutton(checkBoxFrame, text="Include Ganon's Tower and Pyramid Hole in shuffle pool", variable=shuffleGanonVar)
    hintsVar = IntVar()
    hintsVar.set(1) #set default
    hintsCheckbutton = Checkbutton(checkBoxFrame, text="Include Helpful Hints", variable=hintsVar)
    customVar = IntVar()
    customCheckbutton = Checkbutton(checkBoxFrame, text="Use custom item pool", variable=customVar)
    balancingVar = IntVar()
    balancingVar.set(1) #set default
    balancingCheckbutton = Checkbutton(checkBoxFrame, text="Multiworld Progression Balancing", variable=balancingVar)
    createSpoilerCheckbutton.pack(expand=True, anchor=W)
    suppressRomCheckbutton.pack(expand=True, anchor=W)
    openpyramidCheckbutton.pack(expand=True, anchor=W)
    mcsbshuffleFrame.pack(expand=True, anchor=W)
    mcsbLabel.grid(row=0, column=0)
    mapshuffleCheckbutton.grid(row=0, column=1)
    compassshuffleCheckbutton.grid(row=0, column=2)
    keyshuffleCheckbutton.grid(row=0, column=3)
    bigkeyshuffleCheckbutton.grid(row=0, column=4)
    retroCheckbutton.pack(expand=True, anchor=W)
    shuffleGanonCheckbutton.pack(expand=True, anchor=W)
    hintsCheckbutton.pack(expand=True, anchor=W)
    customCheckbutton.pack(expand=True, anchor=W)
    balancingCheckbutton.pack(expand=True, anchor=W)

    romOptionsFrame = LabelFrame(rightHalfFrame, text="Rom options")
    romOptionsFrame.columnconfigure(0, weight=1)
    romOptionsFrame.columnconfigure(1, weight=1)
    for i in range(5):
        romOptionsFrame.rowconfigure(i, weight=1)

    disableMusicVar = IntVar()
    disableMusicCheckbutton = Checkbutton(romOptionsFrame, text="Disable music", variable=disableMusicVar)
    disableMusicCheckbutton.grid(row=0, column=0, sticky=E)

    spriteDialogFrame = Frame(romOptionsFrame)
    spriteDialogFrame.grid(row=0, column=1)
    baseSpriteLabel = Label(spriteDialogFrame, text='Sprite:')

    spriteNameVar = StringVar()
    sprite = None
    def set_sprite(sprite_param):
        nonlocal sprite
        if sprite_param is None or not sprite_param.valid:
            sprite = None
            spriteNameVar.set('(unchanged)')
        else:
            sprite = sprite_param
            spriteNameVar.set(sprite.name)

    set_sprite(None)
    spriteNameVar.set('(unchanged)')
    spriteEntry = Label(spriteDialogFrame, textvariable=spriteNameVar)

    def SpriteSelect():
        SpriteSelector(mainWindow, set_sprite)

    spriteSelectButton = Button(spriteDialogFrame, text='...', command=SpriteSelect)

    baseSpriteLabel.pack(side=LEFT)
    spriteEntry.pack(side=LEFT)
    spriteSelectButton.pack(side=LEFT)

    quickSwapVar = IntVar()
    quickSwapCheckbutton = Checkbutton(romOptionsFrame, text="L/R Quickswapping", variable=quickSwapVar)
    quickSwapCheckbutton.grid(row=1, column=0, sticky=E)

    fastMenuFrame = Frame(romOptionsFrame)
    fastMenuFrame.grid(row=1, column=1, sticky=E)
    fastMenuLabel = Label(fastMenuFrame, text='Menu speed')
    fastMenuLabel.pack(side=LEFT)
    fastMenuVar = StringVar()
    fastMenuVar.set('normal')
    fastMenuOptionMenu = OptionMenu(fastMenuFrame, fastMenuVar, 'normal', 'instant', 'double', 'triple', 'quadruple', 'half')
    fastMenuOptionMenu.pack(side=LEFT)

    heartcolorFrame = Frame(romOptionsFrame)
    heartcolorFrame.grid(row=2, column=0, sticky=E)
    heartcolorLabel = Label(heartcolorFrame, text='Heart color')
    heartcolorLabel.pack(side=LEFT)
    heartcolorVar = StringVar()
    heartcolorVar.set('red')
    heartcolorOptionMenu = OptionMenu(heartcolorFrame, heartcolorVar, 'red', 'blue', 'green', 'yellow', 'random')
    heartcolorOptionMenu.pack(side=LEFT)

    heartbeepFrame = Frame(romOptionsFrame)
    heartbeepFrame.grid(row=2, column=1, sticky=E)
    heartbeepLabel = Label(heartbeepFrame, text='Heartbeep')
    heartbeepLabel.pack(side=LEFT)
    heartbeepVar = StringVar()
    heartbeepVar.set('normal')
    heartbeepOptionMenu = OptionMenu(heartbeepFrame, heartbeepVar, 'double', 'normal', 'half', 'quarter', 'off')
    heartbeepOptionMenu.pack(side=LEFT)

    owPalettesFrame = Frame(romOptionsFrame)
    owPalettesFrame.grid(row=3, column=0, sticky=E)
    owPalettesLabel = Label(owPalettesFrame, text='Overworld palettes')
    owPalettesLabel.pack(side=LEFT)
    owPalettesVar = StringVar()
    owPalettesVar.set('default')
    owPalettesOptionMenu = OptionMenu(owPalettesFrame, owPalettesVar, 'default', 'random', 'blackout')
    owPalettesOptionMenu.pack(side=LEFT)

    uwPalettesFrame = Frame(romOptionsFrame)
    uwPalettesFrame.grid(row=3, column=1, sticky=E)
    uwPalettesLabel = Label(uwPalettesFrame, text='Dungeon palettes')
    uwPalettesLabel.pack(side=LEFT)
    uwPalettesVar = StringVar()
    uwPalettesVar.set('default')
    uwPalettesOptionMenu = OptionMenu(uwPalettesFrame, uwPalettesVar, 'default', 'random', 'blackout')
    uwPalettesOptionMenu.pack(side=LEFT)

    romDialogFrame = Frame(romOptionsFrame)
    romDialogFrame.grid(row=4, column=0, columnspan=2, sticky=W+E)

    baseRomLabel = Label(romDialogFrame, text='Base Rom: ')
    romVar = StringVar(value="Zelda no Densetsu - Kamigami no Triforce (Japan).sfc")
    romEntry = Entry(romDialogFrame, textvariable=romVar)

    def RomSelect():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".sfc", ".smc")), ("All Files", "*")])
        import Patch
        try:
            Patch.get_base_rom_bytes(rom)  # throws error on checksum fail
        except Exception as e:
            logging.exception(e)
            messagebox.showerror(title="Error while reading ROM", message=str(e))
        else:
            romVar.set(rom)
            romSelectButton['state'] = "disabled"
            romSelectButton["text"] = "ROM verified"
    romSelectButton = Button(romDialogFrame, text='Select Rom', command=RomSelect)

    baseRomLabel.pack(side=LEFT)
    romEntry.pack(side=LEFT, expand=True, fill=X)
    romSelectButton.pack(side=LEFT)

    checkBoxFrame.pack(side=TOP, anchor=W, padx=5, pady=10)
    romOptionsFrame.pack(expand=True, fill=BOTH, padx=3)

    drowDownFrame = Frame(topFrame)

    modeFrame = Frame(drowDownFrame)
    modeVar = StringVar()
    modeVar.set('open')
    modeOptionMenu = OptionMenu(modeFrame, modeVar, 'standard', 'open', 'inverted')
    modeOptionMenu.pack(side=RIGHT)
    modeLabel = Label(modeFrame, text='Game mode')
    modeLabel.pack(side=LEFT)

    logicFrame = Frame(drowDownFrame)
    logicVar = StringVar()
    logicVar.set('noglitches')
    logicOptionMenu = OptionMenu(logicFrame, logicVar, 'noglitches', 'minorglitches', 'owglitches', 'nologic')
    logicOptionMenu.pack(side=RIGHT)
    logicLabel = Label(logicFrame, text='Game logic')
    logicLabel.pack(side=LEFT)

    goalFrame = Frame(drowDownFrame)
    goalVar = StringVar()
    goalVar.set('ganon')
    goalOptionMenu = OptionMenu(goalFrame, goalVar, 'ganon', 'pedestal', 'dungeons', 'triforcehunt',
                                'localtriforcehunt', 'crystals')
    goalOptionMenu.pack(side=RIGHT)
    goalLabel = Label(goalFrame, text='Game goal')
    goalLabel.pack(side=LEFT)

    crystalsGTFrame = Frame(drowDownFrame)
    crystalsGTVar = StringVar()
    crystalsGTVar.set('7')
    crystalsGTOptionMenu = OptionMenu(crystalsGTFrame, crystalsGTVar, '0', '1', '2', '3', '4', '5', '6', '7', 'random')
    crystalsGTOptionMenu.pack(side=RIGHT)
    crystalsGTLabel = Label(crystalsGTFrame, text='Crystals to open Ganon\'s Tower')
    crystalsGTLabel.pack(side=LEFT)

    crystalsGanonFrame = Frame(drowDownFrame)
    crystalsGanonVar = StringVar()
    crystalsGanonVar.set('7')
    crystalsGanonOptionMenu = OptionMenu(crystalsGanonFrame, crystalsGanonVar, '0', '1', '2', '3', '4', '5', '6', '7', 'random')
    crystalsGanonOptionMenu.pack(side=RIGHT)
    crystalsGanonLabel = Label(crystalsGanonFrame, text='Crystals to fight Ganon')
    crystalsGanonLabel.pack(side=LEFT)

    swordFrame = Frame(drowDownFrame)
    swordVar = StringVar()
    swordVar.set('random')
    swordOptionMenu = OptionMenu(swordFrame, swordVar, 'random', 'assured', 'swordless', 'vanilla')
    swordOptionMenu.pack(side=RIGHT)
    swordLabel = Label(swordFrame, text='Sword availability')
    swordLabel.pack(side=LEFT)

    difficultyFrame = Frame(drowDownFrame)
    difficultyVar = StringVar()
    difficultyVar.set('normal')
    difficultyOptionMenu = OptionMenu(difficultyFrame, difficultyVar, 'normal', 'hard', 'expert')
    difficultyOptionMenu.pack(side=RIGHT)
    difficultyLabel = Label(difficultyFrame, text='Difficulty: item pool')
    difficultyLabel.pack(side=LEFT)

    itemfunctionFrame = Frame(drowDownFrame)
    itemfunctionVar = StringVar()
    itemfunctionVar.set('normal')
    itemfunctionOptionMenu = OptionMenu(itemfunctionFrame, itemfunctionVar, 'normal', 'hard', 'expert')
    itemfunctionOptionMenu.pack(side=RIGHT)
    itemfunctionLabel = Label(itemfunctionFrame, text='Difficulty: item functionality')
    itemfunctionLabel.pack(side=LEFT)

    timerFrame = Frame(drowDownFrame)
    timerVar = StringVar()
    timerVar.set('none')
    timerOptionMenu = OptionMenu(timerFrame, timerVar, 'none', 'display', 'timed', 'timed-ohko', 'ohko', 'timed-countdown')
    timerOptionMenu.pack(side=RIGHT)
    timerLabel = Label(timerFrame, text='Timer setting')
    timerLabel.pack(side=LEFT)

    dungeonCounterFrame = Frame(drowDownFrame)
    dungeonCounterVar = StringVar()
    dungeonCounterVar.set('auto')
    dungeonCounterOptionMenu = OptionMenu(dungeonCounterFrame, dungeonCounterVar, 'auto', 'off', 'on', 'on_compass_pickup')
    dungeonCounterOptionMenu.pack(side=RIGHT)
    dungeonCounterLabel = Label(dungeonCounterFrame, text='Dungeon Chest Counters')
    dungeonCounterLabel.pack(side=LEFT)

    progressiveFrame = Frame(drowDownFrame)
    progressiveVar = StringVar()
    progressiveVar.set('on')
    progressiveOptionMenu = OptionMenu(progressiveFrame, progressiveVar, 'on', 'off', 'random')
    progressiveOptionMenu.pack(side=RIGHT)
    progressiveLabel = Label(progressiveFrame, text='Progressive equipment')
    progressiveLabel.pack(side=LEFT)

    accessibilityFrame = Frame(drowDownFrame)
    accessibilityVar = StringVar()
    accessibilityVar.set('items')
    accessibilityOptionMenu = OptionMenu(accessibilityFrame, accessibilityVar, 'items', 'locations', 'none')
    accessibilityOptionMenu.pack(side=RIGHT)
    accessibilityLabel = Label(accessibilityFrame, text='Item accessibility')
    accessibilityLabel.pack(side=LEFT)

    algorithmFrame = Frame(drowDownFrame)
    algorithmVar = StringVar()
    algorithmVar.set('balanced')
    algorithmOptionMenu = OptionMenu(algorithmFrame, algorithmVar, 'freshness', 'flood', 'vt21', 'vt22', 'vt25', 'vt26', 'balanced')
    algorithmOptionMenu.pack(side=RIGHT)
    algorithmLabel = Label(algorithmFrame, text='Item distribution algorithm')
    algorithmLabel.pack(side=LEFT)

    shuffleFrame = Frame(drowDownFrame)
    shuffleVar = StringVar()
    shuffleVar.set('full')
    shuffleOptionMenu = OptionMenu(shuffleFrame, shuffleVar, 'vanilla', 'simple', 'restricted', 'full', 'crossed', 'insanity', 'restricted_legacy', 'full_legacy', 'madness_legacy', 'insanity_legacy', 'dungeonsfull', 'dungeonssimple')
    shuffleOptionMenu.pack(side=RIGHT)
    shuffleLabel = Label(shuffleFrame, text='Entrance shuffle algorithm')
    shuffleLabel.pack(side=LEFT)

    modeFrame.pack(expand=True, anchor=E)
    logicFrame.pack(expand=True, anchor=E)
    goalFrame.pack(expand=True, anchor=E)
    crystalsGTFrame.pack(expand=True, anchor=E)
    crystalsGanonFrame.pack(expand=True, anchor=E)
    swordFrame.pack(expand=True, anchor=E)
    difficultyFrame.pack(expand=True, anchor=E)
    itemfunctionFrame.pack(expand=True, anchor=E)
    timerFrame.pack(expand=True, anchor=E)
    dungeonCounterFrame.pack(expand=True, anchor=E)
    progressiveFrame.pack(expand=True, anchor=E)
    accessibilityFrame.pack(expand=True, anchor=E)
    algorithmFrame.pack(expand=True, anchor=E)
    shuffleFrame.pack(expand=True, anchor=E)

    enemizerFrame = LabelFrame(randomizerWindow, text="Enemizer", padx=5, pady=2)


    enemizerPathFrame = Frame(enemizerFrame)
    enemizerPathFrame.grid(row=0, column=0, columnspan=3, sticky=W+E, padx=3)
    enemizerCLIlabel = Label(enemizerPathFrame, text="EnemizerCLI path: ")
    enemizerCLIlabel.pack(side=LEFT)
    enemizerCLIpathVar = StringVar(value="EnemizerCLI/EnemizerCLI.Core")
    enemizerCLIpathEntry = Entry(enemizerPathFrame, textvariable=enemizerCLIpathVar)
    enemizerCLIpathEntry.pack(side=LEFT, expand=True, fill=X)
    def EnemizerSelectPath():
        path = filedialog.askopenfilename(filetypes=[("EnemizerCLI executable", "*EnemizerCLI*")])
        if path:
            enemizerCLIpathVar.set(path)
    enemizerCLIbrowseButton = Button(enemizerPathFrame, text='...', command=EnemizerSelectPath)
    enemizerCLIbrowseButton.pack(side=LEFT)

    potShuffleVar = IntVar()
    potShuffleButton = Checkbutton(enemizerFrame, text="Pot shuffle", variable=potShuffleVar)
    potShuffleButton.grid(row=0, column=3)

    enemizerEnemyFrame = Frame(enemizerFrame)
    enemizerEnemyFrame.grid(row=1, column=0, pady=5)
    enemizerEnemyLabel = Label(enemizerEnemyFrame, text='Enemy shuffle')
    enemizerEnemyLabel.pack(side=LEFT)
    enemyShuffleVar = StringVar()
    enemyShuffleVar.set('none')
    enemizerEnemyOption = OptionMenu(enemizerEnemyFrame, enemyShuffleVar, 'none', 'shuffled', 'chaos')
    enemizerEnemyOption.pack(side=LEFT)

    enemizerBossFrame = Frame(enemizerFrame)
    enemizerBossFrame.grid(row=1, column=1)
    enemizerBossLabel = Label(enemizerBossFrame, text='Boss shuffle')
    enemizerBossLabel.pack(side=LEFT)
    enemizerBossVar = StringVar()
    enemizerBossVar.set('none')
    enemizerBossOption = OptionMenu(enemizerBossFrame, enemizerBossVar, 'none', 'basic', 'normal', 'chaos')
    enemizerBossOption.pack(side=LEFT)

    enemizerDamageFrame = Frame(enemizerFrame)
    enemizerDamageFrame.grid(row=1, column=2)
    enemizerDamageLabel = Label(enemizerDamageFrame, text='Enemy damage')
    enemizerDamageLabel.pack(side=LEFT)
    enemizerDamageVar = StringVar()
    enemizerDamageVar.set('default')
    enemizerDamageOption = OptionMenu(enemizerDamageFrame, enemizerDamageVar, 'default', 'shuffled', 'chaos')
    enemizerDamageOption.pack(side=LEFT)

    enemizerHealthFrame = Frame(enemizerFrame)
    enemizerHealthFrame.grid(row=1, column=3)
    enemizerHealthLabel = Label(enemizerHealthFrame, text='Enemy health')
    enemizerHealthLabel.pack(side=LEFT)
    enemizerHealthVar = StringVar()
    enemizerHealthVar.set('default')
    enemizerHealthOption = OptionMenu(enemizerHealthFrame, enemizerHealthVar, 'default', 'easy', 'normal', 'hard', 'expert')
    enemizerHealthOption.pack(side=LEFT)

    multiworldframe = LabelFrame(randomizerWindow, text="Multiworld", padx=5, pady=2)


    worldLabel = Label(multiworldframe, text='Worlds')
    worldVar = StringVar()
    worldSpinbox = Spinbox(multiworldframe, from_=1, to=255, width=5, textvariable=worldVar)
    namesLabel = Label(multiworldframe, text='Player names')
    namesVar = StringVar()
    namesEntry = Entry(multiworldframe, textvariable=namesVar)
    seedLabel = Label(multiworldframe, text='Seed #')
    seedVar = StringVar()
    seedEntry = Entry(multiworldframe, width=15, textvariable=seedVar)
    countLabel = Label(multiworldframe, text='Count')
    countVar = StringVar()
    countSpinbox = Spinbox(multiworldframe, from_=1, to=100, width=5, textvariable=countVar)

    def generateRom():
        guiargs = Namespace()
        guiargs.multi = int(worldVar.get())
        guiargs.names = namesVar.get()
        guiargs.seed = int(seedVar.get()) if seedVar.get() else None
        guiargs.count = int(countVar.get()) if countVar.get() != '1' else None
        guiargs.mode = modeVar.get()
        guiargs.logic = logicVar.get()
        guiargs.goal = goalVar.get()
        guiargs.crystals_gt = crystalsGTVar.get()
        guiargs.crystals_ganon = crystalsGanonVar.get()
        guiargs.swords = swordVar.get()
        guiargs.difficulty = difficultyVar.get()
        guiargs.item_functionality = itemfunctionVar.get()
        guiargs.timer = timerVar.get()
        guiargs.skip_progression_balancing = not balancingVar.get()
        if guiargs.timer == "none":
            guiargs.timer = False
        guiargs.dungeon_counters = dungeonCounterVar.get()
        if guiargs.dungeon_counters == "on_compass_pickup":
            guiargs.dungeon_counters = "pickup"
        elif guiargs.dungeon_counters == "on":
            guiargs.dungeon_counters = True
        elif guiargs.dungeon_counters == "off":
            guiargs.dungeon_counters = False
        guiargs.progressive = progressiveVar.get()
        guiargs.accessibility = accessibilityVar.get()
        guiargs.algorithm = algorithmVar.get()
        guiargs.shuffle = shuffleVar.get()
        guiargs.heartbeep = heartbeepVar.get()
        guiargs.heartcolor = heartcolorVar.get()
        guiargs.fastmenu = fastMenuVar.get()
        guiargs.create_spoiler = bool(createSpoilerVar.get())
        guiargs.suppress_rom = bool(suppressRomVar.get())
        guiargs.openpyramid = bool(openpyramidVar.get())
        guiargs.mapshuffle = bool(mapshuffleVar.get())
        guiargs.compassshuffle = bool(compassshuffleVar.get())
        guiargs.keyshuffle = bool(keyshuffleVar.get())
        guiargs.bigkeyshuffle = bool(bigkeyshuffleVar.get())
        guiargs.retro = bool(retroVar.get())
        guiargs.quickswap = bool(quickSwapVar.get())
        guiargs.disablemusic = bool(disableMusicVar.get())
        guiargs.ow_palettes = owPalettesVar.get()
        guiargs.uw_palettes = uwPalettesVar.get()
        guiargs.shuffleganon = bool(shuffleGanonVar.get())
        guiargs.hints = bool(hintsVar.get())
        guiargs.enemizercli = enemizerCLIpathVar.get()
        guiargs.shufflebosses = enemizerBossVar.get()
        guiargs.shuffleenemies = enemyShuffleVar.get()
        guiargs.enemy_health = enemizerHealthVar.get()
        guiargs.enemy_damage = enemizerDamageVar.get()
        guiargs.shufflepots = bool(potShuffleVar.get())
        guiargs.custom = bool(customVar.get())
        guiargs.customitemarray = [int(bowVar.get()), int(silverarrowVar.get()), int(boomerangVar.get()), int(magicboomerangVar.get()), int(hookshotVar.get()), int(mushroomVar.get()), int(magicpowderVar.get()), int(firerodVar.get()),
                                   int(icerodVar.get()), int(bombosVar.get()), int(etherVar.get()), int(quakeVar.get()), int(lampVar.get()), int(hammerVar.get()), int(shovelVar.get()), int(fluteVar.get()), int(bugnetVar.get()),
                                   int(bookVar.get()), int(bottleVar.get()), int(somariaVar.get()), int(byrnaVar.get()), int(capeVar.get()), int(mirrorVar.get()), int(bootsVar.get()), int(powergloveVar.get()), int(titansmittVar.get()),
                                   int(proggloveVar.get()), int(flippersVar.get()), int(pearlVar.get()), int(heartpieceVar.get()), int(fullheartVar.get()), int(sancheartVar.get()), int(sword1Var.get()), int(sword2Var.get()),
                                   int(sword3Var.get()), int(sword4Var.get()), int(progswordVar.get()), int(shield1Var.get()), int(shield2Var.get()), int(shield3Var.get()), int(progshieldVar.get()), int(bluemailVar.get()),
                                   int(redmailVar.get()), int(progmailVar.get()), int(halfmagicVar.get()), int(quartermagicVar.get()), int(bcap5Var.get()), int(bcap10Var.get()), int(acap5Var.get()), int(acap10Var.get()),
                                   int(arrow1Var.get()), int(arrow10Var.get()), int(bomb1Var.get()), int(bomb3Var.get()), int(rupee1Var.get()), int(rupee5Var.get()), int(rupee20Var.get()), int(rupee50Var.get()), int(rupee100Var.get()),
                                   int(rupee300Var.get()), int(rupoorVar.get()), int(blueclockVar.get()), int(greenclockVar.get()), int(redclockVar.get()), int(progbowVar.get()), int(bomb10Var.get()), int(triforcepieceVar.get()),
                                   int(triforcecountVar.get()), int(triforceVar.get()),  int(rupoorcostVar.get()), int(universalkeyVar.get())]
        guiargs.rom = romVar.get()
        guiargs.sprite = sprite
        # get default values for missing parameters
        for k,v in vars(parse_arguments(['--multi', str(guiargs.multi)])).items():
            if k not in vars(guiargs):
                setattr(guiargs, k, v)
            elif type(v) is dict: # use same settings for every player
                setattr(guiargs, k, {player: getattr(guiargs, k) for player in range(1, guiargs.multi + 1)})
        try:
            if not guiargs.suppress_rom and not os.path.exists(guiargs.rom):
                raise FileNotFoundError(f"Could not find specified rom file {guiargs.rom}")
            if guiargs.count is not None:
                seed = guiargs.seed
                for _ in range(guiargs.count):
                    main(seed=seed, args=guiargs)
                    seed = random.randint(0, 999999999)
            else:
                main(seed=guiargs.seed, args=guiargs)
        except Exception as e:
            logging.exception(e)
            messagebox.showerror(title="Error while creating seed", message=str(e))
        else:
            messagebox.showinfo(title="Success", message="Rom patched successfully")

    generateButton = Button(farBottomFrame, text='Generate Patched Rom', command=generateRom)

    worldLabel.pack(side=LEFT)
    worldSpinbox.pack(side=LEFT)
    namesLabel.pack(side=LEFT)
    namesEntry.pack(side=LEFT, expand=True, fill=X)
    seedLabel.pack(side=LEFT,  padx=(5, 0))
    seedEntry.pack(side=LEFT)
    countLabel.pack(side=LEFT, padx=(5, 0))
    countSpinbox.pack(side=LEFT)
    generateButton.pack(side=RIGHT, padx=(5, 0))

    openOutputButton.pack(side=LEFT)

    drowDownFrame.pack(side=LEFT)
    rightHalfFrame.pack(side=RIGHT)
    topFrame.pack(side=TOP)
    multiworldframe.pack(side=BOTTOM, expand=True, fill=X)
    enemizerFrame.pack(side=BOTTOM, fill=BOTH)

    # Adjuster Controls

    topFrame2 = Frame(adjustWindow)
    rightHalfFrame2 = Frame(topFrame2)
    checkBoxFrame2 = Frame(rightHalfFrame2)

    quickSwapCheckbutton2 = Checkbutton(checkBoxFrame2, text="Enabled L/R Item quickswapping", variable=quickSwapVar)
    disableMusicCheckbutton2 = Checkbutton(checkBoxFrame2, text="Disable game music", variable=disableMusicVar)

    quickSwapCheckbutton2.pack(expand=True, anchor=W)
    disableMusicCheckbutton2.pack(expand=True, anchor=W)

    fileDialogFrame2 = Frame(rightHalfFrame2)

    romDialogFrame2 = Frame(fileDialogFrame2)
    baseRomLabel2 = Label(romDialogFrame2, text='Rom to adjust')
    romVar2 = StringVar()
    romEntry2 = Entry(romDialogFrame2, textvariable=romVar2)

    def RomSelect2():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".sfc", ".smc")), ("All Files", "*")])
        romVar2.set(rom)
    romSelectButton2 = Button(romDialogFrame2, text='Select Rom', command=RomSelect2)

    baseRomLabel2.pack(side=LEFT)
    romEntry2.pack(side=LEFT)
    romSelectButton2.pack(side=LEFT)

    spriteDialogFrame2 = Frame(fileDialogFrame2)
    baseSpriteLabel2 = Label(spriteDialogFrame2, text='Link Sprite')
    spriteEntry2 = Label(spriteDialogFrame2, textvariable=spriteNameVar)

    def SpriteSelectAdjuster():
        SpriteSelector(mainWindow, set_sprite, adjuster=True)

    spriteSelectButton2 = Button(spriteDialogFrame2, text='Select Sprite', command=SpriteSelectAdjuster)

    baseSpriteLabel2.pack(side=LEFT)
    spriteEntry2.pack(side=LEFT)
    spriteSelectButton2.pack(side=LEFT)

    romDialogFrame2.pack()
    spriteDialogFrame2.pack()

    checkBoxFrame2.pack()
    fileDialogFrame2.pack()

    drowDownFrame2 = Frame(topFrame2)
    heartbeepFrame2 = Frame(drowDownFrame2)
    heartbeepOptionMenu2 = OptionMenu(heartbeepFrame2, heartbeepVar, 'double', 'normal', 'half', 'quarter', 'off')
    heartbeepOptionMenu2.pack(side=RIGHT)
    heartbeepLabel2 = Label(heartbeepFrame2, text='Heartbeep sound rate')
    heartbeepLabel2.pack(side=LEFT)

    heartcolorFrame2 = Frame(drowDownFrame2)
    heartcolorOptionMenu2 = OptionMenu(heartcolorFrame2, heartcolorVar, 'red', 'blue', 'green', 'yellow', 'random')
    heartcolorOptionMenu2.pack(side=RIGHT)
    heartcolorLabel2 = Label(heartcolorFrame2, text='Heart color')
    heartcolorLabel2.pack(side=LEFT)

    fastMenuFrame2 = Frame(drowDownFrame2)
    fastMenuOptionMenu2 = OptionMenu(fastMenuFrame2, fastMenuVar, 'normal', 'instant', 'double', 'triple', 'quadruple', 'half')
    fastMenuOptionMenu2.pack(side=RIGHT)
    fastMenuLabel2 = Label(fastMenuFrame2, text='Menu speed')
    fastMenuLabel2.pack(side=LEFT)

    owPalettesFrame2 = Frame(drowDownFrame2)
    owPalettesOptionMenu2 = OptionMenu(owPalettesFrame2, owPalettesVar, 'default', 'random', 'blackout')
    owPalettesOptionMenu2.pack(side=RIGHT)
    owPalettesLabel2 = Label(owPalettesFrame2, text='Overworld palettes')
    owPalettesLabel2.pack(side=LEFT)

    uwPalettesFrame2 = Frame(drowDownFrame2)
    uwPalettesOptionMenu2 = OptionMenu(uwPalettesFrame2, uwPalettesVar, 'default', 'random', 'blackout')
    uwPalettesOptionMenu2.pack(side=RIGHT)
    uwPalettesLabel2 = Label(uwPalettesFrame2, text='Dungeon palettes')
    uwPalettesLabel2.pack(side=LEFT)

    heartbeepFrame2.pack(expand=True, anchor=E)
    heartcolorFrame2.pack(expand=True, anchor=E)
    fastMenuFrame2.pack(expand=True, anchor=E)
    owPalettesFrame2.pack(expand=True, anchor=E)
    uwPalettesFrame2.pack(expand=True, anchor=E)

    bottomFrame2 = Frame(topFrame2)

    def adjustRom():
        guiargs = Namespace()
        guiargs.heartbeep = heartbeepVar.get()
        guiargs.heartcolor = heartcolorVar.get()
        guiargs.fastmenu = fastMenuVar.get()
        guiargs.ow_palettes = owPalettesVar.get()
        guiargs.uw_palettes = uwPalettesVar.get()
        guiargs.quickswap = bool(quickSwapVar.get())
        guiargs.disablemusic = bool(disableMusicVar.get())
        guiargs.rom = romVar2.get()
        guiargs.baserom = romVar.get()
        guiargs.sprite = sprite
        try:
            guiargs, path = adjust(args=guiargs)
        except Exception as e:
            logging.exception(e)
            messagebox.showerror(title="Error while adjusting Rom", message=str(e))
        else:
            messagebox.showinfo(title="Success", message="Rom patched successfully")
            from Utils import persistent_store
            persistent_store("adjuster", "last_settings", guiargs)

    adjustButton = Button(bottomFrame2, text='Adjust Rom', command=adjustRom)

    adjustButton.pack(side=LEFT, padx=(5, 0))

    drowDownFrame2.pack(side=LEFT, pady=(0, 40))
    rightHalfFrame2.pack(side=RIGHT)
    topFrame2.pack(side=TOP, pady=70)
    bottomFrame2.pack(side=BOTTOM, pady=(180, 0))

    # Custom Controls

    topFrame3 = Frame(customWindow)

    def validation(P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
    vcmd=(topFrame3.register(validation), '%P')

    itemList1 = Frame(topFrame3)
    itemList2 = Frame(topFrame3)
    itemList3 = Frame(topFrame3)
    itemList4 = Frame(topFrame3)
    itemList5 = Frame(topFrame3)

    bowFrame = Frame(itemList1)
    bowLabel = Label(bowFrame, text='Bow')
    bowVar = StringVar(value='0')
    bowEntry = Entry(bowFrame, textvariable=bowVar, width=3, validate='all', vcmd=vcmd)
    bowFrame.pack()
    bowLabel.pack(anchor=W, side=LEFT, padx=(0,53))
    bowEntry.pack(anchor=E)

    progbowFrame = Frame(itemList1)
    progbowLabel = Label(progbowFrame, text='Prog.Bow')
    progbowVar = StringVar(value='2')
    progbowEntry = Entry(progbowFrame, textvariable=progbowVar, width=3, validate='all', vcmd=vcmd)
    progbowFrame.pack()
    progbowLabel.pack(anchor=W, side=LEFT, padx=(0,25))
    progbowEntry.pack(anchor=E)

    boomerangFrame = Frame(itemList1)
    boomerangLabel = Label(boomerangFrame, text='Boomerang')
    boomerangVar = StringVar(value='1')
    boomerangEntry = Entry(boomerangFrame, textvariable=boomerangVar, width=3, validate='all', vcmd=vcmd)
    boomerangFrame.pack()
    boomerangLabel.pack(anchor=W, side=LEFT, padx=(0,14))
    boomerangEntry.pack(anchor=E)

    magicboomerangFrame = Frame(itemList1)
    magicboomerangLabel = Label(magicboomerangFrame, text='M.Boomerang')
    magicboomerangVar = StringVar(value='1')
    magicboomerangEntry = Entry(magicboomerangFrame, textvariable=magicboomerangVar, width=3, validate='all', vcmd=vcmd)
    magicboomerangFrame.pack()
    magicboomerangLabel.pack(anchor=W, side=LEFT)
    magicboomerangEntry.pack(anchor=E)

    hookshotFrame = Frame(itemList1)
    hookshotLabel = Label(hookshotFrame, text='Hookshot')
    hookshotVar = StringVar(value='1')
    hookshotEntry = Entry(hookshotFrame, textvariable=hookshotVar, width=3, validate='all', vcmd=vcmd)
    hookshotFrame.pack()
    hookshotLabel.pack(anchor=W, side=LEFT, padx=(0,24))
    hookshotEntry.pack(anchor=E)

    mushroomFrame = Frame(itemList1)
    mushroomLabel = Label(mushroomFrame, text='Mushroom')
    mushroomVar = StringVar(value='1')
    mushroomEntry = Entry(mushroomFrame, textvariable=mushroomVar, width=3, validate='all', vcmd=vcmd)
    mushroomFrame.pack()
    mushroomLabel.pack(anchor=W, side=LEFT, padx=(0,17))
    mushroomEntry.pack(anchor=E)

    magicpowderFrame = Frame(itemList1)
    magicpowderLabel = Label(magicpowderFrame, text='Magic Powder')
    magicpowderVar = StringVar(value='1')
    magicpowderEntry = Entry(magicpowderFrame, textvariable=magicpowderVar, width=3, validate='all', vcmd=vcmd)
    magicpowderFrame.pack()
    magicpowderLabel.pack(anchor=W, side=LEFT)
    magicpowderEntry.pack(anchor=E)

    firerodFrame = Frame(itemList1)
    firerodLabel = Label(firerodFrame, text='Fire Rod')
    firerodVar = StringVar(value='1')
    firerodEntry = Entry(firerodFrame, textvariable=firerodVar, width=3, validate='all', vcmd=vcmd)
    firerodFrame.pack()
    firerodLabel.pack(anchor=W, side=LEFT, padx=(0,33))
    firerodEntry.pack(anchor=E)

    icerodFrame = Frame(itemList1)
    icerodLabel = Label(icerodFrame, text='Ice Rod')
    icerodVar = StringVar(value='1')
    icerodEntry = Entry(icerodFrame, textvariable=icerodVar, width=3, validate='all', vcmd=vcmd)
    icerodFrame.pack()
    icerodLabel.pack(anchor=W, side=LEFT, padx=(0,37))
    icerodEntry.pack(anchor=E)

    bombosFrame = Frame(itemList1)
    bombosLabel = Label(bombosFrame, text='Bombos')
    bombosVar = StringVar(value='1')
    bombosEntry = Entry(bombosFrame, textvariable=bombosVar, width=3, validate='all', vcmd=vcmd)
    bombosFrame.pack()
    bombosLabel.pack(anchor=W, side=LEFT, padx=(0,32))
    bombosEntry.pack(anchor=E)

    etherFrame = Frame(itemList1)
    etherLabel = Label(etherFrame, text='Ether')
    etherVar = StringVar(value='1')
    etherEntry = Entry(etherFrame, textvariable=etherVar, width=3, validate='all', vcmd=vcmd)
    etherFrame.pack()
    etherLabel.pack(anchor=W, side=LEFT, padx=(0,49))
    etherEntry.pack(anchor=E)

    quakeFrame = Frame(itemList1)
    quakeLabel = Label(quakeFrame, text='Quake')
    quakeVar = StringVar(value='1')
    quakeEntry = Entry(quakeFrame, textvariable=quakeVar, width=3, validate='all', vcmd=vcmd)
    quakeFrame.pack()
    quakeLabel.pack(anchor=W, side=LEFT, padx=(0,42))
    quakeEntry.pack(anchor=E)

    lampFrame = Frame(itemList1)
    lampLabel = Label(lampFrame, text='Lamp')
    lampVar = StringVar(value='1')
    lampEntry = Entry(lampFrame, textvariable=lampVar, width=3, validate='all', vcmd=vcmd)
    lampFrame.pack()
    lampLabel.pack(anchor=W, side=LEFT, padx=(0,46))
    lampEntry.pack(anchor=E)

    hammerFrame = Frame(itemList1)
    hammerLabel = Label(hammerFrame, text='Hammer')
    hammerVar = StringVar(value='1')
    hammerEntry = Entry(hammerFrame, textvariable=hammerVar, width=3, validate='all', vcmd=vcmd)
    hammerFrame.pack()
    hammerLabel.pack(anchor=W, side=LEFT, padx=(0,29))
    hammerEntry.pack(anchor=E)

    shovelFrame = Frame(itemList1)
    shovelLabel = Label(shovelFrame, text='Shovel')
    shovelVar = StringVar(value='1')
    shovelEntry = Entry(shovelFrame, textvariable=shovelVar, width=3, validate='all', vcmd=vcmd)
    shovelFrame.pack()
    shovelLabel.pack(anchor=W, side=LEFT, padx=(0,41))
    shovelEntry.pack(anchor=E)

    fluteFrame = Frame(itemList1)
    fluteLabel = Label(fluteFrame, text='Flute')
    fluteVar = StringVar(value='1')
    fluteEntry = Entry(fluteFrame, textvariable=fluteVar, width=3, validate='all', vcmd=vcmd)
    fluteFrame.pack()
    fluteLabel.pack(anchor=W, side=LEFT, padx=(0,50))
    fluteEntry.pack(anchor=E)

    bugnetFrame = Frame(itemList2)
    bugnetLabel = Label(bugnetFrame, text='Bug Net')
    bugnetVar = StringVar(value='1')
    bugnetEntry = Entry(bugnetFrame, textvariable=bugnetVar, width=3, validate='all', vcmd=vcmd)
    bugnetFrame.pack()
    bugnetLabel.pack(anchor=W, side=LEFT, padx=(0,41))
    bugnetEntry.pack(anchor=E)

    bookFrame = Frame(itemList2)
    bookLabel = Label(bookFrame, text='Book')
    bookVar = StringVar(value='1')
    bookEntry = Entry(bookFrame, textvariable=bookVar, width=3, validate='all', vcmd=vcmd)
    bookFrame.pack()
    bookLabel.pack(anchor=W, side=LEFT, padx=(0,57))
    bookEntry.pack(anchor=E)

    bottleFrame = Frame(itemList2)
    bottleLabel = Label(bottleFrame, text='Bottle')
    bottleVar = StringVar(value='4')
    bottleEntry = Entry(bottleFrame, textvariable=bottleVar, width=3, validate='all', vcmd=vcmd)
    bottleFrame.pack()
    bottleLabel.pack(anchor=W, side=LEFT, padx=(0,53))
    bottleEntry.pack(anchor=E)

    somariaFrame = Frame(itemList2)
    somariaLabel = Label(somariaFrame, text='C.Somaria')
    somariaVar = StringVar(value='1')
    somariaEntry = Entry(somariaFrame, textvariable=somariaVar, width=3, validate='all', vcmd=vcmd)
    somariaFrame.pack()
    somariaLabel.pack(anchor=W, side=LEFT, padx=(0,30))
    somariaEntry.pack(anchor=E)

    byrnaFrame = Frame(itemList2)
    byrnaLabel = Label(byrnaFrame, text='C.Byrna')
    byrnaVar = StringVar(value='1')
    byrnaEntry = Entry(byrnaFrame, textvariable=byrnaVar, width=3, validate='all', vcmd=vcmd)
    byrnaFrame.pack()
    byrnaLabel.pack(anchor=W, side=LEFT, padx=(0,43))
    byrnaEntry.pack(anchor=E)

    capeFrame = Frame(itemList2)
    capeLabel = Label(capeFrame, text='Magic Cape')
    capeVar = StringVar(value='1')
    capeEntry = Entry(capeFrame, textvariable=capeVar, width=3, validate='all', vcmd=vcmd)
    capeFrame.pack()
    capeLabel.pack(anchor=W, side=LEFT, padx=(0,21))
    capeEntry.pack(anchor=E)

    mirrorFrame = Frame(itemList2)
    mirrorLabel = Label(mirrorFrame, text='Magic Mirror')
    mirrorVar = StringVar(value='1')
    mirrorEntry = Entry(mirrorFrame, textvariable=mirrorVar, width=3, validate='all', vcmd=vcmd)
    mirrorFrame.pack()
    mirrorLabel.pack(anchor=W, side=LEFT, padx=(0,15))
    mirrorEntry.pack(anchor=E)

    bootsFrame = Frame(itemList2)
    bootsLabel = Label(bootsFrame, text='Pegasus Boots')
    bootsVar = StringVar(value='1')
    bootsEntry = Entry(bootsFrame, textvariable=bootsVar, width=3, validate='all', vcmd=vcmd)
    bootsFrame.pack()
    bootsLabel.pack(anchor=W, side=LEFT, padx=(0,8))
    bootsEntry.pack(anchor=E)

    powergloveFrame = Frame(itemList2)
    powergloveLabel = Label(powergloveFrame, text='Power Glove')
    powergloveVar = StringVar(value='0')
    powergloveEntry = Entry(powergloveFrame, textvariable=powergloveVar, width=3, validate='all', vcmd=vcmd)
    powergloveFrame.pack()
    powergloveLabel.pack(anchor=W, side=LEFT, padx=(0,18))
    powergloveEntry.pack(anchor=E)

    titansmittFrame = Frame(itemList2)
    titansmittLabel = Label(titansmittFrame, text='Titan\'s Mitt')
    titansmittVar = StringVar(value='0')
    titansmittEntry = Entry(titansmittFrame, textvariable=titansmittVar, width=3, validate='all', vcmd=vcmd)
    titansmittFrame.pack()
    titansmittLabel.pack(anchor=W, side=LEFT, padx=(0,24))
    titansmittEntry.pack(anchor=E)

    proggloveFrame = Frame(itemList2)
    proggloveLabel = Label(proggloveFrame, text='Prog.Glove')
    proggloveVar = StringVar(value='2')
    proggloveEntry = Entry(proggloveFrame, textvariable=proggloveVar, width=3, validate='all', vcmd=vcmd)
    proggloveFrame.pack()
    proggloveLabel.pack(anchor=W, side=LEFT, padx=(0,26))
    proggloveEntry.pack(anchor=E)

    flippersFrame = Frame(itemList2)
    flippersLabel = Label(flippersFrame, text='Flippers')
    flippersVar = StringVar(value='1')
    flippersEntry = Entry(flippersFrame, textvariable=flippersVar, width=3, validate='all', vcmd=vcmd)
    flippersFrame.pack()
    flippersLabel.pack(anchor=W, side=LEFT, padx=(0,43))
    flippersEntry.pack(anchor=E)

    pearlFrame = Frame(itemList2)
    pearlLabel = Label(pearlFrame, text='Moon Pearl')
    pearlVar = StringVar(value='1')
    pearlEntry = Entry(pearlFrame, textvariable=pearlVar, width=3, validate='all', vcmd=vcmd)
    pearlFrame.pack()
    pearlLabel.pack(anchor=W, side=LEFT, padx=(0,23))
    pearlEntry.pack(anchor=E)

    heartpieceFrame = Frame(itemList2)
    heartpieceLabel = Label(heartpieceFrame, text='Piece of Heart')
    heartpieceVar = StringVar(value='24')
    heartpieceEntry = Entry(heartpieceFrame, textvariable=heartpieceVar, width=3, validate='all', vcmd=vcmd)
    heartpieceFrame.pack()
    heartpieceLabel.pack(anchor=W, side=LEFT, padx=(0,10))
    heartpieceEntry.pack(anchor=E)

    fullheartFrame = Frame(itemList2)
    fullheartLabel = Label(fullheartFrame, text='Heart Container')
    fullheartVar = StringVar(value='10')
    fullheartEntry = Entry(fullheartFrame, textvariable=fullheartVar, width=3, validate='all', vcmd=vcmd)
    fullheartFrame.pack()
    fullheartLabel.pack(anchor=W, side=LEFT)
    fullheartEntry.pack(anchor=E)

    sancheartFrame = Frame(itemList2)
    sancheartLabel = Label(sancheartFrame, text='Sanctuary Heart')
    sancheartVar = StringVar(value='1')
    sancheartEntry = Entry(sancheartFrame, textvariable=sancheartVar, width=3, validate='all', vcmd=vcmd)
    sancheartFrame.pack()
    sancheartLabel.pack(anchor=W, side=LEFT)
    sancheartEntry.pack(anchor=E)

    sword1Frame = Frame(itemList3)
    sword1Label = Label(sword1Frame, text='Sword 1')
    sword1Var = StringVar(value='0')
    sword1Entry = Entry(sword1Frame, textvariable=sword1Var, width=3, validate='all', vcmd=vcmd)
    sword1Frame.pack()
    sword1Label.pack(anchor=W, side=LEFT, padx=(0,34))
    sword1Entry.pack(anchor=E)

    sword2Frame = Frame(itemList3)
    sword2Label = Label(sword2Frame, text='Sword 2')
    sword2Var = StringVar(value='0')
    sword2Entry = Entry(sword2Frame, textvariable=sword2Var, width=3, validate='all', vcmd=vcmd)
    sword2Frame.pack()
    sword2Label.pack(anchor=W, side=LEFT, padx=(0,34))
    sword2Entry.pack(anchor=E)

    sword3Frame = Frame(itemList3)
    sword3Label = Label(sword3Frame, text='Sword 3')
    sword3Var = StringVar(value='0')
    sword3Entry = Entry(sword3Frame, textvariable=sword3Var, width=3, validate='all', vcmd=vcmd)
    sword3Frame.pack()
    sword3Label.pack(anchor=W, side=LEFT, padx=(0,34))
    sword3Entry.pack(anchor=E)

    sword4Frame = Frame(itemList3)
    sword4Label = Label(sword4Frame, text='Sword 4')
    sword4Var = StringVar(value='0')
    sword4Entry = Entry(sword4Frame, textvariable=sword4Var, width=3, validate='all', vcmd=vcmd)
    sword4Frame.pack()
    sword4Label.pack(anchor=W, side=LEFT, padx=(0,34))
    sword4Entry.pack(anchor=E)

    progswordFrame = Frame(itemList3)
    progswordLabel = Label(progswordFrame, text='Prog.Sword')
    progswordVar = StringVar(value='4')
    progswordEntry = Entry(progswordFrame, textvariable=progswordVar, width=3, validate='all', vcmd=vcmd)
    progswordFrame.pack()
    progswordLabel.pack(anchor=W, side=LEFT, padx=(0,15))
    progswordEntry.pack(anchor=E)

    shield1Frame = Frame(itemList3)
    shield1Label = Label(shield1Frame, text='Shield 1')
    shield1Var = StringVar(value='0')
    shield1Entry = Entry(shield1Frame, textvariable=shield1Var, width=3, validate='all', vcmd=vcmd)
    shield1Frame.pack()
    shield1Label.pack(anchor=W, side=LEFT, padx=(0,35))
    shield1Entry.pack(anchor=E)

    shield2Frame = Frame(itemList3)
    shield2Label = Label(shield2Frame, text='Shield 2')
    shield2Var = StringVar(value='0')
    shield2Entry = Entry(shield2Frame, textvariable=shield2Var, width=3, validate='all', vcmd=vcmd)
    shield2Frame.pack()
    shield2Label.pack(anchor=W, side=LEFT, padx=(0,35))
    shield2Entry.pack(anchor=E)

    shield3Frame = Frame(itemList3)
    shield3Label = Label(shield3Frame, text='Shield 3')
    shield3Var = StringVar(value='0')
    shield3Entry = Entry(shield3Frame, textvariable=shield3Var, width=3, validate='all', vcmd=vcmd)
    shield3Frame.pack()
    shield3Label.pack(anchor=W, side=LEFT, padx=(0,35))
    shield3Entry.pack(anchor=E)

    progshieldFrame = Frame(itemList3)
    progshieldLabel = Label(progshieldFrame, text='Prog.Shield')
    progshieldVar = StringVar(value='3')
    progshieldEntry = Entry(progshieldFrame, textvariable=progshieldVar, width=3, validate='all', vcmd=vcmd)
    progshieldFrame.pack()
    progshieldLabel.pack(anchor=W, side=LEFT, padx=(0,16))
    progshieldEntry.pack(anchor=E)

    bluemailFrame = Frame(itemList3)
    bluemailLabel = Label(bluemailFrame, text='Blue Mail')
    bluemailVar = StringVar(value='0')
    bluemailEntry = Entry(bluemailFrame, textvariable=bluemailVar, width=3, validate='all', vcmd=vcmd)
    bluemailFrame.pack()
    bluemailLabel.pack(anchor=W, side=LEFT, padx=(0,27))
    bluemailEntry.pack(anchor=E)

    redmailFrame = Frame(itemList3)
    redmailLabel = Label(redmailFrame, text='Red Mail')
    redmailVar = StringVar(value='0')
    redmailEntry = Entry(redmailFrame, textvariable=redmailVar, width=3, validate='all', vcmd=vcmd)
    redmailFrame.pack()
    redmailLabel.pack(anchor=W, side=LEFT, padx=(0,30))
    redmailEntry.pack(anchor=E)

    progmailFrame = Frame(itemList3)
    progmailLabel = Label(progmailFrame, text='Prog.Mail')
    progmailVar = StringVar(value='2')
    progmailEntry = Entry(progmailFrame, textvariable=progmailVar, width=3, validate='all', vcmd=vcmd)
    progmailFrame.pack()
    progmailLabel.pack(anchor=W, side=LEFT, padx=(0,25))
    progmailEntry.pack(anchor=E)

    halfmagicFrame = Frame(itemList3)
    halfmagicLabel = Label(halfmagicFrame, text='Half Magic')
    halfmagicVar = StringVar(value='1')
    halfmagicEntry = Entry(halfmagicFrame, textvariable=halfmagicVar, width=3, validate='all', vcmd=vcmd)
    halfmagicFrame.pack()
    halfmagicLabel.pack(anchor=W, side=LEFT, padx=(0,18))
    halfmagicEntry.pack(anchor=E)

    quartermagicFrame = Frame(itemList3)
    quartermagicLabel = Label(quartermagicFrame, text='Quarter Magic')
    quartermagicVar = StringVar(value='0')
    quartermagicEntry = Entry(quartermagicFrame, textvariable=quartermagicVar, width=3, validate='all', vcmd=vcmd)
    quartermagicFrame.pack()
    quartermagicLabel.pack(anchor=W, side=LEFT)
    quartermagicEntry.pack(anchor=E)

    bcap5Frame = Frame(itemList3)
    bcap5Label = Label(bcap5Frame, text='Bomb C.+5')
    bcap5Var = StringVar(value='0')
    bcap5Entry = Entry(bcap5Frame, textvariable=bcap5Var, width=3, validate='all', vcmd=vcmd)
    bcap5Frame.pack()
    bcap5Label.pack(anchor=W, side=LEFT, padx=(0,16))
    bcap5Entry.pack(anchor=E)

    bcap10Frame = Frame(itemList3)
    bcap10Label = Label(bcap10Frame, text='Bomb C.+10')
    bcap10Var = StringVar(value='0')
    bcap10Entry = Entry(bcap10Frame, textvariable=bcap10Var, width=3, validate='all', vcmd=vcmd)
    bcap10Frame.pack()
    bcap10Label.pack(anchor=W, side=LEFT, padx=(0,10))
    bcap10Entry.pack(anchor=E)

    acap5Frame = Frame(itemList4)
    acap5Label = Label(acap5Frame, text='Arrow C.+5')
    acap5Var = StringVar(value='0')
    acap5Entry = Entry(acap5Frame, textvariable=acap5Var, width=3, validate='all', vcmd=vcmd)
    acap5Frame.pack()
    acap5Label.pack(anchor=W, side=LEFT, padx=(0,7))
    acap5Entry.pack(anchor=E)

    acap10Frame = Frame(itemList4)
    acap10Label = Label(acap10Frame, text='Arrow C.+10')
    acap10Var = StringVar(value='0')
    acap10Entry = Entry(acap10Frame, textvariable=acap10Var, width=3, validate='all', vcmd=vcmd)
    acap10Frame.pack()
    acap10Label.pack(anchor=W, side=LEFT, padx=(0,1))
    acap10Entry.pack(anchor=E)

    arrow1Frame = Frame(itemList4)
    arrow1Label = Label(arrow1Frame, text='Arrow (1)')
    arrow1Var = StringVar(value='1')
    arrow1Entry = Entry(arrow1Frame, textvariable=arrow1Var, width=3, validate='all', vcmd=vcmd)
    arrow1Frame.pack()
    arrow1Label.pack(anchor=W, side=LEFT, padx=(0,18))
    arrow1Entry.pack(anchor=E)

    arrow10Frame = Frame(itemList4)
    arrow10Label = Label(arrow10Frame, text='Arrows (10)')
    arrow10Var = StringVar(value='12')
    arrow10Entry = Entry(arrow10Frame, textvariable=arrow10Var, width=3, validate='all', vcmd=vcmd)
    arrow10Frame.pack()
    arrow10Label.pack(anchor=W, side=LEFT, padx=(0,7))
    arrow10Entry.pack(anchor=E)

    bomb1Frame = Frame(itemList4)
    bomb1Label = Label(bomb1Frame, text='Bomb (1)')
    bomb1Var = StringVar(value='0')
    bomb1Entry = Entry(bomb1Frame, textvariable=bomb1Var, width=3, validate='all', vcmd=vcmd)
    bomb1Frame.pack()
    bomb1Label.pack(anchor=W, side=LEFT, padx=(0,18))
    bomb1Entry.pack(anchor=E)

    bomb3Frame = Frame(itemList4)
    bomb3Label = Label(bomb3Frame, text='Bombs (3)')
    bomb3Var = StringVar(value='16')
    bomb3Entry = Entry(bomb3Frame, textvariable=bomb3Var, width=3, validate='all', vcmd=vcmd)
    bomb3Frame.pack()
    bomb3Label.pack(anchor=W, side=LEFT, padx=(0,13))
    bomb3Entry.pack(anchor=E)

    bomb10Frame = Frame(itemList4)
    bomb10Label = Label(bomb10Frame, text='Bombs (10)')
    bomb10Var = StringVar(value='1')
    bomb10Entry = Entry(bomb10Frame, textvariable=bomb10Var, width=3, validate='all', vcmd=vcmd)
    bomb10Frame.pack()
    bomb10Label.pack(anchor=W, side=LEFT, padx=(0,7))
    bomb10Entry.pack(anchor=E)

    rupee1Frame = Frame(itemList4)
    rupee1Label = Label(rupee1Frame, text='Rupee (1)')
    rupee1Var = StringVar(value='2')
    rupee1Entry = Entry(rupee1Frame, textvariable=rupee1Var, width=3, validate='all', vcmd=vcmd)
    rupee1Frame.pack()
    rupee1Label.pack(anchor=W, side=LEFT, padx=(0,17))
    rupee1Entry.pack(anchor=E)

    rupee5Frame = Frame(itemList4)
    rupee5Label = Label(rupee5Frame, text='Rupees (5)')
    rupee5Var = StringVar(value='4')
    rupee5Entry = Entry(rupee5Frame, textvariable=rupee5Var, width=3, validate='all', vcmd=vcmd)
    rupee5Frame.pack()
    rupee5Label.pack(anchor=W, side=LEFT, padx=(0,12))
    rupee5Entry.pack(anchor=E)

    rupee20Frame = Frame(itemList4)
    rupee20Label = Label(rupee20Frame, text='Rupees (20)')
    rupee20Var = StringVar(value='28')
    rupee20Entry = Entry(rupee20Frame, textvariable=rupee20Var, width=3, validate='all', vcmd=vcmd)
    rupee20Frame.pack()
    rupee20Label.pack(anchor=W, side=LEFT, padx=(0,6))
    rupee20Entry.pack(anchor=E)

    rupee50Frame = Frame(itemList4)
    rupee50Label = Label(rupee50Frame, text='Rupees (50)')
    rupee50Var = StringVar(value='7')
    rupee50Entry = Entry(rupee50Frame, textvariable=rupee50Var, width=3, validate='all', vcmd=vcmd)
    rupee50Frame.pack()
    rupee50Label.pack(anchor=W, side=LEFT, padx=(0,6))
    rupee50Entry.pack(anchor=E)

    rupee100Frame = Frame(itemList4)
    rupee100Label = Label(rupee100Frame, text='Rupees (100)')
    rupee100Var = StringVar(value='1')
    rupee100Entry = Entry(rupee100Frame, textvariable=rupee100Var, width=3, validate='all', vcmd=vcmd)
    rupee100Frame.pack()
    rupee100Label.pack(anchor=W, side=LEFT, padx=(0,0))
    rupee100Entry.pack(anchor=E)

    rupee300Frame = Frame(itemList4)
    rupee300Label = Label(rupee300Frame, text='Rupees (300)')
    rupee300Var = StringVar(value='5')
    rupee300Entry = Entry(rupee300Frame, textvariable=rupee300Var, width=3, validate='all', vcmd=vcmd)
    rupee300Frame.pack()
    rupee300Label.pack(anchor=W, side=LEFT, padx=(0,0))
    rupee300Entry.pack(anchor=E)

    blueclockFrame = Frame(itemList4)
    blueclockLabel = Label(blueclockFrame, text='Blue Clock')
    blueclockVar = StringVar(value='0')
    blueclockEntry = Entry(blueclockFrame, textvariable=blueclockVar, width=3, validate='all', vcmd=vcmd)
    blueclockFrame.pack()
    blueclockLabel.pack(anchor=W, side=LEFT, padx=(0,11))
    blueclockEntry.pack(anchor=E)

    greenclockFrame = Frame(itemList4)
    greenclockLabel = Label(greenclockFrame, text='Green Clock')
    greenclockVar = StringVar(value='0')
    greenclockEntry = Entry(greenclockFrame, textvariable=greenclockVar, width=3, validate='all', vcmd=vcmd)
    greenclockFrame.pack()
    greenclockLabel.pack(anchor=W, side=LEFT, padx=(0,3))
    greenclockEntry.pack(anchor=E)

    redclockFrame = Frame(itemList4)
    redclockLabel = Label(redclockFrame, text='Red Clock')
    redclockVar = StringVar(value='0')
    redclockEntry = Entry(redclockFrame, textvariable=redclockVar, width=3, validate='all', vcmd=vcmd)
    redclockFrame.pack()
    redclockLabel.pack(anchor=W, side=LEFT, padx=(0,14))
    redclockEntry.pack(anchor=E)

    silverarrowFrame = Frame(itemList5)
    silverarrowLabel = Label(silverarrowFrame, text='Silver Arrow')
    silverarrowVar = StringVar(value='0')
    silverarrowEntry = Entry(silverarrowFrame, textvariable=silverarrowVar, width=3, validate='all', vcmd=vcmd)
    silverarrowFrame.pack()
    silverarrowLabel.pack(anchor=W, side=LEFT, padx=(0,64))
    silverarrowEntry.pack(anchor=E)

    universalkeyFrame = Frame(itemList5)
    universalkeyLabel = Label(universalkeyFrame, text='Universal Key')
    universalkeyVar = StringVar(value='0')
    universalkeyEntry = Entry(universalkeyFrame, textvariable=universalkeyVar, width=3, validate='all', vcmd=vcmd)
    universalkeyFrame.pack()
    universalkeyLabel.pack(anchor=W, side=LEFT, padx=(0,57))
    universalkeyEntry.pack(anchor=E)

    triforcepieceFrame = Frame(itemList5)
    triforcepieceLabel = Label(triforcepieceFrame, text='Triforce Piece')
    triforcepieceVar = StringVar(value='0')
    triforcepieceEntry = Entry(triforcepieceFrame, textvariable=triforcepieceVar, width=3, validate='all', vcmd=vcmd)
    triforcepieceFrame.pack()
    triforcepieceLabel.pack(anchor=W, side=LEFT, padx=(0,55))
    triforcepieceEntry.pack(anchor=E)

    triforcecountFrame = Frame(itemList5)
    triforcecountLabel = Label(triforcecountFrame, text='Triforce Pieces Required')
    triforcecountVar = StringVar(value='0')
    triforcecountEntry = Entry(triforcecountFrame, textvariable=triforcecountVar, width=3, validate='all', vcmd=vcmd)
    triforcecountFrame.pack()
    triforcecountLabel.pack(anchor=W, side=LEFT, padx=(0,0))
    triforcecountEntry.pack(anchor=E)

    triforceFrame = Frame(itemList5)
    triforceLabel = Label(triforceFrame, text='Triforce (win game)')
    triforceVar = StringVar(value='0')
    triforceEntry = Entry(triforceFrame, textvariable=triforceVar, width=3, validate='all', vcmd=vcmd)
    triforceFrame.pack()
    triforceLabel.pack(anchor=W, side=LEFT, padx=(0,23))
    triforceEntry.pack(anchor=E)

    rupoorFrame = Frame(itemList5)
    rupoorLabel = Label(rupoorFrame, text='Rupoor')
    rupoorVar = StringVar(value='0')
    rupoorEntry = Entry(rupoorFrame, textvariable=rupoorVar, width=3, validate='all', vcmd=vcmd)
    rupoorFrame.pack()
    rupoorLabel.pack(anchor=W, side=LEFT, padx=(0,87))
    rupoorEntry.pack(anchor=E)

    rupoorcostFrame = Frame(itemList5)
    rupoorcostLabel = Label(rupoorcostFrame, text='Rupoor Cost')
    rupoorcostVar = StringVar(value='10')
    rupoorcostEntry = Entry(rupoorcostFrame, textvariable=rupoorcostVar, width=6, validate='all', vcmd=vcmd)
    rupoorcostFrame.pack()
    rupoorcostLabel.pack(anchor=W, side=LEFT, padx=(0,43))
    rupoorcostEntry.pack(anchor=E)

    itemList1.pack(side=LEFT, padx=(0,0))
    itemList2.pack(side=LEFT, padx=(0,0))
    itemList3.pack(side=LEFT, padx=(0,0))
    itemList4.pack(side=LEFT, padx=(0,0))
    itemList5.pack(side=LEFT, padx=(0,0))
    topFrame3.pack(side=TOP, pady=(17,0))

    if args is not None:
        for k,v in vars(args).items():
            if type(v) is dict:
                setattr(args, k, v[1]) # only get values for player 1 for now
        # load values from commandline args
        createSpoilerVar.set(int(args.create_spoiler))
        suppressRomVar.set(int(args.suppress_rom))
        mapshuffleVar.set(args.mapshuffle)
        compassshuffleVar.set(args.compassshuffle)
        keyshuffleVar.set(args.keyshuffle)
        bigkeyshuffleVar.set(args.bigkeyshuffle)
        retroVar.set(args.retro)
        quickSwapVar.set(int(args.quickswap))
        disableMusicVar.set(int(args.disablemusic))
        if args.count:
            countVar.set(str(args.count))
        if args.seed:
            seedVar.set(str(args.seed))
        modeVar.set(args.mode)
        swordVar.set(args.swords)
        difficultyVar.set(args.difficulty)
        itemfunctionVar.set(args.item_functionality)
        timerVar.set(args.timer)
        progressiveVar.set(args.progressive)
        accessibilityVar.set(args.accessibility)
        goalVar.set(args.goal)
        crystalsGTVar.set(args.crystals_gt)
        crystalsGanonVar.set(args.crystals_ganon)
        algorithmVar.set(args.algorithm)
        shuffleVar.set(args.shuffle)
        heartbeepVar.set(args.heartbeep)
        fastMenuVar.set(args.fastmenu)
        logicVar.set(args.logic)
        romVar.set(args.rom)
        shuffleGanonVar.set(args.shuffleganon)
        hintsVar.set(args.hints)
        if args.sprite is not None:
            set_sprite(Sprite(args.sprite))

    mainWindow.mainloop()

class SpriteSelector(object):
    def __init__(self, parent, callback, adjuster=False):
        if is_bundled():
            self.deploy_icons()
        self.parent = parent
        self.window = Toplevel(parent)
        self.callback = callback
        self.adjuster = adjuster

        self.window.wm_title("TAKE ANY ONE YOU WANT")
        self.window['padx'] = 5
        self.window['pady'] = 5
        self.all_sprites = []

        def open_unofficial_sprite_dir(_evt):
            open_file(self.unofficial_sprite_dir)

        official_frametitle = Label(self.window, text='Official Sprites')

        unofficial_frametitle = Frame(self.window)
        title_text = Label(unofficial_frametitle, text="Unofficial Sprites")
        title_link = Label(unofficial_frametitle, text="(open)", fg="blue", cursor="hand2")
        title_text.pack(side=LEFT)
        title_link.pack(side=LEFT)
        title_link.bind("<Button-1>", open_unofficial_sprite_dir)

        self.icon_section(official_frametitle, self.official_sprite_dir+'/*', 'Official sprites not found. Click "Update official sprites" to download them.')
        self.icon_section(unofficial_frametitle, self.unofficial_sprite_dir+'/*', 'Put sprites in the unofficial sprites folder (see open link above) to have them appear here.')

        frame = Frame(self.window)
        frame.pack(side=BOTTOM, fill=X, pady=5)

        button = Button(frame, text="Browse for file...", command=self.browse_for_sprite)
        button.pack(side=RIGHT, padx=(5, 0))

        button = Button(frame, text="Update official sprites", command=self.update_official_sprites)
        button.pack(side=RIGHT, padx=(5, 0))

        button = Button(frame, text="Default Link sprite", command=self.use_default_link_sprite)
        button.pack(side=LEFT, padx=(0, 5))

        button = Button(frame, text="Random sprite", command=self.use_random_sprite)
        button.pack(side=LEFT, padx=(0, 5))

        if adjuster:
            button = Button(frame, text="Current sprite from rom", command=self.use_default_sprite)
            button.pack(side=LEFT, padx=(0, 5))

        set_icon(self.window)
        self.window.focus()

    def icon_section(self, frame_label, path, no_results_label):
        frame = LabelFrame(self.window, labelwidget=frame_label, padx=5, pady=5)
        frame.pack(side=TOP, fill=X)

        sprites = []

        for file in glob(output_path(path)):
            sprites.append(Sprite(file))

        sprites.sort(key=lambda s: str.lower(s.name or "").strip())

        i = 0
        for sprite in sprites:
            image = get_image_for_sprite(sprite)
            if image is None:
                continue
            self.all_sprites.append(sprite)
            button = Button(frame, image=image, command=lambda spr=sprite: self.select_sprite(spr))
            ToolTips.register(button, sprite.name + ("\nBy: %s" % sprite.author_name if sprite.author_name else ""))
            button.image = image
            button.grid(row=i // 16, column=i % 16)
            i += 1

        if i == 0:
            label = Label(frame, text=no_results_label)
            label.pack()


    def update_official_sprites(self):
        # need to wrap in try catch. We don't want errors getting the json or downloading the files to break us.
        self.window.destroy()
        self.parent.update()
        def work(task):
            resultmessage = ""
            successful = True

            def finished():
                task.close_window()
                if successful:
                    messagebox.showinfo("Sprite Updater", resultmessage)
                else:
                    messagebox.showerror("Sprite Updater", resultmessage)
                SpriteSelector(self.parent, self.callback, self.adjuster)

            try:
                task.update_status("Downloading official sprites list")
                with urlopen('https://alttpr.com/sprites') as response:
                    sprites_arr = json.loads(response.read().decode("utf-8"))
            except Exception as e:
                resultmessage = "Error getting list of official sprites. Sprites not updated.\n\n%s: %s" % (type(e).__name__, e)
                successful = False
                task.queue_event(finished)
                return

            try:
                task.update_status("Determining needed sprites")
                current_sprites = [os.path.basename(file) for file in glob(self.official_sprite_dir+'/*')]
                official_sprites = [(sprite['file'], os.path.basename(urlparse(sprite['file']).path)) for sprite in sprites_arr]
                needed_sprites = [(sprite_url, filename) for (sprite_url, filename) in official_sprites if filename not in current_sprites]
                bundled_sprites = [os.path.basename(file) for file in glob(self.local_official_sprite_dir+'/*')]
                # todo: eventually use the above list to avoid downloading any sprites that we already have cached in the bundle.

                official_filenames = [filename for (_, filename) in official_sprites]
                obsolete_sprites = [sprite for sprite in current_sprites if sprite not in official_filenames]
            except Exception as e:
                resultmessage = "Error Determining which sprites to update. Sprites not updated.\n\n%s: %s" % (type(e).__name__, e)
                successful = False
                task.queue_event(finished)
                return

            updated = 0
            for (sprite_url, filename) in needed_sprites:
                try:
                    task.update_status("Downloading needed sprite %g/%g" % (updated + 1, len(needed_sprites)))
                    target = os.path.join(self.official_sprite_dir, filename)
                    with urlopen(sprite_url) as response, open(target, 'wb') as out:
                        shutil.copyfileobj(response, out)
                except Exception as e:
                    resultmessage = "Error downloading sprite. Not all sprites updated.\n\n%s: %s" % (type(e).__name__, e)
                    successful = False
                updated += 1

            deleted = 0
            for sprite in obsolete_sprites:
                try:
                    task.update_status("Removing obsolete sprite %g/%g" % (deleted + 1, len(obsolete_sprites)))
                    os.remove(os.path.join(self.official_sprite_dir, sprite))
                except Exception as e:
                    resultmessage = "Error removing obsolete sprite. Not all sprites updated.\n\n%s: %s" % (type(e).__name__, e)
                    successful = False
                deleted += 1

            if successful:
                resultmessage = "official sprites updated successfully"

            task.queue_event(finished)

        BackgroundTaskProgress(self.parent, work, "Updating Sprites")


    def browse_for_sprite(self):
        sprite = filedialog.askopenfilename(
            filetypes=[("All Sprite Sources", (".zspr", ".spr", ".sfc", ".smc")),
                       ("ZSprite files", ".zspr"),
                       ("Sprite files", ".spr"),
                       ("Rom Files", (".sfc", ".smc")),
                       ("All Files", "*")])
        try:
            self.callback(Sprite(sprite))
        except Exception:
            self.callback(None)
        self.window.destroy()


    def use_default_sprite(self):
        self.callback(None)
        self.window.destroy()

    def use_default_link_sprite(self):
        self.callback(Sprite.default_link_sprite())
        self.window.destroy()

    def use_random_sprite(self):
        self.callback(random.choice(self.all_sprites) if self.all_sprites else None)
        self.window.destroy()

    def select_sprite(self, spritename):
        self.callback(spritename)
        self.window.destroy()


    def deploy_icons(self):
        if not os.path.exists(self.unofficial_sprite_dir):
            os.makedirs(self.unofficial_sprite_dir)
        if not os.path.exists(self.official_sprite_dir):
            shutil.copytree(self.local_official_sprite_dir, self.official_sprite_dir)

    @property
    def official_sprite_dir(self):
        if is_bundled():
            return output_path("sprites/official")
        return self.local_official_sprite_dir

    @property
    def local_official_sprite_dir(self):
        return local_path("data/sprites/official")

    @property
    def unofficial_sprite_dir(self):
        if is_bundled():
            return output_path("sprites/unofficial")
        return self.local_unofficial_sprite_dir

    @property
    def local_unofficial_sprite_dir(self):
        return local_path("data/sprites/unofficial")


def get_image_for_sprite(sprite):
    if not sprite.valid:
        return None
    height = 24
    width = 16

    def draw_sprite_into_gif(add_palette_color, set_pixel_color_index):

        def drawsprite(spr, pal_as_colors, offset):
            for y, row in enumerate(spr):
                for x, pal_index in enumerate(row):
                    if pal_index:
                        color = pal_as_colors[pal_index - 1]
                        set_pixel_color_index(x + offset[0], y + offset[1], color)

        add_palette_color(16, (40, 40, 40))
        shadow = [
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        ]

        drawsprite(shadow, [16], (2, 17))

        palettes = sprite.decode_palette()
        for i in range(15):
            add_palette_color(i + 1, palettes[0][i])

        body = sprite.decode16(0x4C0)
        drawsprite(body, list(range(1, 16)), (0, 8))
        head = sprite.decode16(0x40)
        drawsprite(head, list(range(1, 16)), (0, 0))

    def make_gif(callback):
        gif_header = b'GIF89a'

        gif_lsd = bytearray(7)
        gif_lsd[0] = width
        gif_lsd[2] = height
        gif_lsd[4] = 0xF4  # 32 color palette follows.  transparant + 15 for sprite + 1 for shadow=17 which rounds up to 32 as nearest power of 2
        gif_lsd[5] = 0  # background color is zero
        gif_lsd[6] = 0  # aspect raio not specified
        gif_gct = bytearray(3 * 32)

        gif_gce = bytearray(8)
        gif_gce[0] = 0x21  # start of extention blocked
        gif_gce[1] = 0xF9  # identifies this as the Graphics Control extension
        gif_gce[2] = 4  # we are suppling only the 4 four bytes
        gif_gce[3] = 0x01  # this gif includes transparency
        gif_gce[4] = gif_gce[5] = 0  # animation frrame delay (unused)
        gif_gce[6] = 0  # transparent color is index 0
        gif_gce[7] = 0  # end of gif_gce
        gif_id = bytearray(10)
        gif_id[0] = 0x2c
        # byte 1,2 are image left. 3,4 are image top both are left as zerosuitsamus
        gif_id[5] = width
        gif_id[7] = height
        gif_id[9] = 0  # no local color table

        gif_img_minimum_code_size = bytes([7])  # we choose 7 bits, so that each pixel is represented by a byte, for conviennce.

        clear = 0x80
        stop = 0x81

        unchunked_image_data = bytearray(height * (width + 1) + 1)
        # we technically need a Clear code once every 125 bytes, but we do it at the start of every row for simplicity
        for row in range(height):
            unchunked_image_data[row * (width + 1)] = clear
        unchunked_image_data[-1] = stop

        def add_palette_color(index, color):
            gif_gct[3 * index] = color[0]
            gif_gct[3 * index + 1] = color[1]
            gif_gct[3 * index + 2] = color[2]

        def set_pixel_color_index(x, y, color):
            unchunked_image_data[y * (width + 1) + x + 1] = color

        callback(add_palette_color, set_pixel_color_index)

        def chunk_image(img):
            for i in range(0, len(img), 255):
                chunk = img[i:i + 255]
                yield bytes([len(chunk)])
                yield chunk

        gif_img = b''.join([gif_img_minimum_code_size] + list(chunk_image(unchunked_image_data)) + [b'\x00'])

        gif = b''.join([gif_header, gif_lsd, gif_gct, gif_gce, gif_id, gif_img, b'\x3b'])

        return gif

    gif_data = make_gif(draw_sprite_into_gif)
    image = PhotoImage(data=gif_data)

    return image.zoom(2)

if __name__ == '__main__':
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    guiMain()
