def name():
    return "Rages"

def parse(parser):
    from ..data.rages import Rages

    rages = parser.add_argument_group("Rages")

    rages.add_argument("-srr", "--start-rages-random", default = None, type = int,
                       nargs = 2, metavar = ("MIN", "MAX"), choices = range(Rages.RAGE_COUNT),
                       help = "Start with random rages learned")

    rages.add_argument("-rnl", "--rages-no-leap", action = "store_true",
                       help = "Leap not available on the Veldt. Rages learnable after every battle")

    rages.add_argument("-rnc", "--rages-no-charm", action = "store_true",
                       help = "Charm ability not available from Nightshade rage")

def process(args):
    args._process_min_max("start_rages_random")

def flags(args):
    flags = ""

    if args.start_rages_random:
        flags += f" -srr {args.start_rages_random_min} {args.start_rages_random_max}"

    if args.rages_no_leap:
        flags += " -rnl"

    if args.rages_no_charm:
        flags += " -rnc"

    return flags

def options(args):
    start_rages = "Original"
    if args.start_rages_random:
        start_rages = f"Random {args.start_rages_random_min}-{args.start_rages_random_max}"

    return [
        ("Start Rages", start_rages),
        ("No Leap", args.rages_no_leap),
        ("No Charm", args.rages_no_charm),
    ]

def menu(args):
    entries = options(args)
    for index, entry in enumerate(entries):
        key, value = entry
        if key == "Start Rages":
            value = value.replace("Random ", "")
            entries[index] = (key, value)
    return (name(), entries)

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        log.append(format_option(*entry))

    return log
