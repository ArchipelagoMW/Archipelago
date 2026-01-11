def name():
    return "Sketch/Control"

def parse(parser):
    sketch_control = parser.add_argument_group("Sketch/Control")

    sketch_control.add_argument("-scis", "--sketch-control-improved-stats", action = "store_true",
                         help = "Sketch & Control 100%% accurate and use Sketcher/Controller's stats")
    sketch_control.add_argument("-scia", "--sketch-control-improved-abilities", action = "store_true",
                         help = "Improves Sketch & Control abilities. Removes Battle from Sketch. Adds Rage as a Sketch/Control possibility for most monsters. Gives Sketch abilities to most bosses.")

def process(args):
    pass

def flags(args):
    flags = ""

    if args.sketch_control_improved_stats:
        flags += " -scis"
    if args.sketch_control_improved_abilities:
        flags += " -scia"

    return flags

def options(args):
    abilities = "Improved" if args.sketch_control_improved_abilities else "Original"
    accuracy = "100%" if args.sketch_control_improved_stats else "Original"
    stats = "Character" if args.sketch_control_improved_stats else "Original"

    sketch_abilities = ("Sketch Ability", abilities)
    sketch_stats = ("Sketch Stats", stats)
    sketch_accuracy = ("Sketch Accuracy", accuracy)

    control_abilities = ("Control Ability", abilities)
    control_stats = ("Control Stats", stats)
        
    return [
        sketch_abilities,
        sketch_accuracy,
        sketch_stats,
        ("", ""),
        control_abilities,
        control_stats,
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
