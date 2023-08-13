from ...stardew_rule import Count, StardewRule, True_
from ...mods.mod_data import ModNames
from ... import options


def has_skull_cavern_elevator_to_floor(self, floor: int) -> StardewRule:
    if self.options[options.ElevatorProgression] != options.ElevatorProgression.option_vanilla and \
            ModNames.skull_cavern_elevator in self.options[options.Mods]:
        return self.received("Progressive Skull Cavern Elevator", floor // 25)
    return True_()
