from ...objectives.results._objective_result import *

def _learn_swdtechs():
    # input: 8 bit number of swdtechs to learn
    # output: learn next given number of swdtechs, skip swdtechs already known
    known_swdtechs_address = 0x1cf7

    src = [
        asm.PHP(),
        asm.AXY8(),
        asm.LDX(field.LongCall.ARG_ADDRESS, asm.DIR),   # x = number of swdtechs to learn
        asm.LDA(0x01, asm.IMM8),                        # a = first swdtech bit

        "SWDTECH_LOOP_START",
        asm.TSB(known_swdtechs_address, asm.ABS),       # learn swdtech
        asm.BNE("NEXT_SWDTECH"),                        # branch if swdtech was already known
        asm.DEX(),                                      # decrement number of swdtechs to learn
        asm.BEQ("RETURN"),                              # return if number of swdtechs left to learn is zero

        "NEXT_SWDTECH",
        asm.ASL(),                                      # next swdtech bit
        asm.BNE("SWDTECH_LOOP_START"),                  # branch if more swdtechs to check

        "RETURN",
        asm.PLP(),
        asm.RTL(),
    ]
    space = Write(Bank.F0, src, "learn swdtechs learn swdtechs")
    return space.start_address
learn_swdtechs = _learn_swdtechs()

class Field(field_result.Result):
    def src(self, count):
        return [
            field.LongCall(START_ADDRESS_SNES + learn_swdtechs, count),
        ]

class Battle(battle_result.Result):
    def src(self, count):
        return [
            asm.LDA(count, asm.IMM8),
            asm.STA(field.LongCall.ARG_ADDRESS, asm.DIR),
            asm.JSL(START_ADDRESS_SNES + learn_swdtechs),
        ]

class Result(ObjectiveResult):
    NAME = "Learn SwdTechs"
    def __init__(self, min_count, max_count):
        self.count = random.randint(min_count, max_count)
        super().__init__(Field, Battle, self.count)
