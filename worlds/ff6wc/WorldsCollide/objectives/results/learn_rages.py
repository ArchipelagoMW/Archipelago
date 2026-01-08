from ...objectives.results._objective_result import *
from ...instruction import f0 as f0

def _random_rage_table():
    from ...constants.rages import id_rage

    rage_table = list(range(len(id_rage)))
    random.shuffle(rage_table)

    space = Write(Bank.F0, rage_table, "learn rages random rage table")
    return space.start_address, len(rage_table)
random_rage_table, random_rage_table_size = _random_rage_table()

def _learn_random_rages():
    # input: 8 bit number of random rages to learn
    # output: learn next given number of rages in random_rage_table, skip rages already known
    learned_start_address = 0x1d2c
    rages_left = 0x30      # temporarily store number rages left to learn in field/battle scratch ram

    src = [
        asm.PHP(),
        asm.XY8(),
        asm.LDA(rages_left, asm.DIR),
        asm.PHA(),                                      # store value at $rages_left to be restored before returning

        asm.LDA(field.LongCall.ARG_ADDRESS, asm.DIR),   # a = number of rages to learn
        asm.STA(rages_left, asm.DIR),                   # $rages_left = number of rages left to learn
        asm.LDX(0x00, asm.IMM8),                        # x = rage table index

        "RAGE_LOOP_START",
        asm.LDA(START_ADDRESS_SNES + random_rage_table, asm.LNG_X), # a = random_rage[x]
        asm.PHX(),                                      # push rage table index
        asm.PHA(),                                      # push random rage
        asm.LSR(),
        asm.LSR(),
        asm.LSR(),                                      # a = random rage // 8
        asm.TAY(),                                      # y = random rage // 8
        asm.PLA(),                                      # a = random rage
        asm.AND(0x07, asm.IMM8),                        # a = random rage % 8
        asm.TAX(),                                      # x = random rage % 8
        asm.JSR(f0.set_bit_x, asm.ABS),                 # a = random rage bitmask
        asm.PLX(),                                      # x = rage table index
        asm.ORA(learned_start_address, asm.ABS_Y),      # set random rage bit
        asm.CMP(learned_start_address, asm.ABS_Y),      # is this rage already known?
        asm.BEQ("NEXT_RAGE"),                           # branch if rage already known
        asm.STA(learned_start_address, asm.ABS_Y),      # learn rage
        asm.DEC(rages_left, asm.DIR),                   # decrement number of rages left to learn
        asm.BEQ("RETURN"),
        "NEXT_RAGE",
        asm.INX(),                                      # next rage in table
        asm.CPX(random_rage_table_size, asm.IMM8),
        asm.BLT("RAGE_LOOP_START"),                     # branch if rage index < len(rage table)

        "RETURN",
        asm.PLA(),
        asm.STA(rages_left, asm.DIR),                   # restore original value at $rages_left
        asm.PLP(),
        asm.RTL(),
    ]
    space = Write(Bank.F0, src, "learn rages learn random rages")
    return space.start_address
learn_random_rages = _learn_random_rages()

class Field(field_result.Result):
    def src(self, count):
        return [
            field.LongCall(START_ADDRESS_SNES + learn_random_rages, count),
        ]

class Battle(battle_result.Result):
    def src(self, count):
        return [
            asm.LDA(count, asm.IMM8),
            asm.STA(field.LongCall.ARG_ADDRESS, asm.DIR),
            asm.JSL(START_ADDRESS_SNES + learn_random_rages),
        ]

class Result(ObjectiveResult):
    NAME = "Learn Rages"
    def __init__(self, min_count, max_count):
        self.count = random.randint(min_count, max_count)
        super().__init__(Field, Battle, self.count)
