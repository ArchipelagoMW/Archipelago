from collections.abc import Generator

from ..options import HKOptions
from . import RCStateVariable, cs, rs, rs_get_value, rs_add_value, rs_set_value
from .equip_charm import EquipCharmVariable, EquipResult, FragileCharmVariable
from .soul_manager import SoulManager


class ShadeStateVariable(RCStateVariable):
    prefix: str = "$SHADESKIP"
    health: int

    fragile_heart: FragileCharmVariable
    voidheart: EquipCharmVariable
    jonis: EquipCharmVariable
    sp_manager: SoulManager

    def __init__(self, *args):
        super().__init__(*args)
        self.fragile_heart = FragileCharmVariable("$EQUIPPEDCHARM[Fragile_Heart]", self.player)
        self.voidheart = EquipCharmVariable("$EQUIPPEDCHARM[Void_Heart]", self.player)
        self.jonis = EquipCharmVariable("$EQUIPPEDCHARM[Joni's_Blessing]", self.player)
        self.sp_manager = SoulManager(SoulManager.prefix, self.player)

    def parse_term(self, *args) -> None:
        if len(args) == 1:
            hits = args[0]
            self.health = int(hits[:-4])
        elif len(args) == 0:
            self.health = 1
        else:
            raise Exception(f"unknown {self.prefix} term, args: {args}")

    @classmethod
    def try_match(cls, term: str) -> bool:
        return term.startswith(cls.prefix)

    @property
    def terms(self) -> list[str]:
        if self.health > 1:
            return ["MASKSHARDS"]
        return []

    def modify_state(self, state_blob: rs, item_state: cs) -> Generator[rs]:
        shade_skipped, ret = self.do_shade_skip(state_blob, item_state)
        if shade_skipped:
            yield ret

    def do_shade_skip(self, state_blob: rs, item_state: cs) -> tuple[bool, rs]:
        if self.voidheart.is_equipped(state_blob):
            return False, state_blob
        if rs_get_value(state_blob, "CANNOTSHADESKIP") or rs_get_value(state_blob, "USEDSHADE"):
            return False, state_blob
        state_blob = self.voidheart.set_unequippable(state_blob)
        state_blob = rs_add_value(state_blob, "USEDSHADE", 1)

        test_one, state_blob = self.sp_manager.try_set_soul_limit(state_blob, item_state, 33, True)
        test_two, state_blob = self.sp_manager.try_set_soul_limit(state_blob, item_state, 0, False)
        if not test_one or not test_two:
            # edge case where using a shade skip is not safe to re-trace the path
            return False, state_blob
        requirement_checked, state_blob = self.check_health_requirement(state_blob, item_state)
        if not requirement_checked:
            # checking joni's and fragile heart
            return False, state_blob
        state_blob = rs_set_value(state_blob, "NOFLOWER", 1)  # just not worth it
        return True, state_blob

    def check_health_requirement(self, state_blob: rs, item_state: cs) -> tuple[bool, rs]:
        if self.health == 1:
            return True, state_blob

        if self.jonis.is_equipped(state_blob):
            return False, state_blob
        state_blob = self.jonis.set_unequippable(state_blob)

        hp = (item_state.count("MASKSHARDS", self.player) // 4) // 2
        if (
            hp >= self.health
            or (self.health == hp + 1 and self.fragile_heart.can_equip(state_blob, item_state) != EquipResult.NONE)
        ):
            state_blob = self.fragile_heart.break_charm(state_blob, item_state)
            return True, state_blob
        return False, state_blob

    def can_exclude(self, options: HKOptions) -> bool:
        return not bool(options.ShadeSkips)
