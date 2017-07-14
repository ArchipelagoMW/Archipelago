import argparse
import os
import logging
import random

from Main import main
from Gui import guiMain

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--create_spoiler', help='Output a Spoiler File', action='store_true')
    parser.add_argument('--logic', default='noglitches', const='noglitches', nargs='?', choices=['noglitches', 'minorglitches'],
                        help='Select Enforcement of Item Requirements. Minor Glitches may require Fake Flippers, Bunny Revival and Dark Room Navigation.')
    parser.add_argument('--mode', default='open', const='open', nargs='?', choices=['standard', 'open', 'swordless'],
                        help='Select game mode. Standard fixes Hyrule Castle Secret Entrance and Front Door, but may lead to weird rain state issues if you exit through the Hyrule Castle side exits before rescuing Zelda in a full shuffle.\n'
                             'Swordless mode is like open, but with no swords. Curtains in Skull Woods and Agahnims Tower are removed, Agahnims Tower barrier can be destroyed with hammer. Misery Mire and Turtle Rock can be opened without a sword.\n'
                             'Hammer damages Ganon. Ether and Bombos Tablet are unreachable but contain trash items always.')
    parser.add_argument('--goal', default='ganon', const='ganon', nargs='?', choices=['ganon', 'pedestal', 'dungeons', 'starhunt', 'triforcehunt'],
                        help='Select completion goal. Pedestal places the Triforce at the Master Sword Pedestal. All dungeons is not enforced ingame but considered in the playthrough. \n'
                             'Star Hunt places 15 Power Stars pieces in the world, collect 10 of them to beat the game.\n'
                             'Triforce Hunt places 3 Triforce Pieces in the world, collect them all to beat the game.')
    parser.add_argument('--difficulty', default='normal', const='normal', nargs='?', choices=['normal', 'timed', 'timed-ohko', 'timed-countdown'],
                        help='Select game difficulty. Affects available itempool.\n'
                             'Timed modes replace low value items with clocks, the overall rupee count in the pool stays roughly the same.\n'
                             'Timed starts with clock at zero. Green Clocks subtract 4 minutes (Total: 20), Blue Clocks subtract 2 minutes (Total: 10), Red Clocks add 2 minutes (Total: 10). Winner is player with lowest time at the end.\n'
                             'Timed OHKO starts clock at 10 minutes. Green Clocks add 5 minutes (Total: 25). As long as clock is at 0, Link will die in one hit.\n'
                             'Timed Countdown starts with clock at 40 minutes. Same clocks as Timed mode. If time runs out, you lose (but can still keep playing).')
    parser.add_argument('--algorithm', default='restrictive', const='restrictive', nargs='?', choices=['freshness', 'flood', 'vt21', 'vt22', 'restrictive'],
                        help='Select item filling algorithm. vt21 is unbiased in its selection, but has tendency to put Ice Rod in Turtle Rock.\n'
                             'vt22 drops off stale locations after 1/3 of progress items were placed to try to circumvent vt21\'s shortcomings.\n'
                             'freshness keeps track of stale locations (ones that cannot be reached yet) and decreases likeliness of selecting them the more often they were found unreachable.\n'
                             'flood pushes out items starting from Link\'s House and is slightly biased to placing progression items with less restrictions.\n'
                             'restrictive shuffles items and then places them in a random location that it is not impossible to be in.')
    parser.add_argument('--shuffle', default='full', const='full', nargs='?', choices=['vanilla', 'simple', 'restricted', 'full', 'madness', 'insanity', 'dungeonsfull', 'dungeonssimple'],
                        help='Select Entrance Shuffling Algorithm.\n'
                             'Simple shuffles Dungeon Entrances/Exits between each other and keeps all 4-entrance dungeons confined to one location. All caves outside of death mountain are shuffled in pairs.\n'
                             'Restricted uses Dungeons shuffling from Simple but freely connects remaining entrances.\n'
                             'Full mixes cave and dungeon entrances freely.\n'
                             'Madness decouples entrances and exits from each other and shuffles them freely, only ensuring that no fake Light/Dark World happens and all locations are reachable.\n'
                             'Insanity is Madness without the world restrictions. Mirror and Pearl are provided early to ensure Filling algorithm works properly. Deal with Fake LW/DW at your discretion. Experimental.\n'
                             'The dungeon variants only mix up dungeons and keep the rest of the overworld vanilla.')
    parser.add_argument('--rom', default='Zelda no Densetsu - Kamigami no Triforce (Japan).sfc', help='Path to an ALttP JAP(1.0) rom to use as a base.')
    parser.add_argument('--loglevel', default='info', const='info', nargs='?', choices=['error', 'info', 'warning', 'debug'], help='Select level of logging for output.')
    parser.add_argument('--seed', help='Define seed number to generate.', type=int)
    parser.add_argument('--count', help='Use to batch generate multiple seeds with same settings. If --seed is provided, it will be used for the first seed, then used to derive the next seed (i.e. generating 10 seeds with --seed given will produce the same 10 (different) roms each time).', type=int)
    parser.add_argument('--quickswap', help='Enable quick item swapping with L and R.', action='store_true')
    parser.add_argument('--nodungeonitems', help='Remove Maps and Compasses from Itempool, replacing them by empty slots.', action='store_true')
    parser.add_argument('--beatableonly', help='Only check if the game is beatable with placement. Do not ensure all locations are reachable. This only has an effect on the restrictive algorithm currently.', action='store_true')
    parser.add_argument('--heartbeep', default='normal', const='normal', nargs='?', choices=['normal', 'half', 'quarter', 'off'],
                        help='Select the rate at which the heart beep sound is played at low health.')
    parser.add_argument('--sprite', help='Path to a sprite sheet to use for Link. Needs to be in binary format and have a length of 0x7000 (28672) bytes.')
    parser.add_argument('--suppress_rom', help='Do not create an output rom file.', action='store_true')
    parser.add_argument('--gui', help='Launch the GUI', action='store_true')
    parser.add_argument('--jsonout', help='Output .json patch file instead of a patched rom. Used for VT site integration, do not use otherwise.')
    args = parser.parse_args()

    # ToDo: Validate files further than mere existance
    if not args.jsonout and not os.path.isfile(args.rom):
        input('Could not find valid base rom for patching at expected path %s. Please run with -h to see help for further information. \nPress Enter to exit.' % args.rom)
        exit(1)
    if args.sprite is not None and not os.path.isfile(args.rom):
        input('Could not find link sprite sheet at given location. \nPress Enter to exit.' % args.sprite)
        exit(1)

    # set up logger
    loglevel = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}[args.loglevel]
    logging.basicConfig(format='%(message)s', level=loglevel)

    if args.gui:
        guiMain(args)
    elif args.count is not None:
        seed = args.seed
        for i in range(args.count):
            main(seed=seed, args=args)
            seed = random.randint(0, 999999999)
    else:
        main(seed=args.seed, args=args)
