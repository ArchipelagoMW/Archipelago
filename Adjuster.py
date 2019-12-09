#!/usr/bin/env python3
import argparse
import os
import logging
import textwrap
import sys

from AdjusterMain import adjust

class ArgumentDefaultsHelpFormatter(argparse.RawTextHelpFormatter):

    def _get_help_string(self, action):
        return textwrap.dedent(action.help)

def main():
    parser = argparse.ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('--rom', default='ER_base.sfc', help='Path to an ALttP JAP(1.0) rom to use as a base.')
    parser.add_argument('--loglevel', default='info', const='info', nargs='?', choices=['error', 'info', 'warning', 'debug'], help='Select level of logging for output.')
    parser.add_argument('--fastmenu', default='normal', const='normal', nargs='?', choices=['normal', 'instant', 'double', 'triple', 'quadruple', 'half'],
                        help='''\
                             Select the rate at which the menu opens and closes.
                             (default: %(default)s)
                             ''')
    parser.add_argument('--quickswap', help='Enable quick item swapping with L and R.', action='store_true')
    parser.add_argument('--disablemusic', help='Disables game music.', action='store_true')
    parser.add_argument('--heartbeep', default='normal', const='normal', nargs='?', choices=['double', 'normal', 'half', 'quarter', 'off'],
                        help='''\
                             Select the rate at which the heart beep sound is played at
                             low health. (default: %(default)s)
                             ''')
    parser.add_argument('--heartcolor', default='red', const='red', nargs='?', choices=['red', 'blue', 'green', 'yellow', 'random'],
                        help='Select the color of Link\'s heart meter. (default: %(default)s)')
    parser.add_argument('--sprite', help='''\
                             Path to a sprite sheet to use for Link. Needs to be in
                             binary format and have a length of 0x7000 (28672) bytes,
                             or 0x7078 (28792) bytes including palette data.
                             Alternatively, can be a ALttP Rom patched with a Link
                             sprite that will be extracted.
                             ''')
    parser.add_argument('--names', default='', type=str)
    args = parser.parse_args()

    # ToDo: Validate files further than mere existance
    if not os.path.isfile(args.rom):
        input('Could not find valid base rom for patching at expected path %s. Please run with -h to see help for further information. \nPress Enter to exit.' % args.rom)
        sys.exit(1)
    if args.sprite is not None and not os.path.isfile(args.sprite):
        input('Could not find link sprite sheet at given location. \nPress Enter to exit.' % args.sprite)
        sys.exit(1)

    # set up logger
    loglevel = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}[args.loglevel]
    logging.basicConfig(format='%(message)s', level=loglevel)

    adjust(args=args)

if __name__ == '__main__':
    main()
