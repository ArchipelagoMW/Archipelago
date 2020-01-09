#!/usr/bin/env python3
import argparse
import hashlib
import logging
import os
import random
import time
import sys

from BaseClasses import World
from Regions import create_regions
from EntranceShuffle import link_entrances, connect_entrance, connect_two_way, connect_exit
from Rom import patch_rom, LocalRom, write_string_to_rom, apply_rom_settings, get_sprite_from_name
from Rules import set_rules
from Dungeons import create_dungeons
from Items import ItemFactory
from ItemList import difficulties
from Main import create_playthrough

__version__ = '0.2-dev'

def main(args):
    start_time = time.process_time()

    # initialize the world
    world = World(1, 'vanilla', 'noglitches', 'standard', 'normal', 'none', 'on', 'ganon', 'freshness', False, False, False, False, False, False, None, False)
    logger = logging.getLogger('')

    hasher = hashlib.md5()
    with open(args.plando, 'rb') as plandofile:
        buf = plandofile.read()
        hasher.update(buf)
    world.seed = int(hasher.hexdigest(), 16) % 1000000000

    random.seed(world.seed)

    logger.info('ALttP Plandomizer Version %s  -  Seed: %s\n\n', __version__, args.plando)

    world.difficulty_requirements[1] = difficulties[world.difficulty[1]]

    create_regions(world, 1)
    create_dungeons(world, 1)

    link_entrances(world, 1)

    logger.info('Calculating Access Rules.')

    set_rules(world, 1)

    logger.info('Fill the world.')

    text_patches = []

    fill_world(world, args.plando, text_patches)

    if world.get_entrance('Dam', 1).connected_region.name != 'Dam' or world.get_entrance('Swamp Palace', 1).connected_region.name != 'Swamp Palace (Entrance)':
        world.swamp_patch_required[1] = True

    logger.info('Calculating playthrough.')

    try:
        create_playthrough(world)
    except RuntimeError:
        if args.ignore_unsolvable:
            pass
        else:
            raise

    logger.info('Patching ROM.')

    rom = LocalRom(args.rom)
    patch_rom(world, 1, rom, False)

    apply_rom_settings(rom, args.heartbeep, args.heartcolor, args.quickswap, args.fastmenu, args.disablemusic, args.sprite, args.ow_palettes, args.uw_palettes)

    for textname, texttype, text in text_patches:
        if texttype == 'text':
            write_string_to_rom(rom, textname, text)
        #elif texttype == 'credit':
        #    write_credits_string_to_rom(rom, textname, text)

    outfilebase = 'Plando_%s_%s' % (os.path.splitext(os.path.basename(args.plando))[0], world.seed)

    rom.write_to_file('%s.sfc' % outfilebase)
    if args.create_spoiler:
        world.spoiler.to_file('%s_Spoiler.txt' % outfilebase)

    logger.info('Done. Enjoy.')
    logger.debug('Total Time: %s', time.process_time() - start_time)

    return world


def fill_world(world, plando, text_patches):
    mm_medallion = 'Ether'
    tr_medallion = 'Quake'
    logger = logging.getLogger('')
    with open(plando, 'r') as plandofile:
        for line in plandofile.readlines():
            if line.startswith('#'):
                continue
            if ':' in line:
                line = line.lstrip()

                if line.startswith('!'):
                    if line.startswith('!mm_medallion'):
                        _, medallionstr = line.split(':', 1)
                        mm_medallion = medallionstr.strip()
                    elif line.startswith('!tr_medallion'):
                        _, medallionstr = line.split(':', 1)
                        tr_medallion = medallionstr.strip()
                    elif line.startswith('!mode'):
                        _, modestr = line.split(':', 1)
                        world.mode = {1: modestr.strip()}
                    elif line.startswith('!logic'):
                        _, logicstr = line.split(':', 1)
                        world.logic = {1: logicstr.strip()}
                    elif line.startswith('!goal'):
                        _, goalstr = line.split(':', 1)
                        world.goal = {1: goalstr.strip()}
                    elif line.startswith('!light_cone_sewers'):
                        _, sewerstr = line.split(':', 1)
                        world.sewer_light_cone = {1: sewerstr.strip().lower() == 'true'}
                    elif line.startswith('!light_cone_lw'):
                        _, lwconestr = line.split(':', 1)
                        world.light_world_light_cone = lwconestr.strip().lower() == 'true'
                    elif line.startswith('!light_cone_dw'):
                        _, dwconestr = line.split(':', 1)
                        world.dark_world_light_cone = dwconestr.strip().lower() == 'true'
                    elif line.startswith('!fix_trock_doors'):
                        _, trdstr = line.split(':', 1)
                        world.fix_trock_doors = {1: trdstr.strip().lower() == 'true'}
                    elif line.startswith('!fix_trock_exit'):
                        _, trfstr = line.split(':', 1)
                        world.fix_trock_exit = {1: trfstr.strip().lower() == 'true'}
                    elif line.startswith('!fix_gtower_exit'):
                        _, gtfstr = line.split(':', 1)
                        world.fix_gtower_exit = gtfstr.strip().lower() == 'true'
                    elif line.startswith('!fix_pod_exit'):
                        _, podestr = line.split(':', 1)
                        world.fix_palaceofdarkness_exit = {1: podestr.strip().lower() == 'true'}
                    elif line.startswith('!fix_skullwoods_exit'):
                        _, swestr = line.split(':', 1)
                        world.fix_skullwoods_exit = {1: swestr.strip().lower() == 'true'}
                    elif line.startswith('!check_beatable_only'):
                        _, chkbtstr = line.split(':', 1)
                        world.check_beatable_only = chkbtstr.strip().lower() == 'true'
                    elif line.startswith('!ganon_death_pyramid_respawn'):
                        _, gnpstr = line.split(':', 1)
                        world.ganon_at_pyramid = gnpstr.strip().lower() == 'true'
                    elif line.startswith('!save_quit_boss'):
                        _, sqbstr = line.split(':', 1)
                        world.save_and_quite_from_boss = sqbstr.strip().lower() == 'true'
                    elif line.startswith('!text_'):
                        textname, text = line.split(':', 1)
                        text_patches.append([textname.lstrip('!text_').strip(), 'text', text.strip()])
                    #temporarilly removed. New credits system not ready to handle this.
                    #elif line.startswith('!credits_'):
                    #    textname, text = line.split(':', 1)
                    #    text_patches.append([textname.lstrip('!credits_').strip(), 'credits', text.strip()])
                    continue

                locationstr, itemstr = line.split(':', 1)
                location = world.get_location(locationstr.strip(), 1)
                if location is None:
                    logger.warning('Unknown location: %s', locationstr)
                    continue
                else:
                    item = ItemFactory(itemstr.strip(), 1)
                    if item is not None:
                        world.push_item(location, item)
                    if item.smallkey or item.bigkey:
                        location.event = True
            elif '<=>' in line:
                entrance, exit = line.split('<=>', 1)
                connect_two_way(world, entrance.strip(), exit.strip(), 1)
            elif '=>' in line:
                entrance, exit = line.split('=>', 1)
                connect_entrance(world, entrance.strip(), exit.strip(), 1)
            elif '<=' in line:
                entrance, exit = line.split('<=', 1)
                connect_exit(world, exit.strip(), entrance.strip(), 1)

    world.required_medallions[1] = (mm_medallion, tr_medallion)

    # set up Agahnim Events
    world.get_location('Agahnim 1', 1).event = True
    world.get_location('Agahnim 1', 1).item = ItemFactory('Beat Agahnim 1', 1)
    world.get_location('Agahnim 2', 1).event = True
    world.get_location('Agahnim 2', 1).item = ItemFactory('Beat Agahnim 2', 1)


def start():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--create_spoiler', help='Output a Spoiler File', action='store_true')
    parser.add_argument('--ignore_unsolvable', help='Do not abort if seed is deemed unsolvable.', action='store_true')
    parser.add_argument('--rom', default='Zelda no Densetsu - Kamigami no Triforce (Japan).sfc', help='Path to an ALttP JAP(1.0) rom to use as a base.')
    parser.add_argument('--loglevel', default='info', const='info', nargs='?', choices=['error', 'info', 'warning', 'debug'], help='Select level of logging for output.')
    parser.add_argument('--seed', help='Define seed number to generate.', type=int)
    parser.add_argument('--fastmenu', default='normal', const='normal', nargs='?', choices=['normal', 'instant', 'double', 'triple', 'quadruple', 'half'],
                        help='''\
                             Select the rate at which the menu opens and closes.
                             (default: %(default)s)
                             ''')
    parser.add_argument('--quickswap', help='Enable quick item swapping with L and R.', action='store_true')
    parser.add_argument('--disablemusic', help='Disables game music.', action='store_true')
    parser.add_argument('--heartbeep', default='normal', const='normal', nargs='?', choices=['normal', 'half', 'quarter', 'off'],
                        help='Select the rate at which the heart beep sound is played at low health.')
    parser.add_argument('--heartcolor', default='red', const='red', nargs='?', choices=['red', 'blue', 'green', 'yellow'],
                        help='Select the color of Link\'s heart meter. (default: %(default)s)')
    parser.add_argument('--ow_palettes', default='default', choices=['default', 'random', 'blackout'])
    parser.add_argument('--uw_palettes', default='default', choices=['default', 'random', 'blackout'])
    parser.add_argument('--sprite', help='Path to a sprite sheet to use for Link. Needs to be in binary format and have a length of 0x7000 (28672) bytes.')
    parser.add_argument('--plando', help='Filled out template to use for setting up the rom.')
    args = parser.parse_args()

    # ToDo: Validate files further than mere existance
    if not os.path.isfile(args.rom):
        input('Could not find valid base rom for patching at expected path %s. Please run with -h to see help for further information. \nPress Enter to exit.' % args.rom)
        sys.exit(1)
    if not os.path.isfile(args.plando):
        input('Could not find Plandomizer distribution at expected path %s. Please run with -h to see help for further information. \nPress Enter to exit.' % args.plando)
        sys.exit(1)
    if args.sprite is not None and not os.path.isfile(args.sprite) and not get_sprite_from_name(args.sprite):
        input('Could not find link sprite sheet at given location. \nPress Enter to exit.')
        sys.exit(1)

    # set up logger
    loglevel = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}[args.loglevel]
    logging.basicConfig(format='%(message)s', level=loglevel)

    main(args=args)

if __name__ == '__main__':
    start()
