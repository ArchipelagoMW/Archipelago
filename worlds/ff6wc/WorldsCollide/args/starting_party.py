def name():
    return "Starting Party"

def parse(parser):
    starting_party = parser.add_argument_group("Starting Party")

    from ..data.characters import Characters
    character_options = [name.lower() for name in Characters.DEFAULT_NAME]
    character_options.append("random")
    character_options.append("randomngu")

    starting_party.add_argument("-sc1", "--start-char1", default = "", type = str.lower, choices = character_options,
                                help = "Starting party member")
    starting_party.add_argument("-sc2", "--start-char2", default = "", type = str.lower, choices = character_options,
                                help = "Starting party member")
    starting_party.add_argument("-sc3", "--start-char3", default = "", type = str.lower, choices = character_options,
                                help = "Starting party member")
    starting_party.add_argument("-sc4", "--start-char4", default = "", type = str.lower, choices = character_options,
                                help = "Starting party member")

def process(args):
    # convert arguments to list of starting party
    args.start_chars = []
    if args.start_char1:
        args.start_chars.append(args.start_char1)
    if args.start_char2:
        args.start_chars.append(args.start_char2)
    if args.start_char3:
        args.start_chars.append(args.start_char3)
    if args.start_char4:
        args.start_chars.append(args.start_char4)

    if not args.start_chars:
        # no starting characters specified, pick one random starting character
        args.start_chars = ["random"]
    else:
        # ensure only 4 starting characters and no duplicates (except random)
        assert len(args.start_chars) <= 4
        start_chars_found = set()
        for char in args.start_chars:
            assert (char == "random" or char == "randomngu" or char not in start_chars_found)
            start_chars_found.add(char)

def flags(args):
    flags = ""

    if args.start_char1:
        flags += f" -sc1 {args.start_char1}"
    if args.start_char2:
        flags += f" -sc2 {args.start_char2}"
    if args.start_char3:
        flags += f" -sc3 {args.start_char3}"
    if args.start_char4:
        flags += f" -sc4 {args.start_char4}"

    return flags

def options(args):
    result = []
    start_chars = [args.start_char1, args.start_char2, args.start_char3, args.start_char4]
    for start_char in start_chars:
        value = "None"
        if start_char == "randomngu":
            value = "Random (No Gogo/Umaro)"
        elif start_char:
            value = start_char.capitalize()

        result.append(("Start Character", value))
    return result

def menu(args):
    entries = options(args)
    for index, entry in enumerate(entries):
        entries[index] = (entry[1], "")
    return (name(), entries)

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        log.append(format_option(*entry))

    return log
