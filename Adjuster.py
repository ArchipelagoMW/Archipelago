#!/usr/bin/env python3
import argparse
import os
import logging
import textwrap
import sys
import time

from Rom import Sprite, LocalRom, apply_rom_settings
from Utils import output_path


class ArgumentDefaultsHelpFormatter(argparse.RawTextHelpFormatter):

    def _get_help_string(self, action):
        return textwrap.dedent(action.help)

def main():
    parser = argparse.ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('--rom', default='ER_base.sfc', help='Path to an ALttP rom to adjust.')
    parser.add_argument('--baserom', default='Zelda no Densetsu - Kamigami no Triforce (Japan).sfc',
                        help='Path to an ALttP JAP(1.0) rom to use as a base.')
    parser.add_argument('--loglevel', default='info', const='info', nargs='?', choices=['error', 'info', 'warning', 'debug'], help='Select level of logging for output.')
    parser.add_argument('--fastmenu', default='normal', const='normal', nargs='?', choices=['normal', 'instant', 'double', 'triple', 'quadruple', 'half'],
                        help='''\
                             Select the rate at which the menu opens and closes.
                             (default: %(default)s)
                             ''')
    parser.add_argument('--quickswap', help='Enable quick item swapping with L and R.', action='store_true')
    parser.add_argument('--disablemusic', help='Disables game music.', action='store_true')
    parser.add_argument('--enableflashing', help='Reenable flashing animations (unfriendly to epilepsy, always disabled in race roms)', action='store_false', dest="reduceflashing")
    parser.add_argument('--heartbeep', default='normal', const='normal', nargs='?', choices=['double', 'normal', 'half', 'quarter', 'off'],
                        help='''\
                             Select the rate at which the heart beep sound is played at
                             low health. (default: %(default)s)
                             ''')
    parser.add_argument('--heartcolor', default='red', const='red', nargs='?', choices=['red', 'blue', 'green', 'yellow', 'random'],
                        help='Select the color of Link\'s heart meter. (default: %(default)s)')
    parser.add_argument('--ow_palettes', default='default', choices=['default', 'random', 'blackout','puke','classic','grayscale','negative','dizzy','sick'])
    parser.add_argument('--link_palettes', default='default', choices=['default', 'random', 'blackout','puke','classic','grayscale','negative','dizzy','sick'])
    parser.add_argument('--shield_palettes', default='default', choices=['default', 'random', 'blackout','puke','classic','grayscale','negative','dizzy','sick'])
    parser.add_argument('--sword_palettes', default='default', choices=['default', 'random', 'blackout','puke','classic','grayscale','negative','dizzy','sick'])
    parser.add_argument('--hud_palettes', default='default', choices=['default', 'random', 'blackout','puke','classic','grayscale','negative','dizzy','sick'])
    parser.add_argument('--uw_palettes', default='default', choices=['default', 'random', 'blackout','puke','classic','grayscale','negative','dizzy','sick'])
    parser.add_argument('--sprite', help='''\
                             Path to a sprite sheet to use for Link. Needs to be in
                             binary format and have a length of 0x7000 (28672) bytes,
                             or 0x7078 (28792) bytes including palette data.
                             Alternatively, can be a ALttP Rom patched with a Link
                             sprite that will be extracted.
                             ''')
    parser.add_argument('--names', default='', type=str)
    args = parser.parse_args()

    # set up logger
    loglevel = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}[
        args.loglevel]
    logging.basicConfig(format='%(message)s', level=loglevel)

    if not os.path.isfile(args.rom):
        adjustGUI()
    else:
        if args.sprite is not None and not os.path.isfile(args.sprite) and not Sprite.get_sprite_from_name(args.sprite):
            input('Could not find link sprite sheet at given location. \nPress Enter to exit.')
            sys.exit(1)

        args, path = adjust(args=args)
        from Utils import persistent_store
        if isinstance(args.sprite, Sprite):
            args.sprite = args.sprite.name
        persistent_store("adjuster", "last_settings_3", args)


def adjust(args):
    start = time.perf_counter()
    logger = logging.getLogger('Adjuster')
    logger.info('Patching ROM.')
    vanillaRom = args.baserom
    if os.path.splitext(args.rom)[-1].lower() == '.bmbp':
        import Patch
        meta, args.rom = Patch.create_rom_file(args.rom)

    if os.stat(args.rom).st_size in (0x200000, 0x400000) and os.path.splitext(args.rom)[-1].lower() == '.sfc':
        rom = LocalRom(args.rom, patch=False, vanillaRom=vanillaRom)
    else:
        raise RuntimeError(
            'Provided Rom is not a valid Link to the Past Randomizer Rom. Please provide one for adjusting.')
    palettes_options={}
    palettes_options['dungeon']=args.uw_palettes

    palettes_options['overworld']=args.ow_palettes
    palettes_options['hud']=args.hud_palettes
    palettes_options['sword']=args.sword_palettes
    palettes_options['shield']=args.shield_palettes
    # palettes_options['link']=args.link_palettesvera
    racerom = rom.read_byte(0x180213) > 0

    apply_rom_settings(rom, args.heartbeep, args.heartcolor, args.quickswap, args.fastmenu, args.disablemusic,
                       args.sprite, palettes_options, reduceflashing=args.reduceflashing or racerom)
    path = output_path(f'{os.path.basename(args.rom)[:-4]}_adjusted.sfc')
    rom.write_to_file(path)

    logger.info('Done. Enjoy.')
    logger.debug('Total Time: %s', time.perf_counter() - start)

    return args, path

def adjustGUI():
    from tkinter import Checkbutton, OptionMenu, Toplevel, LabelFrame, PhotoImage, Tk, LEFT, RIGHT, BOTTOM, TOP, \
        StringVar, IntVar, Frame, Label, W, E, X, BOTH, Entry, Spinbox, Button, filedialog, messagebox, ttk
    from Gui import get_rom_options_frame, get_rom_frame
    from GuiUtils import set_icon
    from argparse import Namespace
    from Main import __version__ as MWVersion
    adjustWindow = Tk()
    adjustWindow.wm_title("Berserker's Multiworld %s LttP Adjuster" % MWVersion)
    set_icon(adjustWindow)

    rom_options_frame, rom_vars, set_sprite = get_rom_options_frame(adjustWindow)

    bottomFrame2 = Frame(adjustWindow)

    romFrame, romVar = get_rom_frame(adjustWindow)

    romDialogFrame = Frame(adjustWindow)
    baseRomLabel2 = Label(romDialogFrame, text='Rom to adjust')
    romVar2 = StringVar()
    romEntry2 = Entry(romDialogFrame, textvariable=romVar2)

    def RomSelect2():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".sfc", ".smc", ".bmbp")), ("All Files", "*")])
        romVar2.set(rom)
    romSelectButton2 = Button(romDialogFrame, text='Select Rom', command=RomSelect2)
    romDialogFrame.pack(side=TOP, expand=True, fill=X)
    baseRomLabel2.pack(side=LEFT)
    romEntry2.pack(side=LEFT, expand=True, fill=X)
    romSelectButton2.pack(side=LEFT)

    def adjustRom():
        guiargs = Namespace()
        guiargs.heartbeep = rom_vars.heartbeepVar.get()
        guiargs.heartcolor = rom_vars.heartcolorVar.get()
        guiargs.fastmenu = rom_vars.fastMenuVar.get()
        guiargs.ow_palettes = rom_vars.owPalettesVar.get()
        guiargs.uw_palettes = rom_vars.uwPalettesVar.get()
        guiargs.hud_palettes = rom_vars.hudPalettesVar.get()
        guiargs.sword_palettes = rom_vars.swordPalettesVar.get()
        guiargs.shield_palettes = rom_vars.shieldPalettesVar.get()
        guiargs.quickswap = bool(rom_vars.quickSwapVar.get())
        guiargs.disablemusic = bool(rom_vars.disableMusicVar.get())
        guiargs.reduceflashing = bool(rom_vars.disableFlashingVar.get())
        guiargs.rom = romVar2.get()
        guiargs.baserom = romVar.get()
        guiargs.sprite = rom_vars.sprite
        try:
            guiargs, path = adjust(args=guiargs)
        except Exception as e:
            logging.exception(e)
            messagebox.showerror(title="Error while adjusting Rom", message=str(e))
        else:
            messagebox.showinfo(title="Success", message="Rom patched successfully")
            from Utils import persistent_store
            from Rom import Sprite
            if isinstance(guiargs.sprite, Sprite):
                guiargs.sprite = guiargs.sprite.name
            persistent_store("adjuster", "last_settings_3", guiargs)

    adjustButton = Button(bottomFrame2, text='Adjust Rom', command=adjustRom)
    rom_options_frame.pack(side=TOP)
    adjustButton.pack(side=BOTTOM, padx=(5, 5))

    bottomFrame2.pack(side=BOTTOM, pady=(5, 5))

    adjustWindow.mainloop()


if __name__ == '__main__':
    main()