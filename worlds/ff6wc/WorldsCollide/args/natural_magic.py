def name():
    return "Natural Magic"

def parse(parser):
    natural_magic = parser.add_argument_group("Natural Magic")

    from ..data.characters import Characters
    natural_magic_char_options = ["random", ""]
    natural_magic_char_options += [name.lower() for name in Characters.DEFAULT_NAME[ : -2]]

    natural_magic.add_argument("-nm1", "--natural-magic1", default = "", type = str.lower, choices = natural_magic_char_options,
                               help = "Character to learn Terra's natural magic")
    natural_magic.add_argument("-rnl1", "--random-natural-levels1", action = "store_true",
                               help = "Randomize levels Terra learns natural spells")
    natural_magic.add_argument("-rns1", "--random-natural-spells1", action = "store_true",
                               help = "Randomize Terra's natural spells")
    natural_magic.add_argument("-nm2", "--natural-magic2", default = "", type = str.lower, choices = natural_magic_char_options,
                               help = "Character to learn Celes' natural magic")
    natural_magic.add_argument("-rnl2", "--random-natural-levels2", action = "store_true",
                               help = "Randomize levels Celes learns natural spells")
    natural_magic.add_argument("-rns2", "--random-natural-spells2", action = "store_true",
                               help = "Randomize Celes' natural spells")
    natural_magic.add_argument("-nmmi", "--natural-magic-menu-indicator", action = "store_true",
                               help = "Add indicator to status menu for characters with natural magic")

def process(args):
    pass

def flags(args):
    flags = ""

    if args.natural_magic1:
        flags += f" -nm1 {args.natural_magic1}"
    if args.random_natural_levels1:
        flags += " -rnl1"
    if args.random_natural_spells1:
        flags += " -rns1"

    if args.natural_magic2:
        flags += f" -nm2 {args.natural_magic2}"
    if args.random_natural_levels2:
        flags += " -rnl2"
    if args.random_natural_spells2:
        flags += " -rns2"

    if args.natural_magic_menu_indicator:
        flags += " -nmmi"

    return flags

def options(args):
    natural_magic1 = "None"
    if args.natural_magic1:
        natural_magic1 = args.natural_magic1.capitalize()

    natural_magic2 = "None"
    if args.natural_magic2:
        natural_magic2 = args.natural_magic2.capitalize()

    return [
        ("Natural Magic", natural_magic1),
        ("Randomize Levels", args.random_natural_levels1),
        ("Randomize Spells", args.random_natural_spells1),

        ("Natural Magic", natural_magic2),
        ("Randomize Levels", args.random_natural_levels2),
        ("Randomize Spells", args.random_natural_spells2),

        ("Menu Indicator", args.natural_magic_menu_indicator),
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
