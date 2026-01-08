def name():
    return "SwdTechs"

def parse(parser):
    swdtechs = parser.add_argument_group("SwdTechs")

    swdtechs.add_argument("-fst", "--fast-swdtech", action = "store_true",
                          help = "SwdTech gauge charges four times faster")
    swdtechs.add_argument("-sel", "--swdtechs-everyone-learns", action = "store_true",
                          help = "SwdTechs learnable by characters without the SwdTech command")

def process(args):
    pass

def flags(args):
    flags = ""

    if args.fast_swdtech:
        flags += " -fst"
    if args.swdtechs_everyone_learns:
        flags += " -sel"

    return flags

def options(args):
    return [
        ("Fast SwdTech", args.fast_swdtech),
        ("Everyone Learns", args.swdtechs_everyone_learns),
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
