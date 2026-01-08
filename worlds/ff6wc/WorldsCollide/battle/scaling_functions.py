from ..memory.space import Bank, Write
from ..instruction import asm as asm
from ..instruction import c2 as c2
from .. import args as args

class ScalingFunctions():
    def __init__(self):
        self.min_max_bound_mod()

        self.party_average_level_mod()
        self.party_highest_level_mod()
        self.ce_mod()
        self.ced_mod()
        self.checks_mod()
        self.time_mod()
        self.bosses_dragons_mod()

        if args.level_scaling_average:
            self.level = self.party_average_level
        elif args.level_scaling_highest:
            self.level = self.party_highest_level
        elif args.level_scaling_ce:
            self.level = self.ce
        elif args.level_scaling_ced:
            self.level = self.ced
        elif args.level_scaling_checks:
            self.level = self.checks
        elif args.level_scaling_bosses_dragons:
            self.level = self.bosses_dragons
        elif args.level_scaling_time:
            self.level = self.time
        else:
            self.level = None

        if args.hp_mp_scaling_average:
            self.hp_mp = self.party_average_level
        elif args.hp_mp_scaling_highest:
            self.hp_mp = self.party_highest_level
        elif args.hp_mp_scaling_ce:
            self.hp_mp = self.ce
        elif args.hp_mp_scaling_ced:
            self.hp_mp = self.ced
        elif args.hp_mp_scaling_checks:
            self.hp_mp = self.checks
        elif args.hp_mp_scaling_bosses_dragons:
            self.hp_mp = self.bosses_dragons
        elif args.hp_mp_scaling_time:
            self.hp_mp = self.time
        else:
            self.hp_mp = None

        if args.xp_gp_scaling_average:
            self.xp_gp = self.party_average_level
        elif args.xp_gp_scaling_highest:
            self.xp_gp = self.party_highest_level
        elif args.xp_gp_scaling_ce:
            self.xp_gp = self.ce
        elif args.xp_gp_scaling_ced:
            self.xp_gp = self.ced
        elif args.xp_gp_scaling_checks:
            self.xp_gp = self.checks
        elif args.xp_gp_scaling_bosses_dragons:
            self.xp_gp = self.bosses_dragons
        elif args.xp_gp_scaling_time:
            self.xp_gp = self.time
        else:
            self.xp_gp = None

    def min_max_bound_mod(self):
        # input: a = 16 bit level
        # clamp value to [3, max_scale_level]

        src = [
            asm.CMP(3, asm.IMM16),
            asm.BGE("CHECK_MAX"),
            asm.LDA(3, asm.IMM16),
            asm.BRA("RETURN"),

            "CHECK_MAX",
            asm.CMP(args.max_scale_level, asm.IMM16),
            asm.BLT("RETURN"),
            asm.LDA(args.max_scale_level, asm.IMM16),

            "RETURN",
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "c2 min max bound")
        self.min_max_bound = space.start_address

    def party_average_level_mod(self):
        # output: 16 bit a = party level sum / party size

        party_size = 0xe8
        party_level_sum = 0xea
        src = [
            asm.PHP(),
            asm.AXY16(),

            asm.LDX(0x0000, asm.IMM16),             # character slot pointer index
            asm.STX(party_level_sum, asm.ABS),      # party level sum = 0
            asm.STX(party_size, asm.ABS),           # party character count = 0

            "SLOT_LOOP_START",
            asm.LDA(0x3010, asm.ABS_X),             # a = pointer to character slot x data
            asm.CMP(0xffff, asm.IMM16),             # character slot empty?
            asm.BEQ("NEXT_SLOT"),                   # if so, go to next slot
            asm.TAY(),                              # y = pointer to character slot x data
            asm.LDA(0x1608, asm.ABS_Y),             # a = character x's level
            asm.AND(0x00ff, asm.IMM16),             # extract 8 bit level
            asm.ADC(party_level_sum, asm.ABS),      # add to level sum
            asm.STA(party_level_sum, asm.ABS),
            asm.INC(party_size, asm.ABS),           # increment character count

            "NEXT_SLOT",
            asm.INX(),
            asm.INX(),
            asm.CPX(0x0008, asm.IMM16),             # all 4 character slots done?
            asm.BLT("SLOT_LOOP_START"),             # branch if not

            asm.LDX(party_size, asm.ABS),           # x = number of characters in party
            asm.LDA(party_level_sum, asm.ABS),      # a = party member's level sum
            asm.JSR(c2.divide, asm.ABS),            # a = level sum / party size

            asm.PLP(),
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "scaling function party average level")
        self.party_average_level = space.start_address

    def party_highest_level_mod(self):
        # output: 16 bit a = highest party member level

        highest_level = 0xe8
        src = [
            asm.PHP(),
            asm.AXY16(),

            asm.LDX(0x0000, asm.IMM16),             # character slot pointer index
            asm.STX(highest_level, asm.ABS), # scale level = 0

            "SLOT_LOOP_START",
            asm.LDA(0x3010, asm.ABS_X),             # a = pointer to character slot x data
            asm.CMP(0xffff, asm.IMM16),             # character slot empty?
            asm.BEQ("NEXT_SLOT"),                   # if so, go to next slot
            asm.TAY(),                              # y = pointer to character slot x data
            asm.LDA(0x1608, asm.ABS_Y),             # a = character x's level
            asm.AND(0x00ff, asm.IMM16),             # extract 8 bit level
            asm.CMP(highest_level, asm.ABS),        # compare to current highest level
            asm.BLT("NEXT_SLOT"),
            asm.STA(highest_level, asm.ABS),        # update highest level

            "NEXT_SLOT",
            asm.INX(),
            asm.INX(),
            asm.CPX(0x0008, asm.IMM16),             # all 4 character slots done?
            asm.BLT("SLOT_LOOP_START"),             # branch if not

            asm.LDA(highest_level, asm.ABS),        # a = party highest level
            asm.PLP(),
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "scaling function party highest level")
        self.party_highest_level = space.start_address

    def ce_mod(self):
        # output: 16 bit a = characters recruited + espers found

        from ..data import event_word as event_word
        espers_found_address = event_word.address(event_word.ESPERS_FOUND)

        src = [
            asm.PHP(),
            asm.AXY16(),

            asm.LDA(0x1edc, asm.ABS),               # a = recruited characters event bytes
            asm.CLC(),
            asm.JSR(0x520e, asm.ABS),               # x = number of bits set in a
            asm.TXA(),
            asm.AND(0x00ff, asm.IMM16),             # a = number of recruited characters
            asm.CLC(),
            asm.ADC(espers_found_address, asm.ABS), # a = characters recruited + espers found

            asm.PLP(),
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "scaling function ce")
        self.ce = space.start_address

    def ced_mod(self):
        # output: 16 bit a = characters recruited + espers found + dragons defeated

        from ..data import event_word as event_word
        dragons_defeated_address = event_word.address(event_word.DRAGONS_DEFEATED)

        src = [
            asm.PHP(),
            asm.AXY16(),

            asm.JSR(self.ce, asm.ABS),              # a = characters recruited + espers found
            asm.CLC(),
            asm.ADC(dragons_defeated_address, asm.ABS), # a = characters + espers + dragons

            asm.PLP(),
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "scaling function ced")
        self.ced = space.start_address

    def checks_mod(self):
        # output: 16 bit a = checks completed

        from ..data import event_word as event_word
        checks_complete_address = event_word.address(event_word.CHECKS_COMPLETE)

        src = [
            asm.PHP(),
            asm.AXY16(),

            asm.LDA(checks_complete_address, asm.ABS),  # a = checks completed

            asm.PLP(),
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "scaling function checks")
        self.checks = space.start_address

    def bosses_dragons_mod(self):
        # output: 16 bit a = bosses completed

        from ..data import event_word as event_word
        boss_complete_address = event_word.address(event_word.BOSSES_DEFEATED)
        dragons_defeated_address = event_word.address(event_word.DRAGONS_DEFEATED)

        src = [
            asm.PHP(),
            asm.AXY16(),

            asm.LDA(boss_complete_address, asm.ABS),  # a = bosses defeated
            asm.CLC(),
            asm.ADC(dragons_defeated_address, asm.ABS), # a = bosses + dragons defeated

            asm.PLP(),
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "scaling function bosses")
        self.bosses_dragons = space.start_address

    def time_mod(self):
        # output: 16 bit a = game time in minutes

        src = [
            asm.PHP(),
            asm.AXY16(),

            asm.LDA(0x021c, asm.ABS),               # a = seconds, minutes
            asm.AND(0x00ff, asm.IMM16),             # extract minutes
            asm.STA(0xea, asm.DIR),
            asm.LDA(0x021b, asm.ABS),               # a = minutes, hours
            asm.AND(0x00ff, asm.IMM16),             # extract hours
            asm.ORA(0x3c00, asm.IMM16),             # high byte a = 60
            asm.JSR(c2.multiply, asm.ABS),          # a = hours * 60
            asm.CLC(),
            asm.ADC(0xea, asm.DIR),                 # a = hours * 60 + minutes

            asm.PLP(),
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "scaling function time")
        self.time = space.start_address
