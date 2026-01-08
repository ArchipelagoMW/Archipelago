id_name = {
    0   : "Fight",
    1   : "Item",
    2   : "Magic",
    3   : "Morph",
    4   : "Revert",
    5   : "Steal",
    6   : "Capture",
    7   : "SwdTech",
    8   : "Throw",
    9   : "Tools",
    10  : "Blitz",
    11  : "Runic",
    12  : "Lore",
    13  : "Sketch",
    14  : "Control",
    15  : "Slot",
    16  : "Rage",
    17  : "Leap",
    18  : "Mimic",
    19  : "Dance",
    20  : "Row",
    21  : "Def",
    22  : "Jump",
    23  : "X Magic",
    24  : "GP Rain",
    25  : "Summon",
    26  : "Health",
    27  : "Shock",
    28  : "Possess",
    29  : "MagiTek",
    30  : "Empty?", # broken? selecting with cursor crashes game
    31  : "Empty",  # cursor can hover over empty but not select
    255 : "None",
}
name_id = {v: k for k, v in id_name.items()}

# random/none arguments (not actual command ids)
RANDOM_COMMAND = 99
RANDOM_UNIQUE_COMMAND = 98
NONE_COMMAND = 97   # none command id is 3 digits in base 10 (255), use a custom 2 digit value for args

COMMAND_OPTIONS = ["Morph", "Steal", "SwdTech", "Throw", "Tools", "Blitz", "Runic", "Lore", "Sketch", "Slot", "Dance", "Rage", "Leap"]
EXCLUDE_COMMANDS = ["Item", "Magic", "Revert", "Leap", "Mimic", "Row", "Def", "Summon", "Empty", "Empty?", "None"]

RANDOM_POSSIBLE_COMMANDS = [option for option in sorted(name_id.keys()) if option not in EXCLUDE_COMMANDS and option != "Fight"]
RANDOM_EXCLUDE_COMMANDS = [NONE_COMMAND] + [name_id[option] for option in RANDOM_POSSIBLE_COMMANDS]
