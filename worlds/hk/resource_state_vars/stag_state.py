from . import RCStateVariable, cs, rs, rs_set_value


class StagStateVariable(RCStateVariable):
    prefix = "$STAGSTATEMODIFIER"

    def parse_term(self) -> None:
        pass

    @classmethod
    def try_match(cls, term: str) -> bool:
        return term.startswith(cls.prefix)

    @property
    def terms(self) -> list[str]:
        return []

    def _modify_state(self, state_blob: rs, item_state: cs) -> tuple[bool, rs]:
        return True, rs_set_value(state_blob, "NOFLOWER", 1)

    def can_exclude(self, options) -> bool:
        return False
