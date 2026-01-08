def name():
    return "Starting Gold/Items"

def parse(parser):
    starting_gold_items = parser.add_argument_group("Starting Gold/Items")

    starting_gold_items.add_argument("-gp", "--gold", default = 0, type = int, choices = range(0, 1000000), metavar = "COUNT",
                                     help = "Start game with %(metavar)s gold [0-999999], default %(default)s")

    starting_gold_items.add_argument("-smc", "--start-moogle-charms", default = 0, type = int, choices = range(4), metavar = "COUNT",
                                     help = "Start game with %(metavar)s Moogle Charms. Overrides No Moogle Charms option")
    starting_gold_items.add_argument("-sshoes", "--start-sprint-shoes", default = 0, type = int, choices = range(4), metavar = "COUNT",
                                     help = "Start game with %(metavar)s Sprint Shoes. Overrides No Sprint Shoes option")

    starting_gold_items.add_argument("-sws", "--start-warp-stones", default = 0, type = int, choices = range(11), metavar = "COUNT",
                                     help = "Start game with %(metavar)s Warp Stones")
    starting_gold_items.add_argument("-sfd", "--start-fenix-downs", default = 0, type = int, choices = range(11), metavar = "COUNT",
                                     help = "Start game with %(metavar)s Fenix Downs")
    starting_gold_items.add_argument("-sto", "--start-tools", default = 0, type = int, choices = range(9), metavar = "COUNT",
                                     help = "Start game with %(metavar)s different random tools"),
    starting_gold_items.add_argument("-sj", "--start-junk", default = 0, type = int, choices = range(25), metavar = "COUNT",
                                     help = "Start game with %(metavar)s unique low tier items. Includes weapons, armors, helmets, shields, and relics"),

def process(args):
    pass

def flags(args):
    flags = ""

    if args.gold != 0:
        flags += f" -gp {args.gold}"
    if args.start_moogle_charms != 0:
        flags += f" -smc {args.start_moogle_charms}"
    if args.start_sprint_shoes != 0:
        flags += f" -sshoes {args.start_sprint_shoes}"
    if args.start_warp_stones != 0:
        flags += f" -sws {args.start_warp_stones}"
    if args.start_fenix_downs != 0:
        flags += f" -sfd {args.start_fenix_downs}"
    if args.start_tools != 0:
        flags += f" -sto {args.start_tools}"
    if args.start_junk != 0:
        flags += f" -sj {args.start_junk}"

    return flags

def options(args):
    opts = [
        ("Start Gold", args.gold),
        ("Start Moogle Charms", args.start_moogle_charms),
        ("Start Sprint Shoes", args.start_sprint_shoes),
        ("Start Warp Stones", args.start_warp_stones),
        ("Start Fenix Downs", args.start_fenix_downs),
        ("Start Tools", args.start_tools),
    ]
    
    if args.start_junk != 0:
        opts += [
            ("Start Junk", args.start_junk)
        ]

    return opts

def menu(args):
    return (name(), options(args))

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        log.append(format_option(*entry))

    return log
