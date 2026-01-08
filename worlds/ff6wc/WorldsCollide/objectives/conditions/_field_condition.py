from ...memory.space import Bank, Write
from ...instruction import field as field
from ...objectives._cached_function import _CachedFunction

from ...data import event_bit as event_bit
from ...data import battle_bit as battle_bit
from ...data import event_word as event_word

class _Condition(_CachedFunction, field.Call):
    def __init__(self, *args, **kwargs):
        _CachedFunction.__init__(self, *args, **kwargs)
        field.Call.__init__(self, self.address(*args, **kwargs))

class _BitCondition(_Condition):
    def write(self, branch, true, false, description):
        if true is None:
            true = []
        if false is None:
            false = []

        src = [
            branch,

            true,
            field.Return(),

            "FALSE",
            false,
            field.Return(),
        ]
        return Write(Bank.CA, src, description)

class EventBitCondition(_BitCondition):
    def write(self, bit, true = None, false = None):
        return super().write(
            field.BranchIfEventBitClear(bit, "FALSE"),
            true, false,
            f"field bit condition {hex(bit)}",
        )

class BattleBitCondition(_BitCondition):
    def write(self, bit, true = None, false = None):
        return super().write(
            field.BranchIfBattleEventBitClear(bit, "FALSE"),
            true, false,
            f"field battle bit condition {hex(bit)}",
        )

class CharacterCondition(_BitCondition):
    def write(self, character, true = None, false = None):
        return super().write(
            field.BranchIfCharacterNotRecruited(character, "FALSE"),
            true, false,
            f"field character condition {character}",
        )

class EsperCondition(_BitCondition):
    def write(self, esper, true = None, false = None):
        return super().write(
            field.BranchIfEsperNotFound(esper, "FALSE"),
            true, false,
            f"field esper condition {esper}",
        )

class EventWordCondition(_Condition):
    def write(self, word, count, ge = None, lt = None):
        if ge is None:
            ge = []
        if lt is None:
            lt = []

        src = [
            field.BranchIfEventWordLess(word, count, "LT"),
            ge,
            field.Return(),

            "LT",
            lt,
            field.Return(),
        ]
        return Write(Bank.CA, src, f"field count condition {hex(word)} {count}")
