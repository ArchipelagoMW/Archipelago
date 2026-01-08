def name():
    return "Scaling"

def parse(parser):
    scaling = parser.add_argument_group("Scaling")

    level_scaling = scaling.add_mutually_exclusive_group()
    level_scaling.add_argument("-lsa", "--level-scaling-average", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 55, 5)],
                               help = "Enemy and boss levels equal to %(metavar)s * party average level")
    level_scaling.add_argument("-lsh", "--level-scaling-highest", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 55, 5)],
                               help = "Enemy and boss levels equal to %(metavar)s * highest level in party")
    level_scaling.add_argument("-lsce", "--level-scaling-ce", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 55, 5)],
                               help = "Enemies and bosses gain %(metavar)s levels for each character recruited and esper acquired")
    level_scaling.add_argument("-lsced", "--level-scaling-ced", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 55, 5)],
                               help = "Enemies and bosses gain %(metavar)s levels for each character recruited, esper acquired, and dragon defeated")
    level_scaling.add_argument("-lsc", "--level-scaling-checks", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 55, 5)],
                               help = "Enemies and bosses gain %(metavar)s levels for each check completed")
    level_scaling.add_argument("-lst", "--level-scaling-time", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 55, 5)],
                               help = "Enemies and bosses gain 1 level every %(metavar)s minutes")
    level_scaling.add_argument("-lsbd", "--level-scaling-bosses-dragons", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 105, 5)],
                               help = "Enemies and bosses gain %(metavar)s levels for each boss and dragon defeated")

    hp_mp_scaling = scaling.add_mutually_exclusive_group()
    hp_mp_scaling.add_argument("-hma", "--hp-mp-scaling-average", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 55, 5)],
                               help = "Enemy and boss hp/mp scales %(metavar)s * party averaage level")
    hp_mp_scaling.add_argument("-hmh", "--hp-mp-scaling-highest", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 55, 5)],
                               help = "Enemy and boss hp/mp scales %(metavar)s * highest level in party")
    hp_mp_scaling.add_argument("-hmce", "--hp-mp-scaling-ce", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 55, 5)],
                               help = "Enemy and boss hp/mp scales %(metavar)s * each character recruited and esper acquired")
    hp_mp_scaling.add_argument("-hmced", "--hp-mp-scaling-ced", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 55, 5)],
                               help = "Enemy and boss hp/mp scales %(metavar)s * each character recruited, esper acquired, and dragon defeated")
    hp_mp_scaling.add_argument("-hmc", "--hp-mp-scaling-checks", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 55, 5)],
                               help = "Enemy and boss hp/mp scales %(metavar)s * each check completed")
    hp_mp_scaling.add_argument("-hmt", "--hp-mp-scaling-time", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 55, 5)],
                               help = "Enemy and boss hp/mp scales every %(metavar)s minutes")
    hp_mp_scaling.add_argument("-hmbd", "--hp-mp-scaling-bosses-dragons", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 105, 5)],
                               help = "Enemy and boss hp/mp scales %(metavar)s * each boss and dragon defeated")

    xp_gp_scaling = scaling.add_mutually_exclusive_group()
    xp_gp_scaling.add_argument("-xga", "--xp-gp-scaling-average", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 55, 5)],
                               help = "Enemy and boss exp/gp scales %(metavar)s * party averaage level")
    xp_gp_scaling.add_argument("-xgh", "--xp-gp-scaling-highest", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 55, 5)],
                               help = "Enemy and boss exp/gp scales %(metavar)s * highest level in party")
    xp_gp_scaling.add_argument("-xgce", "--xp-gp-scaling-ce", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 55, 5)],
                               help = "Enemy and boss exp/gp scales %(metavar)s * each character recruited and esper acquired")
    xp_gp_scaling.add_argument("-xgced", "--xp-gp-scaling-ced", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 55, 5)],
                               help = "Enemy and boss exp/gp scales %(metavar)s * each character recruited, esper acquired, and dragon defeated")
    xp_gp_scaling.add_argument("-xgc", "--xp-gp-scaling-checks", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 55, 5)],
                               help = "Enemy and boss exp/gp scales %(metavar)s * each check completed")
    xp_gp_scaling.add_argument("-xgt", "--xp-gp-scaling-time", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 55, 5)],
                               help = "Enemy and boss exp/gp scales every %(metavar)s minutes")
    xp_gp_scaling.add_argument("-xgbd", "--xp-gp-scaling-bosses-dragons", default = None, type = float,
                               metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 105, 5)],
                               help = "Enemy and boss exp/gp scales %(metavar)s * for each boss and dragon defeated")

    ability_scaling = scaling.add_mutually_exclusive_group()
    ability_scaling.add_argument("-ase", "--ability-scaling-element", default = None, type = float,
                                 metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 55, 5)],
                                 help = "Enemy and boss abilities retain element and increase in tier approximately every (%(metavar)s + 3) levels reaching max tier at level (%(metavar)s + 3) * 8")
    ability_scaling.add_argument("-asr", "--ability-scaling-random", default = None, type = float,
                                 metavar = ("VALUE"), choices = [x / 10.0 for x in range(5, 55, 5)],
                                 help = "Enemy and boss abilities increase in tier approximately every (%(metavar)s + 3) levels reaching max tier at level (%(metavar)s + 3) * 8")

    scaling.add_argument("-msl", "--max-scale-level", default = 99, type = int, choices = range(3, 100), metavar = "VALUE",
                        help = "Max level enemies scaled up to. Note: distortion levels still applied")
    scaling.add_argument("-sed", "--scale-eight-dragons", action = "store_true",
                        help = "Apply scaling to the eight dragons")
    scaling.add_argument("-sfb", "--scale-final-battles", action = "store_true",
                        help = "Apply scaling to the final battles")

def process(args):
    args.level_scaling = True
    if args.level_scaling_average:
        args.level_scaling_factor = args.level_scaling_average
    elif args.level_scaling_highest:
        args.level_scaling_factor = args.level_scaling_highest
    elif args.level_scaling_ce:
        args.level_scaling_factor = args.level_scaling_ce
    elif args.level_scaling_ced:
        args.level_scaling_factor = args.level_scaling_ced
    elif args.level_scaling_checks:
        args.level_scaling_factor = args.level_scaling_checks
    elif args.level_scaling_bosses_dragons:
        args.level_scaling_factor = args.level_scaling_bosses_dragons
    elif args.level_scaling_time:
        args.level_scaling_factor = args.level_scaling_time
    else:
        args.level_scaling = False
        args.level_scaling_factor = None

    args.hp_mp_scaling = True
    if args.hp_mp_scaling_average:
        args.hp_mp_scaling_factor = args.hp_mp_scaling_average
    elif args.hp_mp_scaling_highest:
        args.hp_mp_scaling_factor = args.hp_mp_scaling_highest
    elif args.hp_mp_scaling_ce:
        args.hp_mp_scaling_factor = args.hp_mp_scaling_ce
    elif args.hp_mp_scaling_ced:
        args.hp_mp_scaling_factor = args.hp_mp_scaling_ced
    elif args.hp_mp_scaling_checks:
        args.hp_mp_scaling_factor = args.hp_mp_scaling_checks
    elif args.hp_mp_scaling_bosses_dragons:
        args.hp_mp_scaling_factor = args.hp_mp_scaling_bosses_dragons
    elif args.hp_mp_scaling_time:
        args.hp_mp_scaling_factor = args.hp_mp_scaling_time
    else:
        args.hp_mp_scaling = False
        args.hp_mp_scaling_factor = None

    args.xp_gp_scaling = True
    if args.xp_gp_scaling_average:
        args.xp_gp_scaling_factor = args.xp_gp_scaling_average
    elif args.xp_gp_scaling_highest:
        args.xp_gp_scaling_factor = args.xp_gp_scaling_highest
    elif args.xp_gp_scaling_ce:
        args.xp_gp_scaling_factor = args.xp_gp_scaling_ce
    elif args.xp_gp_scaling_ced:
        args.xp_gp_scaling_factor = args.xp_gp_scaling_ced
    elif args.xp_gp_scaling_checks:
        args.xp_gp_scaling_factor = args.xp_gp_scaling_checks
    elif args.xp_gp_scaling_bosses_dragons:
        args.xp_gp_scaling_factor = args.xp_gp_scaling_bosses_dragons
    elif args.xp_gp_scaling_time:
        args.xp_gp_scaling_factor = args.xp_gp_scaling_time
    else:
        args.xp_gp_scaling = False
        args.xp_gp_scaling_factor = None

    args.ability_scaling = True
    if args.ability_scaling_element:
        args.ability_scaling_factor = args.ability_scaling_element
    elif args.ability_scaling_random:
        args.ability_scaling_factor = args.ability_scaling_random
    else:
        args.ability_scaling = False
        args.ability_scaling_factor = None

def flags(args):
    flags = ""

    if args.level_scaling_average:
        flags += f" -lsa {args.level_scaling_factor:g}"
    elif args.level_scaling_highest:
        flags += f" -lsh {args.level_scaling_factor:g}"
    elif args.level_scaling_ce:
        flags += f" -lsce {args.level_scaling_factor:g}"
    elif args.level_scaling_ced:
        flags += f" -lsced {args.level_scaling_factor:g}"
    elif args.level_scaling_checks:
        flags += f" -lsc {args.level_scaling_factor:g}"
    elif args.level_scaling_bosses_dragons:
        flags += f" -lsbd {args.level_scaling_factor:g}"
    elif args.level_scaling_time:
        flags += f" -lst {args.level_scaling_factor:g}"

    if args.hp_mp_scaling_average:
        flags += f" -hma {args.hp_mp_scaling_factor:g}"
    elif args.hp_mp_scaling_highest:
        flags += f" -hmh {args.hp_mp_scaling_factor:g}"
    elif args.hp_mp_scaling_ce:
        flags += f" -hmce {args.hp_mp_scaling_factor:g}"
    elif args.hp_mp_scaling_ced:
        flags += f" -hmced {args.hp_mp_scaling_factor:g}"
    elif args.hp_mp_scaling_checks:
        flags += f" -hmc {args.hp_mp_scaling_factor:g}"
    elif args.hp_mp_scaling_bosses_dragons:
        flags += f" -hmbd {args.hp_mp_scaling_factor:g}"
    elif args.hp_mp_scaling_time:
        flags += f" -hmt {args.hp_mp_scaling_factor:g}"

    if args.xp_gp_scaling_average:
        flags += f" -xga {args.xp_gp_scaling_factor:g}"
    elif args.xp_gp_scaling_highest:
        flags += f" -xgh {args.xp_gp_scaling_factor:g}"
    elif args.xp_gp_scaling_ce:
        flags += f" -xgce {args.xp_gp_scaling_factor:g}"
    elif args.xp_gp_scaling_ced:
        flags += f" -xgced {args.xp_gp_scaling_factor:g}"
    elif args.xp_gp_scaling_checks:
        flags += f" -xgc {args.xp_gp_scaling_factor:g}"
    elif args.xp_gp_scaling_bosses_dragons:
        flags += f" -xgbd {args.xp_gp_scaling_factor:g}"
    elif args.xp_gp_scaling_time:
        flags += f" -xgt {args.xp_gp_scaling_factor:g}"

    if args.ability_scaling_element:
        flags += f" -ase {args.ability_scaling_factor:g}"
    elif args.ability_scaling_random:
        flags += f" -asr {args.ability_scaling_factor:g}"

    if args.max_scale_level != 99:
        flags += f" -msl {args.max_scale_level}"

    if args.scale_eight_dragons:
        flags += " -sed"
    if args.scale_final_battles:
        flags += " -sfb"

    return flags

def options(args):
    result = []

    level_scaling = "None"
    if args.level_scaling_average:
        level_scaling = "Party Average"
    elif args.level_scaling_highest:
        level_scaling = "Party Highest"
    elif args.level_scaling_ce:
        level_scaling = "Characters + Espers"
    elif args.level_scaling_ced:
        level_scaling = "Characters + Espers + Dragons"
    elif args.level_scaling_checks:
        level_scaling = "Checks"
    elif args.level_scaling_bosses_dragons:
        level_scaling = "Bosses + Dragons"
    elif args.level_scaling_time:
        level_scaling = "Time"

    result.append(("Level Scaling", level_scaling))
    if args.level_scaling_factor is not None:
        result.append(("Level Scaling Factor", f"{args.level_scaling_factor:g}"))

    hp_mp_scaling = "None"
    if args.hp_mp_scaling_average:
        hp_mp_scaling = "Party Average"
    elif args.hp_mp_scaling_highest:
        hp_mp_scaling = "Party Highest"
    elif args.hp_mp_scaling_ce:
        hp_mp_scaling = "Characters + Espers"
    elif args.hp_mp_scaling_ced:
        hp_mp_scaling = "Characters + Espers + Dragons"
    elif args.hp_mp_scaling_checks:
        hp_mp_scaling = "Checks"
    elif args.hp_mp_scaling_bosses_dragons:
        hp_mp_scaling = "Bosses + Dragons"
    elif args.hp_mp_scaling_time:
        hp_mp_scaling = "Time"

    result.append(("HP/MP Scaling", hp_mp_scaling))
    if args.hp_mp_scaling_factor is not None:
        result.append(("HP/MP Scaling Factor", f"{args.hp_mp_scaling_factor:g}"))

    xp_gp_scaling = "None"
    if args.xp_gp_scaling_average:
        xp_gp_scaling = "Party Average"
    elif args.xp_gp_scaling_highest:
        xp_gp_scaling = "Party Highest"
    elif args.xp_gp_scaling_ce:
        xp_gp_scaling = "Characters + Espers"
    elif args.xp_gp_scaling_ced:
        xp_gp_scaling = "Characters + Espers + Dragons"
    elif args.xp_gp_scaling_checks:
        xp_gp_scaling = "Checks"
    elif args.xp_gp_scaling_bosses_dragons:
        xp_gp_scaling = "Bosses + Dragons"
    elif args.xp_gp_scaling_time:
        xp_gp_scaling = "Time"

    result.append(("Exp/GP Scaling", xp_gp_scaling))
    if args.xp_gp_scaling_factor is not None:
        result.append(("Exp/GP Scaling Factor", f"{args.xp_gp_scaling_factor:g}"))

    ability_scaling = "None"
    if args.ability_scaling_element:
        ability_scaling = "Element"
    elif args.ability_scaling_random:
        ability_scaling = "Random"

    result.append(("Ability Scaling", ability_scaling))
    if args.ability_scaling_factor is not None:
        result.append(("Ability Scaling Factor", f"{args.ability_scaling_factor:g}"))

    result.append(("Max Scale Level", args.max_scale_level))
    result.append(("Scale Eight Dragons", args.scale_eight_dragons))
    result.append(("Scale Final Battles", args.scale_final_battles))

    return result

def menu(args):
    entries = options(args)

    for index, entry in enumerate(entries):
        key, value = entry
        try:
            key = key.replace(" Scaling", "")
            value = value.replace("Party Average", "PAverage")
            value = value.replace("Party Highest", "PHighest")
            value = value.replace("Characters + Espers + Dragons", "C + E + D")
            value = value.replace("Characters + Espers", "C + E")
            value = value.replace("Bosses + Dragons", "B + D")
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
