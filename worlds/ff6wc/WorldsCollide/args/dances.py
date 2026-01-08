def name():
    return "Dances"

def parse(parser):
    from ..data.dances import Dances

    dances = parser.add_argument_group("Dances")

    dances.add_argument("-sdr", "--start-dances-random", default = None, type = int,
                        nargs = 2, metavar = ("MIN", "MAX"), choices = range(Dances.DANCE_COUNT + 1),
                        help = "Start with random dances learned")

    dances.add_argument("-das", "--dances-shuffle", action = "store_true",
                        help = "Abilities shuffled between all dances")
    dances.add_argument("-dda", "--dances-display-abilities", action = "store_true",
                        help = "Display ability names in dance skills menu")
    dances.add_argument("-dns", "--dances-no-stumble", action = "store_true",
                        help = "Disable stumbling when dancing in different terrain")
    dances.add_argument("-del", "--dances-everyone-learns", action = "store_true",
                        help = "Dances learnable by characters without the Dance command")

def process(args):
    args._process_min_max("start_dances_random")

def flags(args):
    flags = ""

    if args.start_dances_random:
        flags += f" -sdr {args.start_dances_random_min} {args.start_dances_random_max}"

    if args.dances_shuffle:
        flags += " -das"

    if args.dances_display_abilities:
        flags += " -dda"

    if args.dances_no_stumble:
        flags += " -dns"

    if args.dances_everyone_learns:
        flags += " -del"

    return flags

def options(args):
    start_dances = "None"
    if args.start_dances_random:
        start_dances = f"Random {args.start_dances_random_min}-{args.start_dances_random_max}"

    return [
        ("Start Dances", start_dances),
        ("Shuffle Abilities", args.dances_shuffle),
        ("Display Abilities", args.dances_display_abilities),
        ("No Stumble", args.dances_no_stumble),
        ("Everyone Learns", args.dances_everyone_learns),
    ]

def menu(args):
    return (name(), options(args))

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        log.append(format_option(*entry))

    return log
