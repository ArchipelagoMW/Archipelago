import os
import re
import time
import logging

from Utils import output_path, parse_names_string
from Rom import LocalRom, Sprite, apply_rom_settings


def adjust(args):
    start = time.process_time()
    logger = logging.getLogger('')
    logger.info('Patching ROM.')

    if args.sprite is not None:
        if isinstance(args.sprite, Sprite):
            sprite = args.sprite
        else:
            sprite = Sprite(args.sprite)
    else:
        sprite = None

    outfilebase = os.path.basename(args.rom)[:-4] + '_adjusted'

    if os.stat(args.rom).st_size in (0x200000, 0x400000) and os.path.splitext(args.rom)[-1].lower() == '.sfc':
        rom = LocalRom(args.rom, False)
    else:
        raise RuntimeError('Provided Rom is not a valid Link to the Past Randomizer Rom. Please provide one for adjusting.')

    apply_rom_settings(rom, args.heartbeep, args.heartcolor, args.quickswap, args.fastmenu, args.disablemusic, sprite, parse_names_string(args.names))

    rom.write_to_file(output_path('%s.sfc' % outfilebase))

    logger.info('Done. Enjoy.')
    logger.debug('Total Time: %s', time.process_time() - start)

    return args
