import os
import time
import logging

from Utils import output_path
from Rom import LocalRom, apply_rom_settings


def adjust(args):
    start = time.perf_counter()
    logger = logging.getLogger('Adjuster')
    logger.info('Patching ROM.')

    if os.stat(args.rom).st_size in (0x200000, 0x400000) and os.path.splitext(args.rom)[-1].lower() == '.sfc':
        rom = LocalRom(args.rom, patch=False)
    else:
        raise RuntimeError(
            'Provided Rom is not a valid Link to the Past Randomizer Rom. Please provide one for adjusting.')

    apply_rom_settings(rom, args.heartbeep, args.heartcolor, args.quickswap, args.fastmenu, args.disablemusic,
                       args.sprite, args.ow_palettes, args.uw_palettes)
    path = output_path(f'{os.path.basename(args.rom)[:-4]}_adjusted.sfc')
    rom.write_to_file(path)

    logger.info('Done. Enjoy.')
    logger.debug('Total Time: %s', time.perf_counter() - start)

    return args, path
