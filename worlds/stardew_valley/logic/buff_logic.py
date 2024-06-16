from typing import Union

from .base_logic import BaseLogicMixin, BaseLogic
from .received_logic import ReceivedLogicMixin
from ..stardew_rule import StardewRule
from ..strings.ap_names.buff_names import Buff


class BuffLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buff = BuffLogic(*args, **kwargs)


class BuffLogic(BaseLogic[Union[ReceivedLogicMixin]]):
    def has_max_buffs(self) -> StardewRule:
        return self.has_max_speed() & self.has_max_luck()

    def has_max_speed(self) -> StardewRule:
        return self.logic.received(Buff.movement, self.options.movement_buff_number.value)

    def has_max_luck(self) -> StardewRule:
        return self.logic.received(Buff.luck, self.options.luck_buff_number.value)
