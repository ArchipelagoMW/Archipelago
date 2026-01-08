from ..constants.commands import COMMAND_OPTIONS, RANDOM_COMMAND, RANDOM_UNIQUE_COMMAND, NONE_COMMAND, RANDOM_EXCLUDE_COMMANDS, id_name, name_id

def name():
    return "Commands"

def parse(parser):
    commands = parser.add_argument_group("Commands")
    commands.add_argument("-com", "--commands", type = str, help = "Character commands")
    commands.add_argument("-scc", "--shuffle-commands", action = "store_true", help = "Shuffle selected/randomized commands")
    commands.add_argument("-rec1", "--random-exclude-command1", type = int, choices = RANDOM_EXCLUDE_COMMANDS, metavar = "VALUE", default = NONE_COMMAND, help = "Exclude selected command from random possibilities")
    commands.add_argument("-rec2", "--random-exclude-command2", type = int, choices = RANDOM_EXCLUDE_COMMANDS, metavar = "VALUE", default = NONE_COMMAND, help = "Exclude selected command from random possibilities")
    commands.add_argument("-rec3", "--random-exclude-command3", type = int, choices = RANDOM_EXCLUDE_COMMANDS, metavar = "VALUE", default = NONE_COMMAND, help = "Exclude selected command from random possibilities")
    commands.add_argument("-rec4", "--random-exclude-command4", type = int, choices = RANDOM_EXCLUDE_COMMANDS, metavar = "VALUE", default = NONE_COMMAND, help = "Exclude selected command from random possibilities")
    commands.add_argument("-rec5", "--random-exclude-command5", type = int, choices = RANDOM_EXCLUDE_COMMANDS, metavar = "VALUE", default = NONE_COMMAND, help = "Exclude selected command from random possibilities")
    commands.add_argument("-rec6", "--random-exclude-command6", type = int, choices = RANDOM_EXCLUDE_COMMANDS, metavar = "VALUE", default = NONE_COMMAND, help = "Exclude selected command from random possibilities")

def process(args):
    if not args.commands:
        args.blitz_command_possible = True
        return

    digits = 2 # number of digits each command id substring is
    args.character_commands = [int(args.commands[index : index + digits]) for index in range(0, len(args.commands), digits)]

    args.command_strings = []
    for index, command in enumerate(args.character_commands):
        if command == RANDOM_COMMAND:
            args.command_strings.append("Random")
        elif command == RANDOM_UNIQUE_COMMAND:
            args.command_strings.append("Random Unique")
        elif command == NONE_COMMAND:
            args.command_strings.append("None")
        else:
            args.command_strings.append(id_name[command])

    args.random_exclude_commands = []
    if args.random_exclude_command1 != NONE_COMMAND:
        args.random_exclude_commands.append(args.random_exclude_command1)
    if args.random_exclude_command2 != NONE_COMMAND:
        args.random_exclude_commands.append(args.random_exclude_command2)
    if args.random_exclude_command3 != NONE_COMMAND:
        args.random_exclude_commands.append(args.random_exclude_command3)
    if args.random_exclude_command4 != NONE_COMMAND:
        args.random_exclude_commands.append(args.random_exclude_command4)
    if args.random_exclude_command5 != NONE_COMMAND:
        args.random_exclude_commands.append(args.random_exclude_command5)
    if args.random_exclude_command6 != NONE_COMMAND:
        args.random_exclude_commands.append(args.random_exclude_command6)

    random_exists = "Random" in args.command_strings or "Random Unique" in args.command_strings
    blitz_excluded = name_id["Blitz"] in args.random_exclude_commands
    args.blitz_command_possible = ("Blitz" in args.command_strings) or (random_exists and not blitz_excluded)

def flags(args):
    flags = ""

    if args.commands:
        flags += " -com " + args.commands

    if args.shuffle_commands:
        flags += " -scc"

    if args.random_exclude_command1 != NONE_COMMAND:
        flags += f" -rec1 {args.random_exclude_command1}"
    if args.random_exclude_command2 != NONE_COMMAND:
        flags += f" -rec2 {args.random_exclude_command2}"
    if args.random_exclude_command3 != NONE_COMMAND:
        flags += f" -rec3 {args.random_exclude_command3}"
    if args.random_exclude_command4 != NONE_COMMAND:
        flags += f" -rec4 {args.random_exclude_command4}"
    if args.random_exclude_command5 != NONE_COMMAND:
        flags += f" -rec5 {args.random_exclude_command5}"
    if args.random_exclude_command6 != NONE_COMMAND:
        flags += f" -rec6 {args.random_exclude_command6}"

    return flags

def options(args):
    result = []
    if args.commands is not None:
        for index, command_string in enumerate(args.command_strings):
            result.append((COMMAND_OPTIONS[index], command_string))
    else:
        for option in COMMAND_OPTIONS:
            result.append((option, option))

    result.append(("", ""))
    result.append(("Shuffle Commands", args.shuffle_commands))

    add_exclude_command = lambda command : result.append(("Random Exclude", "None" if command == NONE_COMMAND else id_name[command]))

    add_exclude_command(args.random_exclude_command1)
    add_exclude_command(args.random_exclude_command2)
    add_exclude_command(args.random_exclude_command3)
    add_exclude_command(args.random_exclude_command4)
    add_exclude_command(args.random_exclude_command5)
    add_exclude_command(args.random_exclude_command6)

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
