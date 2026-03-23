from ...logic.base_logic import BaseLogicMixin, BaseLogic
from ...mods.mod_data import ModNames
from ...options import ElevatorProgression
from ...stardew_rule import StardewRule, True_


class ModElevatorLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.elevator = ModElevatorLogic(*args, **kwargs)


class ModElevatorLogic(BaseLogic):
    def has_skull_cavern_elevator_to_floor(self, floor: int) -> StardewRule:
        if self.options.elevator_progression != ElevatorProgression.option_vanilla and self.content.is_enabled(ModNames.skull_cavern_elevator):
            return self.logic.received("Progressive Skull Cavern Elevator", floor // 25)
        return True_()
