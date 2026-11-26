from ..options import HKOptions
from . import RCStateVariable, cs, rs, rs_set_value


class FlowerProviderVariable(RCStateVariable):
    prefix: str = "$FLOWERGET"

    # @classmethod
    # def get_terms(cls):
    #     return (term for term in ("VessleFragments",))

    def _modify_state(self, state_blob: rs, item_state: cs) -> tuple[bool, rs]:
        return True, rs_set_value(state_blob, "NOFLOWER", 0)

    @classmethod
    def try_match(cls, term: str) -> bool:
        return term == cls.prefix

    def can_exclude(self, options: HKOptions) -> bool:
        return False

    @property
    def terms(self) -> list[str]:
        return []
