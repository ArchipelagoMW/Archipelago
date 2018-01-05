#!/usr/bin/env python3
from argparse import Namespace
from glob import glob
import json
import random
import os
import shutil
from tkinter import Checkbutton, OptionMenu, Toplevel, LabelFrame, PhotoImage, Tk, LEFT, RIGHT, BOTTOM, TOP, StringVar, IntVar, Frame, Label, W, E, X, Entry, Spinbox, Button, filedialog, messagebox, ttk
from urllib.parse import urlparse
from urllib.request import urlopen

from AdjusterMain import adjust
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
    notebook.add(randomizerWindow, text='Randomize')
    notebook.add(adjustWindow, text='Adjust')
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
    quickSwapVar = IntVar()
    quickSwapCheckbutton = Checkbutton(checkBoxFrame, text="Enabled L/R Item quickswapping", variable=quickSwapVar)
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
    baseSpriteLabel = Label(spriteDialogFrame, text='Link Sprite:')

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

    spriteSelectButton = Button(spriteDialogFrame, text='Open Sprite Picker', command=SpriteSelect)

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


    fastMenuFrame = Frame(drowDownFrame)
    fastMenuVar = StringVar()
    fastMenuVar.set('normal')
    fastMenuOptionMenu = OptionMenu(fastMenuFrame, fastMenuVar, 'normal', 'instant', 'double', 'triple', 'quadruple', 'half')
    fastMenuOptionMenu.pack(side=RIGHT)
    fastMenuLabel = Label(fastMenuFrame, text='Menu speed')
    fastMenuLabel.pack(side=LEFT)

    modeFrame.pack(expand=True, anchor=E)
    logicFrame.pack(expand=True, anchor=E)
    goalFrame.pack(expand=True, anchor=E)
    difficultyFrame.pack(expand=True, anchor=E)
    timerFrame.pack(expand=True, anchor=E)
    progressiveFrame.pack(expand=True, anchor=E)
    algorithmFrame.pack(expand=True, anchor=E)
    shuffleFrame.pack(expand=True, anchor=E)
    heartbeepFrame.pack(expand=True, anchor=E)
    fastMenuFrame.pack(expand=True, anchor=E)

    bottomFrame = Frame(randomizerWindow)

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
        guiargs.fastmenu = fastMenuVar.get()
        guiargs.create_spoiler = bool(createSpoilerVar.get())
        guiargs.suppress_rom = bool(suppressRomVar.get())
        guiargs.keysanity = bool(keysanityVar.get())
        guiargs.nodungeonitems = bool(dungeonItemsVar.get())
        guiargs.beatableonly = bool(beatableOnlyVar.get())
        guiargs.quickswap = bool(quickSwapVar.get())
        guiargs.disablemusic = bool(disableMusicVar.get())
        guiargs.shuffleganon = bool(shuffleGanonVar.get())
        guiargs.rom = romVar.get()
        guiargs.jsonout = None
        guiargs.sprite = sprite
        try:
            if guiargs.count is not None:
                seed = guiargs.seed
                for _ in range(guiargs.count):
                    main(seed=seed, args=guiargs)
                    seed = random.randint(0, 999999999)
            else:
                main(seed=guiargs.seed, args=guiargs)
        except Exception as e:
            messagebox.showerror(title="Error while creating seed", message=str(e))
        else:
            messagebox.showinfo(title="Success", message="Rom patched successfully")

    generateButton = Button(bottomFrame, text='Generate Patched Rom', command=generateRom)

    seedLabel.pack(side=LEFT)
    seedEntry.pack(side=LEFT)
    countLabel.pack(side=LEFT, padx=(5, 0))
    countSpinbox.pack(side=LEFT)
    generateButton.pack(side=LEFT, padx=(5, 0))

    openOutputButton.pack(side=RIGHT)

    drowDownFrame.pack(side=LEFT)
    rightHalfFrame.pack(side=RIGHT)
    topFrame.pack(side=TOP)
    bottomFrame.pack(side=BOTTOM)

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
        rom = filedialog.askopenfilename()
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
    heartbeepOptionMenu2 = OptionMenu(heartbeepFrame2, heartbeepVar, 'normal', 'half', 'quarter', 'off')
    heartbeepOptionMenu2.pack(side=RIGHT)
    heartbeepLabel2 = Label(heartbeepFrame2, text='Heartbeep sound rate')
    heartbeepLabel2.pack(side=LEFT)

    fastMenuFrame2 = Frame(drowDownFrame2)
    fastMenuOptionMenu2 = OptionMenu(fastMenuFrame2, fastMenuVar, 'normal', 'instant', 'double', 'triple', 'quadruple', 'half')
    fastMenuOptionMenu2.pack(side=RIGHT)
    fastMenuLabel2 = Label(fastMenuFrame2, text='Menu speed')
    fastMenuLabel2.pack(side=LEFT)

    heartbeepFrame2.pack(expand=True, anchor=E)
    fastMenuFrame2.pack(expand=True, anchor=E)

    bottomFrame2 = Frame(topFrame2)

    def adjustRom():
        guiargs = Namespace
        guiargs.heartbeep = heartbeepVar.get()
        guiargs.fastmenu = bool(fastMenuVar.get())
        guiargs.quickswap = bool(quickSwapVar.get())
        guiargs.disablemusic = bool(disableMusicVar.get())
        guiargs.rom = romVar2.get()
        guiargs.sprite = sprite
        try:
            adjust(args=guiargs)
        except Exception as e:
            messagebox.showerror(title="Error while creating seed", message=str(e))
        else:
            messagebox.showinfo(title="Success", message="Rom patched successfully")

    adjustButton = Button(bottomFrame2, text='Adjust Rom', command=adjustRom)

    adjustButton.pack(side=LEFT, padx=(5, 0))

    drowDownFrame2.pack(side=LEFT, pady=(0, 40))
    rightHalfFrame2.pack(side=RIGHT)
    topFrame2.pack(side=TOP, pady=30)
    bottomFrame2.pack(side=BOTTOM, pady=(180, 0))

    if args is not None:
        # load values from commandline args
        createSpoilerVar.set(int(args.create_spoiler))
        suppressRomVar.set(int(args.suppress_rom))
        keysanityVar.set(args.keysanity)
        if args.nodungeonitems:
            dungeonItemsVar.set(int(not args.nodungeonitems))
        beatableOnlyVar.set(int(args.beatableonly))
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
        fastMenuVar.set(args.fastmenu)
        logicVar.set(args.logic)
        romVar.set(args.rom)
        shuffleGanonVar.set(args.shuffleganon)
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

        button = Button(frame, text="Use default Link sprite", command=self.use_default_link_sprite)
        button.pack(side=LEFT, padx=(0, 5))

        if adjuster:
            button = Button(frame, text="Use current sprite from rom", command=self.use_default_sprite)
            button.pack(side=LEFT, padx=(0, 5))

        set_icon(self.window)
        self.window.focus()

    def icon_section(self, frame_label, path, no_results_label):
        frame = LabelFrame(self.window, labelwidget=frame_label, padx=5, pady=5)
        frame.pack(side=TOP, fill=X)

        i = 0
        for file in glob(output_path(path)):
            sprite = Sprite(file)
            image = get_image_for_sprite(sprite)
            if image is None:
                continue
            button = Button(frame, image=image, command=lambda spr=sprite: self.select_sprite(spr))
            ToolTips.register(button, sprite.name + ("\nBy: %s" % sprite.author_name if sprite.author_name is not None else ""))
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
                with urlopen('http://vt.alttp.run/sprites') as response:
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
                resultmessage = "official sprites updated sucessfully"

            task.queue_event(finished)

        BackgroundTaskProgress(self.parent, work, "Updating Sprites")


    def browse_for_sprite(self):
        sprite = filedialog.askopenfilename()
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
    guiMain()
