from ..memory.space import Bank, Reserve, Write
from ..instruction import asm as asm
from .. import args as args

class Retort:
    def __init__(self):
        if args.fix_retort:
            self.mod()

    def mod(self):
        # petrify/zombie/death call c246a9 which marks the entity as dead at 0x3a56
        # this causes cyan's retort to skip checking if it is a normal attack at c24c95
        #   and skip checking if he is the target of the attack and not attacking self at c24c9b
        # to fix this, clear the character's bit at 0x3a56 when revived/unzombied/unpetrified
        src = [
            asm.JSR(0x469c, asm.ABS),   # call original function this function call replaced

            asm.LDA(0x3018, asm.ABS_Y), # a = mask for entity y
            asm.TRB(0x3a56, asm.ABS),   # clear entity bit
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "retort bug fix")
        retort_fix = space.start_address

        space = Reserve(0x245f2, 0x245f4, "call retort bug fix when removing petrify/death")
        space.write(
            asm.JSR(retort_fix, asm.ABS),
        )

        space = Reserve(0x245ae, 0x245b0, "call retort bug fix when removing zombie")
        space.write(
            asm.JSR(retort_fix, asm.ABS),
        )

        # the second part of the bug is using retort and then inflicting cyan with imp
        # this will cause the next attack targeting cyan to counter with a normal attack which will not clear the retort bit
        # as a result, cyan will counter every attack with a normal attack
        # fix this by clearing the retort bit when a character has imp set (or cleared):
        src = [
            asm.INC(0x2f30, asm.ABS_X), # original instruction this function call replaced

            asm.TYX(),                  # x = entity slot * 2
            asm.LSR(0x3e4c, asm.ABS_X), # clear retort bit (0x01)
            asm.ASL(0x3e4c, asm.ABS_X), # restore other bits
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "imp retort bug fix")
        retort_fix = space.start_address

        space = Reserve(0x245ed, 0x245ef, "call imp retort bug fix when setting/clearing imp status")
        space.write(
            asm.JSR(retort_fix, asm.ABS),
        )
