#!/usr/bin/env python3
import argparse
import json
import os
import logging
import queue
import random
import shutil
import textwrap
import sys
import threading
import time
import tkinter as tk
from argparse import Namespace
from concurrent.futures import as_completed, ThreadPoolExecutor
from glob import glob
from tkinter import Tk, Frame, Label, StringVar, Entry, filedialog, messagebox, Button, Radiobutton, LEFT, X, BOTH, TOP, LabelFrame, \
    IntVar, Checkbutton, E, W, OptionMenu, Toplevel, BOTTOM, RIGHT, font as font, PhotoImage
from tkinter.constants import DISABLED, NORMAL
from urllib.parse import urlparse
from urllib.request import urlopen

import ModuleUpdate
ModuleUpdate.update()

from worlds.alttp.Rom import Sprite, LocalRom, apply_rom_settings, get_base_rom_bytes
from Utils import output_path, local_path, user_path, open_file, get_cert_none_ssl_context, persistent_store, \
    get_adjuster_settings, get_adjuster_settings_no_defaults, tkinter_center_window, init_logging


GAME_ALTTP = "A Link to the Past"
WINDOW_MIN_HEIGHT = 525
WINDOW_MIN_WIDTH = 425


class AdjusterWorld(object):
    class AdjusterSubWorld(object):
        def __init__(self, random):
            self.random = random

    def __init__(self, sprite_pool):
        import random
        self.sprite_pool = {1: sprite_pool}
        self.worlds = {1: self.AdjusterSubWorld(random)}


class ArgumentDefaultsHelpFormatter(argparse.RawTextHelpFormatter):

    def _get_help_string(self, action):
        return textwrap.dedent(action.help)


# See argparse.BooleanOptionalAction
class BooleanOptionalActionWithDisable(argparse.Action):
    def __init__(self,
                 option_strings,
                 dest,
                 default=None,
                 type=None,
                 choices=None,
                 required=False,
                 help=None,
                 metavar=None):

        _option_strings = []
        for option_string in option_strings:
            _option_strings.append(option_string)

            if option_string.startswith('--'):
                option_string = '--disable' + option_string[2:]
                _option_strings.append(option_string)

        if help is not None and default is not None:
            help += " (default: %(default)s)"

        super().__init__(
            option_strings=_option_strings,
            dest=dest,
            nargs=0,
            default=default,
            type=type,
            choices=choices,
            required=required,
            help=help,
            metavar=metavar)

    def __call__(self, parser, namespace, values, option_string=None):
        if option_string in self.option_strings:
            setattr(namespace, self.dest, not option_string.startswith('--disable'))

    def format_usage(self):
        return ' | '.join(self.option_strings)


def get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('rom', nargs="?", default='AP_LttP.sfc', help='Path to an ALttP rom to adjust.')
    parser.add_argument('--baserom', default='Zelda no Densetsu - Kamigami no Triforce (Japan).sfc',
                        help='Path to an ALttP Japan(1.0) rom to use as a base.')
    parser.add_argument('--loglevel', default='info', const='info', nargs='?',
                        choices=['error', 'info', 'warning', 'debug'], help='Select level of logging for output.')
    parser.add_argument('--auto_apply', default='ask',
                        choices=['ask', 'always', 'never'], help='Whether or not to apply settings automatically in the future.')
    parser.add_argument('--menuspeed', default='normal', const='normal', nargs='?',
                        choices=['normal', 'instant', 'double', 'triple', 'quadruple', 'half'],
                        help='''\
                             Select the rate at which the menu opens and closes.
                             (default: %(default)s)
                             ''')
    parser.add_argument('--quickswap', help='Enable quick item swapping with L and R.', action='store_true')
    parser.add_argument('--deathlink', help='Enable DeathLink system.', action='store_true')
    parser.add_argument('--allowcollect', help='Allow collection of other player items', action='store_true')
    parser.add_argument('--music', default=True, help='Enables/Disables game music.', action=BooleanOptionalActionWithDisable)
    parser.add_argument('--triforcehud', default='hide_goal', const='hide_goal', nargs='?',
                        choices=['normal', 'hide_goal', 'hide_required', 'hide_both'],
                        help='''\
                            Hide the triforce hud in certain circumstances.
                            hide_goal will hide the hud until finding a triforce piece, hide_required will hide the total amount needed to win
                            (Both can be revealed when speaking to Murahalda)
                            (default: %(default)s)
                            ''')
    parser.add_argument('--enableflashing',
                        help='Reenable flashing animations (unfriendly to epilepsy, always disabled in race roms)',
                        action='store_false', dest="reduceflashing")
    parser.add_argument('--heartbeep', default='normal', const='normal', nargs='?',
                        choices=['double', 'normal', 'half', 'quarter', 'off'],
                        help='''\
                             Select the rate at which the heart beep sound is played at
                             low health. (default: %(default)s)
                             ''')
    parser.add_argument('--heartcolor', default='red', const='red', nargs='?',
                        choices=['red', 'blue', 'green', 'yellow', 'random'],
                        help='Select the color of Link\'s heart meter. (default: %(default)s)')
    parser.add_argument('--ow_palettes', default='default',
                        choices=['default', 'random', 'blackout', 'puke', 'classic', 'grayscale', 'negative', 'dizzy',
                                 'sick'])
    parser.add_argument('--shield_palettes', default='default',
                        choices=['default', 'random', 'blackout', 'puke', 'classic', 'grayscale', 'negative', 'dizzy',
                                 'sick'])
    parser.add_argument('--sword_palettes', default='default',
                        choices=['default', 'random', 'blackout', 'puke', 'classic', 'grayscale', 'negative', 'dizzy',
                                 'sick'])
    parser.add_argument('--hud_palettes', default='default',
                        choices=['default', 'random', 'blackout', 'puke', 'classic', 'grayscale', 'negative', 'dizzy',
                                 'sick'])
    parser.add_argument('--uw_palettes', default='default',
                        choices=['default', 'random', 'blackout', 'puke', 'classic', 'grayscale', 'negative', 'dizzy',
                                 'sick'])
    parser.add_argument('--sprite', help='''\
                             Path to a sprite sheet to use for Link. Needs to be in
                             binary format and have a length of 0x7000 (28672) bytes,
                             or 0x7078 (28792) bytes including palette data.
                             Alternatively, can be a ALttP Rom patched with a Link
                             sprite that will be extracted.
                             ''')
    parser.add_argument('--sprite_pool', nargs='+', default=[], help='''
                             A list of sprites to pull from.
                        ''')
    parser.add_argument('--oof', help='''\
                             Path to a sound effect to replace Link's "oof" sound.
                             Needs to be in a .brr format and have a length of no
                             more than 2673 bytes, created from a 16-bit signed PCM
                             .wav at 12khz. https://github.com/boldowa/snesbrr
                             ''')
    parser.add_argument('--update_sprites', action='store_true', help='Update Sprite Database, then exit.')
    return parser


def main():
    parser = get_argparser()
    args = parser.parse_args(namespace=get_adjuster_settings_no_defaults(GAME_ALTTP))
    
    # set up logger
    loglevel = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}[
        args.loglevel]
    logging.basicConfig(format='%(message)s', level=loglevel)

    if args.update_sprites:
        run_sprite_update()
        sys.exit()

    if not os.path.isfile(args.rom):
        adjustGUI()
    else:
        if args.sprite is not None and not os.path.isfile(args.sprite) and not Sprite.get_sprite_from_name(args.sprite):
            input('Could not find link sprite sheet at given location. \nPress Enter to exit.')
            sys.exit(1)
        if args.oof is not None and not os.path.isfile(args.oof):
            input('Could not find oof sound effect at given location. \nPress Enter to exit.')
            sys.exit(1)
        if args.oof is not None and os.path.getsize(args.oof) > 2673:
            input('"oof" sound effect cannot exceed 2673 bytes. \nPress Enter to exit.')
            sys.exit(1)
            

        args, path = adjust(args=args)
        if isinstance(args.sprite, Sprite):
            args.sprite = args.sprite.name
        persistent_store("adjuster", GAME_ALTTP, args)


def adjust(args):
    start = time.perf_counter()
    init_logging("LttP Adjuster")
    logger = logging.getLogger('Adjuster')
    logger.info('Patching ROM.')
    vanillaRom = args.baserom
    if not os.path.exists(vanillaRom) and not os.path.isabs(vanillaRom):
        vanillaRom = local_path(vanillaRom)
    if os.path.splitext(args.rom)[-1].lower() == '.aplttp':
        import Patch
        meta, args.rom = Patch.create_rom_file(args.rom)

    if os.stat(args.rom).st_size in (0x200000, 0x400000) and os.path.splitext(args.rom)[-1].lower() == '.sfc':
        rom = LocalRom(args.rom, patch=False, vanillaRom=vanillaRom)
    else:
        raise RuntimeError(
            'Provided Rom is not a valid Link to the Past Randomizer Rom. Please provide one for adjusting.')
    palettes_options = {}
    palettes_options['dungeon'] = args.uw_palettes

    palettes_options['overworld'] = args.ow_palettes
    palettes_options['hud'] = args.hud_palettes
    palettes_options['sword'] = args.sword_palettes
    palettes_options['shield'] = args.shield_palettes
    # palettes_options['link']=args.link_palettesvera

    racerom = rom.read_byte(0x180213) > 0
    world = None
    if hasattr(args, "world"):
        world = getattr(args, "world")

    apply_rom_settings(rom, args.heartbeep, args.heartcolor, args.quickswap, args.menuspeed, args.music,
                       args.sprite, args.oof, palettes_options, reduceflashing=args.reduceflashing or racerom, world=world,
                       deathlink=args.deathlink, allowcollect=args.allowcollect)
    path = output_path(f'{os.path.basename(args.rom)[:-4]}_adjusted.sfc')
    rom.write_to_file(path)

    logger.info('Done. Enjoy.')
    logger.debug('Total Time: %s', time.perf_counter() - start)

    return args, path


def adjustGUI():
    from tkinter import Tk, LEFT, BOTTOM, TOP, \
        StringVar, Frame, Label, X, Entry, Button, filedialog, messagebox, ttk
    from argparse import Namespace
    from Utils import __version__ as MWVersion
    adjustWindow = Tk()
    adjustWindow.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
    adjustWindow.wm_title("Archipelago %s LttP Adjuster" % MWVersion)
    set_icon(adjustWindow)

    rom_options_frame, rom_vars, set_sprite = get_rom_options_frame(adjustWindow)

    bottomFrame2 = Frame(adjustWindow, padx=8, pady=2)

    romFrame, romVar = get_rom_frame(adjustWindow)

    romDialogFrame = Frame(adjustWindow, padx=8, pady=2)
    baseRomLabel2 = Label(romDialogFrame, text='Rom to adjust')
    romVar2 = StringVar()
    romEntry2 = Entry(romDialogFrame, textvariable=romVar2)

    def RomSelect2():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".sfc", ".smc", ".aplttp")), ("All Files", "*")])
        romVar2.set(rom)

    romSelectButton2 = Button(romDialogFrame, text='Select Rom', command=RomSelect2)
    romDialogFrame.pack(side=TOP, expand=False, fill=X)
    baseRomLabel2.pack(side=LEFT, expand=False, fill=X, padx=(0, 8))
    romEntry2.pack(side=LEFT, expand=True, fill=BOTH, pady=1)
    romSelectButton2.pack(side=LEFT)

    def adjustRom():
        guiargs = Namespace()
        guiargs.auto_apply = rom_vars.auto_apply.get()
        guiargs.heartbeep = rom_vars.heartbeepVar.get()
        guiargs.heartcolor = rom_vars.heartcolorVar.get()
        guiargs.menuspeed = rom_vars.menuspeedVar.get()
        guiargs.ow_palettes = rom_vars.owPalettesVar.get()
        guiargs.uw_palettes = rom_vars.uwPalettesVar.get()
        guiargs.hud_palettes = rom_vars.hudPalettesVar.get()
        guiargs.sword_palettes = rom_vars.swordPalettesVar.get()
        guiargs.shield_palettes = rom_vars.shieldPalettesVar.get()
        guiargs.quickswap = bool(rom_vars.quickSwapVar.get())
        guiargs.music = bool(rom_vars.MusicVar.get())
        guiargs.reduceflashing = bool(rom_vars.disableFlashingVar.get())
        guiargs.deathlink = bool(rom_vars.DeathLinkVar.get())
        guiargs.allowcollect = bool(rom_vars.AllowCollectVar.get())
        guiargs.rom = romVar2.get()
        guiargs.baserom = romVar.get()
        guiargs.sprite = rom_vars.sprite
        if rom_vars.sprite_pool:
            guiargs.world = AdjusterWorld(rom_vars.sprite_pool)
        guiargs.oof = rom_vars.oof

        try:
            guiargs, path = adjust(args=guiargs)
            if rom_vars.sprite_pool:
                guiargs.sprite_pool = rom_vars.sprite_pool
                delattr(guiargs, "world")
        except Exception as e:
            logging.exception(e)
            messagebox.showerror(title="Error while adjusting Rom", message=str(e))
        else:
            messagebox.showinfo(title="Success", message=f"Rom patched successfully to {path}")
            if isinstance(guiargs.sprite, Sprite):
                guiargs.sprite = guiargs.sprite.name
            delattr(guiargs, "rom")
            persistent_store("adjuster", GAME_ALTTP, guiargs)

    def saveGUISettings():
        guiargs = Namespace()
        guiargs.auto_apply = rom_vars.auto_apply.get()
        guiargs.heartbeep = rom_vars.heartbeepVar.get()
        guiargs.heartcolor = rom_vars.heartcolorVar.get()
        guiargs.menuspeed = rom_vars.menuspeedVar.get()
        guiargs.ow_palettes = rom_vars.owPalettesVar.get()
        guiargs.uw_palettes = rom_vars.uwPalettesVar.get()
        guiargs.hud_palettes = rom_vars.hudPalettesVar.get()
        guiargs.sword_palettes = rom_vars.swordPalettesVar.get()
        guiargs.shield_palettes = rom_vars.shieldPalettesVar.get()
        guiargs.quickswap = bool(rom_vars.quickSwapVar.get())
        guiargs.music = bool(rom_vars.MusicVar.get())
        guiargs.reduceflashing = bool(rom_vars.disableFlashingVar.get())
        guiargs.deathlink = bool(rom_vars.DeathLinkVar.get())
        guiargs.allowcollect = bool(rom_vars.AllowCollectVar.get())
        guiargs.baserom = romVar.get()
        if isinstance(rom_vars.sprite, Sprite):
            guiargs.sprite = rom_vars.sprite.name
        else:
            guiargs.sprite = rom_vars.sprite
        guiargs.sprite_pool = rom_vars.sprite_pool
        guiargs.oof = rom_vars.oof
        persistent_store("adjuster", GAME_ALTTP, guiargs)
        messagebox.showinfo(title="Success", message="Settings saved to persistent storage")

    adjustButton = Button(bottomFrame2, text='Adjust Rom', command=adjustRom)
    rom_options_frame.pack(side=TOP, padx=8, pady=8, fill=BOTH, expand=True)
    adjustButton.pack(side=LEFT, padx=(5,5))

    saveButton = Button(bottomFrame2, text='Save Settings', command=saveGUISettings)
    saveButton.pack(side=LEFT, padx=(5,5))
    bottomFrame2.pack(side=TOP, pady=(5,5))

    tkinter_center_window(adjustWindow)
    adjustWindow.mainloop()


def run_sprite_update():
    import threading
    done = threading.Event()
    try:
        top = Tk()
    except:
        task = BackgroundTaskProgressNullWindow(update_sprites, lambda successful, resultmessage: done.set())
    else:
        top.withdraw()
        task = BackgroundTaskProgress(top, update_sprites, "Updating Sprites", lambda succesful, resultmessage: done.set())
    while not done.is_set():
        task.do_events()
    logging.info("Done updating sprites")


def update_sprites(task, on_finish=None, repository_url: str = "https://alttpr.com/sprites"):
    resultmessage = ""
    successful = True
    sprite_dir = user_path("data", "sprites", "alttp", "remote")
    os.makedirs(sprite_dir, exist_ok=True)
    ctx = get_cert_none_ssl_context()

    def finished():
        task.close_window()
        if on_finish:
            on_finish(successful, resultmessage)

    try:
        task.update_status("Downloading remote sprites list")
        with urlopen(repository_url, context=ctx) as response:
            sprites_arr = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        resultmessage = "Error getting list of remote sprites. Sprites not updated.\n\n%s: %s" % (type(e).__name__, e)
        successful = False
        task.queue_event(finished)
        return

    try:
        task.update_status("Determining needed sprites")
        current_sprites = [os.path.basename(file) for file in glob(sprite_dir + '/*')]
        remote_sprites = [(sprite['file'], os.path.basename(urlparse(sprite['file']).path))
                          for sprite in sprites_arr if sprite["author"] != "Nintendo"]
        needed_sprites = [(sprite_url, filename) for (sprite_url, filename) in remote_sprites if
                          filename not in current_sprites]

        remote_filenames = [filename for (_, filename) in remote_sprites]
        obsolete_sprites = [sprite for sprite in current_sprites if sprite not in remote_filenames]
    except Exception as e:
        resultmessage = "Error Determining which sprites to update. Sprites not updated.\n\n%s: %s" % (
        type(e).__name__, e)
        successful = False
        task.queue_event(finished)
        return

    def dl(sprite_url, filename):
        target = os.path.join(sprite_dir, filename)
        with urlopen(sprite_url, context=ctx) as response, open(target, 'wb') as out:
            shutil.copyfileobj(response, out)

    def rem(sprite):
        os.remove(os.path.join(sprite_dir, sprite))

    with ThreadPoolExecutor() as pool:
        dl_tasks = []
        rem_tasks = []

        for (sprite_url, filename) in needed_sprites:
            dl_tasks.append(pool.submit(dl, sprite_url, filename))

        for sprite in obsolete_sprites:
            rem_tasks.append(pool.submit(rem, sprite))

        deleted = 0
        updated = 0

        for dl_task in as_completed(dl_tasks):
            updated += 1
            task.update_status("Downloading needed sprite %g/%g" % (updated, len(needed_sprites)))
            try:
                dl_task.result()
            except Exception as e:
                logging.exception(e)
                resultmessage = "Error downloading sprite. Not all sprites updated.\n\n%s: %s" % (
                    type(e).__name__, e)
                successful = False

        for rem_task in as_completed(rem_tasks):
            deleted += 1
            task.update_status("Removing obsolete sprite %g/%g" % (deleted, len(obsolete_sprites)))
            try:
                rem_task.result()
            except Exception as e:
                logging.exception(e)
                resultmessage = "Error removing obsolete sprite. Not all sprites updated.\n\n%s: %s" % (
                    type(e).__name__, e)
                successful = False

    if successful:
        resultmessage = "Remote sprites updated successfully"

    task.queue_event(finished)


def set_icon(window):
    logo = tk.PhotoImage(file=local_path('data', 'icon.png'))
    window.tk.call('wm', 'iconphoto', window._w, logo)


class BackgroundTask(object):
    def __init__(self, window, code_to_run, *args):
        self.window = window
        self.queue = queue.Queue()
        self.running = True
        self.process_queue()
        self.task = threading.Thread(target=code_to_run, args=(self, *args))
        self.task.start()

    def stop(self):
        self.running = False

    # safe to call from worker
    def queue_event(self, event):
        self.queue.put(event)

    def process_queue(self):
        try:
            while True:
                if not self.running:
                    return
                event = self.queue.get_nowait()
                event()
                if self.running:
                    # if self is no longer running self.window may no longer be valid
                    self.window.update_idletasks()
        except queue.Empty:
            pass
        if self.running:
            self.window.after(100, self.process_queue)


class BackgroundTaskProgress(BackgroundTask):
    def __init__(self, parent, code_to_run, title, *args):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window['padx'] = 5
        self.window['pady'] = 5

        try:
            self.window.attributes("-toolwindow", 1)
        except tk.TclError:
            pass

        self.window.wm_title(title)
        self.label_var = tk.StringVar()
        self.label_var.set("")
        self.label = tk.Label(self.window, textvariable=self.label_var, width=50)
        self.label.pack()
        self.window.resizable(width=False, height=False)

        set_icon(self.window)
        self.window.focus()
        super().__init__(self.window, code_to_run, *args)

    # safe to call from worker thread
    def update_status(self, text):
        self.queue_event(lambda: self.label_var.set(text))

    def do_events(self):
        self.parent.update()

    # only call this in an event callback
    def close_window(self):
        self.stop()
        self.window.destroy()


class BackgroundTaskProgressNullWindow(BackgroundTask):
    def __init__(self, code_to_run, *args):
        super().__init__(None, code_to_run, *args)

    def process_queue(self):
        try:
            while True:
                if not self.running:
                    return
                event = self.queue.get_nowait()
                event()
        except queue.Empty:
            pass

    def do_events(self):
        self.process_queue()

    def update_status(self, text):
        self.queue_event(lambda: logging.info(text))

    def close_window(self):
        self.stop()


class AttachTooltip(object):

    def __init__(self, parent, text):
        self._parent = parent
        self._text = text
        self._window = None
        parent.bind('<Enter>', lambda event : self.show())
        parent.bind('<Leave>', lambda event : self.hide())

    def show(self):
        if self._window or not self._text:
            return
        self._window = Toplevel(self._parent)
        #remove window bar controls
        self._window.wm_overrideredirect(1)
        #adjust positioning
        x, y, *_ = self._parent.bbox("insert")
        x = x + self._parent.winfo_rootx() + 20
        y = y + self._parent.winfo_rooty() + 20
        self._window.wm_geometry("+{0}+{1}".format(x,y))
        #show text
        label = Label(self._window, text=self._text, justify=LEFT)
        label.pack(ipadx=1)

    def hide(self):
        if self._window:
            self._window.destroy()
            self._window = None


def get_rom_frame(parent=None):
    adjuster_settings = get_adjuster_settings(GAME_ALTTP)

    romFrame = Frame(parent, padx=8, pady=8)
    baseRomLabel = Label(romFrame, text='LttP Base Rom: ')
    romVar = StringVar(value=adjuster_settings.baserom)
    romEntry = Entry(romFrame, textvariable=romVar)

    def RomSelect():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".sfc", ".smc")), ("All Files", "*")])
        try:
            get_base_rom_bytes(rom)  # throws error on checksum fail
        except Exception as e:
            logging.exception(e)
            messagebox.showerror(title="Error while reading ROM", message=str(e))
        else:
            romVar.set(rom)
            romSelectButton['state'] = "disabled"
            romSelectButton["text"] = "ROM verified"

    romSelectButton = Button(romFrame, text='Select Rom', command=RomSelect)

    baseRomLabel.pack(side=LEFT)
    romEntry.pack(side=LEFT, expand=True, fill=BOTH, pady=1)
    romSelectButton.pack(side=LEFT)
    romFrame.pack(side=TOP, fill=X)

    return romFrame, romVar

def get_rom_options_frame(parent=None):
    adjuster_settings = get_adjuster_settings(GAME_ALTTP)

    romOptionsFrame = LabelFrame(parent, text="Rom options", padx=8, pady=8)

    for i in range(5):
        romOptionsFrame.rowconfigure(i, weight=0, pad=4)
    vars = Namespace()

    vars.MusicVar = IntVar()
    vars.MusicVar.set(adjuster_settings.music)
    MusicCheckbutton = Checkbutton(romOptionsFrame, text="Music", variable=vars.MusicVar)
    MusicCheckbutton.grid(row=0, column=0, sticky=E)

    vars.disableFlashingVar = IntVar(value=adjuster_settings.reduceflashing)
    disableFlashingCheckbutton = Checkbutton(romOptionsFrame, text="Disable flashing (anti-epilepsy)",
                                             variable=vars.disableFlashingVar)
    disableFlashingCheckbutton.grid(row=6, column=0, sticky=W)

    vars.DeathLinkVar = IntVar(value=adjuster_settings.deathlink)
    DeathLinkCheckbutton = Checkbutton(romOptionsFrame, text="DeathLink (Team Deaths)", variable=vars.DeathLinkVar)
    DeathLinkCheckbutton.grid(row=7, column=0, sticky=W)

    vars.AllowCollectVar = IntVar(value=adjuster_settings.allowcollect)
    AllowCollectCheckbutton = Checkbutton(romOptionsFrame, text="Allow Collect", variable=vars.AllowCollectVar)
    AllowCollectCheckbutton.grid(row=8, column=0, sticky=W)

    spriteDialogFrame = Frame(romOptionsFrame)
    spriteDialogFrame.grid(row=0, column=1)
    baseSpriteLabel = Label(spriteDialogFrame, text='Sprite:')

    vars.spriteNameVar = StringVar()
    vars.sprite = adjuster_settings.sprite

    def set_sprite(sprite_param):
        nonlocal vars
        if isinstance(sprite_param, str):
            vars.sprite = sprite_param
            vars.spriteNameVar.set(sprite_param)
        elif sprite_param is None or not sprite_param.valid:
            vars.sprite = None
            vars.spriteNameVar.set('(unchanged)')
        else:
            vars.sprite = sprite_param
            vars.spriteNameVar.set(vars.sprite.name)

    set_sprite(adjuster_settings.sprite)
    #vars.spriteNameVar.set(adjuster_settings.sprite)
    spriteEntry = Label(spriteDialogFrame, textvariable=vars.spriteNameVar)

    def SpriteSelect():
        nonlocal vars
        SpriteSelector(parent, set_sprite, spritePool=vars.sprite_pool)

    spriteSelectButton = Button(spriteDialogFrame, text='...', command=SpriteSelect)

    baseSpriteLabel.pack(side=LEFT)
    spriteEntry.pack(side=LEFT, expand=True, fill=X)
    spriteSelectButton.pack(side=LEFT)

    oofDialogFrame = Frame(romOptionsFrame)
    oofDialogFrame.grid(row=1, column=1)
    baseOofLabel = Label(oofDialogFrame, text='"OOF" Sound:')

    vars.oofNameVar = StringVar()
    vars.oof = adjuster_settings.oof

    def set_oof(oof_param):
        nonlocal vars
        if isinstance(oof_param, str) and os.path.isfile(oof_param) and os.path.getsize(oof_param) <= 2673:
            vars.oof = oof_param
            vars.oofNameVar.set(oof_param.rsplit('/',1)[-1])
        else:
            vars.oof = None
            vars.oofNameVar.set('(unchanged)')

    set_oof(adjuster_settings.oof)
    oofEntry = Label(oofDialogFrame, textvariable=vars.oofNameVar)

    def OofSelect():
        nonlocal vars
        oof_file = filedialog.askopenfilename(
            filetypes=[("BRR files", ".brr"),
                       ("All Files", "*")])
        try:
            set_oof(oof_file)
        except Exception:
            set_oof(None)

    oofSelectButton = Button(oofDialogFrame, text='...', command=OofSelect)
    AttachTooltip(oofSelectButton,
                  text="Select a .brr file no more than 2673 bytes.\n" + \
                  "This can be created from a <=0.394s 16-bit signed PCM .wav file at 12khz using snesbrr.")

    baseOofLabel.pack(side=LEFT)
    oofEntry.pack(side=LEFT)
    oofSelectButton.pack(side=LEFT)

    vars.quickSwapVar = IntVar(value=adjuster_settings.quickswap)
    quickSwapCheckbutton = Checkbutton(romOptionsFrame, text="L/R Quickswapping", variable=vars.quickSwapVar)
    quickSwapCheckbutton.grid(row=1, column=0, sticky=E)

    menuspeedFrame = Frame(romOptionsFrame)
    menuspeedFrame.grid(row=6, column=1, sticky=E)
    menuspeedLabel = Label(menuspeedFrame, text='Menu speed')
    menuspeedLabel.pack(side=LEFT)
    vars.menuspeedVar = StringVar()
    vars.menuspeedVar.set(adjuster_settings.menuspeed)
    menuspeedOptionMenu = OptionMenu(menuspeedFrame, vars.menuspeedVar, 'normal', 'instant', 'double', 'triple',
                                     'quadruple', 'half')
    menuspeedOptionMenu.pack(side=LEFT)

    heartcolorFrame = Frame(romOptionsFrame)
    heartcolorFrame.grid(row=2, column=0, sticky=E)
    heartcolorLabel = Label(heartcolorFrame, text='Heart color')
    heartcolorLabel.pack(side=LEFT)
    vars.heartcolorVar = StringVar()
    vars.heartcolorVar.set(adjuster_settings.heartcolor)
    heartcolorOptionMenu = OptionMenu(heartcolorFrame, vars.heartcolorVar, 'red', 'blue', 'green', 'yellow', 'random')
    heartcolorOptionMenu.pack(side=LEFT)

    heartbeepFrame = Frame(romOptionsFrame)
    heartbeepFrame.grid(row=2, column=1, sticky=E)
    heartbeepLabel = Label(heartbeepFrame, text='Heartbeep')
    heartbeepLabel.pack(side=LEFT)
    vars.heartbeepVar = StringVar()
    vars.heartbeepVar.set(adjuster_settings.heartbeep)
    heartbeepOptionMenu = OptionMenu(heartbeepFrame, vars.heartbeepVar, 'double', 'normal', 'half', 'quarter', 'off')
    heartbeepOptionMenu.pack(side=LEFT)

    owPalettesFrame = Frame(romOptionsFrame)
    owPalettesFrame.grid(row=3, column=0, sticky=E)
    owPalettesLabel = Label(owPalettesFrame, text='Overworld palettes')
    owPalettesLabel.pack(side=LEFT)
    vars.owPalettesVar = StringVar()
    vars.owPalettesVar.set(adjuster_settings.ow_palettes)
    owPalettesOptionMenu = OptionMenu(owPalettesFrame, vars.owPalettesVar, 'default', 'good', 'blackout', 'grayscale',
                                      'negative', 'classic', 'dizzy', 'sick', 'puke')
    owPalettesOptionMenu.pack(side=LEFT)

    uwPalettesFrame = Frame(romOptionsFrame)
    uwPalettesFrame.grid(row=3, column=1, sticky=E)
    uwPalettesLabel = Label(uwPalettesFrame, text='Dungeon palettes')
    uwPalettesLabel.pack(side=LEFT)
    vars.uwPalettesVar = StringVar()
    vars.uwPalettesVar.set(adjuster_settings.uw_palettes)
    uwPalettesOptionMenu = OptionMenu(uwPalettesFrame, vars.uwPalettesVar, 'default', 'good', 'blackout', 'grayscale',
                                      'negative', 'classic', 'dizzy', 'sick', 'puke')
    uwPalettesOptionMenu.pack(side=LEFT)

    hudPalettesFrame = Frame(romOptionsFrame)
    hudPalettesFrame.grid(row=4, column=0, sticky=E)
    hudPalettesLabel = Label(hudPalettesFrame, text='HUD palettes')
    hudPalettesLabel.pack(side=LEFT)
    vars.hudPalettesVar = StringVar()
    vars.hudPalettesVar.set(adjuster_settings.hud_palettes)
    hudPalettesOptionMenu = OptionMenu(hudPalettesFrame, vars.hudPalettesVar, 'default', 'good', 'blackout',
                                       'grayscale', 'negative', 'classic', 'dizzy', 'sick', 'puke')
    hudPalettesOptionMenu.pack(side=LEFT)

    swordPalettesFrame = Frame(romOptionsFrame)
    swordPalettesFrame.grid(row=4, column=1, sticky=E)
    swordPalettesLabel = Label(swordPalettesFrame, text='Sword palettes')
    swordPalettesLabel.pack(side=LEFT)
    vars.swordPalettesVar = StringVar()
    vars.swordPalettesVar.set(adjuster_settings.sword_palettes)
    swordPalettesOptionMenu = OptionMenu(swordPalettesFrame, vars.swordPalettesVar, 'default', 'good', 'blackout',
                                         'grayscale', 'negative', 'classic', 'dizzy', 'sick', 'puke')
    swordPalettesOptionMenu.pack(side=LEFT)

    shieldPalettesFrame = Frame(romOptionsFrame)
    shieldPalettesFrame.grid(row=5, column=0, sticky=E)
    shieldPalettesLabel = Label(shieldPalettesFrame, text='Shield palettes')
    shieldPalettesLabel.pack(side=LEFT)
    vars.shieldPalettesVar = StringVar()
    vars.shieldPalettesVar.set(adjuster_settings.shield_palettes)
    shieldPalettesOptionMenu = OptionMenu(shieldPalettesFrame, vars.shieldPalettesVar, 'default', 'good', 'blackout',
                                          'grayscale', 'negative', 'classic', 'dizzy', 'sick', 'puke')
    shieldPalettesOptionMenu.pack(side=LEFT)

    spritePoolFrame = Frame(romOptionsFrame)
    spritePoolFrame.grid(row=5, column=1)
    baseSpritePoolLabel = Label(spritePoolFrame, text='Sprite Pool:')

    vars.spritePoolCountVar = StringVar()
    vars.sprite_pool = adjuster_settings.sprite_pool

    def set_sprite_pool(sprite_param):
        nonlocal vars
        operation = "add"
        if isinstance(sprite_param, tuple):
            operation, sprite_param = sprite_param
        if isinstance(sprite_param, Sprite) and sprite_param.valid:
            sprite_param = sprite_param.name
        if isinstance(sprite_param, str):
            if operation == "add":
                vars.sprite_pool.append(sprite_param)
            elif operation == "remove":
                vars.sprite_pool.remove(sprite_param)
            elif operation == "clear":
                vars.sprite_pool.clear()
        vars.spritePoolCountVar.set(str(len(vars.sprite_pool)))

    set_sprite_pool(None)
    vars.spritePoolCountVar.set(len(adjuster_settings.sprite_pool))
    spritePoolEntry = Label(spritePoolFrame, textvariable=vars.spritePoolCountVar)

    def SpritePoolSelect():
        nonlocal vars
        SpriteSelector(parent, set_sprite_pool, randomOnEvent=False, spritePool=vars.sprite_pool)

    def SpritePoolClear():
        nonlocal vars
        vars.sprite_pool.clear()
        vars.spritePoolCountVar.set('0')

    spritePoolSelectButton = Button(spritePoolFrame, text='...', command=SpritePoolSelect)
    spritePoolClearButton = Button(spritePoolFrame, text='Clear', command=SpritePoolClear)

    baseSpritePoolLabel.pack(side=LEFT)
    spritePoolEntry.pack(side=LEFT)
    spritePoolSelectButton.pack(side=LEFT)
    spritePoolClearButton.pack(side=LEFT)

    vars.auto_apply = StringVar(value=adjuster_settings.auto_apply)
    autoApplyFrame = Frame(romOptionsFrame)
    autoApplyFrame.grid(row=9, column=0, columnspan=2, sticky=W)
    filler = Label(autoApplyFrame, text="Automatically apply last used settings on opening .aplttp files")
    filler.pack(side=TOP, expand=True, fill=X)
    askRadio = Radiobutton(autoApplyFrame, text='Ask', variable=vars.auto_apply, value='ask')
    askRadio.pack(side=LEFT, padx=5, pady=5)
    alwaysRadio = Radiobutton(autoApplyFrame, text='Always', variable=vars.auto_apply, value='always')
    alwaysRadio.pack(side=LEFT, padx=5, pady=5)
    neverRadio = Radiobutton(autoApplyFrame, text='Never', variable=vars.auto_apply, value='never')
    neverRadio.pack(side=LEFT, padx=5, pady=5)

    return romOptionsFrame, vars, set_sprite


class SpriteSelector():
    def __init__(self, parent, callback, adjuster=False, randomOnEvent=True, spritePool=None):
        self.deploy_icons()
        self.parent = parent
        self.window = Toplevel(parent)
        self.callback = callback
        self.adjuster = adjuster
        self.randomOnEvent = randomOnEvent
        self.spritePoolButtons = None

        self.window.wm_title("TAKE ANY ONE YOU WANT")
        self.window['padx'] = 5
        self.window['pady'] = 5
        self.spritesPerRow = 32
        self.all_sprites = []
        self.invalid_sprites = []
        self.sprite_pool = spritePool

        def open_custom_sprite_dir(_evt):
            open_file(self.custom_sprite_dir)

        remote_frametitle = Label(self.window, text='Remote Sprites')

        custom_frametitle = Frame(self.window)
        title_text = Label(custom_frametitle, text="Custom Sprites")
        title_link = Label(custom_frametitle, text="(open)", fg="blue", cursor="hand2")
        title_text.pack(side=LEFT)
        title_link.pack(side=LEFT)
        title_link.bind("<Button-1>", open_custom_sprite_dir)

        self.icon_section(remote_frametitle, self.remote_sprite_dir,
                          'Remote sprites not found. Click "Update remote sprites" to download them.')
        self.icon_section(custom_frametitle, self.custom_sprite_dir,
                          'Put sprites in the custom sprites folder (see open link above) to have them appear here.')
        if not randomOnEvent:
            self.sprite_pool_section(spritePool)

        frame = Frame(self.window)
        frame.pack(side=BOTTOM, fill=X, pady=5)

        if self.randomOnEvent:
            button = Button(frame, text="Browse for file...", command=self.browse_for_sprite)
            button.pack(side=RIGHT, padx=(5, 0))

        button = Button(frame, text="Update remote sprites", command=self.update_remote_sprites)
        button.pack(side=RIGHT, padx=(5, 0))

        repository_label = Label(frame, text='Sprite Repository:')
        self.repository_url = StringVar(frame, "https://alttpr.com/sprites")
        repository_entry = Entry(frame, textvariable=self.repository_url)
        
        repository_entry.pack(side=RIGHT, expand=True, fill=BOTH, pady=1)
        repository_label.pack(side=RIGHT, expand=False, padx=(0, 5))

        button = Button(frame, text="Do not adjust sprite",command=self.use_default_sprite)
        button.pack(side=LEFT, padx=(0, 5))

        button = Button(frame, text="Default Link sprite", command=self.use_default_link_sprite)
        button.pack(side=LEFT, padx=(0, 5))

        self.randomButtonText = StringVar()
        button = Button(frame, textvariable=self.randomButtonText, command=self.use_random_sprite)
        button.pack(side=LEFT, padx=(0, 5))
        self.randomButtonText.set("Random")

        self.randomOnEventText = StringVar()
        self.randomOnHitVar = IntVar()
        self.randomOnEnterVar = IntVar()
        self.randomOnExitVar = IntVar()
        self.randomOnSlashVar = IntVar()
        self.randomOnItemVar = IntVar()
        self.randomOnBonkVar = IntVar()
        self.randomOnRandomVar = IntVar()
        self.randomOnAllVar = IntVar()

        if self.randomOnEvent:
            self.buttonHit = Checkbutton(frame, text="Hit", command=self.update_random_button, variable=self.randomOnHitVar)
            self.buttonHit.pack(side=LEFT, padx=(0, 5))

            self.buttonEnter = Checkbutton(frame, text="Enter", command=self.update_random_button, variable=self.randomOnEnterVar)
            self.buttonEnter.pack(side=LEFT, padx=(0, 5))

            self.buttonExit = Checkbutton(frame, text="Exit", command=self.update_random_button, variable=self.randomOnExitVar)
            self.buttonExit.pack(side=LEFT, padx=(0, 5))

            self.buttonSlash = Checkbutton(frame, text="Slash", command=self.update_random_button, variable=self.randomOnSlashVar)
            self.buttonSlash.pack(side=LEFT, padx=(0, 5))

            self.buttonItem = Checkbutton(frame, text="Item", command=self.update_random_button, variable=self.randomOnItemVar)
            self.buttonItem.pack(side=LEFT, padx=(0, 5))

            self.buttonBonk = Checkbutton(frame, text="Bonk", command=self.update_random_button, variable=self.randomOnBonkVar)
            self.buttonBonk.pack(side=LEFT, padx=(0, 5))

            self.buttonRandom = Checkbutton(frame, text="Random", command=self.update_random_button, variable=self.randomOnRandomVar)
            self.buttonRandom.pack(side=LEFT, padx=(0, 5))

            self.buttonAll = Checkbutton(frame, text="All", command=self.update_random_button, variable=self.randomOnAllVar)
            self.buttonAll.pack(side=LEFT, padx=(0, 5))

        set_icon(self.window)
        self.window.focus()
        tkinter_center_window(self.window)

        if self.invalid_sprites:
            invalid = sorted(self.invalid_sprites)
            logging.warning(f"The following sprites are invalid: {', '.join(invalid)}")
            msg = f"{invalid[0]} "
            msg += f"and {len(invalid)-1} more are invalid" if len(invalid) > 1 else "is invalid"
            messagebox.showerror("Invalid sprites detected", msg, parent=self.window)

    def remove_from_sprite_pool(self, button, spritename):
        self.callback(("remove", spritename))
        self.spritePoolButtons.buttons.remove(button)
        button.destroy()

    def add_to_sprite_pool(self, spritename):
        if isinstance(spritename, str):
            if spritename == "random":
                button = Button(self.spritePoolButtons, text="?")
                button['font'] = font.Font(size=19)
                button.configure(command=lambda spr="random": self.remove_from_sprite_pool(button, spr))
                ToolTips.register(button, "Random")
                self.spritePoolButtons.buttons.append(button)
            else:
                spritename = Sprite.get_sprite_from_name(spritename)
        if isinstance(spritename, Sprite) and spritename.valid:
            image = get_image_for_sprite(spritename)
            if image is None:
                return
            button = Button(self.spritePoolButtons, image=image)
            button.configure(command=lambda spr=spritename: self.remove_from_sprite_pool(button, spr.name))
            ToolTips.register(button, spritename.name +
                              f"\nBy: {spritename.author_name if spritename.author_name else ''}")
            button.image = image

            self.spritePoolButtons.buttons.append(button)
        self.grid_fill_sprites(self.spritePoolButtons)

    def sprite_pool_section(self, spritePool):
        def clear_sprite_pool(_evt):
            self.callback(("clear", "Clear"))
            for button in self.spritePoolButtons.buttons:
                button.destroy()
            self.spritePoolButtons.buttons.clear()

        frametitle = Frame(self.window)
        title_text = Label(frametitle, text="Sprite Pool")
        title_link = Label(frametitle, text="(clear)", fg="blue", cursor="hand2")
        title_text.pack(side=LEFT)
        title_link.pack(side=LEFT)
        title_link.bind("<Button-1>", clear_sprite_pool)

        self.spritePoolButtons = LabelFrame(self.window, labelwidget=frametitle, padx=5, pady=5)
        self.spritePoolButtons.pack(side=TOP, fill=X)
        self.spritePoolButtons.buttons = []

        def update_sprites(event):
            self.spritesPerRow = (event.width - 10) // 38
            self.grid_fill_sprites(self.spritePoolButtons)

        self.grid_fill_sprites(self.spritePoolButtons)
        self.spritePoolButtons.bind("<Configure>", update_sprites)

        if spritePool:
            for sprite in spritePool:
                self.add_to_sprite_pool(sprite)

    def icon_section(self, frame_label, path, no_results_label):
        os.makedirs(path, exist_ok=True)
        frame = LabelFrame(self.window, labelwidget=frame_label, padx=5, pady=5)
        frame.pack(side=TOP, fill=X)

        sprites = []

        for file in os.listdir(path):
            if file == '.gitignore':
                continue
            sprite = Sprite(os.path.join(path, file))
            if sprite.valid:
                sprites.append((file, sprite))
            else:
                self.invalid_sprites.append(file)

        sprites.sort(key=lambda s: str.lower(s[1].name or "").strip())

        frame.buttons = []
        for file, sprite in sprites:
            image = get_image_for_sprite(sprite)
            if image is None:
                continue
            self.all_sprites.append(sprite)
            button = Button(frame, image=image, command=lambda spr=sprite: self.select_sprite(spr))
            ToolTips.register(button, sprite.name +
                              ("\nBy: %s" % sprite.author_name if sprite.author_name else "") +
                              f"\nFrom: {file}")
            button.image = image
            frame.buttons.append(button)

        if not frame.buttons:
            label = Label(frame, text=no_results_label)
            label.pack()

        def update_sprites(event):
            self.spritesPerRow = (event.width - 10) // 38
            self.grid_fill_sprites(frame)

        self.grid_fill_sprites(frame)

        frame.bind("<Configure>", update_sprites)

    def grid_fill_sprites(self, frame):
        for i, button in enumerate(frame.buttons):
            button.grid(row=i // self.spritesPerRow, column=i % self.spritesPerRow)

    def update_remote_sprites(self):
        # need to wrap in try catch. We don't want errors getting the json or downloading the files to break us.
        self.window.destroy()
        self.parent.update()

        def on_finish(successful, resultmessage):
            if successful:
                messagebox.showinfo("Sprite Updater", resultmessage)
            else:
                logging.error(resultmessage)
                messagebox.showerror("Sprite Updater", resultmessage)
            SpriteSelector(self.parent, self.callback, self.adjuster)

        BackgroundTaskProgress(self.parent, update_sprites, "Updating Sprites",
                               on_finish, self.repository_url.get())

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
        if self.randomOnEvent:
            self.callback(Sprite.default_link_sprite())
            self.window.destroy()
        else:
            self.callback("link")
            self.add_to_sprite_pool("link")

    def update_random_button(self):
        if self.randomOnAllVar.get():
            randomon = "all"
            self.buttonHit.config(state=DISABLED)
            self.buttonEnter.config(state=DISABLED)
            self.buttonExit.config(state=DISABLED)
            self.buttonSlash.config(state=DISABLED)
            self.buttonItem.config(state=DISABLED)
            self.buttonBonk.config(state=DISABLED)
            self.buttonRandom.config(state=DISABLED)
        elif self.randomOnRandomVar.get():
            randomon = "random"
            self.buttonHit.config(state=DISABLED)
            self.buttonEnter.config(state=DISABLED)
            self.buttonExit.config(state=DISABLED)
            self.buttonSlash.config(state=DISABLED)
            self.buttonItem.config(state=DISABLED)
            self.buttonBonk.config(state=DISABLED)
        else:
            self.buttonHit.config(state=NORMAL)
            self.buttonEnter.config(state=NORMAL)
            self.buttonExit.config(state=NORMAL)
            self.buttonSlash.config(state=NORMAL)
            self.buttonItem.config(state=NORMAL)
            self.buttonBonk.config(state=NORMAL)
            self.buttonRandom.config(state=NORMAL)
            randomon = "-hit" if self.randomOnHitVar.get() else ""
            randomon += "-enter" if self.randomOnEnterVar.get() else ""
            randomon += "-exit" if self.randomOnExitVar.get() else ""
            randomon += "-slash" if self.randomOnSlashVar.get() else ""
            randomon += "-item" if self.randomOnItemVar.get() else ""
            randomon += "-bonk" if self.randomOnBonkVar.get() else ""

        self.randomOnEventText.set(f"randomon{randomon}" if randomon else None)
        self.randomButtonText.set("Random On Event" if randomon else "Random")

    def use_random_sprite(self):
        if not self.randomOnEvent:
            self.callback("random")
            self.add_to_sprite_pool("random")
            return
        elif self.randomOnEventText.get():
            self.callback(self.randomOnEventText.get())
        elif self.sprite_pool:
            self.callback(random.choice(self.sprite_pool))
        elif self.all_sprites:
            self.callback(random.choice(self.all_sprites))
        else:
            self.callback(None)
        self.window.destroy()

    def select_sprite(self, spritename):
        self.callback(spritename)
        if self.randomOnEvent:
            self.window.destroy()
        else:
            self.add_to_sprite_pool(spritename)

    def deploy_icons(self):
        if not os.path.exists(self.custom_sprite_dir):
            os.makedirs(self.custom_sprite_dir)

    @property
    def remote_sprite_dir(self):
        return user_path("data", "sprites", "alttp", "remote")

    @property
    def custom_sprite_dir(self):
        return user_path("data", "sprites", "alttp", "custom")


def get_image_for_sprite(sprite, gif_only: bool = False):
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
        gif_lsd[
            4] = 0xF4  # 32 color palette follows.  transparant + 15 for sprite + 1 for shadow=17 which rounds up to 32 as nearest power of 2
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

        gif_img_minimum_code_size = bytes(
            [7])  # we choose 7 bits, so that each pixel is represented by a byte, for conviennce.

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
    if gif_only:
        return gif_data

    image = PhotoImage(data=gif_data)

    return image.zoom(2)


class ToolTips(object):
    # This class derived from wckToolTips which is available under the following license:

    # Copyright (c) 1998-2007 by Secret Labs AB
    # Copyright (c) 1998-2007 by Fredrik Lundh
    #
    # By obtaining, using, and/or copying this software and/or its
    # associated documentation, you agree that you have read, understood,
    # and will comply with the following terms and conditions:
    #
    # Permission to use, copy, modify, and distribute this software and its
    # associated documentation for any purpose and without fee is hereby
    # granted, provided that the above copyright notice appears in all
    # copies, and that both that copyright notice and this permission notice
    # appear in supporting documentation, and that the name of Secret Labs
    # AB or the author not be used in advertising or publicity pertaining to
    # distribution of the software without specific, written prior
    # permission.
    #
    # SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO
    # THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
    # FITNESS.  IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR BE LIABLE FOR
    # ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    # WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    # ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
    # OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

    label = None
    window = None
    active = 0
    tag = None
    after_id = None

    @classmethod
    def getcontroller(cls, widget):
        if cls.tag is None:

            cls.tag = "ui_tooltip_%d" % id(cls)
            widget.bind_class(cls.tag, "<Enter>", cls.enter)
            widget.bind_class(cls.tag, "<Leave>", cls.leave)
            widget.bind_class(cls.tag, "<Motion>", cls.motion)
            widget.bind_class(cls.tag, "<Destroy>", cls.leave)

            # pick suitable colors for tooltips
            try:
                cls.bg = "systeminfobackground"
                cls.fg = "systeminfotext"
                widget.winfo_rgb(cls.fg)  # make sure system colors exist
                widget.winfo_rgb(cls.bg)
            except Exception:
                cls.bg = "#ffffe0"
                cls.fg = "black"

        return cls.tag

    @classmethod
    def register(cls, widget, text):
        widget.ui_tooltip_text = text
        tags = list(widget.bindtags())
        tags.append(cls.getcontroller(widget))
        widget.bindtags(tuple(tags))

    @classmethod
    def unregister(cls, widget):
        tags = list(widget.bindtags())
        tags.remove(cls.getcontroller(widget))
        widget.bindtags(tuple(tags))

    # event handlers
    @classmethod
    def enter(cls, event):
        widget = event.widget
        if not cls.label:
            # create and hide balloon help window
            cls.popup = tk.Toplevel(bg=cls.fg, bd=1)
            cls.popup.overrideredirect(1)
            cls.popup.withdraw()
            cls.label = tk.Label(
                cls.popup, fg=cls.fg, bg=cls.bg, bd=0, padx=2, justify=tk.LEFT
            )
            cls.label.pack()
            cls.active = 0
        cls.xy = event.x_root + 16, event.y_root + 10
        cls.event_xy = event.x, event.y
        cls.after_id = widget.after(200, cls.display, widget)

    @classmethod
    def motion(cls, event):
        cls.xy = event.x_root + 16, event.y_root + 10
        cls.event_xy = event.x, event.y

    @classmethod
    def display(cls, widget):
        if not cls.active:
            # display balloon help window
            text = widget.ui_tooltip_text
            if callable(text):
                text = text(widget, cls.event_xy)
            cls.label.config(text=text)
            cls.popup.deiconify()
            cls.popup.lift()
            cls.popup.geometry("+%d+%d" % cls.xy)
            cls.active = 1
            cls.after_id = None

    @classmethod
    def leave(cls, event):
        widget = event.widget
        if cls.active:
            cls.popup.withdraw()
            cls.active = 0
        if cls.after_id:
            widget.after_cancel(cls.after_id)
            cls.after_id = None


if __name__ == '__main__':
    main()
