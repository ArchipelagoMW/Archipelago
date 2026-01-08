from ..memory.space import Bank, START_ADDRESS_SNES, Write
from ..instruction import asm as asm
from ..instruction import field as field

from ..data import event_bit as event_bit
from ..data import event_word as event_word
from ..data import dialogs as dialogs

from ..objectives._cached_function import _CachedFunction

class Field(_CachedFunction, field.Call):
    def __init__(self, *args, **kwargs):
        _CachedFunction.__init__(self, *args, **kwargs)
        field.Call.__init__(self, self.address(*args, **kwargs))

    def write(self, objective):
        objective_event_bit = getattr(event_bit, "OBJECTIVE" + str(objective.id))
        src = [
            field.ReturnIfEventBitSet(objective_event_bit),
            objective.conditions_complete.field(),
            field.ReturnIfEventWordLess(event_word.SCRATCH, objective.conditions_required),

            objective.result.field(),

            field.SetEventBit(objective_event_bit),
            field.Dialog(dialogs.OBJECTIVES[objective.id]),
            field.Return(),
        ]
        return Write(Bank.CA, src, f"field check complete objective {objective.id}")

class Battle(_CachedFunction, asm.JSL):
    def __init__(self, *args, **kwargs):
        _CachedFunction.__init__(self, *args, **kwargs)
        asm.JSL.__init__(self, START_ADDRESS_SNES + self.address(*args, **kwargs))

    def write(self, objective):
        objective_event_bit = getattr(event_bit, "OBJECTIVE" + str(objective.id))
        bitmask = 2 ** event_bit.bit(objective_event_bit)
        src = [
            asm.LDA(event_bit.address(objective_event_bit), asm.ABS),
            asm.AND(bitmask, asm.IMM8),     # objective already complete?
            asm.BEQ("CHECK_CONDITIONS"),    # if not, check conditions
            asm.BRA("RETURN_FALSE"),        # else, skip showing complete message

            "CHECK_CONDITIONS",
            objective.conditions_complete.battle(),             # x = number conditions complete
            asm.CPX(objective.conditions_required, asm.IMM8),   # enough conditions complete for objective?
            asm.BLT("RETURN_FALSE"),                            # if not, return false

            objective.result.battle(),

            asm.LDA(event_bit.address(objective_event_bit), asm.ABS),
            asm.ORA(bitmask, asm.IMM8),
            asm.STA(event_bit.address(objective_event_bit), asm.ABS),   # set objective complete event bit

            asm.LDA(0x01, asm.IMM8),    # return true
            asm.RTL(),

            "RETURN_FALSE",
            asm.LDA(0x00, asm.IMM8),    # return false
            asm.RTL(),
        ]
        return Write(Bank.F0, src, "battle check objective" + str(objective.id))

class CheckComplete:
    def __init__(self, objective):
        self.objective = objective

    def field(self):
        return Field(self.objective)

    def battle(self):
        return Battle(self.objective)
