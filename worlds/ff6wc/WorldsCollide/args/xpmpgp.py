def name():
    return "Experience, Magic Points, Gold"

def parse(parser):
    xpmpgp = parser.add_argument_group("Experience, Magic Points, Gold")

    xpmpgp.add_argument("-xpm", "--xp-mult", default = 1, type = int, choices = range(0, 256), metavar = "VALUE",
                        help = "Multiply experience by %(metavar)s [0-255], default %(default)s")
    xpmpgp.add_argument("-mpm", "--mp-mult", default = 1, type = int, choices = range(0, 256), metavar = "VALUE",
                        help = "Multiply magic points by %(metavar)s [0-255], default %(default)s")
    xpmpgp.add_argument("-gpm", "--gp-mult", default = 1, type = int, choices = range(0, 256), metavar = "VALUE",
                        help = "Multiply gold by %(metavar)s [0-255], default %(default)s.")
    xpmpgp.add_argument("-nxppd", "--no-exp-party-divide", action = "store_true",
                        help = "Do not divide experience by number of surviving party members")

def process(args):
    pass

def flags(args):
    flags = ""

    if args.xp_mult != 1:
        flags += f" -xpm {args.xp_mult}"
    if args.mp_mult != 1:
        flags += f" -mpm {args.mp_mult}"
    if args.gp_mult != 1:
        flags += f" -gpm {args.gp_mult}"

    if args.no_exp_party_divide:
        flags += " -nxppd"

    return flags

def options(args):
    return [
        ("Experience Multiplier", args.xp_mult),
        ("Magic Points Multiplier", args.mp_mult),
        ("Gold Multiplier", args.gp_mult),
        ("No Exp Party Divide", args.no_exp_party_divide),
    ]

def menu(args):
    short_name = "Exp, MP, GP"

    entries = options(args)
    for index in range(3):
        key, value = entries[index]

        key = key.replace(" Multiplier", "")
        value = str(value) + 'x'

        entries[index] = (key, value)

    return (short_name, entries)

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        log.append(format_option(*entry))

    return log
