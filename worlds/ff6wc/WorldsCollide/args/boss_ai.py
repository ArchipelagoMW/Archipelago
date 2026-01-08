def name():
    return "Boss AI"

def parse(parser):
    boss_ai = parser.add_argument_group("Bosses")
    boss_ai.add_argument("-dgne", "--doom-gaze-no-escape", action = "store_true",
                         help = "Doom Gaze does not escape and cannot be escaped from")
    boss_ai.add_argument("-wnz", "--wrexsoul-no-zinger", action = "store_true",
                         help = "Wrexsoul does not use Zinger to possess a character until they expire")
    boss_ai.add_argument("-mmnu", "--magimaster-no-ultima", action = "store_true",
                         help = "MagiMaster does not cast Ultima before death")
    boss_ai.add_argument("-cmd", "--chadarnook-more-demon", action = "store_true",
                         help = "Chadarnook demon form appears for longer and does not immediately switch back to painting")

def process(args):
    pass

def flags(args):
    flags = ""

    if args.doom_gaze_no_escape:
        flags += " -dgne"
    if args.wrexsoul_no_zinger:
        flags += " -wnz"
    if args.magimaster_no_ultima:
        flags += " -mmnu"
    if args.chadarnook_more_demon:
        flags += " -cmd"

    return flags

def options(args):
    return [
        ("Doom Gaze No Escape", args.doom_gaze_no_escape),
        ("Wrexsoul No Zinger", args.wrexsoul_no_zinger),
        ("MagiMaster No Ultima", args.magimaster_no_ultima),
        ("Chadarnook More Demon", args.chadarnook_more_demon),
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
