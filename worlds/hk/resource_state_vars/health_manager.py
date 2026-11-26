from collections.abc import Generator, Iterable
from typing import NamedTuple

from . import ResourceStateHandler, cs, rs, rs_add_value, rs_get_value, rs_set_value, rs_subtract_at_most
from .equip_charm import EquipCharmVariable, FragileCharmVariable
from .soul_manager import SoulManager


class HPInfo(NamedTuple):
    current_white_hp: int
    current_blue_hp: int
    max_white_hp: int


class HitInfo:
    survives: bool
    amount: int
    blue_hp_damage: int
    white_hp_damage: int
    wait_after_hit: bool

    def __init__(self, info: HPInfo, amount: int, wait_after_hit: bool):
        self.amount = amount
        self.wait_after_hit = wait_after_hit
        if info.current_blue_hp >= amount:
            self.blue_hp_damage = amount
        else:
            self.blue_hp_damage = info.current_blue_hp
        if info.current_blue_hp >= amount:
            self.white_hp_damage = 0
        else:
            self.white_hp_damage = amount

        self.survives = (info.current_blue_hp >= amount) or (info.current_white_hp > amount)

    def __repr__(self):
        return "HitInfo(" + ", ".join([f"{v}={getattr(self, v)}" for v in [
            "survives", "amount", "blue_hp_damage", "white_hp_damage", "wait_after_hit"
        ]]) + ")"


class HealthManager(metaclass=ResourceStateHandler):
    prefix = "$HPSM"
    max_damage = 99
    """Used to max out lazy hp to signal it is determined"""
    player: int
    lb_heart: EquipCharmVariable
    lb_core: EquipCharmVariable
    jonis: EquipCharmVariable
    fragile_heart: FragileCharmVariable
    hiveblood: EquipCharmVariable
    deep_focus: EquipCharmVariable
    ssm: SoulManager

    @classmethod
    def try_match(cls, term: str) -> bool:
        return term == cls.prefix

    @property
    def terms(self) -> list[str]:
        sub_terms = [
            term
            for sub_var in [
                self.lb_heart,
                self.lb_core,
                self.jonis,
                self.fragile_heart,
                self.hiveblood,
                self.deep_focus,
                self.ssm,
            ]
            for term in sub_var.terms
        ]
        return [*sub_terms, "MASKSHARDS", "FOCUS"]

    def __init__(self, term: str, player: int):
        self.player = player
        self.lb_heart = EquipCharmVariable("$EQUIPPEDCHARM[Lifeblood_Heart]", self.player)
        self.lb_core = EquipCharmVariable("$EQUIPPEDCHARM[Lifeblood_Core]", self.player)
        self.jonis = EquipCharmVariable("$EQUIPPEDCHARM[Joni's_Blessing]", self.player)
        self.fragile_heart = FragileCharmVariable("$EQUIPPEDCHARM[Fragile_Heart]", self.player)
        self.hiveblood = EquipCharmVariable("$EQUIPPEDCHARM[Hiveblood]", self.player)
        self.deep_focus = EquipCharmVariable("$EQUIPPEDCHARM[Deep_Focus]", self.player)
        self.ssm = SoulManager("$SSM", self.player)

    @property
    def determine_hp_charms(self) -> Iterable[EquipCharmVariable]:
        return self.hiveblood, self.lb_heart, self.lb_core, self.fragile_heart, self.jonis

    @property
    def focus_charms(self) -> Iterable[EquipCharmVariable]:
        return self.deep_focus, self.jonis

    @property
    def before_death_charms(self) -> Iterable[EquipCharmVariable]:
        return self.hiveblood, self.lb_heart, self.lb_core, self.fragile_heart, self.jonis, self.deep_focus

    def give_blue_health(self, state_blob: rs, item_state: cs, amount: int) -> Generator[rs]:
        if not self.is_hp_determined(state_blob):
            rets = self.determine_hp(state_blob, item_state)
            for ret in rets:
                yield next(self.give_blue_health(ret, item_state, amount))
        else:
            yield rs_add_value(state_blob, "SPENTBLUEHP", -amount)

    def give_health(self, state_blob: rs, item_state: cs, amount: int) -> Generator[rs]:
        if not self.is_hp_determined(state_blob):
            if rs_get_value(state_blob, "LAZYSPENTHP") > 0:
                rets = self.determine_hp(state_blob, item_state)
                for ret in rets:
                    yield next(self.give_health(ret, item_state, amount))
            else:
                yield state_blob
        else:
            yield rs_subtract_at_most(state_blob, "SPENTHP", amount)

    def restore_white_health(self, state_blob: rs, item_state: cs) -> Generator[rs]:
        if not self.is_hp_determined(state_blob):
            if rs_get_value(state_blob, "LAZYSPENTHP") == 0:
                yield state_blob
            else:
                rets = self.determine_hp(state_blob, item_state)
                for ret in rets:
                    yield next(self.restore_white_health(ret, item_state))
        else:
            yield rs_set_value(state_blob, "SPENTHP", 0)

    def restore_all_health(self, state_blob: rs, item_state: cs) -> Generator[rs]:
        if not self.is_hp_determined(state_blob):
            yield rs_set_value(state_blob, "LAZYSPENTHP", 0)
        else:
            ret = rs_set_value(state_blob, "SPENTHP", 0)
            yield rs_set_value(ret, "SPENTBLUEHP", 0)

    def try_focus(self, state_blob: rs, item_state: cs) -> tuple[bool, rs]:
        if not item_state.has("FOCUS", self.player) or not self.is_hp_determined(state_blob):
            return False, state_blob
        for charm in self.focus_charms:
            if not charm.is_determined(state_blob, item_state):
                return False, state_blob
        if not self.ssm.try_spend_soul(state_blob, item_state, 33):
            return False, state_blob
        heal_amount = self.get_heal_amount(state_blob, item_state)

        if rs_get_value(state_blob, "SPENTHP") > 0:
            state_blob = rs_subtract_at_most(state_blob, "SPENTHP", heal_amount)
        return True, state_blob

    def do_focus(self, state_blob: rs, item_state: cs, amount: int) -> Generator[rs]:
        if not item_state.has("FOCUS", self.player):
            return
        if not self.is_hp_determined(state_blob):
            for r in self.determine_hp(state_blob, item_state):
                yield from self.do_focus(r, item_state, amount)
            return
        if any(not c.is_determined(state_blob, item_state) for c in self.focus_charms):
            rets = list(EquipCharmVariable.generate_charm_combinations(state_blob, item_state, self.focus_charms))
            for r in rets:
                yield from self.do_focus(r, item_state, amount)
            return
        spent_soul, state_blob = self.ssm.try_spend_soul(state_blob, item_state, 33)
        if not spent_soul:
            return

        heal_amount = self.get_heal_amount(state_blob, item_state)
        yield rs_subtract_at_most(state_blob, "SPENTHP", amount * heal_amount)

    def get_heal_amount(self, state_blob: rs, item_state: cs) -> int:
        if self.jonis.is_equipped(state_blob):
            return 0
        if self.deep_focus.is_equipped(state_blob):
            return 2
        return 1

    def is_hp_determined(self, state_blob: rs) -> bool:
        return rs_get_value(state_blob, "LAZYSPENTHP") == self.max_damage

    def determine_hp(self, state_blob: rs, item_state: cs) -> Generator[rs]:
        if self.is_hp_determined(state_blob):
            yield state_blob
            return

        ret_base = rs_set_value(state_blob, "LAZYSPENTHP", self.max_damage)
        lazy_spent_hp = rs_get_value(state_blob, "LAZYSPENTHP")

        rets = []
        for s in self.decide_overcharm(ret_base, item_state):
            rets += list(EquipCharmVariable.generate_charm_combinations(s, item_state, self.determine_hp_charms))

        for _ in range(lazy_spent_hp):
            rets = [r for s in rets for r in self.take_damage(s, item_state, 1)]
        yield from rets

    def decide_overcharm(self, state_blob: rs, item_state: cs) -> Generator[rs]:
        if rs_get_value(state_blob, "CANNOTOVERCHARM") or rs_get_value(state_blob, "OVERCHARMED"):
            yield state_blob
        else:
            yield rs_set_value(state_blob, "OVERCHARMED", 1)
            yield rs_set_value(state_blob, "CANNOTOVERCHARM", 1)

    def get_hp_info(self, state_blob: rs, item_state: cs) -> HPInfo:
        if not self.is_hp_determined(state_blob):
            raise Exception("get_hp_info called on state with indeterminate hp.")
        max_hp = item_state.count("MASKSHARDS", self.player) // 4
        if self.fragile_heart.is_equipped(state_blob):
            max_hp += 2
        if self.jonis.is_equipped(state_blob):
            max_hp = int(1.4 * max_hp)
        hp = max_hp - rs_get_value(state_blob, "SPENTHP")
        blue_hp = -rs_get_value(state_blob, "SPENTBLUEHP")
        if self.lb_heart.is_equipped(state_blob):
            blue_hp += 2
        if self.lb_core.is_equipped(state_blob):
            blue_hp += 4
        return HPInfo(hp, blue_hp, max_hp)

    def do_hit(self, state_blob: rs, item_state: cs, hit: HitInfo) -> rs:
        if not hit.survives:
            raise Exception("do_hit on lethal damage")
        ret = state_blob
        if hit.blue_hp_damage:
            ret = rs_add_value(ret, "SPENTBLUEHP", hit.blue_hp_damage)
        if hit.white_hp_damage:
            ret = rs_add_value(ret, "SPENTHP", hit.white_hp_damage)
        if hit.wait_after_hit:
            if hit.white_hp_damage > 0 and self.hiveblood.is_equipped(ret):
                ret = rs_add_value(ret, "SPENTHP", -1)
        return rs_set_value(ret, "NOFLOWER", 1)

    def take_damage(self, state_blob: rs, item_state: cs, amount: int) -> Generator[rs]:
        if not self.is_hp_determined(state_blob):
            if amount > 1 or not self.can_take_next_lazy_hit(state_blob, item_state):
                for r in self.determine_hp(state_blob, item_state):
                    yield from self.take_damage_strict(r, item_state, amount, True)
                return
            else:
                yield rs_add_value(state_blob, "LAZYSPENTHP", 1)
        else:
            yield from self.take_damage_strict(state_blob, item_state, amount, True)

    def take_damage_sequence(self, state_blob: rs, item_state: cs, amounts: Iterable[int]) -> Generator[rs]:
        raise NotImplementedError("TODO: when needed research and answer comments from dorijanko's pr")
        if not self.is_hp_determined(state_blob):
            for r in self.determine_hp(state_blob, item_state):
                yield from self.take_damage_sequence(r, item_state, amounts)
            return

        rets = [state_blob]
        for i, amount in enumerate(amounts):
            wait_after_hit = i == len(amounts) - 1
            # I'm assuming that you should look at every option currently in rets to take damage instead of looking at
            # state_blob but this method doesn't seem to be used anywhere so I won't be worrying about it currently
            rets = list(self.take_damage_strict(state_blob, item_state, amount, wait_after_hit))
        for r in rets:
            yield r

    def can_take_next_lazy_hit(self, state_blob: rs, item_state: cs) -> bool:
        hits_taken = rs_get_value(state_blob, "LAZYSPENTHP")
        max_hp = item_state.count("MASKSHARDS", self.player) // 4
        total_hits = (max_hp - 1) // 2
        return total_hits - hits_taken > 0

    def take_damage_strict(self, state_blob: rs, item_state: cs, amount: int, wait_after_hit: bool) -> Generator[rs]:
        adj_amount = 2 * amount if rs_get_value(state_blob, "OVERCHARMED") else amount

        info = self.get_hp_info(state_blob, item_state)
        hit = HitInfo(info, adj_amount, wait_after_hit)
        if hit.survives:
            yield self.do_hit(state_blob, item_state, hit)
            return
        # else
        rets = list(EquipCharmVariable.generate_charm_combinations(state_blob, item_state, self.before_death_charms))
        for r in rets:
            yield from self.take_damage_desperate(r, item_state, amount, True)

    def take_damage_desperate(self, state_blob: rs, item_state: cs, amount: int, wait_after_hit: bool) -> Generator[rs]:
        adj_amount = 2 * amount if rs_get_value(state_blob, "OVERCHARMED") else amount
        info = self.get_hp_info(state_blob, item_state)

        deficit = adj_amount - info.current_white_hp
        if deficit >= 0:
            if not wait_after_hit:
                return
            heal_amount = self.get_heal_amount(state_blob, item_state)
            heal_avail = info.max_white_hp - info.current_white_hp
            heal_req = 1 + deficit
            if heal_amount > 0 and heal_avail >= heal_req:
                rets = list(self.do_focus(state_blob, item_state, heal_req))
            else:
                return
        else:
            rets = [state_blob]

        for r in rets:
            info = self.get_hp_info(r, item_state)
            hit = HitInfo(info, adj_amount, True)
            if not hit.survives:
                continue
            yield self.do_hit(r, item_state, hit)
