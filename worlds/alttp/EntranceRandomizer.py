#!/usr/bin/env python3
import argparse
import copy
import textwrap
import shlex

"""Legacy module, undergoing dismantling."""


class ArgumentDefaultsHelpFormatter(argparse.RawTextHelpFormatter):

    def _get_help_string(self, action):
        return textwrap.dedent(action.help)


def parse_arguments(argv, no_defaults=False):
    def defval(value):
        return value if not no_defaults else None

    # we need to know how many players we have first
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--multi', default=defval(1), type=lambda value: max(int(value), 1))
    multiargs, _ = parser.parse_known_args(argv)

    parser = argparse.ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--logic', default=defval('no_glitches'), const='no_glitches', nargs='?', choices=['no_glitches', 'minor_glitches', 'overworld_glitches', 'hybrid_major_glitches', 'no_logic'],
                        help='''\
                             Select Enforcement of Item Requirements. (default: %(default)s)
                             No Glitches:
                             Minor Glitches: May require Fake Flippers, Bunny Revival
                                             and Dark Room Navigation.
                             Overworld Glitches: May require overworld glitches.
                             Hybrid Major Glitches: May require both overworld and underworld clipping. 
                             No Logic: Distribute items without regard for
                                             item requirements.
                             ''')
    parser.add_argument('--glitch_triforce', help='Allow glitching to Triforce from Ganon\'s room', action='store_true')
    parser.add_argument('--mode', default=defval('open'), const='open', nargs='?', choices=['standard', 'open', 'inverted'],
                        help='''\
                             Select game mode. (default: %(default)s)
                             Open:      World starts with Zelda rescued.
                             Standard:  Fixes Hyrule Castle Secret Entrance and Front Door
                                        but may lead to weird rain state issues if you exit
                                        through the Hyrule Castle side exits before rescuing
                                        Zelda in a full shuffle.
                             Inverted:  Starting locations are Dark Sanctuary in West Dark
                                        World or at Link's House, which is shuffled freely.
                                        Requires the moon pearl to be Link in the Light World
                                        instead of a bunny.
                             ''')
    parser.add_argument('--goal', default=defval('ganon'), const='ganon', nargs='?',
                        choices=['ganon', 'pedestal', 'bosses', 'triforce_hunt', 'local_triforce_hunt', 'ganon_triforce_hunt', 'local_ganon_triforce_hunt', 'crystals', 'ganon_pedestal'],
                        help='''\
                             Select completion goal. (default: %(default)s)
                             Ganon:         Collect all crystals, beat Agahnim 2 then
                                            defeat Ganon.
                             Crystals:      Collect all crystals then defeat Ganon.
                             Pedestal:      Places the Triforce at the Master Sword Pedestal.
                             Ganon Pedestal: Pull the Master Sword Pedestal, then defeat Ganon.
                             All Dungeons:  Collect all crystals, pendants, beat both
                                            Agahnim fights and then defeat Ganon.
                             Triforce Hunt: Places 30 Triforce Pieces in the world, collect
                                            20 of them to beat the game.
                             Local Triforce Hunt: Places 30 Triforce Pieces in your world, collect
                                            20 of them to beat the game.
                             Ganon Triforce Hunt: Places 30 Triforce Pieces in the world, collect
                                            20 of them, then defeat Ganon.
                             Local Ganon Triforce Hunt: Places 30 Triforce Pieces in your world,
                                            collect 20 of them, then defeat Ganon.
                             ''')
    parser.add_argument('--triforce_pieces_available', default=defval(30),
                        type=lambda value: min(max(int(value), 1), 90),
                        help='''Set Triforce Pieces available in item pool.''')
    parser.add_argument('--triforce_pieces_required', default=defval(20),
                        type=lambda value: min(max(int(value), 1), 90),
                        help='''Set Triforce Pieces required to win a Triforce Hunt''')
    parser.add_argument('--difficulty', default=defval('normal'), const='normal', nargs='?',
                        choices=['easy', 'normal', 'hard', 'expert'],
                        help='''\
                             Select game difficulty. Affects available itempool. (default: %(default)s)
                             Easy:            An easier setting with some equipment duplicated and increased health.
                             Normal:          Normal difficulty.
                             Hard:            A harder setting with less equipment and reduced health.
                             Expert:          A harder yet setting with minimum equipment and health.
                             ''')
    parser.add_argument('--item_functionality', default=defval('normal'), const='normal', nargs='?',
                        choices=['easy', 'normal', 'hard', 'expert'],
                        help='''\
                             Select limits on item functionality to increase difficulty. (default: %(default)s)
                             Easy:            Easy functionality. (Medallions usable without sword)
                             Normal:          Normal functionality.
                             Hard:            Reduced functionality.
                             Expert:          Greatly reduced functionality.
                                  ''')
    parser.add_argument('--timer', default=defval('none'), const='normal', nargs='?', choices=['none', 'display', 'timed', 'timed_ohko', 'ohko', 'timed_countdown'],
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
    parser.add_argument('--countdown_start_time', default=defval(10), type=int,
                        help='''Set amount of time, in minutes, to start with in Timed Countdown and Timed OHKO modes''')
    parser.add_argument('--red_clock_time', default=defval(-2), type=int,
                        help='''Set amount of time, in minutes, to add from picking up red clocks; negative removes time instead''')
    parser.add_argument('--blue_clock_time', default=defval(2), type=int,
                        help='''Set amount of time, in minutes, to add from picking up blue clocks; negative removes time instead''')
    parser.add_argument('--green_clock_time', default=defval(4), type=int,
                        help='''Set amount of time, in minutes, to add from picking up green clocks; negative removes time instead''')
    parser.add_argument('--dungeon_counters', default=defval('default'), const='default', nargs='?', choices=['default', 'on', 'pickup', 'off'],
                        help='''\
                             Select dungeon counter display settings. (default: %(default)s)
                             (Note, since timer takes up the same space on the hud as dungeon
                             counters, timer settings override dungeon counter settings.)
                             Default:       Dungeon counters only show when the compass is
                                            picked up, or otherwise sent, only when compass
                                            shuffle is turned on.
                             On:            Dungeon counters are always displayed.
                             Pickup:        Dungeon counters are shown when the compass is
                                            picked up, even when compass shuffle is turned
                                            off.
                             Off:           Dungeon counters are never shown.
                             ''')

    parser.add_argument('--algorithm', default=defval('balanced'), const='balanced', nargs='?',
                        choices=['freshness', 'flood', 'vt25', 'vt26', 'balanced'],
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
                             Flood:       Push out items starting from Link\'s House and
                                          slightly biased to placing progression items with
                                          less restrictions.
                             ''')
    parser.add_argument('--shuffle', default=defval('vanilla'), const='vanilla', nargs='?', choices=['vanilla', 'simple', 'restricted', 'full', 'crossed', 'insanity', 'restricted_legacy', 'full_legacy', 'madness_legacy', 'insanity_legacy', 'dungeons_full', 'dungeons_simple', 'dungeons_crossed'],
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
    parser.add_argument('--open_pyramid', default=defval('auto'), help='''\
                            Pre-opens the pyramid hole, this removes the Agahnim 2 requirement for it.
                            Depending on goal, you might still need to beat Agahnim 2 in order to beat ganon.
                            fast ganon goals are crystals, ganon_triforce_hunt, local_ganon_triforce_hunt, pedestalganon
                            auto - Only opens pyramid hole if the goal specifies a fast ganon, and entrance shuffle
                                   is vanilla, dungeons_simple or dungeons_full.
                            goal - Opens pyramid hole if the goal specifies a fast ganon.
                            yes - Always opens the pyramid hole.
                            no - Never opens the pyramid hole.
                             ''', choices=['auto', 'goal', 'yes', 'no'])

    parser.add_argument('--loglevel', default=defval('info'), const='info', nargs='?', choices=['error', 'info', 'warning', 'debug'], help='Select level of logging for output.')
    parser.add_argument('--seed', help='Define seed number to generate.', type=int)
    parser.add_argument('--count', help='''\
                             Use to batch generate multiple seeds with same settings.
                             If --seed is provided, it will be used for the first seed, then
                             used to derive the next seed (i.e. generating 10 seeds with
                             --seed given will produce the same 10 (different) roms each
                             time).
                             ''', type=int)

    parser.add_argument('--custom', default=defval(False), help='Not supported.')
    parser.add_argument('--customitemarray', default=defval(False), help='Not supported.')
    # included for backwards compatibility
    parser.add_argument('--shuffleganon', help=argparse.SUPPRESS, action='store_true', default=defval(True))
    parser.add_argument('--no-shuffleganon', help='''\
                             If set, the Pyramid Hole and Ganon's Tower are not
                             included entrance shuffle pool.
                             ''', action='store_false', dest='shuffleganon')

    parser.add_argument('--sprite', help='''\
                             Path to a sprite sheet to use for Link. Needs to be in
                             binary format and have a length of 0x7000 (28672) bytes,
                             or 0x7078 (28792) bytes including palette data.
                             Alternatively, can be a ALttP Rom patched with a Link
                             sprite that will be extracted.
                             ''')

    parser.add_argument('--shufflebosses', default=defval('none'), choices=['none', 'basic', 'normal', 'chaos',
                                                                            "singularity"])

    parser.add_argument('--enemy_health', default=defval('default'),
                        choices=['default', 'easy', 'normal', 'hard', 'expert'])
    parser.add_argument('--enemy_damage', default=defval('default'), choices=['default', 'shuffled', 'chaos'])
    parser.add_argument('--beemizer_total_chance', default=defval(0), type=lambda value: min(max(int(value), 0), 100))
    parser.add_argument('--beemizer_trap_chance', default=defval(0), type=lambda value: min(max(int(value), 0), 100))
    parser.add_argument('--shop_shuffle', default='', help='''\
    combine letters for options:
    g: generate default inventories for light and dark world shops, and unique shops
    f: generate default inventories for each shop individually
    i: shuffle the default inventories of the shops around
    p: randomize the prices of the items in shop inventories
    u: shuffle capacity upgrades into the item pool
    w: consider witch's hut like any other shop and shuffle/randomize it too
    ''')
    parser.add_argument('--shuffle_prizes', default=defval('g'), choices=['', 'g', 'b', 'gb'])
    parser.add_argument('--sprite_pool', help='''\
    Specifies a colon separated list of sprites used for random/randomonevent. If not specified, the full sprite pool is used.''')
    parser.add_argument('--dark_room_logic', default=('Lamp'), choices=["lamp", "torches", "none"], help='''\
    For unlit dark rooms, require the Lamp to be considered in logic by default. 
    Torches means additionally easily accessible Torches that can be lit with Fire Rod are considered doable.
    None means full traversal through dark rooms without tools is considered doable.''')
    parser.add_argument('--multi', default=defval(1), type=lambda value: max(int(value), 1))
    parser.add_argument('--names', default=defval(''))
    parser.add_argument('--outputpath')
    parser.add_argument('--game', default="A Link to the Past")
    parser.add_argument('--race', default=defval(False), action='store_true')
    parser.add_argument('--outputname')
    if multiargs.multi:
        for player in range(1, multiargs.multi + 1):
            parser.add_argument(f'--p{player}', default=defval(''), help=argparse.SUPPRESS)

    ret = parser.parse_args(argv)

    # shuffle medallions

    ret.required_medallions = ("random", "random")
    # cannot be set through CLI currently
    ret.plando_items = []
    ret.plando_texts = {}
    ret.plando_connections = []

    if ret.timer == "none":
        ret.timer = False
    if ret.dungeon_counters == 'on':
        ret.dungeon_counters = True
    elif ret.dungeon_counters == 'off':
        ret.dungeon_counters = False

    if multiargs.multi:
        defaults = copy.deepcopy(ret)
        for player in range(1, multiargs.multi + 1):
            playerargs = parse_arguments(shlex.split(getattr(ret, f"p{player}")), True)

            for name in ['logic', 'mode', 'goal', 'difficulty', 'item_functionality',
                         'shuffle', 'open_pyramid', 'timer',
                         'countdown_start_time', 'red_clock_time', 'blue_clock_time', 'green_clock_time',
                         'beemizer_total_chance', 'beemizer_trap_chance',
                         'shufflebosses', 'enemy_health', 'enemy_damage',
                         'sprite',
                         "triforce_pieces_available",
                         "triforce_pieces_required", "shop_shuffle",
                         "required_medallions",
                         "plando_items", "plando_texts", "plando_connections",
                         'dungeon_counters',
                         'shuffle_prizes', 'sprite_pool', 'dark_room_logic',
                         'game']:
                value = getattr(defaults, name) if getattr(playerargs, name) is None else getattr(playerargs, name)
                if player == 1:
                    setattr(ret, name, {1: value})
                else:
                    getattr(ret, name)[player] = value

    return ret