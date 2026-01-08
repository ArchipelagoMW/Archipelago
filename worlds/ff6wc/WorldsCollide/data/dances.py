from ..data.dance import Dance
from ..data.structures import DataArray

from ..memory.space import Bank, Reserve, Allocate, Write, Read
from ..instruction import asm as asm

class Dances:
    DANCE_COUNT = 8

    DATA_START = 0x0ffe80
    DATA_END = 0x0ffe9f
    DATA_SIZE = 4

    NAMES_START = 0x26ff9d
    NAMES_END = 0x26ffff
    NAME_SIZE = 12

    ABILITY_NAMES_START = 0x26f881
    ABILITY_NAME_SIZE = 10

    def __init__(self, rom, args, characters):
        self.rom = rom
        self.args = args
        self.characters = characters

        self.data = DataArray(self.rom, self.DATA_START, self.DATA_END, self.DATA_SIZE)
        self.name_data = DataArray(self.rom, self.NAMES_START, self.NAMES_END, self.NAME_SIZE)

        self.dances = []
        for dance_index in range(len(self.data)):
            dance = Dance(dance_index, self.data[dance_index], self.name_data[dance_index])
            self.dances.append(dance)

        self.start_dances = 0

    def write_learners_table(self):
        self.learners = self.characters.get_characters_with_command("Dance")

        space = Allocate(Bank.CF, self.characters.CHARACTER_COUNT, "dance learners")
        space.write(self.learners)

        self.learners_table = space.start_address
        self.learners_table_end = self.learners_table + len(self.learners)

    def write_is_learner(self):
        from ..instruction import c0 as c0

        src = [
            asm.PHP(),
            asm.XY16(),
            asm.PHX(),
            asm.PHY(),
            asm.LDX(self.learners_table_end, asm.IMM16),    # offset in bank to last learner in table + 1
            asm.LDY(len(self.learners), asm.IMM16),         # learners table size
            asm.JSR(c0.is_skill_learner, asm.ABS),
            asm.PLY(),
            asm.PLX(),
            asm.PLP(),
            asm.RTL(),
        ]
        space = Write(Bank.C0, src, "dance is learner")
        self.is_learner_function = space.start_address_snes

    def after_battle_check_mod(self):
        from ..memory.space import START_ADDRESS_SNES
        from ..instruction import c0 as c0

        character_available = START_ADDRESS_SNES + c0.character_available

        # NOTE: dances are learned by being in the party
        #       on the veldt, the character to possibly appear is added to the party and hidden
        #       this means the invisible character who may or may not show up after battle can still learn abilities
        #       to fix this, CHARACTER_AVAILABLE is called to filter out leapt or not yet recruited characters
        space = Allocate(Bank.C2, 47, "dance check after battle", asm.NOP())
        space.write(
            asm.LDX(0x00, asm.IMM8),            # x = party slot 0
            "LEARNER_CHECK_LOOP",
            asm.TDC(),
            asm.LDA(0x3ed9, asm.ABS_X),         # a = character id
            asm.CMP(0xff, asm.IMM8),            # no character in this slot?
            asm.BEQ("LOOP_INCREMENT"),          # branch to next slot if no character in this slot
            asm.JSL(character_available),
            asm.CMP(0x00, asm.IMM8),            # compare result with 0
            asm.BEQ("LOOP_INCREMENT"),          # branch if character not available
        )
        if self.args.dances_everyone_learns:
            space.write(
                asm.BRA("RETURN_DANCE"),
            )
        else:
            space.write(
                asm.LDA(0x3ed9, asm.ABS_X),     # a = character id
                asm.JSL(self.is_learner_function),
                asm.CMP(0x00, asm.IMM8),        # compare result with 0
                asm.BNE("RETURN_DANCE"),        # branch if character can learn
            )
        space.write(
            "LOOP_INCREMENT",
            asm.INX(),
            asm.INX(),
            asm.CPX(0x08, asm.IMM8),
            asm.BNE("LEARNER_CHECK_LOOP"),      # branch if haven't checked all 4 party members

            asm.LDA(0xff, asm.IMM8),            # return no dance
            asm.BRA("RETURN"),

            "RETURN_DANCE",
            asm.LDX(0x11e2, asm.ABS),           # load battle background
            asm.LDA(0xed8e5b, asm.LNG_X),       # load dance for the background

            "RETURN",
            asm.RTS(),
        )
        get_dance = space.start_address

        space = Reserve(0x25ee5, 0x25ef0, "dance check mog in party", asm.NOP())
        space.write(
            asm.JSR(get_dance, asm.ABS),
        )

    def no_stumble(self):
        space = Reserve(0x2179d, 0x217a1, "randomly fail 50% of dances with mismatching background", asm.NOP())
        space = Reserve(0x217af, 0x217c6, "execute dance stumble", asm.NOP())

    def set_start_dances(self, dance_bits):
        self.start_dances = dance_bits

        src = [
            Read(0x0be2c, 0x0be2e),   # initialize wallpaper index to zero

            asm.LDA(dance_bits, asm.IMM8),
            asm.STA(0x1d4c, asm.ABS),
            asm.RTS(),
        ]
        space = Write(Bank.C0, src, "initialize start dances")
        initialize_dances = space.start_address

        space = Reserve(0x0be2c, 0x0be2e, "initialize wallpaper index to zero", asm.NOP())
        space.write(
            asm.JSR(initialize_dances, asm.ABS),
        )

    def start_random_dances(self):
        import random

        number_initial_dances = random.randint(self.args.start_dances_random_min, self.args.start_dances_random_max)
        initial_dances = random.sample(range(self.DANCE_COUNT), number_initial_dances)

        dance_bits = 0
        for dance_index in initial_dances:
            dance_bits |= 1 << dance_index
        self.set_start_dances(dance_bits)

    def shuffle(self):
        abilities = []
        for dance in self.dances:
            abilities.extend(dance.dances)

        import random
        random.shuffle(abilities)

        for dance_index, dance in enumerate(self.dances):
            ability_index = dance_index * self.DATA_SIZE
            dance.dances = abilities[ability_index : ability_index + self.DATA_SIZE]

    def mod(self):
        self.write_learners_table()
        self.write_is_learner()
        self.after_battle_check_mod()

        if self.args.dances_no_stumble:
            self.no_stumble()

        if self.args.start_dances_random:
            self.start_random_dances()

        if self.args.dances_shuffle:
            self.shuffle()

    def write(self):
        if self.args.spoiler_log:
            self.log()

        for dance_index, dance in enumerate(self.dances):
            self.data[dance_index] = dance.data()
            self.name_data[dance_index] = dance.name_data()

        self.data.write()
        self.name_data.write()

    def log(self):
        from ..data import text as text
        from ..log import section_entries, format_option

        # TODO create abilities class to hold data/names and pass it to dances instead of reading names here
        #      dance abilities are also used by various enemies
        names = []
        for dance_index in range(len(self.dances) * self.DATA_SIZE):
            name_address = self.ABILITY_NAMES_START + dance_index * self.ABILITY_NAME_SIZE
            name_bytes = self.rom.get_bytes(name_address, self.ABILITY_NAME_SIZE)
            name = text.get_string(name_bytes, text.TEXT2)
            names.append(name.rstrip('\0'))

        lentries = []
        rentries = []
        FIRST_DANCE_ID = 101 # wind slash id
        for dance_index, dance in enumerate(self.dances):
            start = "*" if self.start_dances & (1 << dance_index) else " "
            entry = [start + dance.get_name()]
            for ability in dance.dances:
                name_index = ability - FIRST_DANCE_ID # convert dance ability index to name index
                entry.append(format_option(names[name_index], ""))

            if dance_index % 2:
                rentries.append(entry)
            else:
                lentries.append(entry)

        lentries.append(["", "* = Starting Dance"])

        section_entries("Dances", lentries, rentries)

    def print(self):
        for dance in self.dances:
            dance.print()
