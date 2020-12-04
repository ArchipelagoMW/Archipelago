import os
import time
import logging

from Utils import output_path
from Rom import LocalRom, apply_rom_settings


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
    palettes_options['link']=args.link_palettes
    
    apply_rom_settings(rom, args.heartbeep, args.heartcolor, args.quickswap, args.fastmenu, args.disablemusic,
                       args.sprite, palettes_options)
    path = output_path(f'{os.path.basename(args.rom)[:-4]}_adjusted.sfc')
    rom.write_to_file(path)

    logger.info('Done. Enjoy.')
    logger.debug('Total Time: %s', time.perf_counter() - start)

    return args, path
