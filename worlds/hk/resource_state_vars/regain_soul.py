from ..options import HKOptions
from . import RCStateVariable, cs, rs, rs_add_value, rs_get_value, rs_set_value, rs_subtract_at_most


class RegainSoulVariable(RCStateVariable):
    prefix: str = "$REGAINSOUL"
    amount: int

    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Not Fully Implemented, use soul_manager instead if possible")

    def parse_term(self, amount: str) -> None:
        self.amount = int(amount)

    @classmethod
    def try_match(cls, term: str) -> bool:
        return term.startswith(cls.prefix)

    # @classmethod
    # def get_terms(cls):
    #     return (term for term in ("VessleFragments",))

    def _modify_state(self, state_blob: rs, item_state: cs) -> tuple[bool, rs]:
        if rs_get_value(state_blob, "CANNOTREGAINSOUL"):
            return False, state_blob
        if rs_get_value(state_blob, "SPENTALLSOUL"):
            state_blob = rs_set_value(state_blob, "SPENTRESERVESOUL", self.get_max_reserve_soul(item_state))
            state_blob = rs_set_value(state_blob, "SPENTSOUL", self.get_max_soul(state_blob))
            state_blob = rs_set_value(state_blob, "SPENTALLSOUL", 0)
        # rewritten to be actually correct (might be for no reason since it's currently unused, idk)
        spent_soul = rs_get_value(state_blob, "SPENTSOUL")
        if self.amount < spent_soul:
            state_blob = rs_add_value(state_blob, "SPENTSOUL", -self.amount)
        else:
            state_blob = rs_add_value(state_blob, "SPENTSOUL", -spent_soul)
            amount = self.amount - spent_soul
            state_blob = rs_subtract_at_most(state_blob, "SPENTRESERVESOUL", amount)
        return True, state_blob

    def get_max_reserve_soul(self, item_state: cs) -> int:
        return (item_state.count("VesselFragment", self.player) // 3) * 33

    def get_max_soul(self, state_blob: rs) -> int:
        return 99 - rs_get_value(state_blob, "SOULLIMITER")

    def can_exclude(self, options: HKOptions) -> bool:
        return False
