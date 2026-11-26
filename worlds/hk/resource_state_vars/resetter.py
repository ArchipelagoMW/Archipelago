from typing import Any, ClassVar

from ..options import HKOptions
from ..state_mixin import default_state
from . import RCStateVariable, cs, rs, rs_get_value, rs_set_value


class RCResetter:
    reset_state: ClassVar[dict[str, Any]]
    """Target state to reset to"""
    opt_in: bool = False
    """Flag to determine if unhandled terms are reset"""
    reset_properties: ClassVar[dict[str, str]]  # TODO - flesh this out
    """
    Dict of requirement: terms to reset,
    use ANY for terms that can be reset with no requirment
    use NONE for terms that will never be reset even with opt_in False
    """

    def parse_term(self) -> None:
        pass

    def _modify_state(self, state_blob: rs, item_state: cs) -> tuple[bool, rs]:
        # TODO: confirm this is always correct, and deletion isn't too big an assumption
        if self.opt_in:
            for key, value in self.reset_properties.items():
                if value != "None":
                    # if the reset logic evaluates to True, update to new value
                    if key not in self.reset_state:
                        state_blob = rs_set_value(state_blob, key, 0)
                    else:
                        state_blob = rs_set_value(state_blob, key, self.reset_state[key])
            return True, state_blob
        else:  # noqa: RET505
            ret = default_state(defaults=self.reset_state)
            for key, value in self.reset_properties.items():
                if value == "None":  # TODO: fix
                    # if the reset logic evaluates to False keep old value
                    ret = rs_set_value(ret, key, rs_get_value(state_blob, key))
            return True, ret

    @classmethod
    def try_match(cls, term: str) -> bool:
        return term.startswith(cls.prefix)

    def can_exclude(self, options: HKOptions) -> bool:
        return False

    @property
    def terms(self) -> list[str]:
        return []


class BenchResetVariable(RCResetter, RCStateVariable):
    prefix: str = "$BENCHRESET"
    reset_state: ClassVar[dict[str, int]] = {
        "NOPASSEDCHARMEQUIP": 0
    }
    opt_in = False
    reset_properties: ClassVar[dict[str, str]] = {
        "CANNOTREGAINSOUL": "NONE",
        "CANNOTSHADESKIP": "NONE",
        "BROKEHEART": "NONE",
        "BROKEGREED": "NONE",
        "BROKESTRENGTH": "NONE",
        "NOFLOWER": "NONE",
        "SOULLIMITER": "NONE",
        "REQUIREDMAXSOUL": "NONE",

        "SPENTALLSOUL": "Salubra's_Blessing + CANNOTREGAINSOUL=FALSE",
        "SPENTSOUL": "Salubra's_Blessing + CANNOTREGAINSOUL=FALSE",
        "SPENTRESERVESOUL": "Salubra's_Blessing + CANNOTREGAINSOUL=FALSE",
    }


class HotSpringResetVariable(RCResetter, RCStateVariable):
    prefix = "$HOTSPRINGRESET"

    reset_state: ClassVar[dict[str, Any]] = {}
    opt_in = True
    reset_properties: ClassVar[dict[str, str]] = {
        "SPENTALLSOUL": "CANNOTREGAINSOUL=FALSE",
        "SPENTSOUL": "CANNOTREGAINSOUL=FALSE",
        "SPENTRESERVESOUL": "CANNOTREGAINSOUL=FALSE",
        "SPENTHP": "ANY",
    }


class SaveQuitResetVariable(RCResetter, RCStateVariable):
    prefix = "$SAVEQUITRESET"

    reset_state: ClassVar[dict[str, Any]] = {
        "SPENTALLSOUL": True
    }
    opt_in = True
    reset_properties: ClassVar[dict[str, str]] = {
        "SPENTALLSOUL": "CANNOTREGAINSOUL=FALSE",
    }


class StartRespawnResetVariable(RCResetter, RCStateVariable):
    prefix = "$STARTRESPAWN"
    reset_state: ClassVar[dict[str, Any]] = {}
    opt_in = True
    reset_properties: ClassVar[dict[str, str]] = {
        "SPENTALLSOUL": "CANNOTREGAINSOUL=FALSE",
        "SPENTSOUL": "CANNOTREGAINSOUL=FALSE",
        "SPENTRESERVESOUL": "CANNOTREGAINSOUL=FALSE",
        "SPENTHP": "ANY",
    }
