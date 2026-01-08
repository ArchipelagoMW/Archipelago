def name():
    return "Lores"

def parse(parser):
    from ..data.lores import Lores

    lores = parser.add_argument_group("Lores")

    lores.add_argument("-slr", "--start-lores-random", default = None, type = int,
                       nargs = 2, metavar = ("MIN", "MAX"), choices = range(Lores.LORE_COUNT + 1),
                       help = "Start with random lores learned")

    lores_mp = lores.add_mutually_exclusive_group()
    lores_mp.add_argument("-lmps", "--lores-mp-shuffle", action = "store_true",
                          help = "Lore MP costs shuffled")
    lores_mp.add_argument("-lmprv", "--lores-mp-random-value", default = None, type = int,
                          nargs = 2, metavar = ("MIN", "MAX"), choices = range(255),
                          help = "Lore MP costs randomized")
    lores_mp.add_argument("-lmprp", "--lores-mp-random-percent", default = None, type = int,
                          nargs = 2, metavar = ("MIN", "MAX"), choices = range(201),
                          help = "Each lore's MP cost set to random percent of original within given range")

    lores.add_argument("-lel", "--lores-everyone-learns", action = "store_true",
                       help = "Lores learnable by characters without the Lore command")

    lores.add_argument("-llr", "--lores-level-randomize", action = "store_true",
                       help = "Level based lores will have the level randomized (L?, L1-L5)")

def process(args):
    args._process_min_max("start_lores_random")
    args._process_min_max("lores_mp_random_value")
    args._process_min_max("lores_mp_random_percent")

def flags(args):
    flags = ""

    if args.start_lores_random:
        flags += f" -slr {args.start_lores_random_min} {args.start_lores_random_max}"

    if args.lores_mp_shuffle:
        flags += " -lmps"
    elif args.lores_mp_random_value:
        flags += f" -lmprv {args.lores_mp_random_value_min} {args.lores_mp_random_value_max}"
    elif args.lores_mp_random_percent:
        flags += f" -lmprp {args.lores_mp_random_percent_min} {args.lores_mp_random_percent_max}"

    if args.lores_everyone_learns:
        flags += " -lel"

    if args.lores_level_randomize:
        flags += " -llr"
    return flags

def options(args):
    start_lores = "Original"
    if args.start_lores_random:
        start_lores = f"Random {args.start_lores_random_min}-{args.start_lores_random_max}"

    mp = "Original"
    if args.lores_mp_shuffle:
        mp = "Shuffle"
    elif args.lores_mp_random_value:
        mp = f"Random Value {args.lores_mp_random_value_min}-{args.lores_mp_random_value_max}"
    elif args.lores_mp_random_percent:
        mp = f"Random Percent {args.lores_mp_random_percent_min}-{args.lores_mp_random_percent_max}%"

    lvl_x_spells = "Random" if args.lores_level_randomize else "Original"
    opts = [
        ("Start Lores", start_lores),
        ("MP", mp),
        ("Everyone Learns", args.lores_everyone_learns),
        ("L.x Spells", lvl_x_spells)
    ]
    
    
    return opts

def menu(args):
    entries = options(args)
    for index, entry in enumerate(entries):
        key, value = entry
        try:
            if key == "Start Lores":
                value = value.replace("Random ", "")
            elif key == "MP":
                value = value.replace("Random Value ", "")
                value = value.replace("Random Percent ", "")
            entries[index] = (key, value)
        except:
            pass
    return (name(), entries)

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        log.append(format_option(*entry))

    return log
