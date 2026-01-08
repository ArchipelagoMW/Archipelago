def name():
    return "Blitzes"

def parse(parser):
    blitzes = parser.add_argument_group("Blitzes")

    blitzes.add_argument("-brl", "--bum-rush-last", action = "store_true",
                         help = "Bum Rush requires learning every other blitz")
    blitzes.add_argument("-bel", "--blitzes-everyone-learns", action = "store_true",
                         help = "Blitzes learnable by characters without the Blitz command")

def process(args):
    pass

def flags(args):
    flags = ""

    if args.bum_rush_last:
        flags += " -brl"
    if args.blitzes_everyone_learns:
        flags += " -bel"

    return flags

def options(args):
    return [
        ("Bum Rush Last", args.bum_rush_last),
        ("Everyone Learns", args.blitzes_everyone_learns),
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
