from __future__ import annotations

from collections import Counter
from collections.abc import Generator, Iterable
from enum import IntEnum
from typing import ClassVar

from ..charms import charm_name_to_id, charm_names
from ..options import HKOptions
from . import RCStateVariable, cs, rs, rs_add_value, rs_get_value, rs_increase_if_lower, rs_set_value


class EquipResult(IntEnum):
    NONE = 1
    OVERCHARM = 2
    NONOVERCHARM = 3


class EquipCharmVariable(RCStateVariable):
    prefix: str = "$EQUIPPEDCHARM"
    equip_prefix: str = "CHARM"
    no_equip_prefix: str = "noCHARM"
    excluded_charm_ids: tuple[int] = (23, 24, 25, 36,)  # fragiles and Kingsoul
    charm_id: int
    charm_name: str
    charm_key: str

    # maybe remove this later if it ends up not being useful compared to charm_id_and_name
    @staticmethod
    def get_name(charm: str) -> str:
        """Convert charm id to name, or just return the name"""
        if charm.isdigit():
            return charm_names[int(charm) - 1]
        else:  # noqa: RET505
            return charm

    @staticmethod
    def get_id(charm: str) -> int:
        """Convert charm name to id, or just return the id"""
        if charm.isdigit():
            return int(charm)
        else:  # noqa: RET505
            return charm_name_to_id[charm] + 1

    @staticmethod
    def charm_id_and_name(charm: str) -> tuple[int, str]:
        """Convert 1 indexed charm id or charm name to both"""
        if charm.isdigit():
            return int(charm), charm_names[int(charm) - 1]
        else:  # noqa: RET505
            return charm_name_to_id[charm] + 1, charm

    def parse_term(self, term: str) -> None:
        self.charm_id, self.charm_name = self.charm_id_and_name(term)
        self.charm_key = f"CHARM{self.charm_id}"

    @classmethod
    def try_match(cls, term: str) -> bool:
        if term.startswith(cls.prefix):
            # strip the $EQUIPPEDCHARM[] from the term and extract the 1 indexed charm id
            charm_id = cls.get_id(term[len(cls.prefix)+1:-1])
            # covered by other handlers
            if charm_id not in cls.excluded_charm_ids:
                return True
        # else
        return False

    @property
    def terms(self) -> list[str]:
        return [self.charm_name, "NOTCHES"]

    def has_item(self, item_state: cs) -> bool:
        return item_state.has(self.charm_name, self.player)
        # return bool(item_state._hk_processed_item_cache[self.player][self.charm_name])

    def _modify_state(self, state_blob: rs, item_state: cs) -> tuple[bool, rs]:
        return self.try_equip(state_blob, item_state)

    def _try_equip(self, state_blob: rs, item_state: cs) -> tuple[bool, rs]:
        if self.is_equipped(state_blob):
            return True, state_blob
        if self.can_equip(state_blob, item_state) != EquipResult.NONE:
            ret = self.do_equip_charm(state_blob, item_state)
            return True, ret
        return False, state_blob

    def try_equip(self, state_blob: rs, item_state: cs) -> tuple[bool, rs]:
        if self.is_equipped(state_blob):
            return True, state_blob
        if self.can_equip(state_blob, item_state) != EquipResult.NONE:
            return True, self.do_equip_charm(state_blob, item_state)
        return False, state_blob

    @property
    def anti_term(self) -> str:
        return f"{self.no_equip_prefix}{self.charm_id}"

    @property
    def term(self) -> str:
        return f"{self.equip_prefix}{self.charm_id}"

    def has_state_requirements(self, state_blob: rs, item_state: cs) -> bool:
        if rs_get_value(state_blob, "NOPASSEDCHARMEQUIP") or rs_get_value(state_blob, self.anti_term):
            return False
        return True

    def get_total_notches(self, item_state: cs) -> int:
        return item_state.count("NOTCHES", self.player)

    def get_notch_cost(self, item_state: cs) -> int:
        return item_state._hk_charm_costs[self.player][self.charm_name]

    def has_notch_requirments(self, state_blob: rs, item_state: cs) -> EquipResult:
        notch_cost = self.get_notch_cost(item_state)
        if notch_cost <= 0 or self.is_equipped(state_blob):
            return EquipResult.OVERCHARM if rs_get_value(state_blob, "OVERCHARMED") else EquipResult.NONOVERCHARM
        # can be equipped

        net_notches = min(20, self.get_total_notches(item_state)) - rs_get_value(state_blob, "USEDNOTCHES") - notch_cost
        # max 20 total notches used if lots of notches are in starting inventory to not overflow

        if net_notches >= 0:
            return EquipResult.NONOVERCHARM
        # something to figure out if you can overcharm to get this on
        overcharm_save = max(notch_cost, rs_get_value(state_blob, "MAXNOTCHCOST"))
        if net_notches + overcharm_save > 0 and not rs_get_value(state_blob, "CANNOTOVERCHARM"):
            return EquipResult.OVERCHARM
        return EquipResult.NONE  # TODO doublecheck

    def can_equip_non_overcharm(self, state_blob: rs, item_state: cs) -> bool:
        return (self.has_item(item_state) and self.has_state_requirements(state_blob, item_state)
                and self.has_notch_requirments(state_blob, item_state) == EquipResult.NONOVERCHARM)

    def can_equip_overcharm(self, state_blob: rs, item_state: cs) -> bool:
        return (self.has_item(item_state) and self.has_state_requirements(state_blob, item_state)
                and self.has_notch_requirments(state_blob, item_state) != EquipResult.NONE)

    def can_equip(self, state_blob: rs, item_state: cs) -> EquipResult:
        if not self.has_charm_progression(item_state) or not self.has_state_requirements(state_blob, item_state):
            return EquipResult.NONE
        return self.has_notch_requirments(state_blob, item_state)

    def do_equip_charm(self, state_blob: rs, item_state: cs) -> rs:
        notch_cost = self.get_notch_cost(item_state)
        state_blob = rs_add_value(state_blob, "USEDNOTCHES", notch_cost)
        state_blob = rs_set_value(state_blob, self.term, 1)
        # doesn't seem to be used for anything and supporting it would unnecessarily increase the state size
        # state_blob[self.charm_key] = True
        state_blob = rs_increase_if_lower(state_blob, "MAXNOTCHCOST", notch_cost)
        if rs_get_value(state_blob, "USEDNOTCHES") > item_state.count("NOTCHES", self.player):
            state_blob = rs_set_value(state_blob, "OVERCHARMED", 1)
        return state_blob

    def is_equipped(self, state_blob: rs) -> bool:
        return bool(rs_get_value(state_blob, self.term))

    def set_unequippable(self, state_blob: rs) -> rs:
        return rs_set_value(state_blob, self.anti_term, 1)

    def get_avaliable_notches(self, state_blob: rs, item_state: cs) -> int:
        return item_state.count("NOTCHES", self.player) - rs_get_value(state_blob, "USEDNOTCHES")

    def can_exclude(self, options: HKOptions) -> bool:
        return False

    def add_simple_item_reqs(self, items: Counter) -> None:
        items[self.charm_key] = 1

    def is_determined(self, state_blob: rs, item_state: cs) -> bool:
        return bool(rs_get_value(state_blob, self.term)) or bool(rs_get_value(state_blob, self.anti_term))

    def has_charm_progression(self, item_state: cs) -> bool:
        return self.has_item(item_state)

    @staticmethod
    def generate_charm_combinations(
            state_blob: rs,
            item_state: cs,
            charm_list: Iterable[EquipCharmVariable],
    ) -> Generator[rs]:
        charms = []
        base_state = state_blob
        for c in charm_list:
            if not c.is_determined(base_state, item_state):
                if (
                    not c.has_charm_progression(item_state)
                    or not c.has_state_requirements(base_state, item_state)
                    or not c.has_notch_requirments(base_state, item_state)
                ):
                    base_state = c.set_unequippable(base_state)
                else:
                    charms.append(c)

        charm_len = len(charms)
        if charm_len == 0:
            yield base_state
            return
        elif charm_len > 30:
            raise Exception("Out of range when calculating generate_charm_combinations")

        p = 1 << charm_len
        for i in range(p):
            cur_state = base_state
            for j in range(charm_len):
                f = 1 << j
                if (i & f) == f:  # equip
                    equipped, new_state = charms[j].try_equip(cur_state, item_state)
                    if not equipped:
                        # should only fail due to out of notches
                        break
                    else:
                        cur_state = new_state
                else:  # do not equip
                    cur_state = charms[j].set_unequippable(cur_state)
            else:
                # only yield if we did not break
                yield cur_state


class FragileCharmVariable(EquipCharmVariable):
    # prefix = "$EQUIPPEDCHARM"
    fragile_lookup: ClassVar[dict[int, list[str]]] = {
        23: ["Fragile_Heart", "Unbreakable_Heart"],
        24: ["Fragile_Greed", "Unbreakable_Greed"],
        25: ["Fragile_Strength", "Unbreakable_Strength"],
    }
    break_term: str

    def parse_term(self, term: str) -> None:
        super().parse_term(term)
        term_postfix = ["HEART", "GREED", "STRENGTH"][self.charm_id - 23]
        self.break_term = f"BROKE{term_postfix}"

    @property
    def terms(self) -> list[str]:
        return [*super().terms, "Can_Repair_Fragile_Charms"]

    def break_charm(self, state_blob: rs, item_state: cs) -> rs:
        if item_state.has(self.charm_key, self.player, 2):
            return state_blob
        if rs_get_value(state_blob, self.term):
            state_blob = rs_add_value(state_blob, self.term, -1)
            state_blob = rs_add_value(state_blob, "USEDNOTCHES", -self.get_notch_cost(item_state))
            state_blob = rs_set_value(state_blob, "OVERCHARMED", 0)
            state_blob = rs_set_value(state_blob, self.anti_term, 1)
            state_blob = rs_set_value(state_blob, self.break_term, 1)
        return state_blob

    def has_state_requirements(self, state_blob: rs, item_state: cs) -> bool:
        return (super().has_state_requirements(state_blob, item_state)
                and ((self.has_unbreakable_item(item_state))
                     or (not rs_get_value(state_blob, self.break_term)
                         and item_state.has("Can_Repair_Fragile_Charms", self.player))))

    @classmethod
    def try_match(cls, term: str) -> bool:
        if term.startswith(cls.prefix):
            charm_id, _ = cls.charm_id_and_name(term[len(cls.prefix)+1:-1])
            if charm_id in cls.fragile_lookup:
                return True
        # else
        return False

    def has_unbreakable_item(self, item_state: cs) -> bool:
        return item_state.has_from_list(self.fragile_lookup[self.charm_id], self.player, 2)

    def add_simple_item_reqs(self, items: Counter) -> None:
        super().add_simple_item_reqs(items)
        items["Can_Repair_Fragile_Charms"] = 1


class WhiteFragmentEquipVariable(EquipCharmVariable):
    # prefix = "$EQUIPPEDCHARM"
    void: bool
    quantity: int

    def parse_term(self, charm: str) -> None:
        super().parse_term(charm)
        self.void = self.charm_name == "Void_Heart"
        assert not self.void == (self.charm_name == "Kingsoul")
        if self.charm_name == "Kingsoul":
            self.quantity = 2
        if self.charm_name == "Void_Heart":
            self.quantity = 3

    @property
    def terms(self) -> list[str]:
        return ["WHITEFRAGMENT", "NOTCHES"]

    @classmethod
    def try_match(cls, term: str) -> bool:
        if term.startswith(cls.prefix):
            charm_id, _ = cls.charm_id_and_name(term[len(cls.prefix)+1:-1])
            if charm_id == 36:
                return True
        # else
        return False

    def has_item(self, item_state: cs) -> bool:
        if self.void:
            count = 3
        else:
            count = 2
        return item_state.has("WHITEFRAGMENT", self.player, count)

    def add_simple_item_reqs(self, items: Counter) -> None:
        if self.void:
            count = 3
        else:
            count = 2
        if items[self.charm_key] < count:
            items[self.charm_key] = count
