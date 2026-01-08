from ..memory.space import Bank, Write
from ..instruction import asm as asm
from ..instruction import field as field

from ..data import event_word as event_word
from ..objectives._cached_function import _CachedFunction

class Field(_CachedFunction, field.Call):
    def __init__(self, *args, **kwargs):
        _CachedFunction.__init__(self, *args, **kwargs)
        field.Call.__init__(self, self.address(*args, **kwargs))

    def write(self, conditions):
        src = [
            field.SetEventWord(event_word.SCRATCH, 0),
        ]
        for condition in conditions:
            src += [
                condition,
            ]
        src += [
            field.Return(),
        ]
        return Write(Bank.CA, src, f"conditions complete field {str(conditions)}")

class Battle(_CachedFunction, asm.JSR):
    def __init__(self, *args, **kwargs):
        _CachedFunction.__init__(self, *args, **kwargs)
        asm.JSR.__init__(self, self.address(*args, **kwargs), asm.ABS)

    def write(self, conditions):
        src = [
            asm.LDX(0x00, asm.IMM8),
        ]
        for condition in conditions:
            src += [
                condition,
            ]
        src += [
            asm.RTS(),
        ]
        return Write(Bank.F0, src, f"conditions complete battle {str(conditions)}")

class Menu(_CachedFunction, asm.JSR):
    def __init__(self, *args, **kwargs):
        _CachedFunction.__init__(self, *args, **kwargs)
        asm.JSR.__init__(self, self.address(*args, **kwargs), asm.ABS)

    def write(self, conditions):
        src = [
            asm.LDX(0x00, asm.IMM8),
        ]
        for condition in conditions:
            src += [
                condition,
            ]
        src += [
            asm.RTS(),
        ]
        return Write(Bank.F0, src, f"conditions complete menu {str(conditions)}")

class ConditionsComplete:
    def __init__(self, objective):
        self.objective = objective

        self.field_conditions = []
        for condition in self.objective.conditions:
            self.field_conditions.append(condition.field(field.IncrementEventWord(event_word.SCRATCH)))

        self.battle_conditions = []
        for condition in self.objective.conditions:
            self.battle_conditions.append(condition.battle(asm.INX()))

        self.menu_conditions = []
        for condition in self.objective.conditions:
            self.menu_conditions.append(condition.menu(asm.INX()))

    def field(self):
        return Field(self.field_conditions)

    def battle(self):
        return Battle(self.battle_conditions)

    def menu(self):
        return Menu(self.menu_conditions)
