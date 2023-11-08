from ...stardew_rule import Count, StardewRule, True_
from ...mods.mod_data import ModNames
from ... import options


def has_skull_cavern_elevator_to_floor(logic, floor: int) -> StardewRule:
    if logic.options.elevator_progression != options.ElevatorProgression.option_vanilla and \
            ModNames.skull_cavern_elevator in logic.options.mods:
        return logic.received("Progressive Skull Cavern Elevator", floor // 25)
    return True_()
