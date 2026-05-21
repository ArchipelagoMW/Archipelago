from collections.abc import Generator

from . import ResourceStateHandler, cs, rs, rs_add_value, rs_get_value, rs_increase_if_lower, rs_set_value


class SoulInfo:
    soul: int
    max_soul: int
    reserve_soul: int
    max_reserve_soul: int

    def __init__(self, soul, max_soul, reserve_soul, max_reserve_soul):
        self.soul = soul
        self.max_soul = max_soul
        self.reserve_soul = reserve_soul
        self.max_reserve_soul = max_reserve_soul


class SoulManager(metaclass=ResourceStateHandler):
    prefix = "$SSM"
    player: int

    @classmethod
    def try_match(cls, term: str) -> bool:
        return term == cls.prefix

    @property
    def terms(self) -> list[str]:
        return ["VESSELFRAGMENTS"]

    def __init__(self, term: str, player: int):
        self.player = player

    def spend_soul(self, state_blob: rs, item_state: cs, amount: int) -> Generator[rs]:
        spent, ret = self.try_spend_soul(state_blob, item_state, amount)
        if spent:
            yield ret

    def spend_soul_sequence(self):
        ...

    def spend_soul_slow(self):
        ...

    def try_spend_soul(self, state_blob: rs, item_state: cs, amount: int) -> tuple[bool, rs]:
        soul = self.get_soul_info(state_blob, item_state)
        if soul.soul < amount:
            return False, state_blob
        state_blob = self.spend_and_rebalance(state_blob, item_state, amount, soul)
        return True, state_blob

    def spend_and_rebalance(self, state_blob: rs, item_state: cs, amount: int, soul: SoulInfo) -> rs:
        state_blob = self.spend_without_rebalance(state_blob, item_state, amount, soul)
        state_blob = self.rebalance_reserve(state_blob, item_state, soul)
        return state_blob

    def spend_without_rebalance(self, state_blob: rs, item_state: cs, amount: int, soul: SoulInfo) -> rs:
        state_blob = rs_add_value(state_blob, "SPENTSOUL", amount)
        state_blob = rs_increase_if_lower(state_blob, "REQUIREDMAXSOUL", rs_get_value(state_blob, "SPENTSOUL"))
        soul.soul -= amount
        return state_blob

    def rebalance_reserve(self, state_blob: rs, item_state: cs, soul: SoulInfo) -> rs:
        transfer = min(soul.max_soul - soul.soul, soul.reserve_soul)
        if transfer > 0:
            state_blob = rs_add_value(state_blob, "SPENTSOUL", -transfer)
            state_blob = rs_add_value(state_blob, "SPENTRESERVESOUL", transfer)
            soul.soul += transfer
            soul.reserve_soul -= transfer
        return state_blob

    def try_spend_soul_sequence(self, state_blob: rs, item_state: cs, amount: int, casts: list[int]) -> tuple[bool, rs]:
        soul = self.get_soul_info(state_blob, item_state)
        for cast in casts:
            group_total = cast * amount
            if soul.soul < group_total:
                return False, state_blob
            state_blob = self.spend_and_rebalance(state_blob, item_state, group_total, soul)
        return True, state_blob

    def try_spend_soul_slow(self):
        ...

    def try_resore_soul(self):
        ...

    def spend_all_soul(self, state_blob: rs, item_state: cs) -> Generator[rs]:
        spent, ret = self.try_spend_all_soul(state_blob, item_state)
        if spent:
            yield ret

    def try_spend_all_soul(self, state_blob: rs, item_state: cs) -> tuple[bool, rs]:
        info = self.get_soul_info(state_blob, item_state)
        state_blob = rs_set_value(state_blob, "SPENTSOUL", info.max_soul)
        state_blob = rs_set_value(state_blob, "REQUIREDMAXSOUL", info.max_soul)
        state_blob = rs_set_value(state_blob, "SPENTRESERVESOUL", info.max_reserve_soul)
        return True, state_blob

    def restore_soul(self):
        ...

    def restore_all_soul(self, state_blob: rs, item_state: cs, restore_reserves: bool) -> Generator[rs]:
        restored, ret = self.try_restore_all_soul(state_blob, item_state, restore_reserves)
        if restored:
            yield ret

    def try_restore_soul(self):
        ...

    def try_restore_all_soul(self, state_blob: rs, item_state: cs, restore_reserves: bool) -> tuple[bool, rs]:
        if rs_get_value(state_blob, "CANNOTREGAINSOUL"):
            return False, state_blob
        state_blob = rs_set_value(state_blob, "SPENTSOUL", 0)
        if restore_reserves:
            state_blob = rs_set_value(state_blob, "SPENTRESERVESOUL", 0)
        return True, state_blob

    def get_soul_info(self, state_blob: rs, item_state: cs) -> SoulInfo:
        max_soul = 99 - rs_get_value(state_blob, "SOULLIMITER")
        soul = max_soul - rs_get_value(state_blob, "SPENTSOUL")
        vessels = min(6, item_state.count("VESSELFRAGMENTS", self.player) // 3)  # max 6 so that state doesn't overflow
        max_reserve_soul = vessels * 33
        reserve_soul = max_reserve_soul - rs_get_value(state_blob, "SPENTRESERVESOUL")
        return SoulInfo(soul, max_soul, reserve_soul, max_reserve_soul)

    def try_set_soul_limit(
            self,
            state_blob: rs,
            item_state: cs,
            limiter: int,
            applies_to_prior_path: bool
    ) -> tuple[bool, rs]:
        if applies_to_prior_path and rs_get_value(state_blob, "REQUIREDMAXSOUL") > 99 - limiter:
            return False, state_blob
        current = rs_get_value(state_blob, "SOULLIMITER")
        if limiter > current:
            state_blob = rs_add_value(state_blob, "SOULLIMITER", limiter - current)
        elif limiter < current:
            state_blob = rs_add_value(state_blob, "SOULLIMITER", limiter - current)
            _, state_blob = self.try_spend_soul(state_blob, item_state, current - limiter)
        return True, state_blob

    def limit_soul(self, state_blob: rs, item_state: cs, limiter: int, applies_to_prior_path: bool) -> Generator[rs]:
        limited, ret = self.try_set_soul_limit(state_blob, item_state, limiter, applies_to_prior_path)
        if limited:
            yield ret

    def soul_info(self):
        ...
