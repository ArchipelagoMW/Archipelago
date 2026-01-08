def name():
    return "Auction House"

def parse(parser):
    auction = parser.add_argument_group("Auction House")
    auction.add_argument("-ari", "--auction-random-items", action = "store_true",
                         help = "Normal items randomized. Does not affect unbuyable items or Golem/Zoneseek slots")
    auction.add_argument("-anca", "--auction-no-chocobo-airship", action = "store_true",
                         help = "Unbuyable talking chocobo and 1/1200 airship not offered to increase odds of items/espers")
    auction.add_argument("-adeh", "--auction-door-esper-hint", action = "store_true",
                         help = "Door NPC indicates whether espers are still available")
    auction.add_argument("-ame", "--auction-max-espers", default = 2, type = int, choices = range(0, 3), metavar = "COUNT",
                            help = "Auction House has max %(metavar)s espers (can be less)")

def process(args):
    pass

def flags(args):
    flags = ""

    if args.auction_random_items:
        flags += " -ari"
    if args.auction_no_chocobo_airship:
        flags += " -anca"
    if args.auction_door_esper_hint:
        flags += " -adeh"
    if args.auction_max_espers != 2:
        flags += f" -ame {args.auction_max_espers}"

    return flags

def options(args):
    return [
        ("Randomize Items", args.auction_random_items),
        ("No Chocobo/Airship", args.auction_no_chocobo_airship),
        ("Door Esper Hint", args.auction_door_esper_hint),
        ("Max Espers", args.auction_max_espers),
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
