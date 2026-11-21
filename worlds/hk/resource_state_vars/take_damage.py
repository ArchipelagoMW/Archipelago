from collections.abc import Generator

from . import RCStateVariable, cs, rs
from .health_manager import HealthManager


class TakeDamageVariable(RCStateVariable):
    prefix = "$TAKEDAMAGE"
    damage: int
    hp_manager: HealthManager

    def parse_term(self, damage=1) -> None:
        self.damage = int(damage)
        self.hp_manager = HealthManager(HealthManager.prefix, self.player)
        pass

    @classmethod
    def try_match(cls, term: str) -> bool:
        return term.startswith(cls.prefix)

    @property
    def terms(self) -> list[str]:
        return self.hp_manager.terms

    def modify_state(self, state_blob: rs, item_state: cs) -> Generator[rs]:
        yield from self.hp_manager.take_damage(state_blob, item_state, self.damage)

    def can_exclude(self, options) -> bool:
        # can not actually be excluded because the damage skip option is checked in logic seperately
        return False
