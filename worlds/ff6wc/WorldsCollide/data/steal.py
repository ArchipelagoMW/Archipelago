from ..memory.space import Bank, Reserve, Allocate, Write
from ..instruction import asm as asm

class Steal:
    def __init__(self, rom, args):
        self.rom = rom
        self.args = args

    def enable_steal_chances_always(self):
        #Always steal if the enemy has an item. 
        # If the enemy has both rare and common, the rare item will be stolen 3/8 of the time.
        space = Reserve(0x0239b7, 0x0239e4, "steal common vs rare logic", asm.NOP())
        space.add_label("SPACE_END", space.end_address + 1)
        space.write(
            asm.PHY(),
            asm.PHX(),
            asm.LDX(0x3308, asm.ABS_Y), # x = rare item
            asm.INY(),
            asm.LDA(0x3308, asm.ABS_Y), # a = common item
            asm.TAY(),                  # y = common item

            asm.CPX(0xff, asm.IMM8),    # rare steal exists?
            asm.BEQ("STEAL_COMMON"),    # if not, steal common item
            asm.CPY(0xff, asm.IMM8),    # common steal exists?
            asm.BEQ("STEAL_RARE"),      # if not, steal rare item
            asm.JSR(0x4b5a, asm.ABS),   # a = random number between 0 and 255
            asm.CMP(0x60, asm.IMM8),    # compare with 96
            asm.BLT("STEAL_RARE"),      # if a < 96 then steal rare item

            "STEAL_COMMON",
            asm.TYA(),                  # a = common item
            asm.BRA("STEAL_ITEM"),      # steal common item

            "STEAL_RARE",
            asm.TXA(),                  # a = rare item

            "STEAL_ITEM",
            asm.PLX(),
            asm.PLY(),
            asm.BRA("SPACE_END"),       # skip nops
        )

    def enable_steal_chances_higher(self):
        # Increase the Constant added to Attacker's Level from 50 (0x32) to 90 (0x5A)
        # Effectively increases chance of stealing for same-level targets from 50% to 90%
        # Reference on Steal function (starts at C2 399E):
        #  StealValue = Attacker's level + Constant - Target's level
        #  If Thief Glove equipped: StealValue *= 2
        #  If StealValue <= 0 then steal fails
        #  If StealValue >= 128 then you automatically steal
        #  If StealValue < Random Value (0-99), then you fail to steal
        #  Else Steal is successful
        space = Reserve(0x239BB, 0x239BB, "steal value constant")
        space.write(0x5A) # default: 0x32

        # Increase the Rare Steal Constant from 32 (0x20) to 96 (0x60)
        # Effectively increases probably of stealing a rare item from 1/8 to 3/8
        # Occurs after the StealValue calculation above
        # Reference on Rare Steals formula (starts at C2 39DB):
        #  Load Rare Item into Item-to-Steal slot
        #  If Rare Steal Constant > Random Value (0-255),  <- this occurs 7/8 of the time
        #    load Common item into Item-to-Steal slot instead
        #  If Item-to-Steal is not empty, acquire it and set both Common and Rare Items to empty
        #  Else Fail to steal
        space = Reserve(0x239DD, 0x239DD, "rare steal constant")
        space.write(0x60) # default: 0x20

    def mod(self):
        if self.args.steal_chances_higher:
            self.enable_steal_chances_higher()
        elif self.args.steal_chances_always:
            self.enable_steal_chances_always()

    def write(self):
        if self.args.spoiler_log:
            self.log()

    def log(self):
        pass
