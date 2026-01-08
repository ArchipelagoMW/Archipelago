def name():
    return "Bug Fixes"

def parse(parser):
    bug_fixes = parser.add_argument_group("Bug Fixes")
    bug_fixes.add_argument("-fs", "--fix-sketch", action = "store_true",
                           help = "Sketch missing will not cause various major glitches")
    bug_fixes.add_argument("-fe", "--fix-evade", action = "store_true",
                           help = "Evade used for physical attacks instead of mblock. Fixes Beads, Blind, and other status effect influences")
    bug_fixes.add_argument("-fvd", "--fix-vanish-doom", action = "store_true",
                           help = "Vanish does not override instant death immunity")
    bug_fixes.add_argument("-fr", "--fix-retort", action = "store_true",
                           help = "Retort will not counter various actions infinitely with Imp status")
    bug_fixes.add_argument("-fj", "--fix-jump", action = "store_true",
                           help = "Fix characters disappearing as a result of jump/super ball/launcher interactions")
    bug_fixes.add_argument("-fbs", "--fix-boss-skip", action = "store_true",
                           help = "Poltergeist and Inferno in Kefka's Tower cannot be skipped")
    bug_fixes.add_argument("-fedc", "--fix-enemy-damage-counter", action = "store_true",
                           help = "Enemy damage counters only trigger if HP is reduced")
    bug_fixes.add_argument("-fc", "--fix-capture", action = "store_true",
                           help = "Fix Capture such that Weapon Special Effects are applied and Multi-Steals work")

def process(args):
    pass

def flags(args):
    flags = ""

    if args.fix_sketch:
        flags += " -fs"
    if args.fix_evade:
        flags += " -fe"
    if args.fix_vanish_doom:
        flags += " -fvd"
    if args.fix_retort:
        flags += " -fr"
    if args.fix_jump:
        flags += " -fj"
    if args.fix_boss_skip:
        flags += " -fbs"
    if args.fix_enemy_damage_counter:
        flags += " -fedc"
    if args.fix_capture:
        flags += " -fc"

    return flags

def options(args):
    return [
        ("Sketch", args.fix_sketch),
        ("Evade", args.fix_evade),
        ("Vanish/Doom", args.fix_vanish_doom),
        ("Retort", args.fix_retort),
        ("Jump", args.fix_jump),
        ("Boss Skip", args.fix_boss_skip),
        ("Enemy Damage Counter", args.fix_enemy_damage_counter),
        ("Capture", args.fix_capture),
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
