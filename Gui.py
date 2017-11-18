from Main import main, __version__ as ESVersion
from Utils import is_bundled, local_path, output_path, open_file
from argparse import Namespace
from Rom import Sprite
from glob import glob
import json
import random
import os
import shutil
from urllib.parse import urlparse
from urllib.request import urlopen
from tkinter import Checkbutton, OptionMenu, Toplevel, LabelFrame, PhotoImage, Tk, LEFT, RIGHT, BOTTOM, TOP, StringVar, IntVar, Frame, Label, W, E, X, Y, Entry, Spinbox, Button, filedialog, messagebox


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
        SpriteSelector(mainWindow, spriteVar.set)

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

class SpriteSelector(object):
    def __init__(self, parent, callback):
        if is_bundled():
            self.deploy_icons()
        self.parent = parent
        self.window = Toplevel(parent)
        self.callback = callback

        self.window.wm_title("TAKE ANY ONE YOU WANT")
        self.window['padx'] = 5
        self.window['pady'] = 5

        self.icon_section('Official Sprites', self.official_sprite_dir+'/*', 'Official Sprites not found. Click "Update Official Sprites" to download them.')
        self.icon_section('Unofficial Sprites', self.unofficial_sprite_dir+'/*', 'Put sprites in the Sprites/Unofficial folder to have them appear here.')

        frame = Frame(self.window)
        frame.pack(side=BOTTOM, fill=X, pady=5)

        button = Button(frame, text="Browse for file...", command=self.browse_for_sprite)
        button.pack(side=RIGHT, padx=(5, 0))

        button = Button(frame, text="Update Official Sprites", command=self.update_official_sprites)
        button.pack(side=RIGHT, padx=(5, 0))

        button = Button(frame, text="Use Default Sprite", command=self.use_default_sprite)
        button.pack(side=LEFT)

        set_icon(self.window)

    def icon_section(self, frame_label, path, no_results_label):
        frame = LabelFrame(self.window, text=frame_label, padx=5, pady=5)
        frame.pack(side=TOP, fill=X)

        i = 0
        for file in glob(output_path(path)):
            image = get_image_for_sprite(file)
            if image is None: continue
            button = Button(frame, image=image, command=lambda file=file: self.select_sprite(file))
            button.image = image
            button.grid(row=i // 16, column=i % 16)
            i += 1

        if i == 0:
            label = Label(frame, text="Put sprites in the Sprites/Unoffical folder to have them appear here.")
            label.pack()


    def update_official_sprites(self):
        # need to wrap in try catch. We don't want errors getting the json or downloading the files to break us.
        sprites_arr = json.loads(temp_sprites_json)
        current_sprites = [os.path.basename(file) for file in glob('sprites/official/*')]
        official_sprites = [(sprite['file'], os.path.basename(urlparse(sprite['file']).path)) for sprite in sprites_arr]
        needed_sprites = [(sprite_url, filename) for (sprite_url, filename) in official_sprites if filename not in current_sprites]

        for (sprite_url, filename) in needed_sprites:
            target = os.path.join('sprites/official',filename)
            with urlopen(sprite_url) as response, open(target, 'wb') as out:
                shutil.copyfileobj(response, out)

        official_filenames = [filename for (_, filename) in official_sprites]
        obsolete_sprites = [sprite for sprite in current_sprites if sprite not in official_filenames]
        for sprite in obsolete_sprites:
            os.remove(os.path.join('sprites/official', sprite))

        self.window.destroy()
        SpriteSelector(self.parent, self.callback)


    def browse_for_sprite(self):
        sprite = filedialog.askopenfilename()
        self.callback(sprite)
        self.window.destroy()

    def use_default_sprite(self):
        self.callback("")
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
        else:
            return self.local_official_sprite_dir

    @property
    def local_official_sprite_dir(site):
        return local_path("data/sprites/official")

    @property
    def unofficial_sprite_dir(self):
        if is_bundled():
            return output_path("sprites/unofficial")
        else:
            return self.local_unofficial_sprite_dir

    @property
    def local_unofficial_sprite_dir(site):
        return local_path("data/sprites/unofficial")

def get_image_for_sprite(filename):
    sprite = Sprite(filename)
    image = PhotoImage(height=24, width=16, palette="256/256/256")

    def color_to_hex(color):
        return "#{0:02X}{1:02X}{2:02X}".format(*color)

    def drawsprite(spr, pal_as_colors, offset):
        for y in range(len(spr)):
            for x in range(len(spr[y])):
                pal_index = spr[y][x]
                if pal_index:
                    color = pal_as_colors[pal_index - 1]
                    image.put(color_to_hex(color), to=(x + offset[0], y + offset[1]))

    shadow_palette = [(40, 40, 40)]
    shadow = [
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    ]

    drawsprite(shadow, shadow_palette, (2, 17))

    palettes = sprite.decode_palette()
    body = sprite.decode16(0x4C0)
    drawsprite(body, palettes[0], (0, 8))
    head = sprite.decode16(0x40)
    drawsprite(head, palettes[0], (0, 0))

    return image.zoom(2)

temp_sprites_json = '''[{"name":"Link","file":"http:\/\/spr.beegunslingers.com\/link.1.spr"},{"name":"Four Swords Link","file":"http:\/\/spr.beegunslingers.com\/4slink-armors.1.spr"},{"name":"Boo","file":"http:\/\/spr.beegunslingers.com\/boo.2.spr"},{"name":"Boy","file":"http:\/\/spr.beegunslingers.com\/boy.2.spr"},{"name":"Cactuar","file":"http:\/\/spr.beegunslingers.com\/cactuar.1.spr"},{"name":"Cat","file":"http:\/\/spr.beegunslingers.com\/cat.1.spr"},{"name":"Cat Boo","file":"http:\/\/spr.beegunslingers.com\/catboo.1.spr"},{"name":"Cirno","file":"http:\/\/spr.beegunslingers.com\/cirno.1.spr"},{"name":"Dark Boy","file":"http:\/\/spr.beegunslingers.com\/darkboy.2.spr"},{"name":"Dark Girl","file":"http:\/\/spr.beegunslingers.com\/darkgirl.1.spr"},{"name":"Dark Link","file":"http:\/\/spr.beegunslingers.com\/darklink.1.spr"},{"name":"Dark Maple Queen","file":"http:\/\/spr.beegunslingers.com\/shadowsaku.1.spr"},{"name":"Dark Swatchy","file":"http:\/\/spr.beegunslingers.com\/darkswatchy.1.spr"},{"name":"Dark Zelda","file":"http:\/\/spr.beegunslingers.com\/darkzelda.1.spr"},{"name":"Dark Zora","file":"http:\/\/spr.beegunslingers.com\/darkzora.2.spr"},{"name":"Decidueye","file":"http:\/\/spr.beegunslingers.com\/decidueye.1.spr"},{"name":"Demon Link","file":"http:\/\/spr.beegunslingers.com\/demonlink.1.spr"},{"name":"Frog","file":"http:\/\/spr.beegunslingers.com\/froglink.2.spr"},{"name":"Ganondorf","file":"http:\/\/spr.beegunslingers.com\/ganondorf.1.spr"},{"name":"Garfield","file":"http:\/\/spr.beegunslingers.com\/garfield.1.spr"},{"name":"Girl","file":"http:\/\/spr.beegunslingers.com\/girl.2.spr"},{"name":"Headless Link","file":"http:\/\/spr.beegunslingers.com\/headlesslink.1.spr"},{"name":"Invisible Man","file":"http:\/\/spr.beegunslingers.com\/invisibleman.1.spr"},{"name":"Inkling","file":"http:\/\/spr.beegunslingers.com\/inkling.1.spr"},{"name":"Kirby","file":"http:\/\/spr.beegunslingers.com\/kirby-meta.2.spr"},{"name":"Kore8","file":"http:\/\/spr.beegunslingers.com\/kore8.1.spr"},{"name":"Pony","file":"http:\/\/spr.beegunslingers.com\/littlepony.1.spr"},{"name":"Luigi","file":"http:\/\/spr.beegunslingers.com\/luigi.1.spr"},{"name":"Maiden","file":"http:\/\/spr.beegunslingers.com\/maiden.2.spr"},{"name":"Maple Queen","file":"http:\/\/spr.beegunslingers.com\/maplequeen.1.spr"},{"name":"Mario","file":"http:\/\/spr.beegunslingers.com\/mario-classic.1.spr"},{"name":"Marisa","file":"http:\/\/spr.beegunslingers.com\/marisa.1.spr"},{"name":"Mike Jones","file":"http:\/\/spr.beegunslingers.com\/mikejones.2.spr"},{"name":"Minish Cap Link","file":"http:\/\/spr.beegunslingers.com\/minishcaplink.3.spr"},{"name":"Modern Link","file":"http:\/\/spr.beegunslingers.com\/modernlink.1.spr"},{"name":"Mog","file":"http:\/\/spr.beegunslingers.com\/mog.1.spr"},{"name":"Mouse","file":"http:\/\/spr.beegunslingers.com\/mouse.1.spr"},{"name":"Nature Link","file":"http:\/\/spr.beegunslingers.com\/naturelink.1.spr"},{"name":"Negative Link","file":"http:\/\/spr.beegunslingers.com\/negativelink.1.spr"},{"name":"Neon Link","file":"http:\/\/spr.beegunslingers.com\/neonlink.1.spr"},{"name":"Old Man","file":"http:\/\/spr.beegunslingers.com\/oldman.1.spr"},{"name":"Pink Ribbon Link","file":"http:\/\/spr.beegunslingers.com\/pinkribbonlink.1.spr"},{"name":"Popoi","file":"http:\/\/spr.beegunslingers.com\/popoi.1.spr"},{"name":"Pug","file":"http:\/\/spr.beegunslingers.com\/pug.2.spr"},{"name":"Purple Chest","file":"http:\/\/spr.beegunslingers.com\/purplechest-bottle.2.spr"},{"name":"Roy Koopa","file":"http:\/\/spr.beegunslingers.com\/roykoopa.1.spr"},{"name":"Rumia","file":"http:\/\/spr.beegunslingers.com\/rumia.1.spr"},{"name":"Samus","file":"http:\/\/spr.beegunslingers.com\/samus.4.spr"},{"name":"Soda Can","file":"http:\/\/spr.beegunslingers.com\/sodacan.1.spr"},{"name":"Static Link","file":"http:\/\/spr.beegunslingers.com\/staticlink.1.spr"},{"name":"Santa Link","file":"http:\/\/spr.beegunslingers.com\/santalink.1.spr"},{"name":"Super Bunny","file":"http:\/\/spr.beegunslingers.com\/superbunny.1.spr"},{"name":"Swatchy","file":"http:\/\/spr.beegunslingers.com\/swatchy.1.spr"},{"name":"Tingle","file":"http:\/\/spr.beegunslingers.com\/tingle.1.spr"},{"name":"Toad","file":"http:\/\/spr.beegunslingers.com\/toad.1.spr"},{"name":"Valeera","file":"http:\/\/spr.beegunslingers.com\/valeera.1.spr"},{"name":"Vitreous","file":"http:\/\/spr.beegunslingers.com\/vitreous.1.spr"},{"name":"Vivi","file":"http:\/\/spr.beegunslingers.com\/vivi.1.spr"},{"name":"Will","file":"http:\/\/spr.beegunslingers.com\/will.1.spr"},{"name":"Wizzrobe","file":"http:\/\/spr.beegunslingers.com\/wizzrobe.4.spr"},{"name":"Yunica","file":"http:\/\/spr.beegunslingers.com\/yunica.1.spr"},{"name":"Zelda","file":"http:\/\/spr.beegunslingers.com\/zelda.2.spr"},{"name":"Zero Suit Samus","file":"http:\/\/spr.beegunslingers.com\/zerosuitsamus.1.spr"},{"name":"Zora","file":"http:\/\/spr.beegunslingers.com\/zora.1.spr"}]'''

if __name__ == '__main__':
    guiMain()
