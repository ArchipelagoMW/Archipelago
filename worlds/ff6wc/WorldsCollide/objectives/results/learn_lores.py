from ...objectives.results._objective_result import *
from ...instruction import f0 as f0

def _random_lore_table():
    from ...constants.lores import id_lore

    lore_table = list(range(len(id_lore)))
    random.shuffle(lore_table)

    space = Write(Bank.F0, lore_table, "learn lores random lore table")
    return space.start_address, len(lore_table)
random_lore_table, random_lore_table_size = _random_lore_table()

def _learn_random_lores():
    # input: 8 bit number of random lores to learn
    # output: learn next given number of lores in random_lore_table, skip lores already known
    learned_start_address = 0x1d29
    lores_left = 0x30      # temporarily store number lores left to learn in field/battle scratch ram

    src = [
        asm.PHP(),
        asm.XY8(),
        asm.LDA(lores_left, asm.DIR),
        asm.PHA(),                                      # store value at $lores_left to be restored before returning

        asm.LDA(field.LongCall.ARG_ADDRESS, asm.DIR),   # a = number of lores to learn
        asm.STA(lores_left, asm.DIR),                   # $lores_left = number of lores left to learn
        asm.LDX(0x00, asm.IMM8),                        # x = lore table index

        "LORE_LOOP_START",
        asm.LDA(START_ADDRESS_SNES + random_lore_table, asm.LNG_X), # a = random_lore[x]
        asm.PHX(),                                      # push lore table index
        asm.PHA(),                                      # push random lore
        asm.LSR(),
        asm.LSR(),
        asm.LSR(),                                      # a = random lore // 8
        asm.TAY(),                                      # y = random lore // 8
        asm.PLA(),                                      # a = random lore
        asm.AND(0x07, asm.IMM8),                        # a = random lore % 8
        asm.TAX(),                                      # x = random lore % 8
        asm.JSR(f0.set_bit_x, asm.ABS),                 # a = random lore bitmask
        asm.PLX(),                                      # x = lore table index
        asm.ORA(learned_start_address, asm.ABS_Y),      # set random lore bit
        asm.CMP(learned_start_address, asm.ABS_Y),      # is this lore already known?
        asm.BEQ("NEXT_LORE"),                           # branch if lore already known
        asm.STA(learned_start_address, asm.ABS_Y),      # learn lore
        asm.DEC(lores_left, asm.DIR),                   # decrement number of lores left to learn
        asm.BEQ("RETURN"),
        "NEXT_LORE",
        asm.INX(),                                      # next lore in table
        asm.CPX(random_lore_table_size, asm.IMM8),
        asm.BLT("LORE_LOOP_START"),                     # branch if lore index < len(lore table)

        "RETURN",
        asm.PLA(),
        asm.STA(lores_left, asm.DIR),                   # restore original value at $lores_left
        asm.PLP(),
        asm.RTL(),
    ]
    space = Write(Bank.F0, src, "learn lores learn random lores")
    return space.start_address
learn_random_lores = _learn_random_lores()

class Field(field_result.Result):
    def src(self, count):
        return [
            field.LongCall(START_ADDRESS_SNES + learn_random_lores, count),
        ]

class Battle(battle_result.Result):
    def src(self, count):
        return [
            asm.LDA(count, asm.IMM8),
            asm.STA(field.LongCall.ARG_ADDRESS, asm.DIR),
            asm.JSL(START_ADDRESS_SNES + learn_random_lores),
        ]

class Result(ObjectiveResult):
    NAME = "Learn Lores"
    def __init__(self, min_count, max_count):
        self.count = random.randint(min_count, max_count)
        super().__init__(Field, Battle, self.count)
