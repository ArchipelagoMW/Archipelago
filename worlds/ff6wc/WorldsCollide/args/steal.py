def name():
    return "Steal"

def parse(parser):
    steal = parser.add_argument_group("Steal")

    steal_chances = steal.add_mutually_exclusive_group()
    steal_chances.add_argument("-sch", "--steal-chances-higher", action = "store_true",
                         help = "Steal Rate is improved and rare steals are more likely")
    steal_chances.add_argument("-sca", "--steal-chances-always", action = "store_true",
                         help = "Steal will always succeed if enemy has an item")

    steal.add_argument("-ssd", "--shuffle-steals-drops", default = None, type = int,
                          metavar = "PERCENT", choices = range(101),
                          help="Shuffle items stolen and dropped with randomized percent")

def process(args):
    if args.shuffle_steals_drops is not None:
        args.shuffle_steals_drops_random_percent = args.shuffle_steals_drops
        args.shuffle_steals_drops = True
    pass

def flags(args):
    flags = ""

    if args.steal_chances_higher:
        flags += " -sch"
    if args.steal_chances_always:
        flags += " -sca"
    if args.shuffle_steals_drops:
        flags += f" -ssd {args.shuffle_steals_drops_random_percent}"

    return flags

def options(args):
    result = []

    steal_chances = "Original"
    if args.steal_chances_higher:
        steal_chances = "Higher"
    if args.steal_chances_always:
        steal_chances = "Always"

    result.append(("Chances", steal_chances))

    result.append(("Shuffle", args.shuffle_steals_drops))
    if args.shuffle_steals_drops:
        result.append(("Random Percent", f"{args.shuffle_steals_drops_random_percent}%"))

    return result

def menu(args):
    return (name(), options(args))

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        log.append(format_option(*entry))

    return log
