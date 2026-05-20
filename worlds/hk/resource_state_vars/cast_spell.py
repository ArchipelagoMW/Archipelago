from collections import Counter
from collections.abc import Generator
from itertools import chain

from ..constants import NearbySoul
from ..options import HKOptions
from . import RCStateVariable, cs, rs
from .equip_charm import EquipCharmVariable
from .soul_manager import SoulManager


class CastSpellVariable(RCStateVariable):
    prefix: str = "$CASTSPELL"
    casts: list[int]
    before_soul: NearbySoul
    after_soul: NearbySoul
    can_dreamgate: bool

    equip_st: EquipCharmVariable
    sp_manager: SoulManager

    def __init__(self, *args):
        super().__init__(*args)
        self.equip_st = EquipCharmVariable("$EQUIPPEDCHARM[Spell_Twister]", self.player)
        self.sp_manager = SoulManager(SoulManager.prefix, self.player)

    def parse_term(self, *args) -> None:
        self.casts = []
        self.can_dreamgate = True
        self.before_soul = NearbySoul.NONE
        self.after_soul = NearbySoul.NONE
        for arg in args:
            if arg.isdigit():
                self.casts.append(int(arg))
            elif arg == "noDG":
                raise Exception("no dreamgate is currently not implemented")
                self.can_dreamgate = False
            elif arg.startswith("before:"):
                self.before = NearbySoul[arg[7:]]
            elif arg.startswith("after:"):
                self.after = NearbySoul[arg[6:]]
            else:
                raise Exception(f"unknown {self.prefix} term, args: {args}")
        if len(self.casts) == 0:
            self.casts.append(1)

    @classmethod
    def try_match(cls, term: str) -> bool:
        return term.startswith(cls.prefix)

    def can_exclude(self, options: HKOptions) -> bool:
        return False

    @property
    def terms(self) -> list[str]:
        return [*self.equip_st.terms, *self.sp_manager.terms]

    def modify_state(self, state_blob: rs, item_state: cs) -> Generator[rs]:
        if self.nearby_soul_to_bool(item_state, self.before_soul):
            _, state_blob = self.sp_manager.try_restore_all_soul(state_blob, item_state, True)
        if not self.equip_st.is_determined(state_blob, item_state):
            st_equipped, state24 = self.equip_st.try_equip(state_blob, item_state)
            if st_equipped:
                state33 = self.equip_st.set_unequippable(state_blob)
                casted24, state24 = self.try_cast(state24, item_state, 24)
                if casted24:
                    yield state24
                    casted33, state33 = self.try_cast(state33, item_state, 33)
                    if casted33:
                        yield state33
            else:
                state33 = self.equip_st.set_unequippable(state_blob)
                casted33, state33 = self.try_cast(state33, item_state, 33)
                if casted33:
                    yield state33
        else:
            if self.equip_st.is_equipped(state_blob):
                casted24, ret = self.try_cast(state_blob, item_state, 24)
                if casted24:
                    yield ret
            else:
                casted33, ret = self.try_cast(state_blob, item_state, 33)
                if casted33:
                    yield ret

    def nearby_soul_to_bool(self, item_state: cs, soul: NearbySoul) -> bool:
        if soul > NearbySoul.NONE and soul <= NearbySoul.ROOMSOUL:
            mode = self.get_mode(item_state)
            return mode > NearbySoul.NONE and mode <= soul
        return False

    def get_mode(self, item_state: cs) -> NearbySoul:
        return item_state._hk_soul_modes[self.player]

    def try_cast(self, state_blob: rs, item_state: cs, amount_per_cast) -> tuple[bool, rs]:
        soul_spent, new_state = self.sp_manager.try_spend_soul_sequence(
            state_blob, item_state, amount_per_cast, self.casts
        )
        if not soul_spent:
            return False, state_blob
        if self.nearby_soul_to_bool(item_state, self.after_soul):
            new_state = self.sp_manager.try_restore_soul(new_state, item_state, sum(self.casts) * 33)
            # recover the same amount of soul in all paths to respect the state ordering
        return True, new_state


class ShriekPogoVariable(CastSpellVariable):
    prefix = "$SHRIEKPOGO"
    stall_cast: CastSpellVariable | None
    left_stall: bool
    right_stall: bool

    @classmethod
    def try_match(cls, term: str) -> bool:
        return term.startswith(cls.prefix)

    def parse_term(self, *args) -> None:
        self.left_stall = "NOLEFTSTALL" not in args
        self.right_stall = "NORIGHTSTALL" not in args
        if "NOSTALL" in args:
            self.left_stall, self.right_stall = False, False
        args = [a for a in args if a not in ("NOLEFTSTALL", "NORIGHTSTALL", "NOSTALL")]
        super().parse_term(*args)
        if any(cast > 1 for cast in self.casts) and (self.left_stall or self.right_stall):
            sub_params = list(chain.from_iterable([["1"] * int(i) if i.isdigit() else [i] for i in args]))
            # flatten any > 1 cast value into that many copies of 1
            # to tell downstream that there can be a break to regain soul
            self.stall_cast = CastSpellVariable(f"{CastSpellVariable.prefix}[{','.join(sub_params)}]", self.player)
        else:
            self.stall_cast = None

    @property
    def terms(self) -> list[str]:
        self_terms = ["SCREAM"]
        if self.left_stall:
            self_terms.append("LEFTDASH")
        if self.right_stall:
            self_terms.append("RIGHTDASH")
        if self.stall_cast:
            self_terms += self.stall_cast.terms
        return super().terms + self_terms

    def modify_state(self, state_blob: rs, item_state: cs) -> Generator[rs]:
        if not item_state.has_all_counts({"SCREAM": 2, "WINGS": 1}, self.player):
            return
        elif self.stall_cast and ((self.left_stall and item_state.has("LEFTDASH", self.player))
                                  or (self.right_stall and item_state.has("RIGHTDASH", self.player))):
            yield from self.stall_cast.modify_state(state_blob, item_state)
        else:
            yield from super().modify_state(state_blob, item_state)

    def can_exclude(self, options) -> bool:
        if not bool(options.ShriekPogos):
            return True
        if bool(options.DifficultSkips):
            # the casts don't matter
            return False
        if sum(self.casts) > 3:
            # difficult off, so exclude any 4+ cast shrogos
            return True
        return False

    def add_simple_item_reqs(self, items: Counter) -> None:
        items["SCREAM"] = 2
        items["WINGS"] = 1


class SlopeballVariable(CastSpellVariable):
    prefix = "$SLOPEBALL"

    @classmethod
    def try_match(cls, term: str) -> bool:
        return term.startswith(cls.prefix)

    @property
    def terms(self) -> list[str]:
        return [*super().terms, "FIREBALL"]

    def modify_state(self, state_blob: rs, item_state: cs) -> Generator[rs]:
        if not item_state.has("FIREBALL", self.player):
            return
        # else
        yield from super().modify_state(state_blob, item_state)

    def can_exclude(self, options) -> bool:
        return not bool(options.Slopeballs)

    def add_simple_item_reqs(self, items: Counter) -> None:
        items["FIREBALL"] = items.get("FIREBALL", 1)
