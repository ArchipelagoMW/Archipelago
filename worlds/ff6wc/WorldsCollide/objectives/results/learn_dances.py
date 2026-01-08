from ...objectives.results._objective_result import *

def _random_dance_table():
    from ...constants.dances import id_dance

    dance_table = [2 ** index for index in range(len(id_dance))]
    random.shuffle(dance_table)

    space = Write(Bank.F0, dance_table, "learn dances random dance table")
    return space.start_address, len(dance_table)
random_dance_table, random_dance_table_size = _random_dance_table()

def _learn_random_dances():
    # input: 8 bit number of random dances to learn
    # output: learn next given number of dances in random_dance_table, skip dances already known
    known_dances_address = 0x1d4c

    src = [
        asm.PHP(),
        asm.XY8(),
        asm.LDY(field.LongCall.ARG_ADDRESS, asm.DIR),   # y = number of dances to learn
        asm.LDX(0x00, asm.IMM8),                        # x = dance table index

        "DANCE_LOOP_START",
        asm.LDA(START_ADDRESS_SNES + random_dance_table, asm.LNG_X),    # a = bitmask of random_dance[x]
        asm.TSB(known_dances_address, asm.ABS),                         # learn dance
        asm.BNE("NEXT_DANCE"),                          # branch if dance was already known
        asm.DEY(),                                      # decrement number of dances to learn
        asm.BEQ("RETURN"),                              # return if number of dances to learn is zero
        "NEXT_DANCE",
        asm.INX(),                                      # next dance in table
        asm.CPX(random_dance_table_size, asm.IMM8),
        asm.BLT("DANCE_LOOP_START"),                    # branch if dance index < len(dance table)

        "RETURN",
        asm.PLP(),
        asm.RTL(),
    ]
    space = Write(Bank.F0, src, "learn dances learn random dances")
    return space.start_address
learn_random_dances = _learn_random_dances()

class Field(field_result.Result):
    def src(self, count):
        return [
            field.LongCall(START_ADDRESS_SNES + learn_random_dances, count),
        ]

class Battle(battle_result.Result):
    def src(self, count):
        return [
            asm.LDA(count, asm.IMM8),
            asm.STA(field.LongCall.ARG_ADDRESS, asm.DIR),
            asm.JSL(START_ADDRESS_SNES + learn_random_dances),
        ]

class Result(ObjectiveResult):
    NAME = "Learn Dances"
    def __init__(self, min_count, max_count):
        self.count = random.randint(min_count, max_count)
        super().__init__(Field, Battle, self.count)
