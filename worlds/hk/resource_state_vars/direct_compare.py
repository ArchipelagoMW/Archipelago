from ..options import HKOptions
from . import RCStateVariable, cs, rs, rs_get_value


class DirectCompare:
    term: str
    op: str
    value: str  # may be int or bool

    def __init__(self, term: str, player: int):
        self.term, self.value = (*term.split(self.op),)
        self.player = player

    @classmethod
    def try_match(cls, term: str) -> bool:
        return cls.op in term

    def can_exclude(self, options: HKOptions) -> bool:
        return False

    @property
    def terms(self) -> list[str]:
        return [self.term]


class EQVariable(DirectCompare, RCStateVariable):
    term: str
    op: str = "="
    value: str  # may be int or bool

    def _modify_state(self, state_blob: rs, item_state: cs) -> tuple[bool, rs]:
        if self.value.isdigit():
            return rs_get_value(state_blob, self.term) == int(self.value), state_blob
        else:  # noqa: RET505
            v = self.value == "TRUE"
            assert v or self.value == "FALSE"
            return rs_get_value(state_blob, self.term) == v, state_blob


class GTVariable(DirectCompare, RCStateVariable):
    term: str
    op: str = ">"
    value: str

    def _modify_state(self, state_blob: rs, item_state: cs) -> tuple[bool, rs]:
        assert self.value.isdigit()
        return rs_get_value(state_blob, self.term) > int(self.value), state_blob


class LTVariable(DirectCompare, RCStateVariable):
    term: str
    op: str = "<"
    value: str

    def _modify_state(self, state_blob: rs, item_state: cs) -> tuple[bool, rs]:
        assert self.value.isdigit()
        return rs_get_value(state_blob, self.term) < int(self.value), state_blob
