from ...objectives.results._objective_result import *

def _random_blitz_table():
    from ...constants.blitzes import id_blitz

    blitz_table = [2 ** index for index in range(len(id_blitz))]
    random.shuffle(blitz_table)

    space = Write(Bank.F0, blitz_table, "learn blitzes random blitz table")
    return space.start_address, len(blitz_table)
random_blitz_table, random_blitz_table_size = _random_blitz_table()

def _set_bum_rush_learned():
    from ...data import event_bit as event_bit
    from ...data import npc_bit as npc_bit

    # set learned event bit and update duncan npc
    learned_bum_rush_address = event_bit.address(event_bit.LEARNED_BUM_RUSH)
    learned_bum_rush_bit = event_bit.bit(event_bit.LEARNED_BUM_RUSH)

    duncan_training_address = npc_bit.address(npc_bit.DUNCAN_TRAINING)
    duncan_training_bit = npc_bit.bit(npc_bit.DUNCAN_TRAINING)

    duncan_standing_address = npc_bit.address(npc_bit.DUNCAN_STANDING)
    duncan_standing_bit = npc_bit.bit(npc_bit.DUNCAN_STANDING)

    src = [
        asm.LDA(2 ** learned_bum_rush_bit, asm.IMM8),
        asm.TSB(learned_bum_rush_address, asm.ABS),

        asm.LDA(2 ** duncan_training_bit, asm.IMM8),
        asm.TRB(duncan_training_address, asm.ABS),

        asm.LDA(2 ** duncan_standing_bit, asm.IMM8),
        asm.TSB(duncan_standing_address, asm.ABS),

        asm.RTS(),
    ]
    space = Write(Bank.F0, src, "learn blitzes set bum rush learned")
    return space.start_address
set_bum_rush_learned = _set_bum_rush_learned()

def _learn_random_blitzes():
    # input: 8 bit number of random blitzes to learn
    # output: learn next given number of blitzes in random_blitz_table, skip blitzes already known
    known_blitzes_address = 0x1d28
    bum_rush_bit = 0x80

    src = [
        asm.PHP(),
        asm.XY8(),
        asm.LDY(field.LongCall.ARG_ADDRESS, asm.DIR),   # y = number of blitzes to learn
        asm.LDX(0x00, asm.IMM8),                        # x = blitz table index

        "BLITZ_LOOP_START",
        asm.LDA(START_ADDRESS_SNES + random_blitz_table, asm.LNG_X),# a = bitmask of random_blitz[x]
        asm.TSB(known_blitzes_address, asm.ABS),        # learn blitz
        asm.BNE("NEXT_BLITZ"),                          # branch if blitz was already known
        asm.CMP(bum_rush_bit, asm.IMM8),                # learned bum rush?
        asm.BNE("DECREMENT_TO_LEARN"),                  # branch if not
        asm.JSR(set_bum_rush_learned, asm.ABS),         # mark bum rush learned and update duncan
        "DECREMENT_TO_LEARN",
        asm.DEY(),                                      # decrement number of blitzes to learn
        asm.BEQ("RETURN"),                              # return if number of blitzes to learn is zero
        "NEXT_BLITZ",
        asm.INX(),                                      # next blitz in table
        asm.CPX(random_blitz_table_size, asm.IMM8),
        asm.BLT("BLITZ_LOOP_START"),                    # branch if blitz index < len(blitz table)

        "RETURN",
        asm.PLP(),
        asm.RTL(),
    ]
    space = Write(Bank.F0, src, "learn blitzes learn random blitzes")
    return space.start_address
learn_random_blitzes = _learn_random_blitzes()

class Field(field_result.Result):
    def src(self, count):
        return [
            field.LongCall(START_ADDRESS_SNES + learn_random_blitzes, count),
        ]

class Battle(battle_result.Result):
    def src(self, count):
        return [
            asm.LDA(count, asm.IMM8),
            asm.STA(field.LongCall.ARG_ADDRESS, asm.DIR),
            asm.JSL(START_ADDRESS_SNES + learn_random_blitzes),
        ]

class Result(ObjectiveResult):
    NAME = "Learn Blitzes"
    def __init__(self, min_count, max_count):
        self.count = random.randint(min_count, max_count)
        super().__init__(Field, Battle, self.count)
