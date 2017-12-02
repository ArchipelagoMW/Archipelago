from Main import main, __version__ as ESVersion
from Utils import is_bundled, local_path, output_path, open_file
from argparse import Namespace
import random
import subprocess
import os
import sys
from tkinter import Checkbutton, OptionMenu, Tk, LEFT, RIGHT, BOTTOM, TOP, StringVar, IntVar, Frame, Label, W, E, X, Entry, Spinbox, Button, filedialog, messagebox, PhotoImage


def guiMain(args=None):
    mainWindow = Tk()
    mainWindow.wm_title("Entrance Shuffle %s" % ESVersion)

    set_icon(mainWindow)

    topFrame = Frame(mainWindow)
    rightHalfFrame = Frame(topFrame)
    checkBoxFrame = Frame(rightHalfFrame)

    createSpoilerVar = IntVar()
    createSpoilerCheckbutton = Checkbutton(checkBoxFrame, text="Create Spoiler Log", variable=createSpoilerVar)
    suppressRomVar = IntVar()
    suppressRomCheckbutton = Checkbutton(checkBoxFrame, text="Do not create patched Rom", variable=suppressRomVar)
    quickSwapVar = IntVar()
    quickSwapCheckbutton = Checkbutton(checkBoxFrame, text="Enabled L/R Item quickswapping", variable=quickSwapVar)
    fastMenuVar = IntVar()
    fastMenuCheckbutton = Checkbutton(checkBoxFrame, text="Enable instant menu", variable=fastMenuVar)
    keysanityVar = IntVar()
    keysanityCheckbutton = Checkbutton(checkBoxFrame, text="Keysanity (keys anywhere)", variable=keysanityVar)
    dungeonItemsVar = IntVar()
    dungeonItemsCheckbutton = Checkbutton(checkBoxFrame, text="Place Dungeon Items (Compasses/Maps)", onvalue=0, offvalue=1, variable=dungeonItemsVar)
    beatableOnlyVar = IntVar()
    beatableOnlyCheckbutton = Checkbutton(checkBoxFrame, text="Only ensure seed is beatable, not all items must be reachable", variable=beatableOnlyVar)
    disableMusicVar = IntVar()
    disableMusicCheckbutton = Checkbutton(checkBoxFrame, text="Disable game music", variable=disableMusicVar)
    shuffleGanonVar = IntVar()
    shuffleGanonCheckbutton = Checkbutton(checkBoxFrame, text="Include Ganon's Tower and Pyramid Hole in shuffle pool", variable=shuffleGanonVar)

    createSpoilerCheckbutton.pack(expand=True, anchor=W)
    suppressRomCheckbutton.pack(expand=True, anchor=W)
    quickSwapCheckbutton.pack(expand=True, anchor=W)
    fastMenuCheckbutton.pack(expand=True, anchor=W)
    keysanityCheckbutton.pack(expand=True, anchor=W)
    dungeonItemsCheckbutton.pack(expand=True, anchor=W)
    beatableOnlyCheckbutton.pack(expand=True, anchor=W)
    disableMusicCheckbutton.pack(expand=True, anchor=W)
    shuffleGanonCheckbutton.pack(expand=True, anchor=W)

    fileDialogFrame = Frame(rightHalfFrame)

    romDialogFrame = Frame(fileDialogFrame)
    baseRomLabel = Label(romDialogFrame, text='Base Rom')
    romVar = StringVar()
    romEntry = Entry(romDialogFrame, textvariable=romVar)

    def RomSelect():
        rom = filedialog.askopenfilename()
        romVar.set(rom)
    romSelectButton = Button(romDialogFrame, text='Select Rom', command=RomSelect)

    baseRomLabel.pack(side=LEFT)
    romEntry.pack(side=LEFT)
    romSelectButton.pack(side=LEFT)

    spriteDialogFrame = Frame(fileDialogFrame)
    baseSpriteLabel = Label(spriteDialogFrame, text='Link Sprite')
    spriteVar = StringVar()
    spriteEntry = Entry(spriteDialogFrame, textvariable=spriteVar)

    def SpriteSelect():
        sprite = filedialog.askopenfilename()
        spriteVar.set(sprite)

    spriteSelectButton = Button(spriteDialogFrame, text='Select Sprite', command=SpriteSelect)

    baseSpriteLabel.pack(side=LEFT)
    spriteEntry.pack(side=LEFT)
    spriteSelectButton.pack(side=LEFT)

    romDialogFrame.pack()
    spriteDialogFrame.pack()

    checkBoxFrame.pack()
    fileDialogFrame.pack()

    drowDownFrame = Frame(topFrame)

    modeFrame = Frame(drowDownFrame)
    modeVar = StringVar()
    modeVar.set('open')
    modeOptionMenu = OptionMenu(modeFrame, modeVar, 'standard', 'open', 'swordless')
    modeOptionMenu.pack(side=RIGHT)
    modeLabel = Label(modeFrame, text='Game Mode')
    modeLabel.pack(side=LEFT)

    logicFrame = Frame(drowDownFrame)
    logicVar = StringVar()
    logicVar.set('noglitches')
    logicOptionMenu = OptionMenu(logicFrame, logicVar, 'noglitches', 'minorglitches')
    logicOptionMenu.pack(side=RIGHT)
    logicLabel = Label(logicFrame, text='Game logic')
    logicLabel.pack(side=LEFT)

    goalFrame = Frame(drowDownFrame)
    goalVar = StringVar()
    goalVar.set('ganon')
    goalOptionMenu = OptionMenu(goalFrame, goalVar, 'ganon', 'pedestal', 'dungeons', 'triforcehunt', 'crystals')
    goalOptionMenu.pack(side=RIGHT)
    goalLabel = Label(goalFrame, text='Game goal')
    goalLabel.pack(side=LEFT)

    difficultyFrame = Frame(drowDownFrame)
    difficultyVar = StringVar()
    difficultyVar.set('normal')
    difficultyOptionMenu = OptionMenu(difficultyFrame, difficultyVar, 'easy', 'normal', 'hard', 'expert', 'insane')
    difficultyOptionMenu.pack(side=RIGHT)
    difficultyLabel = Label(difficultyFrame, text='Game difficulty')
    difficultyLabel.pack(side=LEFT)

    timerFrame = Frame(drowDownFrame)
    timerVar = StringVar()
    timerVar.set('none')
    timerOptionMenu = OptionMenu(timerFrame, timerVar, 'none', 'display', 'timed', 'timed-ohko', 'ohko', 'timed-countdown')
    timerOptionMenu.pack(side=RIGHT)
    timerLabel = Label(timerFrame, text='Timer setting')
    timerLabel.pack(side=LEFT)

    progressiveFrame = Frame(drowDownFrame)
    progressiveVar = StringVar()
    progressiveVar.set('on')
    progressiveOptionMenu = OptionMenu(progressiveFrame, progressiveVar, 'on', 'off', 'random')
    progressiveOptionMenu.pack(side=RIGHT)
    progressiveLabel = Label(progressiveFrame, text='Progressive equipment')
    progressiveLabel.pack(side=LEFT)

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
    shuffleOptionMenu = OptionMenu(shuffleFrame, shuffleVar, 'vanilla', 'simple', 'restricted', 'full', 'madness', 'insanity', 'dungeonsfull', 'dungeonssimple')
    shuffleOptionMenu.pack(side=RIGHT)
    shuffleLabel = Label(shuffleFrame, text='Entrance shuffle algorithm')
    shuffleLabel.pack(side=LEFT)

    heartbeepFrame = Frame(drowDownFrame)
    heartbeepVar = StringVar()
    heartbeepVar.set('normal')
    heartbeepOptionMenu = OptionMenu(heartbeepFrame, heartbeepVar, 'normal', 'half', 'quarter', 'off')
    heartbeepOptionMenu.pack(side=RIGHT)
    heartbeepLabel = Label(heartbeepFrame, text='Heartbeep sound rate')
    heartbeepLabel.pack(side=LEFT)

    modeFrame.pack(expand=True, anchor=E)
    logicFrame.pack(expand=True, anchor=E)
    goalFrame.pack(expand=True, anchor=E)
    difficultyFrame.pack(expand=True, anchor=E)
    timerFrame.pack(expand=True, anchor=E)
    progressiveFrame.pack(expand=True, anchor=E)
    algorithmFrame.pack(expand=True, anchor=E)
    shuffleFrame.pack(expand=True, anchor=E)
    heartbeepFrame.pack(expand=True, anchor=E)

    bottomFrame = Frame(mainWindow)
    farBottomFrame = Frame(mainWindow)

    seedLabel = Label(bottomFrame, text='Seed #')
    seedVar = StringVar()
    seedEntry = Entry(bottomFrame, textvariable=seedVar)
    countLabel = Label(bottomFrame, text='Count')
    countVar = StringVar()
    countSpinbox = Spinbox(bottomFrame, from_=1, to=100, textvariable=countVar)

    def generateRom():
        guiargs = Namespace
        guiargs.seed = int(seedVar.get()) if seedVar.get() else None
        guiargs.count = int(countVar.get()) if countVar.get() != '1' else None
        guiargs.mode = modeVar.get()
        guiargs.logic = logicVar.get()
        guiargs.goal = goalVar.get()
        guiargs.difficulty = difficultyVar.get()
        guiargs.timer = timerVar.get()
        guiargs.progressive = progressiveVar.get()
        guiargs.algorithm = algorithmVar.get()
        guiargs.shuffle = shuffleVar.get()
        guiargs.heartbeep = heartbeepVar.get()
        guiargs.create_spoiler = bool(createSpoilerVar.get())
        guiargs.suppress_rom = bool(suppressRomVar.get())
        guiargs.keysanity = bool(keysanityVar.get())
        guiargs.nodungeonitems = bool(dungeonItemsVar.get())
        guiargs.beatableonly = bool(beatableOnlyVar.get())
        guiargs.fastmenu = bool(fastMenuVar.get())
        guiargs.quickswap = bool(quickSwapVar.get())
        guiargs.disablemusic = bool(disableMusicVar.get())
        guiargs.shuffleganon = bool(shuffleGanonVar.get())
        guiargs.rom = romVar.get()
        guiargs.jsonout = None
        guiargs.sprite = spriteVar.get() if spriteVar.get() else None
        try:
            if guiargs.count is not None:
                seed = guiargs.seed
                for i in range(guiargs.count):
                    main(seed=seed, args=guiargs)
                    seed = random.randint(0, 999999999)
            else:
                main(seed=guiargs.seed, args=guiargs)
        except Exception as e:
            messagebox.showerror(title="Error while creating seed", message=str(e))
        else:
            messagebox.showinfo(title="Success", message="Rom patched successfully")

    generateButton = Button(bottomFrame, text='Generate Patched Rom', command=generateRom)

    def open_output():
        open_file(output_path(''))

    openOutputButton = Button(farBottomFrame, text='Open Output Directory', command=open_output)

    if os.path.exists(local_path('README.html')):
        def open_readme():
            open_file(local_path('README.html'))
        openReadmeButton = Button(farBottomFrame, text='Open Documentation', command=open_readme)
        openReadmeButton.pack(side=LEFT)

    seedLabel.pack(side=LEFT)
    seedEntry.pack(side=LEFT)
    countLabel.pack(side=LEFT, padx=(5,0))
    countSpinbox.pack(side=LEFT)
    generateButton.pack(side=LEFT, padx=(5,0))

    openOutputButton.pack(side=RIGHT)

    drowDownFrame.pack(side=LEFT)
    rightHalfFrame.pack(side=RIGHT)
    topFrame.pack(side=TOP)
    farBottomFrame.pack(side=BOTTOM, fill=X, padx=5, pady=5)
    bottomFrame.pack(side=BOTTOM)

    if args is not None:
        # load values from commandline args
        createSpoilerVar.set(int(args.create_spoiler))
        suppressRomVar.set(int(args.suppress_rom))
        keysanityVar.set(args.keysanity)
        if args.nodungeonitems:
            dungeonItemsVar.set(int(not args.nodungeonitems))
        beatableOnlyVar.set(int(args.beatableonly))
        fastMenuVar.set(int(args.fastmenu))
        quickSwapVar.set(int(args.quickswap))
        disableMusicVar.set(int(args.disablemusic))
        if args.count:
            countVar.set(str(args.count))
        if args.seed:
            seedVar.set(str(args.seed))
        modeVar.set(args.mode)
        difficultyVar.set(args.difficulty)
        timerVar.set(args.timer)
        progressiveVar.set(args.progressive)
        goalVar.set(args.goal)
        algorithmVar.set(args.algorithm)
        shuffleVar.set(args.shuffle)
        heartbeepVar.set(args.heartbeep)
        logicVar.set(args.logic)
        romVar.set(args.rom)
        shuffleGanonVar.set(args.shuffleganon)
        if args.sprite is not None:
            spriteVar.set(args.sprite)

    mainWindow.mainloop()

def set_icon(window):
    er16 = PhotoImage(file=local_path('data/ER16.gif'))
    er32 = PhotoImage(file=local_path('data/ER32.gif'))
    er48 = PhotoImage(file=local_path('data/ER32.gif'))
    window.tk.call('wm', 'iconphoto', window._w, er16, er32, er48)

if __name__ == '__main__':
    guiMain()
