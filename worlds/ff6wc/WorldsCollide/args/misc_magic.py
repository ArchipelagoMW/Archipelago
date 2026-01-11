def name():
    return "Misc. Magic"

def parse(parser):
    magic = parser.add_argument_group("Misc. Magic")

    magic_mp = magic.add_mutually_exclusive_group()
    magic_mp.add_argument("-mmps", "--magic-mp-shuffle", action = "store_true",
                          help = "Magic spells' MP costs shuffled")
    magic_mp.add_argument("-mmprv", "--magic-mp-random-value", default = None, type = int,
                          nargs = 2, metavar = ("MIN", "MAX"), choices = range(255),
                          help = "Magic spells' MP costs randomized")
    magic_mp.add_argument("-mmprp", "--magic-mp-random-percent", default = None, type = int,
                          nargs = 2, metavar = ("MIN", "MAX"), choices = range(201),
                          help = "Each Magic spell's MP cost set to random percent of original within given range")

def process(args):
    args._process_min_max("magic_mp_random_value")
    args._process_min_max("magic_mp_random_percent")

def flags(args):
    flags = ""

    if args.magic_mp_shuffle:
        flags += " -mmps"
    elif args.magic_mp_random_value:
        flags += f" -mmprv {args.magic_mp_random_value_min} {args.magic_mp_random_value_max}"
    elif args.magic_mp_random_percent:
        flags += f" -mmprp {args.magic_mp_random_percent_min} {args.magic_mp_random_percent_max}"

    return flags

def options(args):

    mp = "Original"
    if args.magic_mp_shuffle:
        mp = "Shuffle"
    elif args.magic_mp_random_value:
        mp = f"Random Value {args.magic_mp_random_value_min}-{args.magic_mp_random_value_max}"
    elif args.magic_mp_random_percent:
        mp = f"Random Percent {args.magic_mp_random_percent_min}-{args.magic_mp_random_percent_max}%"

    return [
        ("MP", mp),
    ]

def menu(args):
    entries = options(args)
    for index, entry in enumerate(entries):
        key, value = entry
        try:
            if key == "MP":
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
