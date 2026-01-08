from multiprocessing.sharedctypes import Value
from ..constants.commands import *
import random
from .. import args as args

class Commands:
    def __init__(self, characters):
        self.characters = characters

    def mod_commands(self):
        command_set = set(name_id[name] for name in RANDOM_POSSIBLE_COMMANDS)
        command_list = list(command_set)

        allowed_commands = command_set | set([name_id["Fight"], RANDOM_COMMAND, RANDOM_UNIQUE_COMMAND, NONE_COMMAND])

        # if morph was explicitly selected remove from available command list
        morph_id = name_id["Morph"]
        for command in args.character_commands:
            if command == morph_id:
                command_list.remove(morph_id)

        for exclude_command in args.random_exclude_commands:
            try:
                command_set.discard(exclude_command)
                command_list.remove(exclude_command)
            except ValueError:
                pass

        from ..data.characters import Characters
        # Give the Moogles for Moogle Defense randomized commands
        # Copy the list minus any exclusions
        possible_moogle_commands = command_list.copy()
        # randomize commands for Moogles during Moogle Defense from the non-excluded set
        # Remove Morph to ensure only 1 character gets Morph
        # Remove Rage to avoid any issues with Randomized Atma weapon
        # Remove X-Magic as they won't have any Magic
        # Remove Blitz, SwdTech, Dance, and Lore because they won't have abilities within unless a party member does
        moogle_exclusions = [morph_id, name_id["Rage"], name_id["X Magic"], name_id["Blitz"], name_id["SwdTech"], name_id["Lore"], name_id["Dance"]]
        for exclude in moogle_exclusions:
            try:
                possible_moogle_commands.remove(exclude)
            except ValueError:
                pass
        if len(possible_moogle_commands) > 0:
            for index in range(Characters.FIRST_MOOGLE, Characters.LAST_MOOGLE + 1):
                self.characters[index].commands[1] = random.choice(possible_moogle_commands)

        # if suplex a train condition exists, guarantee blitz
        from .. import objectives as objectives
        blitz_id = name_id["Blitz"]
        if objectives.suplex_train_condition_exists and blitz_id not in args.character_commands:
            # try to replace a random "Random" or "Random Unique" command with Blitz (even if blitz in excluded commands)
            possible_indices = []
            for index, command in enumerate(args.character_commands):
                if command == RANDOM_COMMAND or command == RANDOM_UNIQUE_COMMAND:
                    possible_indices.append(index)

            if not possible_indices:
                # suplex a train explicitly picked and all commands explicitly picked (but none are blitz)
                # force a random command to be blitz instead
                possible_indices = list(range(len(args.character_commands)))

            random_index = random.choice(possible_indices)
            args.character_commands[random_index] = blitz_id
            command_set.discard(blitz_id)

        for index, command in enumerate(args.character_commands):
            if command not in allowed_commands and (index != 0 or command != name_id["Morph"]) and (index != 12 or command != name_id["Leap"]):
                raise ValueError(f"Invalid character command {command}")
            elif command == RANDOM_COMMAND:
                args.character_commands[index] = random.choice(command_list)
                if args.character_commands[index] == morph_id:
                    command_list.remove(morph_id) # only one character gets morph
            elif command == NONE_COMMAND:
                args.character_commands[index] = name_id["None"]

            command_set.discard(args.character_commands[index])

        for index, command in enumerate(args.character_commands):
            if command == RANDOM_UNIQUE_COMMAND:
                args.character_commands[index] = random.choice(tuple(command_set))
                command_set.discard(args.character_commands[index])

        # apply the commands to the characters
        for index in range(len(args.character_commands[ : -2])):
            self.characters[index].commands[1] = args.character_commands[index]
        self.characters[Characters.GAU].commands[0] = args.character_commands[-2] # rage
        self.characters[Characters.GAU].commands[1] = args.character_commands[-1] # leap

    def shuffle_commands(self):
        from ..data.characters import Characters

        commands = []
        for index in range(len(COMMAND_OPTIONS) - 1):
            commands.append(self.characters[index].commands[1])
        commands.append(self.characters[Characters.GAU].commands[0]) # rage

        random.shuffle(commands)

        for index in range(len(COMMAND_OPTIONS) - 1):
            self.characters[index].commands[1] = commands[index]
        self.characters[Characters.GAU].commands[0] = commands[-1] # rage

    def mod(self):
        from ..data import characters_asm as characters_asm
        from ..data.characters import Characters

        if args.commands:
            self.mod_commands()
        if args.shuffle_commands:
            self.shuffle_commands()

        if args.commands or args.shuffle_commands:
            characters_asm.update_morph_character(self.characters[ : Characters.CHARACTER_COUNT])

    def log(self):
        from ..log import section, format_option
        from ..data.characters import Characters

        lcolumn = []
        for index, option in enumerate(COMMAND_OPTIONS[ : -2]):
            lcolumn.append(format_option(option, id_name[self.characters[index].commands[1]]))
        lcolumn.append(format_option(COMMAND_OPTIONS[-2], id_name[self.characters[Characters.GAU].commands[0]]))
        lcolumn.append(format_option(COMMAND_OPTIONS[-1], id_name[self.characters[Characters.GAU].commands[1]]))

        section("Commands", lcolumn, [])
