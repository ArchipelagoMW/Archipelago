from . import RCStateVariable, cs, rs, rs_add_value, rs_get_value, rs_set_value


class SpendSoulVariable(RCStateVariable):
    prefix = "$SPENDSOUL"
    amount: int

    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Not Fully Implemented, use soul_manager instead if possible")

    def parse_term(self, amount) -> None:
        self.amount = int(amount)

    @classmethod
    def try_match(cls, term: str) -> bool:
        return term.startswith(cls.prefix)

    # @classmethod
    # def get_terms(cls):
    #     return (term for term in ("VessleFragments",))

    def _modify_state(self, state_blob: rs, item_state: cs) -> tuple[bool, rs]:
        if rs_get_value(state_blob, "SPENTALLSOUL"):
            return False, state_blob

        soul = self.get_soul(state_blob)
        if soul < self.amount:
            return False, state_blob

        reserve_soul = self.get_reserve_soul(state_blob, item_state)
        if reserve_soul >= self.amount:
            state_blob = rs_add_value(state_blob, "SPENTRESERVESOUL", self.amount)
        else:
            state_blob = rs_add_value(state_blob, "SPENTRESERVESOUL", reserve_soul)
            state_blob = rs_add_value(state_blob, "SPENTSOUL", self.amount - reserve_soul)

        required_max_soul = rs_get_value(state_blob, "REQUIREDMAXSOUL")
        alt_req = max(self.amount, rs_get_value(state_blob, "SPENTSOUL"))
        if alt_req > required_max_soul:
            state_blob = rs_set_value(state_blob, "REQUIREDMAXSOUL", alt_req)

        return True, state_blob

    def get_soul(self, state_blob: rs) -> int:
        return 99 - rs_get_value(state_blob, "SOULLIMITER") - rs_get_value(state_blob, "SPENTSOUL")

    def get_reserve_soul(self, state_blob: rs, item_state: cs) -> int:
        return (((item_state.count("VESSELFRAGMENTS", self.player) // 3) * 33)
                - rs_get_value(state_blob, "SPENTRESERVESOUL"))

    def can_exclude(self, options) -> bool:
        return False
