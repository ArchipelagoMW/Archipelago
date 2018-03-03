#!/usr/bin/env python3
import argparse
import os
import logging
import random
import textwrap
import sys

from Gui import guiMain
from Main import main
from Utils import is_bundled, close_console


class ArgumentDefaultsHelpFormatter(argparse.RawTextHelpFormatter):

    def _get_help_string(self, action):
        return textwrap.dedent(action.help)


def start():
    parser = argparse.ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--create_spoiler', help='Output a Spoiler File', action='store_true')
    parser.add_argument('--logic', default='noglitches', const='noglitches', nargs='?', choices=['noglitches', 'minorglitches'],
                        help='''\
                             Select Enforcement of Item Requirements. (default: %(default)s)
                             No Glitches:
                             Minor Glitches: May require Fake Flippers, Bunny Revival
                                             and Dark Room Navigation.
                             ''')
    parser.add_argument('--mode', default='open', const='open', nargs='?', choices=['standard', 'open', 'swordless'],
                        help='''\
                             Select game mode. (default: %(default)s)
                             Open:      World starts with Zelda rescued.
                             Standard:  Fixes Hyrule Castle Secret Entrance and Front Door
                                        but may lead to weird rain state issues if you exit
                                        through the Hyrule Castle side exits before rescuing
                                        Zelda in a full shuffle.
                             Swordless: Like Open, but with no swords. Curtains in
                                        Skull Woods and Agahnims Tower are removed,
                                        Agahnim\'s Tower barrier can be destroyed with
                                        hammer. Misery Mire and Turtle Rock can be opened
                                        without a sword. Hammer damages Ganon. Ether and
                                        Bombos Tablet can be activated with Hammer (and Book).
                             ''')
    parser.add_argument('--goal', default='ganon', const='ganon', nargs='?', choices=['ganon', 'pedestal', 'dungeons', 'triforcehunt', 'crystals'],
                        help='''\
                             Select completion goal. (default: %(default)s)
                             Ganon:         Collect all crystals, beat Agahnim 2 then
                                            defeat Ganon.
                             Crystals:      Collect all crystals then defeat Ganon.
                             Pedestal:      Places the Triforce at the Master Sword Pedestal.
                             All Dungeons:  Collect all crystals, pendants, beat both
                                            Agahnim fights and then defeat Ganon.
                             Triforce Hunt: Places 30 Triforce Pieces in the world, collect
                                            20 of them to beat the game.
                             ''')
    parser.add_argument('--difficulty', default='normal', const='normal', nargs='?', choices=['easy', 'normal', 'hard', 'expert', 'insane'],
                        help='''\
                             Select game difficulty. Affects available itempool. (default: %(default)s)
                             Easy:            An easy setting with extra equipment.
                             Normal:          Normal difficulty.
                             Hard:            A harder setting with less equipment and reduced health.
                             Expert:          A harder yet setting with minimum equipment and health.
                             Insane:          A setting with the absolute minimum in equipment and no extra health.
                             ''')
    parser.add_argument('--timer', default='none', const='normal', nargs='?', choices=['none', 'display', 'timed', 'timed-ohko', 'ohko', 'timed-countdown'],
                        help='''\
                             Select game timer setting. Affects available itempool. (default: %(default)s)
                             None:            No timer.
                             Display:         Displays a timer but does not affect
                                              the itempool.
                             Timed:           Starts with clock at zero. Green Clocks
                                              subtract 4 minutes (Total: 20), Blue Clocks
                                              subtract 2 minutes (Total: 10), Red Clocks add
                                              2 minutes (Total: 10). Winner is player with
                                              lowest time at the end.
                             Timed OHKO:      Starts clock at 10 minutes. Green Clocks add
                                              5 minutes (Total: 25). As long as clock is at 0,
                                              Link will die in one hit.
                             OHKO:            Like Timed OHKO, but no clock items are present
                                              and the clock is permenantly at zero.
                             Timed Countdown: Starts with clock at 40 minutes. Same clocks as
                                              Timed mode. If time runs out, you lose (but can
                                              still keep playing).
                             ''')
    parser.add_argument('--progressive', default='on', const='normal', nargs='?', choices=['on', 'off', 'random'],
                        help='''\
                             Select progressive equipment setting. Affects available itempool. (default: %(default)s)
                             On:              Swords, Shields, Armor, and Gloves will
                                              all be progressive equipment. Each subsequent
                                              item of the same type the player finds will
                                              upgrade that piece of equipment by one stage.
                             Off:             Swords, Shields, Armor, and Gloves will not
                                              be progressive equipment. Higher level items may
                                              be found at any time. Downgrades are not possible.
                             Random:          Swords, Shields, Armor, and Gloves will, per
                                              category, be randomly progressive or not.
                                              Link will die in one hit.
                             ''')
    parser.add_argument('--algorithm', default='balanced', const='balanced', nargs='?', choices=['freshness', 'flood', 'vt21', 'vt22', 'vt25', 'vt26', 'balanced'],
                        help='''\
                             Select item filling algorithm. (default: %(default)s
                             balanced:    vt26 derivitive that aims to strike a balance between
                                          the overworld heavy vt25 and the dungeon heavy vt26
                                          algorithm.
                             vt26:        Shuffle items and place them in a random location
                                          that it is not impossible to be in. This includes
                                          dungeon keys and items.
                             vt25:        Shuffle items and place them in a random location
                                          that it is not impossible to be in.
                             vt21:        Unbiased in its selection, but has tendency to put
                                          Ice Rod in Turtle Rock.
                             vt22:        Drops off stale locations after 1/3 of progress
                                          items were placed to try to circumvent vt21\'s
                                          shortcomings.
                             Freshness:   Keep track of stale locations (ones that cannot be
                                          reached yet) and decrease likeliness of selecting
                                          them the more often they were found unreachable.
                             Flood:       Push out items starting from Link\'s House and
                                          slightly biased to placing progression items with
                                          less restrictions.
                             ''')
    parser.add_argument('--shuffle', default='full', const='full', nargs='?', choices=['vanilla', 'simple', 'restricted', 'full', 'crossed', 'insanity', 'restricted_legacy', 'full_legacy', 'madness_legacy', 'insanity_legacy', 'dungeonsfull', 'dungeonssimple'],
                        help='''\
                             Select Entrance Shuffling Algorithm. (default: %(default)s)
                             Full:       Mix cave and dungeon entrances freely while limiting
                                         multi-entrance caves to one world.
                             Simple:     Shuffle Dungeon Entrances/Exits between each other
                                         and keep all 4-entrance dungeons confined to one
                                         location. All caves outside of death mountain are
                                         shuffled in pairs and matched by original type.
                             Restricted: Use Dungeons shuffling from Simple but freely
                                         connect remaining entrances.
                             Crossed:    Mix cave and dungeon entrances freely while allowing
                                         caves to cross between worlds.
                             Insanity:   Decouple entrances and exits from each other and
                                         shuffle them freely. Caves that used to be single
                                         entrance will still exit to the same location from
                                         which they are entered.
                             Vanilla:    All entrances are in the same locations they were
                                         in the base game.
                             Legacy shuffles preserve behavior from older versions of the
                             entrance randomizer including significant technical limitations.
                             The dungeon variants only mix up dungeons and keep the rest of
                             the overworld vanilla.
                             ''')
    parser.add_argument('--rom', default='Zelda no Densetsu - Kamigami no Triforce (Japan).sfc', help='Path to an ALttP JAP(1.0) rom to use as a base.')
    parser.add_argument('--loglevel', default='info', const='info', nargs='?', choices=['error', 'info', 'warning', 'debug'], help='Select level of logging for output.')
    parser.add_argument('--seed', help='Define seed number to generate.', type=int)
    parser.add_argument('--count', help='''\
                             Use to batch generate multiple seeds with same settings.
                             If --seed is provided, it will be used for the first seed, then
                             used to derive the next seed (i.e. generating 10 seeds with
                             --seed given will produce the same 10 (different) roms each
                             time).
                             ''', type=int)
    parser.add_argument('--fastmenu', default='normal', const='normal', nargs='?', choices=['normal', 'instant', 'double', 'triple', 'quadruple', 'half'],
                        help='''\
                             Select the rate at which the menu opens and closes.
                             (default: %(default)s)
                             ''')
    parser.add_argument('--quickswap', help='Enable quick item swapping with L and R.', action='store_true')
    parser.add_argument('--disablemusic', help='Disables game music.', action='store_true')
    parser.add_argument('--keysanity', help='''\
                             Keys (and other dungeon items) are no longer restricted to
                             their dungeons, but can be anywhere
                             ''', action='store_true')
    parser.add_argument('--custom', default=False, help='Not supported.')
    parser.add_argument('--customitemarray', default=False, help='Not supported.')
    parser.add_argument('--nodungeonitems', help='''\
                             Remove Maps and Compasses from Itempool, replacing them by
                             empty slots.
                             ''', action='store_true')
    parser.add_argument('--beatableonly', help='''\
                             Only check if the game is beatable with placement. Do not
                             ensure all locations are reachable. This only has an effect
                             on the restrictive algorithm currently.
                             ''', action='store_true')
    # included for backwards compatibility
    parser.add_argument('--shuffleganon', help=argparse.SUPPRESS, action='store_true', default=True)
    parser.add_argument('--no-shuffleganon', help='''\
                             If set, the Pyramid Hole and Ganon's Tower are not
                             included entrance shuffle pool.
                             ''', action='store_false', dest='shuffleganon')
    parser.add_argument('--heartbeep', default='normal', const='normal', nargs='?', choices=['normal', 'half', 'quarter', 'off'],
                        help='''\
                             Select the rate at which the heart beep sound is played at
                             low health. (default: %(default)s)
                             ''')
    parser.add_argument('--heartcolor', default='red', const='red', nargs='?', choices=['red', 'blue', 'green', 'yellow'],
                        help='Select the color of Link\'s heart meter. (default: %(default)s)')
    parser.add_argument('--sprite', help='''\
                             Path to a sprite sheet to use for Link. Needs to be in
                             binary format and have a length of 0x7000 (28672) bytes,
                             or 0x7078 (28792) bytes including palette data.
                             Alternatively, can be a ALttP Rom patched with a Link
                             sprite that will be extracted.
                             ''')
    parser.add_argument('--suppress_rom', help='Do not create an output rom file.', action='store_true')
    parser.add_argument('--gui', help='Launch the GUI', action='store_true')
    parser.add_argument('--jsonout', action='store_true', help='''\
                            Output .json patch to stdout instead of a patched rom. Used
                            for VT site integration, do not use otherwise.
                            ''')
    args = parser.parse_args()

    if is_bundled() and len(sys.argv) == 1:
        # for the bundled builds, if we have no arguments, the user
        # probably wants the gui. Users of the bundled build who want the command line
        # interface shouuld specify at least one option, possibly setting a value to a
        # default if they like all the defaults
        close_console()
        guiMain()
        sys.exit(0)

    # ToDo: Validate files further than mere existance
    if not args.jsonout and not os.path.isfile(args.rom):
        input('Could not find valid base rom for patching at expected path %s. Please run with -h to see help for further information. \nPress Enter to exit.' % args.rom)
        sys.exit(1)
    if args.sprite is not None and not os.path.isfile(args.sprite):
        if not args.jsonout:
            input('Could not find link sprite sheet at given location. \nPress Enter to exit.' % args.sprite)
            sys.exit(1)
        else:
            raise IOError('Cannot find sprite file at %s' % args.sprite)

    # set up logger
    loglevel = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}[args.loglevel]
    logging.basicConfig(format='%(message)s', level=loglevel)

    if args.gui:
        guiMain(args)
    elif args.count is not None:
        seed = args.seed
        for _ in range(args.count):
            main(seed=seed, args=args)
            seed = random.randint(0, 999999999)
    else:
        main(seed=args.seed, args=args)

if __name__ == '__main__':
    start()
